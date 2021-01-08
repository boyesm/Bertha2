# Code by Jarvis "Smelly" Coghlin and M-Dog
# The main function joins all of the useful functions into one coherent place
import sys
from init import init
# from cli_input import get_video_url
# from video_to_midi import video_to_midi
from pathlib import Path


if __name__ == "__main__":
    print("Starting Bertha2...")
    
    init()

    # start processes
    # exec(open("request_handler.py").read()) # stream chat bot
    exec(open("converter.py").read()) # converter process
    exec(open("livestream.py").read()) # livestream process
