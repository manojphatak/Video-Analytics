from json import dumps, loads
import os

from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import TopicAlreadyExistsError

from config import bootstrap_servers, topic


class KafkaCli:
    def __init__(self, bootstrap_servers, topic,
                 value_serializer, value_deserializer):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.create_topic(topic)
        self.value_serializer= value_serializer
        self.value_deserializer= value_deserializer
        
        
    def create_topic(self, topic):
        try:
            admin_client = KafkaAdminClient(
            bootstrap_servers= bootstrap_servers, 
            )

            topic_list = []
            topic_list.append(NewTopic(name= topic, num_partitions=1, replication_factor=1))
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
        except TopicAlreadyExistsError:
            pass #ignore
        
        
    def send_message(self, msg):
        producer = KafkaProducer(
                                    value_serializer= self.value_serializer, 
                                    bootstrap_servers= bootstrap_servers
        )

        producer.send(self.topic, value= msg)
        producer.flush()
        
        
    def register_consumer(self):
        self.consumer = KafkaConsumer(self.topic,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=True,
                                 group_id='my-group-1',
                                 value_deserializer= self.value_deserializer,
                                 bootstrap_servers= self.bootstrap_servers
                        )
        
    def consume_messages(self):
        for m in self.consumer:
            print(m.value)


class KafkaJsonCli(KafkaCli):
    def __init__(self, bootstrap_servers, topic):
        super(KafkaJsonCli, self).__init__(bootstrap_servers, 
                                           topic,
                                           value_serializer = lambda m: dumps(m).encode('utf-8'),
                                           value_deserializer = lambda m: loads(m.decode('utf-8'))
                                          )



class KafkaImageCli(KafkaCli):
    def __init__(self, bootstrap_servers, topic):
        super(KafkaImageCli, self).__init__(bootstrap_servers, 
                                           topic,
                                           value_serializer = lambda m: m,
                                           value_deserializer = lambda m: m
                                          )
        
    def consume_messages(self):
        frameid = 0
        basepath= "/home/manoj/Pictures"
        for m in self.consumer:
            print("received message from Kafka")
            fname= f"{frameid}.jpg"           
            with open(os.path.join(basepath,fname), "wb") as f:
                f.write(m.value) 
                frameid += 1