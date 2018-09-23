# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/bin/env python
# coding=utf-8
"""
Trace Generator Model
"""

import os


class FileTraceGenerator():
    read_write_list = []
    cell_list = []
    ue_list = []
    location_list = []
    database_list = []
    partition_list = []
    size_list = []
    dc_id_list = []
    time_list = []    

    def __init__(self, trace_file):
        if os.path.exists(trace_file):
            try:
                with open(trace_file, "rU") as f:
                    for line in f:
                        line = line.split(" ")
                        if len(line) == 9:
                            self.read_write_list.append(line[0])
                            self.cell_list.append(int(line[1]))
                            self.ue_list.append(int(line[2]))
                            self.location_list.append(float(line[3])) # UE locations
                            self.size_list.append(int(line[4])) # packet size
                            self.database_list.append(int(line[5])) # DB ID
                            self.partition_list.append(int(line[6])) # DB partitions
                            self.dc_id_list.append(int(line[7])) # DC ID
                            self.time_list.append(int(line[8].strip("\n"))) # time interval
            except OSError as e:
                print ("fail to read tracefile: " + trace_file + " " + str(e.message))
        else:
            print (trace_file + " does not exist")

if __name__ == "__main__":
    file_path = "test_traffic"
    t = FileTraceGenerator(file_path)