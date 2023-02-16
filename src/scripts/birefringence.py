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
df = 0.125
f_min = 20
f_max = 2048
f_ref = 100

# source parameters
m1_msun = 10
m2_msun = 10
chi1 = [0, 0, 0]
chi2 = [0, 0, 0]
dist_mpc = 400
inclination = np.pi/2
phi_ref = 0

# birefringence
kappa = 0.6

m1_kg = m1_msun*lal.MSUN_SI
m2_kg = m2_msun*lal.MSUN_SI
distance = dist_mpc*1e6*lal.PC_SI

hp_freq, hc_freq = lalsim.SimInspiralChooseFDWaveform(m1_kg, m2_kg,
                                            chi1[0], chi1[1], chi1[2],
                                            chi2[0], chi2[1], chi2[2],
                                            distance, inclination,
                                            phi_ref, 0, 0., 0.,
                                            df, f_min, f_max, f_ref,
                                            None, approximant)

freq = np.arange(len(hp_freq.data.data))*df

# let's shift the peak of the waveform `tshift` s before the end of the segment
tshift = 1
hp_fd = hp_freq.data.data * np.exp(2j*np.pi*freq*tshift)
hc_fd = hc_freq.data.data * np.exp(2j*np.pi*freq*tshift)

hl_fd = (hp_fd + (hc_fd * 1j)) /np.sqrt(2)
hr_fd = (hp_fd - (hc_fd * 1j)) /np.sqrt(2)

# apply birefringent transformation and get corresponding plus and cross
hl_bi_fd = hl_fd * np.exp(kappa*(dist_mpc/1000)*(freq/100))
hr_bi_fd = hr_fd * np.exp(-kappa*(dist_mpc/1000)*(freq/100))

hp_bi_fd = (hl_bi_fd + hr_bi_fd) / np.sqrt(2)
hc_bi_fd = 1j*(hl_bi_fd - hr_bi_fd) / np.sqrt(2)

# IFFT all plus and cross
hp_td = np.fft.irfft(hp_fd)
hc_td = np.fft.irfft(hc_fd)

hp_bi_td = np.fft.irfft(hp_bi_fd)
hc_bi_td = np.fft.irfft(hc_bi_fd)

time = np.arange(len(hp_bi_td))/(2*max(freq))
t0 = time[-1] - tshift
time -= t0

fig, axs = plt.subplots(2,1, figsize=(10,8))

c1 = sns.color_palette()[0]
c2 = sns.color_palette()[3]
axs[0].loglog(freq, np.abs(hl_fd), ls=':', c=c1, label=r"L (GR)")
axs[0].loglog(freq, np.abs(hr_fd), ls=':', c=c2, label=r"R (GR)")
axs[0].loglog(freq, np.abs(hl_bi_fd), c=c1, label=r"L (BR)")
axs[0].loglog(freq, np.abs(hr_bi_fd), c=c2, label=r"R (BR)")
axs[0].set_xlim(f_min+1,f_max-22)
axs[0].set_ylim(1e-30,1e-20)
axs[0].legend()
axs[0].set_ylabel(r"$|\tilde{h}|$")
axs[0].set_xlabel(r"$f\mathrm{(Hz)}$")
axs[0].set_yticks([])

axs[1].plot(time, hp_td, ls=':', c=c1, label="GR")
axs[1].plot(time, hp_bi_td, ls='-', c=c2, label="BR")
axs[1].set_ylabel(r"$h_+$")

# axs[2].plot(time, hc_td, ls=':', c=c1, label=r"$+$ (GR)")
# axs[2].plot(time, hc_bi_td, ls='-', c=c2, label=r"$+$ (BR)")
# axs[2].set_ylabel(r"$h_\times$")

for ax in axs[1:]:
    ax.legend()
    ax.set_xlabel(r"$t\mathrm{(s)}$")
    ax.set_xlim(-0.05, 0.01)
    ax.set_yticks([])

fig.tight_layout(pad=0.3)
fig.savefig(paths.figures/"birefringence.pdf", bbox_inches="tight")
