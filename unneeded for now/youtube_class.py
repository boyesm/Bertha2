import sys, os, subprocess
from pytube import YouTube
from pathlib import Path
from moviepy.editor import *
from global_vars import midi_file_path, audio_file_path, video_file_path

# Code by Jarvis Coghlin
# Code based off of pytube

class YVideo:

    VideoName = "N/A"

    def __init__(self, youtube_url, downloaded=False):

        self.URL = youtube_url
        self.downloaded = downloaded # should this be a param?
        self.yt = YouTube(self.URL)
        self.file_name = self.URL[32:43] # is this always going to work?

    # def checkIfSafeforWork(self):
    #     if not self.yt.age_restricted:
    #         return True
    #     else:
    #         return False

    # def check_if_available(self): # implement this
    #     return True

    def downloadVideo(self): # Downloads the video if it hasn't been downloaded yet

        # try:

        print("Attempting to download:", self.yt)

        if self.downloaded == False:
            self.yt.streams.first().download(output_path=video_file_path, filename=self.file_name)
            self.downloaded = True
            print("Video Downloaded")
        else:
            print("Video already downloaded")

        # except:

        #     print("ERROR: FILE NOT DOWNLOADED")

    def convertVideoToMP3(self):

        # try:

        videoclip = VideoFileClip(str(video_file_path / (self.file_name + ".mp4"))) # str conversion + brackets are necessary

        audioclip = videoclip.audio
        audioclip.write_audiofile(str(audio_file_path / (self.file_name + ".mp3"))) # str conversion + brackets are necessary

        audioclip.close()
        videoclip.close()

        return

        # except:

        #     print("ERROR: FILE NOT CONVERTED")




    # def getDownloaded(self):
    #
    #     return self.downloaded

    # def getViews(self):
    #
    #     return self.yt.views

    # def __repr__(self):
    #
    #     #return (self.URL + "|" + self.yt.title)
    #     return ("Name: " + str(self.yt.title) + "| Views: " + str(self.yt.views) + "| Length: " + str(self.yt.length) + " seconds")



