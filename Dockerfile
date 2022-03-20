# BUILD ENV
FROM python:3.8-slim-buster

LABEL version="2.0.25"
LABEL description="Docker image of the FIRST Chesapeake Twitch Bot."
LABEL maintainer="kinglinktiger@gmail.com"

# Set WORKDIR
WORKDIR /code

# Update PIP
RUN /usr/local/bin/python -m pip install --upgrade pip

# Copy the requirements file to the WORKDIR
COPY requirements.txt .

# Install the requirements
RUN pip install -r requirements.txt

# Copy the script source files to the WORKDIR
COPY src/ .

# Configure the volume for logging
#VOLUME firstchesapeaketwitchbot_data:/var/log/firstchesapeaketwitchbot

# Command to run on container start
CMD [ "python", "-u", "./bot.py" ]