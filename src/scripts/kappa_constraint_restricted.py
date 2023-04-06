import numpy as np
import pandas as pd
import scipy
import paths

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
    f.write(f"${restricted_kappa_median:.3f}^{{+{(restricted_kappa_95-restricted_kappa_median):.3f}}}_{{{(restricted_kappa_5-restricted_kappa_median):.3f}}}$")

credible_level = len(likelihood[likelihood > np.interp(0, kappa, likelihood)])/len(likelihood)
with open(paths.output/"CL_kappa_0.txt", "w") as f:
    f.write(f"${credible_level:.3f}$")

absolute_kappa = kappa[len(kappa)//2:]
likelihood_absolute_kappa = likelihood[len(kappa)//2:]+likelihood[0:len(kappa)//2][::-1] # for len(kappa) even
restricted_cdf_absolute_kappa = np.array([np.trapz(likelihood_absolute_kappa[0:i],absolute_kappa[0:i]) for i in range(len(absolute_kappa))])
restricted_absolute_kappa_68 = np.interp(0.6827,restricted_cdf_absolute_kappa,absolute_kappa)
with open(paths.output/"restricted_absolute_kappa_68.txt", "w") as f:
    f.write(f"${restricted_absolute_kappa_68:.2f}$")
restricted_absolute_kappa_90 = np.interp(0.9,restricted_cdf_absolute_kappa,absolute_kappa)
with open(paths.output/"restricted_absolute_kappa_90.txt", "w") as f:
    f.write(f"${restricted_absolute_kappa_90:.2f}$")
