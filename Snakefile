rule compute_Gaussian_stat:
    input:
        "src/data/samples_Gaussian_without_GW200129.npz"
    output:
        "src/tex/output/Gaussian_mean.txt",
        "src/tex/output/kappa_mean.txt"
    script:
        "src/scripts/Gaussian_stat.py"