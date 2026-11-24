class IndexedRegister:
    def __init__(self):
        self.where = {}

    def insert(self, value: int) -> bool:
        if value in self.where:
            return False
        self.where[value] = len(self.where)
        return True

    def position(self, value: int) -> int:
        return self.where.get(value, -1)
