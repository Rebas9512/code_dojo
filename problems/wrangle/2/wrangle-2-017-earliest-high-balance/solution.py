import numpy as np


def peak_balance(changes):
    a = np.array(changes)
    clean = np.where(a == -999, 0, a)
    balances = np.cumsum(clean)
    return int(np.argmax(balances))
