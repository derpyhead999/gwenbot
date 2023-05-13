# bot.py
import os

# imports
import discord
import random

from copypastaList import copypastas

from dotenv import load_dotenv

from discord.ext import commands


load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER_NAME = os.getenv("DISCORD_SERVER_NAME")


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=SERVER_NAME)

    print(
        f"{bot.user.name} is connected to the following guild:\n"
        f"{guild.name}  <->  (id: {guild.id})"
    )

    members = "\n - ".join([member.name for member in guild.members])
    print(f"Guild Members:\n - {members}")


@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name="general")
    await channel.send(f"Hontouni poggers, {member.name}! Welcome to {SERVER_NAME}!")


@bot.command(name="copypasta", help="Gives you a random copypasta")
async def generate_copypasta(ctx):
    response = random.choice(copypastas)
    await ctx.send(response)


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    league_call = ["league", "leeg", "lego"]
    jg_call = [
        "jungle diff",
        "jg diff",
        "jungle differential",
        "jg differential",
        "jg gap",
        "jungle gap",
    ]
    cope_call = ["copium", "cope", "overdose", "overdosing", "coping"]
    if message.author == bot.user:
        return
    if "stupid" in message.content.lower():
        await message.channel.send("stoopid")
    if "valorant" in message.content.lower():
        valorant_references = ["poggers", "least clutch nyoos momento"]
        await message.channel.send(random.choice(valorant_references))
    if any([x in message.content.lower() for x in league_call]):
        league_references = [
            "xdd",
            "chovy cs tho!!!",
            "standard peter @ daily momento",
            "tilt vibes eta 5min in vc \U0001F614",
            "[insert genius pell witty remark on league players]",
            "classico 6 man",
        ]
        await message.channel.send(random.choice(league_references))
    if "genus" in message.content.lower():
        await message.channel.send("um akshually, that's genius pell \U0001F913")
    if "peter" in message.content.lower():
        await message.channel.send("技术问题")

    if message.content.lower() == "riot":
        await message.delete()
        with open("img/RIOT.gif", "rb") as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
    if any([x in message.content.lower() for x in jg_call]):
        with open("img/myjg.png", "rb") as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
            await message.channel.send(
                "my jg watching 3 losing lanes getting blamed lvl 3"
            )
    if message.content.lower() == "xdd":
        await message.delete()
        with open("img/xdd.jpg", "rb") as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
    if "doctor" in message.content.lower():
        with open("img/DOCTOR.jpg", "rb") as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
    if "demote" in message.content.lower():
        with open("img/peter.png", "rb") as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
    if "cursed" in message.content.lower():
        with open("img/sus.png", "rb") as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
    if "sussy" in message.content.lower():
        with open("img/sussy.gif", "rb") as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
    if any([x in message.content.lower() for x in cope_call]):
        with open("img/copege.gif", "rb") as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
    if "promote" in message.content.lower():
        with open("img/promote.png", "rb") as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)