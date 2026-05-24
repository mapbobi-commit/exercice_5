import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
import glob
import os
folders = sorted(glob.glob("Results_tsunami_eq_B_*"))

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

# =========================
# 1. CREST DETECTION
# =========================
for j in range(nx):

    signal = f[:, j]

    # skip completely dead signals
    if np.max(np.abs(signal)) < 1e-8:
        continue

    # safe smoothing window
    window = min(11, len(signal))
    if window % 2 == 0:
        window -= 1

    if window >= 5:
        smooth_signal = savgol_filter(signal, window_length=window, polyorder=2)
    else:
        smooth_signal = signal

    # robust crest detection (more stable than find_peaks here)
    p = np.argmax(smooth_signal)

    t_crest[j] = t[p]

# =========================
# 2. VALID DATA CLEANING
# =========================
valid = ~np.isnan(t_crest)

x_valid = x[valid]
t_valid = t_crest[valid]

print(f"Valid crest points: {len(x_valid)}")

# safety check (prevents your crash)
if len(x_valid) < 3:
    raise ValueError(
        "Too few crest points detected. "
        "Check signal amplitude or smoothing settings."
    )

# =========================
# 3. SMOOTH ARRIVAL TIMES
# =========================
if len(t_valid) >= 11:
    t_valid_smooth = savgol_filter(t_valid, window_length=11, polyorder=2)
else:
    t_valid_smooth = t_valid

# =========================
# 4. VELOCITY ESTIMATION
# =========================
v_simple = np.gradient(x_valid, t_valid_smooth)

# optional smoothing of velocity (very helpful)
if len(v_simple) >= 11:
    v_simple = savgol_filter(v_simple, window_length=11, polyorder=2)

# =========================
# 5. THEORY CURVE
# =========================
v_theory = np.sqrt(v2[valid])

# =========================
# 6. PLOT
# =========================
plt.figure()

plt.scatter(x_valid / 1000, v_simple, s=10, label="numerical (smoothed)")
plt.plot(x_valid / 1000, v_theory, linewidth=2, label="theory √(gh)")

plt.xlabel("x (km)")
plt.ylabel("speed (m/s)")
plt.title("Stable crest-tracking (Eq B)")
plt.legend()
plt.grid()

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