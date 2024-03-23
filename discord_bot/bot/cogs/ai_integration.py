import discord
from discord.ext import commands

class ai_integration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"ai_integration Cog is ready:")
      
         
async def setup(bot):
    await bot.add_cog(ai_integration(bot))