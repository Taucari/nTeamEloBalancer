import config
import checks

import itertools as it
import pprint as pp
from statistics import mean, stdev


def determine_team_combos():
    team_combos = list(list(i) for i in it.combinations(config.PLAYER_LIST, config.TEAM_SIZE))
    c = [i for i in it.combinations(team_combos, int(len(config.PLAYER_LIST) / config.TEAM_SIZE)) if
         len(set(tuple(sum(i, [])))) == len(tuple(sum(i, [])))]
    return c


def calculate_iteration_mean_stdev(combos):
    def calculate_team_mean_stdev(iteration):
        def team_elos(members):
            return [config.PLAYER_LIST.get(member)
                    if len(config.PLAYER_LIST.get(member)) == 1
                    else mean(config.PLAYER_LIST.get(member))
                    for member in members]

        def team_mean(members):
            return round(mean(team_elos(members)), config.DECIMAL_PLACES)

        def team_stdev(members):
            return round(stdev(team_elos(members)), config.DECIMAL_PLACES)

        iteration_dict = {'Team ' + str(team + 1): {'Members': iteration[team],
                                                    'Elos': team_elos(iteration[team]),
                                                    'Team Mean': team_mean(iteration[team]),
                                                    'Team StDev': team_stdev(iteration[team])}
                          for team in range(len(iteration))}

        iteration_mean = round(mean([iteration_dict[team_no]['Team Mean']
                                     for team_no in iteration_dict]), config.DECIMAL_PLACES)
        iteration_stdev = round(stdev([iteration_dict[team_no]['Team Mean']
                                       for team_no in iteration_dict]), config.DECIMAL_PLACES)

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


if __name__ == '__main__':
    print('Commencing Checks.')
    checks.initialize()
    print('Determining all possible teams.')
    combo_iterations = determine_team_combos()
    print('Calculating all team combinations.')
    final_data = calculate_iteration_mean_stdev(combo_iterations)
    print('Number of Iterations: ' + str(len(final_data)))
    if config.PRINT_ALL_COMBINATIONS:
        print('---------===========All Iterations===========---------')
        pp.pprint(final_data, sort_dicts=False)
    if config.PRINT_BEST_COMBINATION:
        pp.pprint(find_best_iteration(final_data), sort_dicts=False)
