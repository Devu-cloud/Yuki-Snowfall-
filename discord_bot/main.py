import discord
import os 
import asyncio
from discord.ext import commands,tasks

from bot import Bot
from config import config

# Access configuration values
BOT_TOKEN = config.DISCORD_BOT_TOKEN
BOT_PREFIX = config.DISCORD_BOT_PREFIX

# Set up intents
intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.presences = True

# Create the bot instance
bot = Bot(BOT_TOKEN, BOT_PREFIX, intents=intents)

async def main():
    # Load cogs
    await bot.load_cogs()
    # Start the bot
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())