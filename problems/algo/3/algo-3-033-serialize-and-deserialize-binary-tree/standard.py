class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        parts = []
        stack = [root]
        while stack:
            node = stack.pop()
            if node is None:
                parts.append('#')
            else:
                parts.append(str(node.val))
                stack.extend([node.right, node.left])
        return ','.join(parts)

    def deserialize(self, text: str) -> TreeNode | None:
        parts = text.split(',')
        index = 0

        def read():
            nonlocal index
            token = parts[index]
            index += 1
            if token == '#':
                return None
            return TreeNode(int(token), read(), read())

        return read()


def run_case(root: TreeNode | None) -> TreeNode | None:
    text = Codec().serialize(root)
    assert isinstance(text, str), '编码结果应为字符串'
    return Codec().deserialize(text)
