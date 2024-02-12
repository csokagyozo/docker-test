docker volume create docker-test_my_vol

docker run -v docker-test_my_vol:/vol --name helper busybox true
docker cp change_detector/state.json helper:/vol
docker cp change_detector/log.json helper:/vol
docker rm helper

docker-compose up
