import asyncio
import time
from pprint import pprint
from os import getcwd

import wget
import random
from pyppeteer import launch
from pytube import YouTube
from pytube.extract import video_id
from settings import video_file_path
from moviepy.editor import VideoFileClip
from settings import (
    midi_file_path,
    audio_file_path,
    proxy_port,
    proxy_username,
    proxy_password,
)

def download_video_audio(youtube_url):
    print("CONVERTER: Converting YouTube URL into audio file...")

    yt = YouTube(youtube_url)
    file_name = video_id(youtube_url)

    # download video
    print("CONVERTER: Starting video download")
    yt.streams.first().download(
        output_path=video_file_path, filename=f"{file_name}.mp4"
    )

    # convert to mp3
    # str conversion + brackets are necessary
    videoclip = VideoFileClip(str(video_file_path / (file_name + ".mp4")))

    audioclip = videoclip.audio
    # str conversion + brackets are necessary
    audioclip.write_audiofile(str(audio_file_path / (file_name + ".mp3")))

    audioclip.close()
    videoclip.close()

    return file_name


# TODO: get this function working
async def convert_audio_to_midi(file_name):
    print("CONVERTER: converting audio to midi")
    # TODO: put some try catches in here to prevent timeouts

    proxy_num = random.randrange(0, 100000)

    # print("ATTEMPTING TO GET LINK")
    browser = await launch(
        {
            "args": [f"--proxy-server=zproxy.lum-superproxy.io:{proxy_port}"],
            # "headless": False,
        }
    )
    page = await browser.newPage()
    await page.authenticate(
        {
            "username": f"{proxy_username}-session-{proxy_num}",
            "password": proxy_password,
        }
    )

    # proxy is working!!!

    try:  # TODO: finish the error checking on this function
        await page.goto("https://www.conversion-tool.com/audiotomidi/", timeout=30000)
        # await page.goto("https://whatmyuseragent.com")

    except Exception as e:
        print("CONVERTER: goto timed out!")
        print(e)  # error -> Navigation Timeout Exceeded: 1000 ms exceeded.
        # return asyncio.get_event_loop().run_until_complete(
        #     convert_audio_to_link(file_name)
        # )
        # TODO: restart function from the top!

    # print("Opened the webpage successfully")
    # time.sleep(30)

    filechoose = await page.querySelector("#localfile")
    upload_file = str(audio_file_path / (file_name + ".mp3"))
    await filechoose.uploadFile(upload_file)

    submit = await page.querySelector("#uploadProgress > p > button")
    await submit.click()

    await page.waitForSelector(
        "#post-472 > div.entry-content.clearfix > ul > li:nth-child(1) > a", timeout=0
    )
    link = await page.querySelectorEval(
        "#post-472 > div.entry-content.clearfix > ul > li:nth-child(1) > a",
        "n => n.href",
    )

    await browser.close()
    # print("Got the link!")

    # os.remove(str(audio_file_path / (file_name + ".mp3")))  # remove unneeded mp3 file
    # print(link)

    print("CONVERTER: Downloading midi file...")
    wget.download(link, str(midi_file_path / (file_name + ".midi")))


def video_to_midi(youtube_url):

    #TODO: add a feature that checks if the youtube video has already been converted

    yt = YouTube(youtube_url)
    video_name = yt.vid_info['videoDetails']['title']
    # video_name = yt.vid_info
    # file_name = video_id(youtube_url)

    # if it's been converted and found in files, return filepath (temporarily disabled for testing)
    # if os.path.isfile(str(midi_file_path / (file_name + ".midi"))):
    #     return str(midi_file_path / (file_name + ".midi"))

    # TODO: can we convert multiple files at the same time? or can we convert them faster?
    file_name = download_video_audio(youtube_url)  # store audio file in audio_file_path

    # TODO: if this fails, rerun the function
    midi_file_url = asyncio.run(convert_audio_to_midi(file_name))

    # TODO: why is midi_file_url not used? That seems like an issue.

    filepath = str(midi_file_path / (file_name + ".midi"))

    return filepath, video_name


def converter_process(sigint_e,conn, link_q, play_q, title_q):
    print("CONVERTER: Converter process has been started.")
    while not sigint_e.is_set():
        try:
            link = link_q.get(timeout=10)  # add a timeout to these. every 10 seconds, if nothing comes through, unblock and skip all code
            print("CONVERTER: starting to convert YT link to MIDI")
            filepath, video_title = video_to_midi(link)
            # time.sleep(10)
            print("CONVERTER: completed the conversion of YT link to MIDI")

            conn.send({"title": video_title,
                       "filepath": f"{getcwd()}/files/video/{YouTube(link).video_id}.mp4"})  # This should be here. As soon as a video is finished converting, it should be added to the queue because we know it's safe

            play_q.put(filepath)
            title_q.put(video_title)
        except:  # this will occur when link_q is empty. not the best way to implement.
            pass

    else:
        print("CONVERTER: Converter process has been shut down.")

# TODO: test longer videos and see how they work
# yt_links = [
#     "jt9LlHXGckg",
#     "3Lyex2tSUyA",
#     "p9RtcklL0as",
#     "meha_FCcHbo",
#     "KRbsco8M7Fc",
#     "jt9LlHXGckg",
#     "3Lyex2tSUyA",
#     "p9RtcklL0as",
#     "meha_FCcHbo",
#     "KRbsco8M7Fc",
#     "jt9LlHXGckg",
#     "3Lyex2tSUyA",
#     "p9RtcklL0as",
#     "meha_FCcHbo",
#     "KRbsco8M7Fc",
#     "jt9LlHXGckg",
#     "3Lyex2tSUyA",
#     "p9RtcklL0as",
#     "meha_FCcHbo",
#     "KRbsco8M7Fc",
# ]
# for link in yt_links:
#     video_to_midi(f"https://www.youtube.com/watch?v={link}")
