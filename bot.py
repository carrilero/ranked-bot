import discord
from discord.ext import commands
import config
from ui_handler import create_queue_message  # Importamos la función que crea el mensaje de la cola

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user.name}')

    guild = discord.utils.get(bot.guilds)
    if not guild:
        print("❌ No se encontró ningún servidor.")
        return

    # Busca un canal de texto llamado "ranked-queue"
    channel = discord.utils.get(guild.text_channels, name="ranked-queue")

    if not channel:
        print("📢 Canal 'ranked-queue' no encontrado, creándolo...")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False)
        }
        channel = await guild.create_text_channel("ranked-queue", overwrites=overwrites)
    else:
        print("📢 Canal 'ranked-queue' ya existe.")

    # Envía el mensaje de la cola si no existe uno persistente
    messages = [message async for message in channel.history(limit=10)]
    if not any(msg.author == bot.user for msg in messages):
        await create_queue_message(channel, bot)
        print("✅ Mensaje de la cola creado.")
    else:
        print("ℹ️ Ya hay un mensaje del bot en el canal.")

# Aquí puedes añadir otros eventos o comandos que tu bot tenga

bot.run(config.TOKEN)
