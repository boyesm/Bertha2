'''
what this file should do:
- read midi file (take a midi file location as input)
- convert to data playable by the hardware
- play on hardware
'''
import mido, time, math
import asyncio

starting_note = 0 # note that actuators start on (lowest note == 0 == C0)
number_of_notes = 50 # number of actuators
time_interval = 20 # milliseconds

# def check_db  ### always be checking db for songs to play



def play_midi_file(midi_filename): # TODO: add a parameter to determine how much time the file is played for

    loop = asyncio.get_event_loop()

    mid = mido.MidiFile(midi_filename)

    for msg in mid.play():
        # print(msg)
        if msg.type == "note_on":
            # turn note on with velocity
            # await note_on(msg.note, msg.time, msg.velocity)
            # asyncio.sleep(1)
            loop.run_until_complete(wait())
            print(msg)


async def wait():
    await time.sleep(1)
    print("lests go!")



'''
#### hardware stuff

from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685


i2c_bus = busio.I2C(SCL, SDA) # Create the I2C bus interface.
pca = PCA9685(i2c_bus) # Create a simple PCA9685 class instance.
pca.frequency = 60 # Set the PWM frequency to 60hz.

async def note_on(note, duration, velocity):

    # check if note is in range of hardware
    # turn on solenoid pwm output to highest value (this should be a function of velocity)
    # reduce the pwm signal to hold solenoid in place without overdelivering power to it

    if (note < starting_note) or (note > (starting_note + number_of_notes)): # check if note is in range of hardware
        return

    start_time = time.time()
    time_passed = 0

    while time_passed < duration:
        pwm_value = power_draw_function(time_passed, velocity)

        update_solenoid_value(note, pwm_value)

        asyncio.sleep(time_interval / 1000)
        time_passed = time.time() - start_time # TODO: check if this is going to produce a float/int time value



def power_draw_function(time_passed, velocity): # a function to produce an optimal duty cycle value for the solenoid so it doesn't draw unnecessary current
    # starting_duty_cycle  # function of velocity
    # final_duty_cycle # function of velocity

    pwm_at_t = math.log(time_passed) + velocity # this is just an example function, not the final one!

    return pwm_at_t # max value is 65535, min is 0


def update_solenoid_value(note, pwm_value):
    pca.channels[note].duty_cycle = hex(pwm_value)






### docs: https://circuitpython.readthedocs.io/projects/pca9685/en/latest/examples.html

'''


