import curses
import math
import numpy as np
from scipy.interpolate import RegularGridInterpolator
from .transform import Transform
from .ticker import autoticks, StrFormatter, default_formatter
from .color import Colormap, Normalize


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
        self._yticks = None

        self._x0 = None
        self._y0 = None
        self.xaxis_formatter = default_formatter
        self.yaxis_formatter = default_formatter
        self.xaxis_location = "bottom"
        self.yaxis_location = "left"

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

    @property
    def right(self) -> int:
        return self._left + self._width
    
    @property
    def bottom(self) -> int:
        return self._top + self._height

    @property
    def top(self) -> int:
        return self._top

    @property
    def left(self) -> int:
        return self._left

    def _is_inside(self, y=None, x=None):
        y_inside = y is None or self._top <= y <= self.bottom
        x_inside = x is None or self._left <= x <= self.right
        return y_inside and x_inside

    def write(self, y: int, x: int, *args, clip=False, **kwargs):
        """Same as `self._window.addstr(y, x, *args, **kwargs)`,
        with bounds check.
        
        """
        if not clip or self._is_inside(y, x):
            self._window.addstr(int(y), int(x), *args, **kwargs)

    def _set_transform(self, top=None, left=None, height=None, width=None):
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
        if top is None:
            top = self._top
        if left is None:
            left = self._left
        if height is None:
            height = self._height
        if width is None:
            width = self._width
        self._transform = Transform(
            top, left, height, width,
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
            if self.yaxis_location == "right":
                x0 = self._xmax
            else:
                x0 = self._xmin
        else:
            x0 = self._x0
        if self._y0 is None:
            if self.xaxis_location == "top":
                y0 = self._ymax
            else:
                y0 = self._ymin
        else:
            y0 = self._y0
        xaxis_x, xaxis_y = self._transform(np.array([self._xmin, self._xmax]), y0)
        yaxis_x, yaxis_y = self._transform(x0, np.array([self._ymin, self._ymax]))
        yaxis_x = math.floor(yaxis_x)
        xaxis_y = math.ceil(xaxis_y)
        if self.xaxis_location is not None:
            # X axis.
            xmin, xmax = map(math.floor, xaxis_x)
            for x1 in range(xmin, xmax+1, 1):
                try:
                    self.write(xaxis_y, x1, "_", clip=True)
                except:
                    pass
        if self.yaxis_location is not None:
            if self.yaxis_location == "right":
                yaxis_x = self.right
            # Y axis.
            ymax, ymin = map(math.ceil, yaxis_y)
            for ypos in  range(ymin, ymax+1, 1):
                try:
                    self.write(ypos, yaxis_x, "|", clip=False)
                except:
                    pass

        # Build ticks.
        xticks, yticks = self._transform(np.array(self._xticks), np.array(self._yticks))

        if self.xaxis_location is not None:
            # X axis.
            xticklabels = self.xaxis_formatter(self._xticks)
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

        if self.yaxis_location is not None:
            if self.yaxis_location == "left":
                tickoff = yaxis_x-1
            elif self.yaxis_location == "right":
                tickoff = yaxis_x + 1
            # Y axis.
            yticklabels = self.yaxis_formatter(self._yticks)
            for ypos, ystr in zip(yticks, yticklabels):
                # Y ticks.
                ypos = math.ceil(ypos)
                try:
                    if self._is_inside(y=ypos):
                        self.write(ypos, tickoff, "_")
                except:
                    pass
                # Y tick labels.
                try:
                    if self._is_inside(y=ypos):
                        if self.yaxis_location == "left":
                            self.write(ypos + 1, yaxis_x - len(ystr), ystr)
                        elif self.yaxis_location == "right":
                            self.write(ypos + 1, yaxis_x + 1, ystr)
                except:
                    pass

    def line(
        self,
        x, y,
        c=None
    ):
        cmap = Colormap()

        self._datalim.update(np.nanmin(x), np.nanmin(y), np.nanmax(x), np.nanmax(y))
        self._set_transform()
        self.axes()

        wf, hf = self._transform(x, y)
        xx = np.linspace(self._left, self._left + self._width - 1, self._width)
        yy = np.interp(xx, wf, hf, left=np.nan, right=np.nan)

        yy0 = np.ceil(yy)
        ss = np.select((
            yy0 - yy > 2 / 3,
            yy0 - yy > 1 / 3), "`-", "_")
        for xi, yi, s in zip(xx, yy, ss):
            if np.isnan(yi) or np.isnan(xi):
                continue
            yi = math.ceil(yi)
            xi = math.floor(xi)
            if c is not None:
                # raise RuntimeError(f"{cmap[c]=}")
                self.write(yi, xi, s, cmap[c], clip=True)
            else:
                # raise RuntimeError(f"{c=}")
                self.write(yi, xi, s, clip=True)

    def matrix(self, x, y, z, cmap, norm):
        if np.ndim(x) == 2 and np.ndim(y) == 2:
            x = x[0, :]
            y = y[:, 0]
        self._datalim.update(np.nanmin(x), np.nanmin(y), np.nanmax(x), np.nanmax(y))
        self._set_transform(left=self._left+1, width=self._width-1)
        self.axes()

        wf, hf = self._transform(x, y)
        interp = RegularGridInterpolator((wf, hf), z, bounds_error=False, fill_value=None)
        xx = np.linspace(self._left+2, self._left + self._width - 1, self._width - 1)
        yy = np.linspace(self._top + 1, self._top + self._height, self._height)
        xx_g, yy_g = np.meshgrid(xx, yy)
        zz_g = interp((xx_g, yy_g))
        zz_g = np.reshape([cmap[cmap.get_color(norm(zzz))] for zzz in np.ravel(zz_g)], zz_g.shape)

        xx_g = np.floor(xx_g)
        yy_g = np.ceil(yy_g)
        cc_g = np.full_like(zz_g, " ", dtype=str)
        cc_g[-1, :] = "_"
        for xx1, yy1, zz1, cc1 in zip(xx_g.ravel(), yy_g.ravel(), zz_g.ravel(), cc_g.ravel()):
            self.write(yy1, xx1, cc1, zz1)

    def colorbar(
        self,
        cmap: Colormap,
        norm: Normalize = None,
        vmin: float = None,
        vmax: float = None,
        formatter: str = StrFormatter(),
        extend=None,
        title=None,
        orientation="vertical"
    ):
        if norm is not None:
            vmin = norm._vmin
            vmax = norm._vmax
        norm = Normalize(vmin, vmax)
        if isinstance(formatter, str):
            formatter = StrFormatter(formatter)
        self.xaxis_formatter = formatter
        self.yaxis_formatter = formatter
        if orientation.startswith("v"):
            self.xaxis_location = None
            self.yaxis_location = "right"
            self.set_xlim(0, 1)
            x = np.linspace(0, 1, 1)
            y = np.linspace(vmin, vmax)
            z = [y]
        else:
            self.xaxis_location = "bottom"
            self.yaxis_location = None
            self.set_ylim(0, 1)
            x = np.linspace(vmin, vmax)
            y = np.linspace(0, 1, 1)
            z = np.transpose([x])
        self._datalim.update(np.nanmin(x), np.nanmin(y), np.nanmax(x), np.nanmax(y))
        self._set_transform()
        self.matrix(x, y, z, cmap=cmap, norm=norm)
        
    def bar(
        self,
        x, y, y0=None, c=None
    ):
        cmap = Colormap()

        self._datalim.update(np.nanmin(x), np.nanmin(y), np.nanmax(x), np.nanmax(y))
        self._set_transform()
        
        self.axes()

        if y0 is None:
            y0 = np.zeros_like(y)

        wf, hf = self._transform(x, y)
        wf0, hf0 = self._transform(x, y0)
        xx = np.linspace(self._left, self._left+self._width, self._width)
        yy = np.interp(xx, wf, hf, left=np.nan, right=np.nan)
        yy0 = np.interp(xx, wf0, hf0, left=np.nan, right=np.nan)


        for xi, yi, yi0 in zip(xx, yy, yy0):
            if np.isnan(yi) or np.isnan(xi) or np.isnan(yi0):
                continue
            yi = math.ceil(yi)
            yi0 = math.ceil(yi0)
            xi = math.floor(xi)
            if yi0 > yi:
                yi0, yi = yi, yi0
            if c is not None:
                for y1 in range(yi0, yi+1):
                    self.write(y1, xi, "|", cmap[c], clip=True)
            else:
                for y1 in range(yi0, yi+1):
                    self.write(y1, xi, "|", clip=True)


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

