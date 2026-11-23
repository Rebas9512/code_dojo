def score_summary(scores: list[int]) -> str:
    average = sum(scores) / len(scores)
    return f"最高{max(scores)} 最低{min(scores)} 平均{average:.1f}"
