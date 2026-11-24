import pandas as pd


def quantities(shelves, stock):
    table = pd.DataFrame({'shelf': shelves, 'stock': stock})
    return table['stock']
