# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/bin/env python
# coding=utf-8
"""
Request Model
"""


class Request:

    def __init__(self):
        self.packet_type = ""
        self.dc_id = 0
        self.partition_id = 0
        self.disk = 0
        self.net = 0
        self.set_num = ""
        self.ue_id = 0
        self.cell_id = 0
        self.database_id = 0
        self.location = 0.0
        self.payload = 0
        self.rate = 0
