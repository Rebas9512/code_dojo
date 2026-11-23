def visit(floor):
    print("到", floor)
    if floor == 0:
        return
    visit(floor - 1)
    print("回", floor)


visit(2)
