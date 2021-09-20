import socket
import time
import asyncio

# import these
server = 'irc.chat.twitch.tv'
port = 6667
nickname = 'berthatwo'
token = 'oauth:in0hpn521ekxrnmhxkzwz64swmein9'
# channel = '#berthatwo'
channel = "#ludwig"

sock = socket.socket()
sock.connect((server, port))
sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

async def check_for_commands():
    resp = sock.recv(2048).decode('utf-8')

    print(resp)

    if resp.startswith('PING'):
        sock.send("PONG\n".encode('utf-8'))

    try:
        message = resp.split(':')[2]
        print(message)
        if message[:1] == '!':
            command = message.split(' ')[0]
            print(command)
            if command == '!play':
                print('playing video')
                # play
    except:
        pass

asyncio.run(check_for_commands())