import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import glob
import os
folders = sorted(glob.glob("Results_tsunami_eq_A_*"))

for folder in folders:

    print("\nProcessing:", folder)

    x_file = glob.glob(os.path.join(folder, "*_x"))[0]
    f_file = glob.glob(os.path.join(folder, "*_f"))[0]
    v_file = glob.glob(os.path.join(folder, "*_v"))[0]

    x = np.loadtxt(x_file)
    data = np.loadtxt(f_file)
    v2 = np.loadtxt(v_file)

    t = data[:, 0]
    f = data[:, 1:]


nx = len(x)

t_crest = np.full(nx, np.nan)

dt = t[1] - t[0]

for j in range(nx):

    signal = f[:, j]
    

    # --------------------------------------------------------
    # 1. find rough maximum (no peaks needed)
    # --------------------------------------------------------
    p = np.argmax(signal)

    # skip if near boundaries
    if p < 2 or p > len(signal) - 3:
        continue

    # --------------------------------------------------------
    # 2. take local window around maximum
    # --------------------------------------------------------
    t_local = t[p-2:p+3]
    f_local = signal[p-2:p+3]

    # --------------------------------------------------------
    # 3. cubic interpolation for smooth peak
    # --------------------------------------------------------
    try:
        coeffs = np.polyfit(t_local, f_local, 3)
        poly = np.poly1d(coeffs)

        # derivative = 0 → maximum
        dpoly = poly.deriv()
        roots = dpoly.r

        # keep only real roots inside window
        roots = roots[np.isreal(roots)].real
        roots = roots[(roots >= t_local[0]) & (roots <= t_local[-1])]

        if len(roots) > 0:
            t_crest[j] = roots[0]
        else:
            t_crest[j] = t[p]

    except:
        t_crest[j] = t[p]


# ------------------------------------------------------------
# keep valid points only
# ------------------------------------------------------------
valid = ~np.isnan(t_crest)

x_valid = x[valid]
t_valid = t_crest[valid]

# ------------------------------------------------------------
# numerical speed
# ------------------------------------------------------------
speed_num = np.gradient(x_valid, t_valid)

# ------------------------------------------------------------
# filter unrealistic values
# ------------------------------------------------------------
mask_speed = np.abs(speed_num) <= 250

x_valid = x_valid[mask_speed]
speed_num = speed_num[mask_speed]

# theory
v_theory = np.sqrt(v2)


# ------------------------------------------------------------
# plot
# ------------------------------------------------------------
plt.figure()

plt.plot(x_valid / 1000, speed_num, label="numerical speed")
plt.plot(x/1000, v_theory, label="theory sqrt(gh)")

plt.xlabel("x (km)")
plt.ylabel("speed (m/s)")
plt.title("Interpolated crest tracking (stable version)")
plt.legend()
plt.grid()

plt.show()




n_snap = 6
idxs = np.linspace(0, len(t)-1, n_snap, dtype=int)

plt.figure(figsize=(10, 5))

for i in idxs:
     plt.plot(x/1000, f[i, :], label=f"t = {t[i]:.1f} s")

plt.title(f"Wave snapshots - {folder}")
plt.xlabel("x (km)")
plt.ylabel("f(x,t)")
plt.grid()
plt.legend()
plt.show()


A = np.max(np.abs(f[:, valid]), axis=0)
h = v2[valid] / 9.81
mask = np.r_[True, np.diff(h) < 0]
h_clean = h[mask]
A_clean = A[mask]   #to have only one A value for each h, or else the reef goes up and down and maybe rflection effects or noise add to unprecision

log_h = np.log(h_clean)
log_A = np.log(A_clean)

coeff = np.polyfit(log_h, log_A, 1)

alpha = coeff[0]
C = np.exp(coeff[1])

A_fit = C * h_clean**alpha


plt.figure()

plt.scatter(h_clean, A_clean, label="data", marker='.')
plt.plot(h_clean, A_fit, label=f"fit: A ~ h^{alpha:.3f}")

plt.xlabel("h (m)")
plt.ylabel("Amplitude")
plt.title("Amplitude vs depth (Eq A)")
plt.legend()
plt.grid()

plt.show()