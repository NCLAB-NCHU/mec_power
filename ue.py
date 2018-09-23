# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

#!/usr/bin/env python
# coding=utf-8
"""
UE Model
"""

import math
import random
from define import CELL_RANGE, TX_POWER

class UE:
    slave_list = []
    location = 0
    tx_power = TX_POWER # transfer power
    ue_id = 0
    rate = 0
    game_type = 0

    def __init__(self, id):
        self.ue_id = id  
        pass
  
