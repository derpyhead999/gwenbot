# bot.py
import os

# imports
import discord
import random

from copypastaList import copypastas

from dotenv import load_dotenv

from discord.ext import commands

# Selenium; automating search tool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time

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
    channel = discord.utils.get(guild.text_channels, name="general")
    # await channel.send("Gwen is booted up!")

    print(
        f"{bot.user.name} is connected to the following guild:\n"
        f"{guild.name}  <->  (id: {guild.id})"
    )

    # members = "\n - ".join([member.name for member in guild.members])
    # print(f"Guild Members:\n - {members}")


@bot.event
async def on_member_join(member):
    guild = member.guild
    channel = discord.utils.get(guild.text_channels, name="general")
    await channel.send(f"Hontouni poggers, {member.name}! Welcome to {SERVER_NAME}!")


@bot.command(name="copypasta", help="Gives you a random copypasta")
async def generate_copypasta(ctx):
    response = random.choice(copypastas)
    await ctx.send(response)


@bot.command(name="uwufy", help="Uwufies most recent message before calling this")
async def uwufy_text(ctx):
    emoticons = [
        "(✿◠‿◠)",
        "(─‿‿─)",
        "(≧◡≦)",
        "≧◠◡◠≦✌",
        "✿◕ ‿ ◕✿",
        "≧'◡'≦",
        "(─‿‿─)♡",
        "(*^.^*)",
    ]

    channel = ctx.channel
    messages = [message async for message in channel.history(limit=5)]
    latest_message = messages[1].content.lower()
    length = len(latest_message)
    output_text = ""
    # check the cases for every individual character
    for i in range(length):
        # initialize the variables
        current_char = latest_message[i]
        previous_char = "&# 092;&# 048;"
        # assign the value of previous_char
        if i > 0:
            previous_char = latest_message[i - 1]

        if current_char == "L" or current_char == "R":
            output_text += "W"
        elif current_char == "l" or current_char == "r":
            output_text += "w"

        # if the current character is 'o' or 'O'
        # also check the previous character
        elif current_char == "O" or current_char == "o":
            if (
                previous_char == "N"
                or previous_char == "n"
                or previous_char == "M"
                or previous_char == "m"
            ):
                output_text += "yo"
            else:
                output_text += current_char
        # if no case match, write it as it is
        else:
            output_text += current_char

    output_text += f" {random.choice(emoticons)}"
    await ctx.send(output_text)


# @bot.command(name='everythingv3', help='Generates an image based on AI stable diffusion model "everythingv3"')
# async def stable_diff_generate(ctx):


# Searches up images with specific tags on safebooru
@bot.command(
    name="safebooru",
    help="Gets a random image from safebooru; Recommend using -booru tags, with commas between tags",
)
async def safebooru_search(ctx, *, tags=""):
    last_message = await ctx.send("Generating your image ⚪ ⚪ ⚪")

    options = webdriver.ChromeOptions()
    # options.binary_location = (
    #     "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    # )

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    options.add_argument("--disable-extensions")
    # options.binary_location = "./BraveSoftware/Brave-Browser/Application/brave.exe"
    options.add_argument("--headless")
    options.add_experimental_option("detach", True)
    options.add_argument("--incognito")

    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")
    # options.add_experimental_option("androidPackage", "com.android.chrome")
    driver = webdriver.Chrome(options=options)  # driver is the browser
    driver.get("https://safebooru.org/")

    if tags != "":
        # Formatting
        tags = tags.strip()
        tags = tags.replace(", ", ",")
        tags = tags.replace(" ", "_")
        tags = tags.replace(",", " ")

    await last_message.edit(content="Generating your image ⚫ ⚪ ⚪")

    # Now find the search bar, input and search according to fields
    try:
        elem = driver.find_element(By.NAME, "tags")
    except NoSuchElementException:
        await last_message.delete()
        await ctx.send("Can't find any images, the booru servers may be down (;﹏;)")

    elem.send_keys(tags + Keys.RETURN)
    elems = driver.find_elements(By.CLASS_NAME, "preview")
    if not elems:
        await last_message.delete()
        await ctx.send(
            "Sowwy, I can't find any tags for what you were looking for （>﹏<）; try use booru tags!"
        )

    await last_message.edit(content="Generating your image ⚫ ⚫ ⚪")

    random.choice(elems).click()
    # Now in the post
    img = driver.find_element(By.ID, "image")

    await last_message.edit(content="Generating your image ⚫ ⚫ ⚫")

    src = img.get_attribute("src")
    driver.quit()

    await ctx.send(src)
    await last_message.delete()


# Searches up images with specific tags on safebooru
@bot.command(
    name="danbooru",
    help="Gets a random image from danbooru; Recommend using -booru tags, with commas between tags; 2 tags max",
)
async def danbooru_search(ctx, *, tags=""):
    if not ctx.channel.nsfw:
        await ctx.send("Horny searches go in nsfw channel! ღゝ◡╹)ノ♡")
        return
    last_message = await ctx.send("Generating your image ⚪ ⚪ ⚪")

    options = webdriver.ChromeOptions()
    # options.binary_location = (
    #     "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
    # )

    options.add_argument("--window-size=1920,1080")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    options.add_argument("--disable-extensions")
    # options.binary_location = "./BraveSoftware/Brave-Browser/Application/brave.exe"
    options.add_argument("--headless")
    options.add_experimental_option("detach", True)
    options.add_argument("--incognito")

    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--allow-running-insecure-content")
    user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
    options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(options=options)  # driver is the browser
    driver.get("https://danbooru.donmai.us/")

    if tags != "":
        # Formatting
        tags = tags.strip()
        tags = tags.replace(", ", ",")
        tags = tags.replace(" ", "_")
        tags = tags.replace(",", " ")
        if len(tags.split()) > 2:
            await last_message.delete()
            await ctx.send(
                "Too many tags; only 2 max! (Make sure to put comments between tags) (Too poor 4 more) -`д´-"
            )

    await last_message.edit(content="Generating your image ⚫ ⚪ ⚪")

    # Now find the search bar, input and search according to fields
    try:
        elem = driver.find_element(By.NAME, "tags")
    except NoSuchElementException:
        await last_message.delete()
        await ctx.send("Can't find any images, the booru servers may be down (;﹏;)")

    # elem.send_keys(tags + Keys.RETURN)
    elem.send_keys(tags + Keys.RETURN)
    elems = driver.find_elements(By.CLASS_NAME, "post-preview-image")
    if not elems:
        await last_message.delete()
        await ctx.send(
            "Sowwy, I can't find any tags for what you were looking for （>﹏<）; try use booru tags!"
        )

    await last_message.edit(content="Generating your image ⚫ ⚫ ⚪")

    random.choice(elems).click()
    # Now in the post
    img = driver.find_element(By.ID, "image")

    await last_message.edit(content="Generating your image ⚫ ⚫ ⚫")

    src = img.get_attribute("src")
    driver.quit()

    await ctx.send(src)
    await last_message.delete()


# Recognises specific keyword from message and responds
@bot.event
async def on_message(message):
    league_call = ["leeg", "lego"]
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
    if "clash" in message.content.lower():
        await message.channel.send(
            "8:00pm Start? ✅\n2 Malders? ✅\n2 Griefers? ✅\n'Idc last game Ionia comp'? ✅\n⭕ ❌ ❌? ✅\nYep that's clash ✅"
        )
    if "valo" in message.content.lower():
        valorant_references = [
            "poggers",
            "least clutch nyoos momento",
            "I've seen APersonOnEarth play, he doesn't even use a monitor. He visualizes the map in a detailed rendering, completely in his mind. He has a biological wallhack; his godlike perception highlights all enemies within light-years. His eyes are closed as his mouse gracefully swerves across the table, making immaculate twitches as he flicks from head to head. The bullets that escape his gun barrel are surgical; each making a deadly strike in between his opponent's eyes.",
        ]
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
        await message.channel.send("pell \U0001F913")
    if "peter" in message.content.lower():
        await message.channel.send("技术问题")
    if "cook" in message.content.lower():
        await message.channel.send("Let him cook 🧑‍🍳")
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
    if "flush" in message.content.lower():
        with open("img/flush.png", "rb") as f:
            picture = discord.File(f)
            await message.channel.send(file=picture)
    await bot.process_commands(message)


@bot.command(name="quit")
@commands.is_owner()
async def quit(ctx):
    guild = discord.utils.get(bot.guilds, name=SERVER_NAME)
    channel = discord.utils.get(guild.text_channels, name="general")
    # await channel.send("Gwen needs a break; will be hopping back on soon!")
    await bot.close()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send("You do not have the correct role for this command.")


bot.run(TOKEN)
