import pprint

import config
import checks
import numpy as np
import itertools as it
import pprint as pp
import concurrent.futures


def determine_team_combos():
    number_of_teams = int(len(config.PLAYER_LIST) / config.TEAM_SIZE)
    highest_players = determine_best_players(number_of_teams)
    lowest_players = determine_worst_players(number_of_teams)
    team_combos = [[*i] for i in it.combinations(config.PLAYER_LIST.keys(), config.TEAM_SIZE)
                   # Omit teams containing more than a certain number of the best players
                   if len(set(highest_players).intersection(i)) <=
                   config.NUMBER_OF_BEST_PLAYERS_ALLOWED_ON_ANY_ONE_TEAM
                   # Omit teams containing more than a certain number of the worst players
                   if len(set(lowest_players).intersection(i)) <=
                   config.NUMBER_OF_WORST_PLAYERS_ALLOWED_ON_ANY_ONE_TEAM]
    print('Number of player combos for teams: ' + str(len(team_combos)))
    print('Determining all possible combinations of teams.')

    output = {}
    for team_combo_no in range(len(team_combos)):
        new_team_combos = [*team_combos]
        head = new_team_combos[team_combo_no]
        del new_team_combos[team_combo_no]
        tail = [actual_combos for actual_combos in new_team_combos if set(head).isdisjoint(set(actual_combos))]
        output[tuple(head)] = tail

    pp.pprint(output)
    return output


def determine_best_players(no_team):
    return sorted(config.PLAYER_LIST.keys(), key=lambda k: sum(config.PLAYER_LIST[k]) / len(config.PLAYER_LIST[k]),
                  reverse=True)[-no_team:]


def determine_worst_players(no_team):
    return sorted(config.PLAYER_LIST.keys(), key=lambda k: sum(config.PLAYER_LIST[k]) / len(config.PLAYER_LIST[k]),
                  reverse=False)[-no_team:]


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


def split_dict_equally(input_dict, chunks=2):
    """Splits dict by keys. Returns a list of dictionaries."""
    # prep with empty dicts
    return_list = [dict() for _ in range(chunks)]
    idx = 0
    for k, v in input_dict.items():
        return_list[idx][k] = v
        if idx < chunks - 1:  # indexes start at 0
            idx += 1
        else:
            idx = 0
    return return_list


def multifunction(input_dict):
    number_of_teams = int(len(config.PLAYER_LIST) / config.TEAM_SIZE)
    print(number_of_teams)
    print('Starting Combination Calculation')
    output = {}
    done = 0
    for k, v in input_dict.items():
        print(k)
        output[k] = [[*i] for i in it.combinations(v, 3) if
                     len(set(it.chain(*i))) == len(list(it.chain(*i)))]
        done += 1
        print('Done ' + str(done))
    print('Ending Combination Calculation')
    print('Processing Results')
    output_list = []
    for k, v in output.items():
        for micro_combo in v:
            head = [[*k]]
            head.extend(micro_combo)
            output_list.append(head)
    print('Finished Results Processing')
    return output_list


def main():
    print('Commencing Checks.')
    checks.initialize()
    print('Determining all possible teams.')
    combo_iterations = determine_team_combos()
    print('Splitting into multiple sections.')
    sectioned_result = split_dict_equally(combo_iterations, chunks=20)
    print('Calculating all team combinations.')
    final_result = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        print('Starting Processes')
        results = executor.map(multifunction, sectioned_result)
        print('Finished Starting Processes')
        for result in results:
            final_result.extend(result)

    final_data = calculate_iteration_mean_stdev(final_result)
    print('Number of Team Combinations: ' + str(len(final_data)))
    if config.PRINT_ALL_COMBINATIONS:
        print('---------===========All Iterations===========---------')
        pp.pprint(final_data, sort_dicts=False)
    if config.PRINT_BEST_COMBINATION:
        pp.pprint(find_best_iteration(final_data), sort_dicts=False)


if __name__ == '__main__':
    main()
