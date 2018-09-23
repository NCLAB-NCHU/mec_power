# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 Network Computing Lab
# All Rights Reserved.
#

#!/usr/bin/env python
# coding=utf-8
"""
Replication Model
"""
__version__ = "0.1"
__author__ = "maygy"

class Replica():
    __count__ = 0

    def __init__(self, id):
        self.__count__ += 1
        self.id = 0
        self.disk = 0
        self.net = 0
        self.dc_id = 0
        self.pm_id = 0
        self.database_id = 0
        self.partition_id = 0
        self.mec_id = 0

    def __str__(self):
        result = "VM[{}- Net:{} Disk:{} -Location:{}/{} - DB:{}/{}]".format(self.id, self.net, self.disk, self.dc_id, self.pm_id, self.database_id, self.partition_id)
        return result

    def __getitem__(self, attribute):
        result = self.value[attribute]
        return result


if __name__ == "__main__":
    id = 1
    replica = Replica(id)
    result = replica.__str__()
    print ("replica=",result)


