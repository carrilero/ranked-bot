# bot.py
import discord
from discord.ext import commands, tasks
from config import DISCORD_TOKEN, LOBBY_CHANNEL_NAME
from ui_handler import QueueView
from match_manager import start_match
from queue_manager import is_ready
from utils import init_db            # ← Importa la función
import logging

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f"Bot conectado como {bot.user}")

    # Inicializa las tablas antes de cualquier otra cosa
    init_db()

    guild = discord.utils.get(bot.guilds)
    lobby = discord.utils.get(guild.text_channels, name=LOBBY_CHANNEL_NAME)
    if not lobby:
        lobby = await guild.create_text_channel(LOBBY_CHANNEL_NAME)

    view = QueueView(bot)
    await lobby.send(content="**Cola de rankeds:** 0/8 jugadores", view=view)

    # Arranca el loop que revisa la cola
    check_queue.start(guild)

@tasks.loop(seconds=5)
async def check_queue(guild):
    if is_ready():
        await start_match(bot, guild)

bot.run(DISCORD_TOKEN)
