# match_manager.py
from queue_manager import form_teams, clear_active_match, reset_queue, add_player
from voice_text_channels import create_private_channels, delete_private_channels
from voting_system import start_map_voting, start_result_voting
import logging

async def start_match(bot, guild):
    team1, team2 = form_teams()
    if not team1:
        logging.warning("[Match] No hay suficientes jugadores.")
        return

    text_channel, voice1, voice2 = await create_private_channels(guild, team1, team2)

    state = {
        "team1": team1,
        "team2": team2,
        "text_channel": text_channel,
        "voice_channels": [voice1, voice2]
    }

    reset_queue()

    async def on_map_voted(winning_map, players, cancelled=False):
        if cancelled:
            logging.info("[Match] Votación de mapa cancelada, devolviendo jugadores a la cola.")
            for uid, name in team1 + team2:
                add_player(uid, name)
            return

        await text_channel.send(f"✅ Mapa confirmado: **{winning_map}**")
        await start_result_voting(text_channel, players, state)

    players_ids = [uid for uid, _ in team1 + team2]
    await start_map_voting(text_channel, players_ids, on_complete=on_map_voted)

    logging.info("[Match] Partida iniciada con state: %s", state)
    return state

async def end_match(state: dict):
    text_channel = state.get("text_channel")
    voice_channels = state.get("voice_channels", [])
    await delete_private_channels(text_channel, voice_channels)
    clear_active_match()
