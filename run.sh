docker volume create my_vol

docker run -v my_vol:/vol --name helper busybox true
docker cp state.json helper:/vol
docker cp log.json helper:/vol
docker rm helper

docker-compose up
