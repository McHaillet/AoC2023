import argparse
import time
import numpy as np
from scipy.spatial.distance import cdist


def read_file(fname):
    data = []
    with open(fname, "r") as file:
        for line in file:
            strip = line.strip()
            if strip != "":
                data.append(strip)
    return data


def index_galaxies(universe):
    points = []
    for x, row in enumerate(universe):
        for y, col in enumerate(row):
            if col == '#':
                points.append((x, y))
    return points


def get_dist_weights(data, expansion_factor):
    width, height = len(data), len(data[0])
    weights = np.ones((width, height))
    for j in range(len(data[0])):
        col = [r[j] for r in data]
        if '#' not in col:
            weights[:, j] = expansion_factor
    for i, row in enumerate(data):
        if '#' not in row:
            weights[i, :] = expansion_factor
    return weights


def galaxy_sum(data, expansion=2):
    dist_weights = get_dist_weights(data, expansion)
    galaxies = index_galaxies(data)
    total_distance = 0
    for i, p1 in enumerate(galaxies):
        for p2 in galaxies[i + 1:]:
            r_start = p1[0] if p1[0] <= p2[0] else p2[0]
            r_end = p2[0] + 1 if p1[0] <= p2[0] else p1[0] + 1
            c_start = p1[1] if p1[1] <= p2[1] else p2[1]
            c_end = p2[1] + 1 if p1[1] <= p2[1] else p1[1] + 1
            distance = (
                    dist_weights[r_start:r_end, p1[1]].sum()
                    + dist_weights[p2[0], c_start:c_end].sum()
                    - 2
            )
            total_distance += distance
    return int(total_distance)


def main(fname):
    start = time.time()
    data = read_file(fname)
    total_1 = galaxy_sum(data, expansion=2)
    t1 = time.time()
    print(f"Part 1: {total_1}")
    print(f"Ran in {t1-start} s")
    total_2 = galaxy_sum(data, expansion=1000000)
    print(f"Part 2: {total_2}")
    print(f"Ran in {time.time()-t1} s")
    print(f"Total ran in {time.time()-start} s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()
    filename = args.filename
    main(filename)
