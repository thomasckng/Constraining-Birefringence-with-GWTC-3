import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from bilby.gw.result import CBCResult
import paths
from kde_contour import Bounded_1d_kde

sns.set_theme(palette='colorblind', font_scale=1.5)
rng = np.random.default_rng(12345)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

nsamples = 10000
fs = (6.807804068078041, 4.207454302822033)

result_GR = CBCResult.from_json(filename=paths.data/"GW170818_GR.json.gz").posterior
result_GR = result_GR.sample(n=nsamples, random_state=rng)

result_BR = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_BR = result_BR[result_BR.event == "GW170818"]
result_BR = result_BR.sample(n=nsamples, random_state=rng)

result = {"BR": result_BR['chi_p'], "GR": result_GR['chi_p']}
xgrid = np.linspace(0, 1, 200)
fig, ax = plt.subplots(1, figsize=fs)
for k, samples in result.items():
    kde = Bounded_1d_kde(samples, xlow=0, xhigh=1)
    y = kde(xgrid)
    l, = ax.plot(xgrid, y, label=k, lw=2)
    ax.fill_between(xgrid, y, color=l.get_color(), alpha=0.1)
ax.legend(title="GW170818")
ax.set_xlabel(r"$\chi_p$")
ax.set_ylabel(r"$p(\chi_p \mid d_i)$")
ax.set_xlim(0, 1)
yl = ax.get_ylim()
ax.set_ylim(0, yl[1])

fig.savefig(fname=paths.figures/"hist_GW170818.pdf", bbox_inches="tight", dpi=300)
