filename = "day4.txt"


def parseText():

    text = open(filename)
    numbers, num_map = [], {}
    for num in text.readline().split(","):
        num = int(num)
        num_map[num] = []
        numbers.append(num)

    text.readline()
    boards, board = [], []
    counter, row = 0, 0
    for line in text:
        if len(line) == 1:
            boards.append(board)
            counter += 1
            board = []
            row = 0
            continue

        nums = [int(num) for num in line.split()]
        for col, num in enumerate(nums):
            if num in numbers:
                num_map[num].append((counter, row, col))
        board.append(nums)
        row += 1
    boards.append(board)
    text.close()

    return numbers, num_map, boards


def part1(numbers, num_map, boards):

    print("Part 1")
    n, r, c = len(boards), len(boards[0]), len(boards[0][0])
    row_counters = [[c] * r for _ in range(n)]
    col_counters = [[r] * c for _ in range(n)]
    game_over = False
    num = winning = 0

    for num in numbers:
        for b, r, c in num_map[num]:
            boards[b][r][c] = 0
            row_counters[b][r] -= 1
            col_counters[b][c] -= 1

            if (
                row_counters[b][r] == 0
                or col_counters[b][c] == 0
            ):
                game_over = True
                winning = b
        if game_over:
            break

    total = sum([sum(x) for x in boards[winning]])
    print(total * num)


def part2(numbers, num_map, boards):

    print("Part 2")
    n, r, c = len(boards), len(boards[0]), len(boards[0][0])
    row_counters = [[c] * r for _ in range(n)]
    col_counters = [[r] * c for _ in range(n)]
    won = set()
    last = winning = 0

    for num in numbers:
        for b, r, c in num_map[num]:
            if b in won:
                continue
            boards[b][r][c] = 0
            row_counters[b][r] -= 1
            col_counters[b][c] -= 1

            if (
                row_counters[b][r] == 0
                or col_counters[b][c] == 0
            ):
                won.add(b)
                winning = b
                last = num

    total = sum([sum(x) for x in boards[winning]])
    print(total * last)


if __name__ == "__main__":
    print("Day 4")
    numbers, num_map, boards = parseText()
    part1(
        numbers,
        num_map,
        [
            [[x for x in row] for row in board]
            for board in boards
        ],
    )
    print("---")
    part2(
        numbers,
        num_map,
        [
            [[x for x in row] for row in board]
            for board in boards
        ],
    )