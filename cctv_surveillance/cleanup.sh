#!/bin/bash

# Stop all services
docker-compose stop

# Remove kafka topics related to our services (clean start)
docker exec kafka bash ./remove_all_topics.sh

# Clear prev logs in containers
#sudo bash ./clear-services-logs.sh
docker-compose rm -f

