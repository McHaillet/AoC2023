import argparse
import time


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                seq = [int(x) for x in strip.split()]
                data.append(seq)
    return data


def list_diff(a):
    return [y - x for x, y in zip(a[:-1], a[1:])]


def recurse_diff1(a):
    diff = list_diff(a)
    if all([x == 0 for x in diff]):
        return 0
    else:
        return diff[-1] + recurse_diff1(diff)


def part_1(data):
    total = 0
    for seq in data:
        total += seq[-1] + recurse_diff1(seq)
    return total


def recurse_diff2(a):
    diff = list_diff(a)
    if all([x == 0 for x in diff]):
        return 0
    else:
        return diff[0] - recurse_diff2(diff)


def part_2(data):
    total = 0
    for seq in data:
        total += seq[0] - recurse_diff2(seq)
    return total


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
