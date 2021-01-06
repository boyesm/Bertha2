# Code by Jarvis Coghlin
from video_dl import YVideo

QLENGTH = 10

Queue = []

def add_video_to_q(link):

    if len(Queue) < QLENGTH:

        Queue.append(YVideo(link))
        Queue[len(Queue)-1].downloadVideo()
        l = Queue[len(Queue)-1].convertVideoToMP3()

        return l

    else:

        return False

def nextVideo():

    Queue.pop(0)


def printQ():

    for i in range(len(Queue)):

        print(str(Queue[i]))





