# FIRSTChesapeakeTwitchBot
Docker image to run the [FIRST Chesapeake](https://www.firstchesapeake.org/) [Twitch](https://twitch.tv/) Bot.

## INTRODUCTION
This is a Docker Image of a Twitch Bot for the FIRST Chesapeake Twitch Channel.

## INSTALLATION
1. Update the .env file with your API Keys and the Twitch Channel you want the bot to join.
2. Run the bot.
3. Enjoy

## VOLUMES
Description | Container Path
---- | ----
Logs | /var/log/firstchesapeaketwitchbot

## EXPOSE PORTS
None

## COMMANDS
Command | Description
---- | ----
!question/comment/qa | *MODERATOR COMMAND* Posts the boilerplate soliciting questions in chat.
!donate | Posts the link to donate to FIRST Chesapeake in the chat.
!uptime/up | Posts the update of the channel in the chat.

## CHANGES
Date | Description
---- | ----
30JAN21 | v1.0.0 - Initial Release
31JAN21 | Adding source files to Github and autobuild DockerHub
4FEB21 | Added Donate and Uptime commands. Started building out Twitch HTTP API as TwitchIO does not include it. (v1.0.1)