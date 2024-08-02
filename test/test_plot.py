# %%
import curses
import sys
import numpy as np
import time
from os.path import dirname, join

sys.path.insert(0, join(dirname(__file__), "..", "src"))

from cuiplotlib.axes import Axes


def window(stdscr: curses.window):
    curses.curs_set(0)
    stdscr.nodelay(True)

    ax = Axes(stdscr, 5, 3, 1, 2)
    # ax.set_ylim(0, 2)
    while True:
        try:
            stdscr.clear()
            x = np.linspace(0, 2*np.pi)
            # y = np.full_like(x, 1)
            y = 2 * x + 1
            # y = np.sin(x)
            ax.plot(x, y, "r")
            stdscr.refresh()
            time.sleep(0.1)
        except KeyboardInterrupt:
             break


if __name__ == "__main__":
     curses.wrapper(window)
# %%
