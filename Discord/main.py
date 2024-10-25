import discord
from discord.ext import commands
import random
import asyncio
from dotenv import load_dotenv
import os

load_dotenv("token.env")
token = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Verbunden mit {bot.user}")

@bot.event
async def on_message(message):
    Urls = [
        "https://imgur.com/gallery/animated-heavy-breathing-cat-NUyttbn",
        "https://imgur.com/gallery/i-havent-laughed-this-hard-while-grXqcNw",
        "https://imgur.com/gallery/when-i-see-cute-animal-post-pbao8mh"
    ]
    randomUrl = random.choice(Urls)

    if message.author == bot.user:
        return

    if message.content == "ping":
        await message.channel.send("pong")

    print(f"{message.author} [{message.channel}]: {message.content}")

    if message.content.startswith("!guess"):
        answer = random.randint(1, 10)

        message.content = message.content.split()

        try:
            cmd = message.content[0]
            arg = message.content[1]
            arg = int(arg)
        except IndexError:
            await message.channel.send("!guess **[number]** *1-10*")
        except ValueError:
            await message.channel.send("**Only numbers!**")

        try:
            if arg == answer:
                await message.channel.send("You are right!")
            elif arg != answer and arg <= 10:
                await message.channel.send(f"You are wrong :/ The **answer** was: ||{answer}||")
            if arg > 10:
                await message.channel.send("You have to **guess** a number between 1 and 10!")
        except UnboundLocalError:
            print("!guess [number]")
        except TypeError:
            print("Typed str instead of integer")

    if message.content == "!help":
        embed = discord.Embed(
            title="Help",
            description="Available commands",
            color=0x0099ff
        )

        embed.set_author(name="Bob", icon_url="https://i.imgur.com/tTYbjIY.jpeg")
        embed.set_thumbnail(url="https://i.imgur.com/tTYbjIY.jpeg")
        embed.add_field(name="Commands 😎", value="!guess\n!help\nping\n!cat\n", inline=False)
        embed.set_footer(text="Bob is here to save the day.")

        await message.channel.send(embed=embed)

    if message.content == "test":
        await message.channel.send("**Hallo!** Das ist eine *schöne* Nachricht mit einem Spoiler: ||das ist verborgen||")

    if message.content == "!cat":
        await message.channel.send("Found a *funny* cat!")
        embed = discord.Embed(
            title="😺 Meow",
            url=randomUrl,
            color=0x0099ff
        )

        await message.channel.send(embed=embed)

@bot.event
async def on_member_join(member):
    role_id = 1295690377872937030  # Rolle-ID hier anpassen
    role = discord.utils.get(member.guild.roles, id=role_id)

    if role:
        await member.add_roles(role)
        print(f"Rolle {role.name} wurde {member.name} gegeben.")

    await member.create_dm()
    await member.dm_channel.send(f"Hello {member.name}, welcome to my Discord Server! If you need help type !help in the discord.")

@bot.event
async def on_guild_channel_create(channel):
    print("Ein neuer Kanal wurde erstellt: ", channel.name)

@bot.event
async def on_guild_channel_delete(channel):
    print("Ein Kanal wurde gelöscht: ", channel.name)

# Bot starten
bot.run(token)
