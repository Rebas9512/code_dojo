def check(args, expected, actual):
    n, prerequisites = args
    if not isinstance(actual, list):
        return False
    if expected == []:
        return actual == []
    if len(actual) != n or any(type(x) is not int for x in actual) or set(actual) != set(range(n)):
        return False
    position = {course: i for i, course in enumerate(actual)}
    return all(position[before] < position[course] for course, before in prerequisites)
