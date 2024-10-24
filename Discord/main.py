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

# Bot-Instanz erstellen
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Verbunden mit {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "ping":
        await message.channel.send("pong")

    print(f"{message.author} [{message.channel}]: {message.content}")

    if message.content.startswith("!guess"):
        #await message.channel.send("Guess a number between 1 and 10.\n You have only one chance!")
        
        answer = random.randint(1,10)

        message.content = message.content.split()
        
        try:
            cmd = message.content[0]
            arg = message.content[1]
            arg = int(arg)
        except IndexError:
            await message.channel.send("Hilfe: !guess [number] | 1-10")
        except ValueError:
            await message.channel.send("Only numbers!")
        
        try:
            if arg == answer:
                await message.channel.send("You are right!")
            elif arg != answer and arg <= 10:
                await message.channel.send(f"You are wrong :/ The answer was: {answer}")
            if arg > 10:
                await message.channel.send("You have to guess a number between 1 and 10!")
        except UnboundLocalError:
            print("!guess [number]")
                      
    if message.content == "!help":
        await message.channel.send("No help right now. :/")


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
    print("Ein neuer Kanal wurde erstellt: ",channel.name)

@bot.event 
async def on_guild_channel_delete(channel):
    print("Ein Kanal wurde gelöscht: ",channel.name)


# Bot starten
bot.run(token)


