import logging
import os
import requests
import requests_cache
import json

from dotenv import load_dotenv
from datetime import datetime, timedelta

class TwitchHTTPAPI:
    def __init__(self, **kwargs):
        self.logger = logging.getLogger('FIRSTChesapeakeTwitchBot')
        
        self.accessToken = kwargs.get("accessToken", None)
        self.accessTokenExpirationTime = None
        
        
        self.CLIENT_ID = kwargs.get("CLIENT_ID", None)
        self.CLIENT_SECRET = kwargs.get("CLIENT_SECRET", None)
        
        #if CLIENT_ID == None load it from ENV
        if self.CLIENT_ID == None:
            load_dotenv()
            self.CLIENT_ID = os.getenv('CLIENT_ID')
        
        if self.CLIENT_SECRET == None:
            load_dotenv()
            self.CLIENT_SECRET = os.getenv('CLIENT_SECRET')  
        
        self.logger.debug("[TwitchHTTPAPI] Instance Created")
        
        if self.accessToken == None:
            self.getAccessToken()
        
    def getAccessToken(self):
        self.logger.debug("[TwitchHTTPAPI][getAccessToken] Trying to get access_token.")
    
        #Get first Access Token from Twitch
        try:
            apiheaders = {'Content-Type':'application/json'}
            
            url = "https://id.twitch.tv/oauth2/token"
            
            postData = {
                "client_id" : self.CLIENT_ID,
                "client_secret" : self.CLIENT_SECRET,
                "grant_type" : "client_credentials"
            }
            
            self.logger.debug("[TwitchHTTPAPI][getAccessToken] URL: " + url)
            self.logger.debug("[TwitchHTTPAPI][getAccessToken] PostData: ".join(postData))
            
            response = requests.post(url, data=postData, timeout=3)
        except(requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            #Server is offline and needs to be handled
            self.logger.error("[TwitchHTTPAPI][getAccessToken] Failed to contact Twitch API!")
        else:
            #We received a reply from the server
            if response.status_code == 200:
                responseData = json.loads(response.text)
                self.accessToken = responseData["access_token"]
                #Set expiration to NOW + Expires In time the API provided
                self.accessTokenExpirationTime = datetime.now() + timedelta(seconds=int(responseData["expires_in"]))
                self.logger.info("[TwitchHTTPAPI][getAccessToken] Received following access token: " + responseData["access_token"])
                self.logger.info("[TwitchHTTPAPI][getAccessToken] Received access token expires in: " + str(responseData["expires_in"]))
            elif response.status_code == 400:
                self.logger.error("[TwitchHTTPAPI][getAccessToken] Must include name as a parameter when requesting API key.")
            else:
                self.logger.warning("[TwitchHTTPAPI][getAccessToken] Invalid response from server.")

    #https://dev.twitch.tv/docs/api/reference#get-streams
    def get_streams(self, **kwargs):
        #Run the PreAPICalls Function before we try to access the APIs
        self.PreAPICalls()
        
        #Access the API
        try:
            apiheaders = {
                'Content-Type':'application/json',
                "Authorization" : "Bearer " + self.accessToken,
                "Client-Id" : self.CLIENT_ID
            }
            url = "https://api.twitch.tv/helix/streams?"+"".join(str(x) + "=" + str(y) for x, y in kwargs.items())
            
            self.logger.debug("[TwitchHTTPAPI][get_streams] "+ url)
            
            response = requests.get(url, headers=apiheaders, timeout=3)
            
        except(requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            self.logger.error("[TwitchHTTPAPI][get_streams] Failed to contact Twitch API!")
        else:
            if response.status_code == 200:
                #200 - Success OK
                self.logger.debug("[TwitchHTTPAPI][get_streams] Response 200")
                responseData = json.loads(response.text)
                self.logger.debug("[TwitchHTTPAPI][get_streams] Response Text: " + response.text)
                

                if len(responseData["data"]) == 0:
                    self.logger.debug("[TwitchHTTPAPI][get_streams] Streamer is not live.")
                    return None
                else:
                    self.logger.debug("[TwitchHTTPAPI][get_streams] Streamer started at: " + responseData["data"][0]["started_at"])
                    return responseData["data"][0]
                
            elif response.status_code == 400:
                #400 - Bad Request
                self.logger.debug("[TwitchHTTPAPI][get_streams] Response 400")
            elif response.status_code == 429:
                #429 - Too Many Requests (AKA Rate Limited)
                self.logger.debug("[TwitchHTTPAPI][get_streams] Response 429")
            else:
                self.logger.error("[TwitchHTTPAPI][get_streams] Invalid response from server.")
        
    def PreAPICalls(self):
        #Make sure we have an accessToken
        if self.accessToken == None:
            self.getAccessToken()
            
        #Make sure our accessToken is still active
        #If the current time is greaterthan or equal to the expiration time we must get a new token
        if datetime.now() >= self.accessTokenExpirationTime:
            self.getAccessToken()









