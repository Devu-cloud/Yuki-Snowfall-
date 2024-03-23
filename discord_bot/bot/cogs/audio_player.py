import discord
from discord.ext import commands

class audio_player(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"audio_player Cog is ready:")
      
         
async def setup(bot):
    await bot.add_cog(audio_player(bot))