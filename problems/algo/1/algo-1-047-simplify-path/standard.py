def simplify_path(path: str) -> str:
    parts = []
    for name in path.split('/'):
        if name == '..':
            if parts:
                parts.pop()
        elif name and name != '.':
            parts.append(name)
    return '/' + '/'.join(parts)
