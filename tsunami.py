import numpy as np
import matplotlib.pyplot as plt
import glob
import os



folders = sorted(glob.glob("Results_tsunami_eq_*"))

for folder in folders:

    print("\nProcessing:", folder)

    # find files inside folder
    x_file = glob.glob(os.path.join(folder, "*_x"))[0]
    f_file = glob.glob(os.path.join(folder, "*_f"))[0]
    v_file = glob.glob(os.path.join(folder, "*_v"))[0]

    x = np.loadtxt(x_file)
    data = np.loadtxt(f_file)
    v2 = np.loadtxt(v_file)

    t = data[:,0]
    f = data[:,1:]


t_crest = np.full(len(x), np.nan)

valid = np.isfinite(t_crest)

xv = x[valid]
tv = t_crest[valid]

# IMPORTANT: sort by x
idx = np.argsort(xv)
xv = xv[idx]
tv = tv[idx]

# smooth time curve
tv_smooth = np.convolve(tv, np.ones(51)/51, mode='same')

# local derivative dt/dx first
dt_dx = np.gradient(tv_smooth, xv)

# then invert safely
speed_num = 1.0 / dt_dx


g = 9.81
c_theory = np.sqrt(v2)

plt.figure()

plt.plot(x/1000, c_theory, label="theoretical sqrt(gh)")
plt.plot(x/1000, speed_num, label="numerical crest speed (A)")

plt.xlabel("x (km)")
plt.ylabel("speed (m/s)")
plt.title("Case A: wave speed comparison")
plt.legend()
plt.grid()

plt.show()

print("speed_num valid points:", np.sum(~np.isnan(speed_num)))

print("valid t_crest:", np.sum(np.isfinite(t_crest)))