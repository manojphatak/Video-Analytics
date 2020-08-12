import os
import sys
import logging
import random
import string

import cv2
import face_recognition

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from kafka_client import KafkaImageCli
from generator.appcommon import init_logger


def get_environ() -> dict:
    return {
        "kafka_endpt": os.environ.get("KAFKA_BROKER_URL", ""),
        "in_topic": os.environ.get("INPUT_TOPIC", ""),
        "out_topic": os.environ.get("OUTPUT_TOPIC", ""),
    }


def save_image_data_to_jpg(imagedata, outpath):
    def get_random_filename():
        letters = ["unknown-"] +  [random.choice(string.ascii_lowercase) for i in range(5)]
        fname = "".join(letters)
        return "{fname}.jpg".format(fname= fname)

    assert os.path.exists(outpath)
    tempjpg = os.path.join(outpath, get_random_filename())
    with open(tempjpg, "wb") as f:
        f.write(imagedata)
    return tempjpg    


def consume_kafka_topic():
    kafkaCli = KafkaImageCli(
        bootstrap_servers= [env["kafka_endpt"]],
        topic= env["in_topic"],
        stop_iteration_timeout= sys.maxsize
        )
    kafkaCli.register_consumer()
    logger.debug("polling kafka topic now...")
    for m in kafkaCli.consumer:
        logger.debug("received message from Kafka")
        tempjpg = save_image_data_to_jpg(m.value, "/tmp")


if __name__== "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside face_detector...----------------------------")
    env = get_environ()
    consume_kafka_topic()