import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import gaussian_kde
from bilby.gw.cosmology import get_cosmology
import paths

# constants
h = 4.135667696e-15 # eV s
c = 299792.458 # km/s
H_0 = get_cosmology().H0.value # km/s/Mpc

sns.set_theme(palette='colorblind', font_scale=1.2)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"]
})

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
events = result_DataFrame['event'].unique()

M_PV_inv = np.linspace(0, 1.5e21, 1000)
kappa = (h*np.pi*H_0/c)*(1e3)*(100)*(M_PV_inv)/1e9

chosen_events = ['GW190727_060333', 'GW200112_155838', 'GW190513_205428', 'GW190915_235702', 'GW190803_022701', 'GW200311_115853']

kernel_dict = {}
for event in chosen_events:
    kernel_dict[event] = gaussian_kde(result_DataFrame[result_DataFrame.event == event]['kappa'])
    plt.plot(M_PV_inv, kernel_dict[event](kappa)+kernel_dict[event](-kappa), label=event)
    
plt.legend(fontsize=14)
plt.xlim(0, 1.5e21)
plt.ylabel(r'$p\left(M_\mathrm{PV}^{-1}\right)$')
plt.xlabel(r'$M_\mathrm{PV}^{-1}\, \left(\mathrm{GeV^{-1}}\right)$')

plt.savefig(fname=paths.figures/"posterior_MPV.pdf", bbox_inches="tight", dpi=300)
