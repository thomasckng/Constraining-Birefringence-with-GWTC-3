import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import paths

sns.set_theme(palette='colorblind', font_scale=1.2)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

samples_Gaussian = np.load(paths.data/"samples_Gaussian.npz")["chains"]
samples_Gaussian = samples_Gaussian.reshape(-1, 2)

df = pd.DataFrame()
df['mu'] = samples_Gaussian.reshape(-1,2)[:,0]
df['sigma'] = samples_Gaussian.reshape(-1,2)[:,1]
df = df.sample(10000)

g = sns.pairplot(df,
                vars=['mu', 'sigma'],
                corner=True, kind='kde',
                diag_kws=dict(common_norm=False, cut=0), plot_kws=dict(common_norm=False, levels=[
                        (1.-0.90),(1.-0.3935)], cut=0))

g.axes[1,1].set_xlabel("$\\sigma$")
g.axes[1,0].set_xlabel("$\\mu$")
g.axes[1,0].set_ylabel("$\\sigma$")

g.savefig(fname=paths.figures/"corner_Gaussian.pdf", bbox_inches="tight", dpi=300)