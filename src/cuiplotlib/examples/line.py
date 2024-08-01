import curses
import numpy as np
import time
from ..line import Axes


def window(stdscr: curses.window):
    curses.curs_set(0)
    stdscr.nodelay(True)

    axes = Axes(stdscr, 5, 1, 0, 0)
    axes._y0 = 0
    
    off = 0
    while True:
        try:
            stdscr.clear()
            off += 2*np.pi / 100
            x = np.linspace(0, 2*np.pi)
            y = np.sin(x - off)
            axes.line(x, y)
            stdscr.refresh()
            time.sleep(0.1)
        except KeyboardInterrupt:
             break
        
def main():
     curses.wrapper(window)
