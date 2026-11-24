def load_data(n):
    with (DATA_DIR / "points.csv").open() as source:
        return [[int(value) for value in row.split(",")] for row in source.readlines()[:n]]
