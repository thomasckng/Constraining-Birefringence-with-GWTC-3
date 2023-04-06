import numpy as np
import pandas as pd
import scipy
import paths

def normal_distribution(x, mu, sigma):
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)

result_dict = {}
result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
events = result_DataFrame['event'].unique()
for event in events:
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]

samples_original = np.load(paths.data/"samples_Gaussian.npz")["chains"]
samples_all = samples_original.reshape(-1, 2)
df_Gaussian_samples_all = pd.DataFrame()
df_Gaussian_samples_all['mu'] = samples_all[:,0]
df_Gaussian_samples_all['sigma'] = samples_all[:,1]

# generic constraint
samples_reweighted = []
for _ in range(1000):
    Gaussian = np.full(shape=(len(result_DataFrame), 2), fill_value=df_Gaussian_samples_all.sample(1))
    weight = normal_distribution(result_DataFrame['kappa'], Gaussian[:,0], Gaussian[:,1])
    weight /= weight.sum()
    samples_reweighted.append(np.random.choice(a=np.array(result_DataFrame['kappa']), size=1, p=weight))
samples_reweighted = np.array(samples_reweighted).reshape(-1)

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

generic_kappa_median = np.median(samples_reweighted)
generic_kappa_95 = np.percentile(a=samples_reweighted,q=95)
generic_kappa_5 = np.percentile(a=samples_reweighted,q=5)
with open(paths.output/"generic_kappa_median.txt", "w") as f:
    f.write(f"${generic_kappa_median:.3f}^{{+{(generic_kappa_95-generic_kappa_median):.3f}}}_{{{(generic_kappa_5-generic_kappa_median):.3f}}}$")

credible_level = len(likelihood[likelihood > np.interp(0, kappa, likelihood)])/len(likelihood)
with open(paths.output/"CL_kappa_0.txt", "w") as f:
    f.write(f"${credible_level:.3f}$")

restricted_kappa_mean = np.trapz(kappa*likelihood,kappa)
restricted_kappa_var = np.trapz(np.square(kappa-restricted_kappa_mean)*likelihood,kappa)
restricted_kappa_std = np.sqrt(restricted_kappa_var)
with open(paths.output/"restricted_kappa_std.txt", "w") as f:
    f.write(f"${restricted_kappa_std:.2f}$")

absolute_kappa = kappa[len(kappa)//2:]
likelihood_absolute_kappa = likelihood[len(kappa)//2:]+likelihood[0:len(kappa)//2][::-1] # for len(kappa) even
restricted_cdf_absolute_kappa = np.array([np.trapz(likelihood_absolute_kappa[0:i],absolute_kappa[0:i]) for i in range(len(absolute_kappa))])
restricted_absolute_kappa_90 = np.interp(0.9,restricted_cdf_absolute_kappa,absolute_kappa)
with open(paths.output/"restricted_absolute_kappa_90.txt", "w") as f:
    f.write(f"${restricted_absolute_kappa_90:.2f}$")
