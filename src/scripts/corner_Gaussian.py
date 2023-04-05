import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from kde_contour import Bounded_1d_kde, kdeplot_2d_clevels
import paths

rng = np.random.default_rng(12345)

sns.set_theme(palette='colorblind', font_scale=1.2)

nsamp = 6000

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

samples_Gaussian = np.load(paths.data/"samples_Gaussian.npz")["chains"]
samples_Gaussian = samples_Gaussian.reshape(-1, 2)
mu_median = np.median(samples_Gaussian[:,0])
sigma_median = np.median(samples_Gaussian[:,1])

df = pd.DataFrame()
df['mu'] = samples_Gaussian.reshape(-1,2)[:,0]
df['sigma'] = samples_Gaussian.reshape(-1,2)[:,1]
df = df.sample(nsamp, random_state=rng)

kde_1d_sigma = Bounded_1d_kde(df['sigma'], xlow=0)
df['sigma_kde'] = kde_1d_sigma(df['sigma'])
df = df.sort_values(['sigma'])

samples_Gaussian_without_GW200129 = np.load(paths.data/"samples_Gaussian_without_GW200129.npz")["chains"]
samples_Gaussian_without_GW200129 = samples_Gaussian_without_GW200129.reshape(-1, 2)
mu_median_without_GW200129 = np.median(samples_Gaussian_without_GW200129[:,0])
sigma_median_without_GW200129 = np.median(samples_Gaussian_without_GW200129[:,1])

df_without_GW200129 = pd.DataFrame()
df_without_GW200129['mu'] = samples_Gaussian_without_GW200129.reshape(-1,2)[:,0]
df_without_GW200129['sigma'] = samples_Gaussian_without_GW200129.reshape(-1,2)[:,1]
df_without_GW200129 = df_without_GW200129.sample(nsamp, random_state=rng)

kde_1d_sigma_without_GW200129 = Bounded_1d_kde(df_without_GW200129['sigma'], xlow=0)
df_without_GW200129['sigma_kde'] = kde_1d_sigma_without_GW200129(df_without_GW200129['sigma'])
df_without_GW200129 = df_without_GW200129.sort_values(['sigma'])

fig, axs = plt.subplots(2,2,sharex='col')
fig.set_size_inches(5,5)

lw = 1

lkws = dict(ls='--', c='k')
axs[0,0].axvline(0, **lkws)
axs[1,0].axvline(0, **lkws)
axs[1,0].axhline(0, **lkws)
axs[1,1].axvline(0, **lkws)

#axs[0,0].axvline(mu_median, color=sns.color_palette()[0])
sns.kdeplot(df['mu'], fill=True, ax=axs[0,0], color=sns.color_palette()[0], lw=lw)
#axs[0,0].axvline(mu_median_without_GW200129, color=sns.color_palette()[1])
sns.kdeplot(df_without_GW200129['mu'], fill=True, ax=axs[0,0], color=sns.color_palette()[1], lw=lw)

axs[0,0].set_ylabel("")
axs[0,0].set_xlim(-.07,.07)
axs[0,0].set_ylim(0)
axs[0,0].set_yticks([])

#axs[1,1].axvline(sigma_median, color=sns.color_palette()[0])
axs[1,1].fill_between(df['sigma'], df['sigma_kde'], np.zeros(len(df['sigma'])), alpha=0.2, color=sns.color_palette()[0])
axs[1,1].plot(df['sigma'], df['sigma_kde'], c=sns.color_palette()[0], lw=lw)
#axs[1,1].axvline(sigma_median_without_GW200129, color=sns.color_palette()[1])
axs[1,1].fill_between(df_without_GW200129['sigma'], df_without_GW200129['sigma_kde'], np.zeros(len(df_without_GW200129['sigma'])), alpha=0.2, color=sns.color_palette()[1])
axs[1,1].plot(df_without_GW200129['sigma'], df_without_GW200129['sigma_kde'], color=sns.color_palette()[1], lw=lw)

axs[1,1].set_xlabel("$\\sigma$")
axs[1,1].set_xlim(0)
axs[1,1].set_ylim(0)
axs[1,1].set_yticks([])

c0 = sns.color_palette('tab20c')
colors = [[c0[2], c0[0]], [c0[7], c0[5]]]

# fix seed so that we always subselect the same samples for reproducibility
seed = 12345
kdeplot_2d_clevels(xs=df['mu'], ys=df['sigma'], ylow=0, ax=axs[1,0], colors=colors[0], levels=[0.90,0.3935], fill=True, alpha=0.7, rng=seed)
kdeplot_2d_clevels(xs=df['mu'], ys=df['sigma'], ylow=0, ax=axs[1,0], color=c0[0], levels=[0.90,0.3935], fill=False, linewidths=0.5, alpha=0.5, rng=seed)

kdeplot_2d_clevels(xs=df_without_GW200129['mu'], ys=df_without_GW200129['sigma'], ylow=0, ax=axs[1,0], colors=colors[1], levels=[0.90,0.3935], fill=True, alpha=0.7, rng=seed)

axs[1,0].set_xlabel("$\\mu$")
axs[1,0].set_ylabel("$\\sigma$")
axs[1,0].set_xlim(-.07,.07)
axs[1,0].set_ylim(0)

for k, c in zip(["with GW200129", "without GW200129"], sns.color_palette()[:2]):
    axs[0,0].plot([], c=c, label=k, lw=2)
axs[0,0].legend(loc='center left', bbox_to_anchor=((1, 0.5)), frameon=False)

plt.subplots_adjust(wspace=0.05, hspace=0.05)
fig.delaxes(axs[0,1])

fig.savefig(fname=paths.figures/"corner_Gaussian.pdf", bbox_inches="tight", dpi=300)
