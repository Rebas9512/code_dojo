class Archive:
    def __init__(self):
        self.root = {}

    def _directory(self, path):
        node = self.root
        for name in path.split("/"):
            if name:
                node = node[name]
        return node

    def mkdir(self, path: str) -> None:
        node = self.root
        for name in path.split("/"):
            if name:
                node = node.setdefault(name, {})

    def ls(self, path: str) -> list[str]:
        node = self._directory(path)
        return sorted(node)

    def addContentToFile(self, path: str, content: str) -> None:
        pass

    def readContentFromFile(self, path: str) -> str:
        pass
