filename: str = "day17.txt"


class TargetArea:
    def __init__(self, x: tuple[int, int], y: tuple[int, int]):
        self.x_min, self.x_max = x
        self.y_min, self.y_max = y


class Probe:
    def __init__(self, dx: int, dy: int, target_area: TargetArea):
        self.x: int = 0
        self.y: int = 0
        self.dx: int = dx
        self.dy: int = dy
        self.target_area: TargetArea = target_area

    def step(self):
        self.x += self.dx
        self.y += self.dy
        self.dx = max(self.dx - 1, 0)
        self.dy -= 1

    def isIn(self, target_range: tuple[int, int], x: int) -> bool:
        return target_range[0] <= x <= target_range[1]

    def xIn(self) -> bool:
        return self.target_area.x_min <= self.x <= self.target_area.x_max

    def yIn(self) -> bool:
        return self.target_area.y_min <= self.y <= self.target_area.y_max

    def inArea(self) -> bool:
        return self.xIn() and self.yIn()

    def overshot(self) -> bool:
        return (
            (self.x > self.target_area.x_max)
            or (self.dx == 0 and not self.xIn())
            or (self.dy < 0 and self.y < self.target_area.y_min)
        )


def getRange(r: str) -> tuple[int, int]:
    return tuple(int(x) for x in r[2:].split(".."))


def parse() -> TargetArea:
    with open(filename, "r") as text:
        line = text.readline()
        _, _, xs, ys = line.split()
        xs = getRange(xs[:-1])
        ys = getRange(ys)

    return TargetArea(xs, ys)


def part1(target_area: TargetArea):
    print("Part 1")

    n: int = -target_area.y_min - 1
    print("Highest distance:", n * (n + 1) // 2)


def part2(target_area: TargetArea):
    print("Part 2")

    count: int = 0
    y_max: int = max(abs(target_area.y_min), abs(target_area.y_max))
    for dx in range(target_area.x_max + 1):
        for dy in range(-y_max, y_max + 1):
            probe: Probe = Probe(dx, dy, target_area)

            while not probe.overshot():
                if probe.inArea():
                    count += 1
                    break
                probe.step()

    print("Distinct velocities:", count)


if __name__ == "__main__":
    print("Day 17")
    target_area: TargetArea = parse()
    part1(target_area)
    print("---")
    part2(target_area)
