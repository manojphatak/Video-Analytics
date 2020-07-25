import os
import fnmatch
import tempfile
import string
import random
from functools import reduce

import face_recognition
from pipe import Pipe, select, where

from kafka_client import KafkaImageCli
from config import bootstrap_servers, topic

basepath = "/home/manoj/Pictures"
known_faces_path = os.path.join(basepath, "known_faces")


@Pipe
def tolist(iterable):
    return list(iterable)

@Pipe
def toSet(iterable):
    return set(iterable)


def load_known_faces(known_faces_path):
    assert os.path.exists(known_faces_path)
    jpgfiles = fnmatch.filter(os.listdir(known_faces_path), "*.jpg")    # Treat filename-without-extn as image title
    image_titles = [os.path.splitext(f)[0] for f in jpgfiles]
    jpgfpaths = [os.path.join(known_faces_path, f) for f in jpgfiles]

    known_faces = {}
    for title, fpath in zip(image_titles, jpgfpaths):
        image = face_recognition.load_image_file(fpath)
        face_encoding = face_recognition.face_encodings(image)[0]
        hashencod = face_encoding.data.tobytes()   # Take hash of face-encode matrix, to serve as dict key
        known_faces[hashencod] = {
            "name": title,
            "imgfile": fpath,
            "face_encoding": face_encoding
        }
    return known_faces


def match_faces(faceencod, known_faces, tolerance):
    knonwn_encodes = known_faces.values() | select(lambda e: e["face_encoding"]) | tolist
    matches = face_recognition.compare_faces(knonwn_encodes, faceencod, tolerance)

    # Select only matched records
    return zip(matches, known_faces.values()) \
        | where(lambda x: x[0])    \
        | select(lambda m: m[1])   \
        | tolist     


def save_image_data_to_jpg(imagedata):
    def get_random_filename():
        letters = ["unknown-"] +  [random.choice(string.ascii_lowercase) for i in range(5)]
        fname = "".join(letters)
        return f"{fname}.jpg"

    tempjpg = os.path.join(tempfile.gettempdir(), get_random_filename())
    with open(tempjpg, "wb") as f:
        f.write(imagedata)
    return tempjpg


def consume_images_from_kafka(kafkaCli):
    '''
    "matched" is a dictionary with structure as follows:
    matched = {
        <hash-of-the-encoding>: {
            "matches": [{
                "name": <title of the image>,   # "unknown" if it doesn't match with anything
                "imgfile": <filepath for the jpeg image",
                "face_encoding": <the face encoding matrix"
            }]
        },
        <another-hash-of-the-encoding> : {...}
    }
    '''
    known_faces = load_known_faces(known_faces_path)
    matched = {}

    for m in kafkaCli.consumer:
        print(f"received message from Kafka")
        tempjpg = save_image_data_to_jpg(m.value)
        image = face_recognition.load_image_file(tempjpg)
        face_encodings = face_recognition.face_encodings(image)  # get encodings for all detected faces

        for encod in face_encodings:
            matched_faces = match_faces(encod, known_faces, tolerance=0.6)
            if matched_faces:
                matched[encod.data.tobytes()] = {"matches": matched_faces}
            else:
                matches = {
                        "name": "unknown",
                        "imgfile": tempjpg,
                        "face_encoding": encod
                    }
                matched[encod.data.tobytes()] = {"matches": [matches]}

    matched_titles = get_names_of_all_matched_images(matched)
    print(matched_titles)
    return matched_titles


def get_names_of_all_matched_images(faces):
    '''
    "faces" is the dictionary, which is keyed by its hash-of-its-encoding-matrix
    '''
    tags = faces.values() | select(lambda x: x["matches"]) | tolist
    tags = reduce(lambda a,b: a+b, tags, [])
    matched_titles = tags | select(lambda r: r["name"]) | tolist | toSet
    return matched_titles


if __name__ == "__main__":
    kafkaCli = KafkaImageCli(
        bootstrap_servers=bootstrap_servers,
        topic=topic,
        stop_iteration_timeout=3000)
    kafkaCli.register_consumer()
    consume_images_from_kafka(kafkaCli)
