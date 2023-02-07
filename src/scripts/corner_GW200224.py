import h5py
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import paths

sns.set_theme(palette='colorblind', font_scale=1.2)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

nsamples = 5000

with h5py.File(paths.data/"IGWN-GWTC3p0-v1-GW200224_222234_PEDataRelease_mixed_nocosmo.h5", 'r') as f:
    f = f['C01:IMRPhenomXPHM']
    result_ligo = pd.DataFrame.from_records(f["posterior_samples"][()])
result_ligo = result_ligo.sample(n=nsamples)
result_ligo['kappa'] = np.zeros(len(result_ligo))
result_ligo['with'] = np.full(len(result_ligo), r"GR (LVK)")

result_bilby = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_bilby = result_bilby[result_bilby.event == "GW200224_222234"]
result_bilby = result_bilby.sample(n=nsamples)
result_bilby['with'] = np.full(len(result_bilby), r"birefringence (frequency dependent)")
result_bilby['cos_iota'] = np.cos(result_bilby['iota'])

result = pd.concat([result_bilby,result_ligo], ignore_index=True)

g = sns.pairplot(result,
                    vars=['kappa', 'mass_ratio', 'chirp_mass', 'luminosity_distance',
                            'dec', 'ra', 'theta_jn', 'psi', 'a_1','a_2','tilt_1','tilt_2','phi_12','phi_jl',
                            'phase', 'geocent_time', 'log_likelihood',
                            ],
                    corner=True, kind='kde', hue='with',
                    diag_kws=dict(common_norm=False), plot_kws=dict(common_norm=False, levels=[
                            (1.-0.90),(1.-0.3935)]))

g.axes[16,0].set_xlabel("$\kappa$")
g.axes[1,0].set_ylabel("$q$")
g.axes[16,1].set_xlabel("$q$")
g.axes[2,0].set_ylabel("$\\mathcal{M}$[$M_{\\odot}$]")
g.axes[16,2].set_xlabel("$\\mathcal{M}$[$M_{\\odot}$]")
g.axes[3,0].set_ylabel("$d_L$")
g.axes[16,3].set_xlabel("$d_L$")
g.axes[4,0].set_ylabel("DEC")
g.axes[16,4].set_xlabel("DEC")
g.axes[5,0].set_ylabel("RA")
g.axes[16,5].set_xlabel("RA")
g.axes[6,0].set_ylabel("$\\theta_{JN}$")
g.axes[16,6].set_xlabel("$\\theta_{JN}$")
g.axes[7,0].set_ylabel("$\\psi$")
g.axes[16,7].set_xlabel("$\\psi$")
g.axes[8,0].set_ylabel("$a_1$")
g.axes[16,8].set_xlabel("$a_1$")
g.axes[9,0].set_ylabel("$a_2$")
g.axes[16,9].set_xlabel("$a_2$")
g.axes[10,0].set_ylabel("$\\theta_1$")
g.axes[16,10].set_xlabel("$\\theta_1$")
g.axes[11,0].set_ylabel("$\\theta_2$")
g.axes[16,11].set_xlabel("$\\theta_2$")
g.axes[12,0].set_ylabel("$\\Delta\\phi$")
g.axes[16,12].set_xlabel("$\\Delta\\phi$")
g.axes[13,0].set_ylabel("$\\phi_{JL}$")
g.axes[16,13].set_xlabel("$\\phi_{JL}$")
g.fig.legends[0].set_bbox_to_anchor((0.9,0.5))

g.savefig(fname=paths.figures/"corner_GW200224.pdf", bbox_inches="tight", dpi=300)