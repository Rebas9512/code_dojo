class Account:
    def __init__(self, start: int):
        self.money = start

    def deposit(self, amount: int) -> None:
        self.money += amount

    def withdraw(self, amount: int) -> bool:
        if amount > self.money:
            return False
        self.money -= amount
        return True

    def balance(self) -> int:
        return self.money
