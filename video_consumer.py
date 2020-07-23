import os

from kafka_client import KafkaImageCli
from config import bootstrap_servers, topic

def consume_messages(kafkaCli):
    frameid = 0
    basepath= "/home/manoj/Pictures"
    for m in kafkaCli.consumer:
        print("received message from Kafka")
        fname= f"{frameid}.jpg"           
        with open(os.path.join(basepath,fname), "wb") as f:
            f.write(m.value) 
            frameid += 1


if __name__ == "__main__":
    kafkaCli = KafkaImageCli(bootstrap_servers= bootstrap_servers, topic= topic)
    kafkaCli.register_consumer()
    consume_messages(kafkaCli)