def score_summary(scores: list[int]) -> str:
    average = sum(scores) / len(scores)
    return f"max{max(scores)} min{min(scores)} avg{average:.1f}"
