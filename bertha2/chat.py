# Built-in packages
import socket
import logging
from multiprocessing import Queue

from pytube.exceptions import RegexMatchError

# Internal imports
from settings import channel, twitch_nickname, twitch_token, cli_args, MAX_YOUTUBE_VIDEO_LENGTH
from utils.logs import get_module_logger
# External imports
from pytube import YouTube
import pytube

# LOGGING SETUP
logger = get_module_logger(__name__)

web_socket = socket.socket()


def send_privmsg(sock, message, twitch_channel, reply_id=None):
    if reply_id is not None:
        msg = f"@reply-parent-msg-id={reply_id} PRIVMSG #{twitch_channel} :{message}\r\n"
        sock.send(msg.encode("utf-8"))
        logger.debug(msg)
    else:
        msg = f"PRIVMSG #{twitch_channel} :{message}\r\n"
        sock.send(msg.encode("utf-8"))
        logger.debug(msg)


def parse_privmsg(msg: str):
    if msg == '':
        return

    # TODO Should this log? What level?
    # logger.debug(msg.rstrip('\n').rstrip('\r'))

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


def login(w_socket):
    """
    Logs in to and starts listening to Twitch chat
    :return:
    """

    # w_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    w_socket.connect(("irc.chat.twitch.tv", 6667))  # connect to server
    w_socket.send(f"CAP REQ :twitch.tv/tags\n".encode("utf-8"))  # req capabilities
    # logger.debug(w_socket)

    # Try to log in 3 times
    attempts = 0
    success = False
    while attempts < 3 and not success:
        try:
            resp = w_socket.recv(2048).decode("utf-8")  # check if cap req was successful
            success = True
        except ConnectionResetError:
            return False

    # TODO Should this log? What level?
    # logger.debug(resp.rstrip('\n').rstrip('\r'))

    if "CAP * NAK" in resp:
        logger.critical("Capabilities couldn't be requested.")
        raise ConnectionRefusedError
    w_socket.send(f"PASS {twitch_token}\n".encode("utf-8"))  # auth user
    w_socket.send(f"NICK {twitch_nickname}\n".encode("utf-8"))
    resp = w_socket.recv(2048).decode("utf-8")  # check if auth was successful

    if "Improperly formatted auth" in resp:
        logger.critical("Improperly formatted auth.")
        raise ConnectionRefusedError
    if "Login authentication failed" in resp:
        logger.critical("Login authentication failed.")
        raise ConnectionRefusedError
    w_socket.send(f"JOIN #{channel}\n".encode("utf-8"))  # join channel
    resp = w_socket.recv(2048).decode("utf-8")  # get join messages

    # TODO Should this log? What level?
    # logger.debug(resp)

    return True


def handle_command(message: dict):
    """
    Handles a twitch command, including all of its arguments
    :param message: The Twitch dict containing information about the message
    :return: False if invalid, YouTube link if valid
    """
    # Get different sections from the message
    command = message["command"]
    content = message["msg_content"]
    arguments = message["command_arg"]
    # The id of the message to reply to in the Twitch chat
    message_id = message["msg_id"]

    logger.info(f"Command: {content}")

    if command == "!play":

        response_link = str(arguments).lstrip("https://")
        logger.info(f"Attempting to add: {response_link}")

        yt = create_yt_object(arguments)

        # Check if it is a valid YouTube link
        if not yt:
            logger.info("Link is invalid")
            response = f"Sorry, {response_link} is not a valid YouTube link."
            send_reply(response, message_id)
            return None

        # Check if it is age restricted
        if yt.age_restricted:
            logger.info("Video is age restricted")
            response = f"Sorry, {response_link} is age restricted."
            send_reply(response, message_id)
            return None

        # Check if it is too long
        if yt.length >= MAX_YOUTUBE_VIDEO_LENGTH:
            logger.info("Video length exceeds max")
            response = f"Sorry, {response_link} is too long. The max video length is {int(MAX_YOUTUBE_VIDEO_LENGTH/60)}:{MAX_YOUTUBE_VIDEO_LENGTH%60}"
            send_reply(response, message_id)
            return None

        # TODO: we can add video_name_q.put() here instead. just use
        #   the youtube link that we have here and create a youtube object

        logger.info(f"The video follow video has been queued: {response_link}")
        send_reply(f"Your video {response_link} has been queued.", message_id)
        return arguments

    else:
        return None


def send_reply(message, message_id):
    try:
        send_privmsg(web_socket,
                     message,
                     channel,
                     reply_id=message_id)
    except Exception as e:
        logging.warning(f"Failed to send a message: {type(e).__name__}: {e}")


def chat_process(link_q):
    """
    Reads through twitch chat and parses out commands
    https://dev.twitch.tv/docs/irc
    :param: link_q: The queue that the YouTube links from chat should be added to
    :return:
    """
    if not twitch_token:
        logger.critical("")
        raise FileNotFoundError
    # We really shouldn't be logging the twitch token, so I disabled this line - Jarvis
    # logger.debug(f"Twitch token, nickname: {twitch_token}, {twitch_nickname}")

    login(web_socket)

    logger.info(f"Ready and waiting for twitch commands in [{channel}]...")

    while True:
        try:
            resp = web_socket.recv(2048).decode("utf-8")
            # Keep the session active
            if resp.startswith("PING"):
                web_socket.send("PONG\n".encode("utf-8"))
            else:
                message = parse_privmsg(resp)
                # logger.debug(message)
                link = handle_command(message)
                if link is not None:
                    link_q.put(link)

        except TypeError:
            # In this case, no message was found
            pass
        except Exception as e:

            logger.critical(f"Error {type(e).__name__}: {e}")
            pass


def create_yt_object(user_input: str):
    """
    Creates a YouTube video object. If the link is not valid, returns false
    :param user_input: URL of the video
    :return:
    """
    try:

        # TEST CASE: https://www.youtube.com/watch?v=KRbsco8M7Fc  # TODO This should go in tests right?
        logger.debug(f"Creating YouTube object...")
        yt = YouTube(user_input)  # if not an url, this will fail
        if yt.age_restricted:  # return so the outside handler can send the right message to the user
            return yt
        try:
            logger.info("Length: " + str(yt.length))  # If we cant access the length, it is not a valid video
        except TypeError:  # Valid link, but not valid video
            return False

        return yt

    except RegexMatchError:  # The YouTube link was not valid
        return False
    except Exception as e:
        logger.warning(f"Could not create youtube object {type(e).__name__}: {e}")
        return False


if __name__ == '__main__':
    chat_process(Queue())  # Start with an empty Queue
