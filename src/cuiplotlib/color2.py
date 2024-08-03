"Color library."
import curses


class ColorManager:
    def __init__(self):
        curses.use_default_colors()
        self._data = {}

        # Some default colors.
        self.new("b", curses.COLOR_BLUE, -1)
        self.new("c", curses.COLOR_CYAN, -1)
        self.new("g", curses.COLOR_GREEN, -1)
        self.new("y", curses.COLOR_YELLOW, -1)
        self.new("r", curses.COLOR_RED, -1)
        self.new("m", curses.COLOR_MAGENTA, -1)
        self.new("k", curses.COLOR_BLACK, -1)
        self.new("w", curses.COLOR_WHITE, -1)
        self.new("none", -1, -1)

    def new(
        self,
        key,
        foreground_color,
        background_color=curses.COLOR_BLACK,
    ):
        "Initialize a color pair with an arbitrary key and return its index."
        if key in self._data:
            return self._data[key]
        else:
            i = len(self._data)
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
        try:
            index = int(value * (len(self._colors) - 1))
            if index < 1:
                index = self._under
            elif index >= len(self._colors):
                index = self._over
            else:
                index = self._colors[index]
        except ValueError:
            index = self._invalid
        return index

    def __getitem__(self, index):
        return color_manager.get(index)


class Normalize:
    "Normalize value in [0, 1] range by [vmin, vmax]."

    def __init__(self, vmin, vmax):
        self._vmin = vmin
        self._vmax = vmax

    def __call__(self, value):
        return (value - self._vmin) / (self._vmax - self._vmin)
