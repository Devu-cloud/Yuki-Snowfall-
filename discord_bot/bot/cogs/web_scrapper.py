import discord
import pandas as pd
import requests
import os
import tempfile
import csv
from discord.ext import commands

MAX_MESSAGE_LENGTH = 1900

class web_scrapper(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"web_scrapper Cog is ready:")

    @commands.command()
    async def get_table(self, ctx, url):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w', encoding='utf-8') as temp_file:
                tables = pd.read_html(url)
                table_count = len(tables)
                await ctx.send(f"Number of tables found: {table_count}")

                for i, table in enumerate(tables, start=1):
                    table.to_csv(temp_file, mode='a', header=False, index=False)

                temp_file.flush()
                with open(temp_file.name, 'rb') as file:
                    await ctx.send(file=discord.File(file, f'table_data.csv'))

            os.unlink(temp_file.name)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def read_csv(self, ctx, url):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='wb') as temp_file:
                response = requests.get(url)
                response.raise_for_status()
                temp_file.write(response.content)
                temp_file.flush()
                with open(temp_file.name, 'rb') as file:
                    await ctx.send(file=discord.File(file, 'csv_data.csv'))

            os.unlink(temp_file.name)

        except UnicodeDecodeError as e:
            await ctx.send(f"Error decoding the CSV file: {e}")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")
    
       
async def setup(bot):
    await bot.add_cog(web_scrapper(bot))