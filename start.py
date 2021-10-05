from multiprocessing import Process, Queue
import os, shutil
from pathlib import Path
from settings import dirs

from input.chat import chat_process
# from input.cli import cli_process
from converter import converter_process
from hardware import hardware_process


def create_dirs(dirs):
    # try:  # TODO: don't delete this directory if it already exists! don't want to lose a bunch of files
    #     shutil.rmtree('files')
    #
    # except:
    #     pass

    for dir in dirs:
        file_dir = Path(dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)


if __name__ == '__main__':
    print("Initializing Bertha2...")

    create_dirs(dirs)

    link_q = Queue()  # we need a queue for youtube links
    play_q = Queue()  # this is the queue of ready to play videos

    # TODO: if processes crash, restart them automatically
    # twitch_p = Process(target=chat_process, args=(link_q,))  # change this so that this could be swapped with a CLI
    # converter_p = Process(target=converter_process, args=(link_q, play_q,))

    # TODO: this might need to be changed to the livestream process, which can in-turn call hardware and play video
    hardware_p = Process(target=hardware_process, args=(play_q,))

    # twitch_p.daemon = True
    # converter_p.daemon = True
    hardware_p.daemon = True

    # twitch_p.start()
    # converter_p.start()
    hardware_p.start()

    # twitch_p.join()
    # converter_p.join()
    hardware_p.join()

    print("Initializing completed...")
