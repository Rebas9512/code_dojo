from collections import deque

line = deque([4, 8])
line.append(1)
print(line.popleft())
line.append(4)
print(line[0])
print(list(line))
