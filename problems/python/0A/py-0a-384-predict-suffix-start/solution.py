def read(cards, i):
    if i == len(cards):
        print("空")
        return
    print(cards[i])
    read(cards, i + 1)


read([3, 1, 4], 1)
