
class Transform:
    def __init__(
        self,
        top, left,  # Top left corner of the axes in the window.
        height, width,  # Axes size in the window.
        xmin, xmax,  # Data X range.
        ymin, ymax  # Data Y range.
    ):
        self._top = top
        self._left = left
        self._width = width
        self._height = height
        self._xmin = xmin
        self._xmax = xmax
        self._ymin = ymin
        self._ymax = ymax

    def __call__(self, x, y):
        xx = (x - self._xmin) / (self._xmax - self._xmin) * self._width + self._left
        yy = (y - self._ymin) / (self._ymax - self._ymin) * -self._height + self._top + self._height - 0.5
        return xx, yy
