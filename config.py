import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))  # opcional
QUEUE_SIZE = 2  # Número de jugadores para iniciar una partida

# Canales y roles (puedes adaptarlo a IDs fijos si lo prefieres)
LOBBY_CHANNEL_NAME = "ranked-lobby"
CATEGORY_NAME = "Partida Ranked"

# Votaciones
MAPS = ["Hacienda", "Red Card", "Rewind", "Skyline", "Vault"]  # Personaliza según el juego
