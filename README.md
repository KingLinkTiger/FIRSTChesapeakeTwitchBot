# FIRSTChesapeakeTwitchBot
Docker image to run the [FIRST Chesapeake](https://www.firstchesapeake.org/) [Twitch](https://twitch.tv/) Bot.

## INTRODUCTION
This is a Docker Image of a Twitch Bot for the FIRST Chesapeake Twitch Channel.

The bot will automatically get a list of today's events on startup!

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
!survey/s | *MODERATOR COMMAND* Posts the link to the team survey to chat.
!teaminfo/ti | *MODERATOR COMMAND* Posts a chat requesting teams to update their info in TIMS.
!matchresult/matchresults/mr | *MODERATOR COMMAND* Sends chats with links to the match results for each of today's events.
!website/websites/w | *MODERATOR COMMAND* Puts the URLs to the CHS and CHS Events website in chat.
!rankings/rank/ranks/r | *MODERATOR COMMAND* Sends chats with the top 5 rankings for each of today's events.
!ping | *MODERATOR COMMAND* Ping/Pong command to help ensure the box is alive.
!YouTube/yt | *MODERATOR COMMAND* Posts links you CHS YouTube Channels