import numpy as np
import paths

samples_Gaussian = np.load(paths.data/"samples_Gaussian_without_GW200129.npz")["chains"]
samples_Gaussian = samples_Gaussian.reshape(-1, 2)

with open(paths.output/"mu_mean.txt", "w") as f:
    f.write(f"${np.mean(samples_Gaussian[:,0]):.3f}\\pm{np.std(samples_Gaussian[:,0]):.3f}$")
with open(paths.output/"sigma_mean.txt", "w") as f:
    f.write(f"${np.mean(samples_Gaussian[:,1]):.3f}\\pm{np.std(samples_Gaussian[:,1]):.3f}$")
with open(paths.output/"mu_median.txt", "w") as f:
    f.write(f"${np.median(samples_Gaussian[:,0]):.3f}$")
with open(paths.output/"sigma_median.txt", "w") as f:
    f.write(f"${np.median(samples_Gaussian[:,1]):.3f}$")