#!/bin/bash

faces=`docker-compose logs face-matcher | cut -d ':' -f 5- | sort | uniq | grep "known faces"`
patt="known faces"
if [[ "$faces" == *"$pat"* ]]; 
then
    echo -e "Service face-matcher: \e[1;32mPASSED \e[0m"
else
    echo -e "Service face-matcher: FAILED"
fi


