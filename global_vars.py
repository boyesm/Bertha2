from os import getcwd
from pathlib import Path
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean

cwd = getcwd()

midi_file_path = Path(cwd / Path("files") / Path("midi"))
audio_file_path = Path(cwd / Path("files") / Path("audio"))
video_file_path = Path(cwd / Path("files") / Path("video"))

meta = MetaData()
queue_table = Table('queue', meta, 
        Column('id', Integer, primary_key = True), 
        Column('username', String),
        Column('link', String),
        Column('filename', String),
        Column('isconverted', Boolean),
        Column('isqueued', Boolean),
    )

tl = { # twitch login
    'username': 'berthatwo',
    'clientid': 'oqjx4qhulp84kvlv32rwggu7q2z2tb',
    'token': 'uk0yu50mnczb6vxf05uy3446b1e3er',
    'channel': 'EntertuneMusic',
}