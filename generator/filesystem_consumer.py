import os
import sys
import logging

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from kafka_client import KafkaImageCli
from generator.appcommon import init_logger, save_image_data_to_jpg

import pbjson

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

    for m in kafkaConsumer.consumer:
        logger.debug("received message from Kafka")
        data = pbjson.loads(m.value)
        logger.debug("Recovering data...")
        logger.debug(f"someint: {data['someint']}")
        save_image_data_to_jpg(data["imagedata"], env["out_fileloc"])


if __name__== "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside face_detector...----------------------------")
    env = get_environ()
    consume_kafka_topic()
    