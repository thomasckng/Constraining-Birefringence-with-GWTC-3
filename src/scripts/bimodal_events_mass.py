import pandas as pd
import numpy as np
import scipy
import paths

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")

with open(paths.output/"bimodal_events_mass.txt", "w") as f:
    f.write(r"\begin{tabular}{lrrr}Event & Total Mass ($M_{\odot}$) & $\kappa$ & CL\\ \hline ")
    for event in ["GW170104", "GW190413_134308", "GW190521", "GW190805_211137", "GW191105_143521"]:
        name = event.replace("_", r"\_")

        mass = result_DataFrame.loc[result_DataFrame["event"] == event, "mass_1"] + result_DataFrame.loc[result_DataFrame["event"] == event, "mass_2"]
        mass_median = mass.median()
        mass_95 = mass.quantile(0.95) - mass_median
        mass_5 = mass_median - mass.quantile(0.05)

        kappa = result_DataFrame[result_DataFrame.event == event]['kappa'].values
        kappa_median = np.median(kappa)
        kappe_95 = np.quantile(kappa, 0.95) - kappa_median
        kappe_5 = kappa_median - np.quantile(kappa, 0.05)

        kernel = scipy.stats.gaussian_kde(kappa)
        kde = [kernel(kappa) for kappa in kappa]
        kde = np.array(kde)
        credible_level = len(kde[kde > kernel(0)[0]])/len(kde)

        f.write(rf"{name} & ${mass_median:.1f}^{{+{mass_95:.1f}}}_{{-{mass_5:.1f}}}$ & ${kappa_median:.3f}^{{+{kappe_95:.3f}}}_{{-{kappe_5:.3f}}}$ & ${credible_level:.3f}$")
        if event != "GW191105_143521":
            f.write(r"\\")
    f.write(r" \end{tabular}")
