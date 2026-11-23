class Codec:
    def serialize(self, root: TreeNode | None) -> str:
        pass

    def deserialize(self, text: str) -> TreeNode | None:
        pass

def run_case(root: TreeNode | None) -> TreeNode | None:
    text = Codec().serialize(root)
    assert isinstance(text, str), '编码结果应为字符串'
    return Codec().deserialize(text)
