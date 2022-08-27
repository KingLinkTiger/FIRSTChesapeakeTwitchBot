import logging
import os
import random
import calendar

from dotenv import load_dotenv
from twitchio.ext import commands
from twitchio.ext import routines
from datetime import datetime, timedelta
from TwitchHTTPAPI import TwitchHTTPAPI
from FIRSTInspiresHTTPAPI import FIRSTInspiresHTTPAPI

class Bot(commands.Bot):
    def __init__(self):
        #28AUG22 - Get logging level from variable
        CHSLOGLEVEL =  os.environ.get('CHSLOGFOLDER', 'INFO').upper()

        #28AUG22 - Add LOGFOLDER Variable
        CHSLOGFOLDER = os.path.join(os.environ.get('CHSLOGFOLDER', '/var/log'), '') # https://stackoverflow.com/questions/2736144/python-add-trailing-slash-to-directory-string-os-independently

        #Start logging
        self.logger = logging.getLogger('FIRSTChesapeakeTwitchBot')
        self.logger.setLevel(level=CHSLOGLEVEL)

        if not os.path.exists(CHSLOGFOLDER):
            os.makedirs(CHSLOGFOLDER)

        fh = logging.FileHandler(CHSLOGFOLDER+"FIRSTChesapeakeTwitchBot.log")
        fh.setLevel(level=CHSLOGLEVEL)

        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        fh.setFormatter(formatter)

        self.logger.addHandler(fh)

        #Load Environment Variables from .env file
        load_dotenv()
        self.CLIENT_ID = os.getenv('TWITCH_CLIENT_ID').replace("'", "").replace('"', '')
        self.CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET').replace("'", "").replace('"', '')
        self.CHANNEL = os.getenv('CHANNEL').replace("'", "").replace('"', '')
        self.ACCESS_TOKEN = os.getenv('TWITCH_ACCESS_TOKEN').replace("'", "").replace('"', '')
        self.FRCEVENTS_KEY = os.getenv('FRCEVENTS_KEY').replace("'", "").replace('"', '')


        self.TwitchHTTPAPI = TwitchHTTPAPI()
        self.FIRSTInspiresHTTPAPI = FIRSTInspiresHTTPAPI(FRCEVENTS_KEY=self.FRCEVENTS_KEY)

        # Set Kickoff Date to None
        self.kickoffDate = None

        #Start the daily routine
        self.rDaily.start()

        #Run fDaily to reset everything on restart
        self.fDaily()

        super().__init__(
            token=self.ACCESS_TOKEN,
            client_id=self.CLIENT_ID,
            nick=os.getenv('BOT_NICK').replace("'", "").replace('"', ''),
            prefix=os.getenv('BOT_PREFIX').replace("'", "").replace('"', ''),
            initial_channels=[self.CHANNEL]
        )


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
        self.logger.debug("[cDonate] " + ctx.author.name + " invoked cDonate command.")
        await ctx.send("Donate to FIRST Chesapeake at https://www.firstchesapeake.org/donate")

    # YouTube Command
    @commands.command(name="YouTube", aliases=['yt'])
    async def cYouTube(self, ctx):
        if ctx.author.is_mod:
            self.logger.debug("[cYouTube] " + ctx.author.name + " invoked cYouTube command.")
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
            self.logger.debug("[cSurvey] " + ctx.author.name + " invoked cSurvey command.")
            listOfMessages = [
                "Team survey to provide information to the commentators: https://docs.google.com/forms/d/e/1FAIpQLSfpVK2WZ_viWGWH1toVCKgSnIBTWp22NLvs2UPugPsi0EY-JQ/viewform",
                "Attention Teams! Would you like to provide the commentators some additional information about your team? If so please fill out the following survey: https://docs.google.com/forms/d/e/1FAIpQLSfpVK2WZ_viWGWH1toVCKgSnIBTWp22NLvs2UPugPsi0EY-JQ/viewform"
            ]
            await ctx.send(random.choice(listOfMessages))

    # Request for Team Inforamtion Command
    @commands.command(name="teaminfo", aliases=['ti'])
    async def cTeamInfo(self, ctx):
        if ctx.author.is_mod:
            self.logger.debug("[cTeamInfo] " + ctx.author.name + " invoked cTeamInfo command.")
            listOfMessages = [
                "Teams, is your team name wrong? Before your next event make sure to update you team information in the FIRST Team Dashboard: https://my.firstinspires.org/Dashboard",
                "Attention Teams! Our systems are pulling data right from HQ so make sure to update your information in the FIRST Team Dashboard: https://my.firstinspires.org/Dashboard"
            ]
            await ctx.send(random.choice(listOfMessages))

    # Match Results Command
    @commands.command(name="matchresult", aliases=['matchresults', 'mr'])
    async def cMatchResult(self, ctx):
        if ctx.author.is_mod:
            self.logger.debug("[cMatchResult] " + ctx.author.name + " invoked cMatchResult command.")

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
            self.logger.debug("[cEventRankings] " + ctx.author.name + " invoked cEventRankings command.")

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
                        self.logger.debug("[cEventRankings] No ranking received!")

    # Websites Command
    @commands.command(name="website", aliases=['websites', 'w'])
    async def cWebsite(self, ctx):
        if ctx.author.is_mod:
            self.logger.debug("[cWebsite] " + ctx.author.name + " invoked cWebsite command.")
            listOfMessages = [
                #"https://www.firstchesapeake.org | https://events.firstchesapeake.org"
                "https://www.firstchesapeake.org"
            ]
            await ctx.send(random.choice(listOfMessages))

    # Ping Command
    @commands.command(name="ping")
    async def cPing(self, ctx):
        if ctx.author.is_mod:
            self.logger.debug("[cPing] " + ctx.author.name + " invoked cPing command.")
            await ctx.send("Pong")

    #Uptime Command
    @commands.command(name="uptime", aliases=['up'])
    async def cUptime(self, ctx):
        self.logger.debug("[cUptime] " + ctx.author.name + " invoked cUptime command.")
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
            self.logger.debug("[cGetAllDistrictEvents] " + ctx.author.name + " invoked cGetAllDistrictEvents command.")

            self.FIRSTInspiresHTTPAPI.update_AllDistrictEvents(districtCode="CHS")
            AllEvents = self.FIRSTInspiresHTTPAPI.get_TodaysDistrictEvents()

            if len(AllEvents) > 0:
                await ctx.send("SUCCESS! Received " + str(len(AllEvents)) + " events.")
                self.logger.info("[cGetTodaysDistrictEvents] SUCCESS! Monitoring " + str(len(TodaysEvents)) + " events.")

    #Get Today's Events
    @commands.command(name="cGetTodaysDistrictEvents")
    async def cGetTodaysDistrictEvents(self, ctx):
        if ctx.author.is_mod:
            self.logger.debug("[cGetTodaysDistrictEvents] " + ctx.author.name + " invoked cGetTodaysDistrictEvents command.")

            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            TodaysEvents = self.FIRSTInspiresHTTPAPI.get_TodaysDistrictEvents()

            if len(TodaysEvents) > 0:
                await ctx.send("SUCCESS! Monitoring " + str(len(TodaysEvents)) + " events.")
                self.logger.info("[cGetTodaysDistrictEvents] SUCCESS! Monitoring " + str(len(TodaysEvents)) + " events.")

    # Routine to run every day a little bit after midnight 
    @routines.routine(time=datetime(year=2022, month=1, day=1, hour=12, minute=55))
    async def rDaily(self):
        self.fDaily()

    # Function to stop all Event Day Routines
    def fDaily(self):      
        self.logger.info("[rDaily] Starting rDaily.")
        # Calculate Kickoff Date
        # First Staturday of January
        # Excluding If New Years is on Friday or Saturday, then following Saturday
        if self.kickoffDate == None:
            c = calendar.Calendar()
            for date in c.itermonthdates(datetime.today().date().year, 1):
                if date.day == 1 or date.day == 2: #If it is the first or second day of the month skip
                    continue
                if date.isoweekday() == 6: #If DOW is Sat
                    self.kickoffDate = date
                    self.logger.debug("[rDaily] Calculated KickOffDate: " + date.strftime("%m/%d/%Y"))
                    break

        # Week 1 = Kickoff + 8 Weeks
        Week1_START = self.kickoffDate + timedelta(weeks=8)
        Week1_END = Week1_START + timedelta(days=1)

        # Week 2 = Kickoff + 9 Weeks
        Week2_START = self.kickoffDate + timedelta(weeks=9)
        Week2_END = Week2_START + timedelta(days=1)

        # Week 3 = Kickoff + 10 Weeks
        Week3_START = self.kickoffDate + timedelta(weeks=10)
        Week3_END = Week3_START + timedelta(days=1)

        # Week 4 = Kickoff + 11 Weeks
        Week4_START = self.kickoffDate + timedelta(weeks=11)
        Week4_END = Week4_START + timedelta(days=1)

        # Week 5 = Kickoff + 12 Weeks
        Week5_START = self.kickoffDate + timedelta(weeks=12)
        Week5_END = Week5_START + timedelta(days=1)

        #DCMP
        #Week 6 = 13 Weeks
        Week6_START = self.kickoffDate + timedelta(weeks=13) - timedelta(days=3)
        Week6_END = self.kickoffDate + timedelta(weeks=13)

        #Week 7 = 14 Weeks
        Week7_START = self.kickoffDate + timedelta(weeks=14) - timedelta(days=3)
        Week7_END = self.kickoffDate + timedelta(weeks=14)

        #Week 8 = 15 Worlds
        #week 9 = 16 Worlds
        self.logger.debug("[rDaily] TODAY: " + datetime.today().date().strftime("%m/%d/%Y"))
        self.logger.debug("[rDaily] Calculated Week1_START: " + Week1_START.strftime("%m/%d/%Y"))
        self.logger.debug("[rDaily] Calculated Week2_START: " + Week2_START.strftime("%m/%d/%Y"))
        self.logger.debug("[rDaily] Calculated Week3_START: " + Week3_START.strftime("%m/%d/%Y"))
        self.logger.debug("[rDaily] Calculated Week4_START: " + Week4_START.strftime("%m/%d/%Y"))
        self.logger.debug("[rDaily] Calculated Week5_START: " + Week5_START.strftime("%m/%d/%Y"))
        self.logger.debug("[rDaily] Calculated Week6_START: " + Week6_START.strftime("%m/%d/%Y"))
        self.logger.debug("[rDaily] Calculated Week7_START: " + Week7_START.strftime("%m/%d/%Y"))

        today = datetime.today().date()

        if today >= Week1_START and today <= Week1_END: # It is week 1!
            self.logger.info("[rDaily] It is Week 1!")
            self.FIRSTInspiresHTTPAPI.update_AllDistrictEvents(districtCode="CHS") #Since it is week 1 sync all events from HQ
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay.start() # Start the routines for the day
        elif today >= Week2_START and today <= Week2_END: # It is week 2!
            self.logger.info("[rDaily] It is Week 2!")
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay.start() # Start the routines for the day
        elif today >= Week3_START and today <= Week3_END: # It is week 3!
            self.logger.info("[rDaily] It is Week 3!")
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay.start() # Start the routines for the day
        elif today >= Week4_START and today <= Week4_END: # It is week 4!
            self.logger.info("[rDaily] It is Week 4!")
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay.start() # Start the routines for the day
        elif today >= Week5_START and today <= Week5_END: # It is week 5!
            self.logger.info("[rDaily] It is Week 5!")
            #We do not normally have week 5 events but this will be a placeholder
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            #self.rStartEventDay.start() # Start the routines for the day
        elif today >= Week6_START and today <= Week6_END: # It is week 6 (DCMP 1)!
            self.logger.info("[rDaily] It is Week 6!")
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay.start() # Start the routines for the day
        elif today >= Week7_START and today <= Week7_END: # It is week 7 (DCMP 2)!
            self.logger.info("[rDaily] It is Week 7!")
            self.FIRSTInspiresHTTPAPI.update_TodaysDistrictEvents(districtCode="CHS")
            self.rStartEventDay.start() # Start the routines for the day
        else:
            self.logger.info("[rDaily] There is no event today. Stopping all relevant routines.")
            #Disable all routines!
            self.fStopEventDay

        #elif today >= Week8_START and today <= Week8_END: # It is week 8 (Worlds 1)! 
        #elif today >= Week9_START and today <= Week9_END: # It is week 9 (worlds 2)!

        self.logger.info("[rDaily] rDaily Has Finished.")

    # Routine to activiate Routines at the start of events
    @routines.routine(time=datetime(year=2022, month=1, day=1, hour=9, minute=0))
    async def rStartEventDay(self):
        self.rMatchResult.start()

    # Function to stop all Event Day Routines
    async def fStopEventDay(self):      
        self.rMatchResult.stop()

    # Command to run fDaily
    @commands.command(name="cDaily")
    async def cDaily(self, ctx):
        if ctx.author.is_mod:
            self.logger.info("[cDaily] Invoking fDaily.")
            self.fDaily()

    # Command to stop all Event Day Routines
    @commands.command(name="StopEvent")
    async def cStopEvent(self, ctx):
        if ctx.author.is_mod:
            await self.fStopEventDay

    # Match Results Routine Start Command
    @commands.command(name="rMatchResultStart")
    async def rMatchResultStart(self, ctx):
        if ctx.author.is_mod:
            await self.rMatchResult.start()

    # Match Results Routine Stop Command
    @commands.command(name="rMatchResultStop")
    async def rMatchResultStop(self, ctx):
        if ctx.author.is_mod:
            await self.rMatchResult.stop()

    # Match Results Routine WITHOUT CTX
    @routines.routine(minutes=20, iterations=None)
    async def rMatchResult(self):
        self.logger.debug("[rMatchResult] rMatchResult invoked.")
        
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
