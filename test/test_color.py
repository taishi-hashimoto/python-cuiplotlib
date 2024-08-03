import math
import curses
import time
import numpy as np
from cuiplotlib.axes import Axes
from cuiplotlib.color2 import Normalize, Colormap

from scipy.interpolate import RegularGridInterpolator


def window(stdscr: curses.window):
    curses.curs_set(0)
    stdscr.nodelay(True)


    cmap = Colormap()
    norm = Normalize(-3, 3)


    self = Axes(stdscr, 5, 3, 30, 2)
    # axes.set_xlim(0, np.pi)
    # axes.set_ylim(-3, 3)
    off = 0
    while True:
        try:
            stdscr.clear()
            # dx, dy = 0.15, 0.05
            # y, x = np.mgrid[-3:3+dy:dy, -3:3+dx:dx]
            # z = (1 - x/2 + x**5 + y**3) * np.exp(-x**2 - y**2)
            x = np.linspace(-3, 3)
            y = np.linspace(-3, 3)
            X, Y = np.meshgrid(x, y, indexing="ij")
            Z1 = np.exp(-X**2 - Y**2)
            Z2 = np.exp(-(X * 10)**2 - (Y * 10)**2)
            z = Z1 + 50 * Z2

            # z = np.random.normal(size=(20, 10))
            # z = z[:-1, :-1]
            # z_min, z_max = -abs(z).max(), abs(z).max()
            self._datalim.update(np.nanmin(x), np.nanmin(y), np.nanmax(x), np.nanmax(y))
            self._set_transform()
            self.axes()

            wf, hf = self._transform(x, y)
            interp = RegularGridInterpolator((wf, hf), z, bounds_error=False, fill_value=None)
            xx = np.linspace(self._left, self._left+self._width-1, self._width)
            yy = np.linspace(self._top+1, self._top+self._height, self._height)
            xx_g, yy_g = np.meshgrid(xx, yy)
            # yy = interp(xx, wf, hf, left=np.nan, right=np.nan)
            zz = interp((xx_g, yy_g))
            zz1 = [cmap[cmap.get_color(norm(zzz))] for zzz in np.ravel(zz)]
            zz1 = np.reshape(zz1, zz.shape)
            for xx1, yy1, zz1 in zip(xx_g.ravel(), yy_g.ravel(), zz1.ravel()):
                yy1 = math.ceil(yy1)
                xx1 = math.floor(xx1)
                stdscr.addstr(yy1, xx1, "■", zz1)
            stdscr.refresh()
            time.sleep(0.1)
        except KeyboardInterrupt:
             break


if __name__ == "__main__":
    curses.wrapper(window)
