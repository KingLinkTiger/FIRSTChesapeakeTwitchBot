# Changelog

All notable changes to the project will be documented in this file.

## [20.0.25] - 13MAR22
### Added
- YouTube Command to put the CHS YouTube links in chat.

## [20.0.24] - 13MAR22
### Changed
- cMatchResult - Fixed missing trailing slash in URL

## [20.0.23] - 13MAR22
### Changed
- bot.py - Accidently had two equal signs when initilizing kickoffDate.
- rDaily - Fixed kickoffDate to self.kickoffDate

## [20.0.22] - 13MAR22
### Changed
- Fixed bug in FIRSTInspiresHTTPAPI where called responseData before setting it.

## [20.0.21] - 13MAR22
### Changed
- Fixed init ordering of FIRSTInspiresHTTPAPI

## [20.0.20] - 13MAR22
### Changed
- Fixed routine datetimes. Accidently had datetime.datetime

## [20.0.19] - 13MAR22
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