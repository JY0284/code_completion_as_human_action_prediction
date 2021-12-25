def convert_str_to_number(x: str):
    total_stars = 0
    num_map = {'K': 1000, 'M': 1000000, 'B': 1000000000}

    if x.isdigit() or (len(x) > 1 and x[0] == '-' and x[1:].isdigit()):
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)
