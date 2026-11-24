import numpy as np


def peak_balance(changes):
    amounts = np.array(changes)
    valid_changes = np.where(amounts == -999, 0, amounts)
    balances = np.cumsum(valid_changes)
    return int(np.argmax(balances))
