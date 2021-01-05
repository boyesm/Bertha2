import asyncio
from pyppeteer import launch

# async def convert_audio_to_midi(audio_file):
    # browser = await launch()
    # page = await browser.newPage()
    # await page.goto('https://www.ofoct.com/audio-converter/convert-wav-or-mp3-ogg-aac-wma-to-midi.html')
    # await page.waitForSelector('input[type=file]')
    # return midi_file


import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://example.com')
    await page.screenshot({'path': 'example.png'})
    await browser.close()


async def main2():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://easyupload.io/')
    await page.waitForSelector('input[type=file]')
    await page.waitFor(1000)

    inputUploadHandle = await 
    fileToUpload = 'example.png'

    '''
    const inputUploadHandle = await page.$('input[type=file]');

    // prepare file to upload, I'm using test_to_upload.jpg file on same directory as this script
    // Photo by Ave Calvar Martinez from Pexels https://www.pexels.com/photo/lighthouse-3361704/
    let fileToUpload = 'test_to_upload.jpg';

    // Sets the value of the file input to fileToUpload
    inputUploadHandle.uploadFile(fileToUpload);
    '''


    await page.waitForSelector('#upload')
    await page.evaluate(() => document.getElementById('upload').click())


    await page.waitForSelector('#upload-link')
    await page.waitFor(5000)

    let downloadUrl = await page.evaluate(() => {
        return document.getElementById('upload-link').value;
    })
    print({'file': fileToUpload,
                 'download_url': downloadUrl})



    await browser.close()



    

asyncio.get_event_loop().run_until_complete(main())