#!/bin/bash

docker-compose stop
docker exec kafka bash remove_all_topics.sh
sudo bash ./restart-containers.sh
