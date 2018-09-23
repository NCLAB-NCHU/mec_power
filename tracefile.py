# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 Network Computing Lab
# All Rights Reserved.
#

#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Traffic Model
"""
import sys
import os
import random
from define import CELL_RANGE, NUM_CELL, NUM_UE, NUM_DC, INTERVAL,NUM_DATABASE, REQUEST_SIZE, NUM_PARTITION, DOWNLOAD_BITRATE, DOWNLOAD_SIZE
from define import scale
import math
import numpy


def caculate_upload_download_rate():
    # reference: “Lte tdd frame,” http://niviuk.free.fr/lte tdd.php, 2017
    download_list = [2, 4, 6,6,7,8,3]
    upload_list = [6,4,2,3,2,1,5]
    rate_list = []
    for i in range(len(upload_list)):
        upload = upload_list[i]
        download = download_list[i]
        rate = upload/(download*1.0)
        rate_list.append(rate)
    return rate_list


def count_traffic_by_size(day):
    num_request_list = []
    # reference: “Performance and implications of ran caching in lte mobile networks: A real traffic analysis,” SECON, 2016
    traffic_list = {}
    traffic_list[0] = [3,3,5,2,1,1,2,7,11,13,14,13, 18,16,8,9,8,13,14,12,6,10, 36,21] # 1th day, traffic size: GB 
    if day > 1:
        traffic_list[1] = [13,3,2,3,4,10,11,8,13,18,14,    18,28,17,18,12,21,17,24,21,18,28,33,24] # 2th day, traffic size: GB
    if day > 2:
        traffic_list[2] = [14,7,6,1,10,11,22,21,20,20,    18,19,20,13,15,14,13,12,8,7,13,21,23,9] # 3th day, traffic size: GB
    if day > 3:
        traffic_list[3] = [3,1,2,2,2,6,4,12,11,13,10,14,  15,12,8,6,6,7,10,13,14,19,20,3] # 4th day, traffic size: GB
    if day > 4:
        traffic_list[4] = [0,0,0,0,0,1,2,5,7,8,9,10,21,   18,10,13,9,12,13,15,15,14,23,25] # 5th day, traffic size: GB
    if day > 5:
        traffic_list[5] = [16,6,3,1,0,1,3,7,9,8,13,13,   19,20,14,10,8,17,13,23,19,20,19,26] # 6th day, traffic size: GB
    if day > 7:
         traffic_list[6] = [13,2,1,2,2,1,3,5,10,6,7,8] # 7th day, traffic size: GB
    for day in traffic_list.keys():
        for traffic_size in traffic_list[day]:
            num_download = int((traffic_size*1000000000/(REQUEST_SIZE*1.0)*(NUM_CELL/scale*1.0)))
            num_request_list.append(num_download)
    return num_request_list

def possion_distribution(x):
    possion = numpy.random.poisson(25, x)
    return possion


def get_cell_id():
    cell_id = 0
    possion_list = possion_distribution(NUM_CELL - 1)
    for i in possion_list:
        x = random.randint(0, len(possion_list)-1)
        cell_id = possion_list[x]-1
        if cell_id < NUM_CELL:
            break
    if int(cell_id) >= int(NUM_CELL):
        cell_id = random.randint(0, NUM_CELL-1)
    return cell_id


def caculate_interval(num_request, num_req_per_sec, hours):
    time = 0
    if num_req_per_sec ==0:
        time = num_request
    else:
        time = int(num_request % INTERVAL)
    interval = hours*INTERVAL+time
    return interval



def gen_trace(num_request_list):
    print num_request_list
    count = 0
    interval = 0
    fn = "test_traffic"
    try:
        with open(fn, "w") as f:
            print ("write to file: " + fn)
            # get ratios for upload/download packets 
            rate_list = caculate_upload_download_rate()
            # generate upload packets by download packets 
            for num_download in num_request_list:
                index = random.randint(0, len(rate_list)-1)
                rate = rate_list[index]
                num_upload = int(rate*num_download)
                num_req = num_download + num_upload
                num_req_per_sec = int(num_req/INTERVAL)
                for num_request in range(num_req):
                    if num_request < num_upload:
                        request = "U"  # upload packets
                    else:
                        request = "D"  # download packets
                    # distribute traffic to cells by possion distribution
                    cell_id = get_cell_id()
                    # randomly generate UEs
                    ue_id = str(random.randint(0, NUM_UE-1))
                    dc_id = str(random.randint(0, NUM_DC-1))
                    location = random.uniform(0, CELL_RANGE-1)
                    database_id = random.randint(0, NUM_DATABASE-1) # 0: application A, 1: applicaiton B, 2: application C
                    partition_id = random.randint(0, NUM_PARTITION-1)
                    time = caculate_interval( num_request, num_req_per_sec, interval)
                    # format: Read/write, Cell ID, UE ID, UE Location, Request Size, Application ID,  DB Partition ID, DC ID, Interval
                    line = request +" " + str(cell_id) + " " + str(ue_id) + " " + str(location) + " " + str(REQUEST_SIZE) + " " + str(database_id)  + " " + str(partition_id) + " " + str(dc_id) + " " + str(time) + "\n"
                    f.write(line)
                    count += 1
                interval += 1
                print (interval, num_download, num_upload)

    except OSError as e:
        print ("fail to write file: " + fn)

if __name__ == "__main__":
    day = sys.argv[1]
    num_request_list = count_traffic_by_size(int(day))
    gen_trace(num_request_list)
