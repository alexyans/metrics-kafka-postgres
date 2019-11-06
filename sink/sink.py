import os
import time
import logging
from kafka import KafkaConsumer
# from pystatsd import Client
import psycopg2

def kafka_consumer_init(service_uri, ca_path, cert_path, key_path, topic="metrics"):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=service_uri,
        auto_offset_reset='earliest',
        security_protocol="SSL",
        ssl_cafile=ca_path,
        ssl_certfile=cert_path,
        ssl_keyfile=key_path,
        consumer_timeout_ms=1000,
    )
    return consumer

def pg_client_init(host="localhost", port=5432, db="metrics", user="admin", pwd="admin"):
    return psycopg2.connect(
        host=host,
        port=port,
        database=db,
        user=user,
        password=pwd
    )

def pass_message_to_pg(pg, message):
    logging.info("Message received: {%s}" % message)

    query = """INSERT INTO metrics(timestamp, metric_name, metric_value)
             VALUES(NOW(), %s, %s) RETURNING metric_id;"""

    metric_name, metric_value = message.split(':')
    cur = None
    try:
        cur = pg.cursor()
        cur.execute(query, (metric_name, metric_value))
        pg.commit()
    except (Exception) as error:
        logging.error("Message failed to be inserted into PG: %s", error)
    finally:
        if cur is not None:
            cur.close()

def poll(consumer, pg, interval=5.0):
    while True:
        start_time = time.time()

        raw_msgs = consumer.poll(timeout_ms=1000)
        logging.info(raw_msgs)
        for tp, msgs in raw_msgs.items():
            for msg in msgs:
                message = msg.value.decode('utf-8')
                pass_message_to_pg(pg, message)

        time.sleep(interval - ((time.time() - start_time) % interval))
        

def main():
    consumer = None
    pg = None
    try:
        # get config from env
        service_uri = os.environ.get('TAKEHOME_KAFKA_URI')
        ca_path = os.environ.get('TAKEHOME_KAFKA_CA')
        cert_path = os.environ.get('TAKEHOME_KAFKA_CERT')
        key_path = os.environ.get('TAKEHOME_KAFKA_KEY')
        topic = os.environ.get('TAKEHOME_KAFKA_TOPIC')

        interval = float(os.environ.get('TAKEHOME_CONSUMER_INTERVAL'))

        host = os.environ.get('TAKEHOME_PG_HOST')
        port = int(os.environ.get('TAKEHOME_PG_PORT'))
        db = os.environ.get('TAKEHOME_PG_DATABASE')
        user = os.environ.get('TAKEHOME_PG_USER')
        pwd = os.environ.get('TAKEHOME_PG_PASSWORD')

        # initialize kafka consumer
        consumer = kafka_consumer_init(
            service_uri=service_uri,
            ca_path=ca_path,
            cert_path=cert_path,
            key_path=key_path,
            topic=topic
        )
        
        # initialize PG client
        pg = pg_client_init(host, port, db, user, pwd)

        # start polling for incoming messages
        poll(
            consumer=consumer,
            pg=pg,
            interval=interval
        )
    except (Exception) as error:
        logging.error("%s" % error) 
        exit(1)
    finally:
        if consumer is not None:
            consumer.close()
        if pg is not None:
            pg.close()


if __name__ == '__main__':
    main()