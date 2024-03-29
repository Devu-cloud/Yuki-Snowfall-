import discord
from discord.ext import commands,tasks
import aiohttp
import random
import requests

class basic(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
  
        
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"basic Cog is ready:")
        
        
    #test commands:  
    @commands.command(aliases= ["yuki_test"])
    async def test(self,ctx):
        await ctx.send("This is a test command!")
        
   #coinflip command:
    @commands.command(aliases= ["yuki_coinflip"])
    async def coinflip(self,ctx):
        try:
            """Flips a coin and returns Heads or Tails."""

            result = "Heads" if random.randint(1, 2) == 1 else "Tails"
            await ctx.send(result)
            print(f"printed")
        except Exception as e:
            print(f"An Error has occured {e}, conflip command")
           
    #rock_papers_scissors command:
    @commands.command(aliases= ["yuki_rps"])
    async def rps(self, ctx, choose):
        """Plays a game of Rock-Paper-Scissors with the bot."""

        valid_choices = ["🪨", "✋", "✂️"]  # List of valid choices

        if choose not in valid_choices:
            await ctx.send(f"Invalid choice! Please choose Rock (🪨), Paper (✋), or Scissors (✂️).")
            return  # Exit the function if invalid input

        list1 = valid_choices
        botchoose = random.choice(list1)
        await ctx.send(f"You chose: {choose}\nI chose: {botchoose}")

        if choose == botchoose:
            await ctx.send("Draw")
        else:
            win_dict = {"🪨": "✂️", "✋": "🪨", "✂️": "✋"}
            if win_dict[choose] == botchoose:
                await ctx.send("You win!")
            else:
                await ctx.send("I win!")

              
    #rolldie command
    @commands.command(name='roll')
    async def roll(self, ctx, dice: str):
        """Rolls a dice in the specified format.

        Example: !roll 2d6 (rolls two six-sided dice)
        """
        try:
            rolls, limit = map(int, dice.split('d'))
        except ValueError:
            await ctx.send('Invalid dice format. Use the format: `NdX` where N is the number of dice and X is the number of sides.')
            return

        result = ', '.join(str(random.randint(1, limit)) for _ in range(rolls))
        await ctx.send(f'🎲 You rolled: {result}')
        
    #roll error handler: 
    @roll.error
    async def roll_error(self,ctx,error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to acess this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Invalid Arguements or Format:")
        else:
            await ctx.send(f"An error occurred: {error}")
    
    #meme command
    @commands.command()
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.reddit.com/r/memes/random/.json") as response:
                data = await response.json()
                meme = data[0]["data"]["children"][0]["data"]
                url = meme["url"]
                title = meme["title"]
                upvotes = meme["ups"]

                embed = discord.Embed(title=title, color=discord.Color.random())
                embed.set_image(url=url)
                embed.set_footer(text=f"👍 {upvotes}")

                await ctx.send(embed=embed)
        
    #meme error handler:
    @meme.error
    async def meme_error(Self, ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You don't have the permssions to use this command")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Bad arguments")
        else:
            await ctx.send(f"An error has occurred {error}")
       
    #dankmeme command:     
    @commands.command()
    @commands.has_role("Dank")
    async def dankmeme(self, ctx):
        """Fetches a random dank meme from Reddit."""
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.reddit.com/r/dankmemes/random/.json") as response:
                data = await response.json()
                meme = data[0]["data"]["children"][0]["data"]
                url = meme["url"]
                title = meme["title"]
                upvotes = meme["ups"]
                nsfw = meme["over_18"]

                if nsfw:
                    embed = discord.Embed(title=title, color=discord.Color.random(), description="⚠️ NSFW Content")
                else:
                    embed = discord.Embed(title=title, color=discord.Color.random())

                embed.set_image(url=url)
                embed.set_footer(text=f"👍 {upvotes}")

                await ctx.send(embed=embed)
    
    #meme error handler:
    @dankmeme.error
    async def dankmeme_error(Self, ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You don't have the permssions to use this command")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Bad arguments")
        else:
            await ctx.send(f"An error has occurred {error}")
            
    #fact command
    @commands.command()
    async def fact(self, ctx):
        try:
            response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
            response.raise_for_status()
            fact = response.json()["text"]
            await ctx.send(f"🧠 Random Fact: {fact}")
        except requests.exceptions.RequestException as e:
            await ctx.send(f"An error occurred while fetching a random fact:\n{e}")
            
    #fact error handler:
    @fact.error
    async def fact_error(Self, ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You don't have the permssions to use this command")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Bad arguments")
        else:
            await ctx.send(f"An error has occurred {error}")
            

    #quote command
    @commands.command()
    async def quote(self, ctx):
        """Sends a random quote."""
        try:
            response = requests.get("https://api.quotable.io/random")
            response.raise_for_status()
            quote = response.json()["content"]
            author = response.json()["author"]
            await ctx.send(f"💬 Random Quote: \"{quote}\" - {author}")
        except requests.exceptions.RequestException as e:
            await ctx.send(f"An error occurred while fetching a random quote:\n{e}")
        
    #quote error handler:
    @quote.error
    async def quote_error(Self, ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("You don't have the permssions to use this command")
        elif isinstance(error,commands.BadArgument):
            await ctx.send("Bad arguments.")
        else:
            await ctx.send(f"An error has occurred {error}")
            
        
async def setup(bot):
     await bot.add_cog(basic(bot))