import os
import sys
import logging
import pickle

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from kafka_client import KafkaImageCli
from cctv_surveillance.appcommon import init_logger, save_image_data_to_jpg
from framedata import FrameData

from kafka_base_consumer import KafkaEndConsumer


class FilesystemConsumer(KafkaEndConsumer):
    def __init__(self):
        super().__init__(handler = self.handle_msg)
        self.discovered = set([])
        out_fileloc: os.environ.get("OUTPUT_FILE_LOCATION", ""),

    
    def handle_msg(self, msg):
        data = pickle.loads(msg)
        matches= set(data.matches)
        if matches.difference(self.discovered):     # new matches discovered    
            self.discovered = self.discovered.union(set(matches))
            save_image_data_to_jpg(data.imagedata, out_fileloc)  # save this image somewhere for ref
            logger.debug(f"discovered so far... {self.discovered}")



if __name__== "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside filesystem-consumer...----------------------------")
    FilesystemConsumer()
    