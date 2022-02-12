filename: str = "day8.txt"

from functools import reduce

digits: list[str] = [
    "abcefg",
    "cf",
    "acdeg",
    "acdfg",
    "bdcf",
    "abdfg",
    "abdefg",
    "acf",
    "abcdefg",
    "abcdfg",
]
code_to_digit: dict[str, int] = {digits[i]: i for i in range(10)}
length_candidates: dict[int, list[str]] = {}
for i in range(10):
    key = len(digits[i])
    length_candidates[key] = length_candidates.get(key, []) + [digits[i]]

uniques: set[int] = {
    length
    for length, candidates in length_candidates.items()
    if len(candidates) == 1
}


def part1():
    print("Part 1")
    count = 0
    with open(filename, "r") as text:
        for line in text:
            _, output, *_ = line.split("|")
            for w in output.split():
                if len(w) in uniques:
                    count += 1
    print("Number of times 1, 4, 7, 8 appears:", count)


def segInd(c: str) -> int:
    return ord(c) - ord("a")


def remap(w: str, wire_map: list[str]) -> str:

    return "".join(
        sorted(reduce(lambda a, b: a + [wire_map[segInd(b)]], w, []))
    )


def calculate(line: str) -> int:
    wiring, output, *_ = line.split("|")

    true_wiring: list[list[str]] = [[]] * 10
    wire_map: list[str] = [""] * 7
    candidates: dict[int, list[str]] = {}
    # Determine the true wiring
    w: str
    for w in wiring.split():
        n: int = len(w)
        if n in uniques:
            actual_num: int = code_to_digit[length_candidates[n][0]]
            true_wiring[actual_num] = sorted(w)
        else:
            candidates[n] = candidates.get(n, []) + [w]

    # Find the top segment wire
    top_wire: int = 0
    for c in true_wiring[7]:
        top_wire ^= ord(c)
    for c in true_wiring[1]:
        top_wire ^= ord(c)
    wire_map[segInd("a")] = chr(top_wire)

    # Intersection of 6 segments
    six_intersection: set[str] = reduce(
        lambda a, b: a & set(b), candidates[6], set(true_wiring[8])
    )

    # Right candidates
    group: set[str] = set(true_wiring[1])
    wire_map[segInd("f")] = next(iter(six_intersection & group))
    wire_map[segInd("c")] = next(iter(group ^ set(wire_map[segInd("f")])))

    # Top left candidates
    group: set[str] = set(true_wiring[1]) ^ set(true_wiring[4])
    wire_map[segInd("b")] = next(iter(six_intersection & group))
    wire_map[segInd("d")] = next(iter(group ^ set(wire_map[segInd("b")])))

    # Bottom left candidates
    eg_candidates: set[str] = set(true_wiring[8]) ^ set(wire_map) ^ set([""])
    wire_map[segInd("g")] = next(iter(six_intersection & eg_candidates))
    wire_map[segInd("e")] = next(
        iter(eg_candidates ^ set(wire_map[segInd("g")]))
    )

    # Inverse the wire map
    wrong_to_true: list[str] = [""] * 7
    for i in range(7):
        wrong_to_true[segInd(wire_map[i])] = chr(ord("a") + i)

    # Map the unknowns
    for w in candidates[6] + candidates[5]:
        num: int = code_to_digit[remap(w, wrong_to_true)]
        true_wiring[num] = sorted(w)

    # Inverse the wires to a number
    wire_to_num: dict[str, int] = {}
    for i in range(10):
        wire: str = "".join(true_wiring[i])
        wire_to_num[wire] = i

    # Determine the correct value
    value = 0
    for w in output.split():
        value = value * 10 + wire_to_num["".join(sorted(w))]

    return value


def part2():
    print("Part 2")
    total = 0
    with open(filename, "r") as text:
        for line in text:
            total += calculate(line)
    print("Total: ", total)


if __name__ == "__main__":
    print("Day 8")
    part1()
    print("---")
    part2()
