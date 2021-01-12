# always checking db for updates
# when relevant updates are found, livestream gui is updated
# also responsible for playing audio and video
# tells vlc what to do

import time, os, sys
from global_vars import midi_file_path, audio_file_path, video_file_path, queue_table
from sqlalchemy import create_engine, select
from moviepy.editor import VideoFileClip

engine = create_engine('sqlite:///bertha2.db', connect_args={'timeout': 120})
conn = engine.connect() # create and connect to database here

queue = [] # queue stores file names
i = 0

if sys.platform == 'darwin':
    vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"
else if sys.plaform == 'win32': # this is untested !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    vlc_path = "C:\Program Files\VideoLAN\VLC"

def check_db_for_new_videos():
    s = select([queue_table])
    result = conn.execute(s)
    
    for row in result:
        if row['isqueued'] == 0 and row['isconverted'] == 1:
            queue.append(row['filename'])
            
            req = queue_table.update().where(queue_table.c.id == row['id']).values(isqueued=1)
            conn.execute(req)

            print(str(row['filename']) + " has been queued!!!")

            print("QUEUE LENGTH: " + str(len(queue)))
            print("ITER: " + str(i))

    result.close()


def start_new_video(file_name):
    clip = VideoFileClip(str(video_file_path / (file_name + ".mp4")))
    play_video(file_name)
    play_midi(file_name)
    time.sleep(clip.duration + 3)


def play_video(file_name):
    try:
        os.popen(str(vlc_path + " -f --video-on-top --no-audio --play-and-exit " + str(video_file_path / (file_name + ".mp4"))))
    except:
        print("CRITICAL: CHECK VLC FILE PATH VARIABLE AND MAKE SURE ITS CORRECT, from Malcolm")

def play_midi(file_name):
    try:
        os.popen(str(vlc_path + " --play-and-exit " + str(midi_file_path / (file_name + ".midi"))))
    except:
        print("CRITICAL: CHECK VLC FILE PATH VARIABLE AND MAKE SURE ITS CORRECT, from Malcolm")
    

while True:
    check_db_for_new_videos()
    if len(queue) > i:
        # print(" NEW VIDEO IS PLAYIGN ")
        start_new_video(queue[i])
        i+=1
    else:
        time.sleep(0.1)


# start_new_video("6XEwPMEUrM0")