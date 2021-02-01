import logging
import os

from dotenv import load_dotenv
from twitchio.ext import commands
from datetime import datetime


#Start logging
logger = logging.getLogger('FIRSTChesapeakeTwitchBot')
logger.setLevel(logging.DEBUG)

if not os.path.exists("/var/log/firstchesapeaketwitchbot"):
    os.makedirs("/var/log/firstchesapeaketwitchbot")

fh = logging.FileHandler("/var/log/firstchesapeaketwitchbot/FIRSTChesapeakeTwitchBot.log")
fh.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

#Load Environment Variables from .env file
load_dotenv()

# api token can be passed as test if not needed.
# Channels is the initial channels to join, this could be a list, tuple or callable
bot = commands.Bot(
    irc_token=os.getenv('TMI_TOKEN'),
    client_id=os.getenv('CLIENT_ID'),
    nick=os.getenv('BOT_NICK'),
    prefix=os.getenv('BOT_PREFIX'),
    initial_channels=[os.getenv('CHANNEL')]
)



# Register an event with the bot
@bot.event
async def event_ready():
    logger.info(f'Ready | {bot.nick}')


@bot.event
async def event_message(message):
    logger.info(message.author.name + ": " + message.content)

    # If you override event_message you will need to handle_commands for commands to work.
    await bot.handle_commands(message)


# Register a command with the bot
@bot.command(name='questions', aliases=['comments','qa'])
async def CHSChatQandA(ctx):
    if ctx.author.is_mod:
        await ctx.send(f"Please post your questions in Chat. You need to have a free account and follow us in order to post, so please do that now and join the conversation! Normal users can't post links in order to thwart evil doers. Sorry.")
        
bot.run()
