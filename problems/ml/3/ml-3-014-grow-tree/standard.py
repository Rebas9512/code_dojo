import numpy as np


def best_cut(x, y):
    values, groups, counts = np.unique(x, return_inverse=True, return_counts=True)
    positive_groups = groups[y == 1]
    positives = np.bincount(positive_groups, minlength=len(values)).tolist()
    counts = counts.tolist()
    left_size = left_positive = 0
    best_num, best_den = np.inf, 1
    for i in range(len(values) - 1):
        left_size += counts[i]
        left_positive += positives[i]
        right_size = len(y) - left_size
        right_positive = len(positive_groups) - left_positive

        # 子组的加权基尼与「正例数 × 负例数 / 组大小」成正比。
        left_pairs = left_positive * (left_size - left_positive)
        right_pairs = right_positive * (right_size - right_positive)
        numerator = left_pairs * right_size + right_pairs * left_size
        denominator = left_size * right_size
        if numerator * best_den < best_num * denominator:
            best_num, best_den = numerator, denominator
            threshold = (values[i] + values[i + 1]) / 2
    return threshold


def grow(x, y, depth):
    x, y = np.asarray(x), np.asarray(y)
    if depth == 0 or np.all(x == x[0]) or np.all(y == y[0]):
        return [[0.0, float(np.mean(y) > 0.5)]]

    threshold = best_cut(x, y)
    left = x <= threshold
    right = x > threshold
    left_tree = grow(x[left], y[left], depth - 1)
    right_tree = grow(x[right], y[right], depth - 1)
    return [[1.0, float(threshold)]] + left_tree + right_tree
