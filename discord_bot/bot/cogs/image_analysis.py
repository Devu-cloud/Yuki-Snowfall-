import discord
from discord.ext import commands

class image_analysis(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"image_analysis Cog is ready:")
      
         
async def setup(bot):
    await bot.add_cog(image_analysis(bot))