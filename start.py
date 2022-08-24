from multiprocessing import Process, Queue, Event
import os
import time
# import shutil
from pathlib import Path
from settings import dirs, queue_save_file
import atexit
import signal
import json

from input.chat import chat_process
from input.cli import cli_process
from converter import converter_process
from hardware import hardware_process


def create_dirs(dirs):
    for dir in dirs:
        file_dir = Path(dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

    print("START: Created directories")

def save_queues(lq, pq):

    # TODO: make sure nothing can go wrong with this code.

    print("START: Saving queues to database.")

    ll = []
    pl = []

    while lq.empty() == False:
        ll.append(lq.get())

    while pq.empty() == False:
        pl.append(pq.get())

    # save q to json file
    backup_file = {
        "play_q": pl,
        "link_q": ll
    }

    with open(f'{queue_save_file}.json', 'w', encoding='utf-8') as f:
        json.dump(backup_file, f, ensure_ascii=False, indent=4)

    print("START: Saved queues to database.")


def load_queue(queue_name):

    # TODO: Write some error checking code here. If this loads incorrectly, we should know.

    print(f"START: Loading queue: {queue_name}")

    q = Queue()

    try:
        with open(f'{queue_save_file}.json') as f:
            o = json.load(f)

        # save it into a queue
        for item in o[queue_name]:
            q.put(item)
    except:
        print("START: Queue could not be loaded.")

    return q


if __name__ == '__main__':

    print("START: Initializing Bertha2...")

    create_dirs(dirs)

    # Set signal handling of SIGINT to ignore mode.
    default_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    link_q = load_queue("link_q")  # we need a queue for youtube links
    play_q = load_queue("play_q")  # this is the queue of ready to play videos

    sigint_e = Event()

    link_q.put("https://www.youtube.com/watch?v=KRbsco8M7Fc")
    link_q.put("https://www.youtube.com/watch?v=KRbsco8M7Fc")
    link_q.put("https://www.youtube.com/watch?v=KRbsco8M7Fc")
    link_q.put("https://www.youtube.com/watch?v=KRbsco8M7Fc")

    # TODO: if processes crash, restart them automatically
    input_p = Process(target=chat_process, args=(link_q,))
    # input_p = Process(target=cli_process, args=(link_q,))
    converter_p = Process(target=converter_process, args=(sigint_e,link_q, play_q,))
    hardware_p = Process(target=hardware_process, args=(sigint_e,play_q,))  # TODO: this might need to be changed to the livestream process, which can in-turn call hardware and play video

    input_p.daemon = True
    converter_p.daemon = True
    hardware_p.daemon = True

    input_p.start()
    converter_p.start()
    hardware_p.start()

    # Since we spawned all the necessary processes already,
    # restore default signal handling for the parent process.
    signal.signal(signal.SIGINT, default_handler)

    try:
        signal.pause()
    except KeyboardInterrupt:
        print("START: Shutting down gracefully...")
        sigint_e.set()
        converter_p.join()
        hardware_p.join()
    except:
        print("START: Error has occurred.")
    finally:
        save_queues(link_q, play_q)
        print("START: Shut down.")
