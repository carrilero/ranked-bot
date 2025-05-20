from queue_manager import form_teams, get_active_match, clear_active_match
from voice_text_channels import create_private_channels, delete_private_channels
from voting_system import start_map_voting
import logging

async def start_match(bot, guild):
    team1, team2 = form_teams()
    if not team1:
        logging.warning("[Match] No hay suficientes jugadores.")
        return

    text_channel, voice1, voice2 = await create_private_channels(guild, team1, team2)
    await start_map_voting(bot, text_channel, team1 + team2)

    logging.info("[Match] Partida iniciada.")
    return {
        "team1": team1,
        "team2": team2,
        "text_channel": text_channel,
        "voice_channels": [voice1, voice2],
    }
async def end_match(state: dict):
    # state contiene team1, team2, text_channel, voice_channels
    text_channel = state["text_channel"]
    voice_channels = state["voice_channels"]

    # Elimina los canales
    await delete_private_channels(text_channel, voice_channels)

    # Limpia el estado
    clear_active_match()