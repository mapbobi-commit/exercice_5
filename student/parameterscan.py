import numpy as np
import subprocess
import os

repertoire     = '/home/boriskiriakov/EPFL/BA4/Physique_Numerique/Exercise5_2026/'
executable     = 'engine.exe'
input_filename = 'trivial.in'

input_parameters = {
    'tfin'           : 15.0,
    'L'              : 20.0,
    'nx'             : 100,
    'CFL'            : 1.0,
    'v_uniform'      : 'true',
    'h00'            : 3.669724489795918,
    'hL'             : 8000.0,
    'hR'             : 20.0,
    'xa'             : 200.0e3,
    'xb'             : 370.0e3,
    'xc'             : 430.0e3,
    'xd'             : 600.0e3,
    'equation_type'  : 'A',
    'cb_gauche'      : 'harmonique',
    'A'              : 1.0,
    'om'             : 5.0,
    'cb_droite'      : 'fixe',
    'impose_nsteps'  : 'false',
    'nsteps'         : 100,
    'output'         : 'trivial_sortie',
    'n_stride'       : 1,
    'ecrire_f'       : 'true',
}

paramstr = 'tfin'

outstr = (f"wave_tfin_{input_parameters['tfin']:.2g}"
          f"_L_{input_parameters['L']:.2g}"
          f"_cb_gauche_{input_parameters['cb_gauche']}"
          f"_cb_droite_{input_parameters['cb_droite']}"
          f"_output_{input_parameters['output']}")

outdir = f"Scan_{paramstr}_{outstr}"
os.makedirs(outdir, exist_ok=True)
print("Saving results in:", outdir)

val = 1
params = input_parameters.copy()

output_file = f"{outstr}_{paramstr}_{val}"
output_path = os.path.join(outdir, output_file)
params["output"] = output_path

exe_path = os.path.join(repertoire, executable)
cmd = [exe_path, input_filename] + [f"{k}={v}" for k, v in params.items()]

print("Command:", " ".join(cmd))
subprocess.run(cmd, check=True)
print("Done.")