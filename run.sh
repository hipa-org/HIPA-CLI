#!/usr/bin/env bash



if docker images hipa; then
    echo 'Found existing container'
     docker run -ti hipa
else
    echo 'No container hipa found'
    echo 'Creating new one'
    docker build -t hipa:hipa .
    docker run -ti hipa

fi






