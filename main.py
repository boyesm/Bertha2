from VideoDownloader import YVideo
# Code by Jarvis Coghlin
# The main function joins all of the useful functions into one coherent place

import sys

def main():

    print("Testing VideoDownloader")

    link = input("Enter the link of the video:")

    YT = YVideo(link, False)

    print(YT, "was downloaded")
    print("Fun bug facts:")
    print("This video has",YT.getViews(), "views")


if __name__ == "__main__":

    main()
