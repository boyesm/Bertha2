import os
os.environ["BLINKA_FT232H"] = "1"

from board import SCL, SDA
import busio
import asyncio
import mido
from adafruit_pca9685 import PCA9685

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 60  # Set the PWM frequency to 60hz. TODO: should this be greater??

# duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.

starting_note = 48

async def turn_on_note(note, delay=0):
    # test async here
    await asyncio.sleep(delay)
    print(f'turned on note {note}')
    try:
        pca.channels[note-starting_note].duty_cycle = 0x03E8
    except:
        pass  # probably not an available pin on the hardware
    # await asyncio.sleep(1)


async def turn_off_note(note, delay=0):
    # test async here
    await asyncio.sleep(delay)
    print(f'turned off note {note}')
    try:
        pca.channels[note - starting_note].duty_cycle = 0x0000
    except:
        pass  # probably not an available pin on the hardware
    # await asyncio.sleep(1)


async def play_midi_file(midi_filename):

    mid = mido.MidiFile(midi_filename)

    msgs = mid.tracks[1]  # this should be the track with the piano roll, but check with midi files from converter

    tasks = []
    time = 0

    for msg in msgs:
        time += (msg.time/1000)
        if msg.type == 'note_on':
            tasks.append(turn_on_note(msg.note, time))
        if msg.type == 'note_off':
            tasks.append(turn_off_note(msg.note, time))

    await asyncio.gather(*tasks)


asyncio.run(play_midi_file('song.mid'))
