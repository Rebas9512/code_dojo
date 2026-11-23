def read(cards, i):
    if i == len(cards):
        print("empty")
        return
    print(cards[i])
    read(cards, i + 1)


read([3, 1, 4], 1)
