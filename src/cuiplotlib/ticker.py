import math


def autoticks(
    vmin: float,
    vmax: float,
    nbins: int = 10,
    steps=(1, 2, 2.5, 5, 10),
    debug=False
):
    """Simplified matplotlib's MaxNLocator's algorithm.

    Parameters
    ==========
    vmin: float
        Data minimum.
    vmax: float
        Data maximum.
    n: int
        Maximum number of division (intervals between ticks).
        Default is `10`.
    steps: list[int | float]
        Candidates of tick multiples.
        Default is `(1, 2, 2.5, 5, 10)`.
    """
    cands = []
    for ndiv in range(1, nbins + 1)[::-1]:
        width = (vmax - vmin) / ndiv
        log_w = math.log10(width)
        order = math.ceil(log_w)
        cands1 = []
        for s in steps:
            for offset in (-1, 0, 1):
                value = math.log10(s) + order + offset
                cands1.append((abs(log_w - value), value))
        value = min(cands1, key=lambda x: x[0])[1]
        width1 = round(10**value)
        if width1 == 0:
            continue
        vmin1 = vmin - vmin % width1
        vmax_over_width1 = vmax % width1
        vmax1 = vmax - vmax_over_width1
        if vmax_over_width1 != 0:
            vmax1 += width1
        ndiv1 = (vmax1 - vmin1) / width1
        cands.append((abs(ndiv1 - ndiv), ndiv, ndiv1, vmin1, vmax1, width1))
    cands.sort(key=lambda x: (x[0], -x[1]))
    best = cands[0]
    _, ndiv, _, vmin1, _, width1 = best
    ticks = [vmin1 + width1 * i for i in range(ndiv + 1)]
    if debug:
        return ticks, cands
    else:
        return ticks


def autoformat(ticks: list[float | int]) -> str:
    """Automated format string for given ticks.

    Parameters
    ==========
    ticks: list[float|int]
        Tick values.
    """

    vmin = min(ticks)
    vmax = max(ticks)

    vrange = int(math.floor(math.log10(vmax - vmin)))
    sigfigs = max(0, 3 - vrange)
    thresh = 1e-3 * 10**vrange
    while sigfigs >= 0:
        if max(abs(x - round(x, sigfigs)) for x in ticks) < thresh:
            sigfigs -= 1
        else:
            break
    sigfigs += 1
    return f"{{:1.{sigfigs}f}}"


class StrFormatter:
    """Simplified matplotlib's StrFormatter.
    """
    def __init__(self, format: str = None):
        self._format = format

    def __call__(self, ticks: list[float | int]):
        """Return formatted strings for given ticks.

        Parameters
        ==========
        ticks: list[float|int]
            Tick values.
        """
        if self._format is None:
            fmt = autoformat(ticks)
        else:
            fmt = self._format
        return [fmt.format(x) for x in ticks]


default_formatter = StrFormatter()
"Default formatter. `StrFormatter(format)` with `format = autoformat(ticks)`."
