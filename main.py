import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

# Last inn miljøvariabler fra .env-filen
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Sett opp logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sett opp intents for boten
intents = discord.Intents.default()
intents.message_content = True

# Bruk et fleksibelt prefikssystem som lar boten også reagere på @mentions
bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), intents=intents)

# Når boten er klar og innlogget
@bot.event
async def on_ready():
    logger.info(f"✅ Logged in as {bot.user}")

# Last inn alle kommandomoduler (cogs) ved oppstart med feilhåndtering
@bot.event
async def setup_hook():
    extensions = [
        "commands.commands_help",
        "commands.music_player",
        "commands.weather",
        "commands.nyheter",
        "commands.travel_planner",
        "commands.uke",
        "commands.google"
    ]
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f"📦 Lastet inn: {extension}")
        except Exception as e:
            logger.error(f"❌ Kunne ikke laste inn {extension}: {e}")

# Start boten med feilhåndtering
if TOKEN:
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.error(f"🚨 En feil oppstod: {e}")
else:
    logger.error("❌ DISCORD_TOKEN mangler i .env-filen")
