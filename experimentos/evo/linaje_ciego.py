"""JUACO-EVO — LINAJE CIEGO (control de P1): evoluciona desde el padre original con muta_ciega v1, hasta G generaciones o
hasta R >= 0.8 en el padre. Cada generacion: 4 candidatos ciegos, seleccion con la regla del preregistro (selecciona.py),
carpeta gen{g}c/. Escribe linaje_ciego.log desde el arranque (regla 10).

Uso:  python linaje_ciego.py <padre.py> <padre_train.json> <padre_heldout.json> [G=6]
"""
import sys, os, json, time, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def log(f, msg):
    l = f"[{time.strftime('%H:%M:%S')}] {msg}"; print(l, flush=True); f.write(l + "\n"); f.flush(); os.fsync(f.fileno())


if __name__ == '__main__':
    padre, pt, ph = [os.path.abspath(a) for a in sys.argv[1:4]]
    G = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    f = open(os.path.join(AQUI, 'linaje_ciego.log'), 'a', encoding='utf-8')
    log(f, f"ARRANQUE linaje ciego: padre {os.path.basename(padre)}, G={G}, operador muta_ciega v1")
    for g in range(1, G + 1):
        carpeta = os.path.join(AQUI, f'gen{g}c'); os.makedirs(carpeta, exist_ok=True)
        for k in range(1, 5):
            out = subprocess.run([PY, os.path.join(AQUI, 'muta_ciega.py'), padre, os.path.join(carpeta, f'ciega_{k}'), str(g), str(k)],
                                 capture_output=True, text=True, encoding='utf-8'); log(f, out.stdout.strip() or out.stderr.strip()[-200:])
        out = subprocess.run([PY, os.path.join(AQUI, 'selecciona.py'), f'{g}c', padre, pt, ph], capture_output=True, text=True, encoding='utf-8')
        for l in out.stdout.strip().splitlines():
            log(f, "   " + l)
        if out.returncode != 0:
            log(f, f"selecciona fallo: {out.stderr[-400:]}"); break
        punt = json.load(open(os.path.join(carpeta, 'puntuaciones.json'), encoding='utf-8'))
        Rp = punt['R_padre']
        if punt['ganador']:
            padre = os.path.join(carpeta, punt['ganador'], 'organismo.py')
            pt = os.path.join(carpeta, punt['ganador'], 'train.json'); ph = os.path.join(carpeta, punt['ganador'], 'heldout.json')
            Rn = json.load(open(pt, encoding='utf-8'))['R']
            log(f, f"gen{g}c: nuevo padre {punt['ganador']} R={Rn}")
            if Rn >= 0.8:
                log(f, f"linaje ciego alcanzo R>=0.8 en la generacion {g}"); break
        else:
            log(f, f"gen{g}c: sin ganador, el padre sigue (R={Rp})")
    log(f, "FIN linaje ciego")
