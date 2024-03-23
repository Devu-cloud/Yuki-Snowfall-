import os
from discord.ext import commands
import discord

class Bot(commands.Bot):
    def __init__(self, token, prefix, intents):
        super().__init__(command_prefix=prefix, intents=intents)
        self.token = token

    async def start(self, *args, **kwargs):
        await super().start(self.token, *args, **kwargs)
    

    async def load_cogs(self):
        cogs_dir = "bot/cogs"
        for filename in os.listdir(cogs_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                cog_name = filename[:-3]  # Remove the ".py" extension
                try:
                    await self.load_extension(f"bot.cogs.{cog_name}")
                    print(f"Loaded {cog_name} cog")
                except Exception as e:
                    print(f"Failed to load {cog_name} cog: {e}")


    async def on_ready(self):
        try:
            print("_______________________\n")
            print(f"{self.user.name} at your Service!!")
            print(f"Bot_ID ={self.user.id}")
            print("_______________________\n")
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Happy Now"))
            
        except Exception as e:
            print(f"An error occurred {e}")