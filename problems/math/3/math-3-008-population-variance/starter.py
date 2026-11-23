def population_variance(values: list[float]) -> float:
    mean = sum(values)/len(values)
    square_sum = sum((v-mean)**2 for v in values)
    return square_sum / ____
