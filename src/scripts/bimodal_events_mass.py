import pandas as pd
import paths

result_DataFrame = pd.read_feather(paths.data/"samples_posterior_birefringence.feather")

with open(paths.output/"bimodal_events_mass.txt", "w") as f:
    f.write(r"\begin{tabular}{lr}Event & Total Mass ($M_{\odot}$)\\ \hline ")
    for event in ["GW170104", "GW190413_134308", "GW190521", "GW190805_211137", "GW191105_143521"]:
        name = event.replace("_", r"\_")
        f.write(rf"{name} & ${(result_DataFrame[result_DataFrame.event == event]['mass_1'].median() + result_DataFrame[result_DataFrame.event == event]['mass_2'].median()):.1f}$")
        if event != "GW191105_143521":
            f.write(r"\\")
    f.write(r" \end{tabular}")
