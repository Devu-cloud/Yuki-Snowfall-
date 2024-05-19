import discord
from discord.ext import commands
import asyncio
from datetime import datetime,timedelta

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = None
        self.welcome_channel = None
        self.last_welcome_message = None
        self.last_dm_message = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name} Utilities Cog is ready.")

    @commands.group(name="setup", invoke_without_command=True)
    async def setup(self, ctx):
        await ctx.send("Use `!setup enable_logging` or `!setup enable_welcome` to configure logging or welcome messages.")

    @setup.command(name="enable_logging")  
    @commands.has_guild_permissions(administrator=True)
    async def setup_log(self, ctx):
        guild = ctx.guild
        self.log_channel = discord.utils.get(guild.text_channels, name="server-logs")
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You don't have administrator permissions to use this command.")
            return
        
        if self.log_channel is not None:
            #chanel already exists , bind listners
            self.start_log_listeners()
            embed = discord.Embed(title=f"{self.bot.user.name} Logging", color=0x00FFFF)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.add_field(name="Server Logs", value=f"Using existing channel 'server-logs' for event logging.", inline=False)
            embed.set_footer(text=f'Initiated by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            await ctx.send("`server_logs` channel already exists. Use `!setup disable_logging` to disable it, or delete the channel manually.")
            return
        
        permissions = discord.Permissions()
        permissions.read_messages = False  # No read access for @everyone

        try:
            overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False)  # Deny read access for @everyone
            }
            self.log_channel = await guild.create_text_channel(name="server-logs", overwrites=overwrites)

            for role in guild.roles:
                if role.permissions.manage_messages:
                    await self.log_channel.set_permissions(role, read_messages=True)

            self.start_log_listeners()
            embed = discord.Embed(title=f"{self.bot.user.name}", color=0x00FFFF)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.add_field(name="Setup Complete", value=f"Log channel 'server-logs' created and events bound successfully.", inline=False)
            embed.set_footer(text=f'Initiated by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            print(f"Error creating log channel: {e}")
            await ctx.send(f"Failed to create log channel. Check bot permissions.")

    @setup.command(name="disable_logging", aliases=["dis_logs"])
    @commands.has_guild_permissions(administrator=True)
    async def disable_logs(self, ctx):
        if self.log_channel is None:
            await ctx.send("Log channel is not set up. Use `!setup enable_logging` to enable it.")
            return

        for role in ctx.guild.roles:
            await self.log_channel.set_permissions(role, read_messages=False)

        self.stop_log_listeners()
        self.log_channel = None
        await ctx.send("Log channel disabled and event listeners stopped.")

    @setup.command(name="enable_welcome")
    @commands.has_guild_permissions(administrator=True)
    async def setup_welcome(self, ctx):
        guild = ctx.guild
        self.welcome_channel = discord.utils.get(guild.text_channels, name="greetings_goodbyes")
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You don't have administrator permissions to use this command.")
            return
           
        if self.welcome_channel is not None:
            #chanel already exists , bind listners
            self.start_welcome_listeners()
            embed = discord.Embed(title=f"{self.bot.user.name} Logging", color=0x00FFFF)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.add_field(name="greetings_goodbyes", value=f"Using existing channel 'greetings_goodbyes' for event logging.", inline=False)
            embed.set_footer(text=f'Initiated by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            await ctx.send("`greetins_goodbyes` channel already exists. Use `!setup disable_welcome` to disable it,or delete the channel manually.")
            return

        
        permissions = discord.Permissions()
        permissions.read_messages = True
        permissions.send_messages = False# No send access for @everyone

        try:
            overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=True,send_messages=False) 
            }
            self.welcome_channel = await guild.create_text_channel(name="Greetings_Goodbyes", overwrites=overwrites)

            for role in guild.roles:
                if role.permissions.manage_messages:
                    await self.welcome_channel.set_permissions(role, read_messages=True)

            self.start_welcome_listeners()
            embed = discord.Embed(title=f"{self.bot.user.name}", color=0x00FFFF)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.add_field(name="Setup Complete", value=f"Text channel 'Greetings_Goodbyes' created and events bound successfully.", inline=False)
            embed.set_footer(text=f'Initiated by {ctx.author}', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            
        except discord.HTTPException as e:
            print(f"Error creating log channel: {e}")
            await ctx.send(f"Failed to create log channel. Check bot permissions.")
            

    @setup.command(name="disable_welcome", aliases=["dis_welcome"])
    @commands.has_guild_permissions(administrator=True)
    async def disable_welcome(self, ctx):
        if self.welcome_channel is None:
            await ctx.send("Welcome channel is not set up. Use `!setup enable_welcome` to enable it.")
            return

        self.stop_welcome_listeners()
        self.welcome_channel = None
        await ctx.send("Welcome messages disabled and event listners stopped.")

    def start_log_listeners(self):
        self.bot.add_listener(self.on_message_edit, name="on_message_edit")
        self.bot.add_listener(self.on_message_delete, name="on_message_delete")
        self.bot.add_listener(self.on_raw_message_delete, name="on_raw_message_delete")
        self.bot.add_listener(self.on_voice_state_update, name="on_voice_state_update")
        self.bot.add_listener(self.on_member_update, name="on_member_update")

    def stop_log_listeners(self):
        self.bot.remove_listener(self.on_message_edit, name="on_message_edit")
        self.bot.remove_listener(self.on_message_delete, name="on_message_delete")
        self.bot.remove_listener(self.on_raw_message_delete, name="on_raw_message_delete")
        self.bot.remove_listener(self.on_voice_state_update, name="on_voice_state_update")
        self.bot.remove_listener(self.on_member_update, name="on_member_update")

    def start_welcome_listeners(self):
        self.bot.add_listener(self.on_member_join, name="on_member_join")
        self.bot.add_listener(self.on_member_remove, name = "on_member_remove")

    def stop_welcome_listeners(self):
        self.bot.remove_listener(self.on_member_join, name="on_member_join")
        self.bot.remove_listener(self.on_member_remove, name = "on_member_remove")

    # Event listeners for logging
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            if before.content != after.content and before.author != self.bot.user:
                # Message content has changed and it's not from the bot itself
                channel = before.channel
                author = before.author
                old_content = before.content
                new_content = after.content
                
                log_channel = self.log_channel
                if log_channel:
                    embed = discord.Embed(title="Message Edited", color=0x00FFFF)
                    embed.set_thumbnail(url=author.avatar.url)
                    embed.set_author(name=f"{author.display_name} (ID: {author.id})", icon_url=author.avatar.url)
                    embed.add_field(name="Channel", value=channel.mention)
                    embed.add_field(name="Before", value=old_content, inline=False)
                    embed.add_field(name="After", value=new_content, inline=False)
                    await log_channel.send(embed=embed)
                    print(f"log added.")
                
        except Exception as e:
            print(f"An error has occurred {e}, cannot send log  to this  channel {log_channel}")
       

    #when someones deletes a message:
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            if message.author != self.bot.user:
                # Message deleted and it's not from the bot itself
                channel = message.channel
                author = message.author
                content = message.content 
                
                log_channel = self.log_channel
                if log_channel:
                    embed = discord.Embed(title="Message Deleted", color=0xE84C93)
                    embed.set_thumbnail(url=author.avatar.url)
                    embed.set_author(name=f"{author.display_name} (ID: {author.id})", icon_url=author.avatar.url)
                    embed.add_field(name="Channel", value=channel.mention)
                    if content:  # Check if content is available
                        embed.add_field(name="Content", value=content, inline=False)
                    else:
                        embed.add_field(name="Content", value="**(attachments only)**", inline=False)
                    await log_channel.send(embed=embed)
        
        except Exception as e:
            print(f"An error has occurred {e} , cannot send log to this channel {log_channel}")
       

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):

            try:
                # Check if the message was deleted from a guild channel
                if not payload.guild_id:
                    return  # Ignore non-guild messages

                # Get log channel and deleted channel
                log_channel = self.log_channel
                if not log_channel:
                    print("Log channel not found!")
                    return  # Ignore if log channel not found

                deleted_channel = self.bot.get_channel(payload.channel_id)
                if not deleted_channel:
                    return  # Ignore if channel not found

                # Try to retrieve the deleted message (optional)
                try:
                    deleted_message = await deleted_channel.fetch_message(payload.message_id)
                except discord.NotFound:
                    # Message might be older than cache limit
                    deleted_message = None

                # Prepare embed for deleted message info
                embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
                embed.set_author(name=f"Channel: #{deleted_channel.name}", icon_url=self.bot.user.avatar.url)

                # Add details based on message availability
                if deleted_message:
                    author_name = deleted_message.author.name
                    author_discriminator = deleted_message.author.discriminator
                    content = deleted_message.content
                    embed.add_field(name="Author", value=f"{author_name}#{author_discriminator} (ID: {deleted_message.author.id})", inline=False)
                    embed.add_field(name="Content", value=content, inline=False)
                else:
                    embed.add_field(name="Content", value="Unavailable (likely older than cache limit)", inline=False)

                # Send embed to log channel
                await log_channel.send(embed=embed)

            except Exception as e:
                print(f"An error occurred processing deleted message: {e}")
        

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print(f"Member joined: {member.name}")
        guild = member.guild
        guildname = guild.name
        # Add this check to ensure the event is only handled once
        if member.bot:
            return  # Ignore bots
    
        try:
            # Try sending DM
            print("Sending DM...")
            dmchannel = await member.create_dm()
            embed = discord.Embed(
                title=f"Greetings ❄️",
                description=f"Welcome to : {guildname}, {member.mention}, Enjoy your stay and feel free to look around :)",
                color=0x00FFFF
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_image(url=self.bot.user.avatar.url)
            await dmchannel.send(embed=embed)
            # DM send succeeded, send welcome channel message if configured
            if self.welcome_channel:
                    print("Sending welcome text...")
                    embed = discord.Embed(
                        title=f"Greetings ❄️",
                        description=f"Welcome to : {guildname}, {member.mention}, Enjoy your stay and feel free to look around :)",
                        color=0x00FFFF
                    )
                    embed.set_thumbnail(url=self.bot.user.avatar.url)  # Use bot's avatar as thumbnail
                    embed.set_image(url=member.avatar.url)
                    embed.add_field(name="Information", value="Please consider to read the latest information!", inline=False)
                    await self.welcome_channel.send(embed=embed)

        except Exception as e:
         print(f"An error has occurred {e}, cannot send DM to the user.")
                 
    
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        print(f"Member left: {member.name}")
        guild = member.guild
        guildname = guild.name

        if member.bot:
            return  
    
        try:
            # Try sending DM
            print("Sending DM...")
            dmchannel = await member.create_dm()
            embed = discord.Embed(
                title=f"Goodbye ❄️",
                description=f"{member.mention}, Thank you for visiting the server,hope you had a great time:)",
                color=0x00FFFF
            )
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_image(url=self.bot.user.avatar.url)
            await dmchannel.send(embed=embed)

            # DM send succeeded, send welcome channel message if configured
            if self.welcome_channel:
                    print("Sending Goodbye text...")
                    embed = discord.Embed(
                        title=f"GOodbye ❄️",
                        description=f"Sad to see you leave : {guildname}, {member.mention}, Hope you enjoyed your stay:)",
                        color=0x00FFFF
                    )
                    embed.set_thumbnail(url=self.bot.user.avatar.url)  # Use bot's avatar as thumbnail
                    embed.set_image(url=member.avatar.url)
                    embed.add_field(name="Information", value="A member has left the server", inline=False)
                    await self.welcome_channel.send(embed=embed)

        except Exception as e:
            print(f"An error has occurred {e}, cannot send DM to the user.")
            
            
    #when member updates data
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
            try:
                if before.id != self.bot.user.id: 
                    log_channel = self.log_channel
                    if log_channel:
                        # Track member updates
                        updated_nickname = before.display_name != after.display_name
                        updated_roles = before.roles != after.roles
                        updated_avatar = before.avatar != after.avatar

                        # Handle member updates with embeds
                        if updated_nickname or updated_roles or updated_avatar:
                            embed = discord.Embed(color=discord.Color.blue()) 
                            embed.set_author(name=f"{after.display_name} (ID: {after.id})", icon_url=after.avatar.url)

                            if updated_nickname:
                                embed.title = "Nickname Update"
                                embed.add_field(name="Old Nickname", value=before.display_name, inline=False)
                                embed.add_field(name="New Nickname", value=after.display_name, inline=False)

                            if updated_roles:
                                added_roles = [role for role in after.roles if role not in before.roles]
                                removed_roles = [role for role in before.roles if role not in after.roles]
                                if added_roles:
                                    added_roles_str = ", ".join([role.name for role in added_roles])
                                    embed.add_field(name="Added Roles", value=added_roles_str, inline=False)
                                if removed_roles:
                                    removed_roles_str = ", ".join([role.name for role in removed_roles])
                                    embed.add_field(name="Removed Roles", value=removed_roles_str, inline=False)
                                if not (added_roles and removed_roles): 
                                    embed.title = "Role Update"

                            if updated_avatar:
                                embed.title = "Avatar Update"
                                embed.add_field(name="New Avatar URL", value=after.avatar.url, inline=False)
                            if not log_channel.permissions_for(log_channel.guild.me).send_messages:
                                 print("The bot lacks permissions to send messages in this channel.")
                            else:
                                await log_channel.send(embed=embed)

            except discord.HTTPException as e:
                print(f"An error occurred sending a message: {e}")
            except Exception as e: 
                print(f"An unexpected error occurred: {e}")
    
    
    #voice_eevnts:
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if not member.guild:
            return  # Ignore events for non-guild members

        log_channel = self.log_channel
        if not log_channel:
            print(f"Logging channel not found")
            return

        embed = discord.Embed(color=0x00ff00)  # Green for join/switch, red for leave
        embed.set_author(name=member.name, icon_url=member.avatar.url)
        timestamp = datetime.utcnow().strftime("%H:%M:%S")

        if not before.channel and after.channel:  # User joined a voice channel
            embed.title = f"{member.name} joined voice channel"
            embed.set_thumbnail(url=member.avatar.url)
            embed.description = f"{after.channel.name} at {timestamp} UTC"
        elif before.channel and not after.channel:  # User left a voice channel
            embed.title = f"{member.name} left voice channel"
            embed.set_thumbnail(url=member.avatar.url)
            embed.description = f"{before.channel.name} at {timestamp} UTC"
            embed.color = 0xff0000  # Red for leaving
        elif before.channel != after.channel:  # User switched voice channels
            embed.title = f"{member.name} switched voice channels"
            embed.description = f"From {before.channel.name} to {after.channel.name} at {timestamp} UTC"
            embed.set_thumbnail(url=member.avatar.url)

        await log_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utilities(bot))