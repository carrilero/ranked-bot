from queue_manager import form_teams, get_active_match, clear_active_match, reset_queue
from voice_text_channels import create_private_channels, delete_private_channels
from voting_system import start_map_voting, start_result_voting
import logging

async def start_match(bot, guild):
    """
    Inicia una partida cuando la cola esté lista.
    Crea canales privados, lanza votación de mapas y gestiona la transición a la votación final.
    """
    # Formar equipos
    team1, team2 = form_teams()
    if not team1:
        logging.warning("[Match] No hay suficientes jugadores.")
        return

    # Crear canales de texto y voz privados
    text_channel, voice1, voice2 = await create_private_channels(guild, team1, team2)

    # Callback cuando termine la votación de mapas
    async def on_map_voted(winning_map, players, cancelled=False):
        if cancelled:
            logging.info("[Match] Votación de mapa cancelada, devolviendo jugadores a la cola.")
            from queue_manager import add_player
            # Devolver manualmente a la cola
            for uid, name in players:
                add_player(uid, name)
            return

        # Confirmar mapa elegido
        await text_channel.send(f"✅ Mapa confirmado: **{winning_map}**")
        # Iniciar votación de resultado
        await start_result_voting(text_channel, players, state)

    # Iniciar votación de mapas
    # Pasamos la lista de tuplas (id, name) para la cola, pero la votación usa solo ids
    players_ids = [uid for uid, _ in team1 + team2]
    reset_queue()
    await start_map_voting(text_channel, players_ids, on_complete=on_map_voted)

    logging.info("[Match] Partida iniciada.")
    return {
        "team1": team1,
        "team2": team2,
        "text_channel": text_channel,
        "voice_channels": [voice1, voice2],
    }

async def end_match(state: dict):
    """
    Finaliza la partida eliminando canales y limpiando el estado interno.
    """
    text_channel = state.get("text_channel")
    voice_channels = state.get("voice_channels", [])

    # Elimina los canales de la partida
    await delete_private_channels(text_channel, voice_channels)
    # Limpia el estado de la partida activa
    clear_active_match()
