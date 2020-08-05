import os
import sys
import fnmatch
import tempfile
import string
import random
import argparse
import logging
from functools import reduce

import face_recognition
from pipe import Pipe, select, where

from kafka_client import KafkaImageCli


# This sets the root logger to write to stdout (your console).
# Your script/app needs to call this somewhere at least once.
logging.basicConfig()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@Pipe
def tolist(iterable):
    return list(iterable)

@Pipe
def toSet(iterable):
    return set(iterable)

def hash_of_encoding(encod):
    return encod.data.tobytes()


def load_known_faces(known_faces_path):
    assert os.path.exists(known_faces_path)
    jpgfiles = fnmatch.filter(os.listdir(known_faces_path), "*.jpg")    # Treat filename-without-extn as image title
    image_titles = [os.path.splitext(f)[0] for f in jpgfiles]
    jpgfpaths = [os.path.join(known_faces_path, f) for f in jpgfiles]

    known_faces = {}
    for title, fpath in zip(image_titles, jpgfpaths):
        image = face_recognition.load_image_file(fpath)
        face_encoding = face_recognition.face_encodings(image)[0]
        hashencod = hash_of_encoding(face_encoding)   # Take hash of face-encode matrix, to serve as dict key
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


def save_image_data_to_jpg(imagedata, outpath):
    def get_random_filename():
        letters = ["unknown-"] +  [random.choice(string.ascii_lowercase) for i in range(5)]
        fname = "".join(letters)
        return "{fname}.jpg".format(fname= fname)

    assert os.path.exists(outpath)
    tempjpg = os.path.join(outpath, get_random_filename())
    with open(tempjpg, "wb") as f:
        f.write(imagedata)
    return tempjpg


def consume_images_from_kafka(kafkaCli, known_faces_path, outpath):
    '''
    "all_faces" is a dictionary with structure as follows:
    Each face is identified by the "hash of its face encoding"
    all_faces = {
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
    all_faces = {}

    logger.debug("polling kafka topic now...")
    for m in kafkaCli.consumer:
        logger.debug("received message from Kafka")
        tempjpg = save_image_data_to_jpg(m.value, outpath)
        image = face_recognition.load_image_file(tempjpg)
        face_encodings = face_recognition.face_encodings(image)  # get encodings for all detected faces

        if not face_encodings:
            os.remove(tempjpg)  # remove the jpg, since it doesn't contain any faces

        for encod in face_encodings:
            matched_faces = match_faces(encod, known_faces, tolerance=0.6)
            if matched_faces:
                all_faces[hash_of_encoding(encod)] = {"matches": matched_faces}
            else:
                matches = {
                        "name": "unknown",
                        "imgfile": tempjpg,
                        "face_encoding": encod
                    }
                all_faces[hash_of_encoding(encod)] = {"matches": [matches]}
                save_image_data_to_jpg(m.value, known_faces_path) # This is an unknown face so far. Copy it to folder of known faces
                known_faces = load_known_faces(known_faces_path)  # Reload the known faces

    matched_titles = get_names_of_all_matched_images(all_faces)
    return matched_titles


def get_names_of_all_matched_images(faces):
    '''
    "faces" is the dictionary, which is keyed by its hash-of-its-encoding-matrix
    '''
    tags = faces.values() | select(lambda x: x["matches"]) | tolist
    tags = reduce(lambda a,b: a+b, tags, [])
    matched_titles = tags | select(lambda r: r["name"]) | tolist | toSet
    return matched_titles


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--knownfaces", help="")
    parser.add_argument("--outpath", help="")
    parser.add_argument("--kafkatopic", help="")
    parser.add_argument("--kafka-endpt", dest= "kafka_endpt", help="")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    assert args.knownfaces, "file path for known faces is not provided"
    assert args.outpath
    assert args.kafka_endpt
    kafka_endpt = args.kafka_endpt.split(",")  #converting to list
    assert kafka_endpt, "kafka bootstrap server list is empty"

    kafkaCli = KafkaImageCli(
        bootstrap_servers=kafka_endpt,
        topic= args.kafkatopic,
        stop_iteration_timeout=5000)

    kafkaCli.register_consumer()
    matched_titles= consume_images_from_kafka(kafkaCli, 
                                            known_faces_path= args.knownfaces, 
                                            outpath= args.outpath
                                            )
    print(matched_titles)
