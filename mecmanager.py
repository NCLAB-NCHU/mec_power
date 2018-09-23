# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/local/bin/python
# -*- coding: utf-8 -*-

"""
MEC Manager
1. manage MECs
"""

from mec import MEC

class MECManager:

    def __init__(self, total_mec):
        self.mec_list = []
        for j in range(total_mec):
            self.mec_list.append(MEC(j))

    def __str__(self):
        result = "MEC["
        for mec in self.mec_list:
            result += str(mec) + ','
        result += "]"
        return result

if __name__ == "__main__":
    total_mec = 3
    mecmanager = MECManager(total_mec)
    result = mecmanager.__str__()
    print (result)
