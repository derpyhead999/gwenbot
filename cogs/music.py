import discord
from discord.ext import commands
import youtube_dl
import asyncio
import random
import time
import validators
from bot import YOUTUBE_API_KEY
from googleapiclient.discovery import build

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
        bot_voice_channel = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice_channel = ctx.author.voice.channel
        if bot_voice_channel and bot_voice_channel.is_connected():
            await bot_voice_channel.move_to(voice_channel)
            return
        await voice_channel.connect()

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
    async def play(self, ctx, *, query=""):
        voice_client = ctx.guild.voice_client
        if voice_client == None:
            print(voice_client)
            await ctx.send("Gwen is not connected to a voice channel!")
            return
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        if not query:
            if not self.song_queue:
                await ctx.send("No songs in queue...")
                return
            data = self.song_queue.pop(0)
        else:
            # Check if input is a url or simple search term
            if not validators.url(query):
                # It is definitely not a link; perform youtube search
                search_response = (
                    youtube.search()
                    .list(
                        q=query,
                        part="id,snippet",
                        maxResults=3,
                        type="video",
                    )
                    .execute()
                )
                if not search_response:
                    await ctx.send(
                        "Couldn't find any related songs! Try use more accurate terms"
                    )
                    return
                video_id = search_response["items"][0]["id"]["videoId"]
                query = f"https://www.youtube.com/watch?v={video_id}"

            data = await self.loop.run_in_executor(
                None, lambda: ytdl.extract_info(url=query, download=False)
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
    async def add_song(self, ctx, *, query=""):
        if not ctx.voice_client.is_playing():
            # If song queue is empty, play song immediately
            await ctx.invoke(self.bot.get_command("play"), query=query)
            return

        if not query:
            await ctx.send("Please specify a song to add (╬≖_≖)")
            return

        data = await self.loop.run_in_executor(
            None, lambda: ytdl.extract_info(url=query, download=False)
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
            await ctx.send("Gwen has been paused!")
        else:
            await ctx.send(
                "Gwen is not playing anything at the moment. Use !play [url] command"
            )

    @commands.command(name="resume", help="Resumes the song")
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
            await ctx.send("Resuming song!")
        else:
            await ctx.send(
                "The bot was not playing anything before this. Use !play [url] command"
            )

    @commands.command(name="stop", help="Stops the song")
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
            await ctx.send("Current song has been cancelled")
        else:
            await ctx.send(
                "Gwen is not playing anything at the moment. Use !play [url] command"
            )

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
        embed.add_field(
            name="Duration", value=self.song_queue[0]["duration"], inline=True
        )
        embed.add_field(
            name="Channel", value=self.song_queue[0]["channel"], inline=True
        )
        embed.add_field(
            name="Views", value=self.song_queue[0]["view_count"], inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name="queue", help="Displays the entire queue of songs")
    async def show_queue(self, ctx):
        embed = discord.Embed(
            title="Queued Songs",
            description="Top of the list is next in queue",
            color=0x3100F5,
        )
        for song in self.song_queue:
            embed.add_field(name=song["title"], value="", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="pop", help="Removes the song at the end of the queue")
    async def pop_song(self, ctx):
        song = self.song_queue.pop()
        if not song:
            await ctx.send("No songs in queue!")
        title = song["title"]
        await ctx.send(f"Popped off {title} from the end of the queue!")

    @commands.command(name="remove", help="Removes the upcoming song from the queue")
    async def remove_song(self, ctx):
        song = self.song_queue.pop(0)
        if not song:
            await ctx.send("No songs in queue!")
        title = song["title"]
        await ctx.send(f"Removed the upcoming song {title} from the queue!")


async def setup(bot: commands.Cog):
    await bot.add_cog(MusicCog(bot))
