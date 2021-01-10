# Code by Jarvis "Smelly" Coghlin and M-Dog
# The main function joins all of the useful functions into one coherent place
import sys, os
from init import init
# from request_handler import get_video_url
# from converter import video_to_midi
# from livestream import start_new_video
from pathlib import Path


if __name__ == "__main__":
    print("Starting Bertha2...")
    
    init()

    # url = get_video_url()
    # file_name = video_to_midi(url)
    # start_new_video(file_name)


    # start processes
    os.popen('python3 livestream.py')
    os.popen('python3 converter.py')
    os.popen('python3 request_handler.py')
    # exec(open("request_handler.py").read()) # stream chat bot
    # exec(open("converter.py").read()) # converter process
    # exec(open("livestream.py").read()) # livestream process


