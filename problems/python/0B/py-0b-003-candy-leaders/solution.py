def candy_leaders(candies: list[int], extra: int) -> list[bool]:
    highest = max(candies)
    leaders = []
    for count in candies:
        leaders.append(count + extra >= highest)
    return leaders
