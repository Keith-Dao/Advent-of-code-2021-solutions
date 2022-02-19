filename: str = "day19.txt"

from typing import Counter


class AxisPair:
    def __init__(self, axis: int, sign: int, diff: int) -> None:
        self.axis = axis
        self.sign = sign
        self.diff = diff


class Scanner:
    def __init__(self, lines: list[str]) -> None:

        _, _, s_id, _ = lines[0].split()
        self.id: int = int(s_id)
        n = len(lines)
        self.points: list[tuple[int, int, int]] = []
        for i in range(1, n):
            self.points.append(
                tuple([int(x) for x in lines[i].strip().split(",")])
            )


def parse() -> list[Scanner]:

    scanners: list[Scanner] = []
    with open(filename, "r") as text:
        sections: list[str] = text.read().split("\n\n")
        for section in sections:
            scanners.append(Scanner(section.splitlines()))

    return scanners


def compare(
    src: Scanner,
    axis: int,
    other: Scanner,
    edges: dict[int, AxisPair],
) -> None:

    for other_axis in [0, 1, 2]:
        for sign in [-1, 1]:
            diffs: dict[int, int] = Counter()
            for pt in src.points:
                for other_pt in other.points:
                    diffs[pt[axis] - other_pt[other_axis] * sign] += 1

            diff, n = diffs.most_common(1)[0]
            if n >= 12:
                edges[other.id] = AxisPair(other_axis, sign, diff)


def xEdgesFrom(
    scanner: Scanner, scanner_by_ids: dict[int, Scanner]
) -> dict[int, AxisPair]:

    x_edges: dict[int, AxisPair] = {}
    for other in scanner_by_ids.values():
        compare(scanner, 0, other, x_edges)

    return x_edges


def yzEdgesFrom(
    scanner: Scanner,
    scanner_by_ids: dict[int, Scanner],
    x_edges: dict[int, AxisPair],
) -> tuple[dict[int, AxisPair], dict[int, AxisPair]]:

    y_edges: dict[int, AxisPair] = {}
    z_edges: dict[int, AxisPair] = {}

    for other_id in x_edges:
        other = scanner_by_ids[other_id]
        compare(scanner, 1, other, y_edges)
        compare(scanner, 2, other, z_edges)

    return y_edges, z_edges


def solve(
    scanners: list[Scanner],
) -> tuple[set[tuple[int, int, int]], list[tuple[int, int, int]]]:

    scanner_by_ids: dict[int, Scanner] = {
        scanner.id: scanner for scanner in scanners
    }
    scanner_pos: dict[int, tuple[int, int, int]] = {0: (0, 0, 0)}
    points: set[tuple[int, int, int]] = set(scanner_by_ids[0].points)

    stack = [scanner_by_ids.pop(0)]
    while len(stack) != 0:
        scanner: Scanner = stack.pop()

        x_edges: dict[int, AxisPair] = xEdgesFrom(scanner, scanner_by_ids)
        y_edges, z_edges = yzEdgesFrom(scanner, scanner_by_ids, x_edges)

        for k in x_edges:
            dx = x_edges[k].diff
            dy = y_edges[k].diff
            dz = z_edges[k].diff

            scanner_pos[k] = (dx, dy, dz)

            next_scanner: Scanner = scanner_by_ids.pop(k)
            next_scanner.points[:] = [
                (
                    dx + x_edges[k].sign * pt[x_edges[k].axis],
                    dy + y_edges[k].sign * pt[y_edges[k].axis],
                    dz + z_edges[k].sign * pt[z_edges[k].axis],
                )
                for pt in next_scanner.points
            ]
            points.update(next_scanner.points)

            stack.append(next_scanner)

    return points, list(scanner_pos.values())


def manhattanDistance(a: tuple[int, int, int], b: tuple[int, int, int]) -> int:

    x1, y1, z1 = a
    x2, y2, z2 = b

    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def part1(points: set[tuple[int, int, int]]):
    print("Part 1")

    print("Total number of beacons:", len(points))


def part2(scanner_pos: list[tuple[int, int, int]]):
    print("Part 2")

    max_distance: int = 0
    n = len(scanner_pos)

    for i in range(n):
        for j in range(i + 1, n):
            max_distance = max(
                max_distance, manhattanDistance(scanner_pos[i], scanner_pos[j])
            )

    print("Maximum distance:", max_distance)


if __name__ == "__main__":
    print("Day 19")
    scanners: list[Scanner] = parse()
    points, scanner_pos = solve(scanners)
    part1(points)
    print("---")
    part2(scanner_pos)
