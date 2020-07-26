## Video-Analytics
Horizontaly Scalable, Distributed system to churn out video feeds &amp; infer analytics

## References
- Face Detection library: https://ourcodeworld.com/articles/read/841/how-to-install-and-use-the-python-face-recognition-and-detection-library-in-ubuntu-16-04

## Run linter & style checker
```
pip install autopep8
autopep8 --in-place --aggressive --aggressive <filename>
```

## Usage
- Run Consumer
```
python video_consumer.py --knownfaces /home/manoj/Pictures/known_faces_empty --outpath /home/manoj/Pictures/out
```
- Run Streamer
```
python video_streamer.py
```


## Feature Backlog
- Set git workflows & commit to master

### Output unique faces 
- Run video consumer in non-blocking mode
- Output "unique" faces in the video. 
- Output "recognized" faces in the video. Create library of "known faces".
- Consume youtube video
- Consume CCTV feeds
- run pylint, formater, profiler
- Automated Tests
- Logging
- arg parser
