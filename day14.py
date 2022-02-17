filename = "day14.txt"

from typing import DefaultDict


def parse() -> tuple[
    dict[tuple[str, str], int],
    dict[tuple[str, str], tuple[tuple[str, str], tuple[str, str]]],
    str,
]:
    compound: str = ""
    rules: dict[tuple[str, str], tuple[tuple[str, str], tuple[str, str]]] = {}
    with open(filename, "r") as text:
        compound = text.readline().strip()

        text.readline()  # Whitespace

        for line in text:
            pair, out = line.strip().split(" -> ")
            a, b = pair
            rules[(a, b)] = ((a, out), (out, b))

    pairs: dict[tuple[str, str], int] = DefaultDict(int)
    for pair in zip(compound, compound[1:]):
        pairs[pair] += 1
    last: str = compound[-1]

    return pairs, rules, last


def simulate(
    pairs: dict[tuple[str, str], int],
    rules: dict[tuple[str, str], tuple[tuple[str, str], tuple[str, str]]],
) -> dict[tuple[str, str], int]:

    new_pairs: dict[tuple[str, str], int] = DefaultDict(int)
    for pair, occurrances in pairs.items():
        if pair not in rules:
            new_pairs[pair] += occurrances
            continue
        outs = rules[pair]
        new_pairs[outs[0]] += occurrances
        new_pairs[outs[1]] += occurrances

    return new_pairs


def solve(
    pairs: dict[tuple[str, str], int],
    rules: dict[tuple[str, str], tuple[tuple[str, str], tuple[str, str]]],
    last: str,
    steps: int,
):

    for _ in range(steps):
        pairs = simulate(pairs, rules)

    char_count: dict[str, int] = DefaultDict(int)
    for (c, _), times in pairs.items():
        char_count[c] += times
    char_count[last] += 1

    print("Result:", max(char_count.values()) - min(char_count.values()))


if __name__ == "__main__":
    print("Day 14")
    pairs, rules, last = parse()
    print("Part 1")
    solve(pairs, rules, last, 10)
    print("---")
    print("Part 2")
    solve(pairs, rules, last, 40)