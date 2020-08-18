import os
import sys
import logging
import pickle
import datetime
import random
import string

import cv2
import imutils
import face_recognition

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from kafka_client import KafkaImageCli
from cctv_surveillance.appcommon import init_logger, save_image_data_to_jpg

#todo: move following variables to docker-compose as env
avg = None
min_area = 12000
delta_thresh = 5
num_initial_frames_to_discard= 25

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


def detect_motion(imagedata):
    detect_motion.frame_id += 1
    logger.debug(f"working on frame: {detect_motion.frame_id}")

    tempjpg = save_image_data_to_jpg(imagedata, "/usr/app/temp")  #todo: remove hardcoded path
    frame = face_recognition.load_image_file(tempjpg)  #todo: should read from in-memory stream- rather than temp file
    os.remove(tempjpg)

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the average frame is None, initialize it
    global avg
    if avg is None:
        logger.debug("starting background model...")
        avg = gray.copy().astype("float")
        return False

    logger.debug("checking the next frame...")

    # accumulate the weighted average between the current frame and
	# previous frames, then compute the difference between the current
	# frame and running average
    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))

    # threshold the delta image, dilate the thresholded image to fill
	# in holes, then find contours on thresholded image
    thresh = cv2.threshold(frameDelta, delta_thresh, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    max_contour_area= 0
    for c in cnts:
        # if the contour is too small, ignore it
        contour_area = cv2.contourArea(c)
        if contour_area < min_area:
            continue
        logger.debug(f"detected contour of size: {contour_area}")
        
        if contour_area > max_contour_area:
            max_contour_area = contour_area
        
        # compute the bounding box for the contour, draw it on the frame,
		# and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        

    if max_contour_area < min_area:
        return False

    if len(cnts) > 0:
        fname = f"{detect_motion.frame_id}_{str(len(cnts))}_{str(max_contour_area)}.jpg"
        outfile= os.path.join("/usr/app/out", fname)   #todo: use env instead of hardcoded path
        cv2.imwrite(outfile,frame)
        return True
    else:
        return False
        


def consume_kafka_topic():
    kafkaConsumer = get_kafka_cli("consumer")
    kafkaConsumer.register_consumer()
    logger.debug("polling kafka topic now...")
    kafkaProducer = get_kafka_cli("producer")

    detect_motion.frame_id= 0   # initalizing function static variable
    for m in kafkaConsumer.consumer:
        logger.debug("received message from Kafka")
        frame = detect_motion(m.value)
        if frame:
            logger.debug("detected motion. Sending output to kafka...")
            kafkaProducer.send_message(m.value)
        

if __name__== "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside motion-detector...----------------------------")
    env = get_environ()
    consume_kafka_topic()    