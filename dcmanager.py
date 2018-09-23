# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#


"""
Data Center Manager
1. manage all datacenters
"""

from datacenter import DataCenter


class DCManager:

    def __init__(self, total_dc):
        self.dc_list = []
        for j in range(total_dc):
            self.dc_list.append(DataCenter(j))

    def __str__(self):
        result = "DCList["
        for dc in self.dc_list:
            result += str(dc) + ','
        result += "]"
        return result


if __name__ == "__main__":
    total_dc = 3
    dcmanager = DCManager(total_dc)
    result = dcmanager.__str__()
    print result
