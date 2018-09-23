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
from physicalmachine import PhysicalMachine
from define import RANDOMRANGE


class PMManager:
    # print "===PMManager==="

    def __init__(self, total_dc, total_pm):
        self.pm_list= []
        self.total_dc = total_dc
        self.total_pm = total_pm
        for i in range(total_dc):
            for j in range(total_pm): 
                self.pm_list.append(PhysicalMachine(i,j))
        # print "pm_list=", self.__str__()

    def __str__(self):
        result = "PMList["
        for pm in self.pm_list:
            result += str(pm) + ","
        result += "]"
        return result

    def place_file(self, database_count, partition_id):
        count = 0
        print ("Random allocate%r DB, and split DB to %r groups" % (database_count, partition_id))
        for database_id in range(database_count):
            for p_id in range(partition_id):
                dc_id = self.random_position(RANDOMRANGE, self.total_dc)
                pm_id = self.random_position(RANDOMRANGE, self.total_pm)
                database = Database(database_id, partition_id)
                database.id = database_id
                database.partition_id = p_id
                database.dc_id = dc_id
                database.pm_id = pm_id
                pm = self.pm_list[pm_id]
                pm.dc_id = dc_id
                pm.id = pm_id
                pm.file_list.append(database)
                pm.disk = pm.disk+ database.file_size
                count += 1
        return self.pm_list

    def random_position(self, range, number):
        result = random.randint(0, range) % number
        return result


if __name__ == "__main__":
    total_dc = 1
    total_pm = 5
    pmmanager = PMManager(total_dc, total_pm)
    pmmanager.place_file(3,2)
    result = pmmanager.__str__()
    print (result)


