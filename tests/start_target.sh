#!/bin/bash
# Used for local development to quickly launch an SSH target.
# We need to publish the port, because Docker for Mac won't let you access a
# container using the IP address as of October 2019.
# https://docs.docker.com/docker-for-mac/networking/
if !(docker ps --format="{{.Names}}" | grep refit)
then docker run -d -p 22:22 --name=refit rastasheep/ubuntu-sshd
fi
