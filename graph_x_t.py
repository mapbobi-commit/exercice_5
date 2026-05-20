import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Data loading
# -----------------------------
base = "/home/boriskiriakov/EPFL/BA4/Physique_Numerique/Exercise5_2026/Scan_tfin_wave_tfin_15_L_20_cb_gauche_harmonique_cb_droite_libre_output_trivial_sortie/wave_tfin_15_L_20_cb_gauche_harmonique_cb_droite_libre_output_trivial_sortie_tfin_1"
base='/home/boriskiriakov/EPFL/BA4/Physique_Numerique/Exercise5_2026/Scan_tfin_wave_tfin_15_L_20_output_trivial_sortie/wave_tfin_15_L_20_output_trivial_sortie_tfin_1'
base='/home/boriskiriakov/EPFL/BA4/Physique_Numerique/Exercise5_2026/Scan_tfin_wave_tfin_15_L_20_cb_gauche_harmonique_cb_droite_libre_output_trivial_sortie/wave_tfin_15_L_20_cb_gauche_harmonique_cb_droite_libre_output_trivial_sortie_tfin_1'

x = np.loadtxt(base + "_x")
vel2 = np.loadtxt(base + "_v")
fdata = np.loadtxt(base + "_f")
edata = np.loadtxt(base + "_en")

t = fdata[:, 0]
f = fdata[:, 1:]        # shape: (nt, nx)

t_en = edata[:, 0]
E = edata[:, 1]

# -----------------------------
# Energy
# -----------------------------
plt.figure()
plt.plot(t_en, E)
plt.xlabel("t")
plt.ylabel("E(t)")
plt.title("Energy vs time")
plt.tight_layout()
plt.savefig(base + "_energy.png", dpi=300)

# -----------------------------
# Velocity profile
# -----------------------------
plt.figure()
plt.plot(x, np.sqrt(vel2))
plt.xlabel("x")
plt.ylabel("c(x)")
plt.title("Wave speed vs x")
plt.tight_layout()
plt.savefig(base + "_velocity.png", dpi=300)

# -----------------------------
# Field snapshots
# -----------------------------
plt.figure()
plt.plot(x, f[0], label=f"t = {t[0]:.3g}")
plt.plot(x, f[len(f)//2], label=f"t = {t[len(f)//2]:.3g}")
plt.plot(x, f[-1], label=f"t = {t[-1]:.3g}")
plt.xlabel("x")
plt.ylabel("f(x,t)")
plt.title("Field snapshots")
plt.legend()
plt.tight_layout()
plt.savefig(base + "_field.png", dpi=300)

# -----------------------------
# Field at middle point vs time
# -----------------------------
plt.figure()
i = len(x) // 2
plt.plot(t, f[:, i])
plt.xlabel("t")
plt.ylabel("f(mid,t)")
plt.title("Field at middle point")
plt.tight_layout()
plt.savefig(base + "_middle.png", dpi=300)

# -----------------------------
# Color plot: x as function of time, with f(x,t) as color
# -----------------------------
plt.figure(figsize=(8, 5))
im = plt.imshow(
    f,
    aspect='auto',
    origin='lower',
    extent=[x.min(), x.max(), t.min(), t.max()],
    cmap='seismic'   # or 'viridis', 'RdBu_r', etc.
)

plt.xlabel("x")
plt.ylabel("t")
plt.title("Field f(x,t)")
cbar = plt.colorbar(im)
cbar.set_label("f(x,t)")

plt.tight_layout()
plt.savefig(base + "_xt_colormap.png", dpi=300)

plt.show()