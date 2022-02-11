filename = "day7.txt"


def quickselect(nums, k):
    pivot = nums[0]
    lower, higher = [], []

    for i in range(1, len(nums)):
        num = nums[i]
        if num < pivot:
            lower.append(num)
        elif num > pivot:
            higher.append(num)

    if k < len(lower):
        return quickselect(lower, k)
    elif k > len(nums) - len(higher) - 1:
        return quickselect(higher, k - len(nums) + len(higher))
    else:
        return pivot


def findMedian(nums):
    n = len(nums)
    if n % 2 == 1:
        return quickselect(nums, n // 2)
    else:
        return (
            quickselect(nums, n // 2 - 1)
            + quickselect(nums, n // 2)
        ) // 2


def getCrabs():
    text = open(filename)

    crabs = []
    for num in text.readline().split(","):
        num = int(num)
        crabs.append(num)
    text.close()

    return crabs


def part1(crabs):

    print("Part 1")
    min_pos = findMedian(crabs)
    cost = 0
    for pos in crabs:
        cost += abs(min_pos - pos)

    print(cost)


def part2(crabs):

    print("Part 2")
    min_pos = sum(crabs) // len(crabs)
    print(min_pos)
    cost = 0
    for pos in crabs:
        n = abs(min_pos - pos)
        cost += n * (n + 1) // 2

    print(cost)


if __name__ == "__main__":
    print("Day 7")
    crabs = getCrabs()
    part1(crabs)
    print("---")
    part2(crabs)