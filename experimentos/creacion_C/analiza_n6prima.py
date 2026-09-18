"""C-P6 — calcula N6' y G-e EXACTAMENTE como los declara PREREGISTRO_n2pred.md (ERR-31: el registro sigue al
preregistro, no al revés), más la lectura honesta del SOLO_R alto. No corre nada: lee los JSON de `datos/`.

    python experimentos/creacion_C/analiza_n6prima.py [patron...]      (por defecto n2pred_s*.json)

N6' (PRINCIPAL, tal como está escrito): el acierto de PRED mudo en Q4 contra el de N0 **al MISMO número acumulado de
mordidas propias**, leído por interpolación lineal sobre `curva_rec` (t, exposiciones, mordidas, acierto).
Criterio: diferencia >= +0.10 en mediana y pareado >= 14/20.
G-e: mediana de `mord` (mordidas propias del receptor) de PRED <= 1.5 x la de N0.

AVISO DE INSTRUMENTO (mío): `corre_n2pred.py` (c92d4792aa3c496f) NO devuelve `curva_rec` en su `tarea()`, así que los
JSON de la serie 121-140 (y los de la réplica lanzada con ese mismo script) **no llevan la curva** y N6' no se puede
calcular con ellos. Este script lo dice y NO lo sustituye por otra cosa llamándola igual: calcula lo que sí se puede
(G-e y las mordidas hasta criterio) y lo etiqueta como SUCEDÁNEO, no como N6'.
"""
import sys, os, json, glob
import numpy as np

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
INF = float('inf')


def cens(x):
    """Cláusula de censura del preregistro: 'no alcanza el criterio' es PEOR que cualquier finito, nunca se salta."""
    return INF if x is None else float(x)


def med(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


def med_c(xs):
    """Mediana con censura: si más de la mitad está censurada, la mediana es 'censurada'."""
    v = sorted(cens(x) for x in xs)
    return None if not v else (None if v[len(v) // 2] == INF else float(np.median(v)))


def acc_a_mordidas(curva, m):
    """Acierto de una curva [(t, expo, mord, acc), ...] al número acumulado de mordidas `m`, por interpolación lineal."""
    if not curva:
        return None
    xs = [c[2] for c in curva]; ys = [c[3] for c in curva]
    if m <= xs[0]:
        return ys[0]
    if m >= xs[-1]:
        return ys[-1]
    return float(np.interp(m, xs, ys))


def analiza(fn):
    d = json.load(open(fn, encoding='utf-8'))
    seeds = d['meta']['semillas']; corr = d['corridas']
    G = lambda b, mu: {r['seed']: r for r in corr if r['brazo'] == b and bool(r['mudo']) == mu}
    hab = {b: G(b, False) for b in d['meta']['brazos']}
    mud = {b: G(b, True) for b in d['meta']['brazos']}
    print(f"\n=== {os.path.basename(fn)}  semillas {seeds[0]}-{seeds[-1]} ===")

    # ---------------- G-e (calculable: `mord` sí está guardado)
    mp, mn = med([r['mord'] for r in hab['PRED'].values()]), med([r['mord'] for r in hab['N0'].values()])
    raz = mp / mn if mn else None
    ge = bool(raz is not None and raz <= 1.5)
    print(f"G-e  mordidas propias del receptor: PRED {mp} / N0 {mn} = {None if raz is None else round(raz,3)} (<=1.5)"
          f"  -> {'OK' if ge else 'SALTA: la experiencia propia NO esta igualada'}")
    for b in d['meta']['brazos']:
        print(f"       {b:>9} mord {med([r['mord'] for r in hab[b].values()])}")

    # ---------------- N6' (sólo si el JSON trae la curva)
    tiene = all('curva_rec' in r for r in corr[:5])
    if not tiene:
        print("N6'  NO CALCULABLE con este JSON: `corre_n2pred.py` no guardo `curva_rec` (error de instrumento, mio).")
        print("     No se sustituye por otra medida con el mismo nombre. Lo que sigue es un SUCEDANEO, etiquetado.")
    else:
        dif, par = [], 0
        for s in seeds:
            p, n = mud['PRED'].get(s), hab['N0'].get(s)
            if not p or not n:
                continue
            a_n = acc_a_mordidas(n['curva_rec'], p['mord'])
            if a_n is None:
                continue
            dif.append(p['acierto'] - a_n); par += (p['acierto'] - a_n) >= 0
        ok = bool(dif and med(dif) >= 0.10 and par >= 14)
        print(f"N6'  PRED mudo - N0 al MISMO nº de mordidas: mediana {round(med(dif),4)} (>=+0.10), pareado {par}/{len(seeds)} (>=14)"
              f"  -> {'OK' if ok else 'NO'}")

    # ---------------- SUCEDANEO emparejado por mordidas: mordidas hasta criterio
    print("SUCEDANEO (no es N6'): mordidas propias hasta el criterio de conducta, con la clausula de censura")
    base = hab['N0']
    for b in ('PRED', 'INNATO', 'N0', 'SOLO_R', 'SHUF', 'SACIEDAD'):
        if b not in hab:
            continue
        v = [r['mord_crit'] for r in hab[b].values()]
        ncen = sum(1 for x in v if x is None)
        mejor = sum(1 for s in seeds if s in hab[b] and s in base and cens(hab[b][s]['mord_crit']) < cens(base[s]['mord_crit']))
        print(f"       {b:>9} mediana {med_c(v)}  censuradas {ncen}/{len(v)}  mejor que N0 en {mejor}/{len(seeds)}")

    # ---------------- la lectura del SOLO_R alto
    print("LECTURA del SOLO_R alto (¿el mundo se aprende solo?):")
    for b in ('N0', 'SOLO_R', 'INNATO', 'PRED'):
        if b in hab:
            print(f"       {b:>9} acierto hablando {med([r['acierto'] for r in hab[b].values()])}"
                  f"  mudo {med([r['acierto'] for r in mud[b].values()]) if mud.get(b) else None}"
                  f"  mord {med([r['mord'] for r in hab[b].values()])}"
                  f"  mord_crit {med_c([r['mord_crit'] for r in hab[b].values()])}")
    ap = med([r['acierto'] for r in hab['PRED'].values()]); asr = med([r['acierto'] for r in hab.get('SOLO_R', {}).values()])
    print(f"       techo de la tarea: SOLO_R {asr} ; margen que le queda al canal sobre N0 ({med([r['acierto'] for r in hab['N0'].values()])}): "
          f"{None if (ap is None or asr is None) else round(ap - asr, 3)} (PRED - SOLO_R)")
    return d


if __name__ == '__main__':
    pats = sys.argv[1:] or [os.path.join(RAIZ, 'datos', 'n2pred_s*.json')]
    fns = sorted({f for p in pats for f in glob.glob(p)})
    if not fns:
        raise SystemExit(f"sin JSON que analizar: {pats}")
    print(f"N6' y G-e segun PREREGISTRO_n2pred.md — {len(fns)} archivo(s)")
    for fn in fns:
        analiza(fn)
