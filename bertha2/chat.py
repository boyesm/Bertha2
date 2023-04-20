import socket
import logging

from settings import channel, twitch_nickname, twitch_token, cli_args
from pytube import YouTube


# LOGGING SETUP
logger = logging.getLogger(__name__)
if cli_args.debug_chat:  # If the debug flag is set high, enable debug level logging
    logging.getLogger(__name__).setLevel(logging.DEBUG)

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


def parse_privmsg(msg):
    if msg == '':
        return

    logger.debug(msg.rstrip('\n').rstrip('\r'))

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
    # print(w_socket.type)
    # logger.debug(w_socket)
    resp = w_socket.recv(2048).decode("utf-8")  # check if cap req was successful

    logger.debug(resp.rstrip('\n').rstrip('\r'))
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
    logger.debug(resp.rstrip('\n').rstrip('\r'))


def handle_command(message):
    """
    Handles a twitch command, including all of its arguments
    :param message: The Twitch dict containing information about the message
    :return:
    """
    # Get different sections from the message
    command = message["command"]
    content = message["msg_content"]
    arguments = message["command_arg"]
    # The id of the message to reply to in the Twitch chat
    message_id = message["msg_id"]

    logger.debug(content)

    if command == "!play":

        if is_valid_youtube_video(arguments):

            # TODO: we can add video_name_q.put() here instead. just use
            #   the youtube link that we have here and create a youtube object
            logger.info(f"The video follow video has been queued: {arguments}")
            send_reply(f"Your video ({arguments}) has been queued.", message_id)
            return arguments

        else:
            logger.debug(f"invalid youtube video")

            response = f"Sorry, {arguments} is not a valid YouTube link. It's either an invalid link or it's age restricted."
            send_reply(response, message_id)
            return None


def send_reply(message, message_id):
    try:
        send_privmsg(web_socket,
                     message,
                     channel,
                     reply_id=message_id)
    except:
        logging.warning("Failed to send a message")


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
    # We really shouldn't be logging the twitch token, so I disabled this line
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
                if link != None:
                    link_q.put(link)

        except TypeError:
            # In this case, no message was found
            pass
        except Exception as e:

            logger.critical(f"Error {type(e).__name__}: {e}")
            pass

def is_valid_youtube_video(user_input):

    # print(user_input)

    try:
        # TEST CASE: https://www.youtube.com/watch?v=KRbsco8M7Fc
        yt = YouTube(user_input)

    except Exception as e:
        print(f"CHAT: link is invalid {e}")
        return False

    try:
        # this will return None if it's available, and an error if it's not
        yt.check_availability()

    except Exception as e:
        print(f"CHAT: {e}")
        return False

    if yt.age_restricted:
        print(f"CHAT: {user_input} is age restricted")
        return False

    # TODO: decide on an appropriate maximum video length
    if yt.length >= 390:
        print(f"CHAT: {user_input} is too long")
        return False

    return True

if __name__ == '__main__':
    chat_process()
