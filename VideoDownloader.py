import sys
import YoutubeIntegration


#Downloads a youtube video based on the video link and a requested filename
def downloadVideo(YoutubeLink, Filename):

    # Retuns true or false based on if the download was sucsessful

    try:

        print("Downloading:", YoutubeLink)
        print("Title of video:", YoutubeIntegration.getVideoName(YoutubeLink))


        return True

    except:

        return False


