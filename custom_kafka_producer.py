#!/usr/bin/env python
import threading, time

from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
from kafka.admin import NewTopic

class CustomKafkaProducer():
    def __init__(self, topic_names: []):
        admin = KafkaAdminClient(bootstrap_servers='localhost:9092')
        existing_topics = admin.list_topics()
        for topic in topic_names:
            if topic not in existing_topics:
                topic = NewTopic(name=topic_names[0],
                                num_partitions=1,
                                replication_factor=1)


                admin.create_topics([topic])

        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
    def __del__(self):
        self.producer.close()
    def write_topic(self, topic, data):
        self.producer.send(topic, data.encode("utf-8"))

