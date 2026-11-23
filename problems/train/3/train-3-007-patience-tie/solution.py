best = 8
wait = 0
for loss in [7, 7, 9, 6, 6]:
    if loss < best:
        best, wait = loss, 0
    else:
        wait += 1
print(best, wait)
