text = open("day3.txt")

print("Part 1")
entries = n = 0
counter = []
for line in text:
    if entries == 0:
        n = len(line) - 1
        counter = [0] * n

    for i in range(n):
        counter[i] += int(line[i])

    entries += 1

text.close()

print(counter, entries)
gamma = 0
for i in range(n):
    gamma <<= 1
    gamma += int(counter[i] > entries / 2)

epsilon = ~gamma & ((1 << n) - 1)

print(gamma * epsilon)

print("Part 2")
