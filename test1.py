import pprint as pp
import math
import concurrent.futures


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def multiply_all_previous(stuff, n):
    return math.prod(stuff[:n])


def setup_operations_queue(population_size, team_size):
    primes = prime_factors(int(population_size / team_size))

    operations = {}
    branch_no = 0
    for prime_no in range(len(primes)):
        prime = primes[prime_no]
        level_ops = {'completion_flag': False, 'data_input_flag': False}
        sub_branch_ops = []
        for branch in range(multiply_all_previous(primes, prime_no)):
            op_data = {
                'id': branch_no,
                'branch_data_input': [],
                'branch_data_output': [],
                'division_size': prime
            }
            sub_branch_ops.append(op_data)
            level_ops['sub_branch_ops'] = sub_branch_ops
            branch_no += 1
        operations[prime_no] = level_ops
    return operations


def detect_level_completion_flags(checking):
    list_of_dicts = [*checking.values()]
    if all(value['completion_flag'] for value in list_of_dicts):
        return True, len(list_of_dicts) - 1
    else:
        for i in range(len(list_of_dicts)):
            if not list_of_dicts[i]['completion_flag']:
                return False, i


def initial_data_input(data, initial_population):
    data[0]['sub_branch_ops'][0]['branch_data_input'] = initial_population
    data[0]['data_input_flag'] = True
    return data


def data_level_transferal(data):
    list_of_dicts = [*data.values()]
    if all(value['data_input_flag'] for value in list_of_dicts):
        return data
    else:
        for i in range(len(list_of_dicts)):
            if not list_of_dicts[i]['data_input_flag']:
                prelevel_data_list = data[i - 1]['sub_branch_ops']
                all_prelevel_data = []
                for prelevel_data in prelevel_data_list:
                    all_prelevel_data.extend(prelevel_data['branch_data_output'])
                for current_level_branch_op in range(len(all_prelevel_data)):
                    data[i]['sub_branch_ops'][current_level_branch_op]['branch_data_input'] = all_prelevel_data[
                        current_level_branch_op]
                data[i]['data_input_flag'] = True
                return data


def data_retrieve_process_return(data):
    list_of_dicts = [*data.values()]
    if all(value['completion_flag'] for value in list_of_dicts):
        return data
    else:
        for i in range(len(list_of_dicts)):
            if not list_of_dicts[i]['completion_flag']:
                prelevel_data_list = data[i]['sub_branch_ops']
                all_prelevel_data = []
                for prelevel_data in prelevel_data_list:
                    all_prelevel_data.append(prelevel_data['branch_data_input'])
                with concurrent.futures.ProcessPoolExecutor() as executor:
                    weird_results = [*executor.map(split_list, all_prelevel_data)]
                for result_no in range(len(weird_results)):
                    data[i]['sub_branch_ops'][result_no]['branch_data_output'] = weird_results[result_no]
                data[i]['completion_flag'] = True
                return data


def split_list(a_list):
    half = len(a_list) // 2
    return [a_list[:half], a_list[half:]]


if __name__ == '__main__':
    setup_dict = setup_operations_queue(population_size=24, team_size=3)

    # print(detect_level_completion_flags(setup_dict))

    setup_dict = initial_data_input(setup_dict, [1, 2, 3, 4, 5, 6, 7, 8])

    while not detect_level_completion_flags(setup_dict)[0]:
        setup_dict = data_retrieve_process_return(setup_dict)

        setup_dict = data_level_transferal(setup_dict)

    setup_dict = data_retrieve_process_return(setup_dict)
    pp.pprint(setup_dict, sort_dicts=False, compact=False)
