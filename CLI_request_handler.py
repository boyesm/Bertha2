
import time, sys, requests
from sqlalchemy import create_engine
from global_vars import midi_file_path, audio_file_path, video_file_path, queue_table, tl
from pytube import YouTube, extract

engine = create_engine('sqlite:///bertha2.db', connect_args={'timeout': 120})
conn = engine.connect()

def get_file_name(link):
    return str(extract.video_id(link))

def check_if_valid_youtube_link(user_input):
    try:
        yt = YouTube(user_input) # YouTube("https://www.youtube.com/watch?v=KRbsco8M7Fc")
        yt.check_availability()
        if yt.length <= 180:
            return True
        else:
            return False
    except:
        return False


# this is disabled for testing
# while True:
#     link = input("enter a YouTube link: ")
#     if check_if_valid_youtube_link(link):
#         print('valid input!')
#         create_row = queue_table.insert().values(username='malcolm', link=link, filename=get_file_name(link), isconverted=False, isqueued=False)
#         conn.execute(create_row)
#     else:
#         print('invalid input :(')


def input_links(link):  # this is for testing purposes only
    if check_if_valid_youtube_link(link):
        print('valid input!')
        create_row = queue_table.insert().values(username='malcolm', link=link, filename=get_file_name(link), isconverted=False, isqueued=False)
        conn.execute(create_row)
    else:
        print('invalid input :(')


# run this file to simulate 5 links being added by users

input_links("https://www.youtube.com/watch?v=mJdeFEog-YQ")
input_links("https://www.youtube.com/watch?v=HHcgTbs7_Os")
input_links("https://www.youtube.com/watch?v=OnZn-ci3ImM")
input_links("https://www.youtube.com/watch?v=Srq1FqFPwj0")
input_links("https://www.youtube.com/watch?v=SmbmeOgWsqE")