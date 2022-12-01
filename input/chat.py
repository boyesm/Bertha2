import socket
import time
from pprint import pprint
import logging
from pytube import YouTube
from settings import channel, nickname, token
from multiprocessing import Queue
from input.valid_link import is_valid_youtube_video

logger = logging.getLogger(__name__)

def chat_process(link_q):
    """
    Reads through twitch chat and parses out commands

    :param link_q: The queue that the YouTube links from chat should be added to
    :return:
    """

    sock = socket.socket()
    sock.connect(("irc.chat.twitch.tv", 6667))
    sock.send(f"PASS {token}\n".encode("utf-8"))
    sock.send(f"NICK {nickname}\n".encode("utf-8"))
    sock.send(f"JOIN {channel}\n".encode("utf-8"))

    resp = sock.recv(2048).decode("utf-8")
    logger.debug(f"{resp}")

    ## This should only say this if it's true. There are not auth checks here to confirm that it's actually connected
    ## One error is "Improperly formatted auth", occurs when args aren't passed in the correct order
    logger.info(f"Ready and waiting for twitch commands in [{channel}]...")

    while True:
        try:
            resp = sock.recv(2048).decode("utf-8")

            # this code ensures the IRC server knows the bot is still listening
            if resp.startswith("PING"):
                sock.send("PONG\n".encode("utf-8"))

            for temp in range(2):
                resp = resp[resp.find(":")+1:]

            if resp == "Improperly formatted auth":
                logger.critical(f"Auth keys aren't working\nERROR: Improperly formatted auth")

            if resp != '':
                logger.debug(f"{resp}")
            #     pprint("Resp:")
            #     pprint(resp)
            message = resp


            if message[:1] == "!":

                command = message.split(" ")[0]
                command_arg = message.split(" ")[1]

                if command == "!play":

                    logger.debug(message)
                    if is_valid_youtube_video(command_arg):
                        # Queue.put adds command_arg to the global Queue variable, not a local Queue.
                        # See multiprocessing.Queue for more info.
                        # TODO: we can add video_name_q.put() here instead. just use the youtube link that we have here and create a youtube object

                        link_q.put(command_arg)
                        logger.info(f"The video follow video has been queued: {command_arg.strip()}")
                        # TODO: send a message to twitch chat that says this ^^
                    else:
                        response = " Sorry, [{message}] is not a valid youtube link"
                        sock.send(f"PRIVMSG #{channel}:{response}\n".encode("utf-8"))

                        logger.debug(f"invalid youtube video")
                        # TODO: send a message to twitch chat that says this ^^ 

        except Exception as e:
            logger.critical(f"Error{e}")
            pass

if __name__ == "__main__":

    play_queue = Queue()
    chat_process(play_queue)