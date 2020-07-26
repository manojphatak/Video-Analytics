import os
import cv2

from config import topic, bootstrap_servers, testvideo
from kafka_client import KafkaImageCli

def stream_video_from_file(moviefile):
    kafkaCli = KafkaImageCli(bootstrap_servers= bootstrap_servers, topic= topic, stop_iteration_timeout=3000)
    
    assert os.path.exists(moviefile)
    video = cv2.VideoCapture(moviefile)
    
    frames_to_skip = 25
    numframes = 0
    maxframes = frames_to_skip * 15
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


if __name__ == "__main__":
    stream_video_from_file(testvideo)