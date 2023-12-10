import argparse
import time
from queue import Queue


PIPE_MOVES = {
    '|': (-1, 1),
    '-': (-1j, 1j),
    'L': (-1, 1j),
    'J': (-1, -1j),
    '7': (1, -1j),
    'F': (1, 1j),
}


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    return data


def get_symbol(pipe_map, loc):
    if loc.real < 0 or loc.real >= len(pipe_map):
        return None
    elif loc.imag < 0 or loc.imag >= len(pipe_map[0]):
        return None
    return pipe_map[int(loc.real)][int(loc.imag)]


def find_start(data):
    start = None
    for i, d in enumerate(data):
        if 'S' in d:
            j = d.index('S')
            start = i + j * 1j
            break
    up = get_symbol(data, start - 1)
    down = get_symbol(data, start + 1)
    left = get_symbol(data, start - 1j)
    right = get_symbol(data, start + 1j)
    down_valid = down is not None and down in '|LJ'
    right_valid = right is not None and right in '-7J'
    left_valid = left is not None and left in '-FL'
    up_valid = up is not None and up in '|F7'
    start_symbol = ''
    match (up_valid, down_valid, left_valid, right_valid):
        case (True, True, False, False):
            start_symbol = '|'
        case (False, False, True, True):
            start_symbol = '-'
        case (True, False, True, False):
            start_symbol = 'J'
        case (True, False, False, True):
            start_symbol = 'L'
        case (False, True, True, False):
            start_symbol = '7'
        case (False, True, False, True):
            start_symbol = 'F'
    data[int(start.real)] = ''.join([
        data[int(start.real)][:int(start.imag)],
        start_symbol,
        data[int(start.real)][int(start.imag) + 1:]
    ])
    return start, data


def part_1(start, pipe_map):
    start_move1, start_move2 = PIPE_MOVES[get_symbol(pipe_map, start)]
    queue = Queue()
    queue.put((start + start_move1, 1))  # make one move to find the loop from start back to start (for part2)
    visited = [start, ]
    max_distance = 1
    while not queue.empty():
        current_loc, distance = queue.get()
        if current_loc in visited:
            continue
        visited += [current_loc]
        move1, move2 = PIPE_MOVES[get_symbol(pipe_map, current_loc)]
        queue.put((current_loc + move1, distance + 1))
        queue.put((current_loc + move2, distance + 1))
        if distance > max_distance:
            max_distance = distance
    return max_distance // 2 + 1, visited


def part_2(loop):
    # first use the shoelace formula to calculate the area of the polygon (i.e. the path)
    area = 0
    for p1, p2 in zip(loop, loop[1:] + [loop[0]]):
        area += (p1.real * p2.imag) - (p1.imag * p2.real)
    area = abs(area) / 2
    # use picks theorem to find the number of integer points inside the polygon
    # S = I + B / 2 - 1  (where S is polygon area, I are integer points inside the polygon, B are polygon edge points)
    inside = area - (len(loop) / 2) + 1
    return int(inside)


def main(fname):
    t0 = time.time()
    start, pipe_map = find_start(read_file(fname))
    total_1, loop = part_1(start, pipe_map)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-t0} s")
    total_2 = part_2(loop)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-t0} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
