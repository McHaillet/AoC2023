import argparse
import time


class ScratchCard:
    def __init__(self, winning, drawn):
        self.winning = winning
        self.drawn = drawn
        self.copies = 1

    def add_copies(self, n):
        self.copies += n

    def get_matches(self):
        hits = [x for x in self.drawn if x in self.winning]
        return len(hits)


def read_file(fname):
    data = dict()
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                card_id, numbers = strip.split(':')
                winning, drawn = numbers.split('|')
                winning = [int(x) for x in winning.split()]
                drawn = [int(x) for x in drawn.split()]
                data[int(card_id.split()[1])] = ScratchCard(winning, drawn)
    return data


def part_1(data):
    result = 0
    for card in data.values():
        hits = card.get_matches()
        if hits > 0:
            result += 2 ** (hits - 1)
    return result


def part_2(data):
    for card_id, card in data.items():
        hits = card.get_matches()
        for i in range(1, hits + 1):
            if card_id + i in data.keys():
                data[card_id + i].add_copies(card.copies)
    return sum([c.copies for c in data.values()])



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
