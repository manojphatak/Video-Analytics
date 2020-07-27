import os
import argparse

import cv2

from config import bootstrap_servers
from kafka_client import KafkaImageCli

def stream_video_from_file(moviefile, topic):
    kafkaCli = KafkaImageCli(bootstrap_servers= bootstrap_servers, topic= topic, stop_iteration_timeout=3000)
    
    assert os.path.exists(moviefile)
    video = cv2.VideoCapture(moviefile)
    
    fps= video.get(cv2.CAP_PROP_FPS)
    frames_to_skip = fps * 60   # we are capturing a frame every minute
    numframes = 0
    maxframes = float('inf')
    while(video.isOpened()):
        success, frame = video.read()
        if not success: break
        numframes += 1 
        if numframes % frames_to_skip: continue
        if numframes > maxframes: break

        print(f"Processing frame #{numframes}")

        ret, buffer = cv2.imencode('.jpg', frame)
        kafkaCli.send_message(buffer.tobytes())
        
    video.release()    


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--videofile", help="")
    parser.add_argument("--kafkatopic", help="")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    assert args.videofile, "pl profile filepath for the videofile to parse"
    assert args.kafkatopic
    stream_video_from_file(args.videofile, args.kafkatopic)