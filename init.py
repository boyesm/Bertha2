import os, shutil
from sqlalchemy import create_engine
from pathlib import Path
from global_vars import midi_file_path, audio_file_path, video_file_path, meta

cwd = os.getcwd()

def init():
    create_dirs()
    create_db()

def create_dirs():
    remove_old_dirs()

    dirs = [midi_file_path, audio_file_path, video_file_path]
    
    for dir in dirs:
        file_dir = Path(dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

def remove_old_dirs():
    shutil.move(str(cwd + "/files/"), str(cwd + "/files.old/"))

def create_db():
    remove_old_db()

    engine = create_engine('postgres:///bertha2.db')
    meta.create_all(engine)

def remove_old_db():
    os.rename('bertha2.db', 'oldbertha2.db')

init()