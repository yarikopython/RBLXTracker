import discord, httpx
from discord.ext import commands
from discord import app_commands
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

def format_message(data: dict):
    return (
        f"*Windows: __{data.get('Windows', 'N/A')}__, Date: {data.get('WindowsDate', 'N/A')}*\n"
        f"*MacOS: __{data.get('Mac', 'N/A')}__, Date: {data.get('MacDate', 'N/A')}*"
    )

@tree.command(name="help")
async def help(intr: discord.Interaction):
    await intr.response.send_message(f"Hello !")


@tree.command(name="rbx-version") # <- fetch current version for windows & macOs
@app_commands.choices(type=[
    app_commands.Choice(name="current", value="current"),
    app_commands.Choice(name="past", value="past"),
    app_commands.Choice(name="future", value="future")
])
async def fetch_version(intr: discord.Interaction, type : app_commands.Choice[str]):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{base_url}/versions/{type.value}")
        data = res.json()
        
    message = format_message(data=data)
    
    embed = discord.Embed(color=discord.Color.dark_purple(), title="**Windows & MacOS Roblox Version**", description=message)
    await intr.response.send_message(embed=embed)

@tree.command(name="exploits")
async def fetch_exps(intr: discord.Interaction):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{base_url}/status/exploits")
        data = res.json()
    
    
    await intr.response.send_message()

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    
    await bot.tree.sync()
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))
    print(discord.__version__)

bot.run(TOKEN)