import discord
from discord.ext import commands
import random

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
sadge_call = ["saj", "sadge", "rip"]
huh_call = [
    "cum",
    "balls",
    "huh",
    "dick",
    "piss",
    "bust",
    "moan",
    "groan",
]
sett_call = ["flash", "sett", "ult", "cookie"]

league_references = [
    "xdd",
    "chovy cs tho!!!",
    "standard peter @ daily momento",
    "tilt vibes eta 5min in vc \U0001F614",
    "[insert genius pell witty remark on league players]",
    "classico 6 man",
    "11:58pm",
]
people = [
    "APersonOnEarth",
    "Genus",
    "Imperial",
    "Nyos",
    "Burnhobo",
    "Derpyhead999",
    "GuessWho",
    "Happyicy",
    "Kaowayne",
    "Catshark",
]
pepege_call = ["pepega", "pepege", "dumb", "idiot"]


class MessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Recognises specific keyword from message and responds
    @commands.Cog.listener()
    async def on_message(self, message: discord.message):
        if message.author == self.bot.user:
            return
        if "stupid" in message.content.lower():
            await message.channel.send("stoopid")
        if "clash" in message.content.lower():
            await message.channel.send(
                "8:00pm Start? ✅\n2 Malders? ✅\n2 Griefers? ✅\n'Idc last game Ionia comp'? ✅\n⭕ ❌ ❌? ✅\nYep that's clash ✅"
            )
        if "valo" in message.content.lower():
            person = random.choice(people)
            valorant_references = [
                "poggers",
                "least clutch nyoos momento",
                f"I've seen {person} play, he doesn't even use a monitor. He visualizes the map in a detailed rendering, completely in his mind. He has a biological wallhack; his godlike perception highlights all enemies within light-years. His eyes are closed as his mouse gracefully swerves across the table, making immaculate twitches as he flicks from head to head. The bullets that escape his gun barrel are surgical; each making a deadly strike in between his opponent's eyes.",
                f"{person} is a tactical genius. He is best known for his signature tactic 'going B, but then going A'. He also has a second little known tactic of 'going A, but going A'. What an absolute legend. Top 3 IGL for sure.",
                f"If {person} has million number of fans i am one of them . if {person} has ten fans i am one of them. if {person} have only one fan and that is me . if {person} has no fans, that means i am no more on the earth. if world against the {person} , i am against the world.",
                f"{person} is fantastic, just need to work on comms, aim, map awareness, crosshair placement, economy management, pistol aim, awp flicks, 1v1 maps, grenade and smoke spots, pop flashes, positioning, bomb plant positions, retake ability, bunny hopping, spray control and getting kills.",
                f"if {person}👽and my girl👧😍 both drowning 😱 👋 and I can only save one😤😬Catch me at the Ascent B site🚪🔴 with my boy on phoenix 🌈🕰",
                f"{person} skilled player but that is not normally, This very very insane....They need to check him pc and game.....Maybe he not cheating but maybe he using the game deficit ...and this cant seem on game screen..He needs to check-up....",
                "valarante child game.... look to cartoon grapfix to make kid player happy like children show.. valarante cartoon world with rainbow unlike counter strike chad with dark corridorr and raelistic gun.. valarante like playhouse. valarant playor run from csgo fear of dark world and realism",
            ]
            await message.channel.send(random.choice(valorant_references))
        if any([x in message.content.lower() for x in league_call]):
            await message.channel.send(random.choice(league_references))
        if "genus" in message.content.lower():
            await message.channel.send("pell \U0001F913")
        if "based" in message.content.lower():
            await message.channel.send(
                "Based? Based on what? In your dick? Please shut the fuck up and use words properly you fuckin troglodyte, do you think God gave us a freedom of speech just to spew random words that have no meaning that doesn't even correllate to the topic of the conversation? Like please you always complain about why no one talks to you or no one expresses their opinions on you because you're always spewing random shit like poggers based cringe and when you try to explain what it is and you just say that it's funny like what? What the fuck is funny about that do you think you'll just become a stand-up comedian that will get a standing ovation just because you said 'cum' in the stage? HELL NO YOU FUCKIN IDIOT, so please shut the fuck up and use words properly you dumb bitch"
            )
        if "peter" in message.content.lower():
            await message.channel.send("技术问题")
        if "lethimcook" in message.content.lower().replace(" ", ""):
            with open("img/lethimcook.jpg", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if message.content.lower() == "riot":
            with open("img/RIOT.gif", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if "kekwait" in message.content.lower():
            with open("img/kekwait.png", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
            return
        if "kekw" in message.content.lower():
            with open("img/kekw.png", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if any([x in message.content.lower() for x in pepege_call]):
            with open("img/pepege.png", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if any([x in message.content.lower() for x in jg_call]):
            with open("img/myjg.png", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
                await message.channel.send(
                    "my jg watching 3 losing lanes getting blamed lvl 3"
                )
        if "xdd" in message.content.lower():
            with open("img/xdd.jpg", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if "monka" in message.content.lower():
            with open("img/monka.png", "rb") as f:
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
        if "madge" in message.content.lower():
            with open("img/madge.png", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if "susge" in message.content.lower():
            with open("img/susge.png", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if "nerdge" in message.content.lower():
            with open("img/nerdge.gif", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if any([x in message.content.lower() for x in sadge_call]):
            with open("img/sadge.png", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if message.content.lower() == "noted":
            await message.delete()
            with open("img/noted.gif", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if any([x in message.content.lower() for x in huh_call]):
            with open("img/huh.gif", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
        if any([x in message.content.lower() for x in sett_call]):
            with open("img/sett.gif", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)
                await message.channel.send("?")
        if message.content.lower() == "5head":
            await message.delete()
            with open("img/5head.png", "rb") as f:
                picture = discord.File(f)
                await message.channel.send(file=picture)


async def setup(bot: commands.Cog):
    await bot.add_cog(MessageCog(bot))
