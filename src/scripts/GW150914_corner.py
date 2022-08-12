import h5py
import pandas as pd
import numpy as np
import seaborn as sns
from bilby.gw.result import CBCResult
import paths

sns.set_theme(palette='colorblind', font_scale=1.2)

nsamples = 5000

with h5py.File(paths.data/"IGWN-GWTC2p1-v2-GW150914_095045_PEDataRelease_mixed_nocosmo.h5", 'r') as f:
    f = f['C01:IMRPhenomXPHM']
    result_ligo = pd.DataFrame.from_records(f["posterior_samples"][()])
result_ligo = result_ligo.sample(n=nsamples)
result_ligo['kappa'] = np.zeros(len(result_ligo))
result_ligo['with'] = np.full(len(result_ligo), "GR (LIGO)")

result_bilby = CBCResult.from_json(filename=paths.data/"GW150914_birefringence.json").posterior
result_bilby = result_bilby.sample(n=nsamples)
result_bilby['with'] = np.full(len(result_bilby), "Non-GR (frequency dependent)")
result_bilby['cos_iota'] = np.cos(result_bilby['iota'])

result_extra = CBCResult.from_json(filename=paths.data/"GW150914_birefringence(frequency_independent).json").posterior
result_extra = result_extra.sample(n=nsamples)
result_extra['kappa'] = result_extra['kappa'] * 1000 # different scale was used in the frequency independent data
result_extra['with'] = np.full(len(result_extra), "Non-GR (frequency independent)")
result_extra['cos_iota'] = np.cos(result_extra['iota'])

result = pd.concat([result_bilby,result_extra,result_ligo], ignore_index=True)

g = sns.pairplot(result,
                 vars=['kappa', 'luminosity_distance', 'cos_iota'],
                 corner=True, kind='kde', hue='with',
                 diag_kws=dict(common_norm=False), plot_kws=dict(common_norm=False, levels=[(1.-0.954499736),(1.-0.682689492)]))

g.axes[2,0].set_xlabel("$\kappa$")
g.axes[1,0].set_ylabel("$d_L$")
g.axes[2,1].set_xlabel("$d_L$")
g.axes[2,0].set_ylabel("$\cos\iota$")
g.axes[2,2].set_xlabel("$\cos\iota$")
g.fig.legends[0].set_bbox_to_anchor((0.65,0.8))

g.savefig(fname=paths.figures/"GW150914_corner.png", bbox_inches="tight", dpi=300)