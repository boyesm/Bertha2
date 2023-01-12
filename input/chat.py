import socket
import time
from pprint import pprint
import logging
from pytube import YouTube
from settings import channel, nickname, token, cli_args
from multiprocessing import Queue
from input.valid_link import is_valid_youtube_video

### LOGGING SETUP ###
logger = logging.getLogger(__name__)
if cli_args.debug_chat:  # If the debug flag is set high, enable debug level logging
    logging.getLogger(__name__).setLevel(logging.DEBUG)


def send_privmsg(sock, message, twitch_channel, reply_id=None):
    if reply_id is not None:
        msg = f"@reply-parent-msg-id={reply_id} PRIVMSG #{twitch_channel} :{message}\r\n"
        sock.send(msg.encode("utf-8"))
        logger.debug(msg)
    else:
        msg = f"PRIVMSG #{twitch_channel} :{message}\r\n"
        sock.send(msg.encode("utf-8"))
        logger.debug(msg)


def parse_privmsg(msg):
    if msg == '':
        return

    logger.debug(msg)

    msg = msg.strip()
    msg = msg.split(" :")

    # check if privmsg
    if "PRIVMSG" not in msg[1]:
        return

    tags = msg[0].split(";")
    msg_id = tags[8].split("=")[1].strip()
    username = tags[4].split("=")[1].strip()

    msg_content = msg[2].strip()
    command, command_arg = None, None
    if msg_content[:1] == "!":
        command = msg_content.split(" ")[0].strip()
        command_arg = msg_content.split(" ")[1].strip()

    return {
        'msg_id': msg_id,
        'username': username,
        'msg_content': msg_content,
        'command': command,
        'command_arg': command_arg,
    }


def chat_process(link_q):
    """
    Reads through twitch chat and parses out commands

    :param: link_q: The queue that the YouTube links from chat should be added to
    :return:
    """

    logger.debug(f"twitch token, nickname: {token}, {nickname}")

    # https://dev.twitch.tv/docs/irc
    sock = socket.socket()
    sock.connect(("irc.chat.twitch.tv", 6667))  # connect to server
    sock.send(f"CAP REQ :twitch.tv/tags\n".encode("utf-8"))  # req capabilities
    resp = sock.recv(2048).decode("utf-8")  # check if cap req was successful
    logger.debug(resp)
    if "CAP * NAK" in resp:
        logger.critical("Capabilities couldn't be requested.")
        raise ConnectionRefusedError
    sock.send(f"PASS {token}\n".encode("utf-8"))  # auth user
    sock.send(f"NICK {nickname}\n".encode("utf-8"))
    resp = sock.recv(2048).decode("utf-8")  # check if auth was successful
    print(resp)
    if "Improperly formatted auth" in resp:
        logger.critical("Improperly formatted auth.")
        raise ConnectionRefusedError
    if "Login authentication failed" in resp:
        logger.critical("Login authentication failed.")
        raise ConnectionRefusedError
    sock.send(f"JOIN #{channel}\n".encode("utf-8"))  # join channel
    resp = sock.recv(2048).decode("utf-8")  # get join messages
    logger.debug(resp)

    logger.info(f"Ready and waiting for twitch commands in [{channel}]...")

    while True:
        try:
            resp = sock.recv(2048).decode("utf-8")

            # this code ensures the IRC server knows the bot is still listening
            if resp.startswith("PING"):
                sock.send("PONG\n".encode("utf-8"))
                continue
            else:
                message_object = parse_privmsg(resp)
                if message_object is None:
                    continue
                logger.debug(message_object)

            if message_object["command"] == "!play":

                logger.debug(message_object["msg_content"])
                if is_valid_youtube_video(message_object["command_arg"]):
                    # Queue.put adds command_arg to the global Queue variable, not a local Queue. See
                    # multiprocessing.Queue for more info.
                    # TODO: we can add video_name_q.put() here instead. just use
                    #   the youtube link that we have here and create a youtube object

                    link_q.put(message_object["command_arg"])
                    logger.info(f"The video follow video has been queued: {message_object['command_arg']}")

                    send_privmsg(sock, f"Your video ({message_object['command_arg']}) has been queued.", channel,
                                 reply_id=message_object["msg_id"])

                else:
                    logger.debug(f"invalid youtube video")

                    send_privmsg(sock,
                                 f"Sorry, {message_object['command_arg']} is not a valid YouTube link. It's either an invalid link or it's age restricted.",
                                 channel,
                                 reply_id=message_object["msg_id"])

        except Exception as e:
            logger.critical(f"Error{e}")
            pass
