import json
import sys
from os import path

KEYWORDS = ['scope', 'regex', 'nesting', 'watch_op', 'watch',
            'assume', 'ensure', 'require', 'strategy', 'check']


def read_file(file_path):
    file_path = path.join('.', file_path)
    assert path.exists(file_path), f"File {file_path} does not exist"

    with open(file_path) as fp:
        user_dsl = fp.read()

    return user_dsl


def formatting_v(k, v):
    """
    As each key word requires different types of v,
    we need to format v manually here
    """
    # if k is `nesting`, the v should be a int list
    if k == 'nesting':
        v = eval(v)
    # if k is `regex`, the v should be a bool
    if k == 'regex':
        v = eval(v)
    # if k is in need_string_list_keywords, the v should be a string list
    need_string_list_keywords = {
        'watch', 'strategy', 'check', 'assume', 'ensure', 'require'}
    if k in need_string_list_keywords:
        v = v[1:-1]  # remove [ and ]
        v = v.split(',')
        v = [i.strip() for i in v]

    return k, v


def check_predicate(one_rule):
    """
    This function checks:
    1. contains a predicate
    2. all the variables in predicate are watched
    """
    # determine if this dsl has and only has one predicate
    predicates_keyword = {'assume', 'ensure', 'require'}
    the_predicate = predicates_keyword.intersection(one_rule.keys())

    # if it has predicate, check watch
    if the_predicate:
        try:
            watched_vars = one_rule['watch']
        except KeyError:
            exit("Please ensure each dsl has `watch`ed variables")

        def clean_env(watched_vars, preds):
            valid_predicate = True
            # iter is a keyword, we have to override it
            def iter(x): pass

            for watched_var in watched_vars:
                exec(watched_var + "= 1")
            try:
                for pred in preds:
                    eval(pred)
            except NameError:
                # if the name is not declared, i.e., not watched
                valid_predicate = False
            return valid_predicate

        preds = one_rule[list(the_predicate)[0]]
        return clean_env(watched_vars, preds)
    else:
        # if there is no predicate, always valid predicate
        return True


def parse_dsl(user_dsl):
    # split by keyword: @dsl-rule and strip each one
    user_dsl_list = user_dsl.split('@dsl-rule')
    user_dsl_list = [i.strip() for i in user_dsl_list][1:]

    # for each @dsl-rule, extract key-value pair
    user_dsl_rules = []
    for each_user_dsl in user_dsl_list:
        one_rule = dict()
        key_value_pairs = each_user_dsl.split('\n')
        for k_v_pair in key_value_pairs:
            colon_index = k_v_pair.find(':')
            assert colon_index != -1, f"Invalid DSL rule! ({k_v_pair})"
            k, v = k_v_pair[:colon_index].strip(
            ), k_v_pair[colon_index+1:].strip()
            k, v = formatting_v(k, v)

            one_rule[k] = v
        # sort the dict by sequence in KEYWORDS
        sorted(one_rule.items(), key=lambda pair: KEYWORDS.index(pair[0]))

        # check semantic correctness of `assume`, `ensure` and `require`
        if not check_predicate(one_rule):
            exit(
                f"Not valid DSL, please check:\n------------------------\n{each_user_dsl}")

        user_dsl_rules.append(one_rule)

    return user_dsl_rules


def write_into_file(user_dsl_rules, file_path):
    # store the list in json format
    with open(file_path + '.json', 'w') as fp:
        json.dump(user_dsl_rules, fp, indent=4)
    print('Done')


if __name__ == '__main__':
    assert len(sys.argv) > 1, "Please input the file name"
    file_path = sys.argv[1]

    user_dsl = read_file(file_path)
    parsed_user_dsl = parse_dsl(user_dsl)
    write_into_file(parsed_user_dsl, file_path)
