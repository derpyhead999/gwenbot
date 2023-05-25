# bot.py
import os

# imports
import discord
from discord.ext import commands
import random

from copypastaList import copypastas

from dotenv import load_dotenv
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_NAME = os.getenv("DISCORD_SERVER_NAME")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
YOUTUBE_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
DANBOORU_API_KEY = os.getenv("DANBOORU_API_KEY")
KONACHAN_PASSWORD = os.getenv("KONACHAN_PASSWORD")
# import youtube_dl

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# client = discord.Client(intents=intents)
help_command = commands.DefaultHelpCommand(no_category="Commands")
bot = commands.Bot(command_prefix="!", intents=intents, help_command=help_command)


# Sends message on user join
@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name="general")
    await channel.send(f"Hontouni poggers, {member.name}! Welcome to {SERVER_NAME}!")


# Generates a random copypasta from a list of stored copypastas
@bot.command(name="copypasta", help="Gives you a random copypasta")
async def generate_copypasta(ctx):
    response = random.choice(copypastas)
    await ctx.send(response)


# quote command


@bot.command(name="quit")
@commands.is_owner()
async def quit(ctx):
    await bot.close()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


@bot.command()
@commands.is_owner()
async def reload(ctx, extension: str = ""):
    if not extension or extension.lower() == "all":
        for ext in initial_extensions:
            await bot.reload_extension(ext)
        embed = discord.Embed(
            title="All Reloaded",
            description="All extensions successfully reloaded",
            color=0xFF00C8,
        )
        await ctx.send(embed=embed)
        return
    else:
        await bot.reload_extension(f"cogs.{extension}")
        embed = discord.Embed(
            title=f"{extension} Reloaded",
            description=f"{extension} successfully reloaded",
            color=0xFF00C8,
        )
        await ctx.send(embed=embed)


initial_extensions = [
    "cogs.message",
    "cogs.search",
    "cogs.uwufy",
    "cogs.user",
    "cogs.music",
]


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=SERVER_NAME)
    print(
        f"{bot.user.name} is connected to the following guild:\n"
        f"{guild.name}  <->  (id: {guild.id})"
    )


@bot.command(name="playlist")
async def playlist(ctx):
    await ctx.send(
        f"A list of some songs I found:\nhttps://music.youtube.com/playlist?list=PLW-ijL1aiiSCeyTjvIPKZbvhe-x88HU6T&feature=share"
    )


# Main function
async def main():
    async with bot:
        for extension in initial_extensions:
            await bot.load_extension(extension)
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
