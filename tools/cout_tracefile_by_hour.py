from define import UPLOAD_SIZE, DOWNLOAD_SIZE, NUM_CELL, DATA, num_up, num_down

size_list = []
upacket_list = []
dpacket_list = []
Hour = 144
size = 1000000
time = 3600
for hour in range (Hour):
    size_list.append(0)
    upacket_list.append(0)
    dpacket_list.append(0)
for i in range (Hour):
    hour = i
    trace_file = "./traffic/test_traffic_hour_%s" % str(hour)
    with open(trace_file, "rU") as f:
        for line in f:
            line = line.split(" ")
            if len(line) == 9:
                if line[0] == "U":
                    size_list[hour] += UPLOAD_SIZE*num_up
                    upacket_list[hour] += 1*num_up*UPLOAD_SIZE
                else:
                    size_list[hour] += DOWNLOAD_SIZE*num_down
                    dpacket_list[hour] += 1*num_down*DOWNLOAD_SIZE
for hour in range(Hour):
    print "hour=", hour, "Size(Mbps)=",size_list[hour]*8/size/NUM_CELL/3600.0, "UPLOAD_size(Mbps)=", upacket_list[hour]*8/size/NUM_CELL/3600.0, "Download_size(Mbps)=", dpacket_list[hour]*8/size/NUM_CELL/3600.0
