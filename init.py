import os, shutil
from pathlib import Path
from global_vars import midi_file_path, audio_file_path, video_file_path, meta

cwd = Path(os.getcwd())

def init():
    print("Initializing Bertha2...")
    create_dirs()
    print("Initializing completed...")

def create_dirs():
    try:

        shutil.rmtree('files')

    except:

        return

    dirs = [midi_file_path, audio_file_path, video_file_path]
    
    for dir in dirs:
        file_dir = Path(dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)


init() # this is not a test case. this is needed to run the program. TODO: reimplemnt this to something like 'if __name__ == '__main__'
