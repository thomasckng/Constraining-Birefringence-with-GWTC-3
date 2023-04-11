import pandas as pd
import paths

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")

mean_over_std_GW200129 = result_DataFrame[result_DataFrame.event == "GW200129_065458"]['kappa'].mean() / result_DataFrame[result_DataFrame.event == "GW200129_065458"]['kappa'].std()

with open(paths.output/"GW200129_constraint.txt", "w") as f:
    f.write(rf"$\mu_i / \sigma_i = {mean_over_std_GW200129:.1f}$")