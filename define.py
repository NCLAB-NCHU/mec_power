# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# coding=utf-8

"""
define system parameters
"""
from tracegen import FileTraceGenerator


RANDOMRANGE = 1000000

###############################################
# Database
###############################################
NUM_DATABASE = 3  # Use 3 databases to store A, B, and C applications
NUM_PARTITION = 1  # The number of partition in each distributed database

###############################################
# Cloud Datacenter
###############################################
NUM_DC = 1  # Number of DC; the ubound number of CDC is 3
NUM_PM = 100  # Number of Servers in each dtacenter. 
# Reference: Is Server Consolidation Beneficial to MMORPG? A Case Study of World of Warcraft, 2010
# - In this paper, a datacenter has 100 servers

NUM_REPLICA = 3 # Each datacenter has 3 replicas of each application
REPLICA_CAPACITY = 90 # The number of users which each VM can serve. 
# Reference: Is Server Consolidation Beneficial to MMORPG? A Case Study of World of Warcraft, 2010
# - In this paper, a server can support 7500 users, a server has 83 VMs, 7500/83 = 90...

###############################################
#  Cell
###############################################
NUM_UE = 30  # The number of UE
NUM_CELL = 50  # The number of Cells
NUM_REPLICA_MEC = 1  # The number of VMs in each MEC server
CELL_RANGE = 500 # The Cell Range
BW = 15000000 # The bandwidth, unit: bytes per second
NOISE = -100 # noise power dBm
TX_POWER = 100  # smallcell=100mWatt
CHANNEL = 5  # The number of channels
# Reference: Efficient multi-user computation offloading for mobile-edge cloud computing, IEEE/ACM Transactions on Networking, 2016

##############################################
# MEC
##############################################
NUM_MEC = 1 # The number of MEC
NUM_PM_MEC = 1 # The number of servers in MEC
MEC_REPLICA_CAPACITY = 90 # Reference: Is Server Consolidation Beneficial to MMORPG? A Case Study of World of Warcraft, 2010
BUSY_POWER = 500 # Watt;  Reference: Mobile edge computing: The edge is the future, 2015
IDLE_POWER = 300 # Watt;  Reference: Mobile edge computing: The edge is the future, 2015 
SLEEP_POWER = 11.5 # Watt; Reference: Mobile edge computing: The edge is the future, 2015
PUE = 1.5
UP_BOUND = 1.0 # The ubound of CPU usage
LOW_BOUND = 0.2 # The lower limit of CPU usage  # Reference: The datacenter as a computer: An introduction to the design of warehouse-scale machines, 2013
UP_BOUND1 = 0.9 # The upper limit of CPU usagae
LOW_BOUND1 = 0.2 # 
MEC_CPU_CYCLE = 1500 # cycle per bit; Energy-efficient resource allocation for mobile-edge computation offloading, 2017
MEC_FREQ = 10000000000 # 10 GHZ; Reference: Efficient multi-user computation offloading for mobile-edge cloud computing, 2016 
MEC_d = 0.2 # VM degrade factor; Reference: A stochastic model to investigate data center performance and qos in iaas cloud computing systems, 2014
DATA = 28597
REQUEST_SIZE =28597 
# Reference: Performance and Implications of RAN Caching in LTE Mobile Networks: A Real Traffic Analysis, 2016
# - the total traffic size: 1776GB
# - the total packets: 62104921
# - each packets is 28597 bytes 

###############################################
# Applications
###############################################
TYPE_A_DELAY = 40 # QOS of A
TYPE_B_DELAY = 80 # OoS of B
TYPE_C_DELAY = 190 # QoS of C
MEC_LIST = ["A", "B"] # 放入MEC的應用
# Reference: Towards pervasive and mobile gaming with distributed cloud infrastructure, 2014


#############################################
# Traffic
#############################################
INTERVAL = 1 # collect traffic each hour 
file_path = "test_traffic"
HOURS = 144 # Hours
UPLOAD_SIZE = 150 # byte; On the performance of onlive thin client games, 2014
DOWNLOAD_SIZE = 1000 # byte; On the performance of onlive thin client games, 2014
UPLOAD_BITRATE = 100000 # bit per secondi, On the performance of onlive thin client games, 2014
DOWNLOAD_BITRATE = 5000000 # bit per second, On the performance of onlive thin client games, 2014
num_up = DATA/UPLOAD_SIZE
num_down = DATA/DOWNLOAD_SIZE
scale = 7 * 50000
