import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from bilby.gw.result import CBCResult
from kde_contour import Bounded_1d_kde, kdeplot_2d_clevels
import paths

rng = np.random.default_rng(12345)
sns.set_theme(palette='colorblind', font_scale=1.5)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

nsamples = 8000

events = ['GW170104', 'GW191105_143521']

fs = (6.807804068078041, 4.207454302822033)
fig, axs = plt.subplots(2,1, figsize=fs)
plt.subplots_adjust(hspace=0.1)

all_result_BR = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")

def kdeplot1d(x, **kws):
    if np.all(x.isna()):
        return
    df = pd.DataFrame({'x': x, 'y': Bounded_1d_kde(x, xlow=0, xhigh=1)(x)})
    df = df.sort_values(['x'])
    plt.fill_between(df['x'], df['y'], np.zeros(len(x)), alpha=0.2)
    plt.plot(df['x'], df['y'], **kws)

for e, ax in zip(events, axs):
    plt.sca(ax)

    result_GR = CBCResult.from_json(filename=paths.data/f"{e}_GR.json.gz").posterior
    result_GR = result_GR.sample(n=nsamples, random_state=rng)
    result_GR['kappa'] = np.full(len(result_GR), None)
    
    result_BR = all_result_BR[all_result_BR.event == e]
    result_BR = result_BR.sample(n=nsamples, random_state=rng)

    kdeplot1d(result_GR['mass_ratio'], label='GR')
    kdeplot1d(result_BR['mass_ratio'], label='BR')

    plt.xlim(0, 1)
    plt.ylim(bottom=0)
    plt.xlabel('$q$')
    plt.ylabel('$p(q)$')
    plt.annotate(e, (0.99, 0.15), ha='right', color='white')

axs[0].legend(loc='upper left')

axs[0].set_xticklabels([])
axs[0].set_xlabel(None)

yls = [ax.get_ylim()[-1] for ax in axs]
for ax in axs:
    ax.set_ylim(0, max(yls))

plt.savefig(fname=paths.figures/"mass_ratio.pdf", bbox_inches="tight")
