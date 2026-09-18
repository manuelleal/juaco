"""Evalua la ENMIENDA 2 (ERR-37) de PREREGISTRO_mundo_vivo.md sobre los JSON ya corridos del mundo vivo.
NO corre el organismo: lee `datos/vivo_s*.json`. Existe porque `corre_vivo.py` se escribio ANTES de la enmienda y
evalua P4'/P7 con la letra VIEJA (ERR-31: el registro sigue la letra del preregistro, no la del runner; y regla 10:
un analisis de subconjunto lo ejecuta un script del repositorio sobre los JSON, nunca en linea).

    python experimentos/nivel11_mundo_vivo/analiza_vivo_enm2.py                 (las dos series que encuentre)
    python experimentos/nivel11_mundo_vivo/analiza_vivo_enm2.py --json a.json b.json

Lo que calcula, con la letra EXACTA de la enmienda 2 (cada umbral lleva su frase al lado, como en corre_vivo.py):
  P4''a  mediana de muertes VIVO / UNA_NEC <= 0.85 y / ESCALAR <= 0.80
  P4''b  A12 = P(muertes VIVO < muertes UNA_NEC) >= 0.75 y contra ESCALAR >= 0.80 (400 comparaciones NO pareadas)
  P4''c  q75(muertes VIVO) < q25(muertes UNA_NEC) y < q25(ESCALAR)
  P7'a   mediana de muertes por agua UNA_NEC / VIVO >= 1.6, y >= 1.5 en >= 16/20 semillas
  P7'b   q75(agua VIVO) < q25(agua UNA_NEC)
  P6'    |W[sal]| <= 0.3 en las DOS necesidades en >= 18/20 (mediana <= 0.1) y censurada 20/20
  P10    en una serie SIN semillas ALIAS: P6' en 20/20 y err_peor de VIVO = 0.00 en 20/20

Dos ambiguedades de la letra, declaradas y resueltas reportando LAS DOS lecturas (no se elige; decide el
coordinador, como en P5):
  (1) "mediana de muertes VIVO / UNA_NEC": puede ser la RAZON DE MEDIANAS (de donde salio el margen observado
      0.72 / 0.64, que el runner calculo asi) o la MEDIANA DE RAZONES por semilla. Se imprimen las dos; el
      veredicto usa la RAZON DE MEDIANAS, que es la lectura de la que salio el numero citado en la enmienda.
  (2) cuartiles: la enmienda no fija metodo. Se usa statistics.quantiles(n=4) por defecto ('exclusive'), que es el
      que produjo los 106 / 125 / 143 citados, y se imprime tambien 'inclusive'.

Subconjunto preregistrado (regla 10): las semillas ALIAS (|code(D) & code(B)| = 3) las calcula
`diagnostico_codigos.py` sin simular un paso. Se reporta SIEMPRE el conjunto completo y, al lado, el de LIMPIAS.
"""
import argparse, glob, hashlib, json, os, statistics as st, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]   # organismo/ PRIMERO (ERR-28)

import diagnostico_codigos as DC

U = {   # la LETRA de la enmienda 2, literal
    'P4a': dict(frase="mediana de muertes VIVO / UNA_NEC <= 0.85 y / ESCALAR <= 0.80", una=0.85, esc=0.80),
    'P4b': dict(frase="A12 = P(muertes VIVO < muertes UNA_NEC) >= 0.75 y contra ESCALAR >= 0.80", una=0.75, esc=0.80),
    'P4c': dict(frase="q75(muertes VIVO) < q25(muertes UNA_NEC) y < q25(ESCALAR)"),
    'P7a': dict(frase="mediana de muertes por agua UNA_NEC / VIVO >= 1.6, y >= 1.5 en >= 16/20 semillas",
                razon=1.6, por_semilla=1.5, n_min=16),
    'P7b': dict(frase="q75(agua VIVO) < q25(agua UNA_NEC)"),
    'P6p': dict(frase="|W[sal]| <= 0.3 en las dos necesidades en >= 18/20 (mediana <= 0.1) y censurada 20/20",
                w_max=0.3, n_min=18, mediana_max=0.1),
    'P10': dict(frase="serie SIN semillas ALIAS: P6' en 20/20 y err_peor de VIVO = 0.00 en 20/20"),
}


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def A12(a, b):
    """P(a < b) + 0.5 P(a = b) sobre TODOS los pares (n x m). Distribucion libre, sin parear por semilla."""
    if not a or not b:
        return None
    return round(sum((x < y) + 0.5 * (x == y) for x in a for y in b) / (len(a) * len(b)), 3)


def q(xs, k, metodo='exclusive'):
    xs = [x for x in xs if x is not None]
    if len(xs) < 4:
        return None
    return round(st.quantiles(xs, n=4, method=metodo)[k], 1)


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(st.median(xs), 3) if xs else None


def razon(x, y):
    return None if (x is None or not y) else round(x / y, 3)


def carga(p):
    d = json.load(open(p, encoding='utf-8'))
    G = {}
    for r in d['principal']:
        G.setdefault(r['brazo'], {})[r['seed']] = r
    return d['meta'], G


def serie(nombre, meta, G, solo=None):
    S = sorted(G['VIVO'])
    if solo is not None:
        S = [s for s in S if s in solo]
    v = lambda b, f: [f(G[b][s]) for s in S if s in G.get(b, {})]
    mu = lambda b: v(b, lambda r: r['deaths'])
    ag = lambda b: v(b, lambda r: r['muertes_nec'][1])
    print(f"\n{'='*112}\n{nombre}   T={meta['T']}   semillas {S[0]}-{S[-1]} (n={len(S)})"
          + ("" if solo is None else "   [SUBCONJUNTO: semillas LIMPIAS, regla 10]"))
    print(f"{'brazo':11s} {'muertes med':>12s} {'q25':>6s} {'q75':>6s} {'agua med':>9s} {'agua q25':>9s} {'agua q75':>9s}")
    for b in ('VIVO', 'UNA_NEC', 'ESCALAR', 'BARAJA_POL', 'BARAJA_CON', 'NO_INFORMA', 'V14'):
        if b not in G:
            continue
        m, a = mu(b), ag(b)
        print(f"{b:11s} {med(m):>12} {q(m,0):>6} {q(m,2):>6} {med(a):>9} {q(a,0):>9} {q(a,2):>9}")

    V, mv, mu_, me = {}, mu('VIVO'), mu('UNA_NEC'), mu('ESCALAR')
    av, au = ag('VIVO'), ag('UNA_NEC')
    print()

    u = U['P4a']
    r_una, r_esc = razon(med(mv), med(mu_)), razon(med(mv), med(me))
    pr_una = med([x / y for x, y in zip(mv, mu_) if y])
    pr_esc = med([x / y for x, y in zip(mv, me) if y])
    V['P4a'] = dict(razon_medianas_una=r_una, razon_medianas_esc=r_esc,
                    mediana_razones_una=pr_una, mediana_razones_esc=pr_esc,
                    pasa=bool(r_una is not None and r_una <= u['una'] and r_esc is not None and r_esc <= u['esc']))
    print(f"P4''a  {u['frase']}")
    print(f"       razon de MEDIANAS   UNA_NEC {r_una}  ESCALAR {r_esc}   ->  {'PASA' if V['P4a']['pasa'] else 'NO'}")
    print(f"       (lectura 2: mediana de RAZONES por semilla  {pr_una} / {pr_esc}; se reporta, no decide)")

    u = U['P4b']
    a1, a2 = A12(mv, mu_), A12(mv, me)
    V['P4b'] = dict(A12_una=a1, A12_esc=a2, n_pares=len(mv) * len(mu_),
                    pasa=bool(a1 is not None and a1 >= u['una'] and a2 is not None and a2 >= u['esc']))
    print(f"P4''b  {u['frase']}")
    print(f"       A12 contra UNA_NEC {a1}   contra ESCALAR {a2}   ({len(mv)*len(mu_)} pares)   ->  {'PASA' if V['P4b']['pasa'] else 'NO'}")

    u = U['P4c']
    q75v, q25u, q25e = q(mv, 2), q(mu_, 0), q(me, 0)
    V['P4c'] = dict(q75_vivo=q75v, q25_una=q25u, q25_esc=q25e,
                    q75_vivo_inc=q(mv, 2, 'inclusive'), q25_una_inc=q(mu_, 0, 'inclusive'),
                    q25_esc_inc=q(me, 0, 'inclusive'),
                    pasa=bool(q75v is not None and q25u is not None and q25e is not None and q75v < q25u and q75v < q25e))
    print(f"P4''c  {u['frase']}")
    print(f"       q75(VIVO) {q75v} < q25(UNA_NEC) {q25u} y < q25(ESCALAR) {q25e}   ->  {'PASA' if V['P4c']['pasa'] else 'NO'}"
          f"   (inclusive: {V['P4c']['q75_vivo_inc']} / {V['P4c']['q25_una_inc']} / {V['P4c']['q25_esc_inc']})")

    u = U['P7a']
    rm = razon(med(au), med(av))
    por = [x / y for x, y in zip(au, av) if y]
    n = sum(x >= u['por_semilla'] for x in por)
    V['P7a'] = dict(razon_medianas=rm, mediana_razones=med(por), n=n, n_total=len(por),
                    pasa=bool(rm is not None and rm >= u['razon'] and n >= u['n_min']))
    print(f"P7'a   {u['frase']}")
    print(f"       razon de MEDIANAS {rm} (medianas {med(au)} / {med(av)})   >= 1.5 en {n}/{len(por)}"
          f"   ->  {'PASA' if V['P7a']['pasa'] else 'NO'}   (mediana de razones {med(por)})")

    u = U['P7b']
    q75a, q25a = q(av, 2), q(au, 0)
    V['P7b'] = dict(q75_agua_vivo=q75a, q25_agua_una=q25a,
                    pasa=bool(q75a is not None and q25a is not None and q75a < q25a))
    print(f"P7'b   {u['frase']}")
    print(f"       q75(agua VIVO) {q75a} < q25(agua UNA_NEC) {q25a}   ->  {'PASA' if V['P7b']['pasa'] else 'NO'}")

    u = U['P6p']
    if 'NO_INFORMA' in G:
        ws = [max(abs(G['NO_INFORMA'][s]['W_nec'][k]['D']) for k in range(len(G['NO_INFORMA'][s]['W_nec'])))
              for s in S if s in G['NO_INFORMA']]
        cens = sum(G['NO_INFORMA'][s]['exp_celda']['1xD'] is None for s in S if s in G['NO_INFORMA'])
        n = sum(w <= u['w_max'] for w in ws)
        V['P6p'] = dict(n=n, n_total=len(ws), mediana=med(ws), maximo=round(max(ws), 3), censuradas=cens,
                        pasa=bool(n >= u['n_min'] and med(ws) <= u['mediana_max'] and cens == len(ws)))
        print(f"P6'    {u['frase']}")
        print(f"       |W[sal]| <= 0.3 en {n}/{len(ws)}   mediana {med(ws)}   maximo {round(max(ws),3)}"
              f"   censuradas {cens}/{len(ws)}   ->  {'PASA' if V['P6p']['pasa'] else 'NO'}")
        print(f"       (la letra VIEJA de P6 agregaba con MAX sobre {len(ws)*2} lecturas: ERR-37c)")

    alias = [s for s in S if DC.solapamientos(s)['D&B'] >= 3]
    ep = [G['VIVO'][s]['err_peor'] for s in S]
    nerr = sum(e == 0.0 for e in ep)
    V['P10'] = dict(alias=alias, n_alias=len(alias), err_peor_cero=nerr, n_total=len(ep),
                    aplica=bool(not alias),
                    pasa=bool(not alias and nerr == len(ep) and V.get('P6p', {}).get('n') == len(ep)))
    print(f"P10    {U['P10']['frase']}")
    print(f"       semillas ALIAS en la serie (diagnostico estructural): {len(alias)} {alias}")
    print(f"       err_peor de VIVO = 0.00 en {nerr}/{len(ep)}   "
          + (f"->  {'PASA' if V['P10']['pasa'] else 'NO'}" if not alias else "->  NO APLICA (la serie tiene ALIAS)"))
    if alias:
        for s in alias:
            print(f"         ALIAS s{s}: err_peor VIVO {G['VIVO'][s]['err_peor']}"
                  + (f", |W[sal]| NO_INFORMA {max(abs(G['NO_INFORMA'][s]['W_nec'][k]['D']) for k in range(len(G['NO_INFORMA'][s]['W_nec'])))}"
                     if 'NO_INFORMA' in G else ""))
    return V, S, alias


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', nargs='*', default=None)
    a = ap.parse_args()
    fs = a.json or sorted(glob.glob(os.path.join(RAIZ, 'datos', 'vivo_s*-*_*.json')))
    fs = [f for f in fs if 'humo' not in os.path.basename(f)]
    print(f"  sha analiza_vivo_enm2.py {h16(os.path.abspath(__file__))}   "
          f"diagnostico_codigos.py {h16(os.path.join(AQUI,'diagnostico_codigos.py'))}")
    print(f"  ENMIENDA 2 (ERR-37) de PREREGISTRO_mundo_vivo.md {h16(os.path.join(AQUI,'PREREGISTRO_mundo_vivo.md'))}")
    print(f"  {len(fs)} serie(s): " + ", ".join(os.path.basename(f) for f in fs))
    todo = {}
    for f in fs:
        meta, G = carga(f)
        nom = os.path.basename(f)
        V, S, alias = serie(nom, meta, G)
        todo[nom] = dict(completo=V, semillas=S, alias=alias, sha=h16(f))
        if alias:   # regla 10: el subconjunto se reporta SIEMPRE al lado del completo
            V2, S2, _ = serie(nom + "  [LIMPIAS]", meta, G, solo=[s for s in S if s not in alias])
            todo[nom]['limpias'] = V2
    print(f"\n{'='*112}\nRESUMEN por prediccion (enmienda 2; el conjunto COMPLETO manda, el subconjunto se reporta)")
    claves = ['P4a', 'P4b', 'P4c', 'P7a', 'P7b', 'P6p', 'P10']
    print(f"  {'serie':34s} " + " ".join(f"{k:>7s}" for k in claves))
    for nom, d in todo.items():
        fila = []
        for k in claves:
            x = d['completo'].get(k)
            fila.append('-' if x is None else ('SI' if x['pasa'] else ('n/a' if k == 'P10' and not x['aplica'] else 'NO')))
        print(f"  {nom[:34]:34s} " + " ".join(f"{v:>7s}" for v in fila))
        if 'limpias' in d:
            fila = ['-' if d['limpias'].get(k) is None else ('SI' if d['limpias'][k]['pasa'] else 'NO') for k in claves]
            print(f"  {'   [subconjunto LIMPIAS]':34s} " + " ".join(f"{v:>7s}" for v in fila))
    d = os.path.join(AQUI, 'analiza_vivo_enm2_salida.json')
    json.dump(todo, open(d, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    print(f"\n  -> {os.path.basename(d)}  sha256_16 = {h16(d)}")
