"""lanza.py — EXPLORATORIO. Cola de corridas: UN proceso por corrida, a lo sumo MAX a la vez (6), sin Pool. Salta las que ya tienen JSON.
    python lanza.py --brazos v143,sac2,... --desde 33001 --n 5 [--T 100000] [--max 6]"""
import argparse, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__)); DATOS = os.path.join(AQUI, 'datos')
ap = argparse.ArgumentParser(); ap.add_argument('--brazos', required=True); ap.add_argument('--desde', type=int, default=33001)
ap.add_argument('--n', type=int, default=5); ap.add_argument('--T', type=int, default=100000); ap.add_argument('--max', type=int, default=6)
a = ap.parse_args()
cola = [(b, s) for s in range(a.desde, a.desde + a.n) for b in a.brazos.split(',') if b]
cola = [(b, s) for b, s in cola if not os.path.exists(os.path.join(DATOS, f"{b}_s{s}_T{a.T}.json"))]
vivos = []; t0 = time.time(); log = open(os.path.join(AQUI, 'lanza.log'), 'a', encoding='utf-8')
def w(s): print(s, flush=True); log.write(s + '\n'); log.flush()
w(f"LANZA {time.strftime('%H:%M:%S')} · {len(cola)} corridas · max {a.max} · T {a.T}")
while cola or vivos:
    vivos = [(p, b, s) for p, b, s in vivos if p.poll() is None]
    while cola and len(vivos) < a.max:
        b, s = cola.pop(0)
        p = subprocess.Popen([sys.executable, os.path.join(AQUI, 'corre_trasp.py'), '--brazo', b, '--semilla', str(s), '--T', str(a.T)],
                             stdout=open(os.path.join(DATOS, f"{b}_s{s}_T{a.T}.out"), 'w'), stderr=subprocess.STDOUT)
        vivos.append((p, b, s)); w(f"  [{time.time()-t0:6.0f}s] lanzo {b} s{s} (vivos {len(vivos)}, en cola {len(cola)})")
    time.sleep(5)
w(f"FIN {time.strftime('%H:%M:%S')} en {time.time()-t0:.0f}s")
