#!/bin/bash

docker exec -it $(docker ps -q -f "name=invoker_gui") bash