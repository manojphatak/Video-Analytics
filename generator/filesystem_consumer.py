import os
import sys
import logging
import pickle

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from kafka_client import KafkaImageCli
from generator.appcommon import init_logger, save_image_data_to_jpg


def get_environ() -> dict:
    return {
        "kafka_endpt": os.environ.get("KAFKA_BROKER_URL", ""),
        "in_topic": os.environ.get("INPUT_TOPIC", ""),
        "out_fileloc": os.environ.get("OUTPUT_FILE_LOCATION", ""),
    }


def get_kafka_cli(clitype):
    return KafkaImageCli(
        bootstrap_servers= [env["kafka_endpt"]],
        topic= env["in_topic"],
        stop_iteration_timeout= sys.maxsize
    )


def consume_kafka_topic():
    kafkaConsumer = get_kafka_cli("consumer")
    kafkaConsumer.register_consumer()
    logger.debug("polling kafka topic now...")

    discovered= set([])

    for m in kafkaConsumer.consumer:
        logger.debug("received message from Kafka")
        data = pickle.loads(m.value)
        
        matches= set(data["matches"])
        if matches.difference(discovered):     # new matches discovered    
            discovered = discovered.union(set(matches))
            save_image_data_to_jpg(data["imagedata"], env["out_fileloc"])  # save this image somewhere for ref
            logger.debug(f"discovered so far... {discovered}")


if __name__== "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside filesystem-consumer...----------------------------")
    env = get_environ()
    consume_kafka_topic()
    