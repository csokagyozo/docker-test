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
with docker already installed:

``docker network create my_net``  
``docker volume create my_vol``  
``cp *.py /var/lib/docker/volumes/my_vol/_data/``  

(evidently the path can be different)
then run paralelly in two terminal windows:

``cd range_printer``  
``sudo docker image build . -t docker_network_test_2``  
``sudo docker run --rm --network my_net --name consumer docker_network_test_2``  

``cd change_detector``  
``sudo docker image build . -t docker_network_test``  
``sudo docker run --mount source=my_vol,target=/vol --network my_net docker_network_test``  
