import os
import argparse
import logging

import cv2

from kafka_client import KafkaImageCli

# This sets the root logger to write to stdout (your console).
# Your script/app needs to call this somewhere at least once.
logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def stream_video_from_file(moviefile, topic, bootstrap_servers):
    logger.debug("streaming to kafka endpoint: {e}".format(e=bootstrap_servers))
    kafkaCli = KafkaImageCli(bootstrap_servers= bootstrap_servers, topic= topic, stop_iteration_timeout=3000)
    
    assert os.path.exists(moviefile)
    video = cv2.VideoCapture(moviefile)
    
    totalframes= video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps= video.get(cv2.CAP_PROP_FPS)
    frames_to_skip = fps * 10   # we are capturing aframe every minute

    logger.info("---------- Summay ----------")
    logger.info("Total # of frames: {numframes}".format(numframes= totalframes))
    logger.info("fps: {fps}".format(fps= fps))
    logger.info("Frames to skip: {frames_to_skip}".format(frames_to_skip= frames_to_skip))
    

    frameid = -1
    maxframes = float('inf')
    while(video.isOpened()):
        success, frame = video.read()
        if not success: break

        frameid += 1 
        if frameid % frames_to_skip: continue
        if frameid > maxframes: break

        logger.debug("Processing frame #{id}".format(id= frameid))
        
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        frame = frame[:, :, ::-1]
        
        ret, buffer = cv2.imencode('.jpg', frame)
        kafkaCli.send_message(buffer.tobytes())
        
    video.release()    


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--videofile", help="")
    parser.add_argument("--kafkatopic", help="")
    parser.add_argument("--kafka-endpt", dest= "kafka_endpt", help="")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    assert args.videofile, "pl profile filepath for the videofile to parse"
    assert args.kafkatopic
    assert args.kafka_endpt
    kafka_endpt = args.kafka_endpt.split(",")  #converting to list
    assert kafka_endpt, "kafka bootstrap server list is empty"
    stream_video_from_file(args.videofile, args.kafkatopic, kafka_endpt)