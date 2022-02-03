"""
what this file should do:
- read midi file (take a midi file location as input)
- convert to data playable by the hardware
- play on hardware
"""

import os
import asyncio
import mido
import math
import datetime
import atexit
import serial
import struct
import time


starting_note = 48
number_of_notes = 16

# https://discussions.apple.com/thread/7659162
arduino = serial.Serial()
try:
    arduino.port='/dev/cu.usbmodem1101'  # TODO: add port config in settings.py
except:
    arduino.port='/dev/cu.usbmodem101'  # TODO: add port config in settings.py

arduino.baudrate=115200 # current bug is independent of baudrate
arduino.timeout=0.1
arduino.open()

# port can be found via the command: ls /dev/

def update_solenoid_value(note, pwm_value):

    note_address = note - starting_note

    # ensure that note_address or pwm_value are always bewtween 1 and 255. 0 must be reserved for error codes in arduino (stupidest thing I ever heard).
    note_address +=1
    pwm_value += 1

    # this will ensure pwm_value does not exceed the bounds of 8-bit int
    if pwm_value > 254: pwm_value = 254
    if pwm_value < 1: pwm_value = 1

    # this will ensure only valid notes are toggled, preventing memory address not found errors
    if (note_address < 0+1) or (note_address > number_of_notes+1) or (note_address >= 254): return

    print(f'{note_address}, {int(pwm_value)}')
    # print(struct.pack('>2B', int(note_address), int(pwm_value)))
    arduino.write(struct.pack('>3B', int(note_address), int(pwm_value), int(255)))


def power_draw_function(time_passed, velocity):
    # a function to produce an optimal duty cycle value for the solenoid so it doesn't draw unnecessary current
    # velocity should impact the speed at which voltage is applied to the solenoids (duH!)
    # pwm_at_t = math.log(time_passed + 1) + velocity  # this must have a max value of 4095  # this is just an example function, not the final one!

    # if time_passed < 0.1:
    #     pwm_at_t = (-40000 * time_passed) + 4065
    # else:
    #     pwm_at_t = 500
    #
    # return pwm_at_t  # max value is 65535, min is 0\

    return 255


async def turn_on_note(note, velocity, delay=0):

    await asyncio.sleep(delay)  # this seems sketchy, but it works
    # print(f"turned on note {note}")
    update_solenoid_value(note, 255)
    # this time is different from the midi time because it's used as the independent variable for the power draw function
    '''
    t0 = datetime.datetime.now()
    for i in range(10):
        t1 = datetime.datetime.now()
        pwm_value = power_draw_function((t1 - t0).total_seconds(), velocity)
        # print(note)
        update_solenoid_value(note, pwm_value)
        await asyncio.sleep(0.01)
    '''


async def turn_off_note(note, delay=0):

    await asyncio.sleep(delay)
    # print(f"turned off note {note}")
    update_solenoid_value(note, 0)


async def play_midi_file(midi_filename):

    mid = mido.MidiFile(midi_filename)

    # this should be the track with the piano roll, but check with midi files from converter
    msgs = mid.tracks[0]
    # msgs = mid.tracks[1]

    tasks = []
    time = 0

    for msg in msgs:
        time += msg.time / 1000
        if msg.type == "note_on":
            tasks.append(turn_on_note(msg.note, msg.velocity, time))
        if msg.type == "note_off":
            tasks.append(turn_off_note(msg.note, time))

    await asyncio.gather(*tasks)


def hardware_process(play_q):
    while True:
        filepath = play_q.get()

        # TODO: this needs to be in sync with video (video can be implemented later)
        asyncio.run(play_midi_file(filepath))


async def turn_off_all():
    for note in range(number_of_notes):
        await turn_off_note(note + starting_note)



@atexit.register
def shutdown():
    asyncio.run(turn_off_all())


# asyncio.run(play_midi_file("song.mid"))
# asyncio.run(play_midi_file("all_notes2.mid"))
# asyncio.run(play_midi_file("take5.mid"))
asyncio.run(play_midi_file("scale2.mid"))
# asyncio.run(play_midi_file("Doja+Cat++Mooo+Official+Video.midi"))
# asyncio.run(play_midi_file("c_repeated.mid"))






# while(True):

# arduino.write(struct.pack('>2B', 0, 255))
# update_solenoid_value(2 + 48, 255)
# arduino.write(struct.pack('>2B', int(15+48), int(255)))

# for i in range(20):
#
#     for note in range(16):
#         # print(note)
#         update_solenoid_value(note + 48, 255)
#
#     time.sleep(0.1)
#
#     for note in range(16):
#         update_solenoid_value(note + 48, 0)
#
#     time.sleep(0.1)
