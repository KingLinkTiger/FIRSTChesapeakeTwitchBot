#!/bin/bash

echo "Stopping Container"
#Stop the container
docker stop firstchesapeaketwitchbot

echo "Removing Container"
#Remove the eventswebsite container
docker rm firstchesapeaketwitchbot

echo "Finding Container ID"
#Get the ID of the image used for portainer
#CONTAINERID="$(sudo docker ps -aqf "name=firstchesapeaketwitchbot")"

#echo "Removing Image"
#Remove the found image
#docker image rm "$CONTAINERID"

#Get the get the discord bot images and delete them
#Get new version number
VERSION="$(grep -i 'LABEL version=' Dockerfile | cut -d'"' -f2)"
SKIPIMAGE="$(docker image ls firstchesapeaketwitchbot:$VERSION -q)"

sudo docker image ls firstchesapeaketwitchbot -q | while read CONTAINERID ; do
    if [$CONTAINERID != $SKIPIMAGE]
    then
        docker image rm "$CONTAINERID"
    fi
done

#Pull the latest portainer image
docker build -t firstchesapeaketwitchbot:$VERSION /home/ryan/FIRSTChesapeakeTwitchBot

docker run -d \
-v /home/ryan/firstchesapeaketwitchbot_data/logs:/var/log/firstchesapeaketwitchbot \
--env-file /home/ryan/FIRSTChesapeakeTwitchBot/prod.env \
--name firstchesapeaketwitchbot  \
--restart unless-stopped \
firstchesapeaketwitchbot:$VERSION