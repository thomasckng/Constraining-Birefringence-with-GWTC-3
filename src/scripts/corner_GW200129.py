import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from bilby.gw.result import CBCResult
import paths

sns.set_theme(palette='colorblind', font_scale=1.2)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

nsamples = 5000
rng = np.random.default_rng(1234)

result = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result = result[result.event == "GW200129_065458"]
result = result.sample(n=nsamples, random_state=rng)
result['with'] = np.full(len(result), "HLV")
result['cos_iota'] = np.cos(result['iota'])

result_without_H1 = CBCResult.from_json(filename=paths.data/"GW200129_065458_birefringence_without_H1.json.gz").posterior
result_without_H1 = result_without_H1.sample(n=nsamples, random_state=rng)
result_without_H1['with'] = np.full(len(result_without_H1), "LV")
result_without_H1['cos_iota'] = np.cos([float(result_without_H1['iota'][i]) for i in result_without_H1.index])

result_without_L1 = CBCResult.from_json(filename=paths.data/"GW200129_065458_birefringence_without_L1.json.gz").posterior
result_without_L1 = result_without_L1.sample(n=nsamples, random_state=rng)
result_without_L1['with'] = np.full(len(result_without_L1), "HV")
result_without_L1['cos_iota'] = np.cos([float(result_without_L1['iota'][i]) for i in result_without_L1.index])

result_without_V1 = CBCResult.from_json(filename=paths.data/"GW200129_065458_birefringence_without_V1.json.gz").posterior
result_without_V1 = result_without_V1.sample(n=nsamples, random_state=rng)
result_without_V1['with'] = np.full(len(result_without_V1), "HL")
result_without_V1['cos_iota'] = np.cos([float(result_without_V1['iota'][i]) for i in result_without_V1.index])

result_all = pd.concat([result,result_without_H1,result_without_L1,result_without_V1], ignore_index=True)
#result_all = pd.concat([result,result_without_H1,result_without_L1], ignore_index=True)

def kdeplot(x, y=None, hue=None, mask=None, **kws):
    if y is not None:
        y = y[mask]
    sns.kdeplot(x=x[mask], y=y, hue=hue[mask], **kws)

p = list(sns.color_palette())[:3] + ['0.35'] # [sns.color_palette()[4]]
g = sns.PairGrid(data=result_all,
                 vars=['kappa', 'luminosity_distance', 'cos_iota'],
                 corner=True, hue='with', diag_sharey=False,
                 layout_pad=0., palette=p,
                )
m = result_all['with'] == "HLV"
g.map_lower(kdeplot, mask=m, common_norm=False, levels=[1.-0.90, 0.9999], fill=True, alpha=0.5)
g.map_lower(kdeplot, mask=m, common_norm=False, levels=[1.-0.90, 0.9999])
g.map_diag(kdeplot, mask=m, common_norm=False, fill=True)

m = (result_all['with'] == "HV") | (result_all['with'] == "LV")
g.map_lower(kdeplot, mask=m, linewidths=2, common_norm=False, levels=[(1.-0.90)])
g.map_diag(kdeplot, mask=m, linewidth=2, common_norm=False, fill=False)

m = result_all['with']=="HL"
g.map_lower(kdeplot, mask=m, linewidths=2, linestyles='--', common_norm=False, levels=[(1.-0.90)], zorder=100)
g.map_diag(kdeplot, mask=m, linewidth=2, linestyle='--', common_norm=False, fill=False, zorder=100)

g.axes[2,0].set_xlabel(r"$\kappa$")
g.axes[1,0].set_ylabel(r"$d_L$")
g.axes[2,1].set_xlabel(r"$d_L$")
g.axes[2,0].set_ylabel(r"$\cos\iota$")
g.axes[2,2].set_xlabel(r"$\cos\iota$")
#g.fig.legends[0].set_bbox_to_anchor((0.65,0.8))

plt.subplots_adjust(wspace=0.05, hspace=0.05)

for k, c in zip(["HLV", "HV", "LV", "HL"], p):
    g.axes[0,0].plot([], c=c, lw=2, ls='--' if k=="HL" else '-', label=k)
g.axes[0,0].legend(loc='center left', bbox_to_anchor=(1.1, 0.5), frameon=False)

g.savefig(fname=paths.figures/"corner_GW200129.pdf", bbox_inches="tight", dpi=300)
