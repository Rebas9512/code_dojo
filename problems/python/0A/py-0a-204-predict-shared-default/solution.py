def pack(bead, bag=[]):
    bag.append(bead)
    return len(bag)


print(pack("红"))
print(pack("蓝", bag=[]))
print(pack("绿"))
