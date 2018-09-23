# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

"""
Enode Manager
"""
from enodeb import EnodeB


class EnodeBManager:

    def __init__(self, total_cell):
        self.cell_list = []
        for j in range(total_cell):
            self.cell_list.append(EnodeB(j))

    def __str__(self):
        result = "EnodeB:["
        for cell in self.cell_list:
            result += str(cell) + ','
        result += "]"
        return result


if __name__ == '__main__':
    enodebmanager = EnodeBManager(10)
    print enodebmanager.__str__()
