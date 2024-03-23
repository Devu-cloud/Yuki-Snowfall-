# config/config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Bot configuration
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_BOT_DESCRIPTION = "A multi-purpose Discord bot with AI integration, audio playback, and image analysis capabilities."


# AI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_CLOUD_API_KEY = os.getenv("GOOGLE_CLOUD_API_KEY")
WOLFRAM_ALPHA_APP_ID = os.getenv("WOLFRAM_ALPHA_APP_ID")

# Database configuration
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", 27017)
DATABASE_NAME = os.getenv("DATABASE_NAME", "discord_bot")

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "discord_bot.log")

# Audio configuration
AUDIO_DOWNLOAD_DIR = os.getenv("AUDIO_DOWNLOAD_DIR", "audio_downloads")
FFMPEG_PATH = os.getenv("FFMPEG_PATH", "/usr/bin/ffmpeg")

# Image analysis configuration
IMAGE_ANALYSIS_MODELS_DIR = os.getenv("IMAGE_ANALYSIS_MODELS_DIR", "image_models")