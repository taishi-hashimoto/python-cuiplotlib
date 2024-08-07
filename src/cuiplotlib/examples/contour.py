import curses
import numpy as np
import time
from ..color import Colormap, Normalize
from ..axes import Axes
from cuiplotlib.logging import MQOut


def window(stdscr: curses.window):
    curses.curs_set(0)
    stdscr.nodelay(True)
    
    ax = Axes(stdscr, 2, 2, 10)
    cax = Axes(stdscr, ax.right + 2, 2, 5)
    norm = Normalize(-2, 2)
    cmap = Colormap.jet_bg()

    mqout = MQOut()
    z = np.random.normal(size=(20, 30))

    while True:
        try:
            x = np.linspace(-3, 3)
            y = np.linspace(-3, 3)
            x_g, y_g = np.meshgrid(x, y, indexing="ij")
            z1 = np.exp(-x_g**2 - y_g**2)
            z2 = np.exp(-(x_g - 1)**2 - (y_g - 1)**2)
            z_g = (z1 - z2) * 2
            ax.matrix(x, y, z_g, cmap=cmap, norm=norm)

            cax.colorbar(cmap, norm, formatter="{:.0f} dB")
            # cax.set_xlim(0, 1)
            # cax.set_xlim(-3, 3)
            # x = np.linspace(0, 1, 1)
            # y = np.linspace(-3, 3, 10)
    
            # cax.set_xlim(0, 1)
            # cax.xaxis_location = None
            # cax.yaxis_location = "right"
            # cax._datalim.update(np.nanmin(x), np.nanmin(y), np.nanmax(x), np.nanmax(y))
            # cax._set_transform()
            # # print(f"{min(x)}, {max(x)}", file=mqout)
            # # print(f"{min(y)}, {max(y)}", file=mqout)

            # cax.matrix(x, y, [y], cmap=cmap, norm=norm)

            stdscr.refresh()
            time.sleep(1)
        except KeyboardInterrupt:
             break
        
def main():
     curses.wrapper(window)
