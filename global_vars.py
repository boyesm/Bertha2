from os import getcwd
from pathlib import Path
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean

cwd = getcwd()

midi_file_path = Path(cwd + "/files/midi/")
audio_file_path = Path(cwd + "/files/audio/")
video_file_path = Path(cwd + "/files/video/")

meta = MetaData()
queue_table = Table('queue', meta, 
        Column('id', Integer, primary_key = True), 
        Column('username', String),
        Column('link', String),
        Column('filename', String),
        Column('isconverted', Boolean),
        Column('isqueued', Boolean),
    )