# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/bin/env python
# coding=utf-8
"""
Simulation Manager
"""

import time
from manager import Manager
import sys
import json
from define import NUM_PM, NUM_REPLICA, NUM_DC, NUM_DATABASE, NUM_MEC, NUM_PM_MEC, NUM_CELL, HOURS

class Simulator:

    def __init__(self):
        self.result = []
        self.write = None

    def simulate_scenario(self, strategy):
        result = {}
        result['manager'] = m = Manager()
        m.set_dc(NUM_DC, NUM_PM)  #  Initialize CDC
        m.set_mec(NUM_CELL, NUM_PM_MEC)  #  Initialize MEC
        m.set_database(NUM_DATABASE)  # Initialize Database
        result = m.run(strategy["algorithm"], strategy["trace_file"], strategy["time"])  # show results
        return result

    def simulate_strategy(self, strategy):
        print ("\n")
        result = self.simulate_scenario(strategy)


if __name__ == "__main__":
    strategy = {}
    for j in range(HOURS):
        i = j + 0
        strategy["algorithm"] = sys.argv[1]  # default, mec_power, mec_off, and mec_vm
        strategy["trace_file"] = "./traffic/test_traffic_hour_%s" % str(i)
        strategy["time"] = i
        simulator = Simulator()
        simulator.simulate_strategy(strategy)
