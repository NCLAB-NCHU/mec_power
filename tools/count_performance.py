import sys
from define import UPLOAD_SIZE, DOWNLOAD_SIZE, NUM_CELL
area = 0
hours = 144
algorithm = sys.argv[1]
tdelay = 0
tqos = 0
trate = 0
thot = 0
tcold = 0
tpower = 0
tpower_off = 0
tforward_load = 0
tforward_node = 0
hour_list = {}
item_list = ["delay", "qos", "hot", "cold", "power", "poweroff", "forward_load", "forward_count"]
for i in range(hours):
     hour_list[i] = {}
     for item in item_list:
        hour_list[i][item] = 0
for i in range(hours):
    if algorithm == "mec_power":
        fn = "./power09-result/result_%s_test_traffic_hour_%s" % (algorithm, str(i))
    elif algorithm == "cloud":
        fn = "./cloud-result/result_default_test_traffic_hour_%s" % (str(i))
    elif algorithm == "poweroff":
        fn = "./poweroff-result/result_mec_low_off_test_traffic_hour_%s" % (str(i))
    elif algorithm == "mec_vm":
        fn = "./vm-result/result_mec_vm_test_traffic_hour_%s" % (str(i)) 
    with open(fn, "r") as f:
        line = f.read().split(" ")
        #print line, len(line)
        hour = float(line[1])
        delay = float(line[3])
        qos = float(line[5])
        rate = float(line[7])
        hot = float(line[9])
        cold = float(line[11])
        power_off = float(line[15])
        power = float(line[13])
        forward_load = 0
        forward_count = 0
        if len(line) == 18:   
            forward_load = float(line[16].split("=")[-1])
            forward_count = float(line[17].split("=")[-1].strip("\n"))
        #print "hour=", hour,"delay=", delay, "qos=", qos, "rate=", rate, "hot", hot, "cold=", cold,"power=",power,  "poweroff=", power_off, "forwardload=", forward_load, "forwardcount=", forward_count
        time = i
        
        hour_list[time]["delay"] += delay
        hour_list[time]["qos"] += qos
        hour_list[time]["hot"] += hot
        hour_list[time]["cold"] += cold
        hour_list[time]["power"] += power
        hour_list[time]["poweroff"] += power_off
        hour_list[time]["forward_load"] += forward_load
        hour_list[time]["forward_count"] += forward_count

        tdelay += delay
        tqos += qos
        trate += rate
        thot += hot
        tcold += cold
        tpower += power
        tpower_off += power_off
        tforward_load += forward_load
        tforward_node += forward_count

for i in range(hours):
    print "========\n"
    for key, value in hour_list[i].items():
        print i, key, value
print "\n"
print "avg_delay=", tdelay/hour, "avg_qos=", tqos/hour, "avg_rate=", trate/hour, "avg_hot", thot/hour, "avg_cold=", tcold/hour, "avg_power=", tpower/hour, "avg_poweroff=",tpower_off/hour, "avg_forward_load=", tforward_load/hour, "avg_forward_node=", tforward_node/hour            
