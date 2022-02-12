import config
import sys


def check_more_than_one_team():
    if len(config.PLAYER_LIST) >= config.TEAM_SIZE:
        return True
    else:
        return False


def check_player_number_multiple():
    if len(config.PLAYER_LIST) % config.TEAM_SIZE == 0:
        return True, 0
    else:
        return False, config.TEAM_SIZE - len(config.PLAYER_LIST) % config.TEAM_SIZE


def initialize():
    if not check_more_than_one_team():
        sys.exit("You don't have enough players. Please add more.")

    player_multiple_check, players_remaining = check_player_number_multiple()
    if player_multiple_check:
        print('Great! You have all the contestants needed for this program to work')
    else:
        if players_remaining == 1:
            sys.exit('You have to add ' + str(players_remaining) + ' more contestant to make equal teams of ' + str(
                config.TEAM_SIZE) + '.')
        else:
            sys.exit('You have to add ' + str(players_remaining) + ' more contestants to make equal teams of ' + str(
                config.TEAM_SIZE) + '.')
