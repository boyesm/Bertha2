import logging
import time
import asyncio
import simpleobsws
from pprint import *
from os import getcwd

# An example list of songs to show on the screen.
songs = ['Sexy frog',
         'Sexy frog',
         'Crazy frog',
         'Happy frog',
         'Yolo beans',
         'Epic finger dance (Must watch!)',
         'Goodnight moon',
         '2203455',
         'video',
         '',
         'Epic finger dance (Must watch!)',
         'Goodnight moon',
         '2203455',
         'video',
         '',
         'Epic finger dance (Must watch!)',
         'Goodnight moon',
         '2203455',
         'video',
         '',
         ]

# TODO: Could these be added to settings?
SCENE_NAME = 'Scene'
MEDIA_NAME = 'Video'
MAX_VIDEO_TITLE_LENGTH_QUEUE = 45
MAX_VIDEO_TITLE_LENGTH_CURRENT = 45
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720

parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)
ws = simpleobsws.WebSocketClient(url = 'ws://localhost:4455', identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.

async def update_obs_obj_args(change_args):
    await ws.connect()  # Make the connection to obs-websocket
    await ws.wait_until_identified()  # Wait for the identification handshake to complete


    # request = simpleobsws.Request('GetSceneItemId', get_item_arguments)
    # ret = await ws.call(request) # Perform the request
    # # pprint(ret)
    # request = simpleobsws.Request('GetInputDefaultSettings', get_arguments)
    # ret = await ws.call(request) # Perform the request
    # pprint(ret)

    # The type of the input is "text_ft2_source_v2"
    request = simpleobsws.Request('SetInputSettings', change_args)
    ret = await ws.call(request)  # Perform the request
    # pprint(ret)

    '''
    if ret.ok():  # Check if the request succeeded
        print(f"Request succeeded! Response data: {ret.responseData}")
    else:
        print("There was an error setting the text in OBS")
    '''

    await ws.disconnect()  # Disconnect from the websocket server cleanly


def change_text_obj_value(text_obj_id, text_obj_value:str):
    """
    Changes the text of a Text object on the screen.
    :param text_obj_id: The name of the Media object to change.
    :param text_obj_value: The text to set for the input
    :return:
    """

    get_item_arguments = {
        'sceneName': SCENE_NAME,
        'sourceName': text_obj_id,
    }

    get_arguments = {
        'inputKind': "text_ft2_source_v2",
        'inputSettings': {
            'text': text_obj_value,
        }
    }

    change_arguments = {
        'inputName': text_obj_id,
        'inputSettings': {
            'text': text_obj_value,
            # 'font': {
            #     'face': 'Helvetica',
            #     'size': '128',
            # }
        }
    }

    loop = asyncio.get_event_loop()  # NOTE: Async function must be called like this.
    loop.run_until_complete(update_obs_obj_args(change_arguments))


def change_video_source(media_obj_id, media_filepath:str):

    get_item_arguments = {
        'sceneName':SCENE_NAME,
        'sourceName':media_obj_id,
    }

    # Use this as a reference for the different options available:
    #     https://github.com/Elektordi/obs-websocket-py/blob/e92960a475d3f1096a4ea41763cbc776b23f0a37/obswebsocket/requests.py#L1480

    change_arguments = {
        'inputName':media_obj_id,
        'inputSettings':{
            'local_file':media_filepath,
            'width':VIDEO_WIDTH,
            'height':VIDEO_HEIGHT,
        }
    }

    loop = asyncio.get_event_loop()  # NOTE: Async function must be called like this.
    loop.run_until_complete(update_obs_obj_args(change_arguments))

def process_title(title:str):
    new_title = filter_cuss_words(title)
    new_title = shorten_title(title)
    return new_title


def filter_cuss_words(title:str):
    new_title = title
    cuss_words = ["nigga", "nigger", "cunt", "fuck", "shit", "cracker", "incel", "virgin", "simp"] # TODO: add some more banned twitch words here
    for word in cuss_words:
        new_title = new_title.replace(word, "****")
    return new_title


def shorten_title(title:str):
    if len(title) > MAX_VIDEO_TITLE_LENGTH_QUEUE:
        title = title[0:(MAX_VIDEO_TITLE_LENGTH_QUEUE - 3)] + "..."

    return title


def update_playing_next(playing_next_list:list):

    # what does this do?: This function takes a list of the names of videos playing next and updates the next playing visual on the screen
    input_string = 'Next Up:\n'

    # TODO: remove the first item of the array, that's the currently playing video. ([1:])
    # TODO: only display the first 10 items.

    max_items = 5

    # TODO: **** out bad words

    for index, video_title in enumerate(playing_next_list):
        if (index < max_items) and (index > 0):
            input_string += f"{str(index+1)}. {process_title(video_title)}\n"

    if(len(playing_next_list) > max_items):
        input_string += f"{len(playing_next_list) - max_items} more video(s) queued..."

    change_text_obj_value('queue', input_string)


def visuals_process(conn, done_conn, video_name_q):
    # this process should control visuals.
    video_name_list = []  # TODO: merge this into l
    l = []

    while True:

        # this receives all the latest processed data
        while conn.poll():
            o = conn.recv()  # receive input from hardware on when to update
            video_name_list.append(o['title'])
            l.append(o)

        # TODO: only refresh when l has changed
        # print("VISUALS: Refreshing visuals.")
        # we always want to update the queue:
        update_playing_next(video_name_list)
        # we should always update the current song as well. just make sure video name list[0] is removed when the song is over
        if l != []:
            print(l[0])
            change_text_obj_value("current_song", f"Current Video: {l[0]['title']}")
            change_video_source("playing_video", l[0]["filepath"])
        else:
            change_text_obj_value("current_song", f"Current Video: not playing")
            change_video_source("playing_video", "")
        # all of this ^^ should happen at the same time this \/\/ is happening.

        if len(l) > 0:
            done_conn.recv() # this will be received once the hardware is done playing the video
            print("VISUALS: Done playing file.")
            l.pop(0) # remove the video that has just been played
            video_name_list.pop(0)

        time.sleep(0.5)



if __name__ == "__main__":
    # these are just some tests
    update_playing_next(songs)

    media_filepath = f"{getcwd()}/files/video/_I5pKnI-WJc.mp4"
    change_video_source("playing_video", media_filepath)


    # while True:
        # input_string = input("Enter some text")

    # input_string = songs[0]
    # update_song_queue(songs)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(change_text('Current Song', 'Current song: ' + input_string))

    # filepath1 = '/Users/owner/Downloads/Xie Hua Piao Piao Comes In Clutch.mp4'
    # filepath2 = '/Users/owner/Downloads/Sledgehammer in office.mp4'
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(change_video_source(MEDIA_NAME, filepath2))
