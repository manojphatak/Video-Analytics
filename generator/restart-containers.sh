#!/bin/bash

docker-compose stop
truncate -s 0 $(sudo docker inspect --format='{{.LogPath}}' movie-feeder)
truncate -s 0 $(sudo docker inspect --format='{{.LogPath}}' face-detector)
truncate -s 0 $(sudo docker inspect --format='{{.LogPath}}' filesystem-consumer)
docker-compose up -d