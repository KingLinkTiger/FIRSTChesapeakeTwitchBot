import logging
import os
import random
import calendar

from dotenv import load_dotenv
from twitchio.ext import commands
from twitchio.ext import routines
from datetime import datetime
from TwitchHTTPAPI import TwitchHTTPAPI
from FIRSTInspiresHTTPAPI import FIRSTInspiresHTTPAPI

class Bot(commands.Bot):
    def __init__(self):
        #Start logging
        self.logger = logging.getLogger('FIRSTChesapeakeTwitchBot')
        self.logger.setLevel(logging.DEBUG)

        if not os.path.exists("/var/log/firstchesapeaketwitchbot"):
            os.makedirs("/var/log/firstchesapeaketwitchbot")

        fh = logging.FileHandler("/var/log/firstchesapeaketwitchbot/FIRSTChesapeakeTwitchBot.log")
        fh.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

        #Load Environment Variables from .env file
        load_dotenv()
        self.CLIENT_ID = os.getenv('CLIENT_ID')
        self.CLIENT_SECRET = os.getenv('CLIENT_SECRET')
        self.CHANNEL = os.getenv('CHANNEL')
        self.ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

        self.TwitchHTTPAPI = TwitchHTTPAPI()
        self.FIRSTInspiresHTTPAPI = FIRSTInspiresHTTPAPI()

        # Set Kickoff Date to None
        self.kickoffDate = None

        super().__init__(
            token=self.ACCESS_TOKEN,
            client_id=self.CLIENT_ID,
            nick=os.getenv('BOT_NICK'),
            prefix=os.getenv('BOT_PREFIX'),
            initial_channels=[self.CHANNEL]
        )

        #Start the daily routine
        self.rDaily.start()

    async def event_ready(self):
        self.logger.info("[event_ready] Bot " + self.nick + " has stated!") 

    async def event_message(self, message):
        self.logger.info(message.author.name + ": " + message.content)
    
        # If you override event_message you will need to handle_commands for commands to work.
        await self.handle_commands(message)

    # Register a command with the bot
    @commands.command(name='questions', aliases=['comments','qa'])
    async def CHSChatQandA(self, ctx):
        if ctx.author.is_mod:
            await ctx.send("Please post your questions in Chat. You need to have a free account and follow us in order to post, so please do that now and join the conversation! Normal users can't post links in order to thwart evil doers. Sorry.")
            
    #Tip/Donate Command
    @commands.command(name="donate", aliases=['tip','tips'])
    async def cDonate(self, ctx):
        self.logger.warning("[cDonate] " + ctx.author.name + " invoked cDonate command.")
        await ctx.send("Donate to FIRST Chesapeake at https://www.firstchesapeake.org/donate")

    # YouTube Command
    @commands.command(name="YouTube", aliases=['yt'])
    async def cYouTube(self, ctx):
        if ctx.author.is_mod:
            self.logger.warning("[cYouTube] " + ctx.author.name + " invoked cYouTube command.")
            listOfMessages = [
                "Official FIRST Chesapeake: https://www.youtube.com/firstchesapeake",
                "FIRST Chesapeake Individual Match Archive: https://www.youtube.com/channel/UCVwW9vgNGrnBXVYSJV-8vmg/playlists"
            ]
            for message in listOfMessages:
                await ctx.send(message)

    # Survey Command
    @commands.command(name="survey", aliases=['s'])
    async def cSurvey(self, ctx):
        if ctx.author.is_mod:
            self.logger.warning("[cSurvey] " + ctx.author.name + " invoked cSurvey command.")
            listOfMessages = [
                "Team survey to provide information to the commentators: https://docs.google.com/forms/d/e/1FAIpQLSfpVK2WZ_viWGWH1toVCKgSnIBTWp22NLvs2UPugPsi0EY-JQ/viewform",
                "Attention Teams! Would you like to provide the commentators some additional information about your team? If so please fill out the following survey: https://docs.google.com/forms/d/e/1FAIpQLSfpVK2WZ_viWGWH1toVCKgSnIBTWp22NLvs2UPugPsi0EY-JQ/viewform"
            ]
            await ctx.send(random.choice(listOfMessages))

    # Request for Team Inforamtion Command
    @commands.command(name="teaminfo", aliases=['ti'])
    async def cTeamInfo(self, ctx):
        if ctx.author.is_mod:
            self.logger.warning("[cTeamInfo] " + ctx.author.name + " invoked cTeamInfo command.")
            listOfMessages = [
                "Teams, is your team name wrong? Before your next event make sure to update you team information in the FIRST Team Dashboard: https://my.firstinspires.org/Dashboard",
                "Attention Teams! Our systems are pulling data right from HQ so make sure to update your information in the FIRST Team Dashboard: https://my.firstinspires.org/Dashboard"
            ]
            await ctx.send(random.choice(listOfMessages))

    # Match Results Command
    @commands.command(name="matchresult", aliases=['matchresults', 'mr'])
    async def cMatchResult(self, ctx):
        if ctx.author.is_mod:
            self.logger.warning("[cMatchResult] " + ctx.author.name + " invoked cMatchResult command.")

            TodaysEvents = self.FIRSTInspiresHTTPAPI.get_TodaysDistrictEvents()

            if len(TodaysEvents) > 0:
                for event in TodaysEvents:
                    message = "Looking for the match results or schedule for " + event["name"] + "? Visit https://frc-events.firstinspires.org/2022/" + event["code"] + ". The Match Results will automatically be updated after each match!"
                    await ctx.send(message)

            # FTC
            # listOfMessages = [
            #    "Looking for the match results for today’s events? Go to https://events.firstchesapeake.org/ and view the Match Schedule for an event. The website is being automatically updated with the results after each match!"
            #]

    # Event Rankings Command
    @commands.command(name="Rankings", aliases=['rank', 'ranks', 'r'])
    async def cEventRankings(self, ctx):
        if ctx.author.is_mod:
            self.logger.warning("[cEventRankings] " + ctx.author.name + " invoked cEventRankings command.")

            TodaysEvents = self.FIRSTInspiresHTTPAPI.get_TodaysDistrictEvents()

            if len(TodaysEvents) > 0:
                for event in TodaysEvents:
                    rankings = self.FIRSTInspiresHTTPAPI.get_FRCEventRankings(eventCode=event["code"])

                    if len(rankings) > 0:
                        await ctx.send("Current Rankings for " + event["name"])
                        for rank in rankings:
                            message = "#" + str(rank["rank"]) + ": " + str(rank["teamNumber"])
                            await ctx.send(message)
                        await ctx.send("For full rankings visit: https://frc-events.firstinspires.org/2022/" + event["code"] + "/rankings#district")
                    else:
                        self.logger.warning("[cEventRankings] No ranking received!")

    # Websites Command
    @commands.command(name="website", aliases=['websites', 'w'])
    async def cWebsite(self, ctx):
        if ctx.author.is_mod:
            self.logger.warning("[cWebsite] " + ctx.author.name + " invoked cWebsite command.")
            listOfMessages = [
                "https://www.firstchesapeake.org | https://events.firstchesapeake.org"
            ]
            await ctx.send(random.choice(listOfMessages))

    # Ping Command
    @commands.command(name="ping")
    async def cPing(self, ctx):
        if ctx.author.is_mod:
            self.logger.warning("[cPing] " + ctx.author.name + " invoked cPing command.")
            await ctx.send("Pong")

    #Uptime Command
    @commands.command(name="uptime", aliases=['up'])
    async def cUptime(self, ctx):
        self.logger.warning("[cUptime] " + ctx.author.name + " invoked cUptime command.")
        getStreamsResponse = TwitchHTTPAPI.get_streams(
            user_login=self.CHANNEL
        )
        
        if getStreamsResponse != None:
            uptime = (datetime.now() - datetime.strptime(getStreamsResponse["started_at"], "%Y-%m-%dT%H:%M:%SZ")).total_seconds()
            
            hours = str(int(uptime/3600))
            minutes = str(int((uptime % 3600)/60))
            seconds = str(int((uptime % 60)))
            
            if uptime >= 3600:
                await ctx.send(self.CHANNEL + " has been streaming for " + hours + " hours " + minutes + " minuites and " + seconds + " seconds.")
            elif uptime >= 60 and uptime < 3600:
                await ctx.send(self.CHANNEL + " has been streaming for " + minutes + " minuites and " + seconds + " seconds.")
            else:
                await ctx.send(self.CHANNEL + " has been streaming for " + seconds + " seconds.")

    #region ====== ADMINISTRATION COMMANDS ======
    #Get Today's Events
    @commands.command(name="cGetAllDistrictEvents")
    async def cGetAllDistrictEvents(self, ctx):
        if ctx.author.is_mod:
            self.logger.warning("[cGetAllDistrictEvents] " + ctx.author.name + " invoked cGetAllDistrictEvents command.")

            self.FIRSTInspiresHTTPAPI.update_AllDistrictEvents(districtCode="CHS")
            AllEvents = self.FIRSTInspiresHTTPAPI.get_TodaysDistrictEvents()

            if len(AllEvents) > 0:
                await ctx.send("SUCCESS! Received " + str(len(AllEvents)) + " events.")

    #Get Today's Events
    @commands.command(name="cGetTodaysDistrictEvents")
    async def cGetTodaysDistrictEvents(self, ctx):
        if ctx.author.is_mod:
            self.logger.warning("[cGetTodaysDistrictEvents] " + ctx.author.name + " invoked cGetTodaysDistrictEvents command.")

            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            TodaysEvents = self.FIRSTInspiresHTTPAPI.get_TodaysDistrictEvents()

            if len(TodaysEvents) > 0:
                await ctx.send("SUCCESS! Monitoring " + str(len(TodaysEvents)) + " events.")

    # Routine to run every day a little bit after midnight 
    @routines.routine(time=datetime(year=2022, month=1, day=1, hour=12, minute=55))
    async def rDaily(self):
        # Calculate Kickoff Date
        # First Staturday of January
        # Excluding If New Years is on Friday or Saturday, then following Saturday
        if self.kickoffDate == None:
            c = calendar.Calendar()
            for date in c.itermonthdates(datetime.today().date().year, 1):
                if date.day == 1 or date.day == 2: #If it is the first or second day of the month skip
                    continue
                if date.weekday() == 5: #If DOW is Sat
                    self.kickoffDate = date
                    break

        # Week 1 = Kickoff + 6 Weeks
        Week1_START = kickoffDate + datetime.timedelta(weeks=6)
        Week1_END = Week1_START + datetime.timedelta(days=1)

        # Week 2 = Kickoff + 7 Weeks
        Week2_START = kickoffDate + datetime.timedelta(weeks=7)
        Week2_END = Week2_START + datetime.timedelta(days=1)

        # Week 3 = Kickoff + 8 Weeks
        Week3_START = kickoffDate + datetime.timedelta(weeks=8)
        Week3_END = Week3_START + datetime.timedelta(days=1)

        # Week 4 = Kickoff + 9 Weeks
        Week4_START = kickoffDate + datetime.timedelta(weeks=9)
        Week4_END = Week4_START + datetime.timedelta(days=1)

        # Week 5 = Kickoff + 10 Weeks
        Week5_START = kickoffDate + datetime.timedelta(weeks=10)
        Week5_END = Week5_START + datetime.timedelta(days=1)

        #DCMP
        #Week 6 = 11 Weeks
        Week6_START = kickoffDate + datetime.timedelta(weeks=11) - datetime.timedelta(days=3)
        Week6_END = kickoffDate + datetime.timedelta(weeks=11)

        #Week 7 = 12 Weeks
        Week7_START = kickoffDate + datetime.timedelta(weeks=12) - datetime.timedelta(days=3)
        Week7_END = kickoffDate + datetime.timedelta(weeks=12)

        #Week 8 = Worlds
        #week 9 = Worlds

        today = datetime.today().date()

        if today >= Week1_START and today <= Week1_END: # It is week 1! 
            self.FIRSTInspiresHTTPAPI.update_AllDistrictEvents(districtCode="CHS") #Since it is week 1 sync all events from HQ
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay # Start the routines for the day
        elif today >= Week2_START and today <= Week2_END: # It is week 2!
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay # Start the routines for the day
        elif today >= Week3_START and today <= Week3_END: # It is week 3!
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay # Start the routines for the day
        elif today >= Week4_START and today <= Week4_END: # It is week 4!
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay # Start the routines for the day
        elif today >= Week5_START and today <= Week5_END: # It is week 5!
            #We do not normally have week 5 events but this will be a placeholder
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            #self.rStartEventDay # Start the routines for the day
        elif today >= Week6_START and today <= Week6_END: # It is week 6 (DCMP 1)!
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay # Start the routines for the day
        elif today >= Week7_START and today <= Week7_END: # It is week 7 (DCMP 2)!
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay # Start the routines for the day
        else:
            #Disable all routines!
            self.fStopEventDay
        #elif today >= Week8_START and today <= Week8_END: # It is week 8 (Worlds 1)! 
        #elif today >= Week9_START and today <= Week9_END: # It is week 9 (worlds 2)! 
        
    # Routine to activiate Routines at the start of events
    @routines.routine(time=datetime(year=2022, month=1, day=1, hour=9, minute=0))
    async def rStartEventDay(self):
        self.rMatchResult.start()

    # Function to stop all Event Day Routines
    async def fStopEventDay(self):      
        self.rMatchResult.stop()

    # Command to stop all Event Day Routines
    @commands.command(name="StopEvent")
    async def cStopEvent(self, ctx):
        if ctx.author.is_mod:
            self.fStopEventDay

    # Match Results Routine Start Command
    @commands.command(name="rMatchResultStart")
    async def rMatchResultStart(self, ctx):
        if ctx.author.is_mod:
            self.rMatchResult.start()

    # Match Results Routine Stop Command
    @commands.command(name="rMatchResultStop")
    async def rMatchResultStop(self, ctx):
        if ctx.author.is_mod:
            self.rMatchResult.stop()

    # Match Results Routine WITHOUT CTX
    @routines.routine(minutes=20, iterations=None)
    async def rMatchResult(self):
        self.logger.warning("[rMatchResult] rMatchResult invoked.")
        
        # Get channel based on bot's name
        c = bot.get_channel(self.CHANNEL)
        
        TodaysEvents = self.FIRSTInspiresHTTPAPI.get_TodaysDistrictEvents()

        if len(TodaysEvents) > 0:
            for event in TodaysEvents:
                message = "Looking for the match results or schedule for " + event["name"] + "? Visit https://frc-events.firstinspires.org/2022/" + event["code"] + ". The Match Results will automatically be updated after each match!"
                await c.send(message)

    #endregion 
bot = Bot()
bot.run() # bot.run() is blocking and will stop execution of any below code here until stopped or closed.
