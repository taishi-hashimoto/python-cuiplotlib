"Colorbar library."
import curses


class Colormap:
    "Colormap."
    
    BASE_COLORS = {
        # color 1 is under, by default same as 2
        "b": (curses.COLOR_BLUE, 2),
        "c": (curses.COLOR_CYAN, 3),
        "g": (curses.COLOR_GREEN, 4),
        "y": (curses.COLOR_YELLOW, 5),
        "r": (curses.COLOR_RED, 6),
        "m": (curses.COLOR_MAGENTA, 7),
        # color 8 is over, by default same as 7
        "k": (curses.COLOR_BLACK, 9),  # invalid
        "w": (curses.COLOR_WHITE, 10),
    }

    DEFAULT_CONTINUOUS = (
        curses.COLOR_BLUE,
        curses.COLOR_CYAN,
        curses.COLOR_GREEN,
        curses.COLOR_YELLOW,
        curses.COLOR_RED,
        curses.COLOR_MAGENTA)

    def __init__(self, colors=None, under=None, over=None, invalid=None):
        if colors is None:
            colors = self.DEFAULT_CONTINUOUS
        for i, color in enumerate(colors, 2):
            curses.init_pair(i, color, curses.COLOR_BLACK)
        if under is None:
            under = colors[0]
        if over is None:
            over = colors[-1]
        if invalid is None:
            invalid = curses.COLOR_BLACK
        curses.init_pair(1, under, curses.COLOR_BLACK)
        curses.init_pair(len(colors) + 2, over, curses.COLOR_BLACK)
        curses.init_pair(len(colors) + 3, invalid, curses.COLOR_BLACK)
        curses.init_pair(len(colors) + 4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self._colors = colors  # Specified color

    @property
    def invalid(self):
        return curses.color_pair(len(self._colors) + 3)

    def __call__(self, value):
        try:
            index = int(value * (len(self._colors)-1)) + 2
        except ValueError:
            return self.invalid
        if index < 1:
            index = 1
        if index > self.ncolors:
            index = self.ncolors
        return curses.color_pair(index)

    def __getitem__(self, index):
        if isinstance(index, str):  # named colors
            index = self.BASE_COLORS[index][1]
        return curses.color_pair(index)

    @property
    def ncolors(self) -> int:
        "The number of assigned colors including over/under."
        return len(self._colors) + 2


class Normalize:
    "Normalize value in [0, 1] range by [vmin, vmax]."

    def __init__(self, vmin, vmax):
        self._vmin = vmin
        self._vmax = vmax

    def __call__(self, value):
        return (value - self._vmin) / (self._vmax - self._vmin)


class Colorbar:
    "Draw a horizontal colorbar."

    def __init__(
        self,
        window: curses.window,
        x0, y0,
        cmap: 'Colormap',
        norm: 'Normalize' = None,
        vmin: str = None,
        vmax: str = None,
        formatter: str = "{}",
        extend=None,
        nchars=2,
        ha="right",
        va="bottom",
        title=None
    ):
        if norm is not None:
            vmin = norm._vmin
            vmax = norm._vmax
        vmin = formatter.format(vmin)
        vmax = formatter.format(vmax)
        colors = [curses.color_pair(index) for index in range(1, cmap.ncolors + 1)]
        length = nchars * len(colors)  # Colorbar's length
        if va == "bottom":
            y = y0 - 3
        elif va == "top":
            y = y0
        if ha == "right":
            x = x0 - length
        elif ha == "left":
            x = x0
        for i, color in enumerate(colors):
            if i not in (0, cmap.ncolors-1) or extend == "both" or (i == 0 and extend == "left") or (i == cmap.ncolors-1 and extend == "right"):
                window.addstr(y, x + i * nchars, "■" * nchars, color)
        window.addstr(y + 1, x + nchars, vmin)
        window.addstr(y + 1, x + length - len(vmax), vmax)
        if title is not None:
            window.addstr(y + 2, x + length//2 - len(title)//2, title)
