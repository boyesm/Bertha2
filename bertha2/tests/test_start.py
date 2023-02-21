import os
import unittest
from multiprocessing import Queue

from pytube import Playlist
from pytube.extract import video_id

from bertha2.settings import queue_save_file
from bertha2.start import save_queues, load_queue


def convert_queue_to_list(in_queue):
    out_list = []

    while in_queue.empty() == False:
        out_list.append(in_queue.get())

    return out_list


def convert_list_to_queue(in_list):
    out_q = Queue()

    for i in in_list:
        out_q.put(i)

    return out_q


class TestQueueSave(unittest.TestCase):
    link_list = []
    play_list = []

    def setUp(self):

        # TODO: safely delete existing saved_queues.json file
        try:
            os.remove(f"{queue_save_file}.json")
        except FileNotFoundError:
            pass

        # create a mock queue with YouTube links in it
        yt_arr = Playlist(
            "https://www.youtube.com/watch?v=q6EoRBvdVPQ&list=PLFsQleAWXsj_4yDeebiIADdH5FMayBiJo").video_urls

        for link in yt_arr:
            self.link_list.append(link)

        for link in yt_arr:
            self.play_list.append(f"{video_id(link)}.mp4")

    # ensure that after the queues have been saved and loaded, they're the same.
    def test_queue_save_and_load(self):

        # mp queues cannot be compared directly, instead they must be converted to lists and compared
        # create queues from lists
        link_q_save = convert_list_to_queue(self.link_list)
        play_q_save = convert_list_to_queue(self.play_list)

        # save queues
        save_queues(link_q_save, play_q_save)

        # load queues
        link_q_loaded = load_queue("link_q")
        play_q_loaded = load_queue("play_q")

        # converted loaded queues into lists
        link_q_loaded_list = convert_queue_to_list(link_q_loaded)
        play_q_loaded_list = convert_queue_to_list(play_q_loaded)

        # check they're the same
        self.assertEqual(link_q_loaded_list, self.link_list)
        self.assertEqual(play_q_loaded_list, self.play_list)

    def tearDown(self):
        os.remove(f"{queue_save_file}.json")


if __name__ == '__main__':
    unittest.main()
