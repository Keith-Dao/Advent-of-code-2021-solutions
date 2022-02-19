filename: str = "day18.txt"

import json
from typing import Any


def parse():
    with open(filename, "r") as text:
        return list(map(json.loads, text.read().splitlines()))


def addLeft(x, n):
    if not n:
        return x
    if isinstance(x, int):
        return x + n
    return [addLeft(x[0], n), x[1]]


def addRight(x, n):
    if not n:
        return x
    if isinstance(x, int):
        return x + n
    return [x[0], addRight(x[1], n)]


def explode(x, depth=0) -> tuple[bool, Any, Any, Any]:
    if isinstance(x, int):
        return False, None, x, None
    if depth == 4:
        return True, x[0], 0, x[1]
    a, b = x
    exploded, left, a, right = explode(a, depth + 1)
    if exploded:
        return True, left, [a, addLeft(b, right)], None
    exploded, left, b, right = explode(b, depth + 1)
    if exploded:
        return True, None, [addRight(a, left), b], right
    return False, None, x, None


def split(x) -> tuple[bool, Any]:
    if isinstance(x, int):
        if x >= 10:
            return True, [x // 2, x // 2 + x % 2]
        return False, x
    a, b = x
    change, a = split(a)
    if change:
        return True, [a, b]
    change, b = split(b)
    if change:
        return True, [a, b]
    return False, [a, b]


def add(a, b):
    x = [a, b]
    changed = True
    while True:
        changed, _, x, _ = explode(x)
        if changed:
            continue

        changed, x = split(x)
        if not changed:
            break
    return x


def magnitude(x) -> int:
    a, b = x
    if isinstance(a, list):
        a = magnitude(a)
    if isinstance(b, list):
        b = magnitude(b)
    return 3 * a + 2 * b


def part1(lines):
    print("Part 1")

    line = lines[0]
    n: int = len(lines)
    for i in range(1, n):
        line = add(line, lines[i])

    print("Magnitude:", magnitude(line))


def part2(lines):
    print("Part 2")

    n: int = len(lines)
    max_magnitude: int = 0
    for i in range(n):
        for j in range(i + 1, n):
            max_magnitude = max(
                max_magnitude,
                magnitude(add(lines[i], lines[j])),
                magnitude(add(lines[j], lines[i])),
            )

    print("Maximum magnitude:", max_magnitude)


if __name__ == "__main__":
    print("Day 18")
    lines = parse()
    part1(lines)
    print("---")
    part2(lines)
