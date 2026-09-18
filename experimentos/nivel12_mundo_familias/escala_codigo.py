"""BLOQUE 0 (0a) — ESCALA DEL CODIGO: barrido estructural (D, NK, K) del alias en el mundo de FAMILIAS.

NO simula un solo paso del organismo (T = 0). NO usa multiprocessing.Pool. NO edita ningun archivo del repo salvo
el preregistro de esta misma carpeta (seccion 8) y su propio JSON de salida. `organismo/` primero en sys.path (ERR-28).

Reproduce la construccion del codigo del TRONCO por ANCLAS DE LECTURA (ninguna constante copiada a mano):
  - importa organismo/organismo_v14.py (sha feefc88b1fd8d434, CONGELADO: solo se lee; run() jamas se llama) -> NK, NKMAX, K
  - verifica LITERALMENTE las tres lineas del tronco que definen el codigo (estado inicial, code(P), constantes)
  - verifica LITERALMENTE contra experimentos/capacidad_grande/construye_capD.py (sha 0dbd2449f4bf0901) la sustitucion
    que generaliza la retina a D pixeles; con D = 6 el consumo del rng es el del tronco (control G0 de capD)

Umbrales, rejilla, catalogos y predicciones estan FIJADOS en PREREGISTRO_bloque0_codigo.md (secciones 3, 4 y 5),
escrito antes de ejecutar esto. Este script no los elige: los lee de las constantes de abajo, que son copia literal
de ese documento.

Uso:  python experimentos/nivel12_mundo_familias/escala_codigo.py [--semillas 200] [--solo-c32]
"""
import argparse, hashlib, itertools, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [os.path.join(RAIZ, 'organismo')]          # ERR-28: organismo/ PRIMERO
import numpy as np
import organismo_v14 as V14                                # CONGELADO: solo se lee; run() no se llama nunca

# ---------------------------------------------------------------- anclas (aborto duro si algo cambio)
SHA_V14 = 'feefc88b1fd8d434'
SHA_CAPD = '0dbd2449f4bf0901'
RUTA_V14 = os.path.join(RAIZ, 'organismo', 'organismo_v14.py')
RUTA_CAPD = os.path.join(RAIZ, 'experimentos', 'capacidad_grande', 'construye_capD.py')

ANCLA_ESTADO = ("Wl=rng.uniform(.1,.4,(2,9)); KW=np.zeros((NKMAX,6)); activa=np.zeros(NKMAX,bool); "
                "KW[:NK]=rng.uniform(0,1,(NK,6)); activa[:NK]=True")
ANCLA_CODE = "        v=KW@P; v=np.where(activa,v,-1e9); return set(np.argsort(v)[-K:])"
ANCLA_CONST = "L=40; NK=30; NKMAX=90; K=3"
ANCLA_CAPD_D = ("Wl=rng.uniform(.1,.4,(2,D+3)); KW=np.zeros((NKMAX,D)); activa=np.zeros(NKMAX,bool); "
                "KW[:NK]=rng.uniform(0,1,(NK,D)); activa[:NK]=True")


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def exige(texto, ancla, n, etiqueta):
    c = texto.count(ancla)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta}: aparece {c} veces, se esperaban {n}. ABORTADO (el preregistro queda sin datos).")


def verifica_anclas():
    """Todo lo que este script sabe del tronco lo aprende AQUI, leyendo. Nada se escribe a mano."""
    s14, scap = h16(RUTA_V14), h16(RUTA_CAPD)
    if s14 != SHA_V14:
        raise SystemExit(f"organismo_v14.py: sha {s14}, se esperaba {SHA_V14}. ABORTADO.")
    if scap != SHA_CAPD:
        raise SystemExit(f"construye_capD.py: sha {scap}, se esperaba {SHA_CAPD}. ABORTADO.")
    t14 = open(RUTA_V14, encoding='utf-8').read()
    tcap = open(RUTA_CAPD, encoding='utf-8').read()
    exige(t14, ANCLA_ESTADO, 1, 'estado inicial (KW y activa) en organismo_v14.py')
    exige(t14, ANCLA_CODE, 1, 'code(P) = top-K de KW@P en organismo_v14.py')
    exige(t14, ANCLA_CONST, 1, 'constantes L/NK/NKMAX/K en organismo_v14.py')
    exige(tcap, ANCLA_ESTADO, 1, 'lado VIEJO de la sustitucion capD (debe ser la linea del tronco)')
    exige(tcap, ANCLA_CAPD_D, 1, 'lado NUEVO de la sustitucion capD (retina D)')
    # y de aqui, no de una constante escrita a mano, salen los valores del tronco:
    return dict(sha_v14=s14, sha_capD=scap, NK_tronco=int(V14.NK), NKMAX_tronco=int(V14.NKMAX), K_tronco=int(V14.K))


# ---------------------------------------------------------------- rejilla y catalogos (PREREGISTRO secciones 3 y 4)
NKS = (30, 60, 90, 180, 360)
KS = (2, 3, 4, 5)
DS = (6, 12)
CATALOGOS = {'C32': dict(F=8, V=3), 'C16': dict(F=4, V=3)}
SEMILLA_MUNDO = 50000          # rng propio del mundo: el catalogo de una semilla es el MISMO en toda la rejilla
PESO_TOKEN = 3                 # tokens de peso 3 sobre los pixeles de forma (DISENO_mundo_grande 1.1)
U1_ALIAS_EXACTO_PCT = 1.0      # A1 < 1.0 % de las semillas
U2_PARCIAL_INTER_PCT = 1.0     # B1 <= 1.0 % de los pares inter-familia
U3_MARGEN_SIM = 0.20           # S1 - S2 >= 0.20
U3_SEMILLAS_MIN = 190          # y S1 > S2 en >= 190/200 semillas
# ancla de verificacion P2 (DISENO_mundo_grande 1.1, D=12 V=3 F=8 K=3 NK=30/60/90, semillas 1-200):
P2_ANCLA = {30: dict(alias_any=0.995, alias_tok=0.190, tokeniza=0.667, exacto=0.125, falsa=0.125),
            60: dict(alias_any=0.950, alias_tok=0.090, tokeniza=0.542, exacto=0.083, falsa=0.083),
            90: dict(alias_any=0.895, alias_tok=0.060, tokeniza=0.500, exacto=0.042, falsa=0.042)}
P2_TOL = 0.05                  # +-5 pp


def catalogo(D, F, V, seed):
    """shape = D-V pixeles de forma; F tokens de peso 3; cada variante = token + 1 pixel de variable (intensidad 1.0).
    Regla declarada en el preregistro 3.1: si D-V < 5, el arm usa V = 1 (comparador degradado; D=6 no hospeda V=3)."""
    if D - V < 5:
        V = 1
    shape = D - V
    combos = list(itertools.combinations(range(shape), PESO_TOKEN))
    if len(combos) < F:
        raise SystemExit(f"catalogo imposible: D={D} V={V} shape={shape} da {len(combos)} tokens < F={F}. ABORTADO.")
    r = np.random.default_rng(SEMILLA_MUNDO + seed)
    r.shuffle(combos)
    P = []; fam = []; es_var = []; idx_token = []
    for k in range(F):
        base = np.zeros(D); base[list(combos[k])] = 1.
        P.append(base); fam.append(k); es_var.append(False); idx_token.append(len(P) - 1)
        raiz = len(P) - 1
        for v in range(V):
            Q = base.copy(); Q[shape + v] = 1.
            P.append(Q); fam.append(k); es_var.append(True); idx_token.append(raiz)
    return np.array(P), np.array(fam), np.array(es_var), np.array(idx_token), V


def kw_del_tronco(seed, NK, D):
    """Orden de consumo del rng EXACTO del tronco, con la retina generalizada por la sustitucion de capD:
       default_rng(seed) -> uniform(.1,.4,(2,D+3))  [las patas, se descartan] -> uniform(0,1,(NK,D)).
       Sin cond(): el rechazo del tronco solo restringe A y B, que no existen en el mundo de familias (declarado
       en el preregistro 2 como cota OPTIMISTA). Todas las celdas activas (arranque de corrida, celdas UNIFORMES)."""
    rng = np.random.default_rng(seed)
    rng.uniform(.1, .4, (2, D + 3))
    return rng.uniform(0, 1, (NK, D))


def codigos(KW, P, K):
    """code(P) = top-K de KW@P (argsort, empates por indice: identico al tronco). Devuelve mascara (n_est, NK)."""
    v = KW @ P.T                                  # (NK, n_est)
    top = np.argsort(v, axis=0)[-K:, :]           # (K, n_est)
    M = np.zeros((P.shape[0], KW.shape[0]), dtype=np.int16)
    M[np.repeat(np.arange(P.shape[0]), K), top.T.ravel()] = 1
    return M


def celda(D, NK, K, F, V, semillas):
    """Una celda de la rejilla: 200 semillas. Devuelve las medidas A1/A2/B1/B2/T1/S1/S2 del preregistro seccion 4."""
    a1 = []; a2 = []; b1 = []; b2 = []; t1 = []; ex = []; fa = []; s1 = []; s2 = []; atok = []; s1s2 = []
    for seed in semillas:
        P, fam, es_var, raiz, Vef = catalogo(D, F, V, seed)
        n = P.shape[0]
        if K > NK:
            return None
        M = codigos(kw_del_tronco(seed, NK, D), P, K)
        ov = M @ M.T                                                  # (n, n) celdas compartidas
        iu = np.triu_indices(n, 1)
        o = ov[iu]; misma = (fam[iu[0]] == fam[iu[1]])
        ident = (o == K)
        a1.append(float(ident.any())); a2.append(float(ident.mean()))
        inter = ~misma
        b1.append(float((o[inter] >= K - 1).mean())); b2.append(float((o[inter] >= K - 1).any()))
        sim = o / K
        m1 = float(sim[misma].mean()); m2 = float(sim[inter].mean())
        s1.append(m1); s2.append(m2); s1s2.append(float(m1 > m2))
        # tokeniza / exacto / falsa: definicion LITERAL de diagnostico_familias_sala2.py (DISENO_mundo_grande 1.1)
        tks = np.flatnonzero(~es_var); nt = nf = ne = 0
        for i in np.flatnonzero(es_var):
            propio = int(ov[i, raiz[i]])
            otros = max(int(ov[i, t]) for t in tks if t != raiz[i])
            if propio == K: ne += 1
            if propio >= K - 1 and propio >= otros: nt += 1
            elif otros >= K - 1: nf += 1
        nv = int(es_var.sum())
        t1.append(nt / nv); ex.append(ne / nv); fa.append(nf / nv)
        atok.append(float(any(ov[a, b] == K for a, b in itertools.combinations(tks.tolist(), 2))))
    f = lambda x: round(float(np.mean(x)), 5)
    cumple_u1 = 100 * np.mean(a1) < U1_ALIAS_EXACTO_PCT
    cumple_u2 = 100 * np.mean(b1) <= U2_PARCIAL_INTER_PCT
    cumple_u3 = (np.mean(s1) - np.mean(s2) >= U3_MARGEN_SIM) and (sum(s1s2) >= U3_SEMILLAS_MIN * len(semillas) / 200)
    if cumple_u1 and cumple_u2 and cumple_u3: veredicto = 'CUMPLE'
    elif cumple_u1 and cumple_u2: veredicto = 'AFILADO'      # no confunde, pero tampoco agrupa
    elif cumple_u3: veredicto = 'BORROSO'                    # agrupa, pero confunde
    else: veredicto = 'NO'
    return dict(D=D, NK=NK, K=K, F=F, V_efectivo=int(Vef), n_estimulos=int(n), n_semillas=len(semillas),
                A1_alias_exacto_semillas_pct=round(100 * float(np.mean(a1)), 3),
                A2_alias_exacto_pares_pct=round(100 * float(np.mean(a2)), 4),
                B1_parcial_inter_pares_pct=round(100 * float(np.mean(b1)), 3),
                B2_parcial_inter_semillas_pct=round(100 * float(np.mean(b2)), 3),
                T1_tokeniza=f(t1), exacto_variante_token=f(ex), familia_falsa=f(fa),
                alias_entre_tokens_semillas=f(atok),
                S1_sim_intra=f(s1), S2_sim_inter=f(s2), S1_menos_S2=round(f(s1) - f(s2), 5),
                semillas_S1_mayor_S2=int(sum(s1s2)),
                U1=bool(cumple_u1), U2=bool(cumple_u2), U3=bool(cumple_u3), veredicto=veredicto)


POSTHOC_NKS = (720, 1440, 2880, 5760)   # FUERA de la rejilla preregistrada: solo para decir CUANTO faltaria


def posthoc(semillas):
    """POST-HOC EXPLORATORIO, declarado como tal: NO es parte del veredicto (la rejilla de 3 esta cerrada).
    Si ninguna celda preregistrada pasa U1, este bloque responde una sola pregunta cuantitativa que la
    recomendacion necesita: *cuanto* NK haria falta, con K = 4 y K = 5, para que A1 baje de 1 %."""
    filas = []
    for NK in POSTHOC_NKS:
        for K in (4, 5):
            r = celda(12, NK, K, CATALOGOS['C32']['F'], CATALOGOS['C32']['V'], semillas)
            filas.append(r)
            print(f"  POSTHOC D=12 NK={NK:5d} K={K}  A1={r['A1_alias_exacto_semillas_pct']:6.2f}%  "
                  f"S1-S2={r['S1_menos_S2']:+.3f}  {r['veredicto']}")
    return filas


def verifica_P2(filas):
    """P2: si esto falla, el instrumento esta mal y NO se publica recomendacion (preregistro seccion 5)."""
    ok = True; det = []
    for nk, esp in P2_ANCLA.items():
        r = next((x for x in filas if x['D'] == 12 and x['NK'] == nk and x['K'] == 3 and x['F'] == 8), None)
        if r is None: continue
        obs = dict(alias_any=r['A1_alias_exacto_semillas_pct'] / 100, alias_tok=r['alias_entre_tokens_semillas'],
                   tokeniza=r['T1_tokeniza'], exacto=r['exacto_variante_token'], falsa=r['familia_falsa'])
        for k, v in esp.items():
            d = abs(obs[k] - v); paso = d <= P2_TOL
            ok = ok and paso
            det.append(dict(NK=nk, medida=k, esperado=v, observado=round(obs[k], 4), delta=round(d, 4), pasa=bool(paso)))
    return ok, det


def tabla_md(filas, titulo):
    L = [f"**{titulo}**", "",
         "| D | NK | K | estim. | alias exacto % (A1) | alias exacto pares % (A2) | alias 2/3 inter % (B1) | "
         "B2 semillas % | tokeniza (T1) | sim intra (S1) | sim inter (S2) | S1−S2 | U1 | U2 | U3 | veredicto |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in filas:
        s = lambda b: '✔' if b else '·'
        L.append(f"| {r['D']} | {r['NK']} | {r['K']} | {r['n_estimulos']} | **{r['A1_alias_exacto_semillas_pct']:.1f}** | "
                 f"{r['A2_alias_exacto_pares_pct']:.3f} | **{r['B1_parcial_inter_pares_pct']:.2f}** | "
                 f"{r['B2_parcial_inter_semillas_pct']:.0f} | {r['T1_tokeniza']:.3f} | {r['S1_sim_intra']:.3f} | "
                 f"{r['S2_sim_inter']:.3f} | **{r['S1_menos_S2']:+.3f}** | {s(r['U1'])} | {s(r['U2'])} | {s(r['U3'])} | "
                 f"{r['veredicto']} |")
    return "\n".join(L)


def escribe_seccion8(texto):
    """Reescribe SOLO la seccion 8 del preregistro de esta carpeta (archivo propio, creado para este bloque)."""
    p = os.path.join(AQUI, 'PREREGISTRO_bloque0_codigo.md')
    s = open(p, encoding='utf-8').read()
    a = s.index('## 8. RESULTADOS'); b = s.index('## 9. RECOMENDACI')
    open(p, 'w', encoding='utf-8', newline='\n').write(s[:a] + '## 8. RESULTADOS\n\n' + texto + '\n\n' + s[b:])
    return p


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--semillas', type=int, default=200)
    ap.add_argument('--solo-c32', action='store_true')
    a = ap.parse_args()
    t0 = time.time()
    anclas = verifica_anclas()
    print('anclas OK:', anclas)
    semillas = list(range(1, a.semillas + 1))
    cats = ['C32'] if a.solo_c32 else list(CATALOGOS)
    out = dict(anclas=anclas, rejilla=dict(NK=list(NKS), K=list(KS), D=list(DS)), catalogos=CATALOGOS,
               semillas=[semillas[0], semillas[-1]],
               umbrales=dict(U1_alias_exacto_pct=U1_ALIAS_EXACTO_PCT, U2_parcial_inter_pct=U2_PARCIAL_INTER_PCT,
                             U3_margen_sim=U3_MARGEN_SIM, U3_semillas_min=U3_SEMILLAS_MIN),
               resultados={})
    for cat in cats:
        F, V = CATALOGOS[cat]['F'], CATALOGOS[cat]['V']
        filas = []
        for D in DS:
            for NK in NKS:
                for K in KS:
                    r = celda(D, NK, K, F, V, semillas)
                    if r is not None:
                        filas.append(r)
                        print(f"  {cat} D={D:2d} NK={NK:3d} K={K}  A1={r['A1_alias_exacto_semillas_pct']:6.1f}%  "
                              f"B1={r['B1_parcial_inter_pares_pct']:6.2f}%  S1-S2={r['S1_menos_S2']:+.3f}  {r['veredicto']}")
        out['resultados'][cat] = filas
    cumple_alguna = any(r['D'] == 12 and r['veredicto'] == 'CUMPLE' for r in out['resultados']['C32'])
    if not cumple_alguna:
        print("\nninguna celda preregistrada CUMPLE -> bloque POST-HOC (fuera de la rejilla, no es veredicto):")
        out['posthoc_fuera_de_rejilla'] = posthoc(semillas)
    okP2, detP2 = verifica_P2(out['resultados']['C32'])
    out['P2_verificacion_instrumento'] = dict(pasa=bool(okP2), detalle=detP2)
    print(f"\nP2 (ancla de instrumento contra DISENO_mundo_grande 1.1): {'PASA' if okP2 else 'FALLA'}")
    for d in detP2:
        if not d['pasa']: print('   FALLA:', d)
    # recomendacion: minimo NK, luego minimo K, solo sobre D=12 y C32 (preregistro seccion 4, regla de minimo)
    cand = [r for r in out['resultados']['C32'] if r['D'] == 12 and r['veredicto'] == 'CUMPLE']
    cand.sort(key=lambda r: (r['NK'], r['K']))
    out['recomendacion'] = (dict(cumple=True, NK=cand[0]['NK'], K=cand[0]['K'], fila=cand[0],
                                 empate=[c for c in cand if (c['NK'], c['K']) == (cand[0]['NK'], cand[0]['K'])].__len__())
                            if cand else dict(cumple=False, motivo='ninguna celda D=12/C32 pasa U1, U2 y U3 a la vez'))
    js = os.path.join(AQUI, 'escala_codigo_salida.json')
    json.dump(out, open(js, 'w', encoding='utf-8'), indent=1)
    txt = tabla_md(out['resultados']['C32'], 'Catálogo C32 (D = 12: 8 tokens × 3 variantes = 32 estímulos; '
                                             'D = 6: comparador degradado V = 1 → 16 estímulos). Semillas 1–200.')
    if 'C16' in out['resultados']:
        txt += "\n\n" + tabla_md(out['resultados']['C16'], 'Catálogo C16 (D = 12: 4 tokens × 3 variantes = 16 estímulos; '
                                                          'D = 6: comparador degradado V = 1 → 8 estímulos). Semillas 1–200.')
    if 'posthoc_fuera_de_rejilla' in out:
        txt += ("\n\n" + tabla_md(out['posthoc_fuera_de_rejilla'],
                'POST-HOC, FUERA de la rejilla preregistrada de §3 y FUERA del veredicto (D = 12, C32, semillas 1–200). '
                'Existe sólo para cuantificar *cuánto* NK haría falta; ninguna de estas filas puede recomendarse.'))
    txt += (f"\n\n**P2 (ancla de instrumento contra `DISENO_mundo_grande` §1.1, ±5 pp): "
            f"{'PASA' if okP2 else 'FALLA — el instrumento está mal y no se publica recomendación'}.** "
            f"Detalle campo a campo en `escala_codigo_salida.json` → `P2_verificacion_instrumento`.\n\n"
            f"*Generado por `escala_codigo.py` en {time.time()-t0:.1f} s, un solo proceso, sin `Pool`. "
            f"Salida cruda: `escala_codigo_salida.json`.*")
    escribe_seccion8(txt)
    print(f"\nrecomendacion: {out['recomendacion']}")
    print(f"escrito: {js}  ({time.time()-t0:.1f} s)")
