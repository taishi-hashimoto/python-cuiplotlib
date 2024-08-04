import curses
from .color import Colormap, Normalize
from .axes import Axes


class Colorbar:
    def __init__(
        ax: Axes,
        cmap: Colormap,
        norm: Normalize = None,
        vmin: float = None,
        vmax: float = None,
        formatter: str = "{}",
        extend=None,
        title=None,
    ):
        if norm is not None:
            vmin = norm._vmin
            vmax = norm._vmax
        