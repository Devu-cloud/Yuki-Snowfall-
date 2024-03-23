import discord
from discord.ext import commands

class web_scrapper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"web_scrapper Cog is ready:")
      
      
    
         
async def setup(bot):
    await bot.add_cog(web_scrapper(bot))