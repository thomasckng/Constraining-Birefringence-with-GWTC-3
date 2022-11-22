rule compute_Gaussian_stat:
    input:
        "src/data/samples_Gaussian_without_GW200129.npz"
    output:
        "src/tex/output/mu_mean.txt",
        "src/tex/output/sigma_mean.txt",
        "src/tex/output/mu_median.txt",
        "src/tex/output/sigma_median.txt"
    script:
        "src/scripts/Gaussian_stat.py"