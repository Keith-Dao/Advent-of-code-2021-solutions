filename = "day6.txt"


def numChildren(initial, end=256):
    if initial >= end:
        return 0
    return (end - initial - 1) // 7 + 1


def solve(days):
    text = open(filename)

    count = 0
    queue = set()
    freq = {}
    for initial in text.readline().split(","):
        initial = int(initial)
        num = numChildren(initial, days)
        count += num + 1
        for i in range(num):
            offset = initial + 9 + i * 7
            queue.add(offset)
            freq[offset] = freq.get(offset, 0) + 1
    text.close()

    while len(queue) != 0:
        initial = queue.pop()
        num = numChildren(initial, days)
        times = freq.pop(initial)
        count += times * num
        for i in range(num):
            offset = initial + 9 + i * 7
            queue.add(offset)
            freq[offset] = freq.get(offset, 0) + times

    print(count)


if __name__ == "__main__":
    print("Part 1")
    solve(80)
    print("---")
    print("Part 2")
    solve(256)