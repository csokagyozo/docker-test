#!/bin/sh

docker network create docker-test_my_net
docker volume create docker-test_my_vol

docker run -v docker-test_my_vol:/vol --name helper busybox true
docker cp state.json helper:/vol
docker cp log.json helper:/vol
docker rm helper

docker-compose build
docker-compose up

