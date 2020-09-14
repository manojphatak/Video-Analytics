#!/bin/bash

# time in secs
WAIT_FOR_SERVICES=$1
echo -e "Time to allow services to start consuming: $WAIT_FOR_SERVICES seconds"

GREEN="\e[1;32m"
RED="\e[1;31m"
MAGENDA="\e[1;35m"
RESET_COLOR="\e[0m"

# Get logs from the particular service & look if the log contains a specific content that we are expecting
CheckService() {
    SERVICE=$1
    PATT=$2

    LOG_OUTPUT=`docker-compose logs $SERVICE | cut -d ':' -f 5- | sort | uniq `
    if [[ "$LOG_OUTPUT" == *"$PATT"* ]]; 
    then
        echo -e "Service $MAGENDA $SERVICE: $GREEN pass $RESET_COLOR"
    else
        echo -e "Service $MAGENDA $SERVICE: $RED fail $RESET_COLOR"
    fi
}


# Stop all services
docker-compose stop

# Remove kafka topics related to our services (clean start)
docker exec kafka bash ./remove_all_topics.sh

# Clear prev logs in containers
#sudo bash ./clear-services-logs.sh
docker-compose rm -f


# Start the Services
docker-compose up -d

#wait for services to do work on test data (time in secs)
sleep $WAIT_FOR_SERVICES   

# Assertions
CheckService "movie-feeder" "got frame id#" 
CheckService "motion-detector" "detected contour of size" 
CheckService "object-detector" "text: person:" 
CheckService "face-detector" "detected a face" 
CheckService "face-matcher" "match found" 
CheckService "filesystem-consumer" "discovered so far... {" 

