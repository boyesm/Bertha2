import logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig()
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

SCENE_NAME = 'Scene'
MEDIA_NAME = 'Video'
MAX_VIDEO_TITLE_LENGTH_QUEUE = 30
MAX_VIDEO_TITLE_LENGTH_CURRENT = 45
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720


parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks = False) # Create an IdentificationParameters object (optional for connecting)
ws = simpleobsws.WebSocketClient(url = 'ws://localhost:4455', identification_parameters = parameters) # Every possible argument has been passed, but none are required. See lib code for defaults.


async def change_text(input_name, input_string:str):
    """
    Changes the text of a Text object on the screen.
    :param input_name: The name of the Text object to change.
    :param input_string: The text to set for the input
    :return:
    """
    # print("Changing string in OBS to [", input_string + ']')

    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete

    get_item_arguments = {
        'sceneName':SCENE_NAME,
        'sourceName':input_name,
    }
    change_arguments = {
        'inputName':input_name,
        'inputSettings':{
            'text':input_string,
            # 'font':'Helvetica'

        }
    }


    # request = simpleobsws.Request('GetSceneItemId', get_item_arguments)
    # ret = await ws.call(request) # Perform the request
    # # pprint(ret)

    request = simpleobsws.Request('SetInputSettings', change_arguments)
    ret = await ws.call(request) # Perform the request
    # pprint(ret)


    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))
    else:
        print("There was an error setting the text in OBS")

    await ws.disconnect() # Disconnect from the websocket server cleanly


def update_song_queue(queue_object):

    input_string = 'Videos playing next: \n'
    index = 0
    for song in queue_object:
        index += 1
        if len(song) > MAX_VIDEO_TITLE_LENGTH_QUEUE:
            song = song[0:(MAX_VIDEO_TITLE_LENGTH_QUEUE-3)] + "..."
        input_string += str(index) + ". " + song + "\n"
    loop = asyncio.get_event_loop()
    loop.run_until_complete(change_text('Queue', input_string))


async def change_video_source(media_name, media_filepath:str):
    """
    Changes the text of a Text object on the screen.
    :param media_name: The name of the Media object to change.
    :param media_filepath: The full filepath for the video that is going to be shown
    :return:
    """
    # print("Changing string in OBS to [", input_string + ']')

    await ws.connect() # Make the connection to obs-websocket
    await ws.wait_until_identified() # Wait for the identification handshake to complete

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


    # request = simpleobsws.Request('GetInputSettings', get_item_arguments)
    # ret = await ws.call(request) # Perform the request
    # pprint(ret)

    request = simpleobsws.Request('SetInputSettings', change_arguments)
    ret = await ws.call(request) # Perform the request
    pprint(ret)


    if ret.ok(): # Check if the request succeeded
        print("Request succeeded! Response data: {}".format(ret.responseData))
    else:
        print("There was an error setting the text in OBS")

    await ws.disconnect() # Disconnect from the websocket server cleanly


if __name__ == "__main__":
    # while True:
        # input_string = input("Enter some text")

    # input_string = songs[0]
    # update_song_queue(songs)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(change_text('Current Song', 'Current song: ' + input_string))

    filepath1 = '/Users/owner/Downloads/Xie Hua Piao Piao Comes In Clutch.mp4'
    filepath2 = '/Users/owner/Downloads/Sledgehammer in office.mp4'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(change_video_source(MEDIA_NAME, filepath2))
