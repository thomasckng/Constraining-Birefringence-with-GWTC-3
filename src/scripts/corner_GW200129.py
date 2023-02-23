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

result = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result = result[result.event == "GW200129_065458"]
result = result.sample(n=nsamples)
result['with'] = np.full(len(result), r"birefringence (H1, L1, V1)")
result['cos_iota'] = np.cos(result['iota'])

result_without_H1 = CBCResult.from_json(filename=paths.data/"GW200129_065458_birefringence_without_H1.json.gz").posterior
result_without_H1 = result_without_H1.sample(n=nsamples)
result_without_H1['with'] = np.full(len(result_without_H1), r"birefringence (L1, V1)")
result_without_H1['cos_iota'] = np.cos([float(result_without_H1['iota'][i]) for i in result_without_H1.index])

result_without_L1 = CBCResult.from_json(filename=paths.data/"GW200129_065458_birefringence_without_L1.json.gz").posterior
result_without_L1 = result_without_L1.sample(n=nsamples)
result_without_L1['with'] = np.full(len(result_without_L1), r"birefringence (H1, V1)")
result_without_L1['cos_iota'] = np.cos([float(result_without_L1['iota'][i]) for i in result_without_L1.index])

result_without_V1 = CBCResult.from_json(filename=paths.data/"GW200129_065458_birefringence_without_V1.json.gz").posterior
result_without_V1 = result_without_V1.sample(n=nsamples)
result_without_V1['with'] = np.full(len(result_without_V1), r"birefringence (H1, L1)")
result_without_V1['cos_iota'] = np.cos([float(result_without_V1['iota'][i]) for i in result_without_V1.index])

result_all = pd.concat([result,result_without_H1,result_without_L1,result_without_V1], ignore_index=True)

g = sns.pairplot(result_all,
                 vars=['kappa', 'luminosity_distance', 'cos_iota'],
                 corner=True, kind='kde', hue='with',
                 diag_kws=dict(common_norm=False, fill=False), plot_kws=dict(common_norm=False, levels=[(1.-0.90)]))

g.axes[2,0].set_xlabel(r"$\kappa$")
g.axes[1,0].set_ylabel(r"$d_L$")
g.axes[2,1].set_xlabel(r"$d_L$")
g.axes[2,0].set_ylabel(r"$\cos\iota$")
g.axes[2,2].set_xlabel(r"$\cos\iota$")
g.fig.legends[0].set_bbox_to_anchor((0.65,0.8))

g.savefig(fname=paths.figures/"corner_GW200129.pdf", bbox_inches="tight", dpi=300)