# always checking db for unconverted links
# when an uncoverted link is found, it is converted

import asyncio, wget, os
import random
from datetime import datetime
import time
import logging

from pyppeteer import launch

from cli_request_handler import engine
from youtube_class import YVideo
from global_vars import midi_file_path, audio_file_path, video_file_path, queue_table, proxy_port, proxy_username, proxy_password
from db_engine import dbEngine

engine = dbEngine()
    
def check_db_for_unconverted_videos():

    print("Checking db for unconverted videos...")

    # Queries the top result from the database

    rows = engine.selectQuery("SELECT TOP 1 id,link FROM Bertha2Table WHERE converted = 0 ")

    if(rows.values.any()):

        print("Found a video to convert")
        for row in rows.values:

            print("Row: ", row)
            print("ID: ", row[0])
            print("Link: ", row[1])
            id = row[0]
            link = row[1]

            try:

                videoInfo = video_to_midi(link)
                filename = videoInfo[0]
                filepath = videoInfo[1]



                engine.insertQuery(f"UPDATE Bertha2Table SET converted = 1, filename = '{filename}', filepath = '{filepath}' WHERE id = {id}")

                print("Successfully converted video")


            except:  # if unconvertable
                #     req = queue_table.update().where(queue_table.c.id == row['id']).values(isqueued=1)

                # Prints the exception, but keeps running the program
                logging.exception("Error converting video")

    else:

        print("No videos to convert")

def video_to_midi(youtube_url):

    # engine = dbEngine()

    print("Converting YouTube URL into audio file...")
    file_name = download_video_audio(youtube_url) # store audio file in audio_file_path

    print("Converting audio to midi...")
    midi_file_url = asyncio.get_event_loop().run_until_complete(convert_audio_to_link(file_name))

    print("Downloading midi file...")
    dl_midi_file(midi_file_url, file_name) # store audio file in midi_file_path

    filepath = str(midi_file_path / (file_name + ".midi"))

    # print("About to query")
    return file_name, filepath

def download_video_audio(youtube_url):

    video_obj = YVideo(youtube_url)
    video_obj.downloadVideo()
    video_obj.convertVideoToMP3()

    return video_obj.file_name

async def convert_audio_to_link(file_name): # put some try catches in here to prevent timeouts

    proxy_num = random.randrange(0, 100000)

    # print("ATTEMPTING TO GET LINK")
    browser = await launch({
        'args': [f'--proxy-server=zproxy.lum-superproxy.io:{proxy_port}'],
        'headless': False
    })
    page = await browser.newPage()
    await page.authenticate({'username': f'{proxy_username}-session-{proxy_num}', 'password': proxy_password})

    try:  # TODO: finish the error checking on this function
        await page.goto('https://www.conversion-tool.com/audiotomidi/', timeout=5000)

    except:
        print("goto timed out!")
        return asyncio.get_event_loop().run_until_complete(convert_audio_to_link(file_name))

    finally:
        await browser.close()

    filechoose = await page.querySelector('#localfile')
    upload_file = str(audio_file_path / (file_name + ".mp3"))
    await filechoose.uploadFile(upload_file)

    submit = await page.querySelector('#uploadProgress > p > button')
    await submit.click()

    await page.waitForSelector('#post-472 > div.entry-content.clearfix > ul > li:nth-child(1) > a', timeout=0)
    link = await page.querySelectorEval('#post-472 > div.entry-content.clearfix > ul > li:nth-child(1) > a', 'n => n.href')

    await browser.close()

    # os.remove(str(audio_file_path / (file_name + '.mp3'))) # remove mp3 file

    return link



def dl_midi_file(url, file_name):
    wget.download(url, str(midi_file_path / (file_name + ".midi")))




print("Started converter")
if __name__ == '__main__':
    while True:
        check_db_for_unconverted_videos()
        time.sleep(1)

