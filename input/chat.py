import socket
import time
from pytube import YouTube
from settings import nickname, token, channel


def valid_youtube_video(user_input):
    try:
        # TEST CASE: https://www.youtube.com/watch?v=KRbsco8M7Fc
        yt = YouTube(user_input)

    except Exception as e:
        print(f"link is invalid {e}")
        return False

    try:
        # this will return None if it's available, and an error if it's not
        yt.check_availability()

    except Exception as e:
        print(e)
        return False

    if yt.age_restricted:
        print(f"{user_input} is age restricted")
        return False

    # TODO: decide on an appropriate maximum video length
    if yt.length >= 390:
        print(f"{user_input} is too long")
        return False

    return True


def chat_process(link_q):
    # this will read through twitch chat and parse out commands

    sock = socket.socket()
    sock.connect(("irc.chat.twitch.tv", 6667))
    sock.send(f"PASS {token}\n".encode("utf-8"))
    sock.send(f"NICK {nickname}\n".encode("utf-8"))
    sock.send(f"JOIN {channel}\n".encode("utf-8"))

    while True:
        resp = sock.recv(2048).decode("utf-8")

        # this code ensures the IRC server knows the bot is still listening
        if resp.startswith("PING"):
            sock.send("PONG\n".encode("utf-8"))

        try:
            message = resp.split(":")[2]

            if message[:1] == "!":

                command = message.split(" ")[0]
                command_arg = message.split(" ")[1]

                if command == "!play":

                    if valid_youtube_video(command_arg):
                        link_q.put(command_arg)

                    else:
                        print("invalid youtube video")

        except:
            pass