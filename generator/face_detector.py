import os
import sys
import logging
import pickle

import cv2
import face_recognition
#import pbjson

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


def get_kafka_cli(clitype):
    topic_mapping= {"producer": env["out_topic"], "consumer": env["in_topic"]} #todo: use enum instead of string
    assert clitype in topic_mapping, "incorrect kafka client requested. It has to be either producer or consumer"
    return KafkaImageCli(
        bootstrap_servers= [env["kafka_endpt"]],
        topic= topic_mapping[clitype],
        stop_iteration_timeout= sys.maxsize
    )


def detect_face(imagedata):
    tempjpg = save_image_data_to_jpg(imagedata, "/tmp")
    image = face_recognition.load_image_file(tempjpg)  #todo: should read from in-memory stream- rather than temp file
    face_encodings = face_recognition.face_encodings(image)  # get encodings for all detected faces
    os.remove(tempjpg)
    return face_encodings


def create_out_msg(imagedata, encod):
    msg= {
        "id": encod.data.tobytes(),    # hash of the encoding matrix: to serve as primary key
        "someint": 123,
        "somestring": "abc",
        "imagedata": imagedata,
        "encod": encod,
    }
    return pickle.dumps(msg)


def consume_kafka_topic():
    kafkaConsumer = get_kafka_cli("consumer")
    kafkaConsumer.register_consumer()
    logger.debug("polling kafka topic now...")
    kafkaProducer = get_kafka_cli("producer")

    for m in kafkaConsumer.consumer:
        logger.debug("received message from Kafka")
        face_encodings= detect_face(m.value)
        for encod in face_encodings:
            logger.debug("detected a face... sending to kafka topic...")
            outmsg= create_out_msg(m.value, encod)
            kafkaProducer.send_message(outmsg)   

        if not face_encodings:
            logger.debug("motion detected, but not face. saving it to file...")
            save_image_data_to_jpg(m.value, "/tmp", prefix= "MotionDetect")    
        

if __name__== "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside face_detector...----------------------------")
    env = get_environ()
    consume_kafka_topic()