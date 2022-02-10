filename = "day1.txt"


def part1():
    print("Part 1")
    text = open(filename)
    prev = None
    count = 0
    for num in text:
        num = int(num)
        if prev and prev < num:
            count += 1
        prev = num
    text.close()
    print(count)


def part2():
    print("Part 2")
    text = open(filename)
    window = []
    for _ in range(3):
        num = int(text.readline())
        window.append(num)

    count = 0
    for num in text:
        num = int(num)
        if num > window.pop(0):
            count += 1
        window.append(num)

    print(count)


if __name__ == "__main__":
    print("Day 1")
    part1()
    print("---")
    part2()