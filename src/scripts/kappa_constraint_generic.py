import numpy as np
import pandas as pd
import paths

def normal_distribution(x, mu, sigma):
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")

samples_original = np.load(paths.data/"samples_Gaussian.npz")["chains"]
samples_all = samples_original.reshape(-1, 2)
df_Gaussian_samples_all = pd.DataFrame()
df_Gaussian_samples_all['mu'] = samples_all[:,0]
df_Gaussian_samples_all['sigma'] = samples_all[:,1]

# generic constraint
samples_reweighted = []
rng = np.random.default_rng(12345)
for _ in range(5000):
    Gaussian = np.full(shape=(len(result_DataFrame), 2), fill_value=df_Gaussian_samples_all.sample(1, random_state=rng))
    weight = normal_distribution(result_DataFrame['kappa'], Gaussian[:,0], Gaussian[:,1])
    weight /= weight.sum()
    samples_reweighted.append(np.random.choice(a=np.array(result_DataFrame['kappa']), size=1, p=weight))
samples_reweighted = np.array(samples_reweighted).reshape(-1)

# output results
generic_kappa_median = np.median(samples_reweighted)
generic_kappa_95 = np.percentile(a=samples_reweighted,q=95)
generic_kappa_5 = np.percentile(a=samples_reweighted,q=5)
with open(paths.output/"generic_kappa_median.txt", "w") as f:
    f.write(f"$\kappa_i = {generic_kappa_median:.3f}^{{+{(generic_kappa_95-generic_kappa_median):.3f}}}_{{{(generic_kappa_5-generic_kappa_median):.3f}}}$")
