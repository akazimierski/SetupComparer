import json

def compare_setups(setup1_path, setup2_path):
    # internal functions
    def setup_iteration(setup_dict):
        for key, value in setup_dict.items():
            # it is list instead of dict, need seperate handling
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

    data1 = load_json_to_dict(setup1_path)
    data2 = load_json_to_dict(setup2_path)

    setup_keys = get_keys_list_from_setup_data(data1)
    setup1_values = get_values_dict_from_setup_data(data1)
    setup2_values = get_values_dict_from_setup_data(data2)

    diff_dict = {}
    i = 0
    while i < len(setup1_values):
        value_type = type(setup1_values[i])
        if value_type == str:
            # booloen information if compared setups are from the same car
            if setup1_values[i] == setup2_values[i]:
                diff_dict[setup_keys[i]] = True
            else:
                diff_dict[setup_keys[i]] = False
        if value_type == int or value_type == float:
            diff_dict[setup_keys[i]] = setup1_values[i] - setup2_values[i]
        if value_type == list:
            diff_dict[setup_keys[i]] = get_diff_list(setup1_values[i], setup2_values[i])
        i += 1

    return diff_dict
# compare_setups

def load_json_to_dict(file_path):
    with open(file_path) as setup1:
        result_dict = json.load(setup1)
    return result_dict
# load_json_to_dict

def save_dict_to_json(dict_to_save, file_path):
    with open(file_path, 'w') as fp:
        json.dump(dict_to_save, fp)
# save_dict_to_json

# main
setup_diff = compare_setups('setup_example1.json', 'setup_example2.json')
for x in setup_diff.items():
        print(x)
save_dict_to_json(setup_diff, 'diff.json')