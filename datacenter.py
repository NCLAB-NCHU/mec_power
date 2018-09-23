# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

"""
Data Center Model
1. record VM replicas in a datacenter by self.replica_list
2. record application data in a datacenter by self.file_list
"""


class DataCenter:
    def __init__(self, id):
        self.dc_id = id
        self.internet_delay = 8  # ms
        self.net = 0
        self.replica_list = []
        self.file_list = []

    def __str__(self):
        result = "Datacenter[DC{}-VM:{}-DB:{}]".format(self.dc_id, len(self.replica_list), len(self.file_list))
        return result

if __name__ == "__main__":
    id = 1
    dc = DataCenter(id)
    result = dc.__str__()
    print "result=", result
