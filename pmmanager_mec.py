# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Physical Machine Manager
1. manage PM
"""


import random
from database import Database
from physicalmachine_mec import PhysicalMachine_MEC
from define import RANDOMRANGE


class PMManager_MEC:
    # print "===PMManager==="

    def __init__(self, total_mec, total_pm):
        self.pm_list= []
        self.total_mec = total_mec
        self.total_pm = total_pm
        for i in range(total_mec):
            for j in range(total_pm): 
                self.pm_list.append(PhysicalMachine_MEC(i,j))

    def __str__(self):
        result = "MECList["
        for pm in self.pm_list:
            result += str(pm) + ","
        result += "]"
        return result

    def random_position(self, range, number):
        result = random.randint(0, range) % number
        return result


if __name__ == "__main__":
    total_mec = 3
    total_pm = 1
    pmmanager = PMManager_MEC(total_mec, total_pm)
    result = pmmanager.__str__()
    print (result)
