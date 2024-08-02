import curses
import math
import numpy as np
from .transform import Transform
from .ticker import autoticks, autoformat, default_formatter


class Bounds:
    def __init__(self, xmin=None, ymin=None, xmax=None, ymax=None):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax

    def update(self, xmin, ymin, xmax, ymax):
        if xmin is not None:
            if self.xmin is None:
                self.xmin = xmin
            else:
                self.xmin = min(self.xmin, xmin)
        if xmax is not None:
            if self.xmax is None:
                self.xmax = xmax
            else:
                self.xmax = max(self.xmax, xmax)
        if ymin is not None:
            if self.ymin is None:
                self.ymin = ymin
            else:
                self.ymin = min(self.ymin, ymin)
        if ymax is not None:
            if self.ymax is None:
                self.ymax = ymax
            else:
                self.ymax = max(self.ymax, ymax)


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
        # datalim
        self._datalim = Bounds()
        # autolim
        self._autolim = Bounds()
        # User specified limits
        self._userlim = Bounds()
        self._transform = None
        self._xticks = None
        self._xformatter = default_formatter
        self._yformatter = default_formatter
        self._yticks = None
        self._x0 = None
        self._y0 = None

    @staticmethod
    def _get_first_valid(*args):
        for each in args:
            if each is not None:
                return each

    @property
    def _xmin(self) -> float:
        return self._get_first_valid(self._userlim.xmin, self._autolim.xmin)

    @property
    def _xmax(self) -> float:
        return self._get_first_valid(self._userlim.xmax, self._autolim.xmax)

    @property
    def _ymin(self) -> float:
        return self._get_first_valid(self._userlim.ymin, self._autolim.ymin)

    @property
    def _ymax(self) -> float:
        return self._get_first_valid(self._userlim.ymax, self._autolim.ymax)

    def _is_inside(self, y=None, x=None):
        y_inside = y is None or self._top <= y <= self._top + self._height
        x_inside = x is None or self._left <= x <= self._left + self._width
        return y_inside and x_inside

    def write(self, y: int, x: int, *args, clip=False, **kwargs):
        """Same as `self._window.addstr(y, x, *args, **kwargs)`,
        with bounds check.
        
        """
        if not clip or self._is_inside(y, x):
            self._window.addstr(y, x, *args, **kwargs)

    def _set_transform(self):
        # First compute x and y ticks.
        try:
            self._xticks = autoticks(
                self._get_first_valid(self._userlim.xmin, self._datalim.xmin),
                self._get_first_valid(self._userlim.xmax, self._datalim.xmax))
            xmin = min(self._xticks)
            xmax = max(self._xticks)
        except:
            xmin = None
            xmax = None
        try:
            self._yticks = autoticks(
                self._get_first_valid(self._userlim.ymin, self._datalim.ymin),
                self._get_first_valid(self._userlim.ymax, self._datalim.ymax))
            ymin = min(self._yticks)
            ymax = max(self._yticks)
        except:
            ymin = None
            ymax = None

        self._autolim.update(xmin, ymin, xmax, ymax)
        self._transform = Transform(
            self._top, self._left, self._height, self._width,
            self._xmin, self._xmax,
            self._ymin, self._ymax)

    def set_xlim(self, xmin=None, xmax=None):
        if xmin is not None:
            self._userlim.xmin = xmin
        if xmax is not None:
            self._userlim.xmax = xmax
        self._set_transform()

    def set_ylim(self, ymin=None, ymax=None):
        if ymin is not None:
            self._userlim.ymin = ymin
        if ymax is not None:
            self._userlim.ymax = ymax
        self._set_transform()

    def axes(self):
        # Axes
        if self._x0 is None:
            x0 = self._xmin
        else:
            x0 = self._x0
        if self._y0 is None:
            y0 = self._ymin
        else:
            y0 = self._y0
        
        xaxis_x, xaxis_y = self._transform(np.array([self._xmin, self._xmax]), y0)
        yaxis_x, yaxis_y = self._transform(x0, np.array([self._ymin, self._ymax]))
        yaxis_x = math.floor(yaxis_x)
        xaxis_y = math.ceil(xaxis_y)
        # X axis.
        xmin, xmax = map(math.floor, xaxis_x)
        for x1 in range(xmin, xmax+1, 1):
            try:
                self.write(xaxis_y, x1, "_", clip=True)
            except:
                pass
        # Y axis.
        ymax, ymin = map(math.ceil, yaxis_y)
        for ypos in  range(ymin, ymax+1, 1):
            try:
                self.write(ypos, yaxis_x, "|", clip=True)
            except:
                pass

        # Build ticks.
        xticks, yticks = self._transform(np.array(self._xticks), np.array(self._yticks))

        # X axis.
        xticklabels = self._xformatter(self._xticks)
        for xpos, xstr in zip(xticks.astype(int), xticklabels):
            # X ticks.
            try:
                if self._is_inside(x=xpos):
                    self.write(xaxis_y + 1, xpos, "|")
            except:
                pass
            # X tick labels.
            try:
                if self._is_inside(x=xpos):
                    self.write(xaxis_y + 1, xpos+1, xstr)
            except:
                pass

        # Y axis.
        yticklabels = self._yformatter(self._yticks)
        for ypos, ystr in zip(yticks, yticklabels):
            # Y ticks.
            ypos = math.ceil(ypos)
            try:
                if self._is_inside(y=ypos):
                    self.write(ypos, yaxis_x-1, "_")
            except:
                pass
            # Y tick labels.
            try:
                if self._is_inside(y=ypos):
                    self.write(ypos + 1, yaxis_x - len(ystr), ystr)
            except:
                pass

    def line(
        self,
        x, y
    ):
        self._datalim.update(np.min(x), np.min(y), np.max(x), np.max(y))
        self._set_transform()
        
        self.axes()

        wf, hf = self._transform(x, y)
        xx = np.linspace(self._left, self._left+self._width, self._width)
        yy = np.interp(xx, wf, hf, left=np.nan, right=np.nan)

        yy0 = np.ceil(yy)
        cc = np.select((
            yy0 - yy > 2/3,
            yy0 - yy > 1/3), "`-", ".")
        for xi, yi, c in zip(xx, yy, cc):
            try:
                self.write(math.ceil(yi), math.floor(xi), c)
            except:
                pass
