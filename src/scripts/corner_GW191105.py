import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import paths

sns.set_theme(palette='colorblind', font_scale=1.5)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

result = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result = result[result.event == "GW191105_143521"]
result['cos_iota'] = np.cos([float(value) for value in result['iota']])

g = sns.pairplot(result,
                    vars=['kappa', 'luminosity_distance', 'cos_iota', 'chi_eff', 'chi_p'],
                    corner=True, kind='hist', diag_kws=dict(common_norm=False), plot_kws=dict(common_norm=False, bins=100, rasterized=True))

g.axes[4,0].set_xlabel(r"$\kappa$")
g.axes[1,0].set_ylabel(r"$d_L$ (Mpc)")
g.axes[4,1].set_xlabel(r"$d_L$ (Mpc)")
g.axes[2,0].set_ylabel(r"$\cos\iota$")
g.axes[4,2].set_xlabel(r"$\cos\iota$")
g.axes[3,0].set_ylabel(r"$\chi_{eff}$")
g.axes[4,3].set_xlabel(r"$\chi_{eff}$")
g.axes[4,0].set_ylabel(r"$\chi_p$")
g.axes[4,4].set_xlabel(r"$\chi_p$")
plt.subplots_adjust(wspace=0.05, hspace=0.05)

g.savefig(fname=paths.figures/"corner_GW191105.pdf", bbox_inches="tight", dpi=300)
