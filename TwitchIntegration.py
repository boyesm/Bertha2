import sys

#Code by Jarvis Coghlin

def getYoutubeLink():

    #The code that retrives the Youtube link to turn into MIDI
    youtubeLink = ""

    youtubeLink = input("Type the link here:\n")



    if youtubeLink != "":
        return True, youtubeLink
    else:
        return False
