filename: str = "day9.txt"


def part1():
    print("Part 1")

    score: int = 0
    with open(filename, "r") as text:
        window: list[list[int]] = [
            [int(x) for x in text.readline() if x != "\n"] for _ in range(2)
        ]
        n = len(window[0])
        # Check the first line
        for i in range(n):
            risk: int = window[0][i] + 1

            if (
                (i != 0 and window[0][i - 1] <= risk - 1)
                or (i != n - 1 and window[0][i + 1] <= risk - 1)
                or (window[1][i] <= risk - 1)
            ):
                risk = 0

            score += risk

        # Go through the lines
        for line in text:
            window.append([int(x) for x in line if x != "\n"])

            for i in range(n):
                risk = window[1][i] + 1

                if (
                    (i != 0 and window[1][i - 1] <= risk - 1)
                    or (i != n - 1 and window[1][i + 1] <= risk - 1)
                    or (window[0][i] <= risk - 1)
                    or (window[2][i] <= risk - 1)
                ):
                    risk = 0

                score += risk

            window.pop(0)

        # Check the last line
        for i in range(n):
            risk: int = window[1][i] + 1

            if (
                (i != 0 and window[1][i - 1] <= risk - 1)
                or (i != n - 1 and window[1][i + 1] <= risk - 1)
                or (window[0][i] <= risk - 1)
            ):
                risk = 0

            score += risk

    print("Score:", score)


def dfs(r: int, c: int, map_t: tuple[list[list[int]], int, int]) -> int:

    map, m, n = map_t
    if not 0 <= r < m or not 0 <= c < n or map[r][c] == 9:
        return 0

    map[r][c] = 9
    count = 1
    if r > 0:
        count += dfs(r - 1, c, map_t)
    if r < m - 1:
        count += dfs(r + 1, c, map_t)
    if c > 0:
        count += dfs(r, c - 1, map_t)
    if c < n - 1:
        count += dfs(r, c + 1, map_t)

    return count


def part2():
    print("Part 2")

    map = []
    with open(filename, "r") as text:
        for line in text:
            map.append([int(x) for x in line if x != "\n"])

    s1 = s2 = s3 = 0
    m, n = len(map), len(map[0])
    for r in range(m):
        for c in range(n):
            if map[r][c] == 9:
                continue

            res: int = dfs(r, c, (map, m, n))

            if s1 < res:
                s1, s2, s3 = res, s1, s2
            elif s2 < res:
                s2, s3 = res, s2
            elif s3 < res:
                s3 = res

    print("Answer:", s1 * s2 * s3)


if __name__ == "__main__":
    print("Day 9")
    part1()
    print("---")
    part2()
