def clothing(temp: int) -> str:
    if temp >= 30:
        return "短袖"
    elif temp >= 15:
        return "外套"
    else:
        return "羽绒服"
