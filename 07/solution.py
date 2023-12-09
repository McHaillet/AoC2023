import argparse
import time
from collections import Counter  # thanks sroet


CARDS1 = [
    'A',
    'K',
    'Q',
    'J',
    'T',
    '9',
    '8',
    '7',
    '6',
    '5',
    '4',
    '3',
    '2',
]
CARDS_TO_VALUES1 = {x: i for i, x in enumerate(CARDS1)}
CARDS2 = [
    'A',
    'K',
    'Q',
    'J',
    'T',
    '9',
    '8',
    '7',
    '6',
    '5',
    '4',
    '3',
    '2',
    'J'
]
CARDS_TO_VALUES2 = {x: i for i, x in enumerate(CARDS2)}


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                hand, bid = strip.split()
                data.append((hand, int(bid)))
    return data


def hand_value1(hand):
    count = Counter(hand)
    n = [c[1] for c in count.most_common(2)]
    if 5 in n:
        return 0
    elif 4 in n:
        return 1
    elif 2 in n and 3 in n:
        return 2
    elif 3 in n:
        return 3
    elif n.count(2) == 2:
        return 4
    elif 2 in n:
        return 5
    else:  # find the highest card
        return 6


def part_1(data):
    sorted_hands = sorted(data, key=lambda x: (
        hand_value1(x[0]),  # first index is the hand value
        [CARDS_TO_VALUES1[c] for c in x[0]]  # second index should compare cards if hands are equal
    ), reverse=True)
    return sum([(i + 1) * x[1] for i, x in enumerate(sorted_hands)])


def hand_value2(hand):
    count = Counter(hand)
    n_jokers = count['J']
    del count['J']
    if n_jokers == 5:
        return 0
    n = [c[1] for c in count.most_common(2)]
    n[0] += n_jokers  # add number of jokers to highest count to get optimal hand!
    if 5 in n:
        return 0
    elif 4 in n:
        return 1
    elif 2 in n and 3 in n:
        return 2
    elif 3 in n:
        return 3
    elif n.count(2) == 2:
        return 4
    elif 2 in n:
        return 5
    else:  # find the highest card
        return 6


def part_2(data):
    sorted_hands = sorted(data, key=lambda x: (
        hand_value2(x[0]),  # first index is the hand value
        [CARDS_TO_VALUES2[c] for c in x[0]]  # second index should compare cards if hands are equal
    ), reverse=True)
    return sum([(i + 1) * x[1] for i, x in enumerate(sorted_hands)])


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
