class Ledger:
    entries = []

    def deposit(self, amount):
        self.entries.append(amount)


a = Ledger()
b = Ledger()
a.deposit(6)
print(a.entries)
print(b.entries)
