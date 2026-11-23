class Ticket:
    def __init__(self, seat):
        self.seat = seat


first = Ticket(2)
second = Ticket(7)
second.seat = 9
print(first.seat)
print(second.seat)
