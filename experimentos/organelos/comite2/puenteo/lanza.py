# EXPLORATORIO, no es dato
"""lanza.py — cola de corridas del puenteo: un proceso por corrida, MAXIMO 4 a la vez, sin Pool. Salta las que ya tienen JSON.
Uso: python lanza.py --puentes patas,boca --semillas 36001-36005 [--max 4] [--T 100000]
"""
import argparse, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, 'datos')


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--puentes', required=True); ap.add_argument('--semillas', required=True)
    ap.add_argument('--max', type=int, default=4); ap.add_argument('--T', type=int, default=100000)
    a = ap.parse_args()
    mx = min(a.max, 4)
    s0, s1 = (int(z) for z in a.semillas.split('-')); sem = list(range(s0, s1 + 1))
    tareas = [(p, s) for s in sem for p in a.puentes.split(',') if p]
    tareas = [(p, s) for p, s in tareas if not os.path.exists(os.path.join(DATOS, f"{p}_s{s}.json"))]
    log = open(os.path.join(AQUI, 'lanza.log'), 'a', encoding='utf-8')
    def w(s):
        print(s, flush=True); log.write(s + '\n'); log.flush()
    w(f"LANZA {time.strftime('%H:%M:%S')} · {len(tareas)} corridas · max {mx} procesos · T {a.T}")
    vivos = []; t0 = time.time()
    while tareas or vivos:
        while tareas and len(vivos) < mx:
            p, s = tareas.pop(0)
            pr = subprocess.Popen([sys.executable, os.path.join(AQUI, 'corre_puenteo.py'), '--puente', p, '--seed', str(s), '--T', str(a.T)],
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            vivos.append((pr, p, s, time.time()))
        time.sleep(3)
        for v in list(vivos):
            pr, p, s, ti = v
            if pr.poll() is not None:
                out = (pr.stdout.read() or '').strip().splitlines()
                w(f"  [{time.time()-t0:7.0f}s] {p} s{s} rc {pr.returncode} ({time.time()-ti:.0f}s) {out[-1] if out else ''}")
                vivos.remove(v)
    w(f"LANZA fin {time.strftime('%H:%M:%S')} · {time.time()-t0:.0f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
