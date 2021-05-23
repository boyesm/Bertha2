# always waiting for web requests
# when a web request is received, user input is validated and sent to db


# when a 'play' command is received, validate the link, then send to db
import irc.bot, requests


from global_vars import tl
from pytube import YouTube, extract
from datetime import datetime
from dbEngine import dbEngine

def get_file_name(link):
    return str(extract.video_id(link))

def check_if_valid_youtube_link(user_input):

    print("LINK TO CHECK: ", user_input)
    # try:

    yt = YouTube(user_input) # YouTube("https://www.youtube.com/watch?v=KRbsco8M7Fc")
    yt.check_availability()


    if yt.length <= 390:

        return True

    else:

        return False

    # except:
    #
    #     print("Error: Unable to determine if video is valid")
    #     return False


def getKeyFromFakeDict(key, parse):
    dictValue = ""
    endLocation = 0
    location = parse.find(key)
    for i in range(location,len(parse)-location):

        if endLocation == 0:
            if parse[i] == "!":
                endLocation = i

    dictValue = parse[location+len(key)+2:endLocation]
    # print("Key found at:", location)
    # print("End key found at:",endLocation)

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
            print('Received command: ' + cmd + 'from' + getKeyFromFakeDict("source",str(e)))
            # print("Raw information from message:" + e.arguments[0])
            self.do_command(cmd, e)

        return

    def do_command(self, cmd, e):

        engine = dbEngine()

        # Take the argument right after the command. With !play the next argument will be the link
        try:

            arg = e.arguments[0].split(' ')[1]

            print("ARGUMENTS")
            print(e.arguments[0])

        except:

            print("Error pulling argument after command in twitchBot")
            return


        # Poll the API to get current game.
        if cmd == "play":

            if(check_if_valid_youtube_link(arg)):

                youtube_url = arg
                # The converter now handles db interactoions, with this just invoking the converter
                dateAdded = datetime.now()

                engine.insertQuery(f"INSERT INTO Bertha2Table(dateadded, played, converted, link) VALUES ('{dateAdded}', 0, 0, '{youtube_url}')")

                # c.privmsg(self.channel, "The video has been added to the queue")

            # else:

                # c.privmsg(self.channel, "The video has NOT been added to the queue. If it longer than 3 minutes, it will not be added.")

            

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


