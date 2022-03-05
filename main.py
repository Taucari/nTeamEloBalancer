import config
import checks
import numpy as np
import itertools as it
import pprint as pp


def determine_team_combos():
    number_of_teams = int(len(config.PLAYER_LIST) / config.TEAM_SIZE)
    highest_players = determine_best_players(number_of_teams)
    lowest_players = determine_worst_players(number_of_teams)
    team_combos = [list(i) for i in it.combinations(config.PLAYER_LIST, config.TEAM_SIZE)
                   # Omit teams containing more than a certain number of the best players
                   if len(set(highest_players).intersection(i)) <=
                   config.NUMBER_OF_BEST_PLAYERS_ALLOWED_ON_ANY_ONE_TEAM
                   # Omit teams containing more than a certain number of the worst players
                   if len(set(lowest_players).intersection(i)) <=
                   config.NUMBER_OF_WORST_PLAYERS_ALLOWED_ON_ANY_ONE_TEAM]
    print('Number of player combos for teams: ', str(len(team_combos)))
    return team_combos


def determine_combos_of_team_combos(team_combos):
    number_of_teams = int(len(config.PLAYER_LIST) / config.TEAM_SIZE)
    combos_of_team_combos = [i for i in it.combinations(team_combos, number_of_teams) if
                             len(set(it.chain(*i))) == len(list(it.chain(*i)))]
    return combos_of_team_combos


def determine_best_players(no_team):
    return sorted(config.PLAYER_LIST, key=lambda k: config.PLAYER_LIST[k]['Mean'],
                  reverse=True)[-no_team:]


def determine_worst_players(no_team):
    return sorted(config.PLAYER_LIST, key=lambda k: config.PLAYER_LIST[k]['Mean'],
                  reverse=False)[-no_team:]


def fast_round(number):
    p = 10 ** config.DECIMAL_PLACES
    return int(number * p + 0.5) / p


def retrieve_member_elos(members):
    return [config.PLAYER_LIST[member]['Mean']
            for member in members]


def retrieve_player_name(player_ids):
    return [config.PLAYER_LIST[id]['Name'] for id in player_ids]


def team_mean(members):
    return fast_round(np.average(retrieve_member_elos(members)))


def team_stdev(members):
    return fast_round(np.std(retrieve_member_elos(members)))


def iteration_mean_and_stdev(team_means):
    it_mean = fast_round(np.average(team_means))
    it_stdev = fast_round(np.std(team_means))
    return it_mean, it_stdev


def calculate_iteration_mean_stdev(combos):
    def calculate_team_mean_stdev(iteration):
        iteration_dict = {'Team ' + str(team + 1): {'Members': retrieve_player_name(iteration[team]),
                                                    'Elos': retrieve_member_elos(iteration[team]),
                                                    'Team Mean': team_mean(iteration[team]),
                                                    'Team StDev': team_stdev(iteration[team])}
                          for team in range(len(iteration))}

        iteration_mean, iteration_stdev = iteration_mean_and_stdev([iteration_dict[team_no]['Team Mean']
                                                                    for team_no in iteration_dict])

        iteration_dict['Iteration Team Elo Mean'] = iteration_mean
        iteration_dict['Iteration Team Elo StDev'] = iteration_stdev
        return iteration_dict

    return {'Iteration ' + str(iteration_no + 1): calculate_team_mean_stdev(combos[iteration_no])
            for iteration_no in range(len(combos))}


def find_best_iteration(data):
    print('---------===========Best Iteration===========---------')
    min_iteration_elo_stdev = min([data[i]['Iteration Team Elo StDev'] for i in data])
    for i in data:
        if data[i]['Iteration Team Elo StDev'] == min_iteration_elo_stdev:
            return data[i]


def main():
    print('Commencing Checks.')
    checks.initialize()
    print('Determining all possible teams.')
    combo_teams = determine_team_combos()
    print('Calculating all team combinations.')
    combo_iterations = determine_combos_of_team_combos(combo_teams)
    final_data = calculate_iteration_mean_stdev(combo_iterations)
    print('Number of Iterations: ' + str(len(final_data)))
    if config.PRINT_ALL_COMBINATIONS:
        print('---------===========All Iterations===========---------')
        pp.pprint(final_data, sort_dicts=False)
    if config.PRINT_BEST_COMBINATION:
        pp.pprint(find_best_iteration(final_data), sort_dicts=False)


if __name__ == '__main__':
    main()
