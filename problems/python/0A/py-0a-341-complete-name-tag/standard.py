class Tag:
    def __init__(self, owner: str):
        self.owner = owner


def read_tag(owner: str) -> str:
    tag = Tag(owner)
    return tag.owner
