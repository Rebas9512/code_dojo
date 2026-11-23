class Entry:
    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev = self.next = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.by_key = {}
        self.front = Entry(0, 0)
        self.back = Entry(0, 0)
        self.front.next = self.back
        self.back.prev = self.front

    def _unlink(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node):
        first = self.front.next
        node.prev, node.next = self.front, first
        self.front.next = first.prev = node

    def get(self, key: int) -> int:
        node = self.by_key.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._add_front(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self.by_key.get(key)
        if node is not None:
            self._unlink(node)
            node.value = value
        else:
            node = Entry(key, value)
            self.by_key[key] = node
        self._add_front(node)
        if len(self.by_key) > self.capacity:
            oldest = self.back.prev
            self._unlink(oldest)
            del self.by_key[oldest.key]
