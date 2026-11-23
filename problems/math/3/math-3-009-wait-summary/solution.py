def wait_summary(values: list[float]) -> list[float]:
    mean = sum(values)/len(values)
    variance = sum((v-mean)**2 for v in values)/len(values)
    return [mean, variance, variance**0.5]
