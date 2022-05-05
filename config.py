import pandas as pd


def read_and_format_csv(filename):
    data = pd.read_csv(filename)
    elo_col_name = ['Unnamed: ' + str(i + 1) for i in range(NO_OF_ELOS)]
    data['Mean'] = data[elo_col_name].mean(axis=1)
    data = data[['Name', 'Mean']]
    return data.to_dict('index')


PLAYER_FILENAME = 'Data_Input.csv'
NO_OF_ELOS = 5
PLAYER_LIST = read_and_format_csv(PLAYER_FILENAME)
TEAM_SIZE = 3
DECIMAL_PLACES = 2

PRINT_ALL_COMBINATIONS = False
PRINT_BEST_COMBINATION = True
NUMBER_OF_BEST_PLAYERS_ALLOWED_ON_ANY_ONE_TEAM = 1
NUMBER_OF_WORST_PLAYERS_ALLOWED_ON_ANY_ONE_TEAM = 1
