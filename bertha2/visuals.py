from multiprocessing import connection

from bertha2.settings import cuss_words, solenoid_cooldown_s, max_video_title_length_queue, no_video_playing_text, \
    status_text_obs_source_id, playing_video_obs_source_id, visuals_nonempty_queue_header_message, visuals_empty_queue_next_up_message, default_visuals_state
from bertha2.utils.logs import initialize_module_logger, log_if_in_debug_mode
from bertha2.utils.obs import update_obs_text_source_value, update_obs_video_source_value

logger = initialize_module_logger(__name__)

visuals_state = default_visuals_state

def filter_cuss_words_from_title(title: str):
    new_title = title
    for word in cuss_words:
        new_title = new_title.replace(word, "****")

    return new_title


def shorten_title(title: str):
    if len(title) > max_video_title_length_queue:
        title = title[0:(max_video_title_length_queue - 3)] + "..."

    return title


def process_title(title: str):
    title = filter_cuss_words_from_title(title)
    title = shorten_title(title)
    return title

def convert_list_of_objects_into_list_of_strings(list_of_objects, key):
    return [object_in_list[key] for object_in_list in list_of_objects]


def create_playing_next_string(queued_video_titles: list):

    playing_next_string = f"{visuals_nonempty_queue_header_message}\n"
    most_queued_videos_to_display = 5

    for index, video_title in enumerate(queued_video_titles):
        # the second condition in this if statement does:
        # if a video is playing, generate next up from the 2nd video in the list instead of the 1st
        if (index < most_queued_videos_to_display) and (index >= (0 + visuals_state["is_video_currently_playing"])):
            playing_next_string += f"{str(index + 1 - visuals_state['is_video_currently_playing'])}. {process_title(video_title)}\n"

    if len(queued_video_titles) > most_queued_videos_to_display:
        playing_next_string += f"{len(queued_video_titles) - most_queued_videos_to_display} more video(s) queued..."

    if len(queued_video_titles) <= visuals_state['is_video_currently_playing']:
        playing_next_string += visuals_empty_queue_next_up_message

    return playing_next_string

def update_playing_next():

    queued_video_titles = convert_list_of_objects_into_list_of_strings(visuals_state["queued_video_metadata_objects"], "title")

    visuals_state["currently_displayed_next_up"] = create_playing_next_string(queued_video_titles)
    update_obs_text_source_value('queue', visuals_state["currently_displayed_next_up"])

    visuals_state["does_next_up_need_update"] = False

    logger.debug(f"Refreshed 'Next Up'.")


def update_status_text():
    if visuals_state["is_bertha_on_cooldown"]:
        visuals_state[
            "currently_displayed_status_text"] = f"Bertha2 is cooling down for the next {solenoid_cooldown_s} seconds, please wait."
        visuals_state["currently_playing_video_path"] = ""

    elif visuals_state["queued_video_metadata_objects"] != []:  # if there are videos in the queue
        visuals_state[
            "currently_displayed_status_text"] = f"Current Video: {visuals_state['queued_video_metadata_objects'][0]['title']}"
        visuals_state["currently_playing_video_path"] = visuals_state["queued_video_metadata_objects"][0][
            "filepath"]
        logger.debug(visuals_state["queued_video_metadata_objects"][0])

    elif visuals_state["queued_video_metadata_objects"] == []:  # there aren't any videos to be played
        visuals_state["currently_displayed_status_text"] = no_video_playing_text
        visuals_state["currently_playing_video_path"] = ""

    update_obs_text_source_value(status_text_obs_source_id, visuals_state["currently_displayed_status_text"])
    update_obs_video_source_value(playing_video_obs_source_id, visuals_state["currently_playing_video_path"])

    visuals_state["does_status_text_need_update"] = False


def update_onscreen_visuals_from_state():
    logger.debug("updating visuals")

    # update next up
    if visuals_state["does_next_up_need_update"]:
        update_playing_next()

    # update status text at the bottom of the screen
    if visuals_state["does_status_text_need_update"]:
        update_status_text()


def update_visuals_state_with_new_video(converted_video_metadata_object):
    visuals_state["queued_video_metadata_objects"].append(converted_video_metadata_object)
    visuals_state["does_next_up_need_update"] = True


def update_visuals_state_with_new_bertha_status(bertha_playing_status):
    logger.debug(f"bertha_playing_status: {bertha_playing_status}")

    if bertha_playing_status == "playing":
        visuals_state["is_video_currently_playing"] = True
        visuals_state["is_bertha_on_cooldown"] = False

    elif bertha_playing_status == "cooldown":
        visuals_state["is_video_currently_playing"] = False
        visuals_state["is_bertha_on_cooldown"] = True

        if len(visuals_state["queued_video_metadata_objects"]) > 0:  # this should always be true
            visuals_state["queued_video_metadata_objects"].pop(0)  # remove the video that has just been played

    elif bertha_playing_status == "waiting":
        visuals_state["is_video_currently_playing"] = False
        visuals_state["is_bertha_on_cooldown"] = False

    # always update next up and status text
    visuals_state["does_next_up_need_update"] = True
    visuals_state["does_status_text_need_update"] = True


def visuals_process_loop(multiprocessing_connection_list):

    # if either (blocking) connection receives something, proceed.
    for current_connection in connection.wait(multiprocessing_connection_list, timeout=None):

        if current_connection == multiprocessing_connection_list[0]:

            converted_video_metadata_object = current_connection.recv()  # receive object (containing video title and video filepath) from converter process
            update_visuals_state_with_new_video(converted_video_metadata_object)

        elif current_connection == multiprocessing_connection_list[1]:

            bertha_playing_status = current_connection.recv()  # this will be received once the hardware is done playing the video
            update_visuals_state_with_new_bertha_status(bertha_playing_status)

    update_onscreen_visuals_from_state()


def visuals_process(converter_visuals_conn, hardware_visuals_conn,):

    log_if_in_debug_mode(logger, __name__)

    multiprocessing_connection_list = [converter_visuals_conn, hardware_visuals_conn]

    # initialize onscreen visuals from default state
    update_onscreen_visuals_from_state()

    while True:

        visuals_process_loop(multiprocessing_connection_list)




if __name__ == "__main__":

    queued_video_titles_case_1 = [
        "10 Surprising Facts About the Universe",
        "Cooking Tutorial: How to Make Delicious Brownies",
        "Exploring Abandoned Places: Haunted Mansion",
        "My Fitness Journey: How I Lost 20 Pounds in 2 Months",
        "Interview with a Celebrity: Behind the Scenes",
        "10 Life Hacks Everyone Should Know",
        "Travel Vlog: Exploring the Streets of Tokyo",
        "DIY Home Decor: How to Upcycle Old Furniture",
        "Top 5 Best Movies of the Year So Far",
        "Reacting to TikTok Trends: Hilarious Compilation"
    ]

    visuals_state["is_video_currently_playing"] = True

    print(create_playing_next_string(queued_video_titles_case_1))
