import discord
from discord.ext import commands
import random
import asyncpraw
import json
import requests

with open('reddit/client_secrets.json') as f:
    creds = json.load(f)

reddit = asyncpraw.Reddit(client_id=creds['client_id'],
                          client_secret=creds['client_secret'],
                          user_agent=creds['user_agent'],
                          redirect_uri=creds['redirect_uri'],
                          refresh_token=creds['refresh_token'])


class RedditPostPuller(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="jptreddit",
        help="Gives a post from r/japanesepeopletwitter",
    )
    async def post_pull(self, ctx):
        name = "japanesepeopletwitter"
        subreddit = await reddit.subreddit(name)
        post_list = []
        async for submission in subreddit.hot(limit=20):
            post_list.append(submission)

        random_num = random.randint(1, 19)
        random_post = post_list[random_num]
        await ctx.send(f"https://www.reddit.com/r/{name}/comments/{random_post.id}")


async def setup(bot: commands.Cog):
    await bot.add_cog(RedditPostPuller(bot))
