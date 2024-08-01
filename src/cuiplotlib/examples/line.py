import curses
import numpy as np
import time
from ..line import line


def window(stdscr: curses.window):
    curses.curs_set(0)
    stdscr.nodelay(True)

    ymax, xmax = stdscr.getmaxyx()

    
    while True:
        try:
            x = np.linspace(0, 2*np.pi)
            y = np.sin(x)
            line(stdscr, 10, 2, xmax//2, ymax-5, x, y)
            stdscr.refresh()
            time.sleep(1)
        except KeyboardInterrupt:
             break
        
def main():
     curses.wrapper(window)
