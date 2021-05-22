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
    remove_old_dirs()

    dirs = [midi_file_path, audio_file_path, video_file_path]
    
    for dir in dirs:
        file_dir = Path(dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

def remove_old_dirs():
    try:
        # shutil.move(str(cwd / Path("files")), str(cwd / Path("files.old")))
        shutil.rmtree('files')
    except:
        return

def create_db():
    remove_old_db()

    engine = create_engine('sqlite:///bertha2.db')
    meta.create_all(engine)

def remove_old_db():
    try:
        # os.rename('bertha2.db', 'oldbertha2.db')
        os.remove('bertha2.db')
    except:
        return

init()