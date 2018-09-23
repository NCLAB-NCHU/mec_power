# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

"""
MEC Model
"""

import math
from define import MEC_CPU_CYCLE, MEC_FREQ, MEC_d


class MEC:
    def __init__(self, id):
        self.mec_id = id
        self.ue_delay = 0  # ms
        self.delay_from_mec_to_enodeb = 0
        self.replica_list = []
        self.upload_request_list = []
        self.download_request_list = []
        self.net = 0  # KB
        self.total_request_list = []
        self.location_table = {}

    def delay_from_mec_to_mec(self, source_id, dest_id):
        s_id = source_id
        d_id = dest_id
        cross_delay = 2
        return cross_delay

    def process_delay(self, packet_size):
        # reference: 
        # Energy-efficient resource allocation for mobile-edge computation offloading, 2017
        # A stochastic model to investigate data center performance and qos in iaas cloud computing systems, 2014    
        process_time = (MEC_CPU_CYCLE*packet_size*8)/(MEC_FREQ*1.0)*1000  # ms
        process_time = process_time*math.pow((1+MEC_d), len(self.replica_list))
        return process_time
        


    def __str__(self):
        result = "MEC[{}-Network{:},Application:{}]".format(self.mec_id, self.net, len(self.replica_list))
        return result

if __name__ == "__main__":
    id = 1
    mec = MEC(id)
    cross_delay = mec.delay_from_mec_to_mec(1,100)
    print "cross_delay=", cross_delay
    result = mec.__str__()
    print "result=", result
