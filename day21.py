filename: str = "day21.txt"

from typing import Generator


def parse():
    with open(filename, "r") as text:
        p1: int = int(text.readline().strip().split()[-1])
        p2: int = int(text.readline().strip().split()[-1])

    return p1, p2


def precomputeWays(target: int, used: int = 0) -> int:
    if used > 3:
        return 0

    if target == 0:
        return int(used == 3)

    count: int = 0
    for i in range(1, 4):
        if i > target:
            break
        count += precomputeWays(target - i, used + 1)
    return count


def moveSet() -> dict[int, int]:
    move_set: dict[int, int] = {}
    for i in range(3, 10):
        move_set[i] = precomputeWays(i)

    return move_set


def move(p: int, spaces: int) -> int:
    return (p + spaces - 1) % 10 + 1


def possible_moves(
    p: int, ways: dict[int, int]
) -> Generator[tuple[int, int], None, None]:
    for i, t in ways.items():
        yield move(p, i), t


def part1(p1: int, p2: int):
    print("Part 1")

    dice: int = 0
    p1_score = p2_score = 0
    winning_score: int = 1000

    while p1_score < winning_score and p2_score < winning_score:

        spaces: int = dice * 3 + 6
        p1 = move(p1, spaces)
        p1_score += p1
        dice += 3

        if p1_score >= winning_score:
            break

        spaces: int = dice * 3 + 6
        p2 = move(p2, spaces)
        p2_score += p2
        dice += 3

    print("Score:", min(p1_score, p2_score) * dice)


def simulate(
    p1: int,
    p2: int,
    dp: dict[tuple[int, int, int, int], tuple[int, int]],
    moves: dict[int, int],
    s1: int = 0,
    s2: int = 0,
) -> tuple[int, int]:

    WINNING_SCORE: int = 21
    if s1 >= WINNING_SCORE:
        return 1, 0
    if s2 >= WINNING_SCORE:
        return 0, 1

    if (state := (p1, p2, s1, s2)) in dp:
        return dp[state]

    t1 = t2 = 0
    for m, t in possible_moves(p1, moves):
        x2, x1 = simulate(p2, m, dp, moves, s2, s1 + m)
        t1 += x1 * t
        t2 += x2 * t

    dp[state] = t1, t2
    return t1, t2


def part2(p1: int, p2: int):
    print("Part 2")

    print("Total winning universes:", max(simulate(p1, p2, {}, moveSet())))


if __name__ == "__main__":
    print("Day 21")
    p1, p2 = parse()
    part1(p1, p2)
    print("---")
    part2(p1, p2)
