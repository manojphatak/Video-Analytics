import os
import sys
import logging
import time
import fnmatch

import cv2

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from kafka_client import KafkaImageCli
from generator.appcommon import init_logger


def get_environ() -> dict:
    return {
        "kafka_endpt": os.environ.get("KAFKA_BROKER_URL", ""),
        "topic": os.environ.get("TRANSACTIONS_TOPIC", ""),
        "stop_iteration_timeout": int(os.environ.get("KAFKA_CLIENT_BLOCKING_TIMEOUT", 3000)),
        "movie_source": os.environ.get("MOVIE_FILES_SOURCE", ""),
        "frame_cap_period": int(os.environ.get("FRAME_CAPTURE_PERIOD", "")),
    }


def get_movie_files() -> list:
    movie_source= env["movie_source"]
    assert os.path.exists(movie_source), f"filepath does not exist: {movie_source}"
    videofiles = fnmatch.filter(os.listdir(movie_source), "*.webm")
    return [os.path.join(movie_source, f) for f in videofiles]


def read_movie(moviefile):
    logger.debug(f"Reading movie file: {moviefile}")
    video = cv2.VideoCapture(moviefile)
    
    totalframes= video.get(cv2.CAP_PROP_FRAME_COUNT)
    logger.debug(f"Total # of frames: {totalframes}")
    fps= video.get(cv2.CAP_PROP_FPS)
    logger.debug(f"fps: {fps}")
    logger.debug(f"Capturing frame every {env['frame_cap_period']} seconds")

    frames_to_skip = fps * env["frame_cap_period"]
    frameid = -1
    while(video.isOpened()):
        success, frame = video.read()
        if not success: 
            break

        frameid += 1 
        if frameid % frames_to_skip: 
            continue

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        frame = frame[:, :, ::-1]    #TODO: This should be moved to consumer    

        ret, buffer = cv2.imencode('.jpg', frame)
        yield buffer
    video.release()  # Todo: Use Context Manager


def stream_movies():
    logger.debug(f"streaming to kafka endpoint: {env['kafka_endpt']}")
    kafkaCli = KafkaImageCli(bootstrap_servers= [env["kafka_endpt"]], 
                             topic= env["topic"],
                             stop_iteration_timeout= env["stop_iteration_timeout"])

    for movie in get_movie_files():
        for frame in read_movie(movie):
            logger.debug("sending frame to kafka topic")       
            kafkaCli.send_message(frame.tobytes())
    
    

if __name__ == "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside movie_streamer...----------------------------")
    env : dict = get_environ()
    stream_movies()