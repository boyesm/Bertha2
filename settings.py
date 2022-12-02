from os import getcwd, getenv
from pathlib import Path
from dotenv import load_dotenv

cwd = getcwd()

midi_file_path = cwd / Path("files") / Path("midi")
audio_file_path = cwd / Path("files") / Path("audio")
video_file_path = cwd / Path("files") / Path("video")

dirs = [midi_file_path, audio_file_path, video_file_path]  # add any other file paths to this variable

queue_save_file = "saved_queues"

channel = '#berthatwo'  # the channel of which chat is being monitored

load_dotenv("secrets.env")

# Twitch Secrets
nickname = getenv("NICKNAME")
token = getenv("TOKEN")
client_id = getenv("CLIENT_ID")

proxy_port = getenv("PROXY_PORT")
proxy_username = getenv("PROXY_USERNAME")
proxy_password = getenv("PROXY_PASSWORD")

cuss_words_file_name = "cuss_words.txt"

def import_cuss_words():
    global cuss_words

    with open(cuss_words_file_name) as f:
        words = f.read()
        word_list = words.split("\n")
        word_list = list(filter(None, word_list))  # Remove blank elements (e.g. "") from array
        return word_list

cuss_words = import_cuss_words()