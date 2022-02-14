import config
import checks
import numpy as np
import itertools as it
import pprint as pp


def determine_team_combos():
    number_of_teams = int(len(config.PLAYER_LIST) / config.TEAM_SIZE)
    team_combos = [[*i] for i in it.combinations(config.PLAYER_LIST, config.TEAM_SIZE)]
    print('Number of possible teams: ' + str(len(team_combos)))
    print('Determining all possible combinations of teams.')
    combo_team_combos = [i for i in it.combinations(team_combos, number_of_teams) if
                         len(set(it.chain(*i))) == len(list(it.chain(*i)))]
    return combo_team_combos


def fast_round(number):
    p = 10 ** config.DECIMAL_PLACES
    return int(number * p + 0.5) / p


def member_elos(members):
    return [sum(config.PLAYER_LIST[member]) / len(config.PLAYER_LIST[member]) for member in members]


def team_mean(members):
    return fast_round(sum(member_elos(members)) / len(member_elos(members)))


def team_stdev(members):
    return fast_round(np.std(np.array(member_elos(members))))


def iteration_mean_and_stdev(team_means):
    it_mean = fast_round(np.average(team_means))
    it_stdev = fast_round(np.std(team_means))
    return it_mean, it_stdev


def calculate_iteration_mean_stdev(combos):
    def calculate_team_mean_stdev(iteration):
        iteration_dict = {'Team ' + str(team + 1): {'Members': iteration[team],
                                                    'Elos': member_elos(iteration[team]),
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
    combo_iterations = determine_team_combos()
    print('Calculating all team combinations.')
    final_data = calculate_iteration_mean_stdev(combo_iterations)
    print('Number of Team Combinations: ' + str(len(final_data)))
    if config.PRINT_ALL_COMBINATIONS:
        print('---------===========All Iterations===========---------')
        pp.pprint(final_data, sort_dicts=False)
    if config.PRINT_BEST_COMBINATION:
        pp.pprint(find_best_iteration(final_data), sort_dicts=False)


if __name__ == '__main__':
    main()
