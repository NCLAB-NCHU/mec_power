from define import UPLOAD_SIZE, DOWNLOAD_SIZE, NUM_CELL
for i in range(144):
    area = i + 0
    trace_file = "test_traffic"
    fn = "../traffic/test_traffic_hour_%s" % str(area)
    with open(trace_file, "rU") as f:
        with open(fn, "w") as f1:
            for line in f:
                line = line.split(" ")
                if len(line) == 9:
                    hour = int(line[8])
                    if hour == area:
                        f1.write(" ".join(line) + "\n")
        print (area)
