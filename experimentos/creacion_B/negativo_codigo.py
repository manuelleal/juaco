"""CREADOR B — NEGATIVO DEL ALIAS DE CODIGO: el tamano real del problema, medido BARATO y sin simular un paso.

Construye KW con el rng de cada semilla EXACTAMENTE como organismo_v14.run (Wl, KW[:NK], bucle de rechazo de cond(),
que solo prohibe code(A) & code(B) != 0) y lee los codigos de Kenyon (top-K=3 de KW@P). Dos mundos, semillas 1-200:

  (1) MUNDO DEL TRONCO / MUNDO VIVO: los cuatro patrones PAT (A comida, B veneno, C agua, D sal), CON cond().
      Tasa por par de colision TOTAL (|code(X) & code(Y)| = 3: el mismo codigo) y PARCIAL (= 2, y = 1).
  (2) MUNDO DE REGLA (bateria_generaliza): los 20 patrones de peso 3, SIN cond() (organismo_v14g no corre el bucle
      con mundo='regla'). Tasa por par y, con la particion px0 de split_regla, cuantos patrones de TEST comparten
      codigo exacto con alguno de TRAIN (y de que valencia): ahi el alias inflaria o hundiria G1 por la razon equivocada.

La copia de codigos() se VERIFICA contra diagnostico_codigos.codigos() (nivel11), que a su vez avisa si el sha del
tronco cambia. Nada se simula; cuesta milisegundos por semilla.

    python experimentos/creacion_B/negativo_codigo.py [--desde 1] [--n 200] [--json]
"""
import argparse, hashlib, itertools, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
NIV11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI, NIV11]   # organismo/ PRIMERO (ERR-28)

import organismo_v14 as V14
import organismo_v14g as V14G
import diagnostico_codigos as DC

SHA_V14_ESPERADO = 'feefc88b1fd8d434'
PARES4 = [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('B', 'D'), ('C', 'D')]


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def kw_y_code(seed, con_cond):
    """Las cinco lineas del arranque de organismo_v14.run. con_cond=False reproduce organismo_v14g con mundo='regla'
    (el bucle `while mundo=='AB' and not cond()` no corre)."""
    NK, NKMAX, K, PAT = V14.NK, V14.NKMAX, V14.K, V14.PAT
    rng = np.random.default_rng(seed)
    rng.uniform(.1, .4, (2, 9))                                  # Wl: consume el rng igual que el tronco
    KW = np.zeros((NKMAX, 6)); activa = np.zeros(NKMAX, bool)
    KW[:NK] = rng.uniform(0, 1, (NK, 6)); activa[:NK] = True

    def code(P):
        v = KW @ P; v = np.where(activa, v, -1e9); return set(np.argsort(v)[-K:])

    if con_cond:
        while len(code(PAT['A']) & code(PAT['B'])) != 0:
            KW[0:NK] = rng.uniform(0, 1, (NK, 6))
    return code


def negativo_tronco(seeds):
    filas = {}
    for s in seeds:
        code = kw_y_code(s, True)
        c = {k: code(V14.PAT[k]) for k in 'ABCD'}
        if s <= seeds[0] + 9:   # verificacion de la copia contra el diagnostico del nivel 11 (10 semillas bastan: mismo rng, mismo bucle)
            assert c == DC.codigos(s), f'la copia de codigos() difiere de diagnostico_codigos en la semilla {s}'
        filas[s] = {f'{a}{b}': len(c[a] & c[b]) for a, b in PARES4}
    return filas


def negativo_regla(seeds):
    pats = V14G.patrones_regla(); nombres = sorted(pats)
    filas = {}
    for s in seeds:
        code = kw_y_code(s, False)
        c = {k: code(pats[k]) for k in nombres}
        pares = {}
        for a, b in itertools.combinations(nombres, 2):
            pares[f'{a}&{b}'] = len(c[a] & c[b])
        _, tren, test, vr = V14G.split_regla(s, 'px0')
        fuga = []   # patrones de TEST con el MISMO codigo que alguno de TRAIN, y si la valencia coincide
        for k in test:
            for j in tren:
                if c[k] == c[j]:
                    fuga.append((k, j, vr[k] == vr[j]))
        filas[s] = dict(pares=pares, fuga_test_train=fuga)
    return filas


def resumen4(filas):
    n = len(filas)
    out = {}
    for a, b in PARES4:
        v = [f[f'{a}{b}'] for f in filas.values()]
        out[f'{a}{b}'] = dict(px_compartidos=int((V14.PAT[a] * V14.PAT[b]).sum()),
                              total_3=sum(x == 3 for x in v), parcial_2=sum(x == 2 for x in v),
                              uno_1=sum(x == 1 for x in v), cero=sum(x == 0 for x in v))
    alg3 = sum(any(f[p] == 3 for p in f) for f in filas.values())
    alg2 = sum(any(f[p] >= 2 for p in f) for f in filas.values())
    return dict(n=n, pares=out, semillas_con_alguna_total=alg3, semillas_con_alguna_parcial_o_total=alg2,
                alias_DB=[s for s, f in filas.items() if f['BD'] == 3],
                alias_cualquier_par=[s for s, f in filas.items() if any(f[p] == 3 for p in f)])


def resumen20(filas):
    n = len(filas); np_ = 190
    t3 = [sum(x == 3 for x in f['pares'].values()) for f in filas.values()]
    t2 = [sum(x == 2 for x in f['pares'].values()) for f in filas.values()]
    fu = [len(f['fuga_test_train']) for f in filas.values()]
    fu_mismo = [sum(z for _, _, z in f['fuga_test_train']) for f in filas.values()]
    return dict(n=n, pares_por_semilla=np_,
                tasa_par_total_3=round(float(np.mean(t3)) / np_, 4), tasa_par_parcial_2=round(float(np.mean(t2)) / np_, 4),
                pares_totales_por_semilla=dict(mediana=float(np.median(t3)), min=int(min(t3)), max=int(max(t3))),
                pares_parciales_por_semilla=dict(mediana=float(np.median(t2)), min=int(min(t2)), max=int(max(t2))),
                semillas_con_alguna_total=int(sum(x > 0 for x in t3)),
                fuga_px0=dict(semillas_con_fuga=int(sum(x > 0 for x in fu)), mediana=float(np.median(fu)),
                              max=int(max(fu)), de_ellas_misma_valencia=int(sum(fu_mismo)), total=int(sum(fu))))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--desde', type=int, default=1)
    ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--json', action='store_true')
    a = ap.parse_args()
    t0 = time.time()
    s14 = h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'))
    print(f"  sha organismo_v14 {s14}" + ("" if s14 == SHA_V14_ESPERADO else f"  *** CAMBIO respecto de {SHA_V14_ESPERADO}"))
    seeds = list(range(a.desde, a.desde + a.n))
    print(f"  NEGATIVO ESTRUCTURAL, sin simular. Semillas {seeds[0]}-{seeds[-1]} ({len(seeds)})\n")

    f4 = negativo_tronco(seeds); r4 = resumen4(f4)
    print("  (1) MUNDO DEL TRONCO / VIVO: 4 patrones, con cond() [code(A)&code(B)=0 impuesto]")
    print("      par  px_comp  total(3/3)  parcial(2/3)  uno(1/3)  cero")
    for p, o in r4['pares'].items():
        print(f"      {p}     {o['px_compartidos']}      {o['total_3']:3d} ({100*o['total_3']/r4['n']:4.1f}%)   "
              f"{o['parcial_2']:3d} ({100*o['parcial_2']/r4['n']:4.1f}%)   {o['uno_1']:3d}      {o['cero']:3d}")
    print(f"      semillas con ALGUN par con el MISMO codigo: {r4['semillas_con_alguna_total']}/{r4['n']} "
          f"({100*r4['semillas_con_alguna_total']/r4['n']:.1f}%); con alguno >= 2/3: {r4['semillas_con_alguna_parcial_o_total']}/{r4['n']}")
    print(f"      ALIAS sal==veneno (BD=3): {r4['alias_DB']}")
    print(f"      alias en cualquier par:   {r4['alias_cualquier_par']}")

    f20 = negativo_regla(seeds); r20 = resumen20(f20)
    print("\n  (2) MUNDO DE REGLA: 20 patrones de peso 3, sin cond() (190 pares por semilla)")
    print(f"      tasa por par: total {r20['tasa_par_total_3']*100:.2f}%   parcial {r20['tasa_par_parcial_2']*100:.2f}%")
    print(f"      pares con el mismo codigo por semilla: mediana {r20['pares_totales_por_semilla']['mediana']} "
          f"[{r20['pares_totales_por_semilla']['min']}, {r20['pares_totales_por_semilla']['max']}]; "
          f"semillas con alguno: {r20['semillas_con_alguna_total']}/{r20['n']}")
    print(f"      pares 2/3 por semilla: mediana {r20['pares_parciales_por_semilla']['mediana']} "
          f"[{r20['pares_parciales_por_semilla']['min']}, {r20['pares_parciales_por_semilla']['max']}]")
    fp = r20['fuga_px0']
    print(f"      FUGA px0 (test con el codigo exacto de un train): semillas {fp['semillas_con_fuga']}/{r20['n']}, "
          f"mediana {fp['mediana']} por semilla, max {fp['max']}; de {fp['total']} fugas, misma valencia {fp['de_ellas_misma_valencia']}")
    print(f"\n  ({time.time()-t0:.1f}s)")
    if a.json:
        d = os.path.join(AQUI, f'negativo_codigo_s{seeds[0]}-{seeds[-1]}.json')
        json.dump(dict(sha_organismo_v14=s14, semillas=[seeds[0], seeds[-1]], tronco4=r4, regla20=r20,
                       detalle_tronco4={str(k): v for k, v in f4.items()},
                       detalle_regla20={str(k): dict(pares_3=[p for p, x in v['pares'].items() if x == 3],
                                                     pares_2=[p for p, x in v['pares'].items() if x == 2],
                                                     fuga=v['fuga_test_train']) for k, v in f20.items()}),
                  open(d, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        print(f"  -> {os.path.basename(d)}  sha256_16 = {h16(d)}")
