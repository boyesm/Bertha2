from multiprocessing import Queue
from is_valid_youtube_link import is_valid_youtube_video

def cli_process(link_q):

    print("CLI: Ready and waiting for links...")

    while True:
        command_arg = input()

        try:
            if is_valid_youtube_video(command_arg):
                # Queue.put adds command_arg to the global Queue variable, not a local Queue.
                # See multiprocessing.Queue for more info.
                link_q.put(command_arg)
                print(f"CHAT: the video follow video has been queued: {command_arg}")
            else:
                print("CHAT: invalid youtube video")

        except:
            pass

if __name__ == "__main__":

    play_queue = Queue()
    cli_process(play_queue)