'''
what this file should do:
- read midi file (take a midi file location as input)
- convert to data playable by the hardware
- play on hardware
'''
import time
# import asyncio

starting_note = 0 # note that actuators start on
number_of_notes = 50 # number of actuators
time_interval = 20 # milliseconds

# def check_db  ### always be checking db for songs to play


def play_midi_file(midi_filename): # add a parameter to determine how much time the file is played for

    # initialize
        # parse midi file
        # etc...
        # signal initization has been completed to calling function (this is so that video can be synced with piano audio) ### toggle flag in db?



    # loop
        # track time in some way
        # at current time, determine which notes should be depressed, and for how long
        # call async functions that depress those notes for set duration

    length_of_midi_file # calculate the length in milliseconds of the midi file

    for i in range(0, length_of_midi_file, time_interval):















#### hardware stuff



### docs: https://circuitpython.readthedocs.io/projects/pca9685/en/latest/examples.html
from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685

i2c_bus = busio.I2C(SCL, SDA) # Create the I2C bus interface.
pca = PCA9685(i2c_bus) # Create a simple PCA9685 class instance.
pca.frequency = 60 # Set the PWM frequency to 60hz.
# pca.channels[0].duty_cycle = 0x7FFF # Set the PWM duty cycle for channel zero to 50%. # max value is 65535, min is 0

def power_draw_function(time, note_velocity): # a function to produce an optimal duty cycle value for the solenoid so it doesn't draw unnecessary current
    starting_duty_cycle # function of velocity
    final_duty_cycle # function of velocity

    return duty_cycle_at_time_t

def turn_on_solenoid(note_number, note_duration, note_velocity): # this needs to be async # note_duration is in milliseconds (or converted to such)

    for i in range(0, note_duration, time_interval): # time values in this function won't be completely accurate
        pca.channels[note_number].duty_cycle = hex(power_draw_function(i, note_velocity))
        time.sleep(time_interval/1000)







