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

nsamples = 5000

result_GR = CBCResult.from_json(filename=paths.data/"GW170818_GR.json.gz").posterior
result_GR = result_GR.sample(n=nsamples, random_state=rng)
result_GR['kappa'] = np.full(len(result_GR), None)
result_GR['with'] = np.full(len(result_GR), "GR")
result_GR['cos_iota'] = np.cos([float(value) for value in result_GR['iota']])

result_BR = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_BR = result_BR[result_BR.event == "GW170818"]
result_BR = result_BR.sample(n=nsamples, random_state=rng)
result_BR['with'] = np.full(len(result_BR), "BR")
result_BR['cos_iota'] = np.cos(result_BR['iota'])

result = pd.concat([result_BR,result_GR], ignore_index=True)

lw = 1

def kdeplot2d(x, y, seed=12345, **kws):
    kws.pop('label', None)
    kdeplot_2d_clevels(xs=x, ys=y, auto_bound=True, linewidths=lw, rng=seed, **kws)

def kdeplot1d(x, **kws):
    if np.all(x.isna()):
        return
    for key in ['label', 'hue_order', 'color']:
        kws.pop(key, None)
    df = pd.DataFrame({'x': x, 'y': Bounded_1d_kde(x, xlow=min(x), xhigh=max(x), **kws)(x)})
    df = df.sort_values(['x'])
    plt.fill_between(df['x'], df['y'], np.zeros(len(x)), alpha=0.2)
    plt.plot(df['x'], df['y'], lw=lw)

vars = ['kappa', 'luminosity_distance', 'cos_iota']
g = sns.PairGrid(data=result,
                 vars=vars,
                 corner=True, hue='with', 
                 diag_sharey=False,
                 layout_pad=0.
                )

g.map_lower(kdeplot2d, levels=[0.90,0.3935])
g.map_diag(kdeplot1d)

for i in range(len(vars)):
    g.axes[i,i].set_xlim(result[vars[i]].min(), result[vars[i]].max())
    g.axes[i,i].set_ylim(0)
    for j in range(i):
        g.axes[i,j].set_xlim(result[vars[j]].min(), result[vars[j]].max())
        g.axes[i,j].set_ylim(result[vars[i]].min(), result[vars[i]].max())

g.axes[2,0].set_xlabel(r"$\kappa$")
g.axes[1,0].set_ylabel(r"$d_L$ (Mpc)")
g.axes[2,1].set_xlabel(r"$d_L$ (Mpc)")
g.axes[2,0].set_ylabel(r"$\cos\iota$")
g.axes[2,2].set_xlabel(r"$\cos\iota$")

for k, c in zip(result['with'].unique(), sns.color_palette()):
    g.axes[1,1].plot([], c=c, lw=2, label=k)
g.axes[1,1].legend(loc='center left', bbox_to_anchor=((1.1, 0.4)), frameon=False)

plt.subplots_adjust(wspace=0.05, hspace=0.05)

ax = g.fig.add_axes([g.axes[2,2].get_position().x0, g.axes[0,0].get_position().y0, g.axes[0,0].get_position().width, g.axes[0,0].get_position().height])

result_BR = result_BR.sort_values(['chi_p'])
result_GR = result_GR.sort_values(['chi_p'])
chi_p_BR = result_BR['chi_p']
chi_p_GR = result_GR['chi_p']
bounded_kde_BR = Bounded_1d_kde(chi_p_BR, xlow=0, xhigh=1)(chi_p_BR)
bounded_kde_GR = Bounded_1d_kde(chi_p_GR, xlow=0, xhigh=1)(chi_p_GR)

ax.plot(chi_p_BR, bounded_kde_BR, color=sns.color_palette()[0], lw=lw)
ax.fill_between(chi_p_BR, bounded_kde_BR, np.zeros(len(chi_p_BR)), alpha=0.2, color=sns.color_palette()[0])
ax.plot(chi_p_GR, bounded_kde_GR, color=sns.color_palette()[1], lw=lw)
ax.fill_between(chi_p_GR, bounded_kde_GR, np.zeros(len(chi_p_GR)), alpha=0.2, color=sns.color_palette()[1])

ax.set_xlabel(r"$\chi_p$")
ax.set_ylabel("")
ax.set_xlim(0, 1)
ax.set_ylim(0)
ax.set_xticks([0.2, 0.5, 0.8])
ax.get_yaxis().set_visible(False)

g.savefig(fname=paths.figures/"corner_GW170818.pdf", bbox_inches="tight", dpi=300)
