filename: str = "day16.txt"

from typing import Callable, Generator


class Sequence:
    def __init__(self):
        self.pos: int = 0
        self.version_sum: int = 0

    def step(self, steps: int):
        self.pos += steps

    def addVersion(self, bits: Generator[int, None, None]):
        self.version_sum += read(bits, self, 3)


def parse() -> Generator[int, None, None]:
    with open(filename, "r") as text:
        return (
            (int(c, 16) >> i) & 1
            for c in text.readline().strip()
            for i in range(3, -1, -1)
        )


def read(
    bits: Generator[int, None, None], sequence: Sequence, size: int
) -> int:
    sequence.step(size)
    return sum(next(bits) << i for i in range(size - 1, -1, -1))


def operations(type_id: int) -> Callable[[int, int], int]:

    operator: list[Callable[[int, int], int]] = [
        lambda a, b: a + b,
        lambda a, b: a * b,
        lambda a, b: min(a, b),
        lambda a, b: max(a, b),
        lambda a, _: a,
        lambda a, b: int(a > b),
        lambda a, b: int(a < b),
        lambda a, b: int(a == b),
    ]

    return operator[type_id]


def packet(bits: Generator[int, None, None], sequence: Sequence) -> int:

    sequence.addVersion(bits)
    total: int = 0

    if (type_id := read(bits, sequence, 3)) == 4:
        # Literal packet
        prefix, total = read(bits, sequence, 1), read(bits, sequence, 4)
        while prefix == 1:
            prefix, total = read(bits, sequence, 1), total << 4 | read(
                bits, sequence, 4
            )
    elif read(bits, sequence, 1) == 0:
        length: int = read(bits, sequence, 15) + sequence.pos
        total = packet(bits, sequence)
        while sequence.pos < length:
            total = operations(type_id)(total, packet(bits, sequence))
    else:
        count: int = read(bits, sequence, 11)
        total = packet(bits, sequence)
        for _ in range(count - 1):
            total = operations(type_id)(total, packet(bits, sequence))

    return total


def part1(sequence: Sequence):
    print("Part 1")

    print("Sum of all version numbers:", sequence.version_sum)


def part2(total: int):
    print("Part 2")

    print("Value of transmission:", total)


if __name__ == "__main__":
    print("Day 16")

    bits: Generator[int, None, None] = parse()
    sequence: Sequence = Sequence()
    total: int = packet(bits, sequence)

    part1(sequence)
    print("---")
    part2(total)
