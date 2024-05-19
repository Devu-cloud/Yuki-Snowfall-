import discord
from discord.ext import commands,tasks
import yt_dlp as youtube_dl
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio
import lyricsgenius
from datetime import datetime,timedelta
from collections import deque
import os

# Configure Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="YOUR_CLIENT_ID", client_secret="YOUR_CLIENT_SECRET"))

genius = lyricsgenius.Genius("GENIUS_ACCESS_TOKEN")

class audio_player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = deque()
        self.current_song = None
        self.playing_song = None
        self.voice_client = None
        self.delete_files = deque()
        self.idle_timeout.start()
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': False,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'source_address': '0.0.0.0'
        }
        self.ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        
    class YTDLSource(discord.PCMVolumeTransformer):
        def __init__(self, source, *, data, volume=0.5):
            super().__init__(source, volume)
            self.data = data
            self.title = data.get('title')
            self.url = data.get('url')
            self.duration = data.get('duration')

        def __str__(self):
            return self.title

        @classmethod
        async def create_source(cls, ctx, search_term, loop=None, download=False):
            loop = loop or asyncio.get_event_loop()
            data = await cls.extract_info(ctx, search_term, loop, download)
            
            if data.get('entries'): #for playlists.
                sources = [cls(discord.FFmpegPCMAudio(entry['url'], **ctx.cog.ffmpeg_options), data=entry) for entry in data['entries']]
                return sources
            else:
                source = discord.FFmpegPCMAudio(data.get('url'), **ctx.cog.ffmpeg_options)
                return cls(source, data=data)

        @staticmethod
        async def extract_info(ctx, search_term, loop, download):
            with youtube_dl.YoutubeDL(ctx.cog.ydl_opts) as ydl:
                try:
                    if search_term.startswith(("http", "www")):
                        info = await loop.run_in_executor(None, lambda: ydl.extract_info(search_term, download=download))
                    else:
                        info = await loop.run_in_executor(None, lambda: ydl.extract_info(f"ytsearch:{search_term}", download=download))
                        info = info.get('entries', [])[0]
                except Exception as e:
                    raise Exception(f"An error occurred while searching: {e}")
            return info

    @tasks.loop(minutes=15)
    async def idle_timeout(self):
        if self.voice_client and not self.voice_client.is_playing():
            await self.voice_client.disconnect()
            await self.voice_client.guild.text_channels[0].send(embed=discord.Embed(
                title="Goodbye!",
                description="Bot has been disconnected due to inactivity.",
                color=discord.Color.red()
            ))
            self.voice_client = None
            self.queue.clear()
            self.current_song = None

    async def check_queue(self, ctx, error=None):
        if error:
            print(f"Error occurred during playback: {error}")
            try:
                await ctx.send(f"Error occurred during playback: {error}")
            except:
                pass

        if self.queue:
            self.current_song = self.queue.popleft()
            self.voice_client = ctx.voice_client
            self.voice_client.play(self.current_song, after=lambda e: asyncio.run_coroutine_threadsafe(self.check_queue(ctx, e), self.bot.loop))
            await ctx.send(f"Now playing: **{self.current_song.title}**")
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=self.current_song.title))
        else:
            self.current_song = None
            self.voice_client.stop()
            await self.bot.change_presence(activity=None)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You're not connected to a voice channel.")
            return

        voice_channel = ctx.author.voice.channel

        if self.voice_client and self.voice_client.channel == voice_channel:
            await ctx.send(embed=discord.Embed(
                description=f"Already joined in {voice_channel.mention}.",
                color=discord.Color.blue()
            ))
            return

        if self.voice_client and self.voice_client.channel != voice_channel:
            if not self.voice_client.is_playing() and len(self.voice_client.channel.members) == 1:
                await self.voice_client.move_to(voice_channel)
            else:
                await ctx.send("Bot is currently playing in another voice channel. Please use the `!!stop` command to stop playback first.")
                return

        if self.voice_client is None:
            self.voice_client = await voice_channel.connect()

    @commands.command()
    async def play(self, ctx, *, search_term):
        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()

        if not ctx.voice_client.is_playing():
            sources = await self.YTDLSource.create_source(ctx, search_term, loop=self.bot.loop, download=False)
            if isinstance(sources, list):
                self.queue.extend(sources)
                source = self.queue[0]
                ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.check_queue(ctx, e), self.bot.loop))
                await ctx.send(f"Playing **{source.title}** from the playlist :musical_note:")
            else:
                self.queue.append(sources)
                ctx.voice_client.play(sources, after=lambda e: asyncio.run_coroutine_threadsafe(self.check_queue(ctx, e), self.bot.loop))
                await ctx.send(f"Playing **{sources.title}** :musical_note:")
        else:
            sources = await self.YTDLSource.create_source(ctx, search_term, loop=self.bot.loop, download=False)
            if isinstance(sources, list):
                self.queue.extend(sources)
                await ctx.send(f"Added playlist to queue.")
            else:
                self.queue.append(sources)
                await ctx.send(f"Added to queue: **{sources.title}**")
                

    @commands.command()
    async def pause(self, ctx):
        if self.voice_client is None or not self.voice_client.is_playing():
            await ctx.send("Bot is not playing audio.")
            return

        self.voice_client.pause()
        await ctx.send("Audio paused.")

    @commands.command(aliases=["stop_music"])
    async def stop(self, ctx):
        if self.voice_client is None or not self.voice_client.is_playing():
            await ctx.send("Bot is not playing audio.")
            return

        self.voice_client.stop()
        await ctx.send("Audio stopped.")

    @commands.command()
    async def resume(self, ctx):
        if self.voice_client is None or not self.voice_client.is_paused():
            await ctx.send("Bot is not paused.")
            return

        self.voice_client.resume()
        await ctx.send("Audio resumed.")


    @commands.command()
    async def queue(self, ctx):
        if not self.queue:
            await ctx.send("Queue is empty.")
            return

        pages = []
        current_page = 0
        total_duration = timedelta()

        for i, source in enumerate(self.queue, start=1):
            duration = str(timedelta(seconds=source.duration))
            total_duration += timedelta(seconds=source.duration)
            requested_by = source.data.get('requested_by', ctx.author.display_name)
            page_entry = f"{i}. {source.title} ({duration}) - Requested by {requested_by}"

            if not pages or len(pages[-1]) >= 10:
                pages.append([])
            pages[-1].append(page_entry)

        embed = discord.Embed(title="Queue", color=discord.Color.blue())

        def update_embed(page):
            nonlocal embed
            embed.clear_fields()
            for entry in pages[page]:
                embed.add_field(name="\u200b", value=entry, inline=False)
            embed.set_footer(text=f"Page {page+1}/{len(pages)} | Total duration: {str(total_duration)}")

        update_embed(current_page)
        message = await ctx.send(embed=embed)

        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
                if str(reaction.emoji) == "⬅️":
                    current_page = max(current_page - 1, 0)
                elif str(reaction.emoji) == "➡️":
                    current_page = min(current_page + 1, len(pages) - 1)
                update_embed(current_page)
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.clear_reactions()
                break
            
    @commands.command()
    async def playtop(self, ctx, position: int = None):
        if not self.queue:
            await ctx.send("Queue is empty.")
            return

        if position is None or position < 1 or position > len(self.queue):
            await ctx.send("Invalid position. Please provide a valid position in the queue.")
            return

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()

        song = self.queue.pop(position - 1)
        self.queue.insert(0, song)

        if not ctx.voice_client.is_playing():
            self.current_song = song
            ctx.voice_client.play(song, after=lambda e: self.check_queue())
            await ctx.send(f"Playing **{song.title}** :musical_note:")
        else:
            await ctx.send(f"Moved **{song.title}** to the top of the queue.")
            
    @commands.command()
    async def remove(self, ctx, position: int = None):
        if not self.queue:
            await ctx.send("Queue is empty.")
            return

        if position is None or position < 1 or position > len(self.queue):
            await ctx.send("Invalid position. Please provide a valid position in the queue.")
            return

        if ctx.voice_client.is_playing():
            if position == 1:
                await ctx.send("Cannot remove the currently playing song. Use the `!!stop` command to stop playback.")
                return

        song = self.queue.pop(position - 1)

        if ctx.voice_client.is_playing() and position == 2:
            self.current_song = self.queue.popleft()
            self.voice_client.stop()
            self.voice_client.play(self.current_song, after=lambda e: self.check_queue())
            await ctx.send(f"Removed **{song.title}** from the queue. Now playing **{self.current_song.title}**.")
        else:
            await ctx.send(f"Removed **{song.title}** from the queue.")

    @commands.command()
    async def disconnect(self, ctx):
        if self.voice_client is None:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        await self.voice_client.disconnect()
        self.voice_client = None
        self.queue.clear()
        self.current_song = None
        
        
    @commands.command(aliases=['np', 'current'])
    async def now_playing(self, ctx):
        try:
            player = ctx.voice_client.source
            if player and player.title:
                embed = discord.Embed(title=player.title, color=discord.Color.blue())
                duration = str(timedelta(seconds=player.duration))
                embed.add_field(name="Duration", value=duration, inline=True)
                embed.set_author(name="Playing Now:", icon_url=self.bot.user.avatar.url)
                await ctx.send(embed=embed)
            else:
                await ctx.send("No song is currently playing or queued.")
        except Exception as e:
            await ctx.send(f"Error retrieving song information: {e}")
    
        
    @commands.command(aliases=["skip"])
    async def next(self, ctx):
        voice_client = ctx.voice_client or self.voice_client

        if not voice_client:
            await ctx.send("Bot is not connected to a voice channel.")
            return

        if not voice_client.is_playing():
            await ctx.send("No audio is currently playing.")
            return

        if self.queue:
            try:
                print(f"Queue length before popping: {len(self.queue)}")
                voice_client.stop()
                next_song = self.queue.popleft()
                self.current_song = next_song
                print(f"Queue length after popping: {len(self.queue)}")
                voice_client.play(next_song, after=self.check_queue(ctx))  # Directly call check_queue
                await ctx.send(f"Skipped to **{next_song.title}**")
            except Exception as e:
                print(f"Error occurred while skipping song: {e}")
                await ctx.send(f"An error occurred while skipping the song: {e}")
        elif self.current_song:
            voice_client.stop()
            self.current_song = None
            await ctx.send("Skipped the current song.")
        else:
            await ctx.send("No songs in the queue.")


    @commands.command(aliases=['ly'])
    async def lyrics(self, ctx):
        if self.current_song is None:
            await ctx.send("No song is currently playing.")
            return

        song_info = genius.search_song(self.current_song.title)
        if song_info:
            lyrics = song_info.lyrics
            if lyrics:
                pages = [lyrics[i:i+2048] for i in range(0, len(lyrics), 2048)]
                current_page = 0
                embed = discord.Embed(title=song_info.title, color=discord.Color.blue())

                def update_embed(page):
                    nonlocal embed
                    embed.description = pages[page]

                update_embed(current_page)
                message = await ctx.send(embed=embed)

                await message.add_reaction("⬅️")
                await message.add_reaction("➡️")

                def check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ["⬅️", "➡️"]

                while True:
                    try:
                        reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
                        if str(reaction.emoji) == "⬅️":
                            current_page = max(current_page - 1, 0)
                        elif str(reaction.emoji) == "➡️":
                            current_page = min(current_page + 1, len(pages) - 1)
                        update_embed(current_page)
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)
                    except asyncio.TimeoutError:
                        await message.clear_reactions()
                        break
        else:
            await ctx.send("Error fetching lyrics.")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        if not after.channel and self.voice_client and self.voice_client.channel == before.channel:
            await self.idle_timeout.stop()
            await self.voice_client.disconnect()
            self.voice_client = None
            self.queue.clear()
            self.current_song = None

    @play.before_invoke
    @queue.before_invoke
    @playtop.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You're not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")

    @join.error
    @disconnect.error
    async def voice_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to use this command.")
        else:
            await ctx.send(f"An error occurred: {error}")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Music Cog is ready:")

    
async def setup(bot):
    await bot.add_cog(audio_player(bot))