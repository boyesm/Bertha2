# Code by Jarvis "Smelly" Coghlin and M-Dog
# The main function joins all of the useful functions into one coherent place
from youtubedl import downloadvideo
import VideoQ

def main():

    print("Starting Bertha2 software integration...")


    #Arbitrary number of runs for testing. When running, this will be while True:
    for i in range(15):

        #FIXME Replace this input function with the input to get links
        link = input("Enter link:")

        if link != "n":

            if VideoQ.addVideo(link):

                print("Video added")

            else:

                print("Q FULL")
        else:

            VideoQ.nextVideo()


        link = ""
        VideoQ.printQ()


if __name__ == "__main__":
    main()