def jumps_to_exit(jumps: list[int]) -> int:
    pos = steps = 0
    while pos < len(jumps):
        pos += jumps[pos]
        steps += 1
    return steps
