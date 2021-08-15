import re


def read_dsl_code():
    with open('./overflow-sample/dsl-overflow.go') as fp:
        dsl_go = fp.read()
    return dsl_go


def parse(code):
    # we only focus on four types of keywords, refer to `DSL-specificaion.pdf`
    found_properties = dict()
    assume_pattern = re.compile(r'^[\s]*?\/\/[ ]?@assume:[ ]?(.*);', re.M)
    ensure_pattern = re.compile(r'^[\s]*?\/\/[ ]?@ensure:[ ]?(.*);', re.M)
    require_pattern = re.compile(r'^[\s]*?\/\/[ ]?@require:[ ]?(.*);', re.M)
    forall_pattern = re.compile(r'^[\s]*?\/\/[ ]?@forall:[ ]?(.*);', re.M)

    found_properties["assume"] = re.findall(assume_pattern, code)
    found_properties["ensure"] = re.findall(ensure_pattern, code)
    found_properties["require"] = re.findall(require_pattern, code)
    found_properties["forall"] = re.findall(forall_pattern, code)

    print(found_properties)
    exit()


def main():
    dsl_go = read_dsl_code()
    parse(dsl_go)


if __name__ == "__main__":
    main()
