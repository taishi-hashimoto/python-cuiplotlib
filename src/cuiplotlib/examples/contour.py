import curses
import numpy as np
import time
from ..color import Colormap, Normalize
from ..axes import Axes
from cuiplotlib.logging import MQOut


def window(stdscr: curses.window):
    curses.curs_set(0)
    stdscr.nodelay(True)
    
    ax = Axes(stdscr, 2, 2, 5)
    cax = Axes(stdscr, ax.right + 2, 2)
    norm = Normalize(-3, 3)
    cmap = Colormap()
    
    cax.set_xlim(0, 1)

    mqout = MQOut()

    while True:
        try:
            nx = 20
            ny = 30
            z = np.random.normal(size=(20, 30))
            x = np.linspace(-5, 5, nx)
            y = np.linspace(-5, 5, ny)
            ax.matrix(x, y, z, cmap=Colormap(), norm=norm)

            # cax.set_xlim(0, 1)
            # cax.set_xlim(-3, 3)
            x = np.linspace(0, 1, 2)
            y = np.linspace(-3, 3, 10)
            cax._datalim.update(np.nanmin(x), np.nanmin(y), np.nanmax(x), np.nanmax(y))
            cax._set_transform()
            print(f"{min(x)}, {max(x)}", file=mqout)
            print(f"{min(y)}, {max(y)}", file=mqout)

            cax.axes()

            cax.matrix(x, y, [y, y], cmap=cmap, norm=norm)

            stdscr.refresh()
            time.sleep(1)
        except KeyboardInterrupt:
             break
        
def main():
     curses.wrapper(window)
