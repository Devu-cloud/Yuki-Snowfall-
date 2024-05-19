from discord import File
import discord
from discord.ext import commands
import google.generativeai as genai
from config import config
import re
from PIL import Image
import io
import aiohttp


GOOGLE_API_KEY = config.GOOGLE_CLOUD_API_KEY
genai.configure(api_key=GOOGLE_API_KEY)

DISCORD_MAX_MESSAGE_LENGTH=2000
PLEASE_TRY_AGAIN_ERROR_MESSAGE ='There was an issue with your query,Please try again...'

text_generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 512,
}
image_generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 512,
}
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
]
text_model = genai.GenerativeModel(model_name="gemini-pro", generation_config=text_generation_config, safety_settings=safety_settings)
image_model = genai.GenerativeModel(model_name="gemini-pro-vision", generation_config=image_generation_config, safety_settings=safety_settings)

class ai_integration(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.text_model =text_model
        self.image_model = image_model
        
    @commands.Cog.listener()
    async def on_ready(self):
      print(f"ai_integration Cog is ready:")
      
      
    @commands.Cog.listener()
    async def on_message(self, msg):
        try:
            if msg.content == "on_ready, gemini_integration_confirmed":
                await msg.channel.send("gemini is ready...")
            elif 'Direct Message' in str(msg.channel) and not msg.author.bot:
                if msg.attachments:
                    # Handle image analysis in DM
                    attachment_url = msg.attachments[0].url
                    image_data = await self.download_image_from_url(attachment_url)
                    response_text = await self.generate_response_with_image_and_text(image_data, msg.content)
                    await msg.channel.send(response_text)
                else:
                    # Handle text response in DM
                    response = self.gemini_generate_content(msg.content)
                    dmchannel = await msg.author.create_dm()
                    await self.send_message_in_chunks(dmchannel, response)
        except Exception as e:
            await msg.channel.send(PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e))

    @commands.command()
    async def ask(self,ctx,question):
        try:
            response = self.gemini_generate_content(question)
            await self.send_message_in_chunks(ctx,response)
        except Exception as e:
            await ctx.send(PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e))

    @commands.command()
    async def dm(self,ctx):
        dmchannel = await ctx.author.create_dm()
        await dmchannel.send('Hi how can I help you today?')

    def gemini_generate_content(self,content):
        try:
            response = self.text_model.generate_content(content,stream=True)
            return response
        except Exception as e:
            return PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e)
        
        
    @commands.command()
    async def analyze(self, ctx, *, text=None):
        """Analyze an image and generate a response with text and an image."""
        try:
            # Check if the user attached an image
            if not ctx.message.attachments:
                await ctx.send("Please attach an image to analyze.")
                return

            # Download the image
            attachment = ctx.message.attachments[0]
            async with aiohttp.ClientSession() as session:
                async with session.get(attachment.url) as response:
                    image_data = await response.read()

            # Generate response with text and image
            response_text = await self.generate_response_with_image_and_text(image_data, text)

            # Send the response
            await ctx.send(response_text)

        except Exception as e:
            await ctx.send(PLEASE_TRY_AGAIN_ERROR_MESSAGE + str(e))
            
    @commands.command()
    async def generate_image(self, ctx, *,prompt):
        try:
            response = image_model.generate_content(prompt)
            if response._error:
                return await ctx.send(f"❌ Image generation failed: {str(response._error)}")
            if isinstance(response.output, list):
                image_data = response.output[0]["data"]
            else:
                image_data = response.output["data"]

            await ctx.send(file=File(io.BytesIO(image_data), filename="generated_image.jpg"))
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {str(e)}")

            
    async def generate_response_with_image_and_text(self, image_data, text):
        image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
        prompt_parts = [image_parts[0], f"\n{text if text else 'What is this a picture of?'}"]

        response = image_model.generate_content(prompt_parts)

        if response._error:
            return "❌" + str(response._error)

        return response.text
        
    async def send_message_in_chunks(self,ctx,response):
        message = ""
        for chunk in response:
            message += chunk.text
            if len(message) > DISCORD_MAX_MESSAGE_LENGTH:
                extraMessage = message[DISCORD_MAX_MESSAGE_LENGTH:]
                message = message[:DISCORD_MAX_MESSAGE_LENGTH]
                await ctx.send(message)
                message = extraMessage
        if len(message) > 0:
            while len(message) > DISCORD_MAX_MESSAGE_LENGTH:
                extraMessage = message[DISCORD_MAX_MESSAGE_LENGTH:]
                message = message[:DISCORD_MAX_MESSAGE_LENGTH]
                await ctx.send(message)
                message = extraMessage
            await ctx.send(message)
            
    async def download_image_from_url(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                image_data = await response.read()
        return image_data
         
async def setup(bot):
    await bot.add_cog(ai_integration(bot))