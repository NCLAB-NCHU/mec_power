# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/bin/env python
# coding=utf-8
"""
Replication Manager
1. import traffic
2. initial VM replicas
"""


from tracegen import FileTraceGenerator
from replication import Replica
from request import Request
from define import RANDOMRANGE, REQUEST_SIZE, NUM_PM_MEC, NUM_REPLICA
import random


class ReplicaManager:
    upload_request_list = [] # upload
    download_request_list = [] # download
    placed_replica_list = []
    placed_mec_replica_list = []
    total_replicas = 0
    total_request_count = 0
    time_list = []
    
    def __init__(self, trace_file):
        self.total_replica = NUM_REPLICA
        self.add_from_trace(trace_file)

    def add_from_trace(self, trace_file):
        print ("Import Traffic")
        tg = FileTraceGenerator(trace_file)
        read_write_list = tg.read_write_list
        dc_id_list = tg.dc_id_list # DC ID
        ue_list = tg.ue_list # UE ID
        cell_list = tg.cell_list # Cell ID
        size_list = tg.size_list # packet size
        location_list = tg.location_list # UE location
        database_list = tg.database_list # DB ID
        partition_list = tg.partition_list  # DB partitions
        time_list = tg.time_list # time intervals
        for i in range(len(read_write_list)):
            if "U" in read_write_list[i]:
                request = Request()
                request.packet_type = "upload" # packet type
                request.dc_id = dc_id_list[i]
                request.type = read_write_list[i]
                request.pm_id = random.randint(0, NUM_PM_MEC-1) # allocated MEC ID
                request.disk = size_list[i] # byte
                request.net = size_list[i] # byte
                request.database_id = database_list[i] # DB ID
                request.partition_id = partition_list[i] # DB partitions
                request.seq_num = i # packet seq
                request.ue_id = ue_list[i] # UE ID
                request.cell_id = cell_list[i] # Cell ID
                request.location = location_list[i] # UE location
                request.payload = size_list[i] # packet size
                request.time = time_list[i] # time interval
                self.upload_request_list.append(request)
            if "D" in read_write_list[i]:
                request = Request()
                request.packet_type = "download"
                request.dc_id = dc_id_list[i]
                request.pm_id = random.randint(0, NUM_PM_MEC-1)
                request.type = read_write_list[i]
                request.disk = size_list[i]
                request.net = size_list[i]
                request.seq_num = i
                request.database_id = database_list[i]
                request.partition_id = partition_list[i]
                request.ue_id = ue_list[i]
                request.cell_id = cell_list[i]
                request.location = location_list[i]
                request.payload = size_list[i]
                request.time = time_list[i]
                self.download_request_list.append(request)
            self.total_request_count += 1
        print ("Import %r packets" % self.total_request_count)

    def create_replica_dc(self, id, file, dc_id, pm_id):
        # create VM replicas in DC
        replica = Replica(id)
        replica.database_id = file.database_id
        replica.dc_id = dc_id
        replica.pm_id = pm_id
        self.placed_replica_list.append(replica)
        return replica

    def create_replica_mec(self, id, file, mec_id, pm_id):
        # create VM replicas in MEC
        replica = Replica(id)
        replica.database_id = file.database_id
        replica.mec_id = mec_id
        replica.pm_id = pm_id
        self.placed_mec_replica_list.append(replica)
        return replica

