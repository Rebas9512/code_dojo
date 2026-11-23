class Tag:
    def __init__(self, owner: str):
        ____ = owner


def read_tag(owner: str) -> str:
    tag = Tag(owner)
    return tag.owner
