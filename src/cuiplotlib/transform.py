
def linear_transform(xmin, xmax, ymin, ymax, x, y):
    xx = (x - min(x)) / (max(x) - min(x)) * (xmax - xmin) + xmin
    yy = (y - min(y)) / (max(y) - min(y)) * (ymax - ymin) + ymin
    return xx, yy
