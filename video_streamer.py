import os
import cv2

from config import topic, bootstrap_servers, testvideo
from kafka_client import KafkaImageCli

def stream_video_from_file(moviefile):
    kafkaCli = KafkaImageCli(bootstrap_servers= bootstrap_servers, topic= topic)
    
    assert os.path.exists(moviefile)
    video = cv2.VideoCapture(moviefile)
    
    numframes = 0
    maxframes = 5
    while(video.isOpened()):
        print(f"Processing frame #{numframes}")
        success, frame = video.read()
        if not success: break
            
        ret, buffer = cv2.imencode('.jpg', frame)
        kafkaCli.send_message(buffer.tobytes())
        
        numframes += 1
        if numframes > maxframes: break
        
    video.release()    


if __name__ == "__main__":
    stream_video_from_file(testvideo)