# bot.py
import discord
from discord.ext import commands, tasks
from config import DISCORD_TOKEN, LOBBY_CHANNEL_NAME
from ui_handler import QueueView
from match_manager import start_match
from queue_manager import is_ready, get_queue
from utils import init_db            # ← Importa la función
import logging
from ui_handler import QueueView

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

    # —    Aquí reemplazamos el envío simple por nuestro embed + QueueView —
    # 1. Creamos el embed inicial (sin jugadores)
    embed = discord.Embed(
        title="🎮 Cola de Rankeds",
        description="No hay jugadores en la cola.",
        color=discord.Color.blue()
    )
    # 2. Enviamos el mensaje y capturamos el objeto
    static_msg = await lobby.send(embed=embed, view=QueueView(None))
    # 3. Asignamos la referencia al view para que pueda editarse
    static_msg.view.static_message = static_msg

    # Arranca el loop que revisa la cola
    check_queue.start(guild)

@tasks.loop(seconds=5)
async def check_queue(guild):
    if is_ready():
        await start_match(bot, guild)

bot.run(DISCORD_TOKEN)
