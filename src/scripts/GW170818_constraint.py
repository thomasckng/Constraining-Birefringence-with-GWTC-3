import pandas as pd
import paths

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")

mean_over_std_GW170818 = result_DataFrame[result_DataFrame.event == "GW170818"]['kappa'].mean() / result_DataFrame[result_DataFrame.event == "GW170818"]['kappa'].std()

with open(paths.output/"GW170818_constraint.txt", "w") as f:
    f.write(rf"$\mu_i / \sigma_i = {mean_over_std_GW170818:.1f}$")