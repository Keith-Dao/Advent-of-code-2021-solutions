filename: str = "day25.txt"

import numpy as np


class Trench:
    def __init__(self) -> None:
        self.moving: list[np.bool_] = [np.True_, np.True_]

        with open(filename, "r") as text:
            self.map: np.ndarray = np.array(
                list(map(list, text.read().strip().split()))
            )

    def step(self) -> None:
        for cucumber_type, axis in ((">", 1), ("v", 0)):
            can_move = (np.roll(self.map, -1, axis) == ".") & (
                self.map == cucumber_type
            )  # Find the cucumbers that can move
            self.moving[axis] = np.any(
                can_move
            )  # Check if any cucumbers can move
            self.map[
                can_move
            ] = "."  # Empty the spaces where the cucumber moved
            self.map[np.roll(can_move, 1, axis)] = cucumber_type

    def is_moving(self) -> bool:
        return any(self.moving)

    def print(self):
        for line in self.map:
            print("".join(line))


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
