import argparse
import sys
import psutil
import time
import daemon
import logging
from kafka import KafkaProducer
# from statsd import Client

# parse args and set defaults
def parse_options():
    parser = argparse.ArgumentParser(description='Pipe OS metrics through Aiven Kafka into Aiven PGSQL', add_help=True)
    parser.add_argument('--interval', type=float, help='Sampling period in sec (default: 5.0)', default=5.0)
    parser.add_argument('--daemon', type=bool, help='Set to True to run as daemon (default: False)', default=False)
    parser.add_argument('--out', type=str, help='Redirect output to file (default: "" (STDOUT))', default="")
    parser.add_argument('--log', type=str, help='Set logfile path (default: "./00.log")', default="00.log")
    
    parser.add_argument('--khost', type=str, help='Kafka Host (default: "localhost")', default="localhost")
    parser.add_argument('--kport', type=str, help='Kafka Port (default: "1234")', default="")
    parser.add_argument('--ktopic', type=str, help='Kafka Topic (default: "metrics")', default="metrics")
    parser.add_argument('--kca', type=str, help='Kafka CA path (default: "")', default="")
    parser.add_argument('--kcert', type=str, help='Kafka Certificate path (default: "")', default="")
    parser.add_argument('--kkey', type=str, help='Kafka Key path (default: "")', default="")
    
    parser.add_argument('--sdhost', type=str, help='Statsd Host (default: "localhost")', default="localhost")
    parser.add_argument('--sdport', type=int, help='Statsd Port (default: "8125")', default=8125)

    return parser.parse_args()

def get_metrics(log):
    # sample metrics: one cpu utilization, one memory utilization, one disk utilization
    cpu_percent = psutil.cpu_percent(False)
    mem_percent = psutil.virtual_memory().percent
    disk_percent = psutil.disk_usage("/").percent

    field_names = ["cpu_percent", "mem_percent", "disk_percent"]
    field_values = [cpu_percent, mem_percent, disk_percent]
    fields = list(zip(field_names, field_values))

    for name, value in fields:
        log.info("%s : %s" % (name, str(value)))

    return fields

def publish_metrics(log, producer, metrics, topic):
    log.info("11111")
    print(metrics)
    for name, value in metrics:
        message = "%s:%s" % (name, str(value))
        log.info('Sending "%s"...' % message)
        producer.send(topic, str.encode(message))

# sample OS metrics at a given sampling rate
def run_sampling_loop(interval, log, args, producer):
    while True:
        start_time = time.time()
        # output one metric
        metrics = get_metrics(log)
        publish_metrics(log, producer, metrics, args.ktopic)
        
        time.sleep(interval - ((time.time() - start_time) % interval))

# initialize collector
def main():
    producer = None
    try:
        args = parse_options()
        if args.out:
            outfile=open(args.out, "w")
        else:
            outfile=sys.stdout

        # initialize logger
        logging.basicConfig(filename=args.log, level=logging.DEBUG)

        # initialize statsd client
        #sc = Client(args.sdhost, args.sdport)
        #logging.info('Statsd client started connected to %s:%d' % (args.sdhost % args.sdport))

        # initialize kafka producer
        server_uri = "%s:%d" % (args.khost, int(args.kport))
        producer = KafkaProducer(
            bootstrap_servers=server_uri,
            security_protocol="SSL",
            ssl_cafile=args.kca,
            ssl_certfile=args.kcert,
            ssl_keyfile=args.kkey,
        )
        logging.info('Kafka producer connected to server %s' % server_uri)

        if args.daemon:
            logging.info("Starting metric collector (daemonized)...")
            with daemon.DaemonContext():
                run_sampling_loop(args.interval, logging, args, producer)
        else:
            logging.info("Starting metric collector...")
            run_sampling_loop(args.interval, logging, args, producer)
    except (Exception) as error:
        logging.error("%s" % error)
    finally:
        if producer is not None:
            producer.close()

if __name__ == "__main__":
    main()



