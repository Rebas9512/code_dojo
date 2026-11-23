boxes = {}
for color, number in [["红", 2], ["蓝", 1], ["红", 3]]:
    if color not in boxes:
        boxes[color] = []
    boxes[color].append(number)
print(boxes["红"])
