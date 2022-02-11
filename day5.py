filename = "day5.txt"


def part1():

    print("Part 1")
    text = open(filename)
    lines = {}
    for line in text:
        p1, p2, *_ = line.split(" -> ")
        x1, y1, *_ = p1.split(",")
        x2, y2, *_ = p2.split(",")

        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        if x1 != x2 and y1 != y2:
            continue

        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y in range(min(y1, y2), max(y1, y2) + 1):
                lines[(x, y)] = lines.get((x, y), 0) + 1
    text.close()

    count = 0
    for c in lines.values():
        count += int(c >= 2)

    print(count)


def part2():

    print("Part 2")
    text = open(filename)
    lines = {}
    for line in text:
        p1, p2, *_ = line.split(" -> ")
        x1, y1, *_ = p1.split(",")
        x2, y2, *_ = p2.split(",")

        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                lines[(x1, y)] = lines.get((x1, y), 0) + 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                lines[(x, y1)] = lines.get((x, y1), 0) + 1
        elif (y1 - y2) / (x1 - x2) == 1:
            x, y = min(x1, x2), min(y1, y2)
            for i in range(abs(y1 - y2) + 1):
                lines[(x + i, y + i)] = (
                    lines.get((x + i, y + i), 0) + 1
                )
        elif (y1 - y2) / (x1 - x2) == -1:
            x, y = min(x1, x2), max(y1, y2)
            for i in range(abs(y1 - y2) + 1):
                lines[(x + i, y - i)] = (
                    lines.get((x + i, y - i), 0) + 1
                )
        else:
            print("no")
    text.close()

    # for i in range(10):
    #     for j in range(10):
    #         print(lines.get((j, i), "."), end="")
    #     print("")

    count = 0
    for c in lines.values():
        count += int(c >= 2)
    print(count)


if __name__ == "__main__":
    print("Day 5")
    part1()
    print("---")
    part2()