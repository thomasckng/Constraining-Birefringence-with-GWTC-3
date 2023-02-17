import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import paths

sns.set_theme(palette='colorblind', font_scale=1.2)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

df_kappa = pd.read_feather(paths.data/'reweighted_kappa_samples_without_GW200129.feather')

g = sns.histplot(df_kappa, element='step', common_norm=False, stat='density', fill=False, binwidth=0.01)
g.get_legend().remove()
g.set_xlabel('$\kappa$')
g.set_ylabel('$p(\kappa|\mu,\sigma)$')
g.set_xlim(-.2,.2)

plt.savefig(fname=paths.figures/"reweighed_kappa.pdf", bbox_inches="tight", dpi=300)