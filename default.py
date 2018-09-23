# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

"""
Cloud  Algorithm:
1. do not put VM in MEC
2. BS forward requests to the remote cloud
"""

import math
import random
from define import RANDOMRANGE, NUM_PM_MEC, NUM_CELL, TYPE_A_DELAY, TYPE_B_DELAY, TYPE_C_DELAY
from define import REQUEST_SIZE, INTERVAL, BUSY_POWER, IDLE_POWER, SLEEP_POWER, UP_BOUND, LOW_BOUND,
from define import MEC_REPLICA_CAPACITY, NUM_REPLICA_MEC, PUE, MEC_CPU_CYCLE, MEC_FREQ, UPLOAD_SIZE, DOWNLOAD_SIZE, UPLOAD_BITRATE, DOWNLOAD_BITRATE, DATA, num_up, num_down
from enodeb import EnodeB
from gateway import SGW
from gateway import PGW
from define import NUM_DC, NUM_PM


def check_app_in_mec(database_id):
    app_type = "A"
    if database_id == 1:
        app_type = "B"
    elif database_id == 2:
        app_type = "C"
    return app_type


def count_interval(request_time, current_time):
    time = int(request_time/INTERVAL)
    return time


class Default:

    def __init__(self):
        self.write_request_list = []
        self.read_request_list = []
        self.replica_manager = None
        self.pm_manager = None
        self.dc_manager = None
        self.mec_manager = None
        self.enodeb = EnodeB(0)
        self.sgw = SGW()
        self.pgw = PGW()
        self.qos_counter = 0
        self.write_qos_counter = 0
        self.read_qos_counter = 0
        self.pm_up_access_list = {}
        self.pm_down_access_list = {}
        self.pm_power_list = {}
        self.pm_usage_list = {}
        self.time = 0
        self.rate = 0
        self.w_rate = 0
        self.r_rate = 0
        self.w_counter = 0
        self.r_counter = 0
        self.t_counter = 0
        self.hot_count = 0
        self.cold_count = 0
        self.total_power = 0
        self.power_off_count = 0

    def run(self, write_request_list, read_request_list, mec_manager, time):
        self.time = time
        result = {}
        self.mec_manager = mec_manager
        self.qos_counter = 0
        self.write_qos_counter = 0
        self.read_qos_counter = 0
        self.w_counter = 0
        self.mw_counter = 0
        self.mr_counter = 0
        self.w_rate = 0
        self.r_rate = 0
        self.w_counter = 0
        self.r_counter = 0
        self.t_counter = 0
        self.rate = 0
        self.hot_count = 0
        self.cold_count = 0
        self.total_power = 0
        for cell_id in range(NUM_CELL):
            self.pm_up_access_list[cell_id] = {}
            self.pm_down_access_list[cell_id] = {}
            self.pm_power_list[cell_id] = {}
            self.pm_usage_list[cell_id] = {}
            for pm_id in range(NUM_PM_MEC):
                self.pm_up_access_list[cell_id][pm_id] = 0
                self.pm_down_access_list[cell_id][pm_id] = 0
                self.pm_power_list[cell_id][pm_id] = 0
                self.pm_usage_list[cell_id][pm_id] = 0
        self.write_request_list = write_request_list
        self.read_request_list = read_request_list
        avg_delay = self.default_algorithm()
        if self.t_counter == 0:
            self.t_counter = 1
        result["avg_rate"] = self.rate/self.t_counter
        result["avg_delay"] = avg_delay
        result["qos_counter"] = float((self.qos_counter*1.0)/(self.t_counter*1.0))
        result["avg_pm_bw"] = 0
        result["avg_hot_pm"] = self.hot_count
        result["avg_cold_pm"] = self.cold_count
        result["avg_power"] = self.total_power*1.0/NUM_CELL
        result["avg_poweroff_pm"] = self.power_off_count
        return result

    def default_algorithm(self):
        self.caculate_pm_request()
        self.caculate_power()
        total_write_delay = self.write_request_delay()
        total_read_delay = self.read_request_delay()
        self.qos_counter = self.write_qos_counter + self.read_qos_counter
        if self.t_counter != 0:
            avg_delay = (total_write_delay+total_read_delay)/self.qos_counter
        else:
            avg_delay = total_write_delay + total_read_delay
        self.caculate_pm_request()
        self.caculate_power()
        return avg_delay

    def write_request_delay(self):
        total_delay = 0
        cloud_delay = 0  # inter-datacenter transfer delay
        for write_request in self.write_request_list:
            if count_interval(write_request.time, self.time) == self.time:
                dc_id = write_request.dc_id
                mec_id = write_request.cell_id
                mec = self.mec_manager.mec_list[mec_id]
                rate = write_request.rate
                if write_request.rate == 0:
                    rate = 1

                up_cell_delay = UPLOAD_SIZE * 8 / rate * 1000
                down_cell_delay = DOWNLOAD_SIZE * 8 / rate * 1000
                process_delay = mec.process_delay(UPLOAD_SIZE)

                flag = False
                pm_id = 0
                delay = 0
                if write_request.database_id in [0, 1]:
                        flag = True
                if flag is True:
                    delay = (up_cell_delay+down_cell_delay + process_delay + 2*self.enodeb.delay_from_enode_to_sgw)
                    self.mw_counter += 1*num_up
                else:
                    delay = up_cell_delay+down_cell_delay + 2*(self.enodeb.delay_from_enode_to_sgw + self.sgw.delay_from_sgw_to_pgw + self.pgw.delaly_from_pgw_to_cloud_list[dc_id]) + cloud_delay
                delay_limit = self.get_qos(write_request.database_id)
                if float(delay) < float(delay_limit):
                    self.write_qos_counter += 1*num_up
                    total_delay += delay*num_up

                self.w_rate += rate*num_up
                self.w_counter += 1*num_up
                self.rate += rate*num_up
                self.t_counter += 1*num_up
        print self.w_counter, self.write_qos_counter, self.t_counter, self.mw_counter
        if self.w_counter != 0:
            print "write qos=", self.write_qos_counter / (self.w_counter * 1.0)
        return total_delay

    def read_request_delay(self):
        total_delay = 0
        cloud_delay = 0
        for read_request in self.read_request_list:
            if count_interval(read_request.time, self.time) == self.time:
                dc_id = read_request.dc_id
                mec_id = read_request.cell_id
                mec = self.mec_manager.mec_list[mec_id]
                rate = read_request.rate
                if read_request.rate == 0:
                    rate = 1
                delay = 0
                up_cell_delay = UPLOAD_SIZE * 8 / rate * 1000
                down_cell_delay = DOWNLOAD_SIZE * 8 / rate * 1000
                process_delay = mec.process_delay(UPLOAD_SIZE)
                flag = False
                if read_request.database_id in [0, 1]:
                        flag = True
                if flag:
                    delay = (up_cell_delay+down_cell_delay + process_delay + 2*self.enodeb.delay_from_enode_to_sgw)
                    self.mr_counter += 1*num_down
                else:
                    delay = up_cell_delay+down_cell_delay + 2*(self.enodeb.delay_from_enode_to_sgw + self.sgw.delay_from_sgw_to_pgw + self.pgw.delaly_from_pgw_to_cloud_list[dc_id]) + cloud_delay
                delay_limit = self.get_qos(read_request.database_id)
                if float(delay) < float(delay_limit):
                    self.read_qos_counter += 1*num_down
                    total_delay += delay*num_down
                self.r_rate += rate*num_down
                self.r_counter += 1*num_down
                self.rate += rate*num_down
                self.t_counter += 1*num_down
        print self.r_counter, self.read_qos_counter, self.t_counter, self.mr_counter
        if self.r_counter != 0:
            print "read qos=", self.read_qos_counter/(self.r_counter*1.0)
        return total_delay

    def get_qos(self, database_id):
        delay_limit = 0
        if database_id == 0:
            delay_limit = TYPE_A_DELAY
        elif database_id == 1:
            delay_limit = TYPE_B_DELAY
        elif database_id == 2:
            delay_limit = TYPE_C_DELAY
        return delay_limit

    def caculate_pm_request(self):
        for write_request in self.write_request_list:
            if count_interval(write_request.time, self.time) == self.time:
                mec_id = write_request.cell_id
                mec = self.mec_manager.mec_list[mec_id]
                if mec.mec_id == write_request.cell_id:
                    pm_id = 0
                    write_flag = False
                    for replica in mec.replica_list:
                        if replica.database_id == write_request.database_id and replica.partition_id == write_request.partition_id:
                            write_flag = True
                            pm_id = replica.pm_id
                    if write_flag is True:
                        self.pm_up_access_list[mec_id][pm_id] += 1 * num_up
        for read_request in self.read_request_list:
            if count_interval(read_request.time, self.time) == self.time:
                mec_id = read_request.cell_id
                mec = self.mec_manager.mec_list[mec_id]
                if mec.mec_id == read_request.cell_id:
                    pm_id = 0
                    read_flag = False
                    for replica in mec.replica_list:
                        if replica.database_id == read_request.database_id and replica.partition_id == read_request.partition_id:
                            read_flag = True
                            pm_id = replica.pm_id
                    if read_flag is True:
                        self.pm_down_access_list[mec_id][pm_id] += 1*num_down

    def caculate_power(self):
        # POWER = IDLE + (PEAK-IDLE) * U + (PUE-1)*PEAK
        #  Reference:  Is Server Consolidation Beneficial to MMORPG? A Case Study of World of Warcraft, 2010
        # Reference: Power Provisioning for a Warehouse-sized Computer, 2007
        hot_mec_list = []
        cold_mec_list = []
        power_off_mec_list = []
        self.hot_count = 0
        self.cold_count = 0
        self.power_off_count = 0
        self.total_power = 0
        total_usage = 0
        for cell_id in self.pm_up_access_list.keys():
            for pm_id in self.pm_up_access_list[cell_id]:
                num_write_request = self.pm_up_access_list[cell_id][pm_id] / 3600.0
                num_read_request = self.pm_down_access_list[cell_id][pm_id] / 3600.0
                usage = (num_write_request * UPLOAD_SIZE * 8 + num_read_request * DOWNLOAD_SIZE * 8) / (MEC_FREQ * 1.0)
                total_usage += usage
                power = IDLE_POWER + (BUSY_POWER - IDLE_POWER) * usage + (PUE-1) * BUSY_POWER
                self.pm_usage_list[cell_id][pm_id] += usage
                self.pm_power_list[cell_id][pm_id] += power

                self.total_power += power
                if usage >= UP_BOUND:
                    self.hot_count += 1
                    hot_mec_list.append(cell_id)
                elif usage <= LOW_BOUND:
                    self.cold_count += 1
                    cold_mec_list.append(cell_id)
                elif usage == 0:
                    self.power_off_count += 0
        print "hot=", hot_mec_list, len(hot_mec_list)
        print "cold=", cold_mec_list, len(cold_mec_list)
        print "poweroff=", power_off_mec_list, len(power_off_mec_list)
        print "usage=", total_usage/(NUM_CELL*1.0)
