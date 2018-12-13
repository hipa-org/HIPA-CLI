#!/usr/bin/env bash

docker build -t hipa:latest .
docker run -ti hipa
