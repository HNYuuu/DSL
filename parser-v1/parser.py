import re
import argparse

PRE_DEFINED_PATTERN = """if !(%s) {
    panic("against: %s")
}"""

PRE_DEFINED_FORALL_PATTERN = """for _, %s := range %s {
    if !(%s) {
        panic("against: %s")
    }
}"""


def write_parsed_go(path, code):
    with open(path, 'w') as fp:
        fp.write(code)


def insert_assume(i, code_lines, pattern):
    assert i+1 < len(code_lines)
    assert re.match(r"func [^\W\d][\w]*\(.*\).*\{", code_lines[i+1])
    code_lines.insert(i+2, PRE_DEFINED_PATTERN % (pattern, pattern))
    return code_lines


def insert_ensure(i, code_lines, pattern):
    parenthesis_stack = 1
    for j in range(i+1, len(code_lines)):
        if '{' in code_lines[j]:
            parenthesis_stack += 1
        if '}' in code_lines[j]:
            parenthesis_stack -= 1
        if parenthesis_stack == 0:
            break
    code_lines.insert(j-1, PRE_DEFINED_PATTERN % (pattern, pattern))
    return code_lines


def insert_require(i, code_lines, pattern):
    code_lines.insert(i+1, PRE_DEFINED_PATTERN % (pattern, pattern))
    return code_lines


def insert_forall(i, code_lines, pattern):
    match_result = re.match(r'([^\W\d][\w]*) ?\$ ?(.*)', pattern)
    iterate_var, predicate = match_result.group(1), match_result.group(2)
    code_lines.insert(i+1, PRE_DEFINED_FORALL_PATTERN %
                      ("_el", iterate_var, predicate, pattern))  # TODO auto extract "_el" from ele
    return code_lines


def parse(code):
    # we only focus on four types of keywords, refer to `DSL-specificaion.pdf`
    assume_pattern = re.compile(r'^[\s]*?\/\/[ ]?@assume:[ ]?(.*);', re.M)
    ensure_pattern = re.compile(r'^[\s]*?\/\/[ ]?@ensure:[ ]?(.*);', re.M)
    require_pattern = re.compile(r'^[\s]*?\/\/[ ]?@require:[ ]?(.*);', re.M)
    forall_pattern = re.compile(r'^[\s]*?\/\/[ ]?@forall:[ ]?(.*);', re.M)

    # split the code line by line
    code_lines = code.split('\n')
    i = 0
    while i < len(code_lines):
        code_line = code_lines[i]
        if re.match(assume_pattern, code_line):
            code_lines = insert_assume(i, code_lines, re.match(
                assume_pattern, code_line).group(1))
            i += 2
        elif re.match(ensure_pattern, code_line):
            code_lines = insert_ensure(i, code_lines, re.match(
                ensure_pattern, code_line).group(1))
        elif re.match(require_pattern, code_line):
            code_lines = insert_require(i, code_lines, re.match(
                require_pattern, code_line).group(1))
            i += 1
        elif re.match(forall_pattern, code_line):
            code_lines = insert_forall(i, code_lines, re.match(
                forall_pattern, code_line).group(1))
            i += 1
        i += 1

    return '\n'.join(code_lines)


def main():
    parser = argparse.ArgumentParser(
        description='DSL Parser')
    inputs = parser.add_argument_group('Input arguments')
    inputs.add_argument('-f', '--file',
                        type=argparse.FileType('r'),
                        help='file path of to be parsed file')
    args = parser.parse_args()

    if not args.file:
        exit("Please input path of the to be parsed file")

    dsl_go = args.file.read()
    parsed_go = parse(dsl_go)

    # append a `parsed` before extension name
    target_path = args.file.name[:args.file.name.rfind(
        '.')] + '-parsed' + args.file.name[args.file.name.rfind('.'):]
    write_parsed_go(target_path, parsed_go)
    print('[!] Done!')


if __name__ == "__main__":
    main()
