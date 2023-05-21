import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from bot import RIOT_API_KEY

# RIOT imports
from urllib.request import urlopen
import json
from riotwatcher import LolWatcher, ApiError

# load_dotenv()
# RIOT_API_KEY = os.getenv("RIOT_API_KEY")


class UserCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Returns a list of information about a user
    @commands.command(
        name="info",
        help="!info [user] [option] :Returns a list of information based on specific user input",
    )
    async def user_info(
        self,
        ctx,
        user: str = commands.parameter(default="", description="A summoner name"),
        option: str = commands.parameter(default="", description="Rank / Mastery"),
    ):
        if user == "":
            await ctx.send(
                "Please provide a summoner name! Please format like so: !info [user] [rank/mastery]"
            )
            return
        elif option == "":
            await ctx.send(
                "Please ask for rank / mastery! Please format like so: !info [user] [rank/mastery]"
            )
            return
        lol_watcher = LolWatcher(RIOT_API_KEY)
        region = "oc1"

        try:
            user_found: dict = lol_watcher.summoner.by_name(region, user)
        except ApiError as err:
            if err.response.status_code == 404:
                await ctx.send(
                    "Sorry, I can't find that summoner! Please format like so: !info [user] [rank/mastery]"
                )
            return

        if "rank" in option.lower():
            ranked_stats: list = lol_watcher.league.by_summoner(
                region, user_found["id"]
            )
            await ctx.send(f"League of legends ranked stats for {user} : ღゝ◡╹ )ノ♡\n")
            for item in ranked_stats:
                await ctx.send(
                    f"Your rank for {item['queueType']} is {item['tier']} {item['rank']} {item['leaguePoints']} LP\n\t-Wins: {item['wins']}\n\t-Losses: {item['losses']}\n"
                )
            await ctx.send("You're doing great! 👍")
        elif "mastery" == option.lower():
            mastery_stats: list = lol_watcher.champion_mastery.by_summoner(
                region, user_found["id"]
            )
            response = urlopen(
                "https://ddragon.leagueoflegends.com/cdn/13.9.1/data/en_US/champion.json"
            )
            data_json = json.load(response)
            champ_data: dict = data_json["data"]
            await ctx.send(
                f"League of legends mastery stats for {user}:\nHere are your top 5 mastery champions! ღゝ◡╹ )ノ♡\n"
            )
            count = 0
            for item in mastery_stats[:5]:
                champ_arr = [
                    str(key)
                    for key, props in champ_data.items()
                    if int(props["key"]) == item["championId"]
                ]
                mastery_points = item["championPoints"]
                await ctx.send(
                    f"{champ_arr[0]}:\n\t-Champion Level: {item['championLevel']}\n\t-Mastery Points: {mastery_points}\n"
                )
                count += mastery_points

            if count > 1000000:
                await ctx.send(
                    "*"
                    + "Wow...so your favourite hobbies are 'smurfing on noobs' and 'climbing out of pisslow'..."
                    + "*"
                )
            elif count > 500000:
                await ctx.send("'You know, I'm something of a league addict myself.'")
            elif count > 100000:
                await ctx.send("*" + "It's an on and off relationship eh?" + "*")
            elif count > 0:
                await ctx.send("Congrats! You're a functional human being! 🎂")


async def setup(bot: commands.Cog):
    await bot.add_cog(UserCog(bot))
