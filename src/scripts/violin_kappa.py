import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import seaborn as sns
import scipy
import paths

sns.set_theme(palette='colorblind', font_scale=2.0)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"]
})

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
events = result_DataFrame['event'].unique()

result_dict = {}
color_DataFrame = pd.DataFrame(columns=['event', 'mean_over_std'])
i = 0
for event in events:
    df = pd.DataFrame()
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]
    color_DataFrame.loc[i] = [event, abs(result_dict[event]['kappa'].mean()/result_dict[event]['kappa'].std())]
    i += 1
color_DataFrame['color_index'] = [round(np.interp(color_DataFrame.loc[i]['mean_over_std'],
                                                  np.array([color_DataFrame['mean_over_std'].min(),
                                                  color_DataFrame['mean_over_std'].max()]),
                                                  np.array([0,255]))) for i in range(len(color_DataFrame))]
color_dict={}
for i in range(len(color_DataFrame)):
    color_dict[color_DataFrame.loc[i]['event']] = sns.color_palette("rocket_r", as_cmap=True, desat=None).colors[color_DataFrame.loc[i]['color_index']]

kernels = [scipy.stats.gaussian_kde(result_dict[event]['kappa']) for event in events[events != "GW200129_065458"]]
kappa = np.linspace(-.1, .1, 1000)
ll = [np.sum([np.log(ker(k)) for ker in kernels]) for k in kappa]
ll = ll - np.max(ll)
likelihood = np.exp(ll)
likelihood = likelihood / np.trapz(likelihood, x=kappa)

#result_DataFrame['hue'] = 'True'
g = sns.violinplot(data=result_DataFrame, y="event", x="kappa",
                   scale="width",
                   width=1.5,
                    inner=None,
                    #palette={True: color_dict, False: color_dict},
                    hue=True,
                    hue_order=[True, False], split=True,
                   saturation=1,
                   )
g.legend_ = None
g.set_xlabel("$\kappa$", fontsize=40)
g.set_xlim(-0.2,0.2)
g.set_ylabel("")
y_low, y_high = g.get_ylim()
g.set_ylim(y_low-0.45, y_high-0.5)

x = [np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)]
low = np.interp(0.05, x, kappa)
hig = np.interp(0.95, x, kappa)
med = np.interp(0.50, x, kappa)
g.fill_betweenx(g.get_ylim(), low, hig, alpha=0.25, color=sns.color_palette()[0], zorder=-100)
g.axvline(med, c='C0', lw=4)

g.axvline(0, c='k', ls='--', lw=4)
#g.figure.autofmt_xdate(rotation=90)
g.figure.set_size_inches(10,40)
g.axes.tick_params(axis='y', labelsize=30)
yl = g.axes.get_yticklabels()
g.axes.set_yticklabels(yl, va='bottom')

cb = g.figure.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(color_DataFrame['mean_over_std'].min(),
                                                                  color_DataFrame['mean_over_std'].max()),
                                        cmap=sns.color_palette("rocket_r", as_cmap=True)),
                  #label="$|\mu/\sigma|$",
                  ax=g.axes,
                  shrink=0.6,
                  fraction=0.046, pad=0.003,
                  location='top', orientation='horizontal'
                 )
cb.ax.tick_params(direction='in')
cb.ax.set_ylabel("$|\mu/\sigma|$", rotation=0, labelpad=30)

g.axes.collections[60].set_linewidth(3) # GW200129_065458
g.axes.collections[60].set_edgecolor(sns.color_palette()[9])

for collection, color in zip(g.axes.collections, color_dict.values()):
    collection.set_facecolor(color)

g.figure.savefig(fname=paths.figures/"violin_kappa.pdf", bbox_inches="tight", dpi=300)
