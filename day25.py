filename: str = "day25.txt"


class Trench:
    def __init__(self) -> None:
        self.east_facing: set[tuple[int, int]] = set()
        self.south_facing: set[tuple[int, int]] = set()
        self.rows: int = 0
        self.columns: int = 0
        self.stopped: bool = False

        with open(filename, "r") as text:
            for y, line in enumerate(text):
                self.columns = len(line.strip())
                self.rows += 1
                for x, c in enumerate(line):
                    if c == ">":
                        self.east_facing.add((x, y))
                    elif c == "v":
                        self.south_facing.add((x, y))

    def step(self) -> None:
        if self.stopped:
            return

        # Step east facing first
        next_east: set[tuple[int, int]] = set()
        for x, y in self.east_facing:
            new_coord: tuple[int, int] = (x + 1) % self.columns, y
            if new_coord in self.south_facing or new_coord in self.east_facing:
                next_east.add((x, y))
            else:
                next_east.add(new_coord)

        # Step south facing first
        next_south: set[tuple[int, int]] = set()
        for x, y in self.south_facing:
            new_coord: tuple[int, int] = x, (y + 1) % self.rows
            if new_coord in self.south_facing or new_coord in next_east:
                next_south.add((x, y))
            else:
                next_south.add(new_coord)

        if self.east_facing == next_east and self.south_facing == next_south:
            self.stopped = True
        self.east_facing, self.south_facing = next_east, next_south

    def is_moving(self) -> bool:
        return not self.stopped

    def print(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if (j, i) in self.east_facing:
                    print(">", end="")
                elif (j, i) in self.south_facing:
                    print("v", end="")
                else:
                    print(".", end="")
            print()


def part1():
    print("Part 1")

    trench: Trench = Trench()
    steps: int = 0
    while trench.is_moving():
        trench.step()
        steps += 1

    print("Total steps:", steps)


if __name__ == "__main__":
    print("Day 25")
    part1()
