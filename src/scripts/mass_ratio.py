import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from bilby.gw.result import CBCResult
from kde_contour import Bounded_1d_kde
import paths

rng = np.random.default_rng(12345)
sns.set_theme(palette='colorblind', font_scale=1.5)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

nsamples = 10000

events = ['GW170104', 'GW191105_143521']

fs = (6.807804068078041, 4.207454302822033)
fig, axs = plt.subplots(2,2, figsize=fs)
plt.subplots_adjust(hspace=0.1, wspace=0.1*fs[1]/fs[0])

all_result_BR = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")

def kdeplot1d(x, **kws):
    if np.all(x.isna()):
        return
    xl = kws.pop('xlow', 0)
    xh = kws.pop('xhigh', 1)
    lw = kws.pop('linewidth', 1)
    df = pd.DataFrame({'x': x, 'y': Bounded_1d_kde(x, xlow=xl, xhigh=xh)(x)})
    df = df.sort_values(['x'])
    plt.fill_between(df['x'], df['y'], np.zeros(len(x)), alpha=0.2)
    plt.plot(df['x'], df['y'], lw=lw, **kws)

for e, ax_row in zip(events, axs):

    result_GR = CBCResult.from_json(filename=paths.data/f"{e}_GR.json.gz").posterior
    result_GR = result_GR.sample(n=nsamples, random_state=rng)
    result_GR['kappa'] = np.full(len(result_GR), None)
    
    result_BR = all_result_BR[all_result_BR.event == e]
    result_BR = result_BR.sample(n=nsamples, random_state=rng)

    plt.sca(ax_row[0])

    kdeplot1d(result_GR['mass_ratio'], label='GR')
    kdeplot1d(result_BR['mass_ratio'], label='BR')

    plt.xlim(0, 1)
    plt.ylim(bottom=0)
    plt.xlabel('$q$')
    plt.ylabel('density')
    plt.annotate(e, (0.97, 0.15), ha='right', color='white', fontsize=14)

    plt.sca(ax_row[1])

    kdeplot1d(result_GR['chi_p'], label='GR')
    kdeplot1d(result_BR['chi_p'], label='BR')

    plt.xlim(0, 1)
    plt.ylim(bottom=0)
    plt.xlabel('$\chi_p$')
    # plt.ylabel('$p(\chi_p)$')
    plt.annotate(e, (0.03, 0.15), ha='left', color='white', fontsize=14)

axs[0,1].legend(loc='lower right', bbox_to_anchor=(1.05, 0.9), fontsize=14,
                ncol=2, frameon=False, columnspacing=1)


for ax in axs[-1]:
    ax.set_xticklabels(['0', '0.5', '1'])

for ax in axs[0]:
    ax.set_xticklabels([])
    ax.set_xlabel(None)

for ax in axs[:,1]:
    ax.set_yticklabels([])
    ax.set_ylabel(None)

yls = [ax.get_ylim()[-1] for ax in axs.flatten()]
for ax in axs.flatten():
    ax.set_ylim(0, max(yls))

plt.savefig(fname=paths.figures/"mass_ratio.pdf", bbox_inches="tight")
