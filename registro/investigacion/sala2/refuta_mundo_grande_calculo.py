"""REFUTADOR sala 2 (lente medibilidad) de DISENO_mundo_grande.md — calculo ESTRUCTURAL, T = 0, un proceso, sin organismo,
sin Pool, sin tocar ningun archivo existente. Cuatro comprobaciones:
  (1) reproduce la fila 1 y la fila "intensidad 0.5" de la tabla §1.1 desde diagnostico_familias_sala2_salida.json, y
      comprueba si las filas 60/90 celdas y D=9 salen del script entregado (tiene NK=30 fijo y un solo JSON de salida);
  (2) separa, dentro de "tokeniza", los EMPATES (propio == otros >= K-1): el script los cuenta como tokenizacion, pero
      _tok (A3) desempata por evidencia ncod, no por "el token propio";
  (3) aritmetica de la via LENTA del tronco (organismo_v14.py lineas 116-120, eta_s=0.15, lam=0.05, clip_s=10) para el
      umbral de P2 "OFF mediana >= 4 mordidas tras el descubrimiento": cuantas mordidas de la excepcion hacen que
      (Wps-Wns)@P tenga el signo del mundo, con k mordidas del token intercaladas por cada mordida de la excepcion;
  (4) aritmetica de la via RAPIDA (lineas 121-129, eta=0.03, clip 3) para el residuo |R - W_tok| de una variante de la
      MISMA valencia cuando el token acaba de cruzar la puerta (puerta_pat=5), frente a umbral_exc=2.0.
Uso: python registro/investigacion/sala2/refuta_mundo_grande_calculo.py   (< 10 s)"""
import sys, os, json, itertools
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__))
K = 3
out = {}

# ---------- (1) la tabla §1.1 desde el JSON entregado ----------
J = json.load(open(os.path.join(AQUI, 'diagnostico_familias_sala2_salida.json'), encoding='utf-8'))
def resumen(d):
    q = lambda x: (round(float(np.median(x)), 3), round(float(np.mean(x)), 3))
    return dict(tokeniza=q(d['tokeniza']), exacto=q(d['exacto']), falsa=q(d['falsa']), ninguna=q(d['ninguna']),
                alias_tok=int(sum(d['alias_tok'])), alias_any=int(sum(d['alias_any'])), S=d['S'], D=d['D'], F=d['F'], NK='30 (fijo en el script)')
out['1_json_entregado'] = {k: resumen(v) for k, v in J.items()}

# ---------- (2) re-implementacion con NK variable y empates separados ----------
def mundo(D, V, F, r):
    shape = D - V; combos = list(itertools.combinations(range(shape), 3)); r.shuffle(combos)
    toks = {}; i = 0
    while len(toks) < F: toks['T%d' % len(toks)] = combos[i]; i += 1
    pats = {}
    for n, c in toks.items():
        P = np.zeros(D); P[list(c)] = 1.; pats[n] = P
        for v in range(V):
            Q = P.copy(); Q[shape + v] = 1.; pats[n + 'v%d' % v] = Q
    return toks, pats
def diag(D, V, F, NK, S=200):
    r = dict(tokeniza=[], tokeniza_estricto=[], empate=[], falsa=[], ninguna=[], exacto=[], alias_tok=[], alias_any=[])
    for seed in range(1, S + 1):
        rng = np.random.default_rng(seed); rng.uniform(.1, .4, (2, D + 3)); KW = rng.uniform(0, 1, (NK, D))
        rw = np.random.default_rng(50000 + seed); toks, pats = mundo(D, V, F, rw)
        cod = {n: frozenset(np.argsort(KW @ P)[-K:].tolist()) for n, P in pats.items()}
        tk = [n for n in pats if 'v' not in n]; nt = ne = nf = nn = ex = 0
        for n in pats:
            if 'v' in n:
                base = n.split('v')[0]; propio = len(cod[n] & cod[base]); otros = max(len(cod[n] & cod[t]) for t in tk if t != base)
                if propio == K: ex += 1
                if propio >= K - 1 and propio >= otros:
                    nt += 1
                    if propio == otros: ne += 1          # EMPATE: el script lo cuenta como tokeniza; _tok desempata por ncod
                elif otros >= K - 1: nf += 1
                else: nn += 1
        nv = F * V
        r['tokeniza'].append(nt / nv); r['tokeniza_estricto'].append((nt - ne) / nv); r['empate'].append(ne / nv)
        r['falsa'].append(nf / nv); r['ninguna'].append(nn / nv); r['exacto'].append(ex / nv)
        r['alias_tok'].append(int(any(cod[a] == cod[b] for a, b in itertools.combinations(tk, 2))))
        r['alias_any'].append(int(any(cod[a] == cod[b] for a, b in itertools.combinations(list(pats), 2))))
    q = lambda x: (round(float(np.median(x)), 3), round(float(np.mean(x)), 3))
    return dict(D=D, V=V, F=F, NK=NK, S=S, tokeniza=q(r['tokeniza']), tokeniza_estricto=q(r['tokeniza_estricto']),
                empate=q(r['empate']), falsa=q(r['falsa']), ninguna=q(r['ninguna']), exacto=q(r['exacto']),
                alias_tok=int(sum(r['alias_tok'])), alias_any=int(sum(r['alias_any'])))
out['2_reimplementacion'] = [diag(12, 3, 8, 30), diag(12, 3, 8, 60), diag(12, 3, 8, 90), diag(9, 3, 4, 30)]
out['2_nota'] = ("NK=60/90 aqui son celdas UNIFORMES nuevas (rng.uniform), que es lo unico que el script puede hacer; en el tronco las celdas 31-90 "
                 "nacen por fision: KW[j]=clip(KW[c]*0.95+paso*(P-mu[c]),0,5)*_rel, ciegas fuera de P y correlacionadas con el codigo de la madre. "
                 "No son la misma poblacion; el 'techo baja al ganar celdas' no esta calculado sobre las celdas que el tronco crea.")

# ---------- (3) via LENTA: mordidas de la excepcion hasta signo correcto (lineas 116-120 del tronco) ----------
eta_s, lam, clip_s, aversion = 0.15, 0.05, 10.0, 1.0
def mordida_lenta(Wps, Wns, P, R):
    _ws = float((Wps - Wns) @ P); _ds = R - _ws
    _mcs = np.minimum(Wps, Wns) * (P > 0); Wps = Wps - lam * _mcs; Wns = Wns - lam * _mcs
    if _ds > 0: Wps = np.clip(Wps + eta_s * _ds * P, 0, clip_s)
    else:       Wns = np.clip(Wns + eta_s * aversion * (-_ds) * P, 0, clip_s)
    return Wps, Wns
def p2_off(R_tok, R_exc, k_tok_entre, n0=30, D=12, tope=20):
    T = np.zeros(D); T[[0, 1, 2]] = 1.; V = T.copy(); V[9] = 1.        # token 3 px de forma; variante = token + 1 px de variable
    Wps = np.zeros(D); Wns = np.zeros(D)
    for _ in range(n0): Wps, Wns = mordida_lenta(Wps, Wns, T, R_tok)      # token consolidado en la lenta
    lect0 = float((Wps - Wns) @ V)
    for n in range(1, tope + 1):
        Wps, Wns = mordida_lenta(Wps, Wns, V, R_exc)                       # mordida n de la excepcion (tras el descubrimiento = mordida 1)
        for _ in range(k_tok_entre): Wps, Wns = mordida_lenta(Wps, Wns, T, R_tok)
        lect = float((Wps - Wns) @ V)
        if lect * R_exc > 0: return dict(mordidas_hasta_signo=n, lectura_antes=round(lect0, 3), lectura_despues=round(lect, 3), W_token_despues=round(float((Wps - Wns) @ T), 3))
    return dict(mordidas_hasta_signo=None, lectura_antes=round(lect0, 3), lectura_despues=round(float((Wps - Wns) @ V), 3))
out['3_P2_OFF_via_lenta'] = {}
for nombre, Rt, Re in (('token_veneno_excepcion_comida', -3.0, 1.0), ('token_comida_excepcion_veneno', 1.0, -3.0)):
    out['3_P2_OFF_via_lenta'][nombre] = {f'k_tok_entre={k}': p2_off(Rt, Re, k) for k in (0, 1, 3, 10)}
out['3_nota'] = ("P2 exige OFF mediana >= 4; el diseno deriva ese 4 de la puerta por codigo (5 mordidas), pero OFF lee la LENTA mientras el codigo "
                 "de la variante no es familiar, y la lenta a eta_s=0.15 mueve 0.15*|R-W| por pixel en UNA mordida (el propio B5 del diseno lo dice). "
                 "La 'mordida 1' de la tabla es la del descubrimiento; el signo se lee ANTES de la mordida siguiente.")

# ---------- (4) via RAPIDA: residuo |R - W_tok| de una variante de la MISMA valencia cuando el token cruza la puerta ----------
eta = 0.03
def w_rapida(R, n):
    Wp = np.zeros(3); Wn = np.zeros(3)
    for _ in range(n):
        wf = float((Wp - Wn).sum()); dlt = R - wf
        ix = np.ones(3, bool); mcom = np.minimum(Wp, Wn); Wp -= lam * mcom; Wn -= lam * mcom
        if dlt > 0: Wp = np.clip(Wp + eta * dlt, 0, 3.)
        else:       Wn = np.clip(Wn + eta * aversion * (-dlt), 0, 3.)
    return float((Wp - Wn).sum())
out['4_residuo_en_la_puerta'] = {}
for nombre, R in (('token_veneno_R=-3', -3.0), ('token_comida_R=+1', 1.0)):
    fila = {}
    for n in (5, 6, 8, 10, 15, 20, 40):
        w = w_rapida(R, n); R_exc = -3.0 if R == 1.0 else 1.0
        fila[f'{n}_mordidas'] = dict(W_tok=round(w, 3), residuo_misma_valencia=round(abs(R - w), 3), residuo_excepcion=round(abs(R_exc - w), 3))
    out['4_residuo_en_la_puerta'][nombre] = fila
out['4_nota'] = ("umbral_exc=2.0: una variante de la MISMA valencia que su token escribe un nodo de excepcion falso si |R-W_tok|>2. "
                 "Con puerta_pat=5 el token es 'familiar' (y por tanto 'token' para _tok) desde su 5a mordida; el residuo a esa altura se lee aqui.")

# ---------- (5) barajado: fraccion esperada de variantes con valencia distinta a su token ----------
out['5_barajado'] = dict(tokens_comida=4, tokens_veneno=4, p_valencia_distinta_si_toma_la_de_OTRO_token_al_azar=round(4 / 7, 3),
                         nota="P8 exige n_slots >= 0.8 x #variantes presentes en 'barajado'; un nodo solo se escribe si |R-W_tok|>2, es decir si la valencia difiere: esperado 4/7 = 0.571 < 0.8 salvo que 'otro token' se restrinja a valencia opuesta (no esta escrito).")

json.dump(out, open(os.path.join(AQUI, 'refuta_mundo_grande_calculo_salida.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
