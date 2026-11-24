def pre_branch(x, norm, branch):
    update = branch(norm(x))
    return x + update
