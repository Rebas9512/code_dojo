def pack(bead, bag=[]):
    bag.append(bead)
    return len(bag)


print(pack("red"))
print(pack("blue", bag=[]))
print(pack("green"))
