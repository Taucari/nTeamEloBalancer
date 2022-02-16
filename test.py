import itertools as it
import pprint
import concurrent.futures

import ppprint


def new_determine_team_combos(player_list, team_size):
    number_of_teams = int(len(player_list) / team_size)
    team_combos = [[*i] for i in it.combinations(player_list, team_size)]
    print('Number of possible teams: ' + str(len(team_combos)))
    print('Determining all possible combinations of teams.')
    output = {}

    for team_combo_no in range(len(team_combos)):
        new_team_combos = [*team_combos]
        head = new_team_combos[team_combo_no]
        del new_team_combos[team_combo_no]
        tail = [actual_combos for actual_combos in new_team_combos if set(head).isdisjoint(set(actual_combos))]
        output[tuple(head)] = tail
    return output


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
    output = {}
    done = 0
    for k, v in input_dict.items():
        output[k] = [[*i] for i in it.combinations(v, 4) if
                     len(set(it.chain(*i))) == len(list(it.chain(*i)))]
        done += 1
        print('Done ' + str(done))
    output_list = []
    for k, v in output.items():
        for micro_combo in v:
            head = [[*k]]
            head.extend(micro_combo)
            output_list.append(head)
    return output_list


def handle_multi():
    # players = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
    size = 3
    players = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

    new_result = new_determine_team_combos(players, size)
    sectioned_result = split_dict_equally(new_result, chunks=20)
    final_result = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(multifunction, sectioned_result)

        for result in results:
            final_result.extend(result)

    print('Number of possible combinations of teams: ' + str(len(final_result)))
    pprint.pprint(final_result[0:5])


if __name__ == '__main__':
    handle_multi()
