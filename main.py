# Code by Jarvis "Smelly" Coghlin and M-Dog
# The main function joins all of the useful functions into one coherent place
import sys
from init import init
from cli_input import get_video_url
from video_to_midi import video_to_midi
from pathlib import Path


def main():
    print("Starting Bertha2 software integration...")

    # start processes
        # converter
        # website backend
        # livestream process


    init()

    youtube_url = get_video_url()

    video_to_midi(youtube_url)





if __name__ == "__main__":
    main()
