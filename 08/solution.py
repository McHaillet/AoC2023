import argparse
import time
from functools import reduce
from math import lcm


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    instruction = data[0]
    node_map = dict()
    for d in data[1:]:
        key, values = d.split(' = ')
        node_map[key] = tuple([v.strip('()') for v in values.split(', ')])
    return instruction, node_map


def part_1(data):
    instruction_set = data[0]
    node_map = data[1]
    steps = 0
    current_index = 'AAA'
    while current_index != 'ZZZ':
        inst = instruction_set[steps % len(instruction_set)]
        if inst == 'R':
            current_index = node_map[current_index][1]
        elif inst == 'L':
            current_index = node_map[current_index][0]
        else:
            raise ValueError('Invalid instruction found')
        steps += 1
    return steps


def part_2(data):
    instruction_set = data[0]
    node_map = data[1]
    current_indices = [x for x in node_map.keys() if x[2] == 'A']
    cycle_ends = [None, ] * len(current_indices)
    steps = 0
    while any([ce is None for ce in cycle_ends]):
        inst = instruction_set[steps % len(instruction_set)]
        steps += 1
        if inst == 'R':
            current_indices = [
                node_map[ci][1] for ci in current_indices
            ]
        elif inst == 'L':
            current_indices = [
                node_map[ci][0] for ci in current_indices
            ]
        else:
            raise ValueError('Invalid instruction found')
        for i, ci in enumerate(current_indices):  # go through current indices to find if a cycle has ended
            if cycle_ends[i] is None and ci[2] == 'Z':
                cycle_ends[i] = steps
    return lcm(*cycle_ends)  # find least common multiple (lcm)


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
