"Bar plot."

import curses
from .transform import linear_transform
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


class Transform:
    def __init__(
        self,
        top, left,  # Top left corner of the axes in the window.
        height, width,  # Axes size in the window.
        xmin, xmax,  # Data X range.
        ymin, ymax  # Data Y range.
    ):
        self._top = top
        self._left = left
        self._width = width
        self._height = height
        self._xmin = xmin
        self._xmax = xmax
        self._ymin = ymin
        self._ymax = ymax

    def __call__(self, x, y):
        xx = (x - self._xmin) / (self._xmax - self._xmin) * self._width + self._left
        yy = (y - self._ymin) / (self._ymax - self._ymin) * -self._height + self._top + self._height
        return xx, yy


def line(
    window: curses.window,
    x0, y0,
    width,
    height, 
    x, y,
    ha="left",
    va="top"
):
    ymax, xmax = window.getmaxyx()
    x0, y0 = compute_position(xmax, ymax, x0, y0, ha=ha, va=va, width=width, height=height)

    transform = Transform(y0, x0, height, width, 0, 2*np.pi, -1, 1)
    # Axes
    xaxis_x, xaxis_y = transform(np.linspace(0, 2*np.pi, 2000), 0)
    yaxis_x, yaxis_y = transform(0, np.linspace(-1, 1, 2000))
    for x1 in xaxis_x:
        window.addstr(int(xaxis_y), int(x1), "_")
    for y1 in yaxis_y:
        window.addstr(int(y1), int(yaxis_x), "|")
    window.addstr(int(xaxis_y), int(yaxis_x), "|")
    window.addstr(ymax-1, xmax-2, "o")

    wf, hf = transform(x, y)
    # raise ValueError(f"{xx}, {yy}")
    # xx, yy = compute_position(xmax-1, ymax-1, xx, yy, xmax-2, ymax-2)
    # np.interp(np.arange())
    # raise ValueError(f"{np.around((hf - np.floor(hf)), 1)}, {hf}")
    xx = np.linspace(x0, x0+width, width)
    yy = np.interp(xx, wf, hf)
    
    yy0 = np.ceil(yy)
    cc = np.select((
        yy0 - yy > 2/3,
        yy0 - yy > 1/3), "`-", ".")
    for xi, yi, c in zip(xx, yy, cc):
            window.addstr(math.ceil(yi), math.floor(xi), c)
