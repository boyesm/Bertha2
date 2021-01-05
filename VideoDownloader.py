import sys
import os
from pytube import YouTube
import subprocess
from moviepy.editor import *
#Code by Jarvis Coghlin

#Code based off of pytube

class YVideo:

    VideoName = "N/A"

    def __init__(self, URL,downloaded=False):

        self.URL = URL
        self.downloaded = downloaded
        self.yt = YouTube(self.URL)

    def checkIfSafeforWork(self):

        safe = False

        if not self.yt.age_restricted:
            safe = True
        else:
            safe = False

        return safe

    #Downloads the video if it hasn't been downloaded yet
    def downloadVideo(self):

        try:

            print("Attempting to download:",self.yt)

            if self.downloaded == False:
                self.yt.streams.first().download(output_path=(os.getcwd()+"/temp"))
                self.downloaded = True
                print("Video Downloaded")
            else:
                print("Video already downladed")

        except:

            print("ERROR: FILE NOT DOWNLOADED")

    def convertVideoToMP3(self):

        try:

            videoclip = VideoFileClip(os.path.join(os.getcwd(),"temp",self.yt.title + ".mp4"))

            audioclip = videoclip.audio
            audioclip.write_audiofile(os.path.join(os.getcwd(), "AudioFiles", self.yt.title + ".mp3"))

            audioclip.close()
            videoclip.close()

            #if os.path.exists(str(os.getcwd()+"/temp" + self.yt.title)):
                #os.remove(os.getcwd()+"/temp", self.yt.title)

        except:

            print("ERROR: FILE NOT CONVERTED")




    def getDownloaded(self):

        return self.downloaded

    def getViews(self):

        return self.yt.views

    def __repr__(self):

        #return (self.URL + "|" + self.yt.title)
        return ("Name: " + str(self.yt.title) + "| Views: " + str(self.yt.views) + "| Length: " + str(self.yt.length) + " seconds")



