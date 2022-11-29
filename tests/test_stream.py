# this program is designed to stress test the stream
# watch and realize bugs with the system
# need different twitch creds to send test messages

import socket
from os import getenv
from dotenv import load_dotenv
import time


## LOAD SECRETS
load_dotenv("../secrets.env")

nickname = getenv("TESTBOT_NICKNAME")
token = getenv("TESTBOT_TOKEN")
client_id = getenv("TESTBOT_CLIENT_ID")
channel = "berthatwo"


## CONNECT TO TWITCH
sock = socket.socket()
sock.connect(("irc.chat.twitch.tv", 6667))
sock.send(f"PASS {token}\n".encode("utf-8"))
sock.send(f"NICK {nickname}\n".encode("utf-8"))
sock.send(f"JOIN {channel}\n".encode("utf-8"))

resp = sock.recv(2048).decode("utf-8")
print(resp)

MAX_MSG_PER_SECOND = 0.5  # this is a speed that works

dx_last_message = time.time()

def send_chat_message(message):
    global dx_last_message
    if(time.time() - dx_last_message < 1/MAX_MSG_PER_SECOND):
        time.sleep((1/MAX_MSG_PER_SECOND) - (time.time() - dx_last_message))

    print(f"PRIVMSG #{channel} :{message}\r\n")
    sock.send(f"PRIVMSG #{channel} :{message}\r\n".encode("utf-8"))
    dx_last_message = time.time()
    # NOTE: the space between the channel name and the semicolon is critical
    # additionally, the /r/n at the end of the statement is also mandatory


if __name__ == "__main__":

    resp = sock.recv(2048).decode("utf-8")
    print(resp)

    yt_arr = ["https://www.youtube.com/watch?v=jt9mM1jw7PE&list=RDMM&index=6",
              "https://www.youtube.com/watch?v=NUC2EQvdzmY&list=RDMM&index=8",
              "https://www.youtube.com/watch?v=ncvH_ZD8Gjs&list=RDMM&index=14",
              "https://www.youtube.com/watch?v=J2AHvZWojSc&list=RDMM&index=25",
              "https://www.youtube.com/watch?v=kfzRXseSBIM&list=RDMM&index=27"]

    for el in yt_arr:
        send_chat_message(f"!play {el}")


