class Archive:
    def __init__(self):
        self.root = {}

    def _node(self, path):
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
        node = self._node(path)
        if isinstance(node, list):
            return [path.rsplit("/", 1)[-1]]
        return sorted(node)

    def addContentToFile(self, path: str, content: str) -> None:
        parent, _, name = path.rpartition("/")
        directory = self._node(parent)
        directory.setdefault(name, []).append(content)

    def readContentFromFile(self, path: str) -> str:
        return "".join(self._node(path))
