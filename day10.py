filename = "day10.txt"

RIGHT_TO_LEFT: dict[str, str] = {"]": "[", ")": "(", ">": "<", "}": "{"}
LEFT_TO_RIGHT: dict[str, str] = {v: k for k, v in RIGHT_TO_LEFT.items()}


def calculateIllegalCharacterScore(line: str) -> int:
    BRACKET_SCORE: dict[str, int] = {")": 3, "]": 57, "}": 1197, ">": 25137}

    stack: list[str] = []
    for c in line:
        if c in RIGHT_TO_LEFT.values():
            stack.append(c)
        elif c in RIGHT_TO_LEFT.keys():
            if RIGHT_TO_LEFT[c] != stack.pop():
                return BRACKET_SCORE[c]
    return 0


def part1():
    print("Part 1")
    score: int = 0
    with open(filename, "r") as text:
        for line in text:
            score += calculateIllegalCharacterScore(line)

    print("Score:", score)


def calculateIncompleteLineScore(line: str) -> int:
    BRACKET_SCORE: dict[str, int] = {")": 1, "]": 2, "}": 3, ">": 4}

    score: int = 0
    stack: list[str] = []
    for c in line:
        if c in RIGHT_TO_LEFT.values():
            stack.append(c)
        elif c in RIGHT_TO_LEFT.keys():
            if RIGHT_TO_LEFT[c] != stack.pop():
                return score

    while len(stack) != 0:
        score = score * 5 + BRACKET_SCORE[LEFT_TO_RIGHT[stack.pop()]]

    return score


def part2():
    print("Part 2")
    scores: list[int] = []
    with open(filename, "r") as text:
        for line in text:
            score = calculateIncompleteLineScore(line)
            if score != 0:
                scores.append(score)

    n = len(scores)
    print("Score:", sorted(scores)[n // 2])


if __name__ == "__main__":
    print("Day 10")
    part1()
    print("---")
    part2()
