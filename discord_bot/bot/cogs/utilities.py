import discord
from discord.ext import commands

class utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"utilities Cog is ready:")
      
         
async def setup(bot):
    await bot.add_cog(utilities(bot))