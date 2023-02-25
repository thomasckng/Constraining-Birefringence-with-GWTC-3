import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import paths
import numpy as np

sns.set_theme(palette='colorblind', font_scale=1.5)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

df = pd.read_feather(paths.data/'reweighted_kappa_samples.feather')

# restructure DataFrame to better work with sns.histplot hues
zscores = pd.Series({e: np.abs(k.mean()/k.std()) for e, k in df.items()})
zscores.sort_values(ascending=False, inplace=True)

cmap = matplotlib.cm.get_cmap('flare')
norm = matplotlib.colors.Normalize(vmin=0, vmax=zscores.max())
color = zscores.apply(lambda z: cmap(norm(z), alpha=norm(z)))

g = sns.kdeplot(df, palette=color.to_dict(), hue_order=zscores.index)
g.get_legend().remove()
g.set_xlabel('$\kappa$')
g.set_ylabel('$p(\kappa)$')
g.set_xlim(-.2,.2)

# alpha assignment through hue above doesn't seem to work, so enforce it manually
norm_alpha = matplotlib.colors.Normalize(vmin=-1E-3, vmax=zscores.max()*1.1)
for i, (z,line) in enumerate(zip(zscores, g.get_lines()[::-1])):
    line.set_alpha(norm_alpha(z))
    if i < 3:
      line.set_label(zscores.index[i].replace('_', r'\_'))
    else:
      line.set_label(None)
g.legend(fontsize=14)

g.axvline(0, ls='--', c='k')

cb = g.figure.colorbar(matplotlib.cm.ScalarMappable(norm=norm, cmap=cmap),
             ax=g.axes, orientation='horizontal', 
             location='top', fraction=0.046, shrink=0.4)
cb.ax.tick_params(labelsize=8)
cb.ax.set_ylabel("$|\mu/\sigma|$", rotation=0, labelpad=30)

plt.savefig(fname=paths.figures/"reweighed_kappa.pdf", bbox_inches="tight", dpi=300)
