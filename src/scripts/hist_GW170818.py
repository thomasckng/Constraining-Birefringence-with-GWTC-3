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

result_GR = CBCResult.from_json(filename=paths.data/"GW170818_GR.json.gz").posterior
result_GR = result_GR.sample(n=nsamples)
result_GR['with'] = np.full(len(result_GR), "GR")
result_GR['cos_iota'] = np.cos([float(value) for value in result_GR['iota']])

result_bilby = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_bilby = result_bilby[result_bilby.event == "GW170818"]
result_bilby = result_bilby.sample(n=nsamples)
result_bilby['with'] = np.full(len(result_bilby), r"BR")
result_bilby['cos_iota'] = np.cos(result_bilby['iota'])

result = pd.concat([result_bilby,result_GR], ignore_index=True)

result[r'$\kappa$'] = result['kappa']
result[r'$\chi_{\rm eff}$'] = result['chi_eff']
result[r'$\chi_p$'] = result['chi_p']
g = sns.pairplot(result,
            vars=[r'$\kappa$', r'$\chi_{\rm eff}$', r'$\chi_p$'],
            corner=True, kind='kde', hue='with',
            diag_kws=dict(common_norm=False),
            plot_kws=dict(common_norm=False, levels=[(1.-0.90),(1.-0.3935)]))

g.fig.legends[0].set_bbox_to_anchor((0.89,0.5))

g.savefig(fname=paths.figures/"hist_GW170818.pdf", bbox_inches="tight", dpi=300)
