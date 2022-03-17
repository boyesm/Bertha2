from os import getcwd
from pathlib import Path

cwd = getcwd()

midi_file_path = cwd / Path("files") / Path("midi")  # TODO: make sure this still works
audio_file_path = cwd / Path("files") / Path("audio")
video_file_path = cwd / Path("files") / Path("video")

dirs = [midi_file_path, audio_file_path, video_file_path]  # add any other file paths to this variable

# TODO: move Twitch login and proxy data to a .env file

nickname = 'berthatwo'
token = 'oauth:efnlrqvy824hqq4h5hczse0ekvms0e'
# channel = '#berthatwo'
channel = "#mizkif"

proxy_port = '22225'
proxy_username = 'lum-customer-hl_65bf90ee-zone-data_center'
proxy_password = '2?f8ek31o~xr'
