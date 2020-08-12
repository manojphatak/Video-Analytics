import os
import sys
import logging
import time
import time

import cv2

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from kafka_client import KafkaImageCli
from generator.appcommon import init_logger


if __name__== "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside face_detector...----------------------------")
    while True:
        logger.debug("checking kafka messages...")
        time.sleep(3)