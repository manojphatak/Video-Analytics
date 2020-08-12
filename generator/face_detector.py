import os
import sys
import logging

import cv2
import face_recognition

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from kafka_client import KafkaImageCli
from generator.appcommon import init_logger, save_image_data_to_jpg


def get_environ() -> dict:
    return {
        "kafka_endpt": os.environ.get("KAFKA_BROKER_URL", ""),
        "in_topic": os.environ.get("INPUT_TOPIC", ""),
        "out_topic": os.environ.get("OUTPUT_TOPIC", ""),
    }


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
        image = face_recognition.load_image_file(tempjpg)  #todo: should read from in-memory stream- rather than temp file
        face_encodings = face_recognition.face_encodings(image)  # get encodings for all detected faces
        if not face_encodings:
            os.remove(tempjpg)  # remove the jpg, since it doesn't contain any faces


if __name__== "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside face_detector...----------------------------")
    env = get_environ()
    consume_kafka_topic()