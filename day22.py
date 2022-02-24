filename: str = "day22.txt"

from typing import Callable
import numpy as np


def getRange(line: str) -> tuple[int, int]:

    lower, upper = line[2:].split("..")
    return int(lower), int(upper)


def intersection(cuboid: list[int], core: list[int]) -> list[int] | None:

    action = [lambda a, b: -b, max, min, max, min, max, min]
    intersection: list[int] = [action[i](cuboid[i], core[i]) for i in range(7)]

    return (
        None
        if intersection[1] > intersection[2]
        or intersection[3] > intersection[4]
        or intersection[5] > intersection[6]
        else intersection
    )


def part1():
    print("Part 1")

    inRange: Callable[[int, int], bool] = lambda x1, x2: 0 <= x1 < x2 <= 101
    shiftRange: Callable[[int, int], tuple[int, int]] = lambda x1, x2: (
        x1 + 50,
        x2 + 51,
    )
    cuboid: np.ndarray = np.zeros((100, 100, 100), dtype=int)
    with open(filename, "r") as text:

        for line in text:
            setting, coords = line.strip().split()
            x, y, z = [shiftRange(*getRange(s)) for s in coords.split(",")]

            if not inRange(*x) or not inRange(*y) or not inRange(*z):
                continue

            cuboid[x[0] : x[1], y[0] : y[1], z[0] : z[1]] = setting == "on"

    print("Cuboids on:", np.sum(cuboid))


def part2():
    print("Part 2")

    cuboids: list[list[int]] = []
    with open(filename, "r") as text:
        for line in text:
            setting, coords = line.strip().split()
            x, y, z = [getRange(s) for s in coords.split(",")]

            cuboids.append([int(setting == "on"), *x, *y, *z])

    cores: list[list[int]] = []
    for cuboid in cuboids:
        to_add: list[list[int]] = [cuboid] if cuboid[0] == 1 else []
        for core in cores:
            inter = intersection(cuboid, core)
            if inter:
                to_add += [inter]

        cores += to_add

    count: int = 0
    for core in cores:
        count += (
            core[0]
            * (core[2] - core[1] + 1)
            * (core[4] - core[3] + 1)
            * (core[6] - core[5] + 1)
        )

    print("Cuboids on:", count)


if __name__ == "__main__":
    print("Day 22")
    part1()
    print("---")
    part2()
