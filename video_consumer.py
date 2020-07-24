import os
import fnmatch

import face_recognition

from kafka_client import KafkaImageCli
from config import bootstrap_servers, topic

basepath= "/home/manoj/Pictures"
known_faces_path = os.path.join(basepath, "known_faces")


def load_known_faces(known_faces_path):
    assert os.path.exists(known_faces_path)
    imgs = fnmatch.filter(os.listdir(known_faces_path), "*.jpg")
    names = [os.path.splitext(f)[0] for f in imgs]
    imgs = [os.path.join(known_faces_path, img) for img in imgs]

    experiment = {}
    known_faces = []
    for n,img in zip(names, imgs):
        image = face_recognition.load_image_file(img)
        face_encoding = face_recognition.face_encodings(image)[0]
        known_faces.append({
            "name": n,
            "imgfile": img,
            "face_encoding":face_encoding
        }
        )
        k = face_encoding.data.tobytes()
        experiment[k]= n
    return known_faces


def match_faces(face_encoding, known_faces, tolerance):
    matched_faces = []
    for kf in known_faces:
        match = face_recognition.compare_faces([kf["face_encoding"]], face_encoding, tolerance)
        if match:
            matched_faces.append(kf["name"])
    return matched_faces


def match_faces_new():
    pass



def consume_images_from_kafka(kafkaCli):
    known_faces = load_known_faces(known_faces_path)
    #print(known_faces)
    for m in kafkaCli.consumer:
        print(f"received message from Kafka")
        tempfile = "tempfile.jpg"
        with open(os.path.join(basepath,tempfile), "wb") as f:
            f.write(m.value) 
        image = face_recognition.load_image_file(os.path.join(basepath,tempfile))
        face_encoding = face_recognition.face_encodings(image)[0]
        
        matched_faces = match_faces(face_encoding, known_faces, tolerance=0.9)
        print(matched_faces)


if __name__ == "__main__":
    kafkaCli = KafkaImageCli(bootstrap_servers= bootstrap_servers, topic= topic)
    kafkaCli.register_consumer()
    consume_images_from_kafka(kafkaCli)