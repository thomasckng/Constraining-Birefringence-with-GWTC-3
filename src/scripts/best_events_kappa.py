import numpy as np
import pandas as pd
import scipy
import paths

def sign(x):
    if x > 0:
        return "+"
    elif x <= 0:
        return ""

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")
events = result_DataFrame['event'].unique()

result_dict = {}
for event in events:
    result_dict[event] = {}
    result_dict[event]['kappa'] = result_DataFrame[result_DataFrame.event == event]['kappa'].values

    result_dict[event]['kappa_std'] = result_dict[event]['kappa'].std()
    
result_dict = {k: v for k, v in sorted(result_dict.items(), key=lambda item: item[1]['kappa_std'])}

with open(paths.output/"best_events_kappa.txt", "w") as f:
    f.write(r"\begin{tabular}{lccc}Event & $\kappa$ & $\sigma_i$ & CL\\ \hline ")
    for i, event in enumerate(result_dict):
        result_dict[event]['event'] = event.replace("_", r"\_")
        
        result_dict[event]['kappa_median'] = np.median(result_dict[event]['kappa'])
        result_dict[event]['kappe_95'] = np.quantile(result_dict[event]['kappa'], 0.95) - result_dict[event]['kappa_median']
        result_dict[event]['kappe_5'] = result_dict[event]['kappa_median'] - np.quantile(result_dict[event]['kappa'], 0.05)

        kernel = scipy.stats.gaussian_kde(result_dict[event]['kappa'])
        kde = [kernel(kappa) for kappa in result_dict[event]['kappa']]
        kde = np.array(kde)
        result_dict[event]['credible_level'] = len(kde[kde > kernel(0)[0]])/len(kde)

        f.write(rf"{result_dict[event]['event']} & ${sign(result_dict[event]['kappa_median'])}{result_dict[event]['kappa_median']:.3f}^{{+{result_dict[event]['kappe_95']:.3f}}}_{{-{result_dict[event]['kappe_5']:.3f}}}$ & ${result_dict[event]['kappa_std']:.3f}$ & ${result_dict[event]['credible_level']:.3f}$")
        if i != 9:
            f.write(r"\\")
        else:
            break
    f.write(r" \end{tabular}")
