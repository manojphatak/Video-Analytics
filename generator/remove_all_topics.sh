#!/bin/bash

# to be run from within the Kafka container

$KAFKA_HOME/bin/kafka-topics.sh --delete --topic queueing.raw-frames  --bootstrap-server kafka:9092
$KAFKA_HOME/bin/kafka-topics.sh --delete --topic transactions.faces  --bootstrap-server kafka:9092
$KAFKA_HOME/bin/kafka-topics.sh --delete --topic transactions.matched-faces  --bootstrap-server kafka:9092

echo "listing topics after deletion:"
$KAFKA_HOME/bin/kafka-topics.sh --list  --bootstrap-server kafka:9092