import sys
import psutil
import time
import daemon

# defaults
interval = 5.0
daemonized = False
#stdout=sys.stdout
outfile="./out"
if outfile:
    stdout=open(outfile, "w")
else:
    stdout=sys.stdout

# output metric to stdout
def output_metrics():
    # one cpu_time
    cpu_times = psutil.cpu_times(False) 
    for name, metric in zip(cpu_times._fields, cpu_times):
        print(name, ": ", metric, file=stdout)

    # one memory

# set sampling rate
def run_sampling_loop():
    while True:
        start_time = time.time()
        # output one metric
        output_metrics()
        time.sleep(interval - ((time.time() - start_time) % interval))

# initialize collector
def main():
    if daemonized:
        print("Starting metric collector (daemonized)")
        with daemon.DaemonContext(stdout=stdout):
            run_sampling_loop()
    else:
        print("Starting metric collector")
        run_sampling_loop()

if __name__ == "__main__":
    main()



