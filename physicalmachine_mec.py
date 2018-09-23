# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Physical Machine in the MEC
"""

#!/usr/bin/env python
# coding=utf-8


class PhysicalMachine_MEC:
    __count__ = 0
    def __init__(self, mec_id, id):
        self.mec_id = mec_id
        self.id = id
        self.replica_list = []
        self.file_list = []
        PhysicalMachine_MEC.__count__ += 1
        self.disk = 0
        self.net = 0

    def replica_to_str(self):
        result = ""
        for replica in self.replica_list:
            result += str(replica) + ","
        return result

    def __str__(self):
        result = "MEC_PM[MEC{}/PM{}- Net:{},Disk:{},VM:{}; DB:{}]".format(self.mec_id, self.id, self.net, self.disk, len(self.replica_list), len(self.file_list))
        return result


if __name__ == "__main__":
    mec_id = 1
    id = 1
    pm = PhysicalMachine_MEC(mec_id, id)
    print (pm)



