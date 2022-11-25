"""
what this file should do:
- read midi file (take a midi file location as input)
- convert to data playable by the hardware
- play on hardware
"""

import os
import asyncio
import subprocess
from pprint import pprint

import mido
import math
import datetime
import atexit
import serial
import struct
import time

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8001))


starting_note = 48
number_of_notes = 48


note_values = [0]*number_of_notes

def generate_hardware_vis(arr, min_val=0, max_val=255, bar_length=30):
    # all elements of arr should be ints
    # generates percentage bars that correspond with output voltage of solenoids
    str = ""

    for i, el in enumerate(arr):
        per = el / max_val

        hashes = '#' * int(round(per * bar_length))
        spaces = ' ' * int(round((1 - per) * bar_length))
        str += f"[{hashes + spaces}]"
        if (i) % 2:
            str+="\n"
        else:
            str+=(" " * 5)

    return str


last_update = time.time()

def update_cl_vis(str):
    # rate limiting
    global last_update
    print(f"TIME SINCE LAST CALL: {time.time() - last_update}")
    if (time.time() - last_update < 0.005): return

    sock.send(b"\033[H")  # sketchy way of clearing the screen
    sock.send(str.encode())

    last_update = time.time()


def turn_off_all():
    for note in range(number_of_notes):
        turn_off_note(note + starting_note)
    print("HARDWARE: All solenoids should be off...")


def turn_off_note(note):
    note_address = note - starting_note
    update_solenoid_value(note_address, 0)


async def test_every_note(hold_note_time=0.25):
    tasks = []
    input_time = 0.0

    for note in range(number_of_notes):
        tasks.append(trigger_note(note, input_time, 127, hold_note_time))
        input_time += hold_note_time

    await asyncio.gather(*tasks)


async def test_every_note_at_once(hold_note_time=10, number_of_notes=5):
    tasks = []
    input_time = 0.0

    for note in range(number_of_notes):
        tasks.append(trigger_note(note, input_time, 127, hold_note_time))
    # input_time+=(hold_note_time*2)

    await asyncio.gather(*tasks)


def turn_on_some_notes():
    for note in range(20):
        update_solenoid_value(note, 254)


def update_solenoid_value(note_address, pwm_value):

    # ensure that note_address or pwm_value are always bewtween 1 and 255. 0 must be reserved for error codes in arduino (stupidest thing I ever heard).
    # note_address += 1
    # pwm_value += 1

    # this will ensure pwm_value does not exceed the bounds of 8-bit int
    if pwm_value > 254: pwm_value = 254
    if pwm_value < 0: pwm_value = 0

    # if a note is up to an octave below what is available to be played, shift it up an octave
    if (note_address < 0):
        print(f"HARDWARE: too low! for now... {note_address}")
        note_address+=24

    # if a note is up to an octave below what is available to be played, shift it up an octave
    if (note_address > number_of_notes):
        print(f"HARDWARE: too high! for now... {note_address}")
        note_address -= 24

    # this will ensure only valid notes are toggled, preventing memory address not found errors
    if (note_address < 0) or (note_address > number_of_notes) or (note_address >= 255): return

    print(f'{note_address}, {pwm_value}')

    note_values[note_address] = pwm_value

    print(note_values)

    o = generate_hardware_vis(note_values)
    update_cl_vis(o)


    # this part of the code will send hardware outputs to an open netcat terminal
    # make sure t

    '''
    if arduino_connection != None:
        arduino_connection.write(struct.pack('>3B', int(note_address), int(pwm_value), int(255)))
    '''


def power_draw_function(velocity, time_passed):
    # create a function that will determine the power emitted at different points in time
    # max output value should be 255?

    a = 100
    b = 1.05
    c = 100
    d = 30
    e = 10

    pwm_at_t = (b ** (c + (velocity / e) - (a * time_passed))) + d
    ## y=1.05^{\left(90+\frac{t}{10}-250x\right)}+100

    print(f"PWM: {pwm_at_t}")
    return pwm_at_t


async def trigger_note(note, init_note_delay=0, velocity=255, hold_note_time=1, ):

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

        await asyncio.sleep(0.01)


async def play_midi_file(midi_filename):

    # TODO: be able to start playback from a certain point in the video (10 seconds in)
    # TODO: add a 30 second limit to video playback

    tasks = []
    start_time = time.time()
    input_time = 0.0
    mid = mido.MidiFile(midi_filename)
    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000 # this is the default MIDI tempo
    temp_lengs = {}

    for msg in mido.merge_tracks(mid.tracks):

        # find the time between turning a note on and off
        # temp_lengs = {note:{vel:127, time_on:0.0}}

        input_time += mido.tick2second(msg.time, ticks_per_beat, tempo)

        if isinstance(msg, mido.MetaMessage):
            continue
        else:
            if msg.type == 'note_on':
                note = msg.note - starting_note
                print(f'note_on {note} {msg.velocity} {input_time}')
                temp_lengs.update({note: {"velocity": msg.velocity, "init_note_delay": input_time}})

            elif msg.type == 'note_off':
                note = msg.note - starting_note
                print(f'note_off {note}')
                # print(temp_lengs)

                ## TODO: error checks
                # make sure temp_lengs[msg.note] exists and isn't from some past note.

                init_note_delay = temp_lengs[note]["init_note_delay"]
                velocity = temp_lengs[note]["velocity"]
                hold_note_time = input_time - temp_lengs[note]["init_note_delay"]

                tasks.append(trigger_note(note, init_note_delay, velocity, hold_note_time))

    # gather tasks and run
    await asyncio.gather(*tasks)
    await asyncio.sleep(30)  # this is for ensuring the solenoids don't overheat


def hardware_process(sigint_e, done_conn, play_q, title_q):
    while not sigint_e.is_set():
        try:
            # title = title_q.get()
            filepath = play_q.get(timeout=10)

            print("TEST HARDWARE: Starting playback of song on hardware")
            asyncio.run(play_midi_file(filepath))
            done_conn.send("done")
            print("TEST HARDWARE: Finished playback of song on hardware")

            #  should we just move visuals here?
        except:
            pass
    else:
        print("TEST HARDWARE: Hardware process has been shut down.")


if __name__ == '__main__':


    # asyncio.run(play_midi_file("../midi-files/take5.mid"))
    # asyncio.run(play_midi_file("../midi-files/song.mid"))
    asyncio.run(play_midi_file("../midi-files/all_notes.mid"))