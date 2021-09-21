import asyncio, wget
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

    yt = YouTube(youtube_url)

    file_name = video_id(youtube_url)

    # download video
    # print('Starting video download')
    yt.streams.first().download(output_path=video_file_path, filename=file_name)

    # convert to mp3
    # str conversion + brackets are necessary
    videoclip = VideoFileClip(str(video_file_path / (file_name + ".mp4")))

    audioclip = videoclip.audio
    # str conversion + brackets are necessary
    audioclip.write_audiofile(str(audio_file_path / (file_name + ".mp3")))

    audioclip.close()
    videoclip.close()

    # TODO: this is the only time YVideo class is used, maybe phase it out
    # video_obj = YVideo(youtube_url)
    # video_obj.downloadVideo()
    # video_obj.convertVideoToMP3()
    #
    # return video_obj.file_name

    return file_name

async def convert_audio_to_link(file_name):
    # TODO: change this function so that it returns midi instead of a link
    # TODO: put some try catches in here to prevent timeouts
    # TODO: implement proxies work correctly

    proxy_num = random.randrange(0, 100000)

    # print("ATTEMPTING TO GET LINK")
    browser = await launch(
        {
            "args": [f"--proxy-server=zproxy.lum-superproxy.io:{proxy_port}"],
            "headless": False,
        }
    )
    page = await browser.newPage()
    await page.authenticate(
        {
            "username": f"{proxy_username}-session-{proxy_num}",
            "password": proxy_password,
        }
    )

    try:  # TODO: finish the error checking on this function
        await page.goto("https://www.conversion-tool.com/audiotomidi/", timeout=5000)

    except:
        print("goto timed out!")
        return asyncio.get_event_loop().run_until_complete(
            convert_audio_to_link(file_name)
        )

    finally:
        await browser.close()

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

    # os.remove(str(audio_file_path / (file_name + '.mp3'))) # remove mp3 file

    return link


def dl_midi_file(url, file_name):
    # TODO: (unimportant) let's remove wget and use a normal python lib like requests
    wget.download(url, str(midi_file_path / (file_name + ".midi")))


def video_to_midi(youtube_url):
    print("Converting YouTube URL into audio file...")
    file_name = download_video_audio(youtube_url)  # store audio file in audio_file_path

    print("Converting audio to midi...")
    midi_file_url = asyncio.run(convert_audio_to_link(file_name))

    print("Downloading midi file...")
    dl_midi_file(midi_file_url, file_name)  # store audio file in midi_file_path

    # TODO: this seems weird to return when this could be returned anywhere?
    filepath = str(midi_file_path / (file_name + ".midi"))

    return filepath


def converter_process(link_q, play_q):
    while True:
        # TODO: add some error checking here so that if it fails, something doesn't get incorrectly added to the q
        link = link_q.get()
        filepath = video_to_midi(link)
        play_q.put(filepath)
