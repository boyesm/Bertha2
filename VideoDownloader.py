import sys
from pytube import YouTube
#Code by Jarvis Coghlin

#Code based off of pytube

class YVideo:

    VideoName = "N/A"

    def __init__(self, URL,downloaded=False):

        self.URL = URL
        self.downloaded = downloaded
        self.yt = YouTube(self.URL)



    def downloadVideo(self):

        print("Attempting to download:",self.yt)

        if self.downloaded == False:
            self.yt.streams.first().download()
            self.downloaded = True
            print("Video Downloaded")
        else:
            print("Video already downladed")




    def getDownloaded(self):

        return self.downloaded

    def getViews(self):

        return self.yt.views

    def __repr__(self):

        return self.URL



