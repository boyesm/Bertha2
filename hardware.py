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

@atexit.register
def shutdown():
    turn_off_all()


starting_note = 48
number_of_notes = 48

# https://discussions.apple.com/thread/7659162
arduino = serial.Serial()
# try:
#     arduino.port='/dev/cu.usbmodem1101'  # TODO: add port config in settings.py
# except:
#     arduino.port='/dev/cu.usbmodem101'  # TODO: add port config in settings.py

# /dev/cu.usbserial-110
# arduino.port = "/dev/cu.usbserial-110"
arduino.port = "/dev/cu.usbserial-10"
# arduino.port='/dev/cu.usbmodem1101'  # TODO: add port config in settings.py
arduino.baudrate=115200
arduino.timeout=0.1
arduino.open()

# port can be found via the command: ls /dev/

def update_solenoid_value(note_address, pwm_value):

    # ensure that note_address or pwm_value are always bewtween 1 and 255. 0 must be reserved for error codes in arduino (stupidest thing I ever heard).
    note_address +=1
    pwm_value += 1

    # this will ensure pwm_value does not exceed the bounds of 8-bit int
    if pwm_value > 254: pwm_value = 254
    if pwm_value < 1: pwm_value = 1

    # this will ensure only valid notes are toggled, preventing memory address not found errors
    if (note_address < 0+1) or (note_address > number_of_notes+1) or (note_address >= 254): return

    print(f'{note_address}, {int(pwm_value)}')
    arduino.write(struct.pack('>3B', int(note_address), int(pwm_value), int(255)))


def power_draw_function(velocity, time_passed):
    # create a function that will determine the power emitted at different points in time
    # max output value should be 255?

    a = 250
    b = 1.05
    c = 90
    d = 100
    e = 10

    pwm_at_t = (b ** (c + (velocity / e) - (a * time_passed))) + d
    ## y=1.05^{\left(90+\frac{t}{10}-250x\right)}+100

    return pwm_at_t

async def trigger_note(note, init_note_delay=0, velocity=255, hold_note_time=1):

    # delay until the note should be turned on
    await asyncio.sleep(init_note_delay)

    # start loop that will initiate and adjust power output to solenoid
    start_time = time.time()

    while True:
        curr_time = time.time()
        passed_time = curr_time - start_time

        if passed_time > hold_note_time:
            update_solenoid_value(0, note)
            return
        else:
            y = power_draw_function(velocity, passed_time)
            update_solenoid_value(y, note)

        await asyncio.sleep(0.1)


def turn_off_note(note):

    note_address = note - starting_note
    update_solenoid_value(note_address, 0)


async def play_midi_file(midi_filename):

    # TODO: be able to start playback from a certain point in the video (10 seconds in)
    # TODO: add a 30 second limit to video playback

    tasks = []
    start_time = time.time()
    input_time = 0.0
    mid = mido.MidiFile(midi_filename)
    ticks_per_beat = mid.ticks_per_beat
    tempo = mid.tempo
    temp_lengs = {}

    i = 0

    for msg in mido.merge_tracks(mid.tracks):

        # find the time between turning a note on and off
        # temp_lengs = {note:{vel:127, time_on:0.0}}

        input_time += mido.tick2second(msg.time, ticks_per_beat, tempo)

        if isinstance(msg, mido.MetaMessage):
            continue
        else:
            i += 1
            if msg.type == 'note_on':
                print(f'note_on {msg.note} {msg.velocity} {input_time}')
                temp_lengs.update({msg.note: {"velocity": msg.velocity, "init_note_delay": input_time}})

            elif msg.type == 'note_off':
                print(f'note_off {msg.note}')
                print(temp_lengs)

                ## error checks
                # make sure temp_lengs[msg.note] exists and isn't from some past note.

                init_note_delay = temp_lengs[msg.note]["init_note_delay"]
                note = msg.note
                velocity = temp_lengs[msg.note]["velocity"]
                hold_note_time = input_time - temp_lengs[msg.note]["init_note_delay"]

                tasks.append(trigger_note(note, init_note_delay, velocity, hold_note_time))

    # gather tasks and run
    await asyncio.gather(*tasks)

def hardware_process(play_q):
    while True:
        filepath = play_q.get()

        # TODO: this needs to be in sync with video (video can be implemented later)
        print("HARDWARE: starting playback of song on hardware")
        asyncio.run(play_midi_file(filepath))
        print("HARDWARE: finished playback of song on hardware")


def turn_off_all():
    # print("Shutting off all solenoids...")
    for note in range(number_of_notes):
        turn_off_note(note + starting_note)
    print("HARDWARE: All solenoids should be off...")


# async def turn_on_all():
#     for note in range(number_of_notes):
#         await turn_on_note(note + starting_note)


# asyncio.run(play_midi_file("midi/song.mid"))
# asyncio.run(play_midi_file("midi/all_notes2.mid"))
# asyncio.run(play_midi_file("midi/test_all_solenoids_at_once.mid"))
# asyncio.run(play_midi_file("midi/take5.mid"))
# asyncio.run(play_midi_file("midi/Guns n Roses - Sweet Child O Mine.mid"))
# play_midi_file("midi/Shape of You.mid")

# Pirate not working
# play_midi_file("midi/Pirate.mid")
# asyncio.run(play_midi_file("midi/scale2.mid"))
# asyncio.run(play_midi_file("midi/Wii Channels - Mii Channel.mid"))
# asyncio.run(play_midi_file("midi/The Legend of Zelda Ocarina of Time - Song of Storms.mid"))
# asyncio.run(play_midi_file("midi/linkin_park-numb.mid"))
# play_midi_file("midi/Doja+Cat++Mooo+Official+Video.midi")
# asyncio.run(play_midi_file("midi/c_repeated.mid"))
# asyncio.run(play_midi_file("files/midi/9Ko-nEYJ1GE.midi"))
# asyncio.run(play_midi_file("midi/Super Mario Bros.mid"))

# asyncio.run(play_midi_file("files/midi/dQw4w9WgXcQ.midi"))


# turn every note on and off
# while True:
#     for i in range(number_of_notes):
#         update_solenoid_value(i, 255)
#
#     time.sleep(1)
#
#     for i in range(number_of_notes):
#         update_solenoid_value(i, 0)
#
#     time.sleep(1)

# while True:
#     for i in range(16):
#         update_solenoid_value(i + 32, 255)
#
#     time.sleep(1)
#
#     for i in range(16):
#         update_solenoid_value(i + 32, 0)
#
#     time.sleep(1)


### turn on every note one at a time
# while True:
#     for note in range(number_of_notes):
#         update_solenoid_value(note, 255)
#         time.sleep(0.2)
#         update_solenoid_value(note, 0)
