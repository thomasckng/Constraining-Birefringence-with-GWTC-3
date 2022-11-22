import numpy as np
import pandas as pd
import paths

def normal_distribution(x, mu, sigma):
    return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mu)/sigma)**2)

samples_Gaussian = np.load(paths.data/"samples_Gaussian_without_GW200129.npz")["chains"]
df = pd.DataFrame()
df['mu'] = samples_Gaussian.reshape(-1,2)[:,0]
df['sigma'] = samples_Gaussian.reshape(-1,2)[:,1]

with open(paths.output/"mu_mean.txt", "w") as f:
    f.write(f"${np.mean(df['mu']):.3f}\\pm{np.std(df['mu']):.3f}$")
with open(paths.output/"sigma_mean.txt", "w") as f:
    f.write(f"${np.mean(df['sigma']):.3f}\\pm{np.std(df['sigma']):.3f}$")
with open(paths.output/"mu_median.txt", "w") as f:
    f.write(f"${np.median(df['mu']):.3f}$")
with open(paths.output/"sigma_median.txt", "w") as f:
    f.write(f"${np.median(df['sigma']):.3f}$")

kappa = np.linspace(-1, 1, 50000)
df = df.sample(10000)

population_probability = np.mean([normal_distribution(kappa[i], df['mu'], df['sigma']) for i in range(len(kappa))], axis=1)
population_probability = population_probability / np.trapz(population_probability, kappa)

kappa_mean = np.trapz(kappa * population_probability, kappa)
kappa_sd = np.sqrt(np.trapz(np.square(kappa - kappa_mean) * population_probability, kappa))

with open(paths.output/"kappa_mean.txt", "w") as f:
    f.write(f"${kappa_mean:.3f}\\pm{kappa_sd:.3f}$")