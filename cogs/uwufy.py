import discord
from discord.ext import commands
import random


class UwufyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Uwufies the previous text
    @commands.command(name="uwufy", help="Uwufies most recent message before this call")
    async def uwufy_text(self, ctx):
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


async def setup(bot: commands.Cog):
    await bot.add_cog(UwufyCog(bot))
