import asyncio, wget, os
from pyppeteer import launch
from pathlib import Path

# midi output dir must be a Path object
def convert_audio_to_midi(upload_file, midi_output_dir, midi_file_name):
    print("Converting audio to midi...")
    url = asyncio.get_event_loop().run_until_complete(get_dl_link(upload_file))
    
    print("Downloading midi file")
    dl_link(url, midi_output_dir, midi_file_name)


async def get_dl_link(upload_file):
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.conversion-tool.com/audiotomidi/')

    filechoose = await page.querySelector('#localfile')
    await filechoose.uploadFile(upload_file)


    submit = await page.querySelector('#uploadProgress > p > button')
    await submit.click()

    await page.waitForSelector('#post-472 > div.entry-content.clearfix > ul > li:nth-child(1) > a')
    link = await page.querySelectorEval('#post-472 > div.entry-content.clearfix > ul > li:nth-child(1) > a', 'n => n.href')

    await browser.close()
    
    return link

def dl_link(url, file_dir, file_name):
    file_dir = Path(file_dir)
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    dl_here = file_dir / file_name
    wget.download(url, str(dl_here)) # must be converted to str type from path object

# cwd = os.getcwd()
# file_dir = cwd + '/files/img/'
# # print(file_dir)
# # convert_audio_to_midi('./test.mp3', Path(file_dir), 'test.mid')
# dl_link('https://i.stack.imgur.com/7302F.png', Path(file_dir), 'test.png')