import logging
import os
import requests
import json

from dotenv import load_dotenv
from datetime import datetime, timedelta

from dateutil import parser
from requests_cache import CachedSession

class FIRSTInspiresHTTPAPI:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger('FIRSTChesapeakeTwitchBot')

        self.FRCEVENTS_KEY = kwargs.get("FRCEVENTS_KEY", None)
        
        #if CLIENT_ID == None load it from ENV
        if self.FRCEVENTS_KEY == None:
            load_dotenv()
            self.FRCEVENTS_KEY = os.getenv('FRCEVENTS_KEY')

        #Initilize requests_cache to cache API calls
        self.session = CachedSession('FIRSTInspiresHTTPAPI', backend='sqlite')

        #temp
        logging.getLogger('requests_cache').setLevel('DEBUG')

        #Get Today's Events
        self.TodaysEvents = None
        self.AllDistrictEvents = None
        self.update_AllDistrictEvents(districtCode="CHS")
        self.update_TodaysDistrictEvents(districtCode="CHS")

        self.logger.debug("[FIRSTInspiresHTTPAPI] Instance Created")

    def get_FRCEventRankings(self, **kwargs):
        eventCode = kwargs.get("eventCode", None)

        if eventCode == None:
            self.logger.error("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Error: Event Code is None!")

        #Access the API
        try:
            apiheaders = {
                'Content-Type':'application/json',
                "Authorization" : "Basic " + self.FRCEVENTS_KEY
                #"If-Modified-Since" : datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT') #If-Modified-Since NOW (in GMT) # THIS BREAKS RANKINGS (Provides 200 result with empty response)
            }

            url = "https://frc-api.firstinspires.org/v3.0/2022/rankings/" + eventCode + "?top=5"
            
            self.logger.debug("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] " + url)

            with self.session.cache_disabled():
                response = self.session.get(url, headers=apiheaders, timeout=(3, 5))
            
        except(requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            self.logger.error("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Failed to contact FIRST INSPIRES API!")
        else:
            if response.status_code == 200:
                #200 - Success OK
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Response 200")
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Response Text: " + response.text)

                responseData = json.loads(response.text)

                return responseData["Rankings"]
            elif response.status_code == 304:
                #HTTP 304 - "Not Modified"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Response 304 - Data Not Modified")
            elif response.status_code == 400:
                #HTTP 400 - "Invalid Season Requested"/"Malformed Parameter Format In Request"/"Missing Parameter In Request"/"Invalid API Version Requested":
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Response 400")
            elif response.status_code == 401:
                #HTTP 401 - "Unauthorized"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Response 401")
            elif response.status_code == 404:
                #HTTP 404 - "Invalid Event Requested"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Response 404")
            elif response.status_code == 500:
                #HTTP 500 - "Internal Server Error"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Response 500")
            elif response.status_code == 501:
                #HTTP 501 - "Request Did Not Match Any Current API Pattern"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Response 501")
            elif response.status_code == 503:
                #HTTP 503 - "Service Unavailable"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Response 503")
            else:
                self.logger.error("[FIRSTInspiresHTTPAPI][get_FRCEventRankings] Invalid response from server.")

    def get_AllDistrictEvents(self):
        return self.AllDistrictEvents

    def update_AllDistrictEvents(self, **kwargs):
        tmpDistrictCode = kwargs.get("districtCode", None)
        if tmpDistrictCode == None:
            tmpDistrictCode = "CHS"

        #Access the API
        try:
            apiheaders = {
                'Content-Type':'application/json',
                "Authorization" : "Basic " + self.FRCEVENTS_KEY
            }
            url = "https://frc-api.firstinspires.org/v3.0/2022/events?districtCode=" + tmpDistrictCode
            
            self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] " + url)
            
            response = self.session.get(url, headers=apiheaders, timeout=3)
            
        except(requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            self.logger.error("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Failed to contact FIRST INSPIRES API!")
        else:
            if response.status_code == 200:
                #200 - Success OK
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Response 200")
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Response Text: " + response.text)
                responseData = json.loads(response.text)
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Received " + str(responseData["eventCount"]) + " events from API.")
                self.AllDistrictEvents = responseData
            elif response.status_code == 304:
                #HTTP 304 - "Not Modified"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Response 304 - Data Not Modified")
            elif response.status_code == 400:
                #HTTP 400 - "Invalid Season Requested"/"Malformed Parameter Format In Request"/"Missing Parameter In Request"/"Invalid API Version Requested":
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Response 400")
            elif response.status_code == 401:
                #HTTP 401 - "Unauthorized"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Response 401")
            elif response.status_code == 404:
                #HTTP 404 - "Invalid Event Requested"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Response 404")
            elif response.status_code == 500:
                #HTTP 500 - "Internal Server Error"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Response 500")
            elif response.status_code == 501:
                #HTTP 501 - "Request Did Not Match Any Current API Pattern"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Response 501")
            elif response.status_code == 503:
                #HTTP 503 - "Service Unavailable"
                self.logger.debug("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Response 503")
            else:
                self.logger.error("[FIRSTInspiresHTTPAPI][get_AllDistrictEvents] Invalid response from server.")

    def get_TodaysDistrictEvents(self, **kwargs):
        return self.TodaysEvents

    def update_TodaysDistrictEvents(self, **kwargs):

        tmpDistrictCode = kwargs.get("districtCode", None)

        if tmpDistrictCode == None:
            tmpDistrictCode = "CHS"

        if len(self.AllDistrictEvents) == 0:
            self.logger.debug("[FIRSTInspiresHTTPAPI][update_TodaysDistrictEvents] AllDistrictEvents is 0. Trying to get Events from FIRST")
            self.update_AllDistrictEvents(districtCode=tmpDistrictCode)
        
        if len(self.AllDistrictEvents) > 0:
            fResult = []

            for event in self.AllDistrictEvents["Events"]:
                self.logger.debug("[FIRSTInspiresHTTPAPI][update_TodaysDistrictEvents] Processing Event: " + event["name"])
                dateStart = parser.parse(event["dateStart"])
                dateEnd = parser.parse(event["dateEnd"])
                if dateStart <= datetime.now() <= dateEnd: # If NOW DATE is BETWEEN eventStart and End
                    if '#' in event["name"] and "Day" in event["name"]: # Contains '#' symbol and 'Day'
                        self.logger.debug("[FIRSTInspiresHTTPAPI][update_TodaysDistrictEvents] Today's Event")
                        fResult.append(event)
                    elif event["type"] == "DistrictChampionship":
                        self.logger.debug("[FIRSTInspiresHTTPAPI][update_TodaysDistrictEvents] DistrictChampionship Event")
                        fResult.append(event)
                    else: #skip
                        #Do nothing
                        self.logger.debug("[FIRSTInspiresHTTPAPI][update_TodaysDistrictEvents] Unwanted Event. Name/Type Not match")
                else:
                    self.logger.debug("[FIRSTInspiresHTTPAPI][update_TodaysDistrictEvents] Unwanted Event, not Today")

            self.TodaysEvents = fResult
            self.logger.info("[FIRSTInspiresHTTPAPI][update_TodaysDistrictEvents] Count of Today's Events: " + str(len(fResult)))
        else:
            self.logger.error("[FIRSTInspiresHTTPAPI][update_TodaysDistrictEvents] No Events to process!")


