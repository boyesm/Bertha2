"""
this process controls livestream visuals
"""


def livestream_process(play_q):
    while True:
        filepath = play_q.get() # get video file from q




