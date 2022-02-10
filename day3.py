filename = "day3.txt"
text = open(filename)

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
    gamma += int(counter[i] >= entries // 2)

epsilon = ~gamma & ((1 << n) - 1)

print(gamma * epsilon)

print("Part 2")
text = open(filename)
poss_oxy, poss_co2 = [], []
msb = int(counter[0] >= entries // 2)

for line in text:
    if int(line[0]) == msb:
        poss_oxy.append(int(line, 2))
    else:
        poss_co2.append(int(line, 2))
text.close()

mask = 1 << (n - 1)
while len(poss_oxy) != 1:
    mask >>= 1
    zeros, ones = [], []
    for num in poss_oxy:
        if num & mask:
            ones.append(num)
        else:
            zeros.append(num)

    if len(zeros) > len(ones):
        poss_oxy = zeros
    else:
        poss_oxy = ones

mask = 1 << (n - 1)
while len(poss_co2) != 1:
    mask >>= 1
    zeros, ones = [], []
    for num in poss_co2:
        if num & mask:
            ones.append(num)
        else:
            zeros.append(num)

    if len(zeros) <= len(ones):
        poss_co2 = zeros
    else:
        poss_co2 = ones

print(poss_oxy[0] * poss_co2[0])
