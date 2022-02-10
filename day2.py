filename = "day2.txt"


def part1():
    print("Part 1")
    x = y = 0
    actions = {
        "forward": lambda z: (x + int(z), y),
        "down": lambda z: (x, y + int(z)),
        "up": lambda z: (x, y - int(z)),
    }

    text = open(filename)
    for line in text:
        action, val = line.split(" ")
        x, y = actions[action](val)
    text.close()

    print(x * y)


def part2():
    print("Part 2")
    x = y = aim = 0
    actions = {
        "forward": lambda z: (x + int(z), y + aim * int(z), aim),
        "down": lambda z: (x, y, aim + int(z)),
        "up": lambda z: (x, y, aim - int(z)),
    }

    text = open(filename)
    for line in text:
        action, val = line.split(" ")
        x, y, aim = actions[action](val)
    text.close()

    print(x * y)


if __name__ == "__main__":
    print("Day 2")
    part1()
    print("---")
    part2()