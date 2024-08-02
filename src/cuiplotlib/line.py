"Bar plot."

import numpy as np
import math


def compute_position(xmax, ymax, x0, y0, width=0, height=0, ha="left", va="top"):
    if va == "bottom":
        y = ymax - y0 - height
    elif va == "top":
        y = y0
    else:
        raise ValueError(va)
    if ha == "right":
        x = xmax - x0 - width
    elif ha == "left":
        x = x0
    else:
        raise ValueError(ha)
    return x, y

