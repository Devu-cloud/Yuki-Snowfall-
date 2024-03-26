import discord
import random
from discord.ext import commands,tasks
from datetime import datetime ,  timezone
import re

class events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"events cog is ready:")
        

    @commands.Cog.listener()
    async def on_message(self,message):
        username = message.author.display_name
        try:
            if message.author == self.bot.user:
                return
            else:
                content_lower = message.content.lower()
                if content_lower in ("hello" , "hey" , "yo",  "yoo","hi"):
                    greetings = ["Hello", "Hi there", "What's up?"]
                    random_greeting = random.choice(greetings)
                    await message.channel.send(f"{random_greeting} {username}!")
                    await message.add_reaction("👋")
        
                pattern = r"\bgood\s*night\b"
                if re.search(pattern, message.content, re.IGNORECASE):
                    await message.add_reaction("❤️")
                    await message.add_reaction("👋")   
        except Exception as e:
            print(f"An error has occurred  {e}, cannot send dm to this user")
            
            
    #part1
    #when the bot joins a new guild
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # Welcome message
        try:
            welcome_message = f"Hello {guild.name}! I am {self.bot.user.name}. Thanks for inviting me!"
            channel = discord.utils.get(guild.text_channels, name="general")  # Try finding the general channel
            if channel:
                await channel.send(welcome_message)
            else:
                print(f"Couldn't find a general channel in {guild.name}. Welcome message not sent.")
                
            # Set default prefix for this guild (if needed)
            await self.bot.command_prefix.set_guild_prefix(self.default_prefix, guild=guild)
            print(f"Set default prefix to '{self.default_prefix}' for guild: {guild.name} (ID: {guild.id})")
        except Exception as e:
            print(f"An error occured , cannot find the channel")
            
    #part2
    #when the bot leaves a guild
    @commands.Cog.listener()
    async def on_guild_leave(self, guild):
        try:
            # Announce departure
            leave_message = f"Goodbye {guild.name}! I hope to see you again soon."
            channel = discord.utils.get(guild.text_channels, name="general") 
            if channel:
                await channel.send(leave_message)
            else:
                print(f"Couldn't find a general channel in {guild.name}. Leave message not sent.")

            # Log the event (optional)
            print(f"Left guild: {guild.name} (ID: {guild.id})")
        except  Exception as e:
            print(f"An error has occured , cannot send the message:")
            
                
async def setup(bot):
    await bot.add_cog(events(bot))