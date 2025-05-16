player_queue = []

def add_player(user):
    if user not in player_queue:
        player_queue.append(user)

def remove_player(user):
    if user in player_queue:
        player_queue.remove(user)

def get_queue():
    return player_queue

def can_start_match():
    return len(player_queue) >= 4

def get_next_match():
    if can_start_match():
        return [player_queue.pop(0) for _ in range(4)]
    return []
