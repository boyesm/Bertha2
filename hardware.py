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
import obsws

starting_note = 48
number_of_notes = 48


try:
    arduino = serial.Serial()
    # Find the usb port to use
    port_to_use = os.popen("ls -a /dev/cu.usbserial*").read().split('\n')[0]
    print(type(port_to_use))

    arduino.port = port_to_use
except:
    raise Warning("Unable to find arduino plugged in")
try:
    arduino.baudrate=115200
    arduino.timeout=0.1
    arduino.open()
except:
    raise Warning("Arduino cannot be opened. Is it plugged in?")

# port can be found via the command: ls /dev/

def turn_off_all():
    # print("Shutting off all solenoids...")
    for note in range(number_of_notes):
        turn_off_note(note + starting_note)
    print("HARDWARE: All solenoids should be off...")

def turn_off_note(note):

    note_address = note - starting_note
    update_solenoid_value(note_address, 0)

@atexit.register
def shutdown():
    turn_off_all()
    turn_off_all()

async def test_every_note(hold_note_time=0.25):

    tasks = []
    input_time = 0.0

    for note in range(number_of_notes):
        tasks.append(trigger_note(note, input_time, 127, hold_note_time))
        input_time += hold_note_time

    await asyncio.gather(*tasks)

def update_solenoid_value(note_address, pwm_value):

    # ensure that note_address or pwm_value are always bewtween 1 and 255. 0 must be reserved for error codes in arduino (stupidest thing I ever heard).
    note_address += 1
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
            update_solenoid_value(note, 0)
            return
        else:
            y = power_draw_function(velocity, passed_time)
            update_solenoid_value(note, y)

        await asyncio.sleep(0.1)


async def play_midi_file(midi_filename):

    # TODO: be able to start playback from a certain point in the video (10 seconds in)
    # TODO: add a 30 second limit to video playback

    tasks = []
    start_time = time.time()
    input_time = 0.0
    mid = mido.MidiFile(midi_filename)
    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000 # mid.tempo
    temp_lengs = {}

    for msg in mido.merge_tracks(mid.tracks):

        # find the time between turning a note on and off
        # temp_lengs = {note:{vel:127, time_on:0.0}}

        input_time += mido.tick2second(msg.time, ticks_per_beat, tempo)

        if isinstance(msg, mido.MetaMessage):
            continue
        else:
            if msg.type == 'note_on':
                print(f'note_on {msg.note} {msg.velocity} {input_time}')
                temp_lengs.update({msg.note: {"velocity": msg.velocity, "init_note_delay": input_time}})

            elif msg.type == 'note_off':
                print(f'note_off {msg.note}')
                print(temp_lengs)

                ## TODO: error checks
                # make sure temp_lengs[msg.note] exists and isn't from some past note.

                init_note_delay = temp_lengs[msg.note]["init_note_delay"]
                note = msg.note
                velocity = temp_lengs[msg.note]["velocity"]
                hold_note_time = input_time - temp_lengs[msg.note]["init_note_delay"]

                tasks.append(trigger_note(note, init_note_delay, velocity, hold_note_time))

    # gather tasks and run
    await asyncio.gather(*tasks)

def hardware_process(play_q, video_name_q):
    while True:
        current_video = video_name_q.get()
        filepath = play_q.get()

        obsws.change_text('Current Song', current_video)

        # TODO: this needs to be in sync with video (video can be implemented later)
        print("HARDWARE: starting playback of song on hardware")
        asyncio.run(play_midi_file(filepath))
        print("HARDWARE: finished playback of song on hardware")


if __name__ == '__main__':

    print("HARDWARE: Running some tests.")

    asyncio.run(test_every_note())

    '''
    midi_filename = "midi/all_notes.mid"

    asyncio.run(play_midi_file(midi_filename))
    '''
