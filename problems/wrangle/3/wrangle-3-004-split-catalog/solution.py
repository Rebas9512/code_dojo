import pandas as pd


def quantities(shelves, stock):
    t = pd.DataFrame({'shelf': shelves, 'stock': stock})
    return t['stock']
