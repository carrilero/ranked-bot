player_que = []

def add_player(user):
    if user not in player_que:
        player_que.append(user)

def remove_player(user):
    if user in player_que:
        player_que.remove(user)

def get_que():
    return player_que

def can_start_match():
    return len(player_que) >= 4

def get_next_match():
    if can_start_match():
        return [player_que.pop(0) for _ in range(4)]
    return []
