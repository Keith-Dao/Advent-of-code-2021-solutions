filename = "day12.txt"

from typing import DefaultDict


def parse() -> dict[str, list[str]]:
    map: dict[str, list[str]] = DefaultDict(list)
    with open(filename, "r") as text:
        for line in text:
            n1, n2, *_ = line.strip().split("-")
            map[n1].append(n2)
            map[n2].append(n1)
    return map


def dfs(node: str, map: dict[str, list[str]], visited: set[str]) -> int:

    count: int = 0
    if node[0].islower():
        visited.add(node)

    for neighbour in map[node]:
        if neighbour in visited:
            continue
        elif neighbour == "end":
            count += 1
        else:
            count += dfs(neighbour, map, visited)
    visited.discard(node)

    return count


def part1(map: dict[str, list[str]]):
    print("Part 1")

    print("Total unique paths:", dfs("start", map, set()))


def dfs2(
    node: str,
    map: dict[str, list[str]],
    visited: dict[str, int],
    visited_twice: bool = False,
) -> int:
    count: int = 0
    if node[0].islower():
        visited[node] += 1

    for neighbour in map[node]:
        if neighbour == "start" or (visited_twice and visited[neighbour] > 0):
            continue
        elif neighbour == "end":
            count += 1
        else:
            count += dfs2(
                neighbour, map, visited, visited_twice or visited[neighbour] > 0
            )
    visited[node] -= 1

    return count


def part2(map: dict[str, list[str]]):
    print("Part 2")

    print("Total unique paths:", dfs2("start", map, DefaultDict(int)))


if __name__ == "__main__":
    print("Day 12")
    map: dict[str, list[str]] = parse()
    part1(map)
    print("---")
    part2(map)