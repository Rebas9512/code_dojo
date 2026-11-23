def storage(t):
    numbers = t['n'].astype('Int64')
    return [str(numbers.dtype), len(numbers.dropna())]
