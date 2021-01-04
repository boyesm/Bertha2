import sys
from pytube import YouTube
#Code by Jarvis Coghlin

#Code based off of pytube

class YVideo:

    VideoName = "N/A"

    def __init__(self, URL,downloaded=False):

        self.URL = URL

        self.downloaded = downloaded



    def downloadVideo(self):

        print("Video Downloaded")

    def getDownloaded(self):

        return downloaded

    def __repr__(self):

        return self.VideoName



