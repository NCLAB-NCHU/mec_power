# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
Physical Machine: PM
"""

#!/usr/bin/env python
# coding=utf-8


class PhysicalMachine:
    __count__ = 0
    def __init__(self, dc_id, id):
        self.dc_id = dc_id
        self.id = id
        self.replica_list = []
        self.file_list = []
        self.__count__ += 1
        self.net = 0
        self.disk = 0

    def replica_to_str(self):
        result = ""
        for replica in self.replica_list:
            result += str(replica) + ","
        return result

    def __str__(self):
        result = "PM[DC{}/PM{}-Net{},Disk{},VM{}, DB{}]".format(self.dc_id, self.id,  self.net, self.disk, len(self.replica_list), len(self.file_list))
        return result


if __name__ == "__main__":
    dc_id = 0
    id = 10
    pm = PhysicalMachine(dc_id, id)
    result = pm
    print (result)



