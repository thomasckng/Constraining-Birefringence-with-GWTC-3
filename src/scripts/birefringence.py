import numpy as np
import matplotlib.pyplot as plt
import lalsimulation as lalsim
import lal
import seaborn as sns
import paths

sns.set_theme(palette='colorblind', font_scale=1.2)

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Computer Modern Roman"],
})

approximant = lalsim.SimInspiralGetApproximantFromString("IMRPhenomD")

# frequency array parameters
df = 0.25
f_min = 20
f_max = 2030
f_ref = 100

# source parameters
m1_msun = 10
m2_msun = 10
chi1 = [0, 0, 0]
chi2 = [0, 0, 0]
dist_mpc = 1000
inclination = np.pi * 0.9
phi_ref = 0

m1_kg = m1_msun*lal.MSUN_SI
m2_kg = m2_msun*lal.MSUN_SI
distance = dist_mpc*1e6*lal.PC_SI

hp, hc = lalsim.SimInspiralChooseFDWaveform(m1_kg, m2_kg,
                                            chi1[0], chi1[1], chi1[2],
                                            chi2[0], chi2[1], chi2[2],
                                            distance, inclination,
                                            phi_ref, 0, 0., 0.,
                                            df, f_min, f_max, f_ref,
                                            None, approximant)

hl = (hp.data.data + (hc.data.data * 1j)) /np.sqrt(2)
hr = (hp.data.data - (hc.data.data * 1j)) /np.sqrt(2)

freq = np.arange(len(hl))*df

kappa = -0.5

hl_bi_L = hl * np.exp(kappa*(dist_mpc/1000)*(freq/100))
hr_bi_L = hr * np.exp(-kappa*(dist_mpc/1000)*(freq/100))

plt.loglog(freq, abs(hl), ls='--', color=sns.color_palette()[0], label=r"L (GR)")
plt.loglog(freq, abs(hr), ls='--', color=sns.color_palette()[3], label=r"R (GR)")
plt.loglog(freq, abs(hl_bi_L), color=sns.color_palette()[0], label=r"L (br)")
plt.loglog(freq, abs(hr_bi_L), color=sns.color_palette()[3], label=r"R (br)")
plt.xlim(f_min+1,f_max-10)
plt.ylim(1e-38,1e-20)
plt.legend()
plt.ylabel(r"$|\tilde{h}|$")
plt.xlabel(r"$f\mathrm{(Hz)}$")

plt.savefig(fname=paths.figures/"birefringence.pdf", bbox_inches="tight", dpi=300)