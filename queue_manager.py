import random
import logging

player_queue = []
active_match = None

def add_player(user_id):
    if user_id not in player_queue:
        player_queue.append(user_id)
        logging.info(f"[Queue] Añadido {user_id}")
    else:
        logging.info(f"[Queue] {user_id} ya estaba en la cola")

def remove_player(user_id):
    if user_id in player_queue:
        player_queue.remove(user_id)
        logging.info(f"[Queue] Eliminado {user_id}")
    else:
        logging.info(f"[Queue] {user_id} no estaba en la cola")

def get_queue():
    return player_queue.copy()

def is_ready():
    return len(player_queue) >= 2

def form_teams():
    global active_match
    if is_ready():
        selected = [player_queue.pop(0) for _ in range(2)]
        random.shuffle(selected)
        team1, team2 = [selected[0]], [selected[1]]
        active_match = (team1, team2)
        logging.info(f"[Match] Equipos creados: {team1} vs {team2}")
        return team1, team2
    return None, None

def get_active_match():
    return active_match

def clear_active_match():
    global active_match
    active_match = None
