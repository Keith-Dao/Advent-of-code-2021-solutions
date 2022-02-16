filename = "day11.txt"

import numpy as np


def loadInput() -> np.ndarray:
    with open(filename, "r") as text:
        return np.array([[int(x) for x in line if x != "\n"] for line in text])


def simulateDay(levels: np.ndarray, m: int, n: int) -> int:
    levels += 1
    flashes = levels > 9
    if not np.any(flashes):
        return 0

    # Increase the energy of surronding squids via BFS
    queue = [(i, j) for j in range(n) for i in range(m) if flashes[i, j]]

    while len(queue) != 0:
        i, j = queue.pop(0)

        for k, l in [
            (i - 1, j - 1),
            (i - 1, j),
            (i - 1, j + 1),
            (i, j - 1),
            (i, j + 1),
            (i + 1, j - 1),
            (i + 1, j),
            (i + 1, j + 1),
        ]:
            if not 0 <= k < m or not 0 <= l < n or flashes[k, l]:
                continue

            levels[k, l] += 1
            if levels[k, l] > 9:
                flashes[k, l] = True
                queue.append((k, l))

    # Reset levels to 0 for all flashing octopuses
    levels *= 1 - flashes

    return np.sum(flashes)


def part1():
    print("Part 1")

    levels: np.ndarray = loadInput()
    m, n = levels.shape

    total_flashes: int = 0
    for _ in range(100):
        total_flashes += simulateDay(levels, m, n)

    print("Total flashes:", total_flashes)


def part2():
    print("Part 2")

    levels: np.ndarray = loadInput()
    m, n = levels.shape

    flashes: int = 0
    step: int = 0
    while flashes != m * n:
        flashes = simulateDay(levels, m, n)
        step += 1

    print("Step:", step)


if __name__ == "__main__":
    print("Day 11")
    part1()
    print("---")
    part2()
