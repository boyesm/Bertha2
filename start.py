from multiprocessing import Process, Queue, Event, Pipe
import os
import time
from pathlib import Path
from argparse import ArgumentParser

from settings import dirs, queue_save_file
import signal
import json

from input.chat import chat_process
# from input.cli import cli_process
from converter import converter_process
from hardware import hardware_process
from tests.hardware import test_hardware_process
from visuals import visuals_process

os.environ['IMAGEIO_VAR_NAME'] = 'ffmpeg'

# Initialize command line args
parser = ArgumentParser(prog = 'Bertha2')
parser.add_argument('--disable_hardware', action='store_true')  # checks if the `--disable_hardware` flag is used


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

    print(f"START: Loading queue: {queue_name}")

    q = Queue()

    try:
        with open(f'{queue_save_file}.json') as f:
            o = json.load(f)

        # save it into a queue
        for item in o[queue_name]:
            q.put(item)
    except Exception as e:
        print(f"START: Queue could not be loaded. {e}")

    return q


if __name__ == '__main__':

    print("START: Initializing Bertha2...")
    create_dirs(dirs)

    # Parse command line args
    args = parser.parse_args()

    # Set signal handling of SIGINT to ignore mode.
    default_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    # TODO: refactor this so that we have a shared state among all the processes instead of weird queue and pipe systems.

    link_q = load_queue("link_q")  # we need a queue for youtube links
    play_q = load_queue("play_q")  # this is the queue of ready to play videos
    title_q = Queue() # queue of video names for obs to display
    video_name_list = []  # The list is only 10 items long  # TODO: this doesn't need to be created here (it doesn't seem like it anyway). it should just be created in livestream.py

    parent_conn, child_conn = Pipe()
    p1_conn, c1_conn = Pipe()

    sigint_e = Event()
    # TODO: if processes crash, restart them automatically
    input_p = Process(target=chat_process, args=(link_q,))
    # input_p = Process(target=cli_process, args=(link_q,))
    converter_p = Process(target=converter_process, args=(sigint_e,child_conn, link_q,play_q,title_q))
    hardware_p = Process(target=hardware_process, args=(sigint_e,c1_conn,play_q,title_q,))  # TODO: this might need to be changed to the livestream process, which can in-turn call hardware and play video
    visuals_p = Process(target=visuals_process, args=(parent_conn,p1_conn,title_q,))

    input_p.daemon = True
    converter_p.daemon = True
    hardware_p.daemon = True
    visuals_p.daemon = True

    input_p.start()
    converter_p.start()
    if not args.disable_hardware:
        hardware_p.start()
    else:
        test_hardware_process.start()
    visuals_p.start()

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
    except Exception as e:
        print(f"START: Error has occurred. {e}")
    finally:
        save_queues(link_q, play_q)
        print("START: Shut down.")