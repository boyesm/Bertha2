import json
import os
import signal
from multiprocessing import Process, Queue, Event, Pipe
from pathlib import Path

from bertha2.settings import dirs, queue_save_file
from bertha2.utils.logs import initialize_root_logger

os.environ['IMAGEIO_VAR_NAME'] = 'ffmpeg'

logger = initialize_root_logger(__name__)


from bertha2.chat import chat_process
from bertha2.converter import converter_process
from bertha2.hardware import hardware_process
from bertha2.visuals import visuals_process


def create_dirs(dirs):
    for dir in dirs:
        file_dir = Path(dir)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

    logger.info(f"Created directories")


def save_queues(lq, pq):
    logger.info(f"Saving queues to database.")

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

    logger.debug(backup_file)

    with open(f'{queue_save_file}.json', 'w', encoding='utf-8') as f:
        json.dump(backup_file, f, ensure_ascii=False, indent=4)

    logger.info(f"Saved queues to database.")


def load_queue(queue_name):
    logger.info(f"Loading queue: {queue_name}")

    q = Queue()

    try:
        with open(f'{queue_save_file}.json') as f:
            o = json.load(f)

        logger.debug(o[queue_name])

        # save it into a queue
        for item in o[queue_name]:
            q.put(item)
    except Exception as ee:
        logger.critical(f"Queue could not be loaded. {ee}")

    return q


if __name__ == '__main__':

    logger.info(f"Initializing Bertha2...")
    create_dirs(dirs)

    # Set signal handling of SIGINT to ignore mode.
    default_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    link_q = load_queue("link_q")  # we need a queue for YouTube links
    play_q = load_queue("play_q")  # this is the queue of ready to play videos

    # converter -> visuals connection
    cv_parent_conn, cv_child_conn = Pipe()
    # hardware -> visuals connection. used for the hardware process to tell the visuals process when its doing things
    hv_child_conn, hv_parent_conn = Pipe()

    sigint_e = Event()
    # TODO: if processes crash, restart them automatically
    # why does visuals have the parent and child conns, when it is only receiving data?
    input_p = Process(target=chat_process, args=(link_q,))
    converter_p = Process(target=converter_process, args=(sigint_e, cv_child_conn, link_q, play_q,))
    hardware_p = Process(target=hardware_process, args=(sigint_e, hv_parent_conn, play_q,))
    visuals_p = Process(target=visuals_process, args=(cv_parent_conn, hv_child_conn,))

    input_p.daemon = True
    converter_p.daemon = True
    hardware_p.daemon = True
    visuals_p.daemon = True

    input_p.start()
    converter_p.start()
    hardware_p.start()
    visuals_p.start()

    # Since we spawned all the necessary processes already,
    # restore default signal handling for the parent process.
    signal.signal(signal.SIGINT, default_handler)

    try:
        signal.pause()
    except KeyboardInterrupt:
        logger.info(f"Shutting down gracefully...")
        sigint_e.set()
        converter_p.join()
        hardware_p.join()
    except Exception as e:
        logger.critical(f"Error has occurred. {e}")
    finally:
        save_queues(link_q, play_q)
        logger.info(f"Shut down.")