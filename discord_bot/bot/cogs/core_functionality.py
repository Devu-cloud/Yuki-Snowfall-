import discord
from discord.ext import commands
from datetime import datetime

class core_functionality(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"core_functionality Cog is ready:")
      
      
    #ping command
    @commands.command()
    async def ping(self, ctx):
        """Sends a 'Pong!' message to test the bot's responsiveness."""
        bot_latency = round(self.bot.latency *1000)
        embed = discord.Embed(title=f"{self.bot.user.name}", 
                              color=0x00FFFF)
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        embed.add_field(name = "Ping!", value= f'Bot latency is {bot_latency} ms.' ,inline = False)
        embed.set_footer(text =f'Requested by {ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed = embed)
        

    #Displays information about the bot."""
    @commands.command()
    async def info(self, ctx):
        try:
            embed = discord.Embed(title=f"{self.bot.user.name}", color=0x00FFFF)
            embed.add_field(name="Developed By ❄️", value="Devendra", inline=False)
            embed.add_field(name="Server Count ❄️", value=len(self.bot.guilds), inline=True)
            embed.add_field(name="User Count ❄️", value=len(set(self.bot.get_all_members())), inline=True)
            embed.set_thumbnail(url = self.bot.user.avatar.url)
            embed.set_footer(text =f'Requested by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        
        except Exception as e:
            print(f"An error has occured {e}, @info_command.")
        
        
    #Displays information about the current server."""        
    @commands.command()
    async def serverinfo(self, ctx):
        try:

            server = ctx.guild
            server_created_at = server.created_at.strftime("%Y-%m-%d %H:%M:%S")
            server_joined_at = server.me.joined_at.strftime("%Y-%m-%d %H:%M:%S")
            total_members = server.member_count
            text_channels = len(server.text_channels)
            voice_channels = len(server.voice_channels)
            categories = len(server.categories)
            roles = len(server.roles)

            embed = discord.Embed(title=f"{server.name}", color=0x00FFFF)
            embed.set_thumbnail(url = self.bot.user.avatar.url)
            embed.add_field(name="Server ID 🆔", value=server.id, inline=True)
            embed.add_field(name="Created at 📍", value=server_created_at, inline=True)
            embed.add_field(name="Joined at 📍", value=server_joined_at, inline=True)
            embed.add_field(name="Members 👤", value=total_members, inline=True)
            embed.add_field(name="Text Channels 💬", value=text_channels, inline=True)
            embed.add_field(name="Voice Channels 🔊", value=voice_channels, inline=True)
            embed.add_field(name="Categories 📌", value=categories, inline=True)
            embed.add_field(name="Roles 📌", value=roles, inline=True)
            embed.set_footer(text =f'Requested by {ctx.author}', icon_url=ctx.author.avatar.url)

            await ctx.send(embed=embed)
        except Exception as e:
            print(f"An error has occured {e}, @serverinfo_command.")
        
        
    #Displays how long the bot has been running."""
    @commands.command()
    async def uptime(self, ctx):
        try:
            uptime = datetime.now() - self.start_time
            days = uptime.days
            hours, remainder = divmod(uptime.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            uptime_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
            
            embed = discord.Embed (title = f'{self.bot.user.name}',
                                color = 0x00FFFF
                                )
            embed.set_thumbnail(url = self.bot.user.avatar)
            embed.add_field(name = "Uptime!" , value= f"I've been running for {uptime_str}", inline = False)
            embed.set_footer(text =f'Requested by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.send(embed = embed)
            
        except Exception as e:
            print(f'An error has occured {e},@uptime_command')
            
       
    #Generates an invite link to the current server    
    @commands.command()
    async def invite(self, ctx):
        invite = await ctx.channel.create_invite(max_age=86400, max_uses=0)
        await ctx.send(f"Invite link: {invite}")

 
        #whois command
    @commands.command(name='whois', aliases=['userinfo'])
    async def whois(self, ctx, member: discord.Member = None):
        """Shows information about a member."""
        member = member or ctx.author
        embed = discord.Embed(title=f'User Information - {member}', color=0x00FFFF)
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Display Name', value=member.display_name, inline=True)
        embed.add_field(name='Joined Server', value=member.joined_at.strftime('%Y-%m-%d'), inline=True)
        embed.add_field(name='Joined Discord', value=member.created_at.strftime('%Y-%m-%d'), inline=True)
        embed.add_field(name='Roles', value=', '.join(r.mention for r in member.roles[1:]), inline=False)
        embed.set_footer(text =f'Requested by {ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
       
    #whois error handler: 
    @whois.error
    async def whois_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to acess this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")
 
 
    #avatar command
    @commands.command(name='avatar')
    async def avatar(self, ctx, member: discord.Member = None):
        """Shows a member's avatar."""
        member = member or ctx.author
        embed = discord.Embed(color=0x00FFFF)
        embed.set_thumbnail(url = self.bot.user.avatar.url)
        embed.set_image(url=member.avatar.url)
        embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        
    #avatar error handler: 
    @avatar.error
    async def avatar_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to acess this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(core_functionality(bot))