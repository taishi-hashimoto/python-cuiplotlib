# %%
import matplotlib.pyplot as plt
import numpy as np
from cuiplotlib.ticker import autoticks
import sys
from os.path import dirname, join

sys.path.insert(0, join(dirname(__file__), "..", "src"))

data = np.random.normal(size=10) * 10

ticks, cands = autoticks(min(data), max(data), debug=True)

fig = plt.figure(figsize=(10, 10))
gs = fig.add_gridspec(nrows=len(cands), ncols=1)
for i, cand in enumerate(cands):
    _, ndiv, _, vmin1, _, width1 = cand
    ticks = [vmin1 + width1 * i for i in range(ndiv + 1)]
    ax = fig.add_subplot(gs[i, 0])
    ax.tick_params(labelbottom=True, bottom=False)
    ax.tick_params(labelleft=False, left=False)
    ax.set_title(("Best: " if i == 0 else "") + str(cand))
    ax.scatter(data, np.zeros_like(data), c='r')
    ax.hlines(y=0, xmin=min(ticks), xmax=max(ticks))
    ax.vlines(x=[i for i in ticks], ymin=-0.04, ymax=0.04)
    ax.set_xticks(ticks)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
fig.tight_layout()
fig.savefig("autoticks.png")
# %%
