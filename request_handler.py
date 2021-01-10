# always waiting for web requests
# when a web request is received, user input is validated and sent to db


# when a 'play' command is received, validate the link, then send to db
import time, sys, irc.bot, requests
from sqlalchemy import create_engine
from global_vars import midi_file_path, audio_file_path, video_file_path, queue_table, tl
from pytube import YouTube

engine = create_engine('sqlite:///bertha2.db')
conn = engine.connect()

def get_file_name(link):
    return link[32:43]

def check_if_valid_youtube_link(user_input):
    try:
        yt = YouTube(user_input)
        yt.check_availability()
        if yt.length <= 180:
            return True
        else:
            return False
    except:
        return False

# def check_if_valid_user(username): # only allow 1 upload per IP/User-agent per n minutes
#     return True


def getKeyFromFakeDict(key, parse):
    dictValue = ""
    endLocation = 0
    location = parse.find(key)
    for i in range(location,len(parse)-location):

        if endLocation == 0:
            if parse[i] == "!":
                endLocation = i

    dictValue = parse[location+len(key)+2:endLocation]
    print("Key found at:", location)
    print("End key found at:",endLocation)

    return dictValue


class TwitchBot(irc.bot.SingleServerIRCBot):

    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel.lower()

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        print(r)
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):

        url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
        headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}

        # print(e)

        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            print('Received command: ' + cmd)
            # print("Raw information from message:" + e.arguments[0])
            print("Sent user:", getKeyFromFakeDict("source",str(e)))
            self.do_command(cmd, e)
        return

    def do_command(self, cmd, e):
        c = self.connection

        try:
            arg = e.arguments[0].split(' ')[1]
        except:
            return

        # Poll the API to get current game.
        if cmd == "play":
            if check_if_valid_youtube_link(arg):
                # print('valid input')
                create_row = queue_table.insert().values(username=str(getKeyFromFakeDict("source",str(e))), link=arg, filename=get_file_name(arg), isconverted=False, isqueued=False)
                conn.execute(create_row)
                c.privmsg(self.channel, "The video has been added to the queue")
            else:
                # print('invalid input')
                c.privmsg(self.channel, "The video has NOT been added to the queue. If it longer than 3 minutes, it will not be added.")

            
            
        # # Poll the API the get the current status of the stream
        # elif cmd == "title":
        #     url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
        #     headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        #     r = requests.get(url, headers=headers).json()
        #     c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        # elif cmd == "toes":
        #     url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
        #     headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        #     r = requests.get(url, headers=headers).json()
        #     c.privmsg(self.channel, 'Yes indeed, ' + r['display_name'] + ' has poggers toes! Lots of cheese!')
        # else:
        #     c.privmsg(self.channel, "Did not understand command: " + cmd)


bot = TwitchBot(tl['username'], tl['clientid'], tl['token'], tl['channel'])
bot.start()

