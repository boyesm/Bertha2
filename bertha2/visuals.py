import asyncio
from multiprocessing import connection

import simpleobsws

from bertha2.settings import cuss_words, solenoid_cooldown_s, scene_name, max_video_title_length_queue, video_width, \
    video_height, no_video_playing_text
from bertha2.utils.logs import initialize_module_logger, log_if_in_debug_mode
from bertha2.utils.obs import create_obs_websocket_client

logger = initialize_module_logger(__name__)
obs_ws_client = create_obs_websocket_client()

visuals_state = {
    "currently_displayed_status_text": no_video_playing_text,
    "currently_playing_video_path": "",
    "queued_video_metadata_objects": [],
    "is_bertha_on_cooldown": False,
    "does_next_up_need_update": True,
    "does_status_text_need_update": True
}



async def update_obs_obj_args(change_args):
    # This will error if OBS isn't running
    await obs_ws_client.connect()  # Make the connection to obs-websocket
    await obs_ws_client.wait_until_identified()  # Wait for the identification handshake to complete

    # The type of the input is "text_ft2_source_v2"
    request = simpleobsws.Request('SetInputSettings', change_args)
    ret = await obs_ws_client.call(request)  # Perform the request

    if ret.ok():  # Check if the request succeeded
        logger.debug(f"Request succeeded! Response data: {ret.responseData}")
    else:
        logger.warning(f"There was an error setting the text in OBS")

    await obs_ws_client.disconnect()  # Disconnect from the websocket server cleanly


def obs_change_text_source_value(text_obj_id, text_obj_value: str):

    get_item_arguments = {
        'sceneName': scene_name,
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
        'sceneName': scene_name,
        'sourceName': media_obj_id,
    }

    # Use this as a reference for the different options available:
    #     https://github.com/Elektordi/obs-websocket-py/blob/e92960a475d3f1096a4ea41763cbc776b23f0a37/obswebsocket/requests.py#L1480

    change_arguments = {
        'inputName': media_obj_id,
        'inputSettings': {
            'local_file': media_filepath,
            'width': video_width,
            'height': video_height,
        }
    }

    # TODO: replace this code with OBS update function
    loop = asyncio.get_event_loop()  # NOTE: Async function must be called like this.
    loop.run_until_complete(update_obs_obj_args(change_arguments))


def process_title(title: str):
    new_title = filter_cuss_words_from_title(title)
    new_title = shorten_title(title)
    return new_title


def filter_cuss_words_from_title(title: str):
    new_title = title
    for word in cuss_words:
        new_title = new_title.replace(word, "****")

    return new_title


def shorten_title(title: str):
    if len(title) > max_video_title_length_queue:
        title = title[0:(max_video_title_length_queue - 3)] + "..."

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

    logger.debug(f"Refreshed 'Next Up'.")


def update_onscreen_visuals_from_state():
    logger.debug("updating visuals")

    # UPDATE ANY VISUALS

    # update next up
    if visuals_state["does_next_up_need_update"]:
        update_playing_next([video['title'] for video in visuals_state["queued_video_metadata_objects"]])
        visuals_state["does_next_up_need_update"] = False

    # update status text at the bottom of the screen
    if visuals_state["does_status_text_need_update"]:
        #### THIS CAN BE A FUNC ####
        # update the video player and 'current video text'
        if visuals_state["is_bertha_on_cooldown"]:  # if b2 is cooling down, update this to the correct text
            visuals_state[
                "currently_displayed_status_text"] = f"Bertha2 is cooling down for the next {solenoid_cooldown_s} seconds, please wait."
            visuals_state["currently_playing_video_path"] = ""

        elif visuals_state["queued_video_metadata_objects"] != []:  # if there are videos in the queue
            visuals_state[
                "currently_displayed_status_text"] = f"Current Video: {visuals_state['queued_video_metadata_objects'][0]['title']}"
            visuals_state["currently_playing_video_path"] = visuals_state["queued_video_metadata_objects"][0][
                "filepath"]
            logger.debug(visuals_state["queued_video_metadata_objects"][0])

        elif visuals_state["queued_video_metadata_objects"] == []:  # there isn't any video to be played
            visuals_state["currently_displayed_status_text"] = no_video_playing_text
            visuals_state["currently_playing_video_path"] = ""

        obs_change_text_source_value("current_song", visuals_state["currently_displayed_status_text"])
        obs_change_video_source_value("playing_video", visuals_state["currently_playing_video_path"])

        visuals_state["does_status_text_need_update"] = False


def update_visual_state_with_new_converted_video(converted_video_metadata_object):
    visuals_state["queued_video_metadata_objects"].append(converted_video_metadata_object)
    logger.debug(f"conn.recv(): {converted_video_metadata_object}")
    visuals_state["does_next_up_need_update"] = True


def update_visual_state_with_bertha_status(bertha_playing_status):
    logger.debug(f"bertha_playing_status: {bertha_playing_status}")

    # bertha_playing_status will be "done" when video isn't playing (done and next video hasn't started yet)
    if len(visuals_state["queued_video_metadata_objects"]) > 0 and bertha_playing_status == "done":
        logger.info(f"Done playing file.")
        logger.debug(
            f"visuals_state['queued_video_metadata_objects']: {visuals_state['queued_video_metadata_objects']}")
        visuals_state["queued_video_metadata_objects"].pop(0)  # remove the video that has just been played
        visuals_state["does_next_up_need_update"] = True
        visuals_state["does_status_text_need_update"] = True
        visuals_state["is_bertha_on_cooldown"] = False

    # bertha_playing_status will be "wait" when a video is currently playing
    if bertha_playing_status == "wait":
        visuals_state["does_status_text_need_update"] = True
        visuals_state["is_bertha_on_cooldown"] = True


def visuals_process(converter_visuals_conn, hardware_visuals_conn):
    # this process controls livestream visuals.
    # CHECK FOR NEW INFORMATION FROM HARDWARE PROCESS AND OTHER PROCESSES

    # this receives all the latest processed data
    ## this is a connection (with converter), when data is available to be read, it is true.
    ## what is sent through this?:

    ##### process outline #####
    # update visuals

    # check if updates are needed
    # from converter process
    # from hardware process
    ## end

    log_if_in_debug_mode(logger, __name__)

    multiprocessing_connection_list = [converter_visuals_conn, hardware_visuals_conn]

    while True:

        update_onscreen_visuals_from_state()

        # if either (blocking) connection receives something, proceed.
        for current_connection in connection.wait(multiprocessing_connection_list, timeout=None):

            if current_connection == converter_visuals_conn:

                converted_video_metadata_object = current_connection.recv()  # receive object (containing video title and video filepath) from converter process
                update_visual_state_with_new_converted_video(converted_video_metadata_object)


            elif current_connection == hardware_visuals_conn:

                bertha_playing_status = current_connection.recv()  # this will be received once the hardware is done playing the video
                update_visual_state_with_bertha_status(bertha_playing_status)
