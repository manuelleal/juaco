"""construye_siembras.py — arma siembras.json: DE DONDE ARRANCA la evolucion (paquete anfitrion, Opus B, 24-sep-2026).

MISION: llegar a la AGI por este camino. Principio del director: 'la evolucion arranca DESDE LO MAS EVOLUCIONADO que tengamos'.
  huespedes: los 200 genomas del banco de VIDA en el corte de ECO v1.1 (FABRICA, w90, juez v2 con placebo: la colonia del banco de VIDA vive
             3.2-3.3x la de AZAR), semillas 19401-19440 (serie + replica): 8000 genomas de 18 genes + los 7 organos de motor_eco3 en 0.9
             (apagados), recortados al rango del motor (se cuenta cuantos valores se recortan).
  simbiontes: los DOMESTICADOS de la serie y la replica de endosimbiosis (22001-22040, brazo VIDA_S): el vector medio g de los simbiontes de
             ADENTRO en cada muestra (cada 1000 pasos) con t >= 10 000 y al menos un portador. (Los genomas individuales transmitidos no se
             guardaron: 'don' solo tiene I; 'dentro_final' tiene 1 genoma en 40 corridas. Declarado.)
Cada fuente con su sha a 16. Uso: python experimentos/organelos/anfitrion/construye_siembras.py [--verifica]
"""
import glob, hashlib, json, os, sys
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__)); RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
for _d in (os.path.join(RAIZ, 'experimentos', 'generaciones'), os.path.join(RAIZ, 'experimentos', 'juaco_eco')):
    if _d not in sys.path: sys.path.insert(0, _d)
sys.dont_write_bytecode = True
DEST = os.path.join(AQUI, 'siembras.json')
H = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def arma():
    import motor_eco3 as M3, pista2
    G0 = M3.genoma0(pista2.cfg_fabrica()); lo, hi = M3.rangos(G0)
    fh = []; hues = []; rec = 0
    for v in ('eco_v11_serie_s19401-19420', 'eco_v11_serie_s19421-19440'):
        for f in sorted(glob.glob(os.path.join(RAIZ, 'experimentos', 'juaco_eco', 'datos', v, 'VIDA_s*.json'))):
            d = json.load(open(f, encoding='utf-8')); fh.append([os.path.relpath(f, RAIZ).replace(os.sep, '/'), H(f)])
            for g in d['corte']['banco']:
                x = np.array(list(g) + [0.9] * 7, float); y = np.clip(x, lo, hi); rec += int((y != x).sum())
                hues.append([round(float(z), 9) for z in y])
    fs = []; simb = []
    for v in ('endo_serie_s22001-22020', 'endo_replica_s22021-22040'):
        for f in sorted(glob.glob(os.path.join(RAIZ, 'experimentos', 'organelos', 'darwin', 'datos', v, 'VIDA_S_s*.json'))):
            d = json.load(open(f, encoding='utf-8')); fs.append([os.path.relpath(f, RAIZ).replace(os.sep, '/'), H(f)])
            for x in d['serie_simb']:
                if x[0] >= 10000 and x[2] >= 1 and x[7] is not None: simb.append([float(z) for z in x[7]])
    return dict(huespedes=hues, n_huespedes=len(hues), recortes_huespedes=rec, fuentes_huespedes=fh,
                simbiontes=simb, n_simbiontes=len(simb), fuentes_simbiontes=fs, genes=list(M3.NOMBRES))


if __name__ == '__main__':
    s = json.dumps(arma(), separators=(',', ':'))
    if '--verifica' in sys.argv[1:]:
        ok = os.path.exists(DEST) and open(DEST, encoding='utf-8').read() == s
        print('VERIFICA', 'OK' if ok else 'FALLA'); sys.exit(0 if ok else 1)
    open(DEST, 'w', encoding='utf-8', newline='\n').write(s)
    d = json.loads(s)
    print('siembras.json', hashlib.sha256(s.encode()).hexdigest()[:16], 'huespedes', d['n_huespedes'], 'recortes', d['recortes_huespedes'], 'simbiontes', d['n_simbiontes'])
