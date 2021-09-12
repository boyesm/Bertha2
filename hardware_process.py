'''
what this file should do:
- read midi file (take a midi file location as input)
- convert to data playable by the hardware
- play on hardware
'''
import os
os.environ["BLINKA_FT232H"] = "1"  # this needs to set before board is imported

from board import SCL, SDA
import busio
import asyncio
import mido
from adafruit_pca9685 import PCA9685
import math
import datetime

i2c_bus = busio.I2C(SCL, SDA)
pca = PCA9685(i2c_bus)
pca.frequency = 60  # Set the PWM frequency to 60hz. TODO: should this be greater??

# duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.

starting_note = 48
number_of_notes = 16


def update_solenoid_value(note, pwm_value):
    if starting_note + number_of_notes <= note:  # this will ensure only valid notes are toggled, preventing memory address not found errors
        pca.channels[note-starting_note].duty_cycle = hex(pwm_value)


async def power_draw_function(time_passed, velocity):  # a function to produce an optimal duty cycle value for the solenoid so it doesn't draw unnecessary current

    # velocity should impact the speed at which voltage is applied to the solenoids (duH!)

    # pwm_at_t = math.log(time_passed + 1) + velocity  # this must have a max value of 4095  # this is just an example function, not the final one!

    if time_passed < 0.2:
        pwm_at_t = (-10000*time_passed) + 4065
    else:
        pwm_at_t = 2065

    return pwm_at_t # max value is 65535, min is 0


async def turn_on_note(note, velocity, delay=0):

    await asyncio.sleep(delay)  # this seems sketchy, but it works
    print(f'turned on note {note}')
    t0 = datetime.datetime.now()  # this time is different from the midi time because it's used as the independent variable for the power draw function
    for i in range(10):
        t1 = datetime.datetime.now()
        pwm_value = power_draw_function((t1 - t0).total_seconds(), velocity)
        update_solenoid_value(note, pwm_value)
        asyncio.sleep(0.01)


async def turn_off_note(note, delay=0):

    await asyncio.sleep(delay)
    print(f'turned off note {note}')
    update_solenoid_value(note, 0)


async def play_midi_file(midi_filename):

    mid = mido.MidiFile(midi_filename)

    msgs = mid.tracks[1]  # this should be the track with the piano roll, but check with midi files from converter

    tasks = []
    time = 0

    for msg in msgs:
        time += (msg.time/1000)
        if msg.type == 'note_on':
            tasks.append(turn_on_note(msg.note, msg.velocity, time))
        if msg.type == 'note_off':
            tasks.append(turn_off_note(msg.note, time))

    await asyncio.gather(*tasks)


# asyncio.run(play_midi_file('song.mid'))


