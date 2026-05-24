import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import glob
import os
folders = sorted(glob.glob("Results_tsunami_eq_C_*"))

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

        if np.max(np.abs(signal)) < 0.05: #skip empty
            continue

        peaks, _ = find_peaks(signal)

        if len(peaks) == 0:
            continue

        p = peaks[0]

        # parabolic refinement necessary for big beautiful graph
        if 0 < p < len(signal) - 1:
            y1, y2, y3 = signal[p - 1], signal[p], signal[p + 1]
            denom = y1 - 2*y2 + y3

            if denom != 0:
                shift = 0.5 * (y1 - y3) / denom
            else:
                shift = 0.0
        else:
            shift = 0.0

        t_crest[j] = t[p] + shift * dt
        #t_crest[j] = t[p]

    valid = ~np.isnan(t_crest)

    x_valid = x[valid]
    t_valid = t_crest[valid]

    for i in range(1, len(t_valid)):
        if t_valid[i] <= t_valid[i - 1]:
            t_valid[i] = np.nan

    mask = ~np.isnan(t_valid)
    x_valid = x_valid[mask]
    t_valid = t_valid[mask]

    window = 7
    speed_num = np.full(len(x_valid), np.nan)

    for i in range(window, len(x_valid) - window):

        x_local = x_valid[i-window:i+window]
        t_local = t_valid[i-window:i+window]

        if len(t_local) < 3:
            continue

        A = np.vstack([t_local, np.ones(len(t_local))]).T
        v, _ = np.linalg.lstsq(A, x_local, rcond=None)[0]

        speed_num[i] = v

    
    mask2 = ~np.isnan(speed_num)
    x_plot = x_valid[mask2] #keep only good not nan values
    v_plot = speed_num[mask2]


    v_theory = np.sqrt(v2[valid])
    v_theory = v_theory[mask][mask2]

    plt.figure()

    plt.plot(x_plot / 1000, v_plot, label="numerical speed")
    plt.plot(x_plot / 1000, v_theory, label="theory sqrt(gh)")

    plt.xlabel("x (km)")
    plt.ylabel("speed (m/s)")
    plt.title("Stable crest-tracking (Eq A)")
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