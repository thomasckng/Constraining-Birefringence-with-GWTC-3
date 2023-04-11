import pandas as pd
import numpy as np
import scipy
from bilby.gw.result import CBCResult
import paths

def sign(x):
    if x > 0:
        return "+"
    elif x <= 0:
        return ""

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")

with open(paths.output/"bimodal_events_mass.txt", "w") as f:
    f.write(r"\begin{tabular}{lcccc}Event & $M$ ($M_{\odot}$) & $\chi_p$ & $\chi_{\rm eff}$ & CL\\ \hline ")
    for event in ["GW170104", "GW190413_134308", "GW190521", "GW190805_211137", "GW191105_143521"]:
        name = event.replace("_", r"\_")

        file_name = str(event)+"_GR.json.gz"
        result_DataFrame_GR = CBCResult.from_json(filename=paths.data/file_name).posterior
        mass = result_DataFrame_GR["mass_1"] + result_DataFrame_GR["mass_2"]
        mass_median = mass.median()
        mass_95 = mass.quantile(0.95) - mass_median
        mass_5 = mass_median - mass.quantile(0.05)

        chi_p_GR = result_DataFrame_GR["chi_p"]
        chi_p_GR_median  = chi_p_GR.median()
        chi_p_GR_95 = chi_p_GR.quantile(0.95) - chi_p_GR_median
        chi_p_GR_5 = chi_p_GR_median - chi_p_GR.quantile(0.05)

        chi_eff_GR = result_DataFrame[result_DataFrame.event == event]['chi_eff']
        chi_eff_GR_median  = chi_eff_GR.median()
        chi_eff_GR_95 = chi_eff_GR.quantile(0.95) - chi_eff_GR_median
        chi_eff_GR_5 = chi_eff_GR_median - chi_eff_GR.quantile(0.05)

        kappa = result_DataFrame[result_DataFrame.event == event]['kappa'].values

        kernel = scipy.stats.gaussian_kde(kappa)
        kde = np.array([kernel(kappa) for kappa in kappa])
        credible_level = len(kde[kde > kernel(0)[0]])/len(kde)

        f.write(rf"{name} & ${mass_median:.1f}^{{+{mass_95:.1f}}}_{{-{mass_5:.1f}}}$ & ${chi_p_GR_median:.2f}^{{+{chi_p_GR_95:.2f}}}_{{-{chi_p_GR_5:.2f}}}$ & ${sign(chi_eff_GR_median)}{chi_eff_GR_median:.2f}^{{+{chi_eff_GR_95:.2f}}}_{{-{chi_eff_GR_5:.2f}}}$ & ${credible_level:.3f}$")
        if event != "GW191105_143521":
            f.write(r"\\")
    f.write(r" \end{tabular}")
