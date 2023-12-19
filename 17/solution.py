import argparse
import time
from functools import partial
from heapq import heappush, heappop


HEIGHT, WIDTH = 0, 0


def read_file(fname):
    global HEIGHT, WIDTH
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append([int(x) for x in strip])
    HEIGHT, WIDTH = len(data), len(data[0])
    return data


def generate_steps(grid, queue, start_r, start_c, move_r, move_c, start_heat=0, min_steps=1, max_steps=3):
    heat_sum = start_heat
    current_r, current_c = start_r, start_c
    for i in range(1, max_steps+1):
        current_r += move_r
        current_c += move_c
        if current_r < 0 or current_r >= HEIGHT:
            break
        if current_c < 0 or current_c >= WIDTH:
            break
        heat_sum += grid[current_r][current_c]
        if i >= min_steps:
            heappush(queue, (heat_sum, current_r, current_c, move_r, move_c))


def dijkstra(data, min_steps, max_steps):
    queue = []
    visited = set()
    generate_cart_specific = partial(generate_steps, min_steps=min_steps, max_steps=max_steps)
    generate_cart_specific(data, queue, 0, 0, 1, 0)  # go right
    generate_cart_specific(data, queue, 0, 0, 0, 1)  # go down
    visited.add((0, 0, 1, 0))
    visited.add((0, 0, 0, 1))
    while True:
        heat_loss, current_x, current_y, move_x, move_y = heappop(queue)
        if current_x == (HEIGHT - 1) and current_y == (WIDTH - 1):
            return heat_loss
        if (current_x, current_y, move_x, move_y) in visited:
            continue
        else:
            visited.add((current_x, current_y, move_x, move_y))
        if move_x != 0:  # go left right
            for step in (-1, 1):
                generate_cart_specific(data, queue, current_x, current_y, 0, step, start_heat=heat_loss)
        else:  # go up down
            for step in (-1, 1):
                generate_cart_specific(data, queue, current_x, current_y, step, 0, start_heat=heat_loss)


def part_1(data):
    return dijkstra(data, 1, 3)


def part_2(data):
    return dijkstra(data, 4, 10)


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
