class MyCircularQueue:
    def __init__(self, k: int):
        self.capacity = k
        self.size = 0
        self.dummy = ListNode()
        self.dummy.next = self.dummy
        self.tail = self.dummy

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        node = ListNode(value, self.dummy)
        self.tail.next = node
        self.tail = node
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.dummy.next = self.dummy.next.next
        self.size -= 1
        if self.isEmpty():
            self.tail = self.dummy
        return True

    def Front(self) -> int:
        return -1 if self.isEmpty() else self.dummy.next.val

    def Rear(self) -> int:
        return -1 if self.isEmpty() else self.tail.val

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity
