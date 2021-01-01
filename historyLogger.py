import sys
import YoutubeIntegration
from datetime import datetime

#Code by Jarvis Coghlin

GLOGFILE = "Bertha2Log"

BLOGFILE = "Bertha2"


#Saves a log of each successful video played on Bertha2.
def saveGSongLog(link):

    try:
        with open(GLOGFILE, "a+") as f:
            f.write(link + '|' + YoutubeIntegration.getVideoName(link) + '|' + YoutubeIntegration.getNumViews(link))
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")

            f.write("Time:" + current_time + " " + datetime.date(datetime.now()))
    except:

        return False


# Saves a log of each unsuccessful video played on Bertha2.
def saveGSongLog(link):
    try:
        with open(GLOGFILE, "a+") as f:
            f.write(link + '|' + YoutubeIntegration.getVideoName(link) + '|' + YoutubeIntegration.getNumViews(link))
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")

            f.write("Time:" + current_time + " " + datetime.date(datetime.now()))

    except:

        return False