#!/bin/sh
docker build . -t morskoi/geeksocks-mail-producer:$1
docker push morskoi/geeksocks-mail-producer:$1
