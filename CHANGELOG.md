# Changelog

All notable changes to the project will be documented in this file.

## [2.0.40] - 27AUG22
### Added
- Checks to ensure FRCEVENTS_KEY and AllDistrictEvents were not equal to None. Raised errors if they are.

### Changed
- Fixed initialization of FRCEVENTS_KEY
- Version numbers to be consistant

## [2.0.39] - 27AUG22
### Changed
- Made environment variable initialization more bulletproof
- ACCESS_TOKEN, CLIENT_ID, and CLIENT_SECRET to TWITCH_ACCESS_TOKEN, TWITCH_CLIENT_ID, and TWITCH_CLIENT_SECRET to avoid conflicts
- Updated workflow to incorporate environment variable changes

## [2.0.38] - 26MAR22
### Changed
- FIRSTInspiresHTTPAPI update_TodaysDistrictEvents function to output the right logging.
- Added Debug output for Week 7 in fDaily

## [2.0.37] - 26MAR22
### Changed
- fDaily TimeDeltas to use correct numbers... Original were incorrect.

## [2.0.36] - 26MAR22
### Added
- Additional logging to fDaily to output what it calculates For Week 1-6 Start Dates

## [2.0.35] - 26MAR22
### Added
- Additional logging to fDaily to output what it calculates as KickoffDate

### Changed
- fDaily date.weekday check for 6 rather than 5 since Monday=0

## [2.0.34] - 26MAR22
### Changed
- datetime.timedelta to just timedelta to reflect the new import... 

## [2.0.33] - 26MAR22
### Added
- timedelta to the imports

## [2.0.32] - 26MAR22
### Changed
- Added self to all references to kickoffDate

## [2.0.31] - 26MAR22
### Changed
- Removed awaits related to fDaily...

## [2.0.30] - 26MAR22
### Changed
- Added Parenthasises to a function fall
- Added awaits because I missed them...

## [2.0.29] - 26MAR22
### Added
- fDaily To move the daily commands to a function that is reusable

### Changed
- cDaily to use fDaily
- Init to invoke fDaily

## [2.0.28] - 26MAR22
### Changed
- Init, moving rDaily to above init command.

## [2.0.27] - 26MAR22
### Added
- Added cDaily command to restart rDaily.

### Changed
- rDaily - Added additional logging
- Updated Base Image Version

## [2.0.26] - 19MAR22
### Changed
- cGetTodaysDistrictEvents and cGetAllDistrictEvents to also log success in the log file.

### Changed
- Website - Removed events website
- Updated requirements.txt
- Updated Python base image

## [2.0.25] - 13MAR22
### Added
- YouTube Command to put the CHS YouTube links in chat.

## [2.0.24] - 13MAR22
### Changed
- cMatchResult - Fixed missing trailing slash in URL

## [2.0.23] - 13MAR22
### Changed
- bot.py - Accidently had two equal signs when initilizing kickoffDate.
- rDaily - Fixed kickoffDate to self.kickoffDate

## [2.0.22] - 13MAR22
### Changed
- Fixed bug in FIRSTInspiresHTTPAPI where called responseData before setting it.

## [2.0.21] - 13MAR22
### Changed
- Fixed init ordering of FIRSTInspiresHTTPAPI

## [2.0.20] - 13MAR22
### Changed
- Fixed routine datetimes. Accidently had datetime.datetime

## [2.0.19] - 13MAR22
### Added
- get_AllDistrictEvents to retrieve and store all events for the district
- update_AllDistrictEvents
- update_TodaysDistrictEvents
- rStartEventDay - Routine to run actions at the start of an event (at 0900)
- fStopEventDay - Function to stop actions at the end of an event

### Changed
- Renamed get_TodaysEventRankings to get_FRCEventRankings as the function is agnostic
- Moved original code from get_AllDistrictEvents to update_AllDistrictEvents
- Moved original code from get_TodaysDistrictEvents to update_AllDistrictEvents
- get_AllDistrictEvents to just return the data stored in AllDistrictEvents
- get_TodaysDistrictEvents to just return the data stored in TodaysDistrictEvents
- rMatchResult to send message to channel without context 

## [2.0.18] - 12MAR22
### Changed
- Removed trailing slashes from URLs

## [2.0.17] - 12MAR22
### Added
- rMatchResultStop to stop the routine

### Changed
- Fixed Match Ranking Link

## [2.0.16] - 12MAR22
### Added
- rMatchResult to start the routine

## [2.0.14] - 12MAR22
### Added
- Ping Command
- Rankings Command
- Created CHANGELOG.md

### Changed
- Removed Changelog from README.md

## [2.0.2] - 12MAR22
### Changed
- Updated Twitch.IO and therefore had to update code to follow new format
- Updated Requirements.txt with the latest versions

## [2.0.0] - 12MAR22
### Added
- FIRST Inspires HTTP API Class
- Added FIRST RFC API Key to the environment file.

### Changed
- MatchResult command to utilize FIRST FRC API

## [1.0.2] - 6FEB21
### Added
- Survey Command
- Team Info Command
- Match Result Command
- Website Command

## [1.0.1] - 4FEB21
### Added
- Donate Command
- Uptime Command
- Twitch HTTP API Class because TwitchIO does not support HTTP API calls

## [1.0.0] - 31JAN21
### Added
- Adding source files to Github and autobuild DockerHub

## [1.0.0] - 30JAN21
- Initial Release