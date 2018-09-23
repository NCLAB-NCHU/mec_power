# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

"""
Enode Mode
"""

import math
import random
from define import CELL_RANGE, NUM_UE, NOISE, BW, CHANNEL, INTERVAL
from ue import UE
from replicamanager import ReplicaManager


class EnodeB:
    delay_from_enodeb_to_enodeb = 2  # ms
    delay_from_enode_to_mec = 0  # ms
    enodeb_id = 0
    delay_from_enode_to_sgw = 5  # ms
    ue_list = []
    upload_ue_list = []
    download_ue_list = []
    read_request_list = []
    write_request_list = []
    total_request_list = []
    net = 0
    time = 0

    def __init__(self, id):
        self.enodeb_id = id

        for i in range(NUM_UE):
            ue = UE(i)
            self.ue_list.append(ue)

    def compute_rate(self, ue, total_active_ue):
        P = ue.tx_power  # mWatt
        noise = math.pow(10, NOISE/10)  # mWatt
        # need to check the gain again
        gain = math.pow(ue.location, -4)
        # compute other UEs gain
        other_P_gain = 0
        # compute SINR
        for i in range(0, total_active_ue - 1, 3):
            other_ue_location = random.uniform(0, CELL_RANGE)
            other_ue_gain = math.pow(other_ue_location, -4)
            other_P_gain += P*other_ue_gain
        SINR = P*gain/(noise + other_P_gain)
        x = 1 + SINR
        rate = BW * math.log(x if x > 0 else 1, 2)  # bits per second
        return rate

    def get_ue_request(self, replica_manager, time):
        self.time = time
        self.write_request_list = replica_manager.upload_request_list
        self.read_request_list = replica_manager.download_request_list
        self.upload_ue_list = []
        self.download_ue_list = []
        # get write requests
        for write_request in self.write_request_list:
            if write_request.cell_id == self.enodeb_id and int(write_request.time/INTERVAL) == self.time:
                self.upload_ue_list.append(write_request)
        #  get read requests
        for read_request in self.read_request_list:
            if read_request.cell_id == self.enodeb_id and int(read_request.time/INTERVAL) == self.time:
                self.download_ue_list.append(read_request)
        self.total_request_list = self.upload_ue_list + self.download_ue_list
        random.shuffle(self.total_request_list)  # packers are random order

    # UE randomly get  channel to transfer data
    def competition_order(self):
        order_list = []
        total_active_ue = 0
        for i in range(len(self.total_request_list)):
            available_channel = random.randint(1, CHANNEL)  # available channels are generate randomly
            for i in range(available_channel):
                order_list.append(available_channel)
            total_active_ue += available_channel
            if total_active_ue >= len(self.total_request_list):
                break
        return order_list

    def compute_rate_by_order(self):
        order_list = self.competition_order()
        for i in range(len(self.total_request_list)):
            total_active_ue = order_list[i]
            ue_id = self.total_request_list[i].ue_id
            ue = UE(ue_id)
            ue.location = self.total_request_list[i].location
            rate = self.compute_rate(ue, total_active_ue)
            self.total_request_list[i].rate = rate

    def compute_avg_rate(self):
        total_rate = 0
        for request in self.total_request_list:
            total_rate += request.rate
        num_request = 1
        if self.total_request_list != []:
            num_request = len(self.total_request_list)
        avg_rate = total_rate/num_request
        return avg_rate

if __name__ == '__main__':
    enodeb = EnodeB(8)
    trace_file = "test_traffic"
    replica_manager = ReplicaManager(trace_file)
