# bot.py
import discord
from discord.ext import commands, tasks
from config import DISCORD_TOKEN, LOBBY_CHANNEL_NAME
from ui_handler import QueueView
from match_manager import start_match
from queue_manager import is_ready, reset_queue
from utils import init_db
import logging

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

queue_view = None

@bot.event
async def on_ready():
    global queue_view
    logging.info(f"Bot conectado como {bot.user}")
    init_db()

    guild = discord.utils.get(bot.guilds)
    lobby = discord.utils.get(guild.text_channels, name=LOBBY_CHANNEL_NAME)
    if not lobby:
        lobby = await guild.create_text_channel(LOBBY_CHANNEL_NAME)

    embed = discord.Embed(
        title="🎮 Cola de Rankeds",
        description="No hay jugadores en la cola.",
        color=discord.Color.blue()
    )

    queue_view = QueueView(None)
    static_msg = await lobby.send(embed=embed, view=queue_view)
    queue_view.static_message = static_msg

    check_queue.start(guild)

@tasks.loop(seconds=5)
async def check_queue(guild):
    global queue_view
    if is_ready():
        state = await start_match(bot, guild)
        reset_queue()
        if queue_view:
            await queue_view.refresh_message()

bot.run(DISCORD_TOKEN)
