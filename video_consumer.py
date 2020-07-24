import os
import fnmatch
import tempfile

import face_recognition
from pipe import Pipe, select, where

from kafka_client import KafkaImageCli
from config import bootstrap_servers, topic

basepath = "/home/manoj/Pictures"
known_faces_path = os.path.join(basepath, "known_faces")


@Pipe
def tolist(iterable):
    return list(iterable)


def load_known_faces(known_faces_path):
    assert os.path.exists(known_faces_path)
    jpgfiles = fnmatch.filter(os.listdir(known_faces_path), "*.jpg")    # Treat filename-without-extn as image title
    image_titles = [os.path.splitext(f)[0] for f in jpgfiles]
    jpgfpaths = [os.path.join(known_faces_path, f) for f in jpgfiles]

    known_faces = {}
    for title, fpath in zip(image_titles, jpgfpaths):
        image = face_recognition.load_image_file(fpath)
        face_encoding = face_recognition.face_encodings(image)[0]
        hashencod = face_encoding.data.tobytes()
        known_faces[hashencod] = {
            "name": title,
            "imgfile": fpath,
            "face_encoding": face_encoding
        }
    return known_faces


def match_faces(faceencod, known_faces, tolerance):
    knonwn_encodes_hashes = known_faces.values()

    knonwn_encodes = knonwn_encodes_hashes | select(lambda e: e["face_encoding"]) | tolist
    matches = face_recognition.compare_faces(knonwn_encodes, faceencod, tolerance)

    return zip(matches, knonwn_encodes_hashes) \
        | where(lambda x: x[0])    \
        | select(lambda m: m[1])


def save_image_data_to_jpg(imagedata):
    tempjpg = os.path.join(tempfile.gettempdir(), "temp.jpg")
    with open(tempjpg, "wb") as f:
        f.write(imagedata)
    return tempjpg


def consume_images_from_kafka(kafkaCli):
    known_faces = load_known_faces(known_faces_path)
    matched = []

    for m in kafkaCli.consumer:
        print(f"received message from Kafka")
        tempjpg = save_image_data_to_jpg(m.value)
        image = face_recognition.load_image_file(tempjpg)
        face_encodings = face_recognition.face_encodings(image)

        for encod in face_encodings:
            matched_faces = match_faces(encod, known_faces, tolerance=0.6)
            matched.extend(matched_faces)

    matched_titles = matched | select(lambda m: m["name"]) | tolist
    print(set(matched_titles))


if __name__ == "__main__":
    kafkaCli = KafkaImageCli(
        bootstrap_servers=bootstrap_servers,
        topic=topic,
        stop_iteration_timeout=3000)
    kafkaCli.register_consumer()
    consume_images_from_kafka(kafkaCli)
