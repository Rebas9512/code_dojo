boxes = {}
for color, number in [["red", 2], ["blue", 1], ["red", 3]]:
    if color not in boxes:
        boxes[color] = []
    boxes[color].append(number)
print(boxes["red"])
