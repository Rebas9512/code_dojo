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


def stump(x, y):
    x, y = np.asarray(x), np.asarray(y)
    threshold = best_cut(x, y)
    left_vote = np.mean(y[x <= threshold]) > 0.5
    right_vote = np.mean(y[x > threshold]) > 0.5
    return np.array([threshold, left_vote, right_vote])
