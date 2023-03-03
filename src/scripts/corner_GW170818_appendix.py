import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from bilby.gw.result import CBCResult
import paths

sns.set_theme(palette='colorblind', font_scale=2.0)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

nsamples = 5000

result_GR = CBCResult.from_json(filename=paths.data/"GW170818_GR.json.gz").posterior
result_GR = result_GR.sample(n=nsamples)
result_GR['with'] = np.full(len(result_GR), "GR")
result_GR['cos_iota'] = np.cos([float(value) for value in result_GR['iota']])

result_bilby = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_bilby = result_bilby[result_bilby.event == "GW170818"]
result_bilby = result_bilby.sample(n=nsamples)
result_bilby['with'] = np.full(len(result_bilby), r"BR")
result_bilby['cos_iota'] = np.cos(result_bilby['iota'])

result = pd.concat([result_bilby,result_GR], ignore_index=True)

g = sns.pairplot(result,
            vars=['kappa','luminosity_distance','cos_iota','psi','a_1','a_2','tilt_1','tilt_2','phi_12','phi_jl','phase'],
            corner=True, kind='kde', hue='with',
            diag_kws=dict(common_norm=False),
            plot_kws=dict(common_norm=False, levels=[(1.-0.90),(1.-0.3935)]))

g.axes[10,0].set_xlabel("$\kappa$")
g.axes[1,0].set_ylabel("$d_L$ (Mpc)")
g.axes[10,1].set_xlabel("$d_L$ (Mpc)")
g.axes[2,0].set_ylabel("$\\cos\\iota$")
g.axes[10,2].set_xlabel("$\\cos\\iota$")
g.axes[3,0].set_ylabel("$\\psi$")
g.axes[10,3].set_xlabel("$\\psi$")
g.axes[4,0].set_ylabel("$a_1$")
g.axes[10,4].set_xlabel("$a_1$")
g.axes[5,0].set_ylabel("$a_2$")
g.axes[10,5].set_xlabel("$a_2$")
g.axes[6,0].set_ylabel("$\\theta_1$")
g.axes[10,6].set_xlabel("$\\theta_1$")
g.axes[7,0].set_ylabel("$\\theta_2$")
g.axes[10,7].set_xlabel("$\\theta_2$")
g.axes[8,0].set_ylabel("$\\Delta\\phi$")
g.axes[10,8].set_xlabel("$\\Delta\\phi$")
g.axes[9,0].set_ylabel("$\\phi_{JL}$")
g.axes[10,9].set_xlabel("$\\phi_{JL}$")
g.axes[10,0].set_ylabel("$\\phi_{\\rm{ref}}$")
g.axes[10,10].set_xlabel("$\\phi_{\\rm{ref}}$")

g.fig.legends[0].set_bbox_to_anchor((0.92,0.5))
g.legend.set_title(None)

g.savefig(fname=paths.figures/"corner_GW170818_appendix.pdf", bbox_inches="tight", dpi=300)
