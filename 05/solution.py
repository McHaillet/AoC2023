import argparse
import time


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    seeds = list(map(int, data[0].replace('seeds:', '').split()))
    maps = [[], ]
    map_id = 0
    for l in data[2:]:
        if l[0].isdigit():
            dest, source, offset = list(map(int, l.split()))
            maps[map_id].append(((source, source + offset), (dest, dest + offset)))
        else:
            maps.append([])
            map_id += 1
    [m.sort(key=lambda x: x[0][0]) for m in maps]
    return seeds, maps


def part_1(data):
    seeds, maps = data
    locations = []
    for s in seeds:
        current = s
        for m in maps:
            new = -1
            for conv in m:
                source, dest = conv
                if source[0] <= current <= source[-1]:
                    offset = current - source[0]
                    new = dest[0] + offset
                    break
            if new >= 0:
                current = new
        locations.append(current)
    return min(locations)


def eval_mapping(seed_range, mapping):
    """
    ranges are a tuple of two elements
    0 points to the start of the range
    1 points to the end of the range
    """
    new = []
    for conv in mapping:
        source, dest = conv
        if seed_range[1] <= source[0]:
            continue
        if seed_range[0] >= source[1]:
            continue
        else:
            if seed_range[0] < source[0]:
                new.append((seed_range[0], source[0]))
                if seed_range[1] < source[1]:
                    offset = source[1] - seed_range[1]
                    new.append((dest[0], dest[0] + offset))
                    break
                else:
                    new.append(dest)
                    seed_range = (source[1], seed_range[1])
            else:
                start = seed_range[0] - source[0]
                if seed_range[1] < source[1]:
                    offset = seed_range[1] - seed_range[0]
                    new.append((dest[0] + start, dest[0] + start + offset))
                    break
                else:
                    new.append((dest[0] + start, dest[1]))
                    seed_range = (source[1], seed_range[1])
    else:
        new.append(seed_range)
    return new


def part_2(data):
    seeds, maps = data
    lowest = None
    for seed, offset in zip(seeds[0::2], seeds[1::2]):
        seed_ranges = [(seed, seed + offset)]
        for x in maps:
            new_seed_ranges = []
            for s in seed_ranges:
                new_seed_ranges += eval_mapping(s, x)
            seed_ranges = new_seed_ranges
            # print(seed_ranges)
        if lowest is None:
            lowest = min([min(x) for x in seed_ranges])
        else:
            lowest = min(lowest, min([min(x) for x in seed_ranges]))
    return lowest


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
