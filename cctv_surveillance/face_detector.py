import os
import sys
import logging
import pickle

import face_recognition

currdir = os.path.dirname(__file__)
sys.path.append(os.path.join(currdir,".."))

from cctv_surveillance.appcommon import init_logger, save_image_data_to_jpg
from framedata import FrameData
from kafka_base_consumer import KafkaStreamingConsumer

class FaceDetector(KafkaStreamingConsumer):
    def __init__(self ):
        super().__init__(handler = self.handle_msg)


    def detect_face(self, imagedata):
        tempjpg = save_image_data_to_jpg(imagedata, "/tmp")
        image = face_recognition.load_image_file(tempjpg)  #todo: should read from in-memory stream- rather than temp file
        face_encodings = face_recognition.face_encodings(image)  # get encodings for all detected faces
        os.remove(tempjpg)
        return face_encodings


    def create_out_msg(self, imagedata, encod):
        framedata = FrameData(
                        id = encod.data.tobytes(), # hash of the encoding matrix: to serve as primary key
                        imagedata = imagedata,
                        encod = encod
                    )
        return pickle.dumps(framedata)


    def handle_msg(self, msg):
        face_encodings= self.detect_face(msg)
        for encod in face_encodings:
            logger.debug("detected a face... sending to kafka topic...")
            outmsg= self.create_out_msg(msg, encod)
            yield outmsg

   

if __name__== "__main__":
    logger = init_logger(__file__)
    logger.debug("------------start: inside face_detector...----------------------------")
    face_detector = FaceDetector()