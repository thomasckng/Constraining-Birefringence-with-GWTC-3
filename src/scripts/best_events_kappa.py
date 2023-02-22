import numpy as np
import pandas as pd
import paths

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
events = result_DataFrame['event'].unique()

result_dict = {}
for event in events:
    result_dict[event] = {}
    result_dict[event]['event'] = event.replace("_", r"\_")
    result_dict[event]['kappa_median'] = result_DataFrame[result_DataFrame.event == event]['kappa'].median()
    result_dict[event]['kappa_std'] = result_DataFrame[result_DataFrame.event == event]['kappa'].std()
    result_dict[event]['kappe_95'] = np.quantile(result_DataFrame[result_DataFrame.event == event]['kappa'], 0.95) - result_dict[event]['kappa_median']
    result_dict[event]['kappe_5'] = result_dict[event]['kappa_median'] - np.quantile(result_DataFrame[result_DataFrame.event == event]['kappa'], 0.05)
result_dict = {k: v for k, v in sorted(result_dict.items(), key=lambda item: item[1]['kappa_std'])}

with open(paths.output/"best_events_kappa.txt", "w") as f:
    f.write(r"\begin{tabular}{lr}Event & $\tilde{\kappa}$ (dimensionless)\\ \hline ")
    for i, event in enumerate(result_dict):
        f.write(rf"{result_dict[event]['event']} & ${result_dict[event]['kappa_median']:.3f}^{{+{result_dict[event]['kappe_95']:.3f}}}_{{-{result_dict[event]['kappe_5']:.3f}}}$")
        if i != 3:
            f.write(r"\\")
        else:
            break
    f.write(r" \end{tabular}")
