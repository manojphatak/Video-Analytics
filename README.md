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
- Download YouTube Videos
```
sudo youtube-dl -F <url>   
sudo youtube-dl -f <id> url
```

- Delete earlier test message if required...
```
sudo docker exec -i -t -u root $(sudo docker ps | grep kafka_kafka | cut -d' ' -f1) /bin/bash   # take bash inside kafka container...

$KAFKA_HOME/bin/kafka-topics.sh --list  --bootstrap-server kafka:9092   # List the topics
$KAFKA_HOME/bin/kafka-topics.sh --delete --topic test1  --bootstrap-server kafka:9092  # Delete a topic
$KAFKA_HOME/bin/kafka-topics.sh --create --partitions 4 --bootstrap-server kafka:9092 --topic test
$KAFKA_HOME/bin/kafka-console-consumer.sh --from-beginning --bootstrap-server kafka:9092 --topic=test  # create a command-line consumer
$KAFKA_HOME/bin/kafka-console-producer.sh --broker-list kafka:9092 --topic=test  # create a command-line producer
```

- Run Consumer
```
python video_consumer.py --knownfaces /home/manoj/Pictures/known_faces_empty --outpath /home/manoj/Pictures/out --kafkatopic testimages2
```
- Run Streamer
```
python video_streamer.py --videofile "/home/manoj/Videos/YouTube/ShriyutGangadharTipre_ MarathiSerial.webm" --kafkatopic testimages2
```

## Feature Backlog
- Run tests outside container as well
- Cleanup: fix #todos
- docker-compose entrypoint: git pull