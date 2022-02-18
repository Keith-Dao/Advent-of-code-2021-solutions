filename: str = "day15.txt"

import heapq


class Node:
    def __init__(self, coord: tuple[int, int], total: int, repeats: int = 1):
        self.coord: tuple[int, int] = coord
        self.total: int = total
        self.repeats: int = repeats

    def getChildren(self, board: list[list[int]]):
        x, y = self.coord
        m, n = len(board), len(board[0])
        M, N = m * self.repeats, n * self.repeats

        for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            new_x, new_y = x + dx, y + dy
            if not 0 <= new_x < M or not 0 <= new_y < N:
                continue

            cost: int = (
                board[new_y % m][new_x % n] + (new_x // m) + (new_y // n) - 1
            ) % 9 + 1  # [1, 9]
            yield Node((new_x, new_y), self.total + cost, self.repeats)

    def isEnd(self, board: list[list[int]]):
        x, y = self.coord
        m, n = len(board) * self.repeats, len(board[0]) * self.repeats

        return y == m - 1 and x == n - 1

    def __lt__(self, other):
        return self.total < other.total


def parse() -> list[list[int]]:
    board: list[list[int]] = []
    with open(filename, "r") as text:
        for line in text:
            board.append([int(x) for x in line.strip()])

    return board


def ucs(
    board: list[list[int]], start: tuple[int, int], repeats: int = 1
) -> int:

    m, n = len(board), len(board[0])
    visited: dict[tuple[int, int], int] = {start: 0}
    start_node: Node = Node(start, 0, repeats)
    queue = [start_node]
    heapq.heapify(queue)

    while len(queue) != 0:
        node: Node = heapq.heappop(queue)

        if node.isEnd(board):
            return node.total

        for child in node.getChildren(board):
            if child.coord in visited and child.total >= visited[child.coord]:
                continue
            heapq.heappush(queue, child)
            visited[child.coord] = child.total

    return 0


def part1(board: list[list[int]]):
    print("Part 1")
    print("Minimum cost:", ucs(board, (0, 0)))


def part2(board: list[list[int]]):
    print("Part 2")
    print("Minimum cost:", ucs(board, (0, 0), 5))


if __name__ == "__main__":
    print("Day 15")
    board: list[list[int]] = parse()
    part1(board)
    print("---")
    part2(board)