# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright (c) 2017-2018 NCHU Network Computing Lab
# All Rights Reserved.
#

"""
Manager Model
1. Initial environment
2. Run algorithms
"""

from dcmanager import DCManager
from pmmanager import PMManager
from mecmanager import MECManager
from pmmanager_mec import PMManager_MEC
from define import RANDOMRANGE, NUM_REPLICA_MEC, NUM_REPLICA, HOURS, NUM_PARTITION, MEC_LIST
from replicamanager import ReplicaManager
from default import Default,check_app_in_mec
from enodebmanager import EnodeBManager
from mec_power import MEC_POWER
from mec_low_off import MEC_LOW_OFF
from mec_vm import MEC_VM


class Manager:
    placement = []
    leader_list = []
    total_dc = 0
    total_pm = 0
    total_mec = 0
    total_dc_replicas = 0
    total_mec_replicas = 0
    database_count = 0
    strategy = None
    replica_manager = None
    pm_manager = None
    dc_manager = None
    pm_manager_mec = None
    mec_manager = None
    enodeb_manager = None
    strategy_name = ""
    avg_rate_list = []
    write_request_list = []
    read_request_list = []
    pm_list = []

    def __init__(self):
        pass

    def set_dc(self, total_dc, total_pm):
        self.total_pm = total_pm
        self.total_dc = total_dc
        self.dc_manager = DCManager(total_dc)  # generate datacenter by total_dc         
        self.pm_manager = PMManager(total_dc, total_pm)  # generate servers for each datacenter

    def set_mec(self, total_mec, total_pm_mec):
        self.total_pm_mec = total_pm_mec
        self.total_mec = total_mec
        self.enodeb_manager = EnodeBManager(total_mec)  # place BS by total_mec
        self.mec_manager = MECManager(total_mec)  # place MEC for each BS
        self.pm_manager_mec = PMManager_MEC(total_mec, total_pm_mec)  # place MEC servers for each MEC

    def set_database(self, database_count):
        # applications are stored in distributed databases
        # each database is splited serveral partitions  
        self.pm_list = self.pm_manager.place_file(database_count, NUM_PARTITION)  # place applications to each server in the cloud
        self.database_count = database_count
        # datacenters record stored applications 
        for dc in self.dc_manager.dc_list:      
            for pm in self.pm_manager.pm_list:
                if dc.dc_id == pm.dc_id:               
                    for file in pm.file_list:
                        dc.file_list.append(file)

    def set_replica(self, trace_file):
        # generate VM replicas by traffic 
        self.replica_manager = ReplicaManager(trace_file)
        # place VM rerplicas in the cloud datacenters
        self.initial_create_replica_dc(NUM_REPLICA)
        # place VM replicas in the MEC
        self.initial_create_replica_mec(NUM_REPLICA_MEC)
        self.write_request_list = self.replica_manager.upload_request_list
        self.read_request_list = self.replica_manager.download_request_list

    
    def initial_create_replica_dc(self, total_dc_replicas):
        id = 0
        for pm in self.pm_list:
            for file in pm.file_list:
                for i in range(total_dc_replicas):
                    # ranndomly place VM replicas in the cloud datacenters
                    dc_id = self.pm_manager.random_position(RANDOMRANGE, self.total_dc)
                    pm_id = self.pm_manager.random_position(RANDOMRANGE, self.total_pm)
                    replica = self.replica_manager.create_replica_dc(id, file, dc_id, pm_id)
                    self.total_dc_replicas = self.total_dc_replicas + 1
                    pm.disk = pm.disk + replica.disk
                    pm.net = pm.net + replica.net
                    pm.replica_list.append(replica)
                    pm.dc_id = dc_id
                    dc = self.dc_manager.dc_list[dc_id]
                    dc.replica_list.append(replica)
                    id = id + 1

    def initial_create_replica_mec(self, total_mec_replicas):
        id = 0
        for pm in self.pm_list:  
            for file in pm.file_list:
                # only place applications of MEC_LIST in the MEC
                if check_app_in_mec(file.database_id) in MEC_LIST:
                    for i in range(total_mec_replicas):
                        for mec in self.mec_manager.mec_list:
                            mec_id = mec.mec_id
                            # ranndomly place VM replicas in the MEC 
                            pm_id = self.pm_manager_mec.random_position(RANDOMRANGE, self.total_pm_mec)
                            replica = self.replica_manager.create_replica_mec(i, file, mec_id, pm_id)
                            self.total_mec_replicas = self.total_mec_replicas + 1
                            for mec_pm in self.pm_manager_mec.pm_list:
                                if mec_pm.mec_id == mec_id and mec_pm.id == pm_id:
                                    mec_pm.disk += replica.disk
                                    mec_pm.net += replica.net
                                    mec_pm.replica_list.append(replica)
                            mec.replica_list.append(replica)
                            id = id + 1
    
    def set_ue_in_cells(self, time):
        # generate UEs
        self.avg_rate_list = []
        for enodeb in self.enodeb_manager.cell_list:
            enodeb.get_ue_request(self.replica_manager, time)
            enodeb.compute_rate_by_order()
            avg_rate = enodeb.compute_avg_rate()
            self.avg_rate_list.append(avg_rate)
            for mec in self.mec_manager.mec_list:
                if enodeb.enodeb_id == mec.mec_id:
                    mec.write_request_list = enodeb.upload_ue_list
                    mec.read_request_list = enodeb.download_ue_list
    
    def set_strategy(self, strategy):
        if "default" in strategy: # MEC
            default = Default()
            self.strategy_name = strategy
            self.strategy = default
            self.strategy.replica_manager = self.replica_manager
            self.strategy.pm_manager = self.pm_manager
            self.strategy.dc_manager = self.dc_manager
        if "mec_power" in strategy: # COHM
            mec_power = MEC_POWER()
            self.strategy_name = strategy
            self.strategy = mec_power
            self.strategy.replica_manager = self.replica_manager
            self.strategy.pm_manager = self.pm_manager
            self.strategy.dc_manager = self.dc_manager
        if "mec_low_off" in strategy: # Sleep
            mec_low_off = MEC_LOW_OFF()
            self.strategy_name = strategy
            self.strategy = mec_low_off
            self.strategy.replica_manager = self.replica_manager
            self.strategy.pm_manager = self.pm_manager
            self.strategy.dc_manager = self.dc_manager
        if "mec_vm" in strategy: # Migration
            mec_vm = MEC_VM()
            self.strategy_name = strategy
            self.strategy = mec_vm
            self.strategy.replica_manager = self.replica_manager
            self.strategy.pm_manager = self.pm_manager
            self.strategy.dc_manager = self.dc_manager

    def run(self, strategy_name, trace_file, time):
        self.set_replica(trace_file)  
        self.set_strategy(strategy_name)
        print ("Algorithm= %r" % strategy_name)
        print ("Traffic=%s" % trace_file)
        self.strategy_name = strategy_name
        total_time = HOURS
        result = {}
        result["avg_delay"] = []
        result["qos_counter"] = []
        result["avg_pm_bw"] = []
        result["avg_hot_pm"] = []
        result["avg_cold_pm"] = []
        result["avg_rate"] = []
        result["avg_power"] = []
        result["forward_load"] = []
        self.set_ue_in_cells(time)
        output = self.strategy.run(self.write_request_list, self.read_request_list, self.mec_manager, time)
        result["avg_delay"].append(output["avg_delay"])
        result["qos_counter"].append(output["qos_counter"])
        result["avg_hot_pm"].append(output["avg_hot_pm"])
        result["avg_cold_pm"].append(output["avg_cold_pm"])
        result["avg_rate"].append(output["avg_rate"])
        result["avg_power"].append(output["avg_power"])
        if output.get("forward_load"):
            result["forward_load"].append(output.get("forward_load"))
        line = "%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" % ("hour=", time, "response_time(ms)=", output["avg_delay"], "qos_rate=", output["qos_counter"], "rate(Mbps)=", output["avg_rate"]/1000000, "hot_pm=", output["avg_hot_pm"], "cold_pm=", output["avg_cold_pm"], "power=", output["avg_power"], "poweroff_pm=", output["avg_poweroff_pm"])
        if output.get("forward_load"):
            line += " forward_load=%s forward_node=%s" % (str(output.get("forward_load")), str(output.get("forward_node")))
        print line
        # write simmulation results to ./result/
        fn = "./result/result_%s_%s" % (strategy_name, trace_file.split("/")[2])
        with open(fn, "w") as f1:
            f1.write(line + "\n")
        return result
