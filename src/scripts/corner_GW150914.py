import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from bilby.gw.result import CBCResult
import paths

sns.set_theme(palette='colorblind', font_scale=1.5)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

nsamples = 5000

result_GR = CBCResult.from_json(filename=paths.data/"GW150914_GR.json.gz").posterior
result_GR = result_GR.sample(n=nsamples)
result_GR['with'] = np.full(len(result_GR), "GR")
result_GR['cos_iota'] = np.cos([float(value) for value in result_GR['iota']])

result_bilby = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_bilby = result_bilby[result_bilby.event == "GW150914"]
result_bilby = result_bilby.sample(n=nsamples)
result_bilby['with'] = np.full(len(result_bilby), "BR (frequency dependent)")
result_bilby['cos_iota'] = np.cos(result_bilby['iota'])

result_extra = CBCResult.from_json(filename=paths.data/"GW150914_birefringence(frequency_independent).json").posterior
result_extra = result_extra.sample(n=nsamples)
result_extra['kappa'] = result_extra['kappa'] * 1000 # different scale was used in the frequency independent data
result_extra['with'] = np.full(len(result_extra), "BR (frequency independent)")
result_extra['cos_iota'] = np.cos(result_extra['iota'])

result = pd.concat([result_bilby,result_extra,result_GR], ignore_index=True)

p = [sns.color_palette()[i] for i in [0, 2, 1]]
g = sns.pairplot(result,
                 vars=['kappa', 'luminosity_distance', 'cos_iota'],
                 corner=True, kind='kde', hue='with', palette=p,
                 diag_kws=dict(common_norm=False), plot_kws=dict(common_norm=False, levels=[(1.-0.90),(1.-0.3935)]))

g.axes[2,0].set_xlabel(r"$\kappa$")
g.axes[1,0].set_ylabel(r"$d_L$ (Mpc)")
g.axes[2,1].set_xlabel(r"$d_L$ (Mpc)")
g.axes[2,0].set_ylabel(r"$\cos\iota$")
g.axes[2,2].set_xlabel(r"$\cos\iota$")
g.fig.legends[0].set_bbox_to_anchor((0.65,0.8))
g.legend.set_title(None)
plt.subplots_adjust(wspace=0.05, hspace=0.05)

g.savefig(fname=paths.figures/"corner_GW150914.pdf", bbox_inches="tight", dpi=300)
