import numpy as np
import paths

h = 4.135667696e-15 # eV s
c = 299792.458 # km/s
H_0 = 68.3 # km/s/Mpc

M_PV_lower_limit = 1e-22*1e9 # eV

kappa_Wang = (h*np.pi*H_0/c)*(1e3)*(100)*np.reciprocal(M_PV_lower_limit)

with open(paths.output/"kappa_Wang.txt", "w") as f:
    f.write(f"${kappa_Wang:.2f}$")
