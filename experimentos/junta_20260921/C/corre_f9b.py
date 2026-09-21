"""FASE 9 BLOQUE 2 (candidato del creador C, junta del 21-sep-2026) — MINI-PRUEBA DE UN PROCESO.

MISION: llegar a la AGI por este camino. Pregunta: ¿que le falta al cuerpo nuevo con nodo por relevancia
para que un linaje MORTAL llegue a R0 >= 0.9 (H-1 / ERR-62)?

HIPOTESIS C-F9B: el nodo transmite hoy la REGLA (via lenta, lineal, generaliza) y NO los CASOS (via
rapida, Kenyon, por patron). Por eso el recien nacido sabe QUE es bueno pero decide siempre con la
lectura gruesa: la puerta de v14 nunca consulta la via rapida porque su codigo no tiene evidencia.
Si el mensaje entra por LAS DOS VIAS con la MISMA regla local de la mordida (nodo_via=1), el cuerpo nuevo
nace con la discriminacion fina de su linaje, vive mas y R0 sube.

NO ES UN CANDIDATO AL TRONCO (CRITERIO_TRONCO_v2 no aplica): mide un mecanismo en el mundo vivo.
Cadena anclada en v14.1 por la misma razon que el bloque 1 (la linea base de H-1 esta medida ahi).

ESTO ES UN HUMO: n = 2, SEMILLAS 1 y 2, YA VISTAS (son las del humo del bloque 1). No refuta ni
confirma nada y NINGUN umbral del preregistro se fija con el (regla 4). Un proceso, sin Pool, 6 corridas.

PREDICCIONES DEL HUMO, ESCRITAS ANTES DE LANZARLO (§8 del estilo del bloque 1)
  HB1  vida mediana(REL2) > vida mediana(REL) en 2/2 (acum=1).
  HB2  R0(REL2) > R0(REL) en 2/2 (acum=1); rango esperado de R0(REL2, acum=1): [0.55, 0.95].
  HB3  SIN CAUTELA GENERICA (la trampa 2): J = p1 + c1 - 1 de REL2 >= J(REL) - 0.05 en 2/2.
  HB4  INSTRUMENTO (BLOQUEA): via_msg > 0 y media(fam_nac) >= 1.5 en los 3 brazos REL2 (la puerta se abre).
  HB5  INSTRUMENTO (BLOQUEA): contabilidad H1-8 coherente y len(p1)=len(c1)=len(t_ok)=muertes en 6/6.
  HB6  ANCLA: REL acum=0 semilla 1 reproduce el humo del bloque 1 (R0 0.408, vida 598, p1 0.960, c1 1.000).
  Solo HB4, HB5 y HB6 bloquean (son el instrumento). HB1, HB2 y HB3 son la hipotesis: si fallan se
  escriben tal cual en el informe y la prediccion del creador queda REFUTADA por su propio humo.

Uso:  python experimentos/junta_20260921/C/corre_f9b.py --humo
"""
import argparse, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N09 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo')
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
sys.path[:0] = [AQUI, N09, N13, N11, os.path.join(RAIZ, 'organismo')]

import organismo_f9 as F9
import organismo_f9b as F9B
import corre_f9 as CF

DATOS = os.path.join(RAIZ, 'datos')
HUMO = os.path.join(DATOS, 'humo')
T_HUMO = 100000

BRAZOS = {
    'REL':  dict(CF.BRAZOS['REL'], nodo_via=0),   # el candidato del bloque 1 (leer solo con la via lenta)
    'REL2': dict(CF.BRAZOS['REL'], nodo_via=1),   # EL CANDIDATO DEL BLOQUE 2 (leer con las DOS vias)
}
CELDAS = [('REL', 1, 1), ('REL2', 1, 1), ('REL', 2, 1), ('REL2', 2, 1), ('REL', 1, 0), ('REL2', 1, 0)]


def jota(o):
    """Indice de DISCRIMINACION del cuerpo nuevo (Youden): rechazar lo malo + morder lo bueno - 1.
    Vale 0 para las dos politicas degeneradas (morder todo / no morder nada) y por eso NO se puede
    subir con cautela generica. Es la letra que el creador C propone para F9-4bis (ERR-91)."""
    if o['p1'] is None or o['c1'] is None:
        return None
    return round(o['p1'] + o['c1'] - 1.0, 4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true', required=True,
                    help='unica forma de correr esto: 6 corridas, un proceso, semillas 1 y 2 ya vistas')
    ap.add_argument('--T', type=int, default=T_HUMO)
    a = ap.parse_args()
    os.makedirs(HUMO, exist_ok=True)
    sel = time.strftime('%Y%m%d_%H%M%S')
    flog = os.path.join(HUMO, f'f9b_humo_{sel}.log')
    fjson = os.path.join(HUMO, f'f9b_humo_{sel}.json')
    lf = open(flog, 'w', encoding='utf-8')

    def log(s=''):
        print(s)
        lf.write(s + '\n')
        lf.flush()

    t0 = time.time()
    log(f"FASE 9 BLOQUE 2 (creador C) — HUMO · {time.strftime('%Y-%m-%d %H:%M:%S')} · T={a.T} · "
        f"semillas 1 y 2 (YA VISTAS) · 6 corridas · UN PROCESO, sin Pool")
    log(f"  organismo_f9b.py sha {CF.h16(os.path.join(AQUI, 'organismo_f9b.py'))} · "
        f"organismo_f9.py sha {CF.h16(os.path.join(N09, 'organismo_f9.py'))} (origen)")
    log(f"  runner sha {CF.h16(os.path.abspath(__file__))}")

    log('\nETAPA 1/3 — identidad DENTRO del runner (regla 14, ERR-38)')
    ide = []
    for s in (1, 2):
        A = F9.run(s, T=20000, **CF.BRAZOS['REL'])
        Bv = F9B.run(s, T=20000, **BRAZOS['REL'])
        f = [k for k in A if k not in Bv] + [k for k in A if k in Bv and CF.N(A[k]) != CF.N(Bv[k])]
        ide.append(['(1) nodo_via=0 == organismo_f9 REL', not f, f'dif {f}'])
        C = F9B.run(s, T=20000, **BRAZOS['REL2'])
        dif = [k for k in A if k in C and CF.N(A[k]) != CF.N(C[k])]
        ide.append(['(2) nodo_via=1 != 0 (si no, INERTE: ERR-38)', bool(dif),
                    f'claves que cambian {len(dif)} · via_msg {C.get("f9", {}).get("via_msg")}'])
    for e, ok, d in ide:
        log(f"  {'OK  ' if ok else 'FALLA'} {e}   {d}")
    if not all(ok for _, ok, _ in ide):
        log('\nIDENTIDAD INCOMPLETA: no se mira ningun numero.')
        json.dump(dict(identidad=ide, ok=False), open(fjson, 'w'), indent=1)
        raise SystemExit(1)

    log('\nETAPA 2/3 — 6 corridas (una a una, un proceso)')
    filas = []
    for br, s, ac in CELDAS:
        t1 = time.time()
        r = F9B.run(s, T=a.T, **dict(BRAZOS[br], rep_acum=ac))
        o = CF.resumen(br, s, ac, r, round(time.time() - t1, 2))
        f9 = r.get('f9') or {}
        fn = f9.get('fam_nac') or []
        o['J'] = jota(o)
        o['via_msg'] = f9.get('via_msg')
        o['fam_nac_med'] = round(sum(fn) / len(fn), 3) if fn else None
        o['fam_nac_max'] = max(fn) if fn else None
        o['n_cod'] = r.get('n_cod')
        filas.append(o)
        log(f"  [{time.time()-t0:7.1f}s] {br:5s} s={s} acum={ac}  R0 {o['R0']:.3f}  r {o['r']:+5d}  "
            f"vida {o['vida_med']}  p1 {o['p1']}  c1 {o['c1']}  J {o['J']}  sac {o['sac_frac']}  "
            f"expA {o['exp_A']}  via_msg {o['via_msg']}  fam {o['fam_nac_med']}  coh {o['coherente']}")

    log('\nETAPA 3/3 — LAS SEIS PREDICCIONES DEL HUMO (escritas antes de lanzarlo)')
    g = {(o['brazo'], o['seed'], o['acum']): o for o in filas}
    res = {}
    res['HB1'] = (sum(g[('REL2', s, 1)]['vida_med'] > g[('REL', s, 1)]['vida_med'] for s in (1, 2)), 2)
    res['HB2'] = (sum(g[('REL2', s, 1)]['R0'] > g[('REL', s, 1)]['R0'] for s in (1, 2)), 2)
    res['HB3'] = (sum(g[('REL2', s, 1)]['J'] >= g[('REL', s, 1)]['J'] - 0.05 for s in (1, 2)), 2)
    res['HB4'] = (sum(o['via_msg'] and o['fam_nac_med'] is not None and o['fam_nac_med'] >= 1.5
                      for o in filas if o['brazo'] == 'REL2'), 3)
    res['HB5'] = (sum(bool(o['coherente']) and bool(o['f9_len']) for o in filas), 6)
    anc = g[('REL', 1, 0)]
    res['HB6'] = (int(abs(anc['R0'] - 0.408) < 1e-9 and abs(anc['vida_med'] - 598) < 1e-9
                      and abs(anc['p1'] - 0.960) < 0.0011 and abs(anc['c1'] - 1.000) < 0.0011), 1)
    for k in ('HB1', 'HB2', 'HB3', 'HB4', 'HB5', 'HB6'):
        n, d = res[k]
        log(f"  {k}: {n}/{d}  {'SI' if n == d else 'NO'}")
    log(f"  ANCLA HB6 medida: REL acum=0 s=1 -> R0 {anc['R0']} vida {anc['vida_med']} "
        f"p1 {anc['p1']} c1 {anc['c1']} (bloque 1: 0.408 / 598 / 0.960 / 1.000)")
    log('\n  R0(acum=1): ' + ' · '.join(f"{b} s{s} {g[(b, s, 1)]['R0']:.3f}"
                                        for s in (1, 2) for b in ('REL', 'REL2')))
    log(f"  Umbral de H-1 (H1-6): R0 >= 0.90. El humo NO lo decide (n=2, semillas ya vistas).")

    json.dump(dict(bloque='fase9_bloque2_humo_C', sello=sel, T=a.T, semillas=[1, 2],
                   identidad=[[e, bool(o), d] for e, o, d in ide],
                   sha_f9b=CF.h16(os.path.join(AQUI, 'organismo_f9b.py')),
                   sha_f9=CF.h16(os.path.join(N09, 'organismo_f9.py')),
                   predicciones={k: list(v) for k, v in res.items()}, corridas=filas),
              open(fjson, 'w'), indent=1)
    log(f'\n  JSON {fjson} (sha {CF.h16(fjson)})')
    log(f'Terminado en {time.time()-t0:.1f}s')
    lf.close()


if __name__ == '__main__':
    main()
