import discord
from discord.ext import commands,tasks
from datetime import datetime

class server_defination(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"server_defination Cog is ready:")
      
    #leave command  
    @commands.command(aliases = ["yuki_leave the_server"])
    @commands.has_guild_permissions(manage_guild=True)  # Only allow users with "Manage Guild" permission
    async def yuki_leave_the_server(self, ctx):
        """
        This command allows the bot owner or authorized users to make the bot leave the server.
        """
        try:
            await ctx.guild.leave()
            await ctx.send(f"Goodbye {ctx.guild.name}! ")
            print(f"Left guild: {ctx.guild.name} (ID: {ctx.guild.id})")
        except discord.HTTPException as e:
            print(f"Failed to leave guild: {e}")
            await ctx.send(f"An error occurred while trying to leave the server. Please check bot permissions.")
            
    #leave command error handler
    @yuki_leave_the_server.error
    async def yuki_leave_the_server_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid role or member specified.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to Kick YUKI.")
        else:
            await ctx.send(f"An error occurred: {error}")
     
    #create role     
    @commands.command(aliases = ["yuki_create_role"])
    @commands.has_guild_permissions(manage_roles=True)
    async def create_role(self, ctx, *, role_name):
        """Creates a new role with the specified name."""
        guild = ctx.guild
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if existing_role:
            await ctx.send(f"The role '{role_name}' already exists in this server.")
        else:
            try:
                new_role = await guild.create_role(name=role_name)
                await ctx.send(f"Created a new role: {new_role.name}")
            except discord.HTTPException as e:
                await ctx.send(f"Failed to create the role '{role_name}'.\n{e}")
                
    #create_role command error handler
    @create_role.error
    async def create_role_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid role  specified.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to create role.")
        else:
            await ctx.send(f"An error occurred: {error}")
      
    #delete_role command      
    @commands.command(aliases = ["yuki_delete_role"])
    @commands.has_guild_permissions(administrator=True)
    async def delete_role(self, ctx, *, role: discord.Role):
        """Deletes the specified role from the server."""
        if role.is_default():
            await ctx.send("You cannot delete the default '@everyone' role.")
        else:
            try:
                await role.delete()
                await ctx.send(f"Deleted the role '{role.name}'.")
            except discord.HTTPException as e:
                await ctx.send(f"Failed to delete the role '{role.name}'.\n{e}")
    
    #create_role command error handler
    @create_role.error
    async def delete_role_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid role specified.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to delete role.")
        else:
            await ctx.send(f"An error occurred: {error}")
            
    #change server name command:
    @commands.command(aliases =["yuki_set_server_name"], description = "Change server name of the server.")
    @commands.has_guild_permissions(administrator=True)
    async def set_server_name(self, ctx , *, input):
        """ changes the server name """
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You do not have permission to use this command:")
            return
        
        if len(input)>50:
            await ctx.send("The name of the server cannot be longer than 50 characters")
            return
        
        if input == ctx.guild.name:
            await ctx.send("Server name is already set to that name.")
            return
        
        try:
            await ctx.guild.edit (name = input)
            embed1 = discord.Embed(title = "Update",
                                   description ="The server name has been updated:",
                                   color=0x00FFFF
            )
            embed1.set_thumbnail(url=self.bot.user.avatar.url)
            embed1.add_field( name = "Updated Name:", value =f"{ctx.guild.name}" , inline = False)
            embed1.set_footer(text=f"Updated by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed1)
            
        except Exception as e:
            await ctx.send(f"An error has occured as {e}, cannot change the server name:")
            
    #set_servername command error handler
    @set_server_name.error
    async def set_server_name_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Invalid name specified.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")
            
    #changing the region of the server
    #not anymore , discord doesn't allow you to change region through api
    #@commands.command(aliases =["yuki_set_server_region"], description =" Changes the server region of the server")
    #@commands.has_guild_permissions(manage_guild=True)
    #async def set_server_region(self, ctx, region: str):
        #"""Sets the server's region."""
        #try:
            #await ctx.guild.edit(name=region.replace(" ", "").lower())
            #embed1 = discord.Embed(title = "Update",
                                   #description ="The server name has been updated:",
                                  # color=0x00FFFF )
            #embed1.set_thumbnail(url=self.bot.user.avatar.url)
            #embed1.add_field( name = "Updated Region:", value =f"{ctx.guild.region}" , inline = False)
            #embed1.set_footer(text=f"Updated by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            #await ctx.send(embed=embed1)
            
        #except discord.HTTPException as e:
            #await ctx.send(f"Failed to set server region. Error: {e}")


    """Creates a new text channel."""
    @commands.command(aliases = ["yuki_create_text_channel"], description = "Creates a new text channel")
    @commands.has_guild_permissions(administrator=True)
    async def create_text_channel(self, ctx, channel_name):
       
        try:
            await ctx.guild.create_text_channel(channel_name)
            embed1 = discord.Embed(title = "Created",
                                   description ="A new text channel has been created:",
                                   color=0x00FFFF 
            )
            embed1.set_thumbnail(url=self.bot.user.avatar.url)
            embed1.add_field( name = "New Text Channel:", value =f"{channel_name}" , inline = False)
            embed1.set_footer(text=f"Created by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed1)
        except discord.HTTPException as e:
            await ctx.send(f"Failed to create text channel. Error: {e}")

    #error handler for text channel creation
    @create_text_channel.error
    async def create_text_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to create text channels.")
        else:
            await ctx.send(f"An error occurred: {error}")
    
    
    #Creates a new voice channel
    @commands.command(aliases = ["yuki_create_voice_channel"], description = "Creates a voice channel")
    @commands.has_guild_permissions(administrator=True)
    async def create_voice_channel(self, ctx, channel_name):
        
        try:
            await ctx.guild.create_voice_channel(channel_name)
            embed1 = discord.Embed(title = "Created",
                                   description ="A new voice channel has been created:",
                                   color=0x00FFFF 
            )
            embed1.set_thumbnail(url=self.bot.user.avatar.url)
            embed1.add_field( name = "New voice Channel:", value =f"{channel_name}" , inline = False)
            embed1.set_footer(text=f"Created by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed1)
        except discord.HTTPException as e:
            await ctx.send(f"Failed to create voice channel. Error: {e}")


    #voice channel error handler
    @create_voice_channel.error
    async def create_voice_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to create voice channels.")
        else:
            await ctx.send(f"An error occurred: {error}")
         
    #Deletes the specified text channel.
    @commands.command(aliases = ["yuki_delete_text_channel"], description = "Deletes a text channel")
    @commands.has_guild_permissions(administrator=True)
    async def delete_text_channel(self, ctx, channel: discord.TextChannel):
        try:
            await channel.delete()
            await ctx.send(f"Text channel '{channel.name}' has been deleted.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to delete text channel. Error: {e}")

    #delete_text_channel error handler
    @delete_text_channel.error
    async def delete_text_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to delete text channels.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid text channel specified.")
        else:
            await ctx.send(f"An error occurred: {error}")


    #Deletes the specified voice channel.
    @commands.command(aliases = ["yuki_delete_voice_channel"], description = "Deletes a voice channel")
    @commands.has_guild_permissions(administrator=True)
    async def delete_voice_channel(self, ctx, channel: discord.VoiceChannel):

        try:
            await channel.delete()
            await ctx.send(f"Voice channel '{channel.name}' has been deleted.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to delete voice channel. Error: {e}")

    #delete_voice_channel error handler
    @delete_voice_channel.error
    async def delete_voice_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to delete voice channels.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid voice channel specified.")
        else:
            await ctx.send(f"An error occurred: {error}")
            
         
async def setup(bot):
    await bot.add_cog(server_defination(bot))