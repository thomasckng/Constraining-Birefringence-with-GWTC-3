# following script is used to generate reweighted_kappa_samples.feather and reweighted_kappa_samples_without_GW200129.feather

import numpy as np
import pandas as pd
import paths

def normal_distribution(x, mu, sigma):
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)

result_DataFrame = pd.read_feather(paths.data/'samples_posterior_birefringence.feather')

samples_original = np.load(paths.data/'samples_Gaussian.npz')["chains"] # use this for reweighted_kappa_samples.feather
# samples_original = np.load(paths.data/'samples_Gaussian_without_GW200129.npz')["chains"] # use this for reweighted_kappa_samples_without_GW200129.feather

samples_all = samples_original.reshape(-1, 2)

df_Gaussian_samples_all = pd.DataFrame()
df_Gaussian_samples_all['mu'] = samples_all[:,0]
df_Gaussian_samples_all['sigma'] = samples_all[:,1]

reweighted_kappa_samples = pd.DataFrame()

rng = np.random.default_rng(12345)

for event in result_DataFrame['event'].unique():
    samples_reweighted = []
    result_DataFrame_event = result_DataFrame[result_DataFrame.event == event]
    length = len(result_DataFrame_event)
    for _ in range(3000):
        Gaussian = np.full(shape=(length, 2), fill_value=df_Gaussian_samples_all.sample(1, random_state=rng))
        weight = np.array([normal_distribution(result_DataFrame_event['kappa'][i], Gaussian[i,0], Gaussian[i,1]) for i in range(len(result_DataFrame_event['kappa']))])
        weight /= weight.sum()
        samples_reweighted.append(np.random.choice(a=np.array(result_DataFrame_event['kappa']), size=1, p=weight))
    reweighted_kappa_samples[event] = np.array(samples_reweighted).reshape(-1)
    print(event+" done!")

reweighted_kappa_samples.to_feather(paths.static/'reweighted_kappa_samples.feather')
# reweighted_kappa_samples.to_feather(paths.static/'reweighted_kappa_samples_without_GW200129.feather')
