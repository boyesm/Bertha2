import os
from pathlib import Path
from global_vars import midi_file_path, audio_file_path, video_file_path

def init():
    create_dirs()

def create_dirs():
    dirs = [midi_file_path, audio_file_path, video_file_path]
    
    for dir in dirs:
        file_dir = Path(dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
