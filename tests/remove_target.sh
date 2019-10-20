#!/bin/bash
if (docker ps --format="{{.Names}}" | grep refit)
then docker rm --force refit
fi
