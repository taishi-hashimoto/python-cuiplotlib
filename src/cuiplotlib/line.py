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
        yy = (y - self._ymin) / (self._ymax - self._ymin) * -self._height + self._top + self._height - 0.5
        return xx, yy


class Axes:
    def __init__(
        self,
        window: curses.window,
        left_margin=0, bottom_margin=0,
        right_margin=0, top_margin=0
    ):
        ymax, xmax = window.getmaxyx()
        width = xmax - left_margin - right_margin
        height = ymax - bottom_margin - top_margin
        bottom_margin += 1
        width -= 1
        height -= 1
        self._window = window
        self._top = ymax - bottom_margin - height
        self._left = left_margin
        self._width = width
        self._height = height
        self._xmin = None
        self._xmax = None
        self._ymin = None
        self._ymax = None
        self._transform = None
        self._x0 = None
        self._y0 = None

    def _set_transform(self, xmin=None, ymin=None, xmax=None, ymax=None):
        if xmin is not None and self._xmin is None:
            self._xmin = xmin
        if xmax is not None and self._xmax is None:
            self._xmax = xmax
        if ymin is not None and self._ymin is None:
            self._ymin = ymin
        if ymax is not None and self._ymax is None:
            self._ymax = ymax
        self._transform = Transform(
            self._top, self._left, self._height, self._width,
            self._xmin, self._xmax, self._ymin, self._ymax)

    def set_xlim(self, xmin=None, xmax=None):
        if xmin is not None:
            self._xmin = xmin
        if xmax is not None:
            self._xmax = xmax
        self._set_transform()

    def set_ylim(self, ymin=None, ymax=None):
        if ymin is not None:
            self._ymin = ymin
        if ymax is not None:
            self._ymax = ymax
        self._set_transform()

    def axes(
        self,
    ):
        # Axes
        if self._x0 is None:
            x0 = self._xmin
        else:
            x0 = self._x0
        if self._y0 is None:
            y0 = self._ymin
        else:
            y0 = self._y0
        xaxis_x, xaxis_y = self._transform((self._xmin, self._xmax), y0)
        yaxis_x, yaxis_y = self._transform(x0, (self._ymin, self._ymax))

        xmin, xmax = np.fix(xaxis_x)
        for x1 in np.arange(xmin, xmax+1, 1):
            try:
                self._window.addstr(math.ceil(xaxis_y), int(x1), "_")
            except:
                pass
        ymax, ymin = np.ceil(yaxis_y)
        for y1 in  np.arange(ymin, ymax+1, 1):
            try:
                self._window.addstr(math.ceil(y1), int(yaxis_x), "|")
            except:
                pass

    def line(
        self,
        x, y
    ):
        self._set_transform(np.min(x), np.min(y), np.max(x), np.max(y))
        
        self.axes()

        wf, hf = self._transform(x, y)
        xx = np.linspace(self._left, self._left+self._width, self._width)
        yy = np.interp(xx, wf, hf)

        yy0 = np.ceil(yy)
        cc = np.select((
            yy0 - yy > 2/3,
            yy0 - yy > 1/3), "`-", ".")
        for xi, yi, c in zip(xx, yy, cc):
            try:
                self._window.addstr(math.ceil(yi), math.floor(xi), c)
            except:
                pass
