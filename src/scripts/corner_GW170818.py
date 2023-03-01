import h5py
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import paths

sns.set_theme(palette='colorblind', font_scale=1.5)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

nsamples = 5000

with h5py.File(paths.data/"IGWN-GWTC2p1-v2-GW170818_022509_PEDataRelease_mixed_nocosmo.h5", 'r') as f:
    f = f['C01:IMRPhenomXPHM']
    result_ligo = pd.DataFrame.from_records(f["posterior_samples"][()])
result_ligo = result_ligo.sample(n=nsamples)
result_ligo['kappa'] = np.zeros(len(result_ligo))
result_ligo['with'] = np.full(len(result_ligo), "GR")

result_bilby = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_bilby = result_bilby[result_bilby.event == "GW170818"]
result_bilby = result_bilby.sample(n=nsamples)
result_bilby['with'] = np.full(len(result_bilby), "BR")
result_bilby['cos_iota'] = np.cos(result_bilby['iota'])

result = pd.concat([result_bilby,result_ligo], ignore_index=True)

g = sns.pairplot(result,
                    vars=['kappa', 'luminosity_distance', 'cos_iota'],
                    corner=True, kind='kde', hue='with',
                    diag_kws=dict(common_norm=False), plot_kws=dict(common_norm=False, levels=[
                            (1.-0.90),(1.-0.3935)]))

g.axes[2,0].set_xlabel(r"$\kappa$")
g.axes[1,0].set_ylabel(r"$d_L$ (Mpc)")
g.axes[2,1].set_xlabel(r"$d_L$ (Mpc)")
g.axes[2,0].set_ylabel(r"$\cos\iota$")
g.axes[2,2].set_xlabel(r"$\cos\iota$")
g.fig.legends[0].set_bbox_to_anchor((0.55,0.8))
g.legend.set_title(None)
plt.subplots_adjust(wspace=0.05, hspace=0.05)

g.savefig(fname=paths.figures/"corner_GW170818.pdf", bbox_inches="tight", dpi=300)
