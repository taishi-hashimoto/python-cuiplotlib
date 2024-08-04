import curses
import numpy as np
import time
from ..color import Colormap, Normalize
from ..axes import Axes


def window(stdscr: curses.window):
    curses.curs_set(0)
    stdscr.nodelay(True)
    
    ax = Axes(stdscr, 2, 2, 5)
    cax = Axes(stdscr, ax.right + 2, 2)
    # cax.set_xlim(0, 1)
    # cax.set_xlim(-3, 3)
    cax._datalim.update(0, -3, 1, 3)
    cax._set_transform()
    x = np.linspace(0, 1, 1)
    y = np.linspace(-3, 3)

    norm = Normalize(-3, 3)
    cmap = Colormap()
    cax.matrix(x, y, ([y]), cmap=cmap, norm=norm)
    
    while True:
        try:
            nx = 20
            ny = 30
            z = np.random.normal(size=(20, 30))
            x = np.linspace(-5, 5, nx)
            y = np.linspace(-5, 5, ny)
            ax.matrix(x, y, z, cmap=Colormap(), norm=norm)

            cax.axes()
            stdscr.refresh()
            time.sleep(1)
        except KeyboardInterrupt:
             break
        
def main():
     curses.wrapper(window)
