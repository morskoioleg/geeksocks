#!/bin/sh
docker build . -t morskoi/geeksocks-mail:$1
docker push morskoi/geeksocks-mail:$1
