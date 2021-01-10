# always checking db for updates
# when relevant updates are found, livestream gui is updated
# also responsible for playing audio and video
# tells vlc what to do

import time, os
from global_vars import midi_file_path, audio_file_path, video_file_path, queue_table
from sqlalchemy import create_engine, select
from moviepy.editor import VideoFileClip

engine = create_engine('sqlite:///bertha2.db')
conn = engine.connect()

queue = [] # queue stores file names
i = 0

vlc_path = "/Applications/VLC.app/Contents/MacOS/VLC"

def check_db_for_new_videos(): # make sure videos are converted as wel!!!!!
    s = select([queue_table])
    result = conn.execute(s)
    for row in result:
        # print(row)
        if row['isqueued'] == 0 and row['isconverted'] == 1:
            queue.append(row['filename'])
    
            req = queue_table.update().where(queue_table.c.id == row['id']).values(isqueued=1)
            conn.execute(req)

    # print(queue)


def start_new_video(file_name):
    clip = VideoFileClip(str(video_file_path / (file_name + ".mp4")))
    play_video(file_name)
    play_midi(file_name)
    time.sleep(clip.duration + 10)


def play_video(file_name):
    os.popen(str(vlc_path + " -f --video-on-top --no-audio " + str(video_file_path / (file_name + ".mp4"))))

    ## --play-and-exit
    ## --start-paused
    ## 

def play_midi(file_name):
    os.popen(str(vlc_path + " " + str(midi_file_path / (file_name + ".midi"))))
    

while True:
    check_db_for_new_videos()
    if len(queue) > i:
        start_new_video(queue[i])
        i+=1
    # else:
    #     time.sleep(0.1)


# start_new_video("mJdeFEog-YQ")