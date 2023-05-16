#!/bin/bash
sudo docker build . -f DockerfileApi -t api:01
sudo docker build . -f DockerfileFront -t front:01
sudo docker run -d -p 5000:5000 -p 8089:8089 api:01
sudo docker run -d -v /home/ubuntu/usuarios.csv -p 80:80 front:01
