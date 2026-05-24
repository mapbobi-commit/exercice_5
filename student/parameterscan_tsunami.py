import numpy as np
import subprocess
import os

repertoire     = './student'
executable     = 'engine.exe'
input_filename = 'trivial.in'

input_parameters = {
    'tfin'          : 8700.0,
    'L'             : 800e3,
    'nx'            : 8000,
    'CFL'           : 0.5,
    'v_uniform'     : 'false',
    'h00'           : 4000.0,
    'hL'            : 8000.0,
    'hR'            : 20.0,
    'xa'            : 200e3,
    'xb'            : 370e3,
    'xc'            : 430e3,
    'xd'            : 600e3,
    'cb_gauche'     : 'harmonique',
    'A'             : 1.0,
    'om'            : 2*np.pi/900.0,
    'cb_droite'     : 'sortie',
    'impose_nsteps' : 'false',
    'nsteps'        : 100,
    'n_stride'      : 10,
    'ecrire_f'      : 'true',
}

exe_path = os.path.join(repertoire, executable)

for eq in ['A', 'B', 'C']:

    params = input_parameters.copy()
    params['equation_type'] = eq

    outstr = (
        f"tsunami"
        f"_eq_{eq}"
        f"_nx_{params['nx']}"
        f"_L_{int(params['L']/1000)}km"
        f"_bcR_{params['cb_droite']}"
    )

    outdir = f"Results_{outstr}"
    os.makedirs(outdir, exist_ok=True)

    print("Saving results in:", outdir)

    output_path = os.path.join(outdir, outstr)
    params["output"] = output_path

    cmd = [exe_path, input_filename] + [
        f"{k}={v}" for k, v in params.items()
    ]

    print("Command:", " ".join(cmd))

    subprocess.run(cmd, check=True)

print("Done.")