import argparse
import time


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    return data


def check_valid_part_1(data, row_id, c1, c2):
    symbols = []
    for x in [-1, 0, 1]:
        if row_id + x < 0 or row_id + x >= len(data):
            continue
        for y in range(c1 - 1, c2 + 1):
            if y < 0 or y >= len(data[0]):
                continue
            element = data[row_id + x][y]
            if not element.isdigit() and not element == '.':
                symbols.append(element)
    return len(symbols) > 0


def check_valid_part_2(data, row_id, c1, c2):
    symbols = []
    for x in [-1, 0, 1]:
        if row_id + x < 0 or row_id + x >= len(data):
            continue
        for y in range(c1 - 1, c2 + 1):
            if y < 0 or y >= len(data[0]):
                continue
            element = data[row_id + x][y]
            if element == '*':
                return (element, row_id + x, y)
    return None


def part_1(data):
    total = 0
    for k, row in enumerate(data):
        i = 0
        while i < len(row):
            if row[i].isdigit():
                j = i + 1
                while j < len(row) and row[j].isdigit():
                    j += 1
                if check_valid_part_1(data, k, i, j):
                    total += int(row[i: j])
                i = j
            else:
                i += 1
    return total


def part_2(data):
    total = []
    for k, row in enumerate(data):
        i = 0
        while i < len(row):
            if row[i].isdigit():
                j = i + 1
                while j < len(row) and row[j].isdigit():
                    j += 1
                res = check_valid_part_2(data, k, i, j)
                if res is not None:
                    total.append((int(row[i: j]), res))
                i = j
            else:
                i += 1
    # start finding matches
    gear = 0
    while len(total) != 0:
        first = total.pop(0)
        for i, t in enumerate(total):
            if first[1] == t[1]:
                second = total.pop(i)
                gear += (first[0] * second[0])
                break
    return gear


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
