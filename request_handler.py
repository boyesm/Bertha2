# always waiting for web requests
# when a web request is received, user input is validated and sent to db


# when a 'play' command is received, validate the link, then send to db
import time
from sqlalchemy import create_engine
from global_vars import midi_file_path, audio_file_path, video_file_path, queue_table

engine = create_engine('sqlite:///bertha2.db')
conn = engine.connect()

def read_chat():
    user_input = input("Enter chat: ")

    # verify
    if check_if_youtube_link(user_input):
        print('valid input')
        create_row = queue_table.insert().values(username='malcolm', link=user_input, filename=get_file_name(user_input), isconverted=False, isqueued=False)
        conn.execute(create_row)
        # enter into db
    else:
        print('invalid input')



# def get_video_url():
#     user_input = input("Input YouTube link: ")
    
#     if check_if_youtube_link(user_input):
#         print("YouTube link was accepted")
#         return user_input
#     else:
#         print("Not recognized as a YouTube link, please try again.")
#         get_video_url()
#         return

def get_file_name(link):
    return link[32:43]


def check_if_youtube_link(user_input):
    start = user_input.find("https://www.youtube.com/watch?v=")
    if start == 0:
        return True
    else:
        return False

def check_if_valid_user(username): # only allow 1 upload per IP/User-agent per n minutes
    return True


while True:
    read_chat()