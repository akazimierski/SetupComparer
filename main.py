import json

def compare_setups(setup1_path, setup2_path):
    # internal functions
    def setup_iteration(setup_dict):
        for key, value in setup_dict.items():
            if type(value) == str:
                continue
            if key == 'pitStrategy':
                continue
            if isinstance(value, dict):
                for pair in setup_iteration(value):
                    yield(key, *pair)
            else:
                yield(key, value)

    def get_diff_list(list1, list2):
        result = []
        i = 0
        while i < len(list1):
            result.append(list1[i] - list2[i])
            i += 1
        return result

    def get_values_dict_from_setup_data(data):
        setup_values = {}
        i = 0
        for pair in setup_iteration(data):
            setup_values[i] = pair[-1]
            i += 1
        return setup_values

    def get_keys_list_from_setup_data(data):
        setup_keys = []
        for pair in setup_iteration(data):
            setup_keys.append(pair[-2])
        return setup_keys
    # end internal functions

    with open(setup1_path) as setup1:
        data1 = json.load(setup1)

    with open(setup2_path) as setup2:
        data2 = json.load(setup2)

    setup_keys = get_keys_list_from_setup_data(data1)
    setup1_values = get_values_dict_from_setup_data(data1)
    setup2_values = get_values_dict_from_setup_data(data2)

    diff_dict = {}
    i = 0
    while i < len(setup1_values):
        value_type = type(setup1_values[i])
        if value_type == int or value_type == float:
            diff_dict[setup_keys[i]] = setup1_values[i] - setup2_values[i]
        if value_type == list:
            diff_dict[setup_keys[i]] = get_diff_list(setup1_values[i], setup2_values[i])
        i += 1

    return diff_dict
# compare_setups

# main
setup_diff = compare_setups('aggr.json', 'CDA_M4_MON_Q01.json')
for x in setup_diff.items():
        print(x)