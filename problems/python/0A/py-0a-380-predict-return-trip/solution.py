def visit(floor):
    print("enter", floor)
    if floor == 0:
        return
    visit(floor - 1)
    print("return", floor)


visit(2)
