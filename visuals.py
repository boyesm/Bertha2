import logging
import time
import asyncio
import simpleobsws
from pprint import *

# An example list of songs to show on the screen.
songs = ['Sexy frog',
         'Crazy frog',
         'Happy frog',
         'Yolo beans',
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
    pprint(ret)

    if ret.ok():  # Check if the request succeeded
        print(f"Request succeeded! Response data: {ret.responseData}")
    else:
        print("There was an error setting the text in OBS")

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
            'font': {
                'face': 'Helvetica',
                'size': '128',
            }
        }
    }

    # asyncio.run(update_obs_obj_args(change_arguments))
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(update_obs_obj_args(change_arguments))


async def change_video_source(media_name, media_filepath:str):
    """
    Changes the text of a Text object on the screen.
    :param media_name: The name of the Media object to change.
    :param media_filepath: The full filepath for the video that is going to be shown
    :return:
    """

    get_item_arguments = {
        'sceneName':SCENE_NAME,
        'sourceName':media_name,
    }

    # Use this as a reference for the different options available:
    #     https://github.com/Elektordi/obs-websocket-py/blob/e92960a475d3f1096a4ea41763cbc776b23f0a37/obswebsocket/requests.py#L1480
    change_arguments = {
        'inputName':'Video',
        'inputSettings':{
            'local_file':media_filepath,
            'width':VIDEO_WIDTH,
            'height':VIDEO_HEIGHT,
        }
    }

    asyncio.run(update_obs_obj_args(change_arguments))


def shorten_title(title):
    if len(title) > MAX_VIDEO_TITLE_LENGTH_QUEUE:
        title = title[0:(MAX_VIDEO_TITLE_LENGTH_QUEUE - 3)] + "..."

    return title


def update_playing_next(playing_next_object):

    # what does this do?: This function takes a list of the names of videos playing next and updates the next playing visual on the screen
    input_string = 'Videos playing next: \n'

    # TODO: remove the first item of the array, that's the currently playing video. ([1:])
    # TODO: only display the first 10 items.

    for video_title, index in enumerate(playing_next_object):
        input_string += f"{str(index)}. {shorten_title(video_title)}\n"

    change_text_obj_value('Queue', input_string)


def visuals_process(conn, video_name_q):
    # this process should control visuals.
    video_name_list = []

    while True:

        o = conn.recv()  # receive input from hardware on when to update

        print(f"VISUALS: Received object from hardware process {o}")

        # when input is received:
            # play next video
        # add that here
            # update play next
        video_name_list.append(o['title'])
        update_playing_next(video_name_list)
            # update currently playing
        change_text_obj_value('Current Song: ', video_name_list[0])



if __name__ == "__main__":
    change_text_obj_value("this_is_my_id", "this is some text")






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
