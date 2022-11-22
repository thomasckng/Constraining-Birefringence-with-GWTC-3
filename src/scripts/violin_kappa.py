import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import paths

sns.set_theme(palette='colorblind', font_scale=1.2)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"]
})

result_dict = {}
median_std_dict = {}
result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_DataFrame = result_DataFrame[result_DataFrame.event != "GW200129_065458"] # remove GW200129
for event in result_DataFrame['event'].unique():
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]
    median_std_dict[event] = abs(result_dict[event]['kappa'].median()/result_dict[event]['kappa'].std())
median_std_dict = {k: v for k, v in sorted(median_std_dict.items(), key=lambda item: item[1])}

samples_Gaussian = np.load(paths.data/"samples_Gaussian_without_GW200129.npz")["chains"]
samples_Gaussian = samples_Gaussian.reshape(-1, 2)
mu_median = np.median(samples_Gaussian[:,0])
sigma_median = np.median(samples_Gaussian[:,1])

g = sns.violinplot(data=result_DataFrame, x="event", y="kappa", scale="width", inner=None, 
                    order=list(median_std_dict.keys()), palette="magma"
                   )

g.set_ylabel("$\kappa$", fontsize=20)
g.set_ylim(-0.2,0.2)
g.set_xlabel("")
g.axhline(0, color=sns.color_palette()[3])
x_low, x_high = g.get_xlim()
g.fill_between([x_low-1,x_high+1], mu_median-sigma_median, mu_median+sigma_median, alpha=0.3, color=sns.color_palette()[9])
g.set_xlim(x_low-0.5,x_high+0.5)
g.axhline(mu_median,color=sns.color_palette()[9])
g.figure.autofmt_xdate(rotation=45)
g.figure.set_size_inches(30,10)

g.figure.savefig(fname=paths.figures/"violin_kappa.pdf", bbox_inches="tight", dpi=300)