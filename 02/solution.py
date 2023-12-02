import argparse
import time
from functools import reduce


def read_file(fname):
    data = dict()
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                game, outcome = strip.split(':')
                game_index = int(game.split(' ')[1])
                data[game_index] = []
                draws = [draw.split(',') for draw in outcome.split(';')]
                for d in draws:
                    data[game_index].append({y[1]: int(y[0]) for y in [x.strip().split(' ') for x in d]})
    return data


def game_max(game):
    result = {'green': 0, 'red': 0, 'blue': 0}
    for draw in game:
        for color, count in draw.items():
            if count > result[color]:
                result[color] = count
    return result


def part_1(data, game_limit):
    total = 0
    for game_id, outcome in data.items():
        game_score = game_max(outcome)
        if all([game_score[k] <= game_limit[k] for k in game_limit.keys()]):
            total += game_id
    return total


def part_2(data):
    total = 0
    for game_id, outcome in data.items():
        game_score = game_max(outcome)
        total += reduce(lambda x, y: x * y, game_score.values())
    return total


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1 = part_1(data, {'red': 12, 'green': 13, 'blue': 14})
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
