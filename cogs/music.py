import discord
from discord.ext import commands
import youtube_dl
import asyncio
import random
import time

ytdlopts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0",
    "force-ipv4": True,
    "preferredcodec": "mp3",
    "cachedir": False,
}

ffmpeg_options = {
    "options": "-vn",
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
}

ytdl = youtube_dl.YoutubeDL(ytdlopts)


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.song_queue = []
        self.loop = asyncio.get_event_loop()

    def play_next(self, ctx):
        voice_client = ctx.guild.voice_client
        if len(self.song_queue) >= 1:
            data = self.song_queue.pop(0)
            song = data["url"]
            try:
                voice_client.play(
                    discord.FFmpegPCMAudio(
                        source=song, **ffmpeg_options, executable="ffmpeg"
                    ),
                    after=lambda e: MusicCog.play_next(self, ctx),
                )  # playing the audio
                voice_client.source = discord.PCMVolumeTransformer(
                    voice_client.source, 0.15
                )
            except Exception as e:
                print(e)

        else:
            time.sleep(90)
            if not voice_client.is_playing():
                asyncio.run_coroutine_threadsafe(voice_client.disconnect(), self.loop)
                asyncio.run_coroutine_threadsafe(
                    ctx.send("No songs in queue; shutting down"), self.loop
                )

    @commands.command(name="join", help="Tells the bot to join the voice channel")
    async def join_call(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(
                "{} is not connected to a voice channel".format(ctx.message.author.name)
            )
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

        # try:
        #   voice_channel = (
        #     ctx.author.voice.channel
        #   )  # checking if user is in a voice channel
        # except AttributeError:
        #   return await ctx.send(
        #     "No channel to join. Make sure you are in a voice channel."
        #   )  # member is not in a voice channel

        # permissions = voice_channel.permissions_for(ctx.me)
        # if not permissions.connect or not permissions.speak:
        #   await ctx.send(
        #     "I don't have permission to join or speak in that voice channel."
        #   )
        #   return

    @commands.command(name="leave", help="To make the bot leave the voice channel")
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")

    @commands.command(name="play", help="To play song")
    async def play(self, ctx, url=""):
        voice_client = ctx.guild.voice_client
        if voice_client == None:
            await ctx.send("Gwen is not connected to a voice channel!")
            return

        if not url:
            if not self.song_queue:
                await ctx.send("No songs in queue...")
                return
            data = self.song_queue.pop(0)
        else:
            data = await self.loop.run_in_executor(
                None, lambda: ytdl.extract_info(url=url, download=False)
            )  # extracting the info and not downloading the source

        if "entries" in data:
            # checking if the url is a playlist or not; extends from else statement
            data = random.choice(
                data["entries"]
            )  # if its a playlist, we get a random item from it

        title = data["title"]  # getting the title
        song = data["url"]  # getting the url

        try:
            voice_client.play(
                discord.FFmpegPCMAudio(
                    source=song, **ffmpeg_options, executable="ffmpeg"
                ),
                after=lambda e: MusicCog.play_next(self, ctx),
            )  # playing the audio
            voice_client.source = discord.PCMVolumeTransformer(
                voice_client.source, 0.15
            )
            await ctx.send(
                f"**Now playing:** {title}"
            )  # sending the title of the video
        except Exception as e:
            print(e)
            await ctx.send(f"An error occurred. :pensive:")

    @commands.command(name="add", help="Adds a song to the end of the queue")
    async def add_song(self, ctx, url):
        data = await self.loop.run_in_executor(
            None, lambda: ytdl.extract_info(url=url, download=False)
        )  # extracting the info and not downloading the source

        if "entries" in data:  # checking if the url is a playlist or not
            data = random.choice(
                data["entries"]
            )  # if its a playlist, we get a random item from it
        title = data["title"]
        self.song_queue.append(data)
        await ctx.send(f"Added {title} to the queue!")

    @commands.command(name="clear", help="Clears the queue of songs")
    async def clear_queue(self, ctx):
        del self.song_queue[:]
        await ctx.send("Song queue has been emptied!")

    @commands.command(name="pause", help="This command pauses the song")
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name="resume", help="Resumes the song")
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
        else:
            await ctx.send(
                "The bot was not playing anything before this. Use !play [url] command"
            )

    @commands.command(name="stop", help="Stops the song")
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
        else:
            await ctx.send("The bot is not playing anything at the moment.")

    @commands.command(name="next", help="Gets the name of the next song")
    async def get_song(self, ctx):
        if not self.song_queue:
            await ctx.send("No songs left in queue")
            return
        color = random.randint(0, 0xFFFFFF)
        embed = discord.Embed(
            title=self.song_queue[0]["title"],
            description="Next Song",
            color=color,
        )
        await ctx.send(embed=embed)


async def setup(bot: commands.Cog):
    await bot.add_cog(MusicCog(bot))
