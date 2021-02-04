import logging
import os

from dotenv import load_dotenv
from twitchio.ext import commands
from datetime import datetime
from TwitchHTTPAPI import TwitchHTTPAPI


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
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CHANNEL = os.getenv('CHANNEL')


# api token can be passed as test if not needed.
# Channels is the initial channels to join, this could be a list, tuple or callable
bot = commands.Bot(
    irc_token=os.getenv('TMI_TOKEN'),
    client_id=CLIENT_ID,
    nick=os.getenv('BOT_NICK'),
    prefix=os.getenv('BOT_PREFIX'),
    initial_channels=[CHANNEL]
)

TwitchHTTPAPI = TwitchHTTPAPI()


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
        await ctx.send("Please post your questions in Chat. You need to have a free account and follow us in order to post, so please do that now and join the conversation! Normal users can't post links in order to thwart evil doers. Sorry.")
        
#Tip/Donate Command
@bot.command(name="donate", aliases=['tip','tips'])
async def cDonate(ctx):
    logger.warning("[cDonate] " + ctx.author.name + " invoked cDonate command.")
    await ctx.send("Donate to FIRST Chesapeake at https://www.firstchesapeake.org/donate")

#Uptime Command
@bot.command(name="uptime", aliases=['up'])
async def cUptime(ctx):
    logger.warning("[cUptime] " + ctx.author.name + " invoked cUptime command.")
    getStreamsResponse = TwitchHTTPAPI.get_streams(
        user_login=CHANNEL
    )
    
    if getStreamsResponse != None:
        uptime = (datetime.now() - datetime.strptime(getStreamsResponse["started_at"], "%Y-%m-%dT%H:%M:%SZ")).total_seconds()
        
        hours = str(int(uptime/3600))
        minutes = str(int((uptime % 3600)/60))
        seconds = str(int((uptime % 60)))
        
        if uptime >= 3600:
            await ctx.send(CHANNEL + " has been streaming for " + hours + " hours " + minutes + " minuites and " + seconds + " seconds.")
        elif uptime >= 60 and uptime < 3600:
            await ctx.send(CHANNEL + " has been streaming for " + minutes + " minuites and " + seconds + " seconds.")
        else:
            await ctx.send(CHANNEL + " has been streaming for " + seconds + " seconds.")

bot.run()
