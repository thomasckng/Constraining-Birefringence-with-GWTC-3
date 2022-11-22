import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import paths

sns.set_theme(palette='colorblind', font_scale=1.2)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

result_dict = {}
result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_DataFrame = result_DataFrame[result_DataFrame.event != "GW200129"] # remove GW200129
for event in result_DataFrame['event'].unique():
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]

for event in result_DataFrame['event'].unique():
    g = sns.kdeplot(result_dict[event]['kappa'], fill=True)

g.set_xlabel("$\kappa$")
g.set_xlim(-1,1)

g.figure.savefig(fname=paths.figures/"kappa_stacked.pdf", bbox_inches="tight", dpi=300)