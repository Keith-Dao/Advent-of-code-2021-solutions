filename: str = "day13.txt"


def parse() -> tuple[set[tuple[int, int]], list[tuple[str, int]]]:
    points: set[tuple[int, int]] = set()
    instructions: list[tuple[str, int]] = []
    with open(filename, "r") as text:
        line: str = text.readline()
        while line != "\n":
            x, y = (int(a) for a in line.strip().split(","))
            points.add((x, y))
            line = text.readline()

        line = text.readline()
        while line:
            instruction = line.strip().split()[-1]
            axis, val = instruction.split("=")
            instructions.append((axis, int(val)))
            line = text.readline()
    return points, instructions


def foldAlongX(points: set[tuple[int, int]], axis: int) -> None:
    p: list[tuple[int, int]] = list(points)
    for x, y in p:
        if x <= axis:
            continue
        points.remove((x, y))
        new_x: int = 2 * axis - x
        points.add((new_x, y))


def foldAlongY(points: set[tuple[int, int]], axis: int) -> None:
    p: list[tuple[int, int]] = list(points)
    for x, y in p:
        if y <= axis:
            continue
        points.remove((x, y))
        new_y: int = 2 * axis - y
        points.add((x, new_y))


def performInstruction(
    points: set[tuple[int, int]], instruction: tuple[str, int]
) -> None:
    axis, value = instruction
    if axis == "x":
        foldAlongX(points, value)
    elif axis == "y":
        foldAlongY(points, value)


def part1(points: set[tuple[int, int]], instructions: list[tuple[str, int]]):
    print("Part 1")

    performInstruction(points, instructions[0])
    print("Number of visible points:", len(points))


def part2(points: set[tuple[int, int]], instructions: list[tuple[str, int]]):
    print("Part 2")

    for instruction in instructions:
        performInstruction(points, instruction)

    # Create a human readable grid
    m, n = (
        max(points, key=lambda a: a[1])[1] + 1,
        max(points, key=lambda a: a[0])[0] + 1,
    )
    grid: list[list[int]] = [[0] * n for _ in range(m)]
    for x, y in points:
        grid[y][x] = 1

    print("Code:")
    for line in grid:
        for c in line:
            print("█" if c else " ", end="")
        print("")


if __name__ == "__main__":
    print("Day 13")
    points, instructions = parse()
    part1(points, instructions)
    print("---")
    part2(points, instructions)