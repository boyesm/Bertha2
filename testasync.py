import asyncio
import mido


background_tasks = set()

# loop = asyncio.get_event_loop()
# loop.run_forever()



async def play_note(note):
    print(f"playing note {note}")
    await asyncio.sleep(1)
    print(f"finished playing note {note}")


async def test():
    print("testtttt")


async def main():
    mid = mido.MidiFile("midi/c_repeated.mid")

    for msg in mid.play():
        if msg.type == "note_on":
            print("starting note")
            # task = asyncio.create_task(play_note(msg.note))
            task = loop.create_task(test())
            # background_tasks.add(task)
            # task.add_done_callback(background_tasks.discard)


asyncio.run(main())