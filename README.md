# docker-test

This is a small dummy project demonstrating basic features of docker, including networking, mounting volumes, running simple python scripts.

## overview

The idea is that we have some tasks with an incremented id. We process them keeping the order. The id of the latest task is stored in state.json. The id of the last processed task is stored in log.json. There are two python scripts running in containers: a change detector and a range printer. The change detector checks every 10 seconds the two json files if there are unprocessed tasks. If so, it sends a message to the range printer task, which first does the processing (printing the ids and thier sum), and then send a message back to the change detector, which updates the log file.

### network
The containers are connected to a custom local network. The messaging is done through sockets.  
see: https://docs.docker.com/network/

### volume
The two json files are stored in a volume, so they are saved after runs and we can access and modify them at testing.  
see: https://docs.docker.com/storage/volumes/

### create tasks
Update the index stored field in state.json or the last_processed field in log.json manually.

## how to run
If not interested in the details, just run ``docker_build_run.sh``  

Otherwise, starting with docker already installed:

``docker network create my_net``  
``docker volume create my_vol``  

copying the files to the volume can be hacky. If you have access to the folder, you can do it like this:
``cp *.py /var/lib/docker/volumes/my_vol/_data/``  

or you can use the docker api:
``docker run -v my_vol:/vol --name helper busybox true``  
``docker cp state.json helper:/vol``  
``docker cp log.json helper:/vol``  
``docker rm helper``  

### without docker-compose
then run paralelly in two terminal windows:

``cd range_printer``  
``docker image build . -t docker_network_test_2``  
``docker run --rm --network my_net --name docker-test_range_printer_1 docker_network_test_2``  

``cd change_detector``  
``docker image build . -t docker_network_test``  
``docker run --mount source=my_vol,target=/vol --network my_net docker_network_test``  

### with docker-compose
``docker-compose build``  
``docker-compose up``  
