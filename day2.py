text = open("day2.txt")

print("Part 1")
x = y = 0
actions = {
    "forward": lambda z: (x + int(z), y),
    "down": lambda z: (x, y + int(z)),
    "up": lambda z: (x, y - int(z)),
}

for line in text:
    action, val = line.split(" ")
    x, y = actions[action](val)

print(x * y)
text.close()

text = open("day2.txt")

print("Part 2")
x = y = aim = 0
actions = {
    "forward": lambda z: (x + int(z), y + aim * int(z), aim),
    "down": lambda z: (x, y, aim + int(z)),
    "up": lambda z: (x, y, aim - int(z)),
}

for line in text:
    action, val = line.split(" ")
    x, y, aim = actions[action](val)

print(x * y)
text.close()