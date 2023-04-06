rule compute_Gaussian_result:
    input:
        "src/data/samples_Gaussian.npz"
    output:
        "src/tex/output/mu_median.txt",
        "src/tex/output/sigma_median.txt"
    script:
        "src/scripts/Gaussian_result.py"

rule compute_kappa_constraint:
    input:
        "src/data/samples_Gaussian.npz",
        "src/data/samples_posterior_birefringence.feather"
    output:
        "src/tex/output/restricted_kappa_median.txt",
        "src/tex/output/generic_kappa_median.txt",
        "src/tex/output/CL_kappa_0.txt",
        "src/tex/output/restricted_kappa_std.txt",
        "src/tex/output/restricted_absolute_kappa_90.txt"
    script:
        "src/scripts/kappa_constraint.py"

rule compute_best_events_kappa:
    input:
        "src/data/samples_posterior_birefringence.feather"
    output:
        "src/tex/output/best_events_kappa.txt"
    script:
        "src/scripts/best_events_kappa.py"

rule compute_GW170818_constraint:
    input:
        "src/data/samples_posterior_birefringence.feather"
    output:
        "src/tex/output/GW170818_constraint.txt"
    script:
        "src/scripts/GW170818_constraint.py"

rule compute_GW200129_constraint:
    input:
        "src/data/samples_posterior_birefringence.feather"
    output:
        "src/tex/output/GW200129_constraint.txt"
    script:
        "src/scripts/GW200129_constraint.py"

rule compute_bimodal_events_mass:
    input:
        "src/data/samples_posterior_birefringence.feather",
        "src/data/GW170104_GR.json.gz",
        "src/data/GW190413_134308_GR.json.gz",
        "src/data/GW190521_GR.json.gz",
        "src/data/GW190805_211137_GR.json.gz",
        "src/data/GW191105_143521_GR.json.gz"
    output:
        "src/tex/output/bimodal_events_mass.txt"
    script:
        "src/scripts/bimodal_events_mass.py"
