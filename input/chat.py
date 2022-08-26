import multiprocessing
from multiprocessing import Queue
from pprint import pprint

from settings import token, nickname, channel, client_id
from input.valid_link import is_valid_youtube_video
from twitchio.ext import commands


class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        super().__init__(token=token, prefix='!', initial_channels=[channel])


    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')


    @commands.command()
    async def play(self, ctx: commands.Context):

        command_arg = ctx.message.content
        print(command_arg)

        if is_valid_youtube_video(command_arg):
            # Queue.put adds command_arg to the global Queue variable, not a local Queue.
            # See multiprocessing.Queue for more info.
            # TODO: we can add video_name_q.put() here instead. just use the youtube link that we have here and create a youtube object

            link_q.put(command_arg)
            print(f"CHAT: the video follow video has been queued: {command_arg}")

            await ctx.send(f"{ctx.author.name}  Added the video to the queue. Thanks!")

        else:
            await ctx.send(f"{ctx.author.name} Sorry, we couldn't find this video. Please try another link")
            # print("CHAT: invalid youtube video")

def chat_process(link_q:multiprocessing.Queue):

    bot = Bot()
    bot.run()


if __name__ == "__main__":


    link_q = Queue()
    chat_process(link_q)