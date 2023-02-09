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

samples_Gaussian = np.load(paths.data/"samples_Gaussian_without_GW200129.npz")["chains"]
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

fig = plt.figure(figsize=(5,5))
ax1 = fig.add_subplot(221)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)

ax1.axvline(mu_median, color=sns.color_palette()[3])
sns.kdeplot(df['mu'], fill=True, ax=ax1)

ax1.set_xlabel("")
ax1.set_ylabel("")
ax1.set_xlim(-.07,.07)
ax1.set_ylim(0)
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_box_aspect(1)

ax4.axvline(sigma_median, color=sns.color_palette()[3])
ax4.fill_between(df['sigma'], df['sigma_kde'], np.zeros(len(df['sigma'])), alpha=0.2)
ax4.plot(df['sigma'], df['sigma_kde'])

ax4.set_xlabel("$\\sigma$")
ax4.set_xlim(0)
ax4.set_ylim(0)
ax4.set_yticks([])
ax4.get_lines()[1].set_linewidth(1)
ax4.set_box_aspect(1)

ax3.axvline(mu_median, color=sns.color_palette()[3])
ax3.axhline(sigma_median, color=sns.color_palette()[3])
kde_contour.kdeplot_2d_clevels(xs=df['mu'], ys=df['sigma'], ylow=0, ax=ax3,
                               color=sns.color_palette()[0], levels=[0.90,0.3935])

ax3.set_xlabel("$\\mu$")
ax3.set_ylabel("$\\sigma$")
ax3.set_xlim(-.07,.07)
ax3.set_ylim(0)
ax3.set_box_aspect(1)

fig.tight_layout(pad=0)

fig.savefig(fname=paths.figures/"corner_Gaussian.pdf", bbox_inches="tight", dpi=300)