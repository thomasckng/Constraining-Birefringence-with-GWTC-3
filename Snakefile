rule compute_Gaussian_result:
    input:
        "src/data/samples_Gaussian_without_GW200129.npz"
    output:
        "src/tex/output/mu_median.txt",
        "src/tex/output/sigma_median.txt"
    script:
        "src/scripts/Gaussian_result.py"

rule compute_kappa_constraint:
    input:
        "src/data/samples_Gaussian_without_GW200129.npz",
        "src/data/samples_posterior_birefringence.feather"
    output:
        "src/tex/output/restricted_kappa_median.txt",
        "src/tex/output/generic_kappa_median.txt"
    script:
        "src/scripts/kappa_constraint.py"

rule compute_best_events:
    input:
        "src/data/samples_posterior_birefringence.feather"
    output:
        "src/tex/output/best_events.txt",
    script:
        "src/scripts/best_events.py"

rule compute_GW170818_constraint:
    input:
        "src/data/samples_posterior_birefringence.feather"
    output:
        "src/tex/output/GW170818_constraint.txt",
    script:
        "src/scripts/GW170818_constraint.py"

rule compute_bimodal_events_mass:
    input:
        "src/data/samples_posterior_birefringence.feather"
    output:
        "src/tex/output/bimodal_events_mass.txt",
    script:
        "src/scripts/bimodal_events_mass.py"
        