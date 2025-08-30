import discord, httpx
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import json

load_dotenv(".env")

TOKEN = getenv("DISCORD_TOKEN")
prefix = "/"
base_url = "https://weao.xyz/api"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=prefix, intents=intents)
tree = bot.tree

#####

# intr -> interaction

#####

@tree.command(name="help")
async def help(intr: discord.Interaction):
    await intr.response.send_message(f"Hello !")


@tree.command(name="rbx-version") # <- fetch current version for windows & macOs
async def fetch_version(intr: discord.Interaction):
    data = httpx.get(f"{base_url}/versions/current").json()
    message = f"""
        *Windows: __{data['Windows']}__, Date: {data['WindowsDate']}*
        *MacOS: __{data['Mac']}__, Date: {data['MacDate']}*
    """
    embed = discord.Embed(color=discord.Color.dark_purple(), title="**Windows & MacOS Roblox Version**", description=message)
    await intr.response.send_message(embed=embed)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    
    await bot.tree.sync()
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))
    print(discord.__version__)

bot.run(TOKEN)