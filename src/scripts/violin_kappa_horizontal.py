import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import seaborn as sns
import scipy
import paths

sns.set_theme(palette='colorblind', font_scale=1.2)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"]
})

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
events = result_DataFrame['event'].unique()

result_dict = {}
color_DataFrame = pd.DataFrame(columns=['event', 'median_over_std'])
i = 0
for event in events:
    df = pd.DataFrame()
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]
    color_DataFrame.loc[i] = [event, abs(result_dict[event]['kappa'].median()/result_dict[event]['kappa'].std())]
    i += 1
color_DataFrame['color_index'] = [round(np.interp(color_DataFrame.loc[i]['median_over_std'], np.array([color_DataFrame['median_over_std'].min(), color_DataFrame['median_over_std'].max()]), np.array([0,255]))) for i in range(len(color_DataFrame))]
color_dict={}
for i in range(len(color_DataFrame)):
    color_dict[color_DataFrame.loc[i]['event']] = sns.color_palette("rocket_r", as_cmap=True).colors[color_DataFrame.loc[i]['color_index']]

kernels = [scipy.stats.gaussian_kde(result_dict[event]['kappa']) for event in events[events != "GW200129_065458"]]
kappa = np.linspace(-.1, .1, 1000)
ll = [np.sum([np.log(ker(k)) for ker in kernels]) for k in kappa]
ll = ll - np.max(ll)
likelihood = np.exp(ll)
likelihood = likelihood / np.trapz(likelihood, x=kappa)

g = sns.violinplot(data=result_DataFrame, x="event", y="kappa",
                    scale="width", inner=None,
                    palette=color_dict
                   )
g.set_ylabel("$\kappa$", fontsize=20)
g.set_ylim(-0.2,0.2)
g.set_xlabel("")
x_low, x_high = g.get_xlim()
g.set_xlim(x_low-0.5,x_high+0.5)
g.axhline(np.interp(0.05,[np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)],kappa), color=sns.color_palette()[0], linestyle='--')
g.axhline(np.interp(0.95,[np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)],kappa), color=sns.color_palette()[0], linestyle='--')
g.axhline(np.interp(0.5,[np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)],kappa),color=sns.color_palette()[0])
g.axhline(0, color=sns.color_palette()[4])
g.figure.autofmt_xdate(rotation=45)
g.figure.set_size_inches(40,10)
g.figure.colorbar(plt.cm.ScalarMappable(norm=mpl.colors.Normalize(color_DataFrame['median_over_std'].min(),
                                                                  color_DataFrame['median_over_std'].max()),
                                        cmap=sns.color_palette("rocket_r", as_cmap=True)),
                  label="$|\mathrm{median}/\sigma|$",
                  ax=g.axes
                 )
g.axes.collections[59].set_linewidth(3) # GW200129_065458
g.axes.collections[59].set_edgecolor(sns.color_palette()[9])

g.figure.savefig(fname=paths.figures/"violin_kappa.pdf", bbox_inches="tight", dpi=300)