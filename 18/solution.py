import argparse
import time
import operator


def parse_instructions(data):
    sets = {}
    for line in data:
        name, instruct = line.split('{')
        instruction_set = []
        for rule in instruct.strip('}').split(','):
            if ':' in rule:
                comp, out = rule.split(':')
                if '>' in comp:
                    x, y = comp.split('>')
                    op = operator.gt
                if '<' in comp:
                    x, y = comp.split('<')
                    op = operator.lt
                instruction_set.append([x, op, int(y), out])
            else:
                instruction_set.append([rule])
        sets[name] = instruction_set
    return sets


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    gears = [eval(x.
              replace('x', "'x'").
              replace('s', "'s'").
              replace('m', "'m'").
              replace('a', "'a'").
              replace('=', ':')) for x in data if x.startswith('{')]
    instructions = parse_instructions([x for x in data if not x.startswith('{')])
    return gears, instructions


def run_instruction(gear, rule):
    for r in rule:
        if len(r) == 1:
            return r[0]
        elif r[1](gear[r[0]], r[2]):
            return r[3]


def part_1(data):
    g, i = data
    accepted = 0
    for x in g:
        res = run_instruction(x, i['in'])
        while True:
            res = run_instruction(x, i[res])  # eval next instruction
            if res == 'R':
                break
            if res == 'A':
                accepted += sum(x.values())
                break
    return accepted


def part_2(data):
    pass


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1 = part_1(data)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = part_2(data)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
