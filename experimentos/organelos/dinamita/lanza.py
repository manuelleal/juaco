"""lanza.py — cola EXPLORATORIA con subprocess (sin Pool): hasta --max procesos de UNA corrida cada uno (explora_dinamita.py). Salta los JSON
que ya existen. Log en lanza.log. MISION: llegar a la AGI por este camino.

    python experimentos/organelos/dinamita/lanza.py --brazos termo,o1,vu --desde 39201 --n 10 [--max 6]
"""
import argparse, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--brazos', required=True); ap.add_argument('--desde', type=int, required=True); ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--max', type=int, default=6)
    a = ap.parse_args()
    if a.max > 6: raise SystemExit("maximo 6 procesos")
    brazos = a.brazos.split(',')
    tareas = [(s, b) for s in range(a.desde, a.desde + a.n) for b in brazos
              if not os.path.exists(os.path.join(AQUI, 'datos', 'explora', f"{b}_s{s}_T100000.json"))]
    log = open(os.path.join(AQUI, 'lanza.log'), 'a', encoding='utf-8')
    L = lambda s: (log.write(time.strftime('%H:%M:%S ') + s + '\n'), log.flush(), print(s, flush=True))
    L(f"cola {len(tareas)} tareas · brazos {brazos} · semillas {a.desde}-{a.desde + a.n - 1} · max {a.max}")
    vivos = []
    while tareas or vivos:
        while tareas and len(vivos) < a.max:
            s, b = tareas.pop(0)
            p = subprocess.Popen([sys.executable, os.path.join(AQUI, 'explora_dinamita.py'), '--seed', str(s), '--brazo', b],
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
            vivos.append((p, s, b, time.time()))
        time.sleep(2)
        for it in list(vivos):
            p, s, b, t0 = it
            if p.poll() is not None:
                out = (p.stdout.read() or '').strip().splitlines()
                L(f"[{time.time()-t0:5.0f}s rc {p.returncode}] " + (out[-1] if out else f"{b} s{s} sin salida"))
                vivos.remove(it)
    L("cola terminada")


if __name__ == '__main__':
    main()
