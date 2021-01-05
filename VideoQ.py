#Code by Jarvis Coghlin
from VideoDownloader import YVideo


QLENGTH = 10

Queue = []

def addVideo(link):

    if len(Queue) < QLENGTH:

        Queue.append(YVideo(link))
        Queue[len(Queue)-1].downloadVideo()
        Queue[len(Queue)-1].convertVideoToMP3()

        return True

    else:

        return False

def nextVideo():

    Queue.pop(0)


def printQ():

    for i in range(len(Queue)):

        print(str(Queue[i]))





