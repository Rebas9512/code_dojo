import numpy as np


def audit_totals(rows, positions):
    picked = np.array(rows)[positions]
    return np.sum(picked, axis=1)
