import os

from kafka_client import KafkaImageCli
from config import bootstrap_servers, topic


if __name__ == "__main__":
    kafkaCli = KafkaImageCli(bootstrap_servers= bootstrap_servers, topic= topic)
    kafkaCli.register_consumer()
    kafkaCli.consume_messages()