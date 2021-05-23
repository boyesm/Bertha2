import os, shutil
from sqlalchemy import create_engine
from pathlib import Path
from global_vars import midi_file_path, audio_file_path, video_file_path, meta

cwd = Path(os.getcwd())

def init():
    print("Initializing Bertha2...")

    create_dirs()
    create_db()
    print("Initializing completed...")

def create_dirs():

    # Remove old Database
    try:

        shutil.rmtree('files')

    except:

        return

    dirs = [midi_file_path, audio_file_path, video_file_path]
    
    for dir in dirs:
        file_dir = Path(dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

def create_db():

    # Delete the old database
    try:

        os.remove('bertha2.db')

    except:

        return

init() # this is not a test case. this is needed to run the program.

engine = create_engine('sqlite:///bertha2.db')
meta.create_all(engine)
