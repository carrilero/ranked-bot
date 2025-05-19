from queue_manager import form_teams, get_active_match, clear_active_match
from voice_text_channels import create_private_channels
from voting_system import start_mode_voting
import logging

async def start_match(bot, guild):
    team1, team2 = form_teams()
    if not team1:
        logging.warning("[Match] No hay suficientes jugadores.")
        return

    text_channel, voice1, voice2 = await create_private_channels(guild, team1, team2)
    await start_mode_voting(bot, text_channel, team1 + team2)

    logging.info("[Match] Partida iniciada.")
    return {
        "team1": team1,
        "team2": team2,
        "text_channel": text_channel,
        "voice_channels": [voice1, voice2],
    }
