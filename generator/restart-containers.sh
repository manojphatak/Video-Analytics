#!/bin/bash

docker-compose stop
truncate -s 0 $(sudo docker inspect --format='{{.LogPath}}' movie-feeder)
truncate -s 0 $(sudo docker inspect --format='{{.LogPath}}' face-detector)
docker-compose up -d