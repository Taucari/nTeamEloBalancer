import config


def check_player_number_multiple():
    if len(config.PLAYER_LIST) % config.TEAM_SIZE == 0:
        return True, 0
    else:
        return False, config.TEAM_SIZE - len(config.PLAYER_LIST) % config.TEAM_SIZE
