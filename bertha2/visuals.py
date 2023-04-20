# Built-in packages
import asyncio
import time

# Internal imports
from bertha2.settings import cuss_words, SOLENOID_COOLDOWN_SECONDS
from bertha2.utils.logs import initialize_module_logger, log_if_in_debug_mode

# External imports
import simpleobsws

logger = initialize_module_logger(__name__)

# TODO: Could these be added to settings?
SCENE_NAME = 'Scene'
MEDIA_NAME = 'Video'
MAX_VIDEO_TITLE_LENGTH_QUEUE = 45
MAX_VIDEO_TITLE_LENGTH_CURRENT = 45
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720

parameters = simpleobsws.IdentificationParameters(
    ignoreNonFatalRequestChecks=False)  # Create an IdentificationParameters object (optional for connecting)
obs_websocket = simpleobsws.WebSocketClient(url='ws://127.0.0.1:4444',
                                 identification_parameters=parameters)  # Every possible argument has been passed, but none are required. See lib code for defaults.


async def update_obs_obj_args(change_args):
    # This will error if OBS isn't running
    logger.info("Updating OBS objects")
    try:
        await obs_websocket.connect()  # Make the connection to obs-websocket
    except OSError:
        # This happens when OBS isn't open
        logger.critical("Could not connect to OBS. Is it open on your computer?")
        return
    except Exception:
        logger.critical("Could not connect to OBS.")
    await obs_websocket.wait_until_identified()  # Wait for the identification handshake to complete

    # The type of the input is "text_ft2_source_v2"
    request = simpleobsws.Request('SetInputSettings', change_args)
    ret = await obs_websocket.call(request)  # Perform the request

    if ret.ok():  # Check if the request succeeded
        logger.debug(f"Request succeeded! Response data: {ret.responseData}")
    else:
        logger.warning(f"There was an error setting the text in OBS")

    await obs_websocket.disconnect()  # Disconnect from the websocket server cleanly


def obs_change_text_source_value(text_obj_id, text_obj_value: str):

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

    # TODO: create a function for updating OBS and include this in it \/
    try:
        loop = asyncio.get_event_loop()  # NOTE: Async function must be called like this.
        loop.run_until_complete(update_obs_obj_args(change_arguments))
    except Exception as e:
        logger.warning(f"Unable to connect to OBS. Is it running right now?")


def obs_change_video_source_value(media_obj_id, media_filepath: str):
    get_item_arguments = {
        'sceneName': SCENE_NAME,
        'sourceName': media_obj_id,
    }

    # Use this as a reference for the different options available:
    #     https://github.com/Elektordi/obs-websocket-py/blob/e92960a475d3f1096a4ea41763cbc776b23f0a37/obswebsocket/requests.py#L1480

    change_arguments = {
        'inputName': media_obj_id,
        'inputSettings': {
            'local_file': media_filepath,
            'width': VIDEO_WIDTH,
            'height': VIDEO_HEIGHT,
        }
    }

    # TODO: replace this code with OBS update function
    loop = asyncio.get_event_loop()  # NOTE: Async function must be called like this.
    loop.run_until_complete(update_obs_obj_args(change_arguments))


def process_title(title: str):
    # new_title = filter_cuss_words(title)
    new_title = shorten_title(title)
    return new_title


def filter_cuss_words(title: str):
    new_title = title
    for word in cuss_words:
        new_title = new_title.replace(word, "****")

    return new_title


def shorten_title(title: str):
    if len(title) > MAX_VIDEO_TITLE_LENGTH_QUEUE:
        title = title[0:(MAX_VIDEO_TITLE_LENGTH_QUEUE - 3)] + "..."

    return title


def update_playing_next(playing_next_list: list):
    # what does this do?: This function takes a list of the names of videos playing next and
    #   updates the next playing visual on the screen
    input_string = 'Next Up:\n'

    max_items = 5

    for index, video_title in enumerate(playing_next_list):
        if (index < max_items) and (index > 0):
            input_string += f"{str(index)}. {process_title(video_title)}\n"

    if len(playing_next_list) > max_items:
        input_string += f"{len(playing_next_list) - max_items} more video(s) queued..."

    if len(playing_next_list) <= 1:
        input_string += "Nothing queued."

    obs_change_text_source_value('queue', input_string)


def visuals_process(converter_visuals_conn, hardware_visuals_conn, video_name_q):
    # this process should control livestream visuals.

    log_if_in_debug_mode(logger, __name__)

    no_video_playing_text = "Nothing currently playing."

    ## STATE variables & default values
    obs_current_status_text = no_video_playing_text
    obs_current_video_path = ""
    video_data_queue = []
    cooldown_bool = False
    update_next_up = True
    update_status_text = True

    ##

    while True:

        # CHECK FOR NEW INFORMATION FROM HARDWARE PROCESS AND OTHER PROCESSES

        # this receives all the latest processed data
        while converter_visuals_conn.poll():
            o = converter_visuals_conn.recv()  # receive input from hardware on when to update
            video_data_queue.append(o)
            logger.debug(f"conn.recv(): {o}")
            update_next_up = True

        # UPDATE ANY VISUALS

        # update next up
        if update_next_up:
            # update the on-screen list of videos that are playing next
            update_playing_next([video['title'] for video in video_data_queue])
            logger.debug(f"Refreshed 'Next Up'")

            update_next_up = False

        # update status text at the bottom of the screen
        if update_status_text:
            # update the video player and 'current video text'
            if cooldown_bool:  # if b2 is cooling down, update this to the correct text
                obs_current_status_text = f"Bertha2 is cooling down for the next {SOLENOID_COOLDOWN_SECONDS} seconds, please wait."
                obs_current_video_path = ""

            elif video_data_queue:  # if there are videos in the queue
                obs_current_status_text = f"Current Video: {video_data_queue[0]['title']}"
                obs_current_video_path = video_data_queue[0]["filepath"]

                logger.debug(video_data_queue[0])
            elif not video_data_queue:  # there isn't any video to be played
                obs_current_status_text = no_video_playing_text
                obs_current_video_path = ""

            obs_change_text_source_value("current_song", obs_current_status_text)
            obs_change_video_source_value("playing_video", obs_current_video_path)

            update_status_text = False

        # CHECK IF CURRENTLY PLAYING VIDEO IS DONE PLAYING YET

        if hardware_visuals_conn.poll():

            msg = hardware_visuals_conn.recv()  # this will be received once the hardware is done playing the video
            logger.debug(f"msg: {msg}")

            if len(video_data_queue) > 0 and msg == "done":
                logger.info(f"Done playing file.")
                logger.debug(f"video_data_queue: {video_data_queue}")
                video_data_queue.pop(0)  # remove the video that has just been played
                update_next_up = True
                update_status_text = True
                cooldown_bool = False

            if msg == "wait":
                update_status_text = True
                cooldown_bool = True

        time.sleep(0.5)
