import numpy as np
import pandas as pd
import scipy
import paths

# constants
h = 4.135667696e-15 # eV s
c = 299792.458 # km/s
H_0 = 68.3 # km/s/Mpc

result_dict = {}
result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
events = result_DataFrame['event'].unique()
for event in events:
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]

# restricted constraint
kernels = [scipy.stats.gaussian_kde(result_dict[event]['kappa']) for event in events]
kappa = np.linspace(-.1, .1, 1000)
ll = [np.sum([np.log(ker(k)) for ker in kernels]) for k in kappa]
ll = ll - np.max(ll)
likelihood = np.exp(ll)
likelihood = likelihood / np.trapz(likelihood, x=kappa)

# output results
restricted_cdf = np.array([np.trapz(likelihood[0:i],kappa[0:i]) for i in range(len(kappa))])
restricted_kappa_median = np.interp(0.5,restricted_cdf,kappa)
restricted_kappa_95 = np.interp(0.95,restricted_cdf,kappa)
restricted_kappa_5 = np.interp(0.05,restricted_cdf,kappa)
with open(paths.output/"restricted_kappa_median.txt", "w") as f:
    f.write(f"$\kappa = {restricted_kappa_median:.3f}^{{+{(restricted_kappa_95-restricted_kappa_median):.3f}}}_{{{(restricted_kappa_5-restricted_kappa_median):.3f}}}$")

credible_level = len(likelihood[likelihood > np.interp(0, kappa, likelihood)])/len(likelihood)
with open(paths.output/"CL_kappa_0.txt", "w") as f:
    f.write(f"${credible_level:.3f}$")

absolute_kappa = kappa[len(kappa)//2:]
likelihood_absolute_kappa = likelihood[len(kappa)//2:]+likelihood[0:len(kappa)//2][::-1] # for len(kappa) even
restricted_cdf_absolute_kappa = np.array([np.trapz(likelihood_absolute_kappa[0:i],absolute_kappa[0:i]) for i in range(len(absolute_kappa))])
restricted_absolute_kappa_68 = np.interp(0.68,restricted_cdf_absolute_kappa,absolute_kappa)
with open(paths.output/"restricted_absolute_kappa_68.txt", "w") as f:
    f.write(f"$|\kappa| < {restricted_absolute_kappa_68:.2f}$")

improvement_Okounkova = 0.74/restricted_absolute_kappa_68
with open(paths.output/"improvement_Okounkova.txt", "w") as f:
    f.write(rf"${{\sim}}{int(np.round(improvement_Okounkova))}\times$")

restricted_absolute_kappa_90 = np.interp(0.9,restricted_cdf_absolute_kappa,absolute_kappa)
with open(paths.output/"restricted_absolute_kappa_90.txt", "w") as f:
    f.write(f"$|\kappa| < {restricted_absolute_kappa_90:.2f}$")

# Wang's constraint in kappa
M_PV_Wang = 1e-22 # GeV
kappa_Wang = (h*np.pi*H_0/c)*(1e3)*(100)*np.reciprocal(M_PV_Wang*1e9)
with open(paths.output/"kappa_Wang.txt", "w") as f:
    f.write(f"$|\kappa| \lesssim {kappa_Wang:.2f}$")

# Constraint comparison
kappa_Okounkova = 0.74
M_PV_Okounkova = (h*np.pi*H_0/c)*(1e3)*(100)*np.reciprocal(kappa_Okounkova)/1e9

kappa_this_work = restricted_absolute_kappa_90
M_PV_this_work = (h*np.pi*H_0/c)*(1e3)*(100)*np.reciprocal(kappa_this_work)/1e9

with open(paths.output/"M_PV_constraint.txt", "w") as f:
    f.write(rf"$M_{{\rm PV}} \gtrsim {M_PV_this_work/1e-21:.1f} \times 10^{{-21}}\, {{\rm GeV}}$")

with open(paths.output/"comparison_summary.txt", "w") as f:
    f.write(r"\begin{tabular}{lccc} & $M_{\rm PV}$ ($10^{-21}\, {\rm GeV}$) & $|\kappa|$ & CL (\%) \\ \hline ")
    f.write(rf"\citet{{Wang_2021}} & $> {M_PV_Wang/1e-21:.2f}$ & $< {kappa_Wang:.2f}$ & 90 \\ ")
    f.write(rf"\citet{{Okounkova_2022}} & $> {M_PV_Okounkova/1e-21:.2f}$ & $< {kappa_Okounkova:.2f}$ & 68 \\ ")
    f.write(rf"Ng \emph{{et al.}} (this work) & $> {M_PV_this_work/1e-21:.2f}$ & $< {kappa_this_work:.2f}$ & 90")
    f.write(r" \end{tabular}")
