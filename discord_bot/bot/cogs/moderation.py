import discord
from discord.ext import commands

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"moderation Cog is ready:")
      
    #command to remove a user from the server
    @commands.command(aliases= ["yuki_kick"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        try:
            guildname=member.guild.name
            dmchannel = await member.create_dm()
            embed = discord.Embed(
                title =f"Sayonara:",
                description=f" {member.mention}, You have been kicked from the serever: {guildname} :)",
                color =0xFF0000
            )
            await dmchannel.send(embed = embed)
        except Exception as e:
            print(f"An error has occured {e} in @kick command, cannot send dm to the user")
        
        try:
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f"{member} has been kicked!")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to kick {member}. Error: {e}")
    
    # Kick error handler
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to kick members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")
            
    
    #command to ban a user from the server
    @commands.command(aliases= ["yuki_ban"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        try:
            guildname=member.guild.name
            dmchannel = await member.create_dm()
            embed = discord.Embed(
                title =f"Sayonara:",
                description=f" {member.mention}, You have been Banned from the serever: {guildname} :)",
                color =0xFF0000
            )
            await dmchannel.send(embed = embed)
        except Exception as e:
            print(f"An error has occured {e} in @ban command, cannot send dm to the user")
        
        try:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f"{member} has been Banned!")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to Bann {member}. Error: {e}")
    
    #handling ban errors
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to ban members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")
    
    
    
    #command to unban a user from the server:
    @commands.command(aliases=["yuki_unban"])
    @commands.guild_only()
    @commands.has_permissions(ban_members =True)
    async def unban(self,ctx,userID):
        try:
            user =discord.Object(id= userID)
            await ctx.guild.unban(user)
            embed =discord.Embed(title ="Sucess", color = 0xFF0000)
            embed.add_field(name="Unbanned", value =f"<@{userID}> has been unbanned from the server  by {ctx.author.mention}.",inline =False)
            await ctx.send(embed= embed)
            
        except Exception as e:
            print(f"An error occurred {e} @unban_command, the user cannot be unbanned.")
    
    # Unban error handler
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to unban members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid user ID or mention.")
        else:
            await ctx.send(f"An error occurred: {error}")
        
    
    #purge command to delete last 100 msges:
    @commands.command(aliases= ["yuki_purge"])
    @commands.has_permissions(manage_messages=True)  # Requires "Manage Messages" permission
    async def purge(self, ctx, amount:int):
        if amount <1 or amount > 100:
            await ctx.send("You can only delete up to 100 messages at a time.")
            return
        
        try:
            deleted = await ctx.channel.purge(limit=amount)
            embed = discord.Embed(
                title = "Purge_initiated",
                color=0x00FFFF
            )
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.add_field(name="Purged", value=f"Deleted {len(deleted)} messages.", inline=False)
            embed.set_footer(text =f'Command Initiated by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.send(embed= embed)
        except discord.HTTPException as e:
            await ctx.send(f"Failed to delete messages: {e}")
    
    # Purge error handler
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to delete messages.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid amount of messages to delete.")
        else:
            await ctx.send(f"An error occurred: {error}")
            
    
    #command to mute a user:
    @commands.command(aliases= ["yuki_mute"])
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        """Mutes a user from the server."""
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")

        if not muted_role:
            muted_role = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(muted_role, send_messages=False)

        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"{member.mention} has been muted.")

    
    #mute error handler
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to mute members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")

    #unmute command:
    @commands.command(aliases= ["yuki_unmute"])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f"{member.mention} has been unmuted.")
        else:
            await ctx.send(f"{member.mention} is not muted.")
            
    #unmute error handler
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to unmute members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")
            
    # Deafen command 
    @commands.command(aliases= ["yuki_deafen"])
    @commands.has_permissions(manage_roles=True)
    async def deafen(self, ctx, member: discord.Member, *, reason=None):
        """Deafens a user from the server."""
        voice_state = member.voice
        guild = ctx.guild
        deafened_role = discord.utils.get(guild.roles, name="Deafened")

        if not deafened_role:
            deafened_role = await guild.create_role(name="Deafened")
            for channel in guild.voice_channels:
                await channel.set_permissions(deafened_role, connect=True, speak=False)
        await member.add_roles(deafened_role, reason=reason)
        await ctx.send(f"{member.mention} has been deafened.")

    #deafen error handler:
    @deafen.error
    async def deafen_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to deafen members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")

    # Undeafen command 
    @commands.command(aliases=["yuki_undeafen"])
    @commands.has_permissions(manage_roles=True)
    async def undeafen(self, ctx, member: discord.Member):
        """Undeafens a user from the server."""
        guild = ctx.guild
        deafened_role = discord.utils.get(guild.roles, name="Deafened")

        if deafened_role in member.roles:
            await member.remove_roles(deafened_role)
            await ctx.send(f"{member.mention} has been undeafened.")
        else:
            voice_state = member.voice
            if voice_state and voice_state.channel:
                # Member is connected to a voice channel
                await member.edit(deafen=False)
                await ctx.send(f"{member.mention} has been undeafened.")
            else:
                await ctx.send(f"{member.mention} is not deafened or not in a voice channel.")

    #undeafen error handler:
    @undeafen.error
    async def undeafen_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to undeafen members.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")
        
    #"""Kicks a user from the voice channel."""    
    @commands.command(aliases= ["yuki_voicekick"])
    @commands.has_permissions(kick_members=True)
    async def voicekick(self, ctx, member: discord.Member, *, reason=None):
        
        voice_state = member.voice
        if voice_state is None:
            return await ctx.send(f"{member.mention} is not in a voice channel.")

        await member.edit(voice_channel=None, reason=reason)
        await ctx.send(f"{member.mention} has been kicked from the voice channel.")

    #voicekick error handler
    @voicekick.error
    async def voicekick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to kick members from voice channels.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")

    # VoiceBan command and error handler
    #"""Bans a user from joining any voice channel."""
    @commands.command(aliases= ["yuki_voiceban"])
    @commands.has_permissions(ban_members=True)
    async def voiceban(self, ctx, member: discord.Member, *, reason=None):
        voice_state = member.voice
        if voice_state is not None:
            await member.edit(voice_channel=None, reason=reason)

        guild = ctx.guild
        voice_channels = [channel for channel in guild.channels if isinstance(channel, discord.VoiceChannel)]

        for channel in voice_channels:
            await channel.set_permissions(member, connect=False)

        await ctx.send(f"{member.mention} has been banned from joining voice channels.")

    @voiceban.error
    async def voiceban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to ban members from voice channels.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")


    #voice_unban command:
    @commands.command(aliases=["yuki_voice_unban"])
    @commands.has_permissions(manage_channels=True)  # Requires "Manage Channels" permission
    async def voice_unban(self, ctx, member: discord.Member, *, reason = None):
        # Grant "Connect" permission to all voice channels the bot has "Manage Channels" permission for
        guild = ctx.guild
        for channel in guild.channels:
            if isinstance(channel, discord.VoiceChannel) and channel.permissions_for(ctx.me).manage_channels:
                # Bot has "Manage Channels" permission for this channel
                await channel.set_permissions(member, connect=True)

        await ctx.send(f"{member.mention} has been unbanned from voice channels.")
    
    #voice_bunban error handler
    @voiceban.error
    async def voiceban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to un_ban members from voice channels.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid member mentioned.")
        else:
            await ctx.send(f"An error occurred: {error}")
    
    # Slowmode command
    #"""Sets the slowmode duration for the current channel."""
    @commands.command(aliases= ["yuki_slowmode"])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        
        if seconds > 21600:
            await ctx.send("The maximum slowmode duration is 6 hours (21600 seconds).")
            return
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"Slowmode set to {seconds} seconds.")

    #slowmode error handler
    @slowmode.error
    async def slowmode_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to set slowmode.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid duration provided.")
        else:
            await ctx.send(f"An error occurred: {error}")
            
    #give_roll command
    @commands.command(aliases =["yuki_giverole"])
    @commands.has_permissions(manage_roles=True)
    async def giverole(self, ctx, member: discord.Member, *, role: discord.Role):
        """Gives a role to a member."""
        if role in member.roles:
            await ctx.send(f"{member.mention} already has the {role.name} role.")
        else:
            try:
                await member.add_roles(role)
                await ctx.send(f"Gave {role.name} role to {member.mention}.")
            except discord.HTTPException as e:
                await ctx.send(f"Failed to give {role.name} role to {member.mention}.\n{e}")
                
    #give_roll error handler
    @giverole.error
    async def giverole_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid role or member specified.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to manage roles.")
        else:
            await ctx.send(f"An error occurred: {error}")

    #revoke_roll command
    @commands.command(aliases = ["yuki_revokerole"])
    @commands.has_permissions(manage_roles=True)
    async def revokerole(self, ctx, member: discord.Member, *, role: discord.Role):
        """Revokes a role from a member."""
        if role not in member.roles:
            await ctx.send(f"{member.mention} doesn't have the {role.name} role.")
        else:
            try:
                await member.remove_roles(role)
                await ctx.send(f"Revoked {role.name} role from {member.mention}.")
            except discord.HTTPException as e:
                await ctx.send(f"Failed to revoke {role.name} role from {member.mention}.\n{e}")

    #revoke roll error handler
    @revokerole.error
    async def revokerole_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid role or member specified.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to manage roles.")
        else:
            await ctx.send(f"An error occurred: {error}")
    
         
async def setup(bot):
    await bot.add_cog(moderation(bot))