import numpy as np
import pandas as pd
import scipy
import paths

def normal_distribution(x, mu, sigma):
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)

result_dict = {}
result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
result_DataFrame = result_DataFrame[result_DataFrame.event != "GW200129_065458"]
events = result_DataFrame['event'].unique()
for event in events:
    result_dict[event] = result_DataFrame[result_DataFrame.event == event]

samples_original = np.load(paths.data/"samples_Gaussian_without_GW200129.npz")["chains"]
samples_all = samples_original.reshape(-1, 2)
df_Gaussian_samples_all = pd.DataFrame()
df_Gaussian_samples_all['mu'] = samples_all[:,0]
df_Gaussian_samples_all['sigma'] = samples_all[:,1]

samples_reweighted = []
for _ in range(1000):
    Gaussian = np.full(shape=(len(result_DataFrame), 2), fill_value=df_Gaussian_samples_all.sample(1))
    weight = normal_distribution(result_DataFrame['kappa'], Gaussian[:,0], Gaussian[:,1])
    weight /= weight.sum()
    samples_reweighted.append(np.random.choice(a=np.array(result_DataFrame['kappa']), size=1, p=weight))

kernels = [scipy.stats.gaussian_kde(result_dict[event]['kappa']) for event in events[events != "GW200129_065458"]]
kappa = np.linspace(-.1, .1, 1000)
ll = [np.sum([np.log(ker(k)) for ker in kernels]) for k in kappa]
ll = ll - np.max(ll)
likelihood = np.exp(ll)
likelihood = likelihood / np.trapz(likelihood, x=kappa)

restricted_kappa_median = np.interp(0.5,[np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)],kappa)
generic_kappa_median = np.median(np.array(samples_reweighted).reshape(-1))

with open(paths.output/"restricted_kappa_median.txt", "w") as f:
    f.write(f"${restricted_kappa_median:.3f}^{(np.interp(0.95,[np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)],kappa)-restricted_kappa_median):.3f}_{(np.interp(0.05,[np.trapz(likelihood[0:i],kappa[0:i]) for i in range(1000)],kappa)-restricted_kappa_median):.3f}$")

with open(paths.output/"generic_kappa_median.txt", "w") as f:
    f.write(f"${generic_kappa_median:.3f}^{(np.percentile(a=np.array(samples_reweighted).reshape(-1),q=95)-generic_kappa_median):.3f}_{(np.percentile(a=np.array(samples_reweighted).reshape(-1),q=5)-generic_kappa_median):.3f}$")
