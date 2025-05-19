import random
import logging

# Cola de jugadores: lista de tuplas (user_id, display_name)
player_queue = []
active_match = None


def add_player(user_id, display_name):
    """
    Añade un jugador a la cola si no está ya, guardando su ID y nombre.
    """
    if (user_id, display_name) not in player_queue:
        player_queue.append((user_id, display_name))
        logging.info(f"[Queue] Añadido {(user_id, display_name)}")
    else:
        logging.info(f"[Queue] {(user_id, display_name)} ya estaba en la cola")


def remove_player(user_id):
    """
    Elimina un jugador de la cola por su ID.
    """
    global player_queue
    original_len = len(player_queue)
    player_queue = [item for item in player_queue if item[0] != user_id]
    if len(player_queue) < original_len:
        logging.info(f"[Queue] Eliminado jugador {user_id}")
    else:
        logging.info(f"[Queue] Usuario {user_id} no estaba en la cola")


def get_queue():
    """
    Devuelve una copia de la lista de tuplas (user_id, display_name).
    """
    return player_queue.copy()


def is_ready():
    """
    Comprueba si hay al menos 2 jugadores (o ajustar según LOBBY size).
    """
    return len(player_queue) >= 2


def form_teams():
    """
    Forma dos equipos de igual tamaño a partir de los primeros jugadores en cola.
    """
    global active_match
    if is_ready():
        count = len(player_queue) // 2 * 2
        selected = [player_queue.pop(0) for _ in range(count)]
        random.shuffle(selected)
        half = count // 2
        team1 = selected[:half]
        team2 = selected[half:]
        active_match = (team1, team2)
        logging.info(f"[Match] Equipos creados: {team1} vs {team2}")
        return team1, team2
    return None, None


def get_active_match():
    """
    Devuelve los equipos de la partida activa.
    """
    return active_match


def clear_active_match():
    """
    Limpia la partida activa.
    """
    global active_match
    active_match = None

