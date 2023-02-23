import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import kde_contour as kde_contour
import paths

sns.set_theme(palette='colorblind', font_scale=1.2)

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
df = df.sample(10000)

kde_1d_sigma = kde_contour.Bounded_1d_kde(df['sigma'], xlow=0)
df['sigma_kde'] = kde_1d_sigma(df['sigma'])
df = df.sort_values(['sigma'])

samples_Gaussian_without_GW200129 = np.load(paths.data/"samples_Gaussian_without_GW200129.npz")["chains"]
samples_Gaussian_without_GW200129 = samples_Gaussian_without_GW200129.reshape(-1, 2)
mu_median_without_GW200129 = np.median(samples_Gaussian_without_GW200129[:,0])
sigma_median_without_GW200129 = np.median(samples_Gaussian_without_GW200129[:,1])

df_without_GW200129 = pd.DataFrame()
df_without_GW200129['mu'] = samples_Gaussian_without_GW200129.reshape(-1,2)[:,0]
df_without_GW200129['sigma'] = samples_Gaussian_without_GW200129.reshape(-1,2)[:,1]
df_without_GW200129 = df_without_GW200129.sample(10000)

kde_1d_sigma_without_GW200129 = kde_contour.Bounded_1d_kde(df['sigma'], xlow=0)
df_without_GW200129['sigma_kde'] = kde_1d_sigma_without_GW200129(df['sigma'])
df_without_GW200129 = df_without_GW200129.sort_values(['sigma'])

fig, axs = plt.subplots(2,2,sharex='col')
fig.set_size_inches(5,5)

axs[0,0].axvline(mu_median, color=sns.color_palette()[0])
sns.kdeplot(df['mu'], fill=True, ax=axs[0,0])
axs[0,0].axvline(mu_median_without_GW200129, color=sns.color_palette()[3])
sns.kdeplot(df_without_GW200129['mu'], fill=True, ax=axs[0,0])

axs[0,0].set_ylabel("")
axs[0,0].set_xlim(-.07,.07)
axs[0,0].set_ylim(0)
axs[0,0].set_yticks([])

axs[1,1].axvline(sigma_median, color=sns.color_palette()[0])
axs[1,1].fill_between(df['sigma'], df['sigma_kde'], np.zeros(len(df['sigma'])), alpha=0.2)
axs[1,1].plot(df['sigma'], df['sigma_kde'])
axs[1,1].axvline(sigma_median_without_GW200129, color=sns.color_palette()[3])
axs[1,1].fill_between(df_without_GW200129['sigma'], df_without_GW200129['sigma_kde'], np.zeros(len(df_without_GW200129['sigma'])), alpha=0.2)
axs[1,1].plot(df_without_GW200129['sigma'], df_without_GW200129['sigma_kde'])

axs[1,1].set_xlabel("$\\sigma$")
axs[1,1].set_xlim(0)
axs[1,1].set_ylim(0)
axs[1,1].set_yticks([])
axs[1,1].get_lines()[1].set_linewidth(1)

axs[1,0].axvline(mu_median, color=sns.color_palette()[0])
axs[1,0].axhline(sigma_median, color=sns.color_palette()[0])
kde_contour.kdeplot_2d_clevels(xs=df['mu'], ys=df['sigma'], ylow=0, ax=axs[1,0], color=sns.color_palette()[0], levels=[0.90,0.3935])
axs[1,0].axvline(mu_median_without_GW200129, color=sns.color_palette()[3])
axs[1,0].axhline(sigma_median_without_GW200129, color=sns.color_palette()[3])
kde_contour.kdeplot_2d_clevels(xs=df_without_GW200129['mu'], ys=df_without_GW200129['sigma'], ylow=0, ax=axs[1,0], color=sns.color_palette()[3], levels=[0.90,0.3935])

axs[1,0].set_xlabel("$\\mu$")
axs[1,0].set_ylabel("$\\sigma$")
axs[1,0].set_xlim(-.07,.07)
axs[1,0].set_ylim(0)

fig.delaxes(axs[0,1])
fig.tight_layout(pad=0.3)

fig.savefig(fname=paths.figures/"corner_Gaussian.pdf", bbox_inches="tight", dpi=300)
