import discord
from discord.ext import commands
import random
from bot import DANBOORU_API_KEY
from pybooru import Danbooru, Moebooru
from bot import KONACHAN_PASSWORD
import requests
import xml.etree.ElementTree as ET

# Selenium; automating search tool
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

SAFEBOORU_API_ROUTE = "https://safebooru.org/index.php?page=dapi&s=post&q=index"


class SearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="search",
        help="Searches for posts on danbooru with !search [danbooru/safebooru/konachan/yandere/safebooru2] [Up to 2 fields separated by commas]\nNote that with konachan/yandere, tags are ignored",
    )
    async def search(self, ctx, *, tags=""):
        last_message = await ctx.send("Generating your image; just wait a min~~")
        tags = tags.split(" ", 1)
        option = tags[0]
        if len(tags) == 1:
            fields = ""
        else:
            fields = tags[1]

        if fields != "":
            # Formatting
            fields = fields.strip()
            fields = fields.replace(", ", ",")
            fields = fields.replace(" ", "_")
            fields = fields.replace(",", " ")
            if len(fields.split()) > 2 and option != "safebooru2":
                await last_message.delete()
                await ctx.send(
                    "Too many tags (max 2); Make sure to put comma's between tags -`д´-"
                )
                return
        if option == "safebooru2":
            res = requests.get(
                SAFEBOORU_API_ROUTE + "&limit=100&tags=" + fields.replace(" ", "%20")
            )
            # Parse XML document
            posts = ET.fromstring(res.text)
            if len(posts) == 0:
                await ctx.send(
                    "No posts found! Makes sure there are only 2 tags max + the format as specified in !help"
                )
                return
            post = random.choice(posts)
            # Select attribute with "file_url" and post image
            await ctx.send(post.attrib["file_url"])
            return

        if not ctx.channel.nsfw and option != "safebooru":
            await ctx.send("Horny searches go in nsfw channel! ღゝ◡╹)ノ♡")
            return
        if option == "danbooru" or option == "safebooru":
            client = Danbooru(option, username="derpyhead999", api_key=DANBOORU_API_KEY)
            posts = client.post_list(tags=fields, limit=100)
        elif option == "konachan" or option == "yandere":
            client = Moebooru(
                option, username="derpyhead999", password=KONACHAN_PASSWORD
            )
            posts = client.post_list(limit=100)
        else:
            await ctx.send(
                "Please specify an option !search [danbooru/safebooru/lolibooru/konachan/yandere] [Up to 0-2 fields separated by comma's]\nNote that with lolibooru/konachan/yandere, tags are ignored"
            )
            return
        if len(posts) == 0:
            await ctx.send(
                "No posts found! Makes sure there are only 2 tags max + the format as specified in !help"
            )
            return
        await ctx.send(random.choice(posts)["file_url"])

    # Searches up images with specific tags on safebooru
    @commands.command(
        name="danbooru",
        help="Gets a random image from danbooru; Recommend using -booru tags, with commas between tags; 2 tags max",
    )
    async def danbooru_search(self, ctx, *, tags=""):
        if not ctx.channel.nsfw:
            await ctx.send("Horny searches go in nsfw channel! ღゝ◡╹)ノ♡")
            return
        last_message = await ctx.send("Generating your image; just wait a min~~")

        options = webdriver.ChromeOptions()

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        options.add_argument("--disable-extensions")
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
                    "Too many tags; only 2 max! (Make sure to put comma's between tags) (Too poor 4 more) -`д´-"
                )
        else:
            # If no tags are provided
            tags += " highres"

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

        random.choice(elems).click()
        # Now in the post
        img = driver.find_element(By.ID, "image")

        src = img.get_attribute("src")
        driver.quit()

        await ctx.send(src)
        await last_message.delete()

    # Searches up images with specific tags on safebooru
    @commands.command(
        name="safebooru",
        help="Gets a random image from safebooru; Recommend using -booru tags, with commas between tags",
    )
    async def safebooru_search(self, ctx, *, tags=""):
        last_message = await ctx.send("Generating your image; just wait a min~~")

        options = webdriver.ChromeOptions()

        options.add_argument("--window-size=1920,1080")
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")

        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_experimental_option("detach", True)
        options.add_argument("--incognito")

        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")
        driver = webdriver.Chrome(options=options)  # driver is the browser
        driver.get("https://safebooru.org/")

        if tags != "":
            # Formatting
            tags = tags.strip()
            tags = tags.replace(", ", ",")
            tags = tags.replace(" ", "_")
            tags = tags.replace(",", " ")
            tags += " score:>=6"

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

        random.choice(elems).click()
        # Now in the post
        img = driver.find_element(By.ID, "image")

        src = img.get_attribute("src")
        driver.quit()

        await ctx.send(src)
        await last_message.delete()


async def setup(bot: commands.Cog):
    await bot.add_cog(SearchCog(bot))
