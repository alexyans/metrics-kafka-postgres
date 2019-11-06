 #!/bin/bash

source .env

echo "---> Starting up metric collector..."
python collector.py \
    --daemon=True \
    --khost=$TAKEHOME_KAFKA_HOST \
    --kport=$TAKEHOME_KAFKA_PORT \
    --ktopic=$TAKEHOME_KAFKA_TOPIC \
    --kca=$TAKEHOME_KAFKA_CA \
    --kcert=$TAKEHOME_KAFKA_CERT \
    --kkey=$TAKEHOME_KAFKA_KEY