# always checking db for unconverted links
# when an uncoverted link is found, it is converted

import asyncio, wget, os, time
from pyppeteer import launch
from pathlib import Path
from youtube_class import YVideo
from global_vars import midi_file_path, audio_file_path, video_file_path, queue_table
from sqlalchemy import create_engine, select

engine = create_engine('sqlite:///bertha2.db', connect_args={'timeout': 120})
conn = engine.connect() # create and connect to database here
    
def check_db_for_unconverted_videos():
    print("checking db for unconverted videos")
    s = select([queue_table])
    result = conn.execute(s)
    for row in result:
        # print(row)
        if row['isconverted'] == 0:
            print("found an unconverted video, converting it")
            # convert it
            if video_to_midi(row['link']):
                req = queue_table.update().where(queue_table.c.id == row['id']).values(isconverted=1)
                print("successfully converted it")
            else: # if unconvertable
                req = queue_table.update().where(queue_table.c.id == row['id']).values(isqueued=1)
                print("unsuccessfully converted it")
            conn.execute(req)

    result.close()


def video_to_midi(youtube_url):
    try:
        print("Converting YouTube URL into audio file...")
        file_name = download_video_audio(youtube_url) # store audio file in audio_file_path
        
        print("Converting audio to midi...")
        midi_file_url = asyncio.get_event_loop().run_until_complete(convert_audio_to_link(file_name))
        
        print("Downloading midi file...")
        dl_midi_file(midi_file_url, file_name) # store audio file in midi_file_path

        return True
    except:
        return False

def download_video_audio(youtube_url):
    video_obj = YVideo(youtube_url)
    video_obj.downloadVideo()
    video_obj.convertVideoToMP3()

    return video_obj.file_name

async def convert_audio_to_link(file_name): # put some try catches in here to prevent timeouts
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.conversion-tool.com/audiotomidi/')

    filechoose = await page.querySelector('#localfile')
    upload_file = str(audio_file_path / (file_name + ".mp3"))
    await filechoose.uploadFile(upload_file)

    submit = await page.querySelector('#uploadProgress > p > button')
    await submit.click()

    await page.waitForSelector('#post-472 > div.entry-content.clearfix > ul > li:nth-child(1) > a')
    link = await page.querySelectorEval('#post-472 > div.entry-content.clearfix > ul > li:nth-child(1) > a', 'n => n.href')

    await browser.close()

    os.remove(str(audio_file_path / (file_name + '.mp3'))) # remove mp3 file
    
    return link

def dl_midi_file(url, file_name):
    wget.download(url, str(midi_file_path / (file_name + ".midi")))

while True:
    check_db_for_unconverted_videos()
    time.sleep(10)
