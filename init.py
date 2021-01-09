import os
from sqlalchemy import create_engine
from pathlib import Path
from global_vars import midi_file_path, audio_file_path, video_file_path, meta

def init():
    create_dirs()
    create_db()

def create_dirs():
    # delete them if they already exist


    dirs = [midi_file_path, audio_file_path, video_file_path]
    
    for dir in dirs:
        file_dir = Path(dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

def create_db():
    engine = create_engine('sqlite:///bertha2.db')
    # add: backup existing queue table and delete it  
    meta.create_all(engine)

# init()