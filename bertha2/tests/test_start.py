import unittest
from multiprocessing import Queue
from pytube import Playlist
from pytube import YouTube
from pytube.extract import video_id
from bertha2.start import save_queues, load_queue


class TestQueueSave(unittest.TestCase):

    # create mock queues
    link_q = Queue()  # queue for YouTube links
    play_q = Queue()  # queue of ready to play videos (and their absolute file path)

    def setUp(self):

        yt_arr = Playlist(
            "https://www.youtube.com/watch?v=q6EoRBvdVPQ&list=PLFsQleAWXsj_4yDeebiIADdH5FMayBiJo").video_urls

        for link in yt_arr:
            self.link_q.put(link)

        for link in yt_arr:
            self.play_q.put(f"{video_id(link)}.mp4")


    def test_save_n_load(self):


        # ensure that after the queues have been saved and loaded, they're the same.

        # create backups of the queues
        link_q_backup = self.link_q
        play_q_backup = self.play_q

        # save queues
        save_queues(link_q_backup, play_q_backup)

        # load queues
        link_q_loaded = load_queue("link_q")
        play_q_loaded = load_queue("play_q")

        # check they're the same
        self.assertEqual(link_q_loaded.queue, self.link_q.queue)
        self.assertEqual(play_q_loaded.queue, self.play_q.queue)



    '''
    def tearDown(self):
        # code that is run once tests are finished
        return
    '''



if __name__ == '__main__':
    unittest.main()
