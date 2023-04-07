import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from bilby.gw.result import CBCResult
from kde_contour import Bounded_1d_kde, kdeplot_2d_clevels
import paths

rng = np.random.default_rng(12345)

sns.set_theme(palette='colorblind', font_scale=2.0)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

nsamples = 5000

result_GR = CBCResult.from_json(filename=paths.data/"GW190521_GR.json.gz").posterior
result_GR = result_GR.sample(n=nsamples, random_state=rng)
result_GR['kappa'] = np.full(len(result_GR), None)
result_GR['with'] = np.full(len(result_GR), "GR")
result_GR['cos_iota'] = np.cos([float(value) for value in result_GR['iota']])
result_GR['cos_tilt_1'] = np.cos([float(value) for value in result_GR['tilt_1']])
result_GR['cos_tilt_2'] = np.cos([float(value) for value in result_GR['tilt_2']])

result_BR = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_BR = result_BR[result_BR.event == "GW190521"]
result_BR = result_BR.sample(n=nsamples, random_state=rng)
result_BR['with'] = np.full(len(result_BR), r"BR")
result_BR['cos_iota'] = np.cos(result_BR['iota'])
result_BR['cos_tilt_1'] = np.cos([float(value) for value in result_BR['tilt_1']])
result_BR['cos_tilt_2'] = np.cos([float(value) for value in result_BR['tilt_2']])

result = pd.concat([result_BR,result_GR], ignore_index=True)

lw = 1

def kdeplot2d(x, y, rgn=12345, **kws):
    kws.pop('label', None)
    kdeplot_2d_clevels(xs=x, ys=y, auto_bound=True, rng=rng, **kws)

def kdeplot1d(x, **kws):
    if np.all(x.isna()):
        return
    for key in ['label', 'hue_order', 'color']:
        kws.pop(key, None)
    df = pd.DataFrame({'x': x, 'y': Bounded_1d_kde(x, xlow=min(x), xhigh=max(x), **kws)(x)})
    df = df.sort_values(['x'])
    plt.fill_between(df['x'], df['y'], np.zeros(len(x)), alpha=0.2)
    plt.plot(df['x'], df['y'], lw=lw)
    plt.xlim(df['x'].min(), df['x'].max())
    current_ymax = plt.ylim()[1]
    if current_ymax > df['y'].max()*1.1:
        plt.ylim(0,current_ymax)
    else:
        plt.ylim(0,df['y'].max()*1.1)

vars = ['kappa','luminosity_distance','cos_iota','psi','a_1','a_2','cos_tilt_1','cos_tilt_2','phi_12','phi_jl','phase']
c0 = sns.color_palette('tab20c')
g = sns.PairGrid(data=result,
                 vars=vars,
                 corner=True, hue='with', 
                 diag_sharey=False,
                 layout_pad=0.,
                 hue_kws={'colors': [[c0[3], c0[0]], [c0[7], c0[5]]]}
                )

g.map_lower(kdeplot2d, levels=[0.90,0.3935], alpha=0.7, fill=True)
g.map_diag(kdeplot1d)

for i in range(len(vars)):
    for j in range(i):
        g.axes[i,j].set_xlim(result[vars[j]].min(), result[vars[j]].max())
        g.axes[i,j].set_ylim(result[vars[i]].min(), result[vars[i]].max())

g.axes[10,0].set_xlabel("$\kappa$")
g.axes[1,0].set_ylabel("$d_L$ (Mpc)")
g.axes[10,1].set_xlabel("$d_L$ (Mpc)")
g.axes[2,0].set_ylabel("$\\cos\\iota$")
g.axes[10,2].set_xlabel("$\\cos\\iota$")
g.axes[3,0].set_ylabel("$\\psi$")
g.axes[10,3].set_xlabel("$\\psi$")
g.axes[4,0].set_ylabel("$\chi_1$")
g.axes[10,4].set_xlabel("$\chi_1$")
g.axes[5,0].set_ylabel("$\chi_2$")
g.axes[10,5].set_xlabel("$\chi_2$")
g.axes[6,0].set_ylabel("$\\cos\\theta_1$")
g.axes[10,6].set_xlabel("$\\cos\\theta_1$")
g.axes[7,0].set_ylabel("$\\cos\\theta_2$")
g.axes[10,7].set_xlabel("$\\cos\\theta_2$")
g.axes[8,0].set_ylabel("$\\Delta\\phi$")
g.axes[10,8].set_xlabel("$\\Delta\\phi$")
g.axes[9,0].set_ylabel("$\\phi_{JL}$")
g.axes[10,9].set_xlabel("$\\phi_{JL}$")
g.axes[10,0].set_ylabel("$\\phi_{\\rm{ref}}$")
g.axes[10,10].set_xlabel("$\\phi_{\\rm{ref}}$")

for k, c in zip(result['with'].unique(), sns.color_palette()):
    g.axes[5,5].plot([], c=c, lw=2, label=k)
g.axes[5,5].legend(loc='center left', bbox_to_anchor=((1.1,0.5)), frameon=False)

plt.subplots_adjust(wspace=0.05, hspace=0.05)

g.savefig(fname=paths.figures/"corner_GW190521_appendix.pdf", bbox_inches="tight", dpi=300)
