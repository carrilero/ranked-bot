import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))  # opcional
QUEUE_SIZE = 8  # Número de jugadores para iniciar una partida

# Canales y roles (puedes adaptarlo a IDs fijos si lo prefieres)
LOBBY_CHANNEL_NAME = "ranked-lobby"
CATEGORY_NAME = "Partida Ranked"

# Votaciones
GAME_MODES = ["Punto Caliente", "Buscar y Destruir", "Control"]
MAPS = ["Mapa 1", "Mapa 2", "Mapa 3"]  # Personaliza según el juego
