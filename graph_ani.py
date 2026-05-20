import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -----------------------------
# Data loading
# -----------------------------
base = "/home/boriskiriakov/EPFL/BA4/Physique_Numerique/Exercise5_2026/Scan_tfin_wave_tfin_15_L_20_cb_gauche_harmonique_cb_droite_libre_output_trivial_sortie/wave_tfin_15_L_20_cb_gauche_harmonique_cb_droite_libre_output_trivial_sortie_tfin_1"
base='/home/boriskiriakov/EPFL/BA4/Physique_Numerique/Exercise5_2026/Scan_tfin_wave_tfin_15_L_20_output_trivial_sortie/wave_tfin_15_L_20_output_trivial_sortie_tfin_1'

x = np.loadtxt(base + "_x")
vel2 = np.loadtxt(base + "_v")
fdata = np.loadtxt(base + "_f")
edata = np.loadtxt(base + "_en")

t = fdata[:, 0]
f = fdata[:, 1:]

t_en = edata[:, 0]
E = edata[:, 1]

nt, nx = f.shape
assert len(x) == nx, "Mismatch: x and f dimensions do not agree"

# -----------------------------
# Static plots
# -----------------------------
plt.figure()
plt.plot(t_en, E)
plt.xlabel("t")
plt.ylabel("E(t)")
plt.title("Energy vs time")
plt.tight_layout()
plt.savefig(base + "_energy.png", dpi=300)

plt.figure()
plt.plot(x, np.sqrt(vel2))
plt.xlabel("x")
plt.ylabel("c(x)")
plt.title("Wave speed vs x")
plt.tight_layout()
plt.savefig(base + "_velocity.png", dpi=300)

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

plt.figure()
i_mid = len(x) // 2
plt.plot(t, f[:, i_mid])
plt.xlabel("t")
plt.ylabel("f(mid,t)")
plt.title("Field at middle point")
plt.tight_layout()
plt.savefig(base + "_middle.png", dpi=300)

# -----------------------------
# Animated field profile f(x,t)
# -----------------------------
fig, ax = plt.subplots()

line, = ax.plot(x, f[0], lw=2)
time_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, va="top")

ax.set_xlabel("x")
ax.set_ylabel("f(x,t)")
ax.set_title("Field evolution")
ax.set_xlim(x.min(), x.max())

fmin = np.min(f)
fmax = np.max(f)
pad = 0.05 * (fmax - fmin if fmax > fmin else 1.0)
ax.set_ylim(fmin - pad, fmax + pad)

def update(frame):
    line.set_ydata(f[frame])
    time_text.set_text(f"t = {t[frame]:.5g}")
    return line, time_text

ani = animation.FuncAnimation(
    fig,
    update,
    frames=nt,
    interval=50,
    blit=True
)

# -----------------------------
# Saving animation
# -----------------------------
mp4_file = base + "_animation.mp4"
gif_file = base + "_animation.gif"

saved_any = False

try:
    ani.save(mp4_file, writer="ffmpeg", fps=20, dpi=200)
    print(f"Saved MP4: {mp4_file}")
    saved_any = True
except Exception as e:
    print("Could not save MP4 with ffmpeg:", e)

try:
    ani.save(gif_file, writer="pillow", fps=20, dpi=120)
    print(f"Saved GIF: {gif_file}")
    saved_any = True
except Exception as e:
    print("Could not save GIF with pillow:", e)

if not saved_any:
    print("No animation writer worked. Install ffmpeg and/or pillow.")

plt.show()