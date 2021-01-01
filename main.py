import sys
import TwitchIntegration
import YoutubeIntegration
import VideoDownloader
import historyLogger

#Code by Jarvis Coghlin
#
#The main function joins all of the useful functions into one coheirent place


def main():

    link = TwitchIntegration.getYoutubeLink()

    videoName = YoutubeIntegration.getVideoName(link)

    if VideoDownloader.downloadVideo(link, videoName.strip(" ")):
        historyLogger.saveGSongLog(link)
    else:
        historyLogger.saveBSongLog()

    print("The signal inforamtion is in the file: ", videoName.strip(" "),".txt", sep="")



if __name__ == "__main__"():

    main()
