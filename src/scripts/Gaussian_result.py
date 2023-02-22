import numpy as np
import pandas as pd
import paths

samples_Gaussian = np.load(paths.data/"samples_Gaussian_without_GW200129.npz")["chains"]
df = pd.DataFrame()
df['mu'] = samples_Gaussian.reshape(-1,2)[:,0]
df['sigma'] = samples_Gaussian.reshape(-1,2)[:,1]
mu_median = np.median(df['mu'])
sigma_median = np.median(df['sigma'])

with open(paths.output/"mu_median.txt", "w") as f:
    f.write(rf"${mu_median:.3f}^{{+{(np.percentile(a=df['mu'],q=95)-mu_median):.3f}}}_{{{(np.percentile(a=df['mu'],q=5)-mu_median):.3f}}}$")

with open(paths.output/"sigma_median.txt", "w") as f:
    f.write(rf"${np.percentile(a=df['sigma'],q=90):.3f}$")
