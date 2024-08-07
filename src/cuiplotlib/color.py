"Color library."
import curses
import math


class ColorManager:
    def __init__(self):
        curses.use_default_colors()
        self._data = {}

        # Some default colors.
        self.new("b", curses.COLOR_BLUE)
        self.new("c", curses.COLOR_CYAN)
        self.new("g", curses.COLOR_GREEN)
        self.new("y", curses.COLOR_YELLOW)
        self.new("r", curses.COLOR_RED)
        self.new("m", curses.COLOR_MAGENTA)
        self.new("k", curses.COLOR_BLACK)
        self.new("w", curses.COLOR_WHITE)
        self.new("none", -1, -1)

        self.new("bg_b", -1, curses.COLOR_BLUE)
        self.new("bg_c", -1, curses.COLOR_CYAN)
        self.new("bg_g", -1, curses.COLOR_GREEN)
        self.new("bg_y", -1, curses.COLOR_YELLOW)
        self.new("bg_r", -1, curses.COLOR_RED)
        self.new("bg_m", -1, curses.COLOR_MAGENTA)
        self.new("bg_k", -1, curses.COLOR_BLACK)
        self.new("bg_w", -1, curses.COLOR_WHITE)

    def new(
        self,
        key,
        foreground_color,
        background_color=-1,
    ):
        "Initialize a color pair with an arbitrary key and return its index."
        if key in self._data:
            return self._data[key]
        else:
            i = len(self._data) + 1
            curses.init_pair(i, foreground_color, background_color)
            self._data[key] = i
        return i

    def get(self, index):
        if not isinstance(index, int):
            index = self._data[index]
        return curses.color_pair(index)

    def get_cmap(self, name=None):
        if name is None:  # Default colormap.
            return Colormap()


color_manager = None
"Global color manager"


class Colormap:
    @staticmethod
    def jet_bg():
        return Colormap(
            ["bg_b", "bg_c", "bg_g", "bg_y", "bg_r", "bg_m"]
        )

    def __init__(self, colors=None, under=None, over=None, invalid=None):
        if colors is None:
            colors = "bcgyrm"
        self._colors = colors
        if under is None:
            under = colors[0]
        self._under = under
        if over is None:
            over = colors[-1]
        self._over = over
        if invalid is None:
            invalid = "k"
        self._invalid = invalid
        global color_manager
        if color_manager is None:
            color_manager = ColorManager()

    def get_color(self, value: float):
        "value: normalized value in [0, 1] range."
        try:
            index = math.ceil(value * (len(self._colors)))
            if index < 0:
                index = self._under
            elif index >= len(self._colors):
                index = self._over
            else:
                index = self._colors[index]
        except ValueError:
            index = self._invalid
        return index

    def __call__(self, value):
        self[self.get_color(value)]

    def __getitem__(self, index):
        return color_manager.get(index)


class Normalize:
    "Normalize value in [0, 1] range by [vmin, vmax]."

    def __init__(self, vmin, vmax):
        self._vmin = vmin
        self._vmax = vmax

    def __call__(self, value):
        return (value - self._vmin) / (self._vmax - self._vmin)
