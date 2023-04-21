from os import getcwd, getenv, path
from pathlib import Path
import argparse
import pandas as pd
from dotenv import load_dotenv


def import_cuss_words(filename: str):
    with open(filename) as f:
        words = f.read()
        word_list = words.split("\n")
        word_list = list(filter(None, word_list))  # Remove blank elements (e.g. "") from array

        return word_list


# ================================
# Secrets
# ================================
load_dotenv("./secrets.env")


# ================================
# File paths
# ================================
cwd = getcwd()
MIDI_FILE_PATH = cwd / Path("tmp-files") / Path("midi")
AUDIO_FILE_PATH = cwd / Path("tmp-files") / Path("audio")
VIDEO_FILE_PATH = cwd / Path("tmp-files") / Path("video")
# midi_file_path = os.path.join(cwd, 'tmp-files', 'midi')
# audio_file_path = os.path.join(cwd, 'tmp-files', 'audio')
# video_file_path = os.path.join(cwd, 'tmp-files', 'video')
dirs = [MIDI_FILE_PATH, AUDIO_FILE_PATH, VIDEO_FILE_PATH]  # add any other file paths to this variable
queue_save_file = "saved_queues"


# ================================
# Twitch
# ================================
client_id = getenv("CLIENT_ID")
channel = 'berthatwo'  # the channel of which chat is being monitored
twitch_nickname = getenv("NICKNAME")
twitch_token = getenv("TOKEN")
if not twitch_token or not twitch_nickname:

    raise Exception("Couldn't load Twitch authentication info! Did you add secrets.env to the right location?")

# ================================
# Hardware
# ================================
SOLENOID_COOLDOWN_SECONDS = 30
STARTING_NOTE = 48
NUMBER_OF_NOTES = 48
arduino_connection = None
sock = None
HARDWARE_TEST_FLAG = False


# ================================
# Parser
# ================================
parser = argparse.ArgumentParser(prog='Bertha2')
parser.add_argument('--disable_hardware', action='store_true')  # Checks if the `--disable_hardware` flag is used
parser.add_argument('-l', "--log_to_file", action="store_true")
parser.add_argument("--log_level", action="store")  # The default logging level
parser.add_argument("--log_level_main", action="store")
parser.add_argument("--log_level_visuals", action="store")
parser.add_argument("--log_level_converter", action="store")
parser.add_argument("--log_level_hardware", action="store")
parser.add_argument("--log_level_chat", action="store")
cli_args = parser.parse_args()

# print(cli_args)

# ================================
# Other
# ================================
# Cuss words
CUSS_WORDS_FILE_NAME = "cuss_words.txt"
global cuss_words
cuss_words = import_cuss_words(CUSS_WORDS_FILE_NAME)
# Proxy
proxy_port = getenv("PROXY_PORT")
proxy_username = getenv("PROXY_USERNAME")
proxy_password = getenv("PROXY_PASSWORD")
# Make the terminal output wider
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 100)

MAX_YOUTUBE_VIDEO_LENGTH = 400

