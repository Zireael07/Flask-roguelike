
def tiles_distance_to(start, target):
    x_diff = start[0] - target[0]
    y_diff = start[1] - target[1]

    ##ensure always positive values
    if x_diff < 0:
        x_diff = x_diff * -1

    if y_diff < 0:
        y_diff = y_diff * -1

    return max(x_diff, y_diff)