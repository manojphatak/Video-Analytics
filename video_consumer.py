import os
import fnmatch

import face_recognition
from pipe import Pipe, select, where

from kafka_client import KafkaImageCli
from config import bootstrap_servers, topic

basepath= "/home/manoj/Pictures"
known_faces_path = os.path.join(basepath, "known_faces")

@Pipe
def tolist(iterable):
    return list(iterable)


def load_known_faces(known_faces_path):
    assert os.path.exists(known_faces_path)
    jpgfiles = fnmatch.filter(os.listdir(known_faces_path), "*.jpg")
    image_titles = [os.path.splitext(f)[0] for f in jpgfiles]   # Treat filename-without-extn as image title
    jpgfpaths = [os.path.join(known_faces_path, f) for f in jpgfiles]

    known_faces = {}
    for title,fpath in zip(image_titles, jpgfpaths):
        image = face_recognition.load_image_file(fpath)
        face_encoding = face_recognition.face_encodings(image)[0]
        hashencod = face_encoding.data.tobytes()
        known_faces[hashencod] = {
            "name": title,
            "imgfile": fpath,
            "face_encoding":face_encoding
        }
    return known_faces


def match_faces(faceencod, known_faces, tolerance):
    knonwn_encodes_hashes = known_faces.values()
    
    knonwn_encodes = knonwn_encodes_hashes | select(lambda e: e["face_encoding"]) | tolist
    matches = face_recognition.compare_faces(knonwn_encodes, faceencod, tolerance)
    
    return zip(matches, knonwn_encodes_hashes) \
                                             | where(lambda x: x[0])    \
                                             | select(lambda m: m[1])     



def consume_images_from_kafka(kafkaCli):
    known_faces = load_known_faces(known_faces_path)
    for m in kafkaCli.consumer:
        print(f"received message from Kafka")
        tempfile = "tempfile.jpg"
        with open(os.path.join(basepath,tempfile), "wb") as f:
            f.write(m.value) 
        image = face_recognition.load_image_file(os.path.join(basepath,tempfile))
        face_encoding = face_recognition.face_encodings(image)[0]
        
        matched_faces = match_faces(face_encoding, known_faces, tolerance=0.6)
        matched_faces = list(map(lambda m:m["name"], matched_faces))
        print(matched_faces)


if __name__ == "__main__":
    kafkaCli = KafkaImageCli(bootstrap_servers= bootstrap_servers, topic= topic)
    kafkaCli.register_consumer()
    consume_images_from_kafka(kafkaCli)