import os
import asyncio
import mido
import math
import time

### Goal: play each midi note with it's corresponding velocity

### Functions
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


def set_solenoid_value(value, solenoid_n):
    print(f"set solenoid {solenoid_n} to value {value}") # replace this with actual function...


async def trigger_note(init_note_delay, note, velocity, hold_note_time):

    # delay until the note should be turned on
    await asyncio.sleep(init_note_delay)

    # start loop that will initiate and adjust power output to solenoid
    start_time = time.time()

    while True:
        curr_time = time.time()
        passed_time = curr_time - start_time

        # print(f"{passed_time} {hold_note_time}")

        if passed_time > hold_note_time:
            set_solenoid_value(0, note)
            return
        else:
            y = power_draw_function(velocity, passed_time)
            set_solenoid_value(y, note)

        await asyncio.sleep(0.1)

    '''
    
    get the current time and set to a variable called init_time
    
    while:
        get the amount of time that has passed
         
        if amount of time that the note has been pressed has exceeded hold_note_time:
            return
        else:
            get value for n time on power draw function
            set power level to the respective value
        
        asyncio wait for n seconds
    '''


# midi_filename = "midi/Wii Channels - Mii Channel.mid"
midi_filename = "midi/all_notes.mid"

### Main program


async def play_midi_file(midi_filename):

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
            i+=1
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




asyncio.run(play_midi_file(midi_filename))

