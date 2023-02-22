import pandas as pd
import paths

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")

with open(paths.output/"bimodal_events_mass.txt", "w") as f:
    f.write(r"\begin{tabular}{lr}Event & Total Mass ($M_{\odot}$)\\ \hline ")
    for event in ["GW170104", "GW190413_134308", "GW190521", "GW190805_211137", "GW191105_143521"]:
        name = event.replace("_", r"\_")
        # add mass_1 and mass_2 for each sample
        mass = result_DataFrame.loc[result_DataFrame["event"] == event, "mass_1"] + result_DataFrame.loc[result_DataFrame["event"] == event, "mass_2"]
        mass_median = mass.median()
        mass_95 = mass.quantile(0.95) - mass_median
        mass_5 = mass_median - mass.quantile(0.05)
        f.write(rf"{name} & ${mass_median:.1f}^{{+{mass_95:.1f}}}_{{-{mass_5:.1f}}}$")
        if event != "GW191105_143521":
            f.write(r"\\")
    f.write(r" \end{tabular}")
