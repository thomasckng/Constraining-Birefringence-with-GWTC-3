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
inclination = np.pi * 0.9
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

hl_time = (hp_time.data.data + (hc_time.data.data * 1j)) /np.sqrt(2)
hr_time = (hp_time.data.data - (hc_time.data.data * 1j)) /np.sqrt(2)

time = np.arange(len(hl_time))*dt

hp_freq_fft = np.fft.fft(hp_time.data.data, norm="ortho")
hc_freq_fft = np.fft.fft(hc_time.data.data, norm="ortho")

n = np.fft.fftfreq(len(hp_freq_fft))
freq_fft = n[:len(n)//2]*len(n)//4

hl_freq_fft = (hp_freq_fft + (hc_freq_fft * 1j)) /np.sqrt(2)
hr_freq_fft = (hp_freq_fft - (hc_freq_fft * 1j)) /np.sqrt(2)

kappa = -0.01

hl_bi_freq_fft = hl_freq_fft[::2] * np.exp(kappa*(dist_mpc/1000)*(freq_fft/100))
hr_bi_freq_fft = hr_freq_fft[::2] * np.exp(-kappa*(dist_mpc/1000)*(freq_fft/100))

plt.subplot(211)
plt.plot(time+0.02, hl_time, ls='--', color=sns.color_palette()[0], label=r"L (GR)")
plt.plot(time+0.02, hr_time, ls=':', color=sns.color_palette()[3], label=r"R (GR)")
plt.xlim(8.3,8.5)
plt.legend()
plt.ylabel(r"$|{h}|$")
plt.yticks([])

plt.subplot(212)
plt.plot(time[::2]+0.051, np.fft.ifft(hl_bi_freq_fft, norm="ortho"), ls='-', color=sns.color_palette()[0], label=r"L (birefringence)")
plt.plot(time[::2]+0.051, np.fft.ifft(hr_bi_freq_fft, norm="ortho"), ls='-', color=sns.color_palette()[3], label=r"R (birefringence)")
plt.xlim(8.3,8.5)
plt.legend()
plt.ylabel(r"$|{h}|$")
plt.xlabel(r"$t\mathrm{(s)}$")
plt.yticks([])

plt.savefig(fname=paths.figures/"birefringence_time_domain.pdf", bbox_inches="tight", dpi=300)