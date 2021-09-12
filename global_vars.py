from os import getcwd
from pathlib import Path
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean


##### \/ \/ move this into a dotenv file \/ \/ ##### set in init

cwd = getcwd()

midi_file_path = Path(cwd / Path("files") / Path("midi"))
audio_file_path = Path(cwd / Path("files") / Path("audio"))
video_file_path = Path(cwd / Path("files") / Path("video"))


##### ^^ move this into a dotenv file ^^ #####

meta = MetaData()
queue_table = Table('queue', meta, 
        Column('id', Integer, primary_key = True), 
        Column('username', String),
        Column('link', String),
        Column('filename', String),
        Column('isconverted', Boolean),
        Column('isqueued', Boolean),
    )

##### \/ \/ move this into a dotenv file \/ \/ #####


tl = { # twitch login
    'username': 'berthatwo',
    'clientid': 'oqjx4qhulp84kvlv32rwggu7q2z2tb',
    'token': 'uk0yu50mnczb6vxf05uy3446b1e3er',
    'channel': 'entertunemusic',
}


##### ^^ move this into a dotenv file ^^ #####

proxy_port = '22225'
proxy_username = 'lum-customer-hl_65bf90ee-zone-data_center'
proxy_password = '2?f8ek31o~xr'
