from __future__ import annotations
from io import TextIOWrapper

filename: str = "day24.txt"

from typing import Callable


class ALU:
    instructions: dict[str, Callable[[ALU, str, int], int]] = {
        "inp": lambda alu, a, b: b,
        "add": lambda alu, a, b: alu.variables[a] + b,
        "mul": lambda alu, a, b: alu.variables[a] * b,
        "div": lambda alu, a, b: alu.variables[a] // b,
        "mod": lambda alu, a, b: alu.variables[a] % b,
        "eql": lambda alu, a, b: int(alu.variables[a] == b),
    }

    def __init__(self, variables: dict[str, int] | None = None) -> None:
        self.variables: dict[str, int] = variables or {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }

    def apply_instruction(self, instruction: str, a: str, b_s: str):
        b: int = int(b_s) if b_s.isdigit() else self.variables[b_s]
        self.variables[a] = self.instructions[instruction](self, a, b)

    def is_valid(self) -> bool:
        return self.variables["z"] == 0

    def clone(self) -> ALU:
        return ALU({k: v for k, v in self.variables.items()})


def skip(text: TextIOWrapper, n: int):
    for _ in range(n):
        text.readline()


def perform(alu: ALU, i: int, instructions: list[str]) -> tuple[bool, int]:
    if i == len(instructions):
        return alu.is_valid(), 0

    while i < len(instructions):
        instruction, a, *b_s = instructions[i].split()
        if instruction == "inp":
            for b in range(9, -1, -1):
                new_alu: ALU = alu.clone()
                new_alu.apply_instruction(instruction, a, str(b))
                valid, path = perform(new_alu, i + 1, instructions)
                if valid:
                    return valid, b * 10 + path

        else:
            alu.apply_instruction(instruction, a, b_s[0])

    return False, 0


def get_constraints() -> list[tuple[int, int, int]]:
    constraints: list[tuple[int, int, int]] = []
    stack: list[tuple[int, int]] = []

    with open(filename, "r") as text:
        for i in range(14):  # Total of 14 chunks
            skip(text, 4)
            line: str = text.readline().strip()
            assert line.startswith("div z "), "Invalid input."

            if line == "div z 1":
                skip(text, 10)
                line = text.readline()
                assert line.startswith("add y"), "Invalid input."

                b = int(line.strip().split()[-1])
                stack.append((i, b))
                skip(text, 2)
            else:
                line = text.readline()
                assert line.startswith("add x"), "Invalid input."

                b = int(line.strip().split()[-1])
                j, a = stack.pop()
                constraints.append((i, j, a + b))
                skip(text, 12)

    return constraints


def part1():
    print("Part 1")

    constraints: list[tuple[int, int, int]] = get_constraints()
    digits: list[int] = [0] * 14
    for i, j, diff in constraints:
        if diff > 0:
            digits[i], digits[j] = 9, 9 - diff
        else:
            digits[i], digits[j] = 9 + diff, 9

    num: int = 0
    for d in digits:
        num = num * 10 + d
    print("Largest valid model number", num)


def part2():
    print("Part 2")

    constraints: list[tuple[int, int, int]] = get_constraints()
    digits: list[int] = [0] * 14
    for i, j, diff in constraints:
        if diff > 0:
            digits[i], digits[j] = 1 + diff, 1
        else:
            digits[i], digits[j] = 1, 1 - diff

    num: int = 0
    for d in digits:
        num = num * 10 + d
    print("Smallest valid model number", num)


if __name__ == "__main__":
    print("Day 24")
    part1()
    print("---")
    part2()
