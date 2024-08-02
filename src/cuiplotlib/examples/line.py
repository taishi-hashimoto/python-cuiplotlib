import curses
import numpy as np
import time
from ..axes import Axes


def window(stdscr: curses.window):
    curses.curs_set(0)
    stdscr.nodelay(True)

    axes = Axes(stdscr, 5, 3, 30, 2)
    axes.set_xlim(0, np.pi)
    # axes.set_ylim(-3, 3)@
    off = 0
    while True:
        try:
            stdscr.clear()
            off = 0
            # off += 2*np.pi / 100
            x = np.linspace(0, 2*np.pi)
            y = np.sin(x - off)
            
            axes.line(x, y)
            stdscr.refresh()
            time.sleep(0.1)
        except KeyboardInterrupt:
             break
        
def main():
     curses.wrapper(window)
