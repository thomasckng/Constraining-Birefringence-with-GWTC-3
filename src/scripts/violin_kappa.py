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
result_DataFrame = pd.read_feather(paths.data/"samples_posterior_nonGR.feather")
for event in result_DataFrame['event'].unique():
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]
    median_std_dict[event] = abs(result_dict[event]['kappa'].median()/result_dict[event]['kappa'].std())
median_std_dict = {k: v for k, v in sorted(median_std_dict.items(), key=lambda item: item[1])}

samples_Gaussian = np.load(paths.data/"samples_Gaussian.npz")["chains"]
samples_Gaussian = samples_Gaussian.reshape(-1, 2)
mean_median = np.median(samples_Gaussian[:,0])
sd_median = np.median(samples_Gaussian[:,1])

g = sns.violinplot(data=result_DataFrame, x="event", y="kappa", scale="width", inner=None, 
                    order=list(median_std_dict.keys())
                   )

g.set_ylabel("$\kappa$", fontsize=20)
g.set_ylim(-0.2,0.2)
g.set_xlabel("")
g.axhline(0,color=sns.color_palette()[3])
x_low, x_high = g.get_xlim()
g.fill_between([x_low-1,x_high+1], mean_median-sd_median, mean_median+sd_median, alpha=0.2)
g.set_xlim(x_low-0.5,x_high+0.5)
g.axhline(mean_median,color=sns.color_palette()[0])
g.figure.autofmt_xdate(rotation=45)
g.figure.set_size_inches(30,10)

g.figure.savefig(fname=paths.figures/"violin_kappa.pdf", bbox_inches="tight", dpi=300)