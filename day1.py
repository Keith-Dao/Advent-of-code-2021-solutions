text = open("day1.txt")

print("Part 1")
prev = None
count = 0
for num in text:
    num = int(num)
    if prev and prev < num:
        count += 1
    prev = num
print(count)
text.close()

text = open("day1.txt")
print("Part 2")
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