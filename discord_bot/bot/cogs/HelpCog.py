import discord
from discord.ext import commands
from discord import ui, Interaction, ButtonStyle

class PaginatedHelpView(ui.View):
    def __init__(self, ctx, embeds):
        super().__init__(timeout=60)
        self.ctx = ctx
        self.embeds = embeds
        self.current_page = 0

    @ui.button(label="⏮️", style=ButtonStyle.grey, disabled=True)
    async def first(self, interaction: Interaction, button: ui.Button):
        self.current_page = 0
        await self.update_page(interaction)

    @ui.button(label="◀️", style=ButtonStyle.grey, disabled=True)
    async def previous(self, interaction: Interaction, button: ui.Button):
        self.current_page -= 1
        await self.update_page(interaction)

    @ui.button(label="▶️", style=ButtonStyle.grey)
    async def next(self, interaction: Interaction, button: ui.Button):
        self.current_page += 1
        await self.update_page(interaction)

    @ui.button(label="⏭️", style=ButtonStyle.grey)
    async def last(self, interaction: Interaction, button: ui.Button):
        self.current_page = len(self.embeds) - 1
        await self.update_page(interaction)

    async def update_page(self, interaction: Interaction):
        embed = self.embeds[self.current_page]
        self.previous.disabled = self.current_page == 0
        self.next.disabled = self.current_page == len(self.embeds) - 1
        self.first.disabled = self.current_page == 0
        self.last.disabled = self.current_page == len(self.embeds) - 1
        await interaction.response.edit_message(embed=embed, view=self)

    async def on_interaction(self, interaction: Interaction):
        for button in self.children:
            if interaction.data.get("custom_id") == button.custom_id:
                await button.callback(interaction)

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Help_Cog Cog is ready:")

    def generate_embeds(self, ctx, title, commands):
        embeds = []
        pages = [commands[i:i+5] for i in range(0, len(commands), 5)]
        for page in pages:
            embed = discord.Embed(title=title, color=0x00FFFF)
            for command in page:
                embed.add_field(name=command[0], value=command[1], inline=False)
            embeds.append(embed)
        return embeds

    @commands.command(aliases=["about"])
    async def help(self, ctx):
        commands = [
            ("`!help_general`", "List of General Commands."),
            ("`!help_music`", "List of Music Commands."),
            ("`!help_moderation`", "List of Moderation commands."),
            ("`!help_admins`", "List of Defination and Setup Commands."),
            ("`!snowfall_info`", "Provides Information on snowfall."),
        ]
        embeds = self.generate_embeds(ctx, "List of Accessible Commands.", commands)
        view = PaginatedHelpView(ctx, embeds)
        await ctx.send(embed=embeds[0], view=view)
        
        
    @commands.command(aliases=["general"])
    async def help_general(self, ctx):
        commands = [
            ("`!yuki_ping`", "checks bot latency"),
            ("`!yuki_coinflip`", "Flips a coin"),
            ("`!yuki_roll`", "Rolls a Random Number"),
            ("`!yuki_meme`", "Shares a Randome Meme."),
            ("`!yuki_dankmeme`", "Shares a dank meme"),
            ("`!yuki_quote`", "Quotes a person."),
            ("`!yuki_fact`", "Shares a Random Fact."),
            ("`!yuki_rps <choice>`", "Plays a game of rock paper and scissors."),
            ("`!yuki_test`", "checks bot latency"),
            ("`!yuki_avatar <username>`", "Shows user avatar"),
            ("`!yuki_userinfo <username>`", "Shows user info"),
            ("`!snowfall_info`", "provides information on Snowfall."),
        ]
        embeds = self.generate_embeds(ctx, "General Commands", commands)
        view = PaginatedHelpView(ctx, embeds)
        await ctx.send(embed=embeds[0], view=view)
        
        
    @commands.command(aliases=["music"])
    async def help_music(self, ctx):
        commands = [
            ("`!yuki_join`", "Joins a Voice channel."),
            ("`!yuki_leave`", "Leaves the Voice Channel."),
            ("`!yuki_play`", "Plays the song."),
            ("`!yuki_pause`", "Pauses the current song."),
            ("`!yuki_resume`", "Resumes the current song."),
            ("`!yuki_skip`", "Skipes to the next song."),
            ("`!yuki_stop`", "Stops playing all the songs."),
            ("`!yuki_queue`", "Displays the list of songs from the queue."),
            ("`!yuki_now_playing`", "Status of the song being played."),
            ("`!yuki_playtop`", "Moves a song from of the queue to the next song."),
            ("`!yuki_remove`", "Removes a song from the queue."),
            ("`!yuki_lyrics`", "Displays the lyrics of the song being played"),
            ("`!snowfall_info`", "provides information on Snowfall."),
        ]
        embeds = self.generate_embeds(ctx, "Music Commands", commands)
        view = PaginatedHelpView(ctx, embeds)
        await ctx.send(embed=embeds[0], view=view)
        
    @commands.command(aliases=["mods"])
    @commands.has_permissions(manage_messages=True)
    async def help_moderation(self, ctx):
        commands = [
            ("`!yuki_kick <username>`", "Kicks a user out of the guild."),
            ("`!yuki_ban <username>`", "Bans a user from the guild."),
            ("`!yuki_unban <username>`", "Unbans a user from the guild."),
            ("`!yuki_purge <>`", "Deletes a certain amount of messages."),
            ("`!yuki_mute <username>`", "Mutes a user."),
            ("`!yuki_unmute <username>`", "Unmutes the user."),
            ("`!yuki_deafen <username>`", "Defeans the user."),
            ("`!yuki_undeafen <username>`", "Undeafens the user."),
            ("`!yuki_voicekick <username>`", "Kicks the user form the voice channel."),
            ("`!yuki_voiceban <username>`", "Bans the user from the voice_channels."),
            ("`!yuki_voice_unban <username>`", "Unbans the user from the voice_channels."),
            ("`!yuki_giverole <username> <role>`", "Grants the specified role to the user"),
            ("`!yuki_yuki_revokerole <username> <role>`", "Revokes the specified role from the user."),
            ("`!snowfall_info`", "provides information on Snowfall."),
        ]
        embeds = self.generate_embeds(ctx, "Music Commands", commands)
        view = PaginatedHelpView(ctx, embeds)
        await ctx.send(embed=embeds[0], view=view)
        
    @help_moderation.error
    async def help_moderation_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to access this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid Command, Please use the `!help` command to access the list of the commands.")
        else:
            await ctx.send(f"An error occurred: {error}")
            
    @commands.command(aliases=["admins"])
    @commands.has_permissions(manage_messages=True)
    async def help_admins(self, ctx):
        commands = [
            ("`!yuki_leave_the_server `", "Bot leaves the server."),
            ("`!yuki_create_role <rolename>`", "Creates a role with specified name."),
            ("`!yuki_delete_role <rolename>`", "Deletes a role with sepcified name."),
            ("`!yuki_set_server_name <name>`", "Sets a new name for the server."),
            ("`!yuki_create_text_channel <name>`", "Creates a text channel with sepcified name."),
            ("`!yuki_delete_text_channel <name>`", "Deletes a text channel with sepcified name."),
            ("`!yuki_create_voice_channel <name>`", "Creates a voice channel with sepcified name."),
            ("`!yuki_delete_voice_channel <name>`", "Deletes a voice channel with sepcified name."),
            ("`!yuki_setup enable_logging`", "Enables logs for the server."),
            ("`!yuki_setup disbale_logging`", "Disables logs for the server."),
            ("`!yuki_setup enable_welcome`", "Enables Greetings (welcome_goodbyes) messages."),
            ("`!yuki_setup disable_welcome`", "Disables Greetings(Welcome_goodbyes) messages."),
            ("`!snowfall_info`", "provides information on Snowfall."),
        ]
        embeds = self.generate_embeds(ctx, "Music Commands", commands)
        view = PaginatedHelpView(ctx, embeds)
        await ctx.send(embed=embeds[0], view=view)
        
    @help_admins.error
    async def help_admins_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to access this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid Command, Please use the `!help` command to access the list of the commands.")
        else:
            await ctx.send(f"An error occurred: {error}")

async def setup(bot):
    await bot.add_cog(HelpCog(bot))