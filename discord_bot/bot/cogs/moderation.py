import discord
from discord.ext import commands

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"core_functionality Cog is ready:")
      
      
    
         
async def setup(bot):
    await bot.add_cog(moderation(bot))