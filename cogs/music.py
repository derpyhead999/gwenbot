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

ffmpeg_options = {"options": "-vn"}

ytdl = youtube_dl.YoutubeDL(ytdlopts)


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join", help="Tells the bot to join the voice channel")
    async def join_call(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send(
                "{} is not connected to a voice channel".format(ctx.message.author.name)
            )
            return
        else:
            channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        voice.source = discord.PCMVolumeTransformer(voice.source, volume=0.3)
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
    async def play(self, ctx, url):
        time.sleep(0.5)

        voice_client = ctx.guild.voice_client
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url=url, download=False)
        )  # extracting the info and not downloading the source

        title = data["title"]  # getting the title
        song = data["url"]  # getting the url

        if "entries" in data:  # checking if the url is a playlist or not
            data = random.choice(
                data["entries"]
            )  # if its a playlist, we get the first item of it

            # MAKE LIST FOR QUEUE?

        try:
            voice_client.play(
                discord.FFmpegPCMAudio(
                    source=song, **ffmpeg_options, executable="ffmpeg"
                )
            )  # playing the audio
        except Exception as e:
            print(e)

        await ctx.send(f"**Now playing:** {title}")  # sending the title of the video

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


async def setup(bot: commands.Cog):
    await bot.add_cog(MusicCog(bot))
