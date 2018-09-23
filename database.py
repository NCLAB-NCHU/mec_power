# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU  Network Computing Lab
# All Rights Reserved.
#

"""
Database Mode
1. store applications
2. each application is stored in a database
"""
from define import REQUEST_SIZE


class Database():
    __count__ = 0

    def __init__(self, id, partition_id):
        self.database_id = id
        self.partition_id = partition_id
        self.file_size = REQUEST_SIZE  # packet size
        self.dc_id = 0
        self.pm_id = 0

    def __str__(self):
        result = "Database[DB:{}/Partition{}-DC:{}/Server:{}]".format(self.database_id, self.partition_id, self.dc_id, self.pm_id)
        return result

if __name__ == "__main__":
    database = Database(1, 2)
    result = database.__str__()
    print result
