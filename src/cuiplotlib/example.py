import curses
import numpy as np
import time
from .colorbar import Colormap, Colorbar, Normalize


def window(stdscr: curses.window):
    curses.curs_set(0)
    stdscr.nodelay(True)

    ymax, xmax = stdscr.getmaxyx()


    cmap = Colormap(under=curses.COLOR_BLACK)
    
    while True:
        try:
            data = np.random.normal(size=(ymax-3, xmax))
            norm = Normalize(-3, 3)
            ny, nx = data.shape
            for iy in range(ny):
                for ix in range(nx):
                        stdscr.addstr(iy, ix, "■", cmap(norm(data[iy, ix])))
            Colorbar(stdscr, ymax, xmax, cmap=cmap, norm=norm, title="Standard normal", formatter="{:.0f}")
            stdscr.refresh()
            time.sleep(1)
        except KeyboardInterrupt:
             break
        
def main():
     curses.wrapper(window)
