import os.path
from typing import Any

import argparse
from os import getcwd, getenv
from pathlib import Path

from dotenv import load_dotenv

cwd = getcwd()

solenoid_cooldown_s = 30

import pandas as pd
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 100)

midi_file_path = cwd / Path("tmp-files") / Path("midi")
# midi_file_path = os.path.join(cwd, 'tmp-files', 'midi')
audio_file_path = cwd / Path("tmp-files") / Path("audio")
video_file_path = cwd / Path("tmp-files") / Path("video")

dirs = [midi_file_path, audio_file_path, video_file_path]  # add any other file paths to this variable

queue_save_file = "saved_queues"
channel = 'berthatwo'  # the channel of which chat is being monitored

load_dotenv("./secrets.env")

# Twitch Secrets
twitch_nickname = getenv("NICKNAME")
twitch_token = getenv("TOKEN")
if not twitch_token or not twitch_nickname:

    raise Exception("Couldn't load Twitch authentication info! Did you add secrets.env to the right location?")

client_id = getenv("CLIENT_ID")

proxy_port = getenv("PROXY_PORT")
proxy_username = getenv("PROXY_USERNAME")
proxy_password = getenv("PROXY_PASSWORD")

cuss_words_file_name = "cuss_words.txt"


def import_cuss_words():

    with open(cuss_words_file_name) as f:
        words = f.read()
        word_list = words.split("\n")
        word_list = list(filter(None, word_list))  # Remove blank elements (e.g. "") from array

        return word_list


global cuss_words
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
# log_format = f"{blue}[%(levelname)-10s]{magenta}[%(name)-20s]{reset} %(message)-70s     {green}[%(filename)s:%(lineno)d]{reset}"
# This format is aligned for ease of reading
log_format = f"{blue}[%(levelname)-10s]{magenta}[%(name)-20s]{reset} %(message)-70s     {green}[%(filename)s:%(lineno)d]{reset}"
