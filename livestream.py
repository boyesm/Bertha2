# always checking db for updates
# when relevant updates are found, livestream gui is updated
# also responsible for playing audio and video
# tells vlc what to do

import vlc, time
from global_vars import midi_file_path, audio_file_path, video_file_path, queue_table
from sqlalchemy import create_engine, select

vlc_instance = vlc.Instance()

video_player = vlc_instance.media_player_new()
midi_player = vlc_instance.media_player_new()
video_player.audio_set_volume(0)

engine = create_engine('sqlite:///bertha2.db')
conn = engine.connect()

queue = [] # queue stores file names
i = 0

def check_db_for_new_videos():
    s = select([queue_table])
    result = conn.execute(s)
    for row in result:
        # print(row)
        if row['isqueued'] == 0:
            queue.append(row['filename'])
    
    # req = queue_table.update().values(isqueued=1)
    # conn.execute(req)

    # print(queue)


def start_new_video(file_name):

    video = vlc_instance.media_new(str(video_file_path / (file_name + ".mp4")))
    midi = vlc_instance.media_new(str(midi_file_path / (file_name + ".midi")))
    # video_player = vlc_instance.media_player_new()
    # midi_player = vlc_instance.media_player_new()
    video_player.set_media(video)
    midi_player.set_media(midi)
    video_player.play()
    midi_player.play()    
    
    time.sleep(0.3)
    # print((video_player.get_length()) / 1000)
    # print((midi_player.get_length()) / 1000)
    # time.sleep(10)
    time.sleep(video_player.get_length() / 1000)

# start_new_video("mJdeFEog-YQ")
# check_db_for_new_videos()

# while True:
#     check_db_for_new_videos()
#     if len(queue) > i:
#         start_new_video(queue[i])
#         i+=1
#     else:
#         # time.sleep(10)
#         break

start_new_video('mJdeFEog-YQ')