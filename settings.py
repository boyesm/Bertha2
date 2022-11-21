from os import getcwd, getenv
from pathlib import Path
from dotenv import load_dotenv

cwd = getcwd()

midi_file_path = cwd / Path("files") / Path("midi-files")  # TODO: make sure this still works
audio_file_path = cwd / Path("files") / Path("audio")
video_file_path = cwd / Path("files") / Path("video")

dirs = [midi_file_path, audio_file_path, video_file_path]  # add any other file paths to this variable

queue_save_file = "saved_queues"

load_dotenv()
# nickname = getenv("NICKNAME")
# token = getenv("TOKEN")

nickname = 'berthatwo'
token = 'oauth:efnlrqvy824hqq4h5hczse0ekvms0e'
client_id = 'oqjx4qhulp84kvlv32rwggu7q2z2tb'
channel = '#berthatwo'  # the channel of which chat is being monitored
# channel = "#lashieloo12"

proxy_port = '22225'
proxy_username = 'lum-customer-hl_65bf90ee-zone-data_center'
proxy_password = '2?f8ek31o~xr'
