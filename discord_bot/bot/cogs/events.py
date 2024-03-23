import discord
import random
from discord.ext import commands,tasks
from datetime import datetime
import re

class events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"events cog is ready:")
        

    #Member events
    
    #member joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            guild = member.guild
            guildname = guild.name   
            dmchannel = await member.create_dm()
            channel_id = 1216737091082256384  #sent
            channel = guild.get_channel(channel_id)
            
            embed = discord.Embed(
                    title = f"Greetings ❄️",
                    description= f"Welcome to : {guildname}, {member.mention},Enjoy your your stay and feel free to look around :)",
                    color = 0x00FFFF
            )
            embed.set_image(url  = member.avatar.url)
            await dmchannel.send(embed = embed)
            
        except Exception as e:
            print(f"An error has occured {e}, cannot send dm to the user.")
            
        try:
            if channel:
                embed1 = discord.Embed(
                    title = f"Greetings ❄️",
                    description=f"welcome to : {guildname}, { member.mention}, Enjoy your stay and feel free to look around :)",
                    color =0x00FFFF
                )
            embed1.set_thumbnail(url =member.avatar.url)
            embed1.set_image(url =member.avatar.url)
            embed1.add_field(name="Information",value= "Please consider to read the latest information!",inline = False)
            
            await channel.send(embed = embed1)
            
        except Exception as e:
                print(f"An error has occurred {e} , cannot send dm to this user")
                
                
             
    #member leaves the guild   
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        try:
            guild = member.guild
            guildname = guild.name
            dmchannel = await member.create_dm()
            channel_id = 1216966481494147184  #your channel_id where you want the msg to be sent
            channel = guild.get_channel(channel_id)
            
            embed = discord.Embed(
                title =f"Goodbye:",
                description=f" {member.mention}, Sad to see you leave our server: {guildname} :)",
                color =0xFF0000
            )
            embed.set_image(url = self.bot.user.avatar.url)
            await dmchannel.send(embed = embed)
            
        except Exception as e:
            print(f"An error has occurred , cannot send dm to this user")
          
        try:  
            if channel:
            
                embed1 =discord.Embed(
                    title = f"Goodbye ❄️",
                    description=f" Sad to see  you leave,  { member.mention} Thank you for your visit:)",
                    color =0xFF0000  
            )
            embed1.set_thumbnail(url =member.avatar.url)
            embed1.set_image(url =member.avatar.url)
            embed1.add_field(name="Information",value= f"Member left the server!",inline = False)
            
            await channel.send(embed = embed1)
            
        except Exception as e:
                print(f"An error has occurred {e}, cannot send dm to this user")
    
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
            try:
                if before.id != self.bot.user.id: 
                    channel_id = 1216973226366996570 #log channel_id
                    log_channel = self.bot.get_channel(channel_id) 
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
                
                
        #part1
     #when they send a specific message:
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
            
    #part2
    #when someone edites the messgae:
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            if before.content != after.content and before.author != self.bot.user:
                # Message content has changed and it's not from the bot itself
                channel = before.channel
                author = before.author
                old_content = before.content
                new_content = after.content
                channel_id= 1216973226366996570
                log_channel = self.bot.get_channel(channel_id)
                if log_channel:
                    embed = discord.Embed(title="Message Edited", color=discord.Color.orange())
                    embed.set_author(name=f"{author.display_name} (ID: {author.id})", icon_url=author.avatar.url)
                    embed.add_field(name="Channel", value=channel.mention)
                    embed.add_field(name="Before", value=old_content, inline=False)
                    embed.add_field(name="After", value=new_content, inline=False)
                    await log_channel.send(embed=embed)
                
        except Exception as e:
            print(f"An error has occurred {e}, cannot send log  to this  channel {channel_id}")
    
    #part3
    #when someones deletes a message:
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            if message.author != self.bot.user:
                # Message deleted and it's not from the bot itself
                channel = message.channel
                author = message.author
                content = message.content 
                channel_id= 1216973226366996570
                log_channel = self.bot.get_channel(channel_id)
                if log_channel:
                    embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
                    embed.set_author(name=f"{author.display_name} (ID: {author.id})", icon_url=author.avatar.url)
                    embed.add_field(name="Channel", value=channel.mention)
                    if content:  # Check if content is available
                        embed.add_field(name="Content", value=content, inline=False)
                    else:
                        embed.add_field(name="Content", value="**(attachments only)**", inline=False)
                    await log_channel.send(embed=embed)
        
        except Exception as e:
            print(f"An error has occurred {e} , cannot send log to this channel {channel_id}")
                
    #part4
    #deletes msges older than weeks
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):

            try:
                # Check if the message was deleted from a guild channel
                if not payload.guild_id:
                    return  # Ignore non-guild messages

                # Get log channel and deleted channel
                self.log_channel_id = 1217003457009942618
                log_channel = self.bot.get_channel(self.log_channel_id)
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
                
      
    #GUILD EVENTS
    
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
    
    
    #ERROR COMMANDS
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Check for specific error types and provide user-friendly messages
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"Command '{ctx.command}' not found. Try using `help` for a list of commands.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument(s) for command '{ctx.command.qualified_name}'.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(f"You don't have the necessary permissions to use '{ctx.command}'.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"Invalid argument(s) provided for command '{ctx.command}'.")
        else:
            # Handle other unexpected errors
            print(f"An error occurred while processing command '{ctx.command}': {error}")
            
            
            
    #part2
    @commands.Cog.listener()
    async def on_voice_client_speaking(self, member, speaking):
        try:
            if speaking:
                print(f"{member.name} started speaking in {member.voice.channel.name}")
            else:
                print(f"{member.name} stopped speaking in {member.voice.channel.name}")
        except Exception as e:
                print(f"An error has occured {e} @on_voice_client_speaking , cannot send the message")
            

    #part3
    @commands.Cog.listener()
    async def on_audio_data_received(self, data, user, vchannel):
        print(f"Received audio data from {user.name} in {vchannel.name}")
        # Process the audio data here
        pass
    
    #part4:
    @commands.Cog.listener()
    async def on_voice_client_disconnect(self, vc):
        print(f"Bot disconnected from {vc.channel.name}")

    #part5
    @commands.Cog.listener()
    async def on_voice_client_move(self, vc, old_channel, new_channel):
        print(f"Bot moved from {old_channel.name} to {new_channel.name}")

    #part6
    @commands.Cog.listener()
    async def on_voice_client_kick(self, vc, moderator):
        print(f"Bot kicked from {vc.channel.name} by {moderator.name}")
        
                
                
async def setup(bot):
    await bot.add_cog(events(bot))