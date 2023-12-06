import argparse
import time


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    time = [int(x) for x in data[0].split() if x.isdigit()]
    distance = [int(x) for x in data[1].split() if x.isdigit()]
    return time, distance


def calc_distance(hold, total):
    return hold * (total - hold)


def part_1(times, distances):
    beatings = 1
    for t, d in zip(times, distances):
        beatings *= len([i for i in range(1, t) if calc_distance(i, t) > d])
    return beatings


def part_2(times, distances):
    time = int(''.join([str(t) for t in times]))
    distance = int(''.join([str(d) for d in distances]))
    return len([i for i in range(1, time) if calc_distance(i, time) > distance])


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1 = part_1(*data)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = part_2(*data)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
