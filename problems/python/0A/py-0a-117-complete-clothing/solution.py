def clothing(temp: int) -> str:
    if temp >= 30:
        return "T-shirt"
    elif temp >= 15:
        return "jacket"
    else:
        return "down jacket"
