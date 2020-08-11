import os
import sys
import logging
import logging.config
import time

import cv2

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from kafka_client import KafkaImageCli
from common import get_env, setup_logging

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_environ() -> dict:
    return {
        "kafka_endpt": os.environ.get("KAFKA_BROKER_URL", ""),
        "topic": os.environ.get("TRANSACTIONS_TOPIC", ""),
        "stop_iteration_timeout": int(os.environ.get("KAFKA_CLIENT_BLOCKING_TIMEOUT", 3000))
    }


def get_movie_files() -> list:
    return []


def stream_movie_file():
    logger.debug(f"streaming to kafka endpoint: {env['kafka_endpt']}")
    logger.debug("second line")
    while True:
        logger.debug("busy...")
        time.sleep(3)
        
    kafkaCli = KafkaImageCli(bootstrap_servers= [env["kafka_endpt"]], 
                             topic= env["topic"],
                             stop_iteration_timeout= env["stop_iteration_timeout"])
    for movie in get_movie_files():
        pass
    
        

if __name__ == "__main__":
    print("inside movie_streamer...")
    env : dict = get_environ()
    stream_movie_file()