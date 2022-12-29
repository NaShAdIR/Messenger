def fix(message):
    if len(message) < 6:
        size = .22
        halign = "center"
    elif len(message) < 11:
        size = .32
        halign = "center"
    elif len(message) < 16:
        size = .45
        halign = "center"
    elif len(message) < 21:
        size = .58
        halign = "center"
    elif len(message) < 26:
        size = .71
        halign = "center"
    else:
        size = .77
        halign = "left"

    return (size, halign)