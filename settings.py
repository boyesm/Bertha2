from os import getcwd, getenv
from pathlib import Path
from dotenv import load_dotenv

cwd = getcwd()

midi_file_path = cwd / Path("files") / Path("midi")  # TODO: make sure this still works
audio_file_path = cwd / Path("files") / Path("audio")
video_file_path = cwd / Path("files") / Path("video")

dirs = [midi_file_path, audio_file_path, video_file_path]  # add any other file paths to this variable

load_dotenv()
# nickname = getenv("NICKNAME")
# token = getenv("TOKEN")

nickname = 'berthatwo'
token = 'oauth:efnlrqvy824hqq4h5hczse0ekvms0e'
channel = '#berthatwo'  # the channel of which chat is being monitored
# channel = "#lashieloo12"

proxy_port = '22225'
proxy_username = 'lum-customer-hl_65bf90ee-zone-data_center'
proxy_password = '2?f8ek31o~xr'
