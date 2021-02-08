#!/bin/bash -v
docker-compose down
docker stop $(docker ps -aq)
docker rm $(docker ps -a -q)
#docker volume rm $(docker volume ls -q)
docker network prune -f
#docker rmi $(docker images -q)
