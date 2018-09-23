from define import UPLOAD_SIZE, DOWNLOAD_SIZE, NUM_CELL, DATA, num_up, num_down

size_list = []
upacket_list = []
dpacket_list = []
for cell in range (NUM_CELL):
    size_list.append(0)
    upacket_list.append(0)
    dpacket_list.append(0)

for hour in range(24):
    trace_file = "./traffic/test_traffic_hour_%s" % str(hour)
    with open(trace_file, "rU") as f:
        for line in f:
            line = line.split(" ")
            if len(line) == 9:
                cell = int(line[1])
                if line[0] == "U":
                    size_list[cell] += UPLOAD_SIZE*num_up
                    upacket_list[cell] += 1*num_up
                else:
                    size_list[cell] += DOWNLOAD_SIZE*num_down
                    dpacket_list[cell] += 1*num_down
    
for cell in range(NUM_CELL):
    print "cell=", cell, "Size(M)=",size_list[cell]*1.0/1000000, "upload packet=", upacket_list[cell], "download packet=", dpacket_list[cell]
