import argparse
from os import getcwd, getenv
from pathlib import Path

from dotenv import load_dotenv

cwd = getcwd()

solenoid_cooldown_s = 30

midi_file_path = cwd / Path("tmp-files") / Path("midi")
audio_file_path = cwd / Path("tmp-files") / Path("audio")
video_file_path = cwd / Path("tmp-files") / Path("video")

dirs = [midi_file_path, audio_file_path, video_file_path]  # add any other file paths to this variable

queue_save_file = "saved_queues"

channel = 'berthatwo'  # the channel of which chat is being monitored

load_dotenv("secrets.env")

# Twitch Secrets
nickname = getenv("NICKNAME")
token = getenv("TOKEN")
client_id = getenv("CLIENT_ID")

proxy_port = getenv("PROXY_PORT")
proxy_username = getenv("PROXY_USERNAME")
proxy_password = getenv("PROXY_PASSWORD")

cuss_words_file_name = "cuss_words.txt"

obs_websocket_url = 'ws://127.0.0.1:4444'

no_video_playing_text = "Nothing currently playing."

status_text_obs_source_id = "current_song"
playing_video_obs_source_id = "playing_video"

visuals_empty_queue_next_up_message = "Nothing queued."
visuals_nonempty_queue_header_message = "Next Up:"

default_visuals_state = {
    "currently_displayed_status_text": no_video_playing_text,
    "currently_playing_video_path": "",
    "currently_displayed_next_up": "",
    "queued_video_metadata_objects": [],  # 0th subscript in this list is the currently playing video
    "is_video_currently_playing": False,
    "is_bertha_on_cooldown": False,
    "does_next_up_need_update": True,
    "does_status_text_need_update": True
}


def import_cuss_words():
    global cuss_words

    try:
        with open(cuss_words_file_name) as f:
            words = f.read()
            word_list = words.split("\n")
            word_list = list(filter(None, word_list))  # Remove blank elements (e.g. "") from array
            return word_list
    except Exception as e:
        # TODO Log this
        print("CUSS WORDS NOT ENABLED")
        return []

cuss_words = import_cuss_words()

# Initialize command line args
parser = argparse.ArgumentParser(prog='Bertha2')
parser.add_argument('--disable_hardware', action='store_true')  # checks if the `--disable_hardware` flag is used
parser.add_argument("--log", action="store")
parser.add_argument("--debug_visuals", action='store_true')
parser.add_argument("--debug_converter", action='store_true')
parser.add_argument("--debug_hardware", action='store_true')
parser.add_argument("--debug_chat", action='store_true')

cli_args = parser.parse_args()

# Logging Formatter
# Easily create ANSI escape codes here: https://ansi.gabebanks.net
magenta = "\x1b[35;49;1m"
blue = "\x1b[34;49;1m"
green = "\x1b[32;49;1m"
reset = "\x1b[0m"
log_format = f"{blue}[%(levelname)s]{magenta}[%(name)s]{reset} %(message)s     {green}[%(filename)s:%(lineno)d]{reset}"

scene_name = 'Scene'
media_name = 'Video'
max_video_title_length_queue = 45
max_video_title_length_current = 45
video_width = 1280
video_height = 720
