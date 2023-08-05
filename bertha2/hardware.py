import asyncio
import socket
import struct
import subprocess
import time
import os
import random

import mido
import serial

import logging

from bertha2.settings import cli_args, solenoid_cooldown_s, log_format
from bertha2.utils.logs import initialize_module_logger, log_if_in_debug_mode, initialize_root_logger

# logger = initialize_module_logger(__name__)
logging.basicConfig(level=10, format=log_format)
logger = logging.getLogger(__name__)

### GLOBAL VARIABLES ###
starting_note = 41
number_of_notes = 48
arduino_connection = None
sock = None
TEST_FLAG = False

# TODO: this shouldn't be defined when not in test mode
last_cl_update = time.time()
sock = None
note_values = [0] * number_of_notes


### TEST PATTERN FUNCTIONS ###
async def test_every_note(hold_note_time=0.25):
    tasks = []
    input_time = 0

    for note in range(number_of_notes):
        tasks.append(trigger_note(note, input_time, 127, hold_note_time))
        input_time += hold_note_time

    await asyncio.gather(*tasks)


async def test_every_note_at_once(hold_note_time=10, number_of_notes=5):
    tasks = []
    input_time = 0

    for note in range(number_of_notes):
        tasks.append(trigger_note(note, input_time, 127, hold_note_time))
    # input_time+=(hold_note_time*2)

    await asyncio.gather(*tasks)


def turn_on_some_notes():
    for note in range(20):
        update_solenoid_value(note, 254)


'''
def turn_off_all():
    for note in range(number_of_notes):
        turn_off_note(note + starting_note)
    print("HARDWARE: All solenoids should be off...")


def turn_off_note(note):
    note_address = note - starting_note
    update_solenoid_value(note_address, 0)


# @atexit.register
# def shutdown():
#     # Run twice because sometimes some don't shut off
#     turn_off_all()
#     time.sleep(0.5)
#     turn_off_all()
'''


### TEST MODE FUNCTIONS ###
def generate_hardware_vis(arr, min_val=0, max_val=255, bar_length=30):
    # all elements of arr should be ints
    # generates percentage bars that correspond with output voltage of solenoids
    out_str = ""

    for i, el in enumerate(arr):
        per = el / max_val

        hashes = '#' * int(round(per * bar_length))
        spaces = ' ' * int(round((1 - per) * bar_length))
        out_str += f"[{hashes + spaces}]"
        if i % 2:
            out_str += "\n"
        else:
            out_str += (" " * 5)

    return out_str


def update_cl_vis(out_str):
    # rate limiting
    global last_cl_update
    # logger.debug(f"TIME SINCE LAST CALL: {time.time() - last_cl_update}")
    if time.time() - last_cl_update < 0.005: return

    sock.send(b"\033[H")  # sketchy way of clearing the screen
    sock.send(out_str.encode())

    last_cl_update = time.time()


### IMPORTANT MAIN FUNCTIONS ###
def update_solenoid_value(note_address, pwm_value):
    if TEST_FLAG:  # when testing, output doesn't go to the actual hardware, it's just visualized on the command line

        # this will ensure pwm_value does not exceed the bounds of 8-bit int
        if pwm_value > 254: pwm_value = 254
        if pwm_value < 0: pwm_value = 0

        # if a note is up to an octave below what is available to be played, shift it up an octave
        if note_address < 0:
            logger.debug(f"too low! for now... {note_address}")
            note_address += 24

        # if a note is up to an octave below what is available to be played, shift it up an octave
        if note_address > number_of_notes:
            logger.debug(f"too high! for now... {note_address}")
            note_address -= 24

        # this will ensure only valid notes are toggled, preventing memory address not found errors
        if (note_address < 0) or (note_address > number_of_notes - 1) or (note_address >= 255): return

        note_values[note_address] = pwm_value

        # logger.debug(note_values)

        o = generate_hardware_vis(note_values)
        # this part of the code will send hardware outputs to an open netcat terminal
        update_cl_vis(o)

    else:
        # ensure that note_address or pwm_value are always between 1 and 255.
        #   0 must be reserved for error codes in arduino (the stupidest thing I ever heard).
        note_address += 1
        pwm_value += 1

        # this will ensure pwm_value does not exceed the bounds of 8-bit int
        if pwm_value > 254:
            pwm_value = 254
        if pwm_value < 1:
            pwm_value = 1

        # if a note is up to an octave below what is available to be played, shift it up an octave
        if note_address < 0 + 1:
            # logger.debug(f"too low! for now... {note_address}")
            note_address += 24

        # if a note is up to an octave below what is available to be played, shift it up an octave
        if note_address > number_of_notes + 1:
            # logger.debug(f"too high! for now... {note_address}")
            note_address -= 24

        # this will ensure only valid notes are toggled, preventing memory address not found errors
        if (note_address < 0 + 1) or (note_address > number_of_notes + 1) or (note_address >= 254): return

        logger.debug(f"{note_address}, {int(pwm_value)}")
        if arduino_connection is not None:
            arduino_connection.write(struct.pack('>3B', int(note_address), int(pwm_value), int(255)))


def power_draw_function(velocity, time_passed):
    # create a function that will determine the power emitted at different points in time
    # max output value should be 255?

    cutoff = 0.1  # TODO: find a value for this variable. seconds
    minimum_power = 100  # TODO: find a value for this variable. minimum amount of power required to depress note
    minimum_hold = 50  # TODO: find a value for this variable. minimum amount of power to keep depressing the note after it's already been depressed initially
    maximum_power = 150
    maximum_velocity = 127

    if time_passed < cutoff:
        pwm_at_t = minimum_power + ((maximum_power - minimum_power) / maximum_velocity) * velocity
    else:
        pwm_at_t = minimum_hold

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

        await asyncio.sleep(0.01)


async def play_midi_file(midi_filename):
    # TODO: be able to start playback from a certain point in the video (10 seconds in)
    # TODO: add a 30 second limit to video playback

    tasks = []
    start_time = time.time()
    input_time = 0
    mid = mido.MidiFile(midi_filename)
    ticks_per_beat = mid.ticks_per_beat
    tempo = 500000  # this is the default MIDI tempo
    temp_lengs = {}

    for msg in mido.merge_tracks(mid.tracks):

        # find the time between turning a note on and off
        # temp_lens = {note:{vel:127, time_on:0.0}}

        input_time += mido.tick2second(msg.time, ticks_per_beat, tempo)

        if isinstance(msg, mido.MetaMessage):
            if msg.type == 'set_tempo':
                tempo = msg.tempo
            else:
                continue
        else:
            if msg.type == 'note_on':
                note = msg.note - starting_note
                logger.debug(f"note_on {note} {msg.velocity} {input_time}")
                temp_lengs.update({note: {"velocity": msg.velocity, "init_note_delay": input_time}})

            elif msg.type == 'note_off':
                note = msg.note - starting_note
                logger.debug(f"note_off {note}")
                # logger.debug(temp_lens)

                # TODO: error checks
                # make sure temp_lens[msg.note] exists and isn't from some past note.

                init_note_delay = temp_lengs[note]["init_note_delay"]
                velocity = temp_lengs[note]["velocity"]
                hold_note_time = input_time - temp_lengs[note]["init_note_delay"]

                tasks.append(trigger_note(note, init_note_delay, velocity, hold_note_time))

    # gather tasks and run
    await asyncio.gather(*tasks)


def create_connection_with_piano():
    global arduino_connection

    # Find the usb port that has something plugged in to use from /dev/ (only works with unix)
    # port can be found via the command: ls /dev/
    # port_to_use = os.popen("ls -a /dev/cu.usbserial*", ).read().split('\n')[0]

    try:
        potential_ports = subprocess.check_output(["ls -a /dev/cu.usbserial*"], shell=True,
                                                  stderr=subprocess.DEVNULL).decode('ascii')

        logger.debug(f"Setting serial up")
        arduino_connection = serial.Serial()
        port_to_use = potential_ports.split("\n")[0]
        logger.debug(f"Setting Arduino port to: {port_to_use}")
        arduino_connection.port = port_to_use
        logger.debug(f"Setting Arduino baudrate and timeout: {port_to_use}")
        arduino_connection.baudrate = 115200
        arduino_connection.timeout = 0.1
        logger.debug(f"Connecting to arduino on port:{port_to_use}")
        arduino_connection.open()

    except:
        logger.warning("Unable to connect to Arduino. Is it plugged in?")
        raise ConnectionRefusedError


def hardware_process_loop(hardware_visuals_conn, play_q):
    filepath = play_q.get(timeout=10)
    logger.info("Starting playback of song on hardware")
    hardware_visuals_conn.send("playing")
    asyncio.run(play_midi_file(filepath))
    hardware_visuals_conn.send("cooldown")
    # wait to cool down solenoids
    time.sleep(solenoid_cooldown_s)
    hardware_visuals_conn.send("waiting")
    logger.info("Finished playback of song on hardware")


def create_connection_with_terminal():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(('127.0.0.1', 8001))
    except:
        logger.error(f"Socket connection refused. Run netcat with `nc -dkl 8001`.")
        raise ConnectionRefusedError


def hardware_process(sigint_e, hardware_visuals_conn, play_q, ):
    log_if_in_debug_mode(logger, __name__)

    global TEST_FLAG
    TEST_FLAG = cli_args.disable_hardware

    if TEST_FLAG:
        create_connection_with_terminal()

    else:  # test mode is disabled
        create_connection_with_piano()

    while not sigint_e.is_set():
        try:
            hardware_process_loop(hardware_visuals_conn, play_q)

        except:
            pass
    else:
        logger.info("Hardware process has been shut down.")

def play_random_verified_song():

    mypath = "/Users/malcolm/Projects/Personal Projects/Bertha2/files/midi/verified"
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]

    random.shuffle(onlyfiles)

    for mid_track in onlyfiles:
        try:
            asyncio.run(
                play_midi_file(f"{mypath}/{mid_track}"))
            time.sleep(10)
        except KeyboardInterrupt:
            time.sleep(3)
            continue



if __name__ == '__main__':
    logger.info("Running some tests.")

    create_connection_with_piano()

    # asyncio.run(test_every_note())
    # asyncio.run(test_every_note_at_once())

    # turn_on_some_notes()  # NOTE: Don't run this with power enabled

    # mid_tracks = ["Pirate.mid"]
    #
    # for mid_track in mid_tracks:
    #     asyncio.run(play_midi_file(f"/Users/malcolm/Projects/Personal Projects/Bertha2/files/midi/verified/{mid_track}"))
    #     time.sleep(10)

    play_random_verified_song()
