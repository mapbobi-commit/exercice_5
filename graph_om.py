import numpy as np
import matplotlib.pyplot as plt
from glob import glob
import os

pattern = "/home/boriskiriakov/EPFL/BA4/Physique_Numerique/Exercise5_2026/Scan_om_wave_tfin_2e+02_L_20_output_trivial_sortie/wave_tfin_2e+02_L_20_output_trivial_sortie_om_*_en"
pattern='/home/boriskiriakov/EPFL/BA4/Physique_Numerique/Exercise5_2026/Scan_om_wave_tfin_2e+02_L_20_output_trivial_sortie/wave_tfin_2e+02_L_20_output_trivial_sortie_om_*_en'

files_en = sorted(glob(pattern))

omegas = []
Emax = []

for file_en in files_en:
    name = os.path.basename(file_en)
    om = float(name.split("_om_")[-1].split("_")[0])

    data = np.loadtxt(file_en)
    E = data[:, 1]

    omegas.append(om)
    Emax.append(np.max(E))

omegas = np.array(omegas)
Emax = np.array(Emax)

idx = np.argsort(omegas)
omegas = omegas[idx]
Emax = Emax[idx]

plt.figure(figsize=(7, 5))
plt.plot(omegas, Emax, marker="o", linestyle="-", alpha=0.7)
plt.xlabel(r"$\omega$")
plt.ylabel(r"$E_{\max}$")
plt.title(r"Maximum energy as a function of $\omega$")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("Emax_vs_omega1.png", dpi=300)
plt.show()