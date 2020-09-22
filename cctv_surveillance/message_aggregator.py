import os
import sys
import logging

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from kafka_client import KafkaCli
from cctv_surveillance.appcommon import init_logger
from kafka_base_consumer import KafkaEndConsumer


class MessageAggregator(KafkaEndConsumer):
    def __init__(self):
        self.discovered_faces = set([])
        self.discovered_objects = set([])
        super().__init__()
        
    
    def handle_msg(self, msg):
        self.discovered_faces = self.discovered_faces.union(set(msg.matched_faces))
        logger.debug(f"discovered faces... {self.discovered_faces}")

        # sample contents of msg.objects: ["person: 0.99", "cat: 0.98"]
        # drop the confidense number & extract inly the objects i.e. person, cat etc
        objects = map(lambda x: x.split(":")[0], msg.objects)
        
        self.discovered_objects = self.discovered_objects.union(set(objects))
        logger.debug(f"discovered objects... {self.discovered_objects}")



if __name__== "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside message-aggregator...----------------------------")
    MessageAggregator()
    