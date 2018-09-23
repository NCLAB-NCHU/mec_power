# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

"""
SGW and PGW
"""


class SGW:
    delay_from_enodeb_to_sgw = 5  # ms
    delay_from_sgw_to_pgw = 18  # ms

    def __init__(self):
        pass


class PGW:
    # Reference: A self-configurable geo-replicated cloud storage system, 2014
    delaly_from_pgw_to_cloud_list = [6, 53, 6]  # ms

    def __init__(self):
        pass
