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
f_min = 20
f_ref = 100

# source parameters
m1_msun = 10
m2_msun = 10
chi1 = [0, 0, 0]
chi2 = [0, 0, 0]
dist_mpc = 1000
inclination = np.pi / 2
phi_ref = 0

m1_kg = m1_msun*lal.MSUN_SI
m2_kg = m2_msun*lal.MSUN_SI
distance = dist_mpc*1e6*lal.PC_SI

# time array parameters
dt = 1e-4

hp_time, hc_time = lalsim.SimInspiralChooseTDWaveform(m1_kg, m2_kg,
                                            chi1[0], chi1[1], chi1[2],
                                            chi2[0], chi2[1], chi2[2],
                                            distance, inclination,
                                            phi_ref, 0, 0., 0.,
                                            dt, f_min, f_ref,
                                            None, approximant)

time = np.arange(hp_time.data.length)*dt

hp_freq_fft = np.fft.fft(hp_time.data.data, norm="ortho")
hc_freq_fft = np.fft.fft(hc_time.data.data, norm="ortho")
n = np.fft.fftfreq(len(hp_freq_fft))
freq_fft = n[:len(n)//2]*len(n)//4

hl_freq_fft = (hp_freq_fft + (hc_freq_fft * 1j)) /np.sqrt(2)
hr_freq_fft = (hp_freq_fft - (hc_freq_fft * 1j)) /np.sqrt(2)

kappa = 0.01

hl_bi_freq_fft = hl_freq_fft[::2] * np.exp(kappa*(dist_mpc/1000)*(freq_fft/100))
hr_bi_freq_fft = hr_freq_fft[::2] * np.exp(-kappa*(dist_mpc/1000)*(freq_fft/100))

fig, axs = plt.subplots(2,1,sharex=True)

axs[0].plot(time+0.02, np.fft.ifft(hl_freq_fft, norm="ortho").real, ls='--', color=sns.color_palette()[0], label=r"L (GR)")
axs[0].plot(time+0.02, np.fft.ifft(hr_freq_fft, norm="ortho").real, ls=':', color=sns.color_palette()[3], label=r"R (GR)")
axs[0].legend()
axs[0].set_ylabel(r"${h}$")
axs[0].set_yticks([])

axs[1].plot(time[::2]+0.051, np.fft.ifft(hl_bi_freq_fft, norm="ortho").real, ls='-', color=sns.color_palette()[0], label=r"L (birefringence)")
axs[1].plot(time[::2]+0.051, np.fft.ifft(hr_bi_freq_fft, norm="ortho").real, ls='-', color=sns.color_palette()[3], label=r"R (birefringence)")
axs[1].set_xlim(8.3,8.5)
axs[1].legend()
axs[1].set_ylabel(r"${h}$")
axs[1].set_xlabel(r"$t\mathrm{(s)}$")
axs[1].set_yticks([])

fig.tight_layout(pad=0.3)

plt.savefig(fname=paths.figures/"birefringence_time_domain.pdf", bbox_inches="tight", dpi=300)