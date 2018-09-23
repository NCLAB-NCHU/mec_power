# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import os
import random
import json
from define import MEC_FREQ, UPLOAD_SIZE, DOWNLOAD_SIZE, NUM_PM_MEC, NUM_CELL, TYPE_A_DELAY, TYPE_B_DELAY, TYPE_C_DELAY, BUSY_POWER, IDLE_POWER,UP_BOUND, LOW_BOUND,MEC_REPLICA_CAPACITY, NUM_REPLICA_MEC, PUE, SLEEP_POWER, UP_BOUND1, LOW_BOUND1, num_up, num_down
from enodeb import EnodeB
from gateway import SGW
from gateway import PGW
from mec import MEC
from default import check_app_in_mec, count_interval


class MEC_POWER:
    
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
        self.power_off_count = 0
        self.total_power = 0
        self.cold_mec_list = []
        self.hot_mec_list = []
        self.available_mec_list = {}
        self.forward_list ={}
            #0: {2: 0}, 1: {2: 0}, 3: {2: 0}, 4: {2: 0}, 5: {7: 0}, 6: {7: 0}, 8: {9: 0}, 11: {10: 0}, 12: {14: 0}, 13: {14: 0}, 15: {14: 0}, 16: {14: 0}, 17: {14: 0}, 18: {14: 0}, 21: {14: 0}, 22: {14: 0}, 23: {14: 0}, 24: {14: 0}, 25: {14: 0}, 26: {37: 0}, 27: {37: 0}, 28: {37: 0}, 29: {37: 0}, 30: {37: 0}, 31: {37: 0}, 32: {37: 0}, 33: {37: 0}, 34: {37: 0}, 35: {37: 0}, 36: {37: 0}, 38: {39: 0}, 40: {39: 0}, 41: {39: 0}, 42: {44: 0}, 43: {44: 0}, 46: {45: 0}, 47: {45: 0}, 48: {45: 0}, 49: {45: 0}, 19: {14: 0.9332932098765434}, 20: {14: 6.820466049382717}}
        #{0: {1: 0}, 2: {1: 0}, 3: {1: 0}, 4: {6: 0}, 5: {6: 0}, 7: {6: 0}, 8: {6: 0}, 9: {6: 0}, 10: {6: 0}, 11: {6: 0}, 12: {6: 0}, 13: {19: 0}, 14: {19: 0}, 16: {19: 0}, 17: {19: 0}, 18: {19: 0}, 20: {19: 0}, 21: {19: 0}, 22: {19: 0}, 23: {26: 0}, 24: {26: 0}, 25: {26: 0}, 28: {27: 0}, 29: {30: 0}, 31: {30: 0}, 33: {32: 0}, 34: {32: 0}, 35: {37: 0}, 36: {37: 0}, 38: {37: 0}, 39: {37: 0}, 40: {37: 0}, 41: {45: 0}, 42: {45: 0}, 43: {45: 0}, 44: {45: 0}, 46: {45: 0}, 47: {45: 0}, 48: {45: 0}, 49: {45: 0}, 15: {19: 8.553759259259259}}
            #{0: {20: 0}, 1: {20: 0}, 2: {20: 0}, 3: {20: 0}, 4: {20: 0}, 5: {20: 0}, 6: {20: 0}, 7: {20: 0}, 8: {20: 0}, 9: {20: 0}, 10: {20: 0}, 13: {20: 0}, 14: {20: 0}, 15: {20: 0}, 16: {20: 0}, 17: {20: 0}, 18: {20: 0}, 21: {20: 0}, 22: {20: 0}, 23: {20: 0}, 24: {20: 0}, 11: {20: 1.1947438271604938}, 12: {20: 1.9376913580246915}, 19: {20: 1.1143024691358023}}


    def run(self, write_request_list, read_request_list, mec_manager, time):
        fn = "mec_power_forward_list"
        if os.path.exists(fn) and time != 0:
            with open(fn, "r") as f1:
                output = f1.readline()
                os.remove(fn)
                # print "XXX=", output 
                self.forward_list = eval(output)
        for cell in self.forward_list.keys():
            self.forward_list[cell] = {} 
        print "forward list(%s) at interval %s" % (str(self.forward_list), str(time -1))
        self.available_mec_list = self.forward_list         

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
        self.power_off_count = 0
        self.total_power = 0
        self.cold_mec_list = []
        self.hot_mec_list = []
        self.available_mec_list = []
        self.available_mec_capacity_list = {}
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
        avg_delay = self.mec_power_algorithm()#下方def mec_power_algorithm(self):
        if self.t_counter == 0:
            self.t_counter = 1
        result["avg_rate"] = self.rate/self.t_counter
        result["avg_delay"] = avg_delay
        result["qos_counter"] = float((self.qos_counter*1.0)/self.t_counter)
        result["avg_pm_bw"] = 0
        result["avg_hot_pm"] = self.hot_count
        result["avg_cold_pm"] = self.cold_count
        result["avg_poweroff_pm"] = self.power_off_count
        result["avg_power"] = self.total_power*1.0/NUM_CELL
        total_load = 0
        forward_count = 0
        for node_id, load in self.forward_list.items():
            for forward_id, forward_load in load.items():
                total_load += forward_load
                forward_count += 1
        if forward_count == 0:
            forward_count = 1 
        result["forward_load"] = total_load/forward_count      
        result["forward_node"] = forward_count
        return result

    def mec_power_algorithm(self):#上方avg_delay = self.mec_power_algorithm()
        avg_delay = 0
        self.forward_list = {}
        self.caculate_pm_request_new(self.forward_list)
        self.caculate_power()
        print"hot mec list=", self.hot_mec_list
        print"cold mec list= ", self.cold_mec_list
        print"available mec list = ", self.available_mec_list
        if not self.hot_mec_list and not self.cold_mec_list and not self.available_mec_list and self.time != 0:
            print ("failed to get hot/cold/available mec list")
            return 0
        if not self.cold_mec_list and not self.available_mec_list and self.time!=0:
            print("failed to get cold/available mec list")
            return 0
        # re-compute forwarding list
        if self.cold_mec_list:
            cold_forward_list = self.cold_mec_algorithm()
            #print "from cold_mec to available_mec=", cold_forward_list
            self.forward_list.update(cold_forward_list)
            self.caculate_pm_request_new(self.forward_list)
            self.caculate_power()
        if self.hot_mec_list:
            hot_forward_list = self.hot_mec_algorithm()
            #print "from hot_mec to available_mec", hot_forward_list
            self.forward_list.update(hot_forward_list)
            self.caculate_pm_request_new(self.forward_list)
            self.caculate_power()
        total_write_delay = self.write_request_delay(self.forward_list)
        total_read_delay = self.read_request_delay(self.forward_list)
        self.qos_counter = self.write_qos_counter + self.read_qos_counter
        if self.t_counter != 0:
            avg_delay = (total_write_delay+total_read_delay)/self.qos_counter
        else:
            avg_delay = total_write_delay + total_read_delay
        #self.caculate_pm_request_new(self.forward_list)
        print "forward_list=", self.forward_list
        if self.forward_list:
            fn = "mec_power_forward_list"
            with open(fn, "w") as f1:
                line = str(self.forward_list)
                f1.write(line)
        else:
            print "no forward_list..."
        self.caculate_power()
        return avg_delay

    def caculate_usage(self, cell_id):
        pm_id = 0
        usage = self.pm_usage_list[cell_id][pm_id]
        return usage

    def caculate_requests(self, cell_id):
        packets = 0
        for pm_id in self.pm_up_access_list[cell_id]:
            packets += self.pm_up_access_list[cell_id][pm_id]
            packets += self.pm_down_access_list[cell_id][pm_id]
        return packets

    def find_neast_mec(self, mec_id, degree):
        dest_list = []
        try:
            pm_id = 0
            for available_id in self.available_mec_list:
                usage = self.pm_usage_list[available_id][pm_id]
                if usage < UP_BOUND1 and usage >= 0:
                    dest = abs(available_id - mec_id) + usage*10
                    dest_list.append(dest)
                else:
                    self.available_mec_list.remove(available_id)
            min_dest = sorted(dest_list)[degree]
            index = dest_list.index(min_dest)
            #print mec_id, "dest_list=", dest_list, degree, index, self.available_mec_list
            available_id = self.available_mec_list[index]
        except Exception as e:
            print "no available mec_list:", str(e)
            available_id = -1
        return available_id

    def find_available_mec_list(self, rate):
        count = 0
        while True:
            if self.cold_mec_list or self.power_off_mec_list:
                available_mec_list = self.cold_mec_list + self.power_off_mec_list
                mec_index = random.randint(0, len(available_mec_list) - 1)
                count += 1
                mec_id = available_mec_list[mec_index]
                self.available_mec_list.append(mec_id)
                if mec_id in self.cold_mec_list:                        
                    self.cold_mec_list.remove(mec_id)
                if mec_id in self.power_off_mec_list:
                    self.power_off_mec_list.remove(mec_id)
                if count > int(rate*len(available_mec_list)):
                    break
            #else:
            #    mec_index = random.randint(0, len(self.power_off_mec_list) - 1)
            #    count += 1
            #    mec_id = self.power_off_mec_list[mec_index]
            #    self.available_mec_list.append(mec_id)
            #    self.power_off_mec_list.remove(mec_id)
            #    if count > int(rate*len(self.power_off_mec_list)):
            #        break

    def caculate_capacity(self, available_mec_id, capacity):
        usage = self.caculate_usage(available_mec_id)
        usage += capacity
        return usage


    def caculate_forward_list(self, mec_list, mec_type):
        total_capacity = 0
        total_available_usage = 0
        pm_id = 0

        print "available mec is not enough, add mec from cold mec"
        if mec_type == "cold":
            self.find_available_mec_list(0.1)
        else:
            self.find_available_mec_list(1.0)
        print "new available mec list=", self.available_mec_list
        forward_list = {}
        for mec_id in mec_list:
            forward_list[mec_id] = {}
            capacity = self.caculate_usage(mec_id)
            if mec_type != "cold":
                capacity = self.caculate_usage(mec_id)
                available_mec_id = self.find_neast_mec(mec_id, 0)
                print mec_id, capacity, available_mec_id
                if available_mec_id == -1:
                    continue
                usage = self.pm_usage_list[available_mec_id][pm_id]
                remaind_usage = UP_BOUND1 - usage
                print "mec_id=", mec_id, "find available_mec=", available_mec_id, usage
                if remaind_usage > 0 and usage < 1:
                    capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id, mec_type="hot")
                   if capacity >= UP_BOUND1:
                        available_mec_id = self.find_neast_mec(mec_id, 1)
                        if available_mec_id == -1:
                            continue
                        usage = self.pm_usage_list[available_mec_id][pm_id]
                        remaind_usage = UP_BOUND1 - usage
                        if remaind_usage > 0 and usage < 1:
                            capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id, mec_type="hot")
                            if capacity >= UP_BOUND1:
                                available_mec_id = self.find_neast_mec(mec_id, 2)
                                if available_mec_id == -1:
                                    continue
                                usage = self.pm_usage_list[available_mec_id][pm_id]
                                remaind_usage = UP_BOUND1 - usage
                                if remaind_usage > 0 and usage < 1:
                                    capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id, mec_type="hot")
                                    if capacity >= UP_BOUND1:
                                        available_mec_id = self.find_neast_mec(mec_id, 3)
                                        if available_mec_id == -1:
                                            continue
                                        usage = self.pm_usage_list[available_mec_id][pm_id]
                                        remaind_usage = UP_BOUND1 - usage
                                        if remaind_usage > 0 and usage < 1:
                                            capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id, mec_type="hot")
                        else:
                            available_mec_id = self.find_neast_mec(mec_id, 2)
                            if available_mec_id == -1:
                                continue
                            usage = self.pm_usage_list[available_mec_id][pm_id]
                            remaind_usage = UP_BOUND1 - usage
                            if remaind_usage > 0 and usage < 1:
                                capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id, mec_type="hot")
                                #print mec_id, "forwading 02 ", available_mec_id, usage, remaind_usage, capacity, "==>", self.pm_usage_list[available_mec_id][pm_id], self.pm_usage_list[mec_id][pm_id]
                                if capacity >= UP_BOUND1:
                                    available_mec_id = self.find_neast_mec(mec_id, 3)
                                    if available_mec_id == -1:
                                        continue
                                    usage = self.pm_usage_list[available_mec_id][pm_id]
                                    remaind_usage = UP_BOUND1 - usage
                                    if remaind_usage > 0 and usage < 1:
                                        capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id, mec_type="hot")
                                        #print mec_id, "forwading 04 ", available_mec_id, usage, remaind_usage, capacity, "==>", self.pm_usage_list[available_mec_id][pm_id], self.pm_usage_list[mec_id][pm_id]
                                    else:
                                        available_mec_id = self.find_neast_mec(mec_id, 4)
                                        if available_mec_id == -1:
                                            continue
                                        usage = self.pm_usage_list[available_mec_id][pm_id]
                                        remaind_usage = UP_BOUND1 - usage
                                        if remaind_usage > 0 and usage < 1:
                                            capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id, mec_type="hot")
                                            #print mec_id, "forwading 06 ", available_mec_id, usage, remaind_usage, capacity, "==>", self.pm_usage_list[available_mec_id][pm_id], self.pm_usage_list[mec_id][pm_id]    
                else:
                    available_mec_id = self.find_neast_mec(mec_id, 1)
                    if available_mec_id == -1:
                        continue
                    usage = self.pm_usage_list[available_mec_id][pm_id]
                    remaind_usage = UP_BOUND1 - usage
                    if remaind_usage > 0 and usage < 1:
                        capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id)
                        #print mec_id, "forwading 11 ", available_mec_id, usage, remaind_usage, capacity
                        if capacity > UP_BOUND1:
                            available_mec_id = self.find_neast_mec(mec_id, 2)
                            usage = self.pm_usage_list[available_mec_id][pm_id]
                            remaind_usage = UP_BOUND1 - usage
                            if remaind_usage > 0 and usage < 1:
                                capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id)
                                #print mec_id, "forwading 12 ",available_mec_id, usage, remaind_usage, capacity
                        else:
                            available_mec_id = self.find_neast_mec(mec_id, 3)
                            usage = self.pm_usage_list[available_mec_id][pm_id]
                            remaind_usage = UP_BOUND1 - usage
                            if remaind_usage > 0 and usage < 1:
                                capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id)
                                #print mec_id, "forwading 13 ",available_mec_id, usage, remaind_usage, capacity
            else:
                available_mec_id = self.find_neast_mec(mec_id, 0)
                if available_mec_id == -1:
                    continue
                usage = self.pm_usage_list[available_mec_id][pm_id]
                remaind_usage = UP_BOUND1 - usage
                if remaind_usage > 0 and usage < 1:
                    capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id)
                    #print mec_id, "forwading 21 ", available_mec_id, usage, remaind_usage, capacity, "==>", self.pm_usage_list[available_mec_id][pm_id], self.pm_usage_list[mec_id][pm_id]
                else:
                    available_mec_id = self.find_neast_mec(mec_id, 1)
                    usage = self.pm_usage_list[available_mec_id][pm_id]
                    remaind_usage = UP_BOUND1 - usage
                    if remaind_usage > 0 and usage < 1:
                        capacity, forward_list = self.caculate_forwarding(available_mec_id, capacity, forward_list, mec_id)
                        #print mec_id, "forwading 22 ", available_mec_id, usage, remaind_usage, capacity, "==>", self.pm_usage_list[available_mec_id][pm_id], self.pm_usage_list[mec_id][pm_id]
        for mec_id in mec_list:
            capacity = self.caculate_usage(mec_id)
            if mec_type == "cold":
                if capacity <= LOW_BOUND and capacity > 0:
                    print "still cold after forwarding= ",mec_id, capacity
            else:
                if capacity >= UP_BOUND:
                    print "still hot after forwarding=", mec_id, capacity
        return forward_list

    def caculate_forwarding(self, available_mec_id, capacity, forward_list, mec_id, mec_type="cold"):
        pm_id = 0
        usage = self.pm_usage_list[available_mec_id][pm_id]
        remaind_usage = UP_BOUND1 - usage
        #print "before===", mec_id, capacity, available_mec_id, usage, remaind_usage
        if capacity > usage:
            if mec_type == "cold":
                move_usage = remaind_usage
            else:
                move_capacity = capacity - UP_BOUND1
                if move_capacity - remaind_usage > 0:
                    move_usage = remaind_usage
                    
                else:
                    move_usage = move_capacity
        else:
            move_usage = capacity
            capacity = 0
        #print "after===", mec_id, capacity, available_mec_id, usage, remaind_usage
        self.pm_usage_list[available_mec_id][pm_id] += move_usage
        self.pm_usage_list[mec_id][pm_id] -= move_usage
        capacity = self.pm_usage_list[mec_id][pm_id]
        usage = self.pm_usage_list[available_mec_id][pm_id]
        if usage > UP_BOUND1:
            self.available_mec_list.remove(available_mec_id)
        forward_list[mec_id][available_mec_id] = move_usage        
        return capacity, forward_list
    

    def caculate_available_mec_capacity(self):
        available_mec_usage_list = {}
        for mec_id in self.available_mec_list:
            usage = self.caculate_usage(mec_id)
            self.available_mec_capacity_list[mec_id] = usage
        #print self.available_mec_capacity_list

    def cold_mec_algorithm(self):
        print ("cold MEC algorithm")
        forward_list = {}
        if not self.cold_mec_list:
            print ("no cold MEC")
            return forward_list

        BOUND = 0.2
        print "available_list=", self.available_mec_list
        if  not self.available_mec_list and self.cold_mec_list:
            self.find_available_mec_list(BOUND)

        print "before="
        self.caculate_available_mec_capacity() # renew
        forward_list = self.caculate_forward_list(self.cold_mec_list, mec_type="cold")
        print "after="
        self.caculate_available_mec_capacity()
        return forward_list

    def hot_mec_algorithm(self):
        print("HOT MECAlgorithm")
        forward_list = {}
        if not self.hot_mec_list:
            print("No HOT MEC")
            return forward_list

        print "available_list=", self.available_mec_list
        BOUND = 1.0 
        if (not self.available_mec_list and self.cold_mec_list) or len(self.available_mec_list) <= UP_BOUND*NUM_CELL:
            self.find_available_mec_list(BOUND)

        print "before="
        self.caculate_available_mec_capacity()
        forward_list = self.caculate_forward_list(self.hot_mec_list, mec_type="hot")
        print "after="
        self.caculate_available_mec_capacity()
        return forward_list

    def write_request_delay(self, forward_list):
        self.write_qos_counter = 0
        self.mw_counter = 0
        self.w_counter = 0
        total_delay = 0
        cloud_delay = 0
        pm_id = 0
        for write_request in self.write_request_list:
            if count_interval(write_request.time, self.time) == self.time:
                rate = write_request.rate
                if write_request.rate == 0:
                    rate = 1
                delay = 0
                up_cell_delay = 150*8/rate*1000
                down_cell_delay = 1000*8/rate*1000
                dc_id = write_request.dc_id
                mec_id = write_request.cell_id
                mec = self.mec_manager.mec_list[mec_id]
                dest_mec_id_list = forward_list.get(mec_id, {})
                process_delay = mec.process_delay(UPLOAD_SIZE)
                if write_request.database_id in [0, 1]:
                    if dest_mec_id_list:
                        for dest_mec_id in dest_mec_id_list.keys():
                            forward_delay = 2*MEC(mec_id).delay_from_mec_to_mec(mec_id, dest_mec_id)
                            delay += (up_cell_delay+down_cell_delay + forward_delay + 2*process_delay + 2*self.enodeb.delay_from_enode_to_sgw)# 到MEC的平均反應時間
                            delay = delay/len(dest_mec_id_list)
                                
                    else:
                        delay = (up_cell_delay+down_cell_delay + process_delay + 2*self.enodeb.delay_from_enode_to_sgw) # only access its own mec
                    self.mw_counter += 1*num_up
                else:
                    delay = (up_cell_delay+down_cell_delay + 2*(self.enodeb.delay_from_enode_to_sgw + self.sgw.delay_from_sgw_to_pgw + self.pgw.delaly_from_pgw_to_cloud_list[dc_id]) + cloud_delay) 
                delay_limit = self.get_qos(write_request.database_id)

                if float(delay) < float(delay_limit):
                    self.write_qos_counter += 1*num_up
                    total_delay += delay*num_up
                self.w_rate += rate*num_up
                self.w_counter += 1*num_up
                self.rate += rate*num_up
                self.t_counter += 1*num_up
        print "write=", self.write_qos_counter, self.mw_counter, self.w_counter, self.t_counter, self.write_qos_counter/(self.w_counter*1.0), total_delay/self.write_qos_counter
        return total_delay

    def read_request_delay(self, forward_list):
        self.r_counter = 0
        self.mr_counter = 0
        self.read_qos_counter = 0
        total_delay = 0
        pm_id = 0
        cloud_delay = 0
        for read_request in self.read_request_list:
            if count_interval(read_request.time, self.time) == self.time:
                rate = read_request.rate
                if read_request.rate == 0:
                    rate = 1
                delay = 0
                up_cell_delay = UPLOAD_SIZE * 8 / rate * 1000
                down_cell_delay = DOWNLOAD_SIZE * 8 / rate * 1000
                dc_id = read_request.dc_id
                mec_id = read_request.cell_id
                mec = self.mec_manager.mec_list[mec_id]
                dest_mec_id_list = forward_list.get(mec_id, {})
                process_delay = mec.process_delay(UPLOAD_SIZE)
                forward_delay = 0
                if read_request.database_id in [0, 1]:
                    if dest_mec_id_list:
                        for dest_mec_id in dest_mec_id_list:
                            forward_delay = 2*MEC(mec_id).delay_from_mec_to_mec(mec_id, dest_mec_id)
                            delay += (up_cell_delay+down_cell_delay + forward_delay +2*process_delay + 2*self.enodeb.delay_from_enode_to_sgw)
                            delay = delay/len(dest_mec_id_list)
                    else:
                        delay = (up_cell_delay+down_cell_delay + process_delay + 2*self.enodeb.delay_from_enode_to_sgw)
                    self.mr_counter += 1*num_down
                else:
                    delay = (up_cell_delay+down_cell_delay + 2*(self.enodeb.delay_from_enode_to_sgw + self.sgw.delay_from_sgw_to_pgw + self.pgw.delaly_from_pgw_to_cloud_list[dc_id]) + cloud_delay) # 到資料中心的平均反應時間
                delay_limit = self.get_qos(read_request.database_id)
                #print delay, read_request.database_id, up_cell_delay, down_cell_delay, process_delay, forward_delay, cloud_delay
                if float(delay) < float(delay_limit):
                    self.read_qos_counter += 1*num_down
                    total_delay += delay*num_down
                self.r_rate += rate*num_down
                self.r_counter += 1*num_down
                self.rate += rate*num_down
                self.t_counter += 1*num_down
        print "read=", self.read_qos_counter, self.mr_counter, self.r_counter, self.t_counter, self.read_qos_counter/(self.r_counter*1.0), total_delay/self.read_qos_counter
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

    def caculate_pm_request_new(self, forward_list):
        self.hot_count = 0
        self.cold_count = 0
        self.hot_mec_list = []
        self.cold_mec_list = []
        self.available_mec_list = []

        for mec_id in self.pm_up_access_list.keys(): # 每次都從薪計算
            for pm_id in self.pm_up_access_list[mec_id]:
                self.pm_up_access_list[mec_id][pm_id] = 0
                self.pm_down_access_list[mec_id][pm_id] = 0

        pm_id = 0
        for write_request in self.write_request_list:
            if count_interval(write_request.time, self.time) == self.time:
                mec_id = write_request.cell_id
                mec = self.mec_manager.mec_list[mec_id]
                if mec.mec_id == write_request.cell_id and write_request.database_id in [0, 1]:
                    self.pm_up_access_list[mec_id][pm_id] += 1 * num_up

        for read_request in self.read_request_list:       
            if count_interval(read_request.time, self.time) == self.time:
                mec_id = read_request.cell_id
                mec = self.mec_manager.mec_list[mec_id]    
                if mec.mec_id == read_request.cell_id and read_request.database_id in [0, 1]:
                    self.pm_down_access_list[mec_id][pm_id] += 1 * num_up

        total_num_up = MEC_FREQ/UPLOAD_SIZE/8
        total_num_down = MEC_FREQ/DOWNLOAD_SIZE/8                              
        #print forward_list
        for mec_id in forward_list.keys():
            for dest_mec_id in forward_list[mec_id].keys():
                if dest_mec_id != -1:  # 如果沒有，就原本的MEC處理
                    num_write_request = self.pm_up_access_list[mec_id][pm_id]/3600.0
                    num_read_request = self.pm_down_access_list[mec_id][pm_id]/3600.0
                    move_p = forward_list[mec_id][dest_mec_id]
                    original_p = (num_write_request * UPLOAD_SIZE * 8 + num_read_request * DOWNLOAD_SIZE * 8)/ (MEC_FREQ * 1.0)
                    # upload    
                    #print "source=", mec_id, p, move_p, "target=", dest_mec_id, original_p        
                    if move_p != original_p:
                        up_move_packets = total_num_up*move_p*3600/2
                        #print mec_id, total_num_up, move_p, up_move_packets, original_p, dest_mec_id
                        self.pm_up_access_list[dest_mec_id][pm_id] += up_move_packets
                        self.pm_up_access_list[mec_id][pm_id] -= up_move_packets
                        # download
                        down_move_packets = total_num_down*move_p*3600/2
                        self.pm_down_access_list[dest_mec_id][pm_id] += down_move_packets
                        self.pm_down_access_list[mec_id][pm_id] -= down_move_packets
                        #print "up=", up_move_packets, dest_mec_id, self.pm_up_access_list[dest_mec_id][pm_id], mec_id, self.pm_up_access_list[mec_id][pm_id]
                        #print "down=",down_move_packets, dest_mec_id, self.pm_down_access_list[dest_mec_id][pm_id], mec_id, self.pm_down_access_list[mec_id][pm_id]
                    else:
                        self.pm_up_access_list[dest_mec_id][pm_id] += self.pm_up_access_list[mec_id][pm_id]
                        self.pm_up_access_list[mec_id][pm_id] = 0
                        self.pm_down_access_list[dest_mec_id][pm_id] += self.pm_down_access_list[mec_id][pm_id]
                        self.pm_down_access_list[mec_id][pm_id] = 0

    def caculate_power(self):
        # POWER = IDLE + (PEAK-IDLE) * U + (PUE-1)*PEAK
        #  參考 Is Server Consolidation Beneficial to MMORPG? A Case Study of World of Warcraft, 2010
        # 參考Power Provisioning for a Warehouse-sized Computer, 2007
        self.hot_mec_list = []
        self.cold_mec_list = []
        self.power_off_mec_list = []
        self.available_mec_list = []
        self.hot_count = 0
        self.cold_count = 0
        self.power_off_count = 0
        self.total_power = 0
        total_usage = 0    
        self.available_mec_list = []
        for cell_id in self.pm_up_access_list:
            for pm_id in self.pm_up_access_list[cell_id]:
                power = 0
                num_write_request = self.pm_up_access_list[cell_id][pm_id]/3600.0
                num_read_request = self.pm_down_access_list[cell_id][pm_id]/3600.0
                usage = (num_write_request * UPLOAD_SIZE * 8 + num_read_request * DOWNLOAD_SIZE * 8)/ (MEC_FREQ * 1.0)
                if usage != 0:
                    power = IDLE_POWER + (BUSY_POWER - IDLE_POWER) * usage + (PUE-1)*BUSY_POWER
                else:
                    power = SLEEP_POWER
                self.pm_power_list[cell_id][pm_id] = power
                self.pm_usage_list[cell_id][pm_id] = usage

                self.total_power += power
                total_usage += usage
                if usage >= UP_BOUND:
                    #print cell_id, usage
                    self.hot_count += 1
                    self.hot_mec_list.append(cell_id)
                elif usage <= LOW_BOUND and usage != 0:
                    #print cell_id, usage
                    self.cold_count += 1
                    self.cold_mec_list.append(cell_id)
                elif usage == 0:
                    self.power_off_count += 1
                    self.power_off_mec_list.append(cell_id)
                elif usage < UP_BOUND and usage > LOW_BOUND:
                    self.available_mec_list.append(cell_id)
        print "hot=", self.hot_mec_list, len(self.hot_mec_list)
        print "cold=", self.cold_mec_list, len(self.cold_mec_list)
        print "poweroff=", self.power_off_mec_list, len(self.power_off_mec_list)
        print "usage=", total_usage/(NUM_CELL*1.0)


