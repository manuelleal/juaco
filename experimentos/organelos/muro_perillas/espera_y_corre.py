"""espera_y_corre.py — vigia: espera a que los python.exe de trabajo ajenos bajen del tope (regla de CPU) y entonces, en UN solo proceso,
corre (1) identidad_muro_perillas.py (arnes corregido) -> identidad_muro_perillas_salida2.txt y (2) compara_sinlimpia.py -> compara_sinlimpia_salida.txt.
    python experimentos/organelos/muro_perillas/espera_y_corre.py
"""
import os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_muro_perillas as R

t0 = time.time()
while True:
    n, tot = R.python_de_trabajo()
    print(f"[{time.strftime('%H:%M:%S')}] python de trabajo ajenos {n} (totales {tot})", flush=True)
    if 0 <= n < R.CPU_TOPE or time.time() - t0 > 2 * 3600: break
    time.sleep(60)
for script, salida in (('identidad_muro_perillas.py', 'identidad_muro_perillas_salida2.txt'), ('compara_sinlimpia.py', 'compara_sinlimpia_salida.txt')):
    print(f"[{time.strftime('%H:%M:%S')}] corre {script}", flush=True)
    with open(os.path.join(AQUI, salida), 'w', encoding='utf-8') as fh:
        subprocess.run([sys.executable, os.path.join(AQUI, script)], stdout=fh, stderr=subprocess.STDOUT, cwd=os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
    print(f"[{time.strftime('%H:%M:%S')}] listo {salida}", flush=True)
