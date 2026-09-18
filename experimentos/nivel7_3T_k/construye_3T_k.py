"""Genera mundo_temporal_k.py = mundo_temporal_v13.py (f9c3169b32f393d4) + profundidad de historia k.
Con k=1 es mundo_temporal_v13 EXACTO (identidad obligatoria). Anclas con conteo exacto.
  - entrada [actual, h1..hk] (NIN = 6*(k+1)); regla: A comida si hk == 'B', veneno si hk == 'A'; B neutro.
  - W / sep / solap_A promediados sobre los 2^(k-1) rellenos de los distractores (k=1: identicos a los originales).
"""
import hashlib, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(RAIZ, 'experimentos', 'v13_reverificacion', 'mundo_temporal_v13.py')
NL = chr(10)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sust(texto, viejo, nuevo, n=1, etiqueta=''):
    c = texto.count(viejo)
    if c != n:
        raise SystemExit(f"ANCLA {etiqueta or viejo[:60]!r}: aparece {c} veces, se esperaban {n}. Abortado.")
    return texto.replace(viejo, nuevo)


# (ancla, reemplazo, n, etiqueta). Las lineas se unen con NL para no depender del escapado del editor.
PARCHES = [
    (["import sys, numpy as np"], ["import sys, numpy as np", "import itertools   # 3T-k"], 1, 'import'),
    (["def valor(cur, last):", "    if cur == 'B': return 'neutro'", "    return 'comida' if last == 'B' else 'veneno'"],
     ["def valor(cur, last):",
      "    \"\"\"3T-k: last es la historia (h1..hk); manda el slot MAS PROFUNDO. Con k=1 es la regla original.\"\"\"",
      "    if cur == 'B': return 'neutro'",
      "    hk = last[-1] if isinstance(last, tuple) else last",
      "    return 'comida' if hk == 'B' else 'veneno'"], 1, 'regla del mundo'),
    (["memoria_rechazo=20, mu_norm=False, div_signo=False, eta_s=0.0, clip_s=3.0, puerta=None):"],
     ["memoria_rechazo=20, mu_norm=False, div_signo=False, eta_s=0.0, clip_s=3.0, puerta=None, kprof=1):"], 1, 'firma'),
    (["    cfg = ARMS[arm]; NIN = cfg['nin']; plast = cfg['plast']; falso = cfg['falso']"],
     ["    cfg = ARMS[arm]; NIN = cfg['nin'] if cfg['nin'] == 6 else 6 * (kprof + 1); plast = cfg['plast']; falso = cfg['falso']   # 3T-k",
      "    FILL = list(itertools.product('AB', repeat=kprof - 1))   # rellenos de los distractores (k=1: uno, vacio)",
      "    def hist_de(p, fill=None): return (tuple('A' * (kprof - 1)) if fill is None else tuple(fill)) + (p,)   # h1..hk con hk = p"],
     1, 'NIN y rellenos'),
    (["rng.uniform(0, 1, (NK, 12))"], ["rng.uniform(0, 1, (NK, NIN))"], 2, 'init full (C2)'),
    (["    def inp(cur, prev):", "        return PAT[cur] if NIN == 6 else np.concatenate([PAT[cur], PAT[prev]])"],
     ["    def inp(cur, prev):",
      "        if NIN == 6: return PAT[cur]",
      "        h = prev if isinstance(prev, tuple) else hist_de(prev)   # una letra = slot profundo con relleno canonico 'A'",
      "        return np.concatenate([PAT[cur]] + [PAT[x] for x in h])"], 1, 'entrada'),
    (["    pos = 0; E = 1.0; objs = {}; tipos = ['A', 'B']; last = 'B'"],
     ["    pos = 0; E = 1.0; objs = {}; tipos = ['A', 'B']; last = ('B',) * kprof   # 3T-k: historia h1..hk"], 1, 'historia inicial'),
    (["        cods = {f'{c}|{p}': code(inp(c, p)) for c, p in SIT}"],
     ["        cods = {f'{c}|{p}': code(inp(c, p)) for c, p in SIT}   # relleno canonico (k=1: exacto)",
      "        _ov = lambda c: [len(code(inp(c, hist_de('A', f))) & code(inp(c, hist_de('B', f)))) for f in FILL]",
      "        _sA = _ov('A'); _sB = _ov('B')"], 1, 'codigos'),
    (["        return dict(t=t, solap_A=len(cods['A|A'] & cods['A|B']),", "                    solap_B=len(cods['B|A'] & cods['B|B']),"],
     ["        return dict(t=t, solap_A=(_sA[0] if kprof == 1 else round(float(np.mean(_sA)), 3)),",
      "                    solap_B=(_sB[0] if kprof == 1 else round(float(np.mean(_sB)), 3)),"], 1, 'solap'),
    (["wt = float(KW[activa, 6:].sum()) if NIN == 12 else 0.0"], ["wt = float(KW[activa, 6:].sum()) if NIN > 6 else 0.0"], 1, 'wt'),
    (["wt_c = float(KW[idx, 6:].sum()) if NIN == 12 else 0.0"], ["wt_c = float(KW[idx, 6:].sum()) if NIN > 6 else 0.0"], 1, 'wt_c'),
    (["                    W={f'{c}|{p}': round(valor_tot(inp(c, p)), 3) for c, p in SIT})   # v13: valor total"],
     ["                    W={f'{c}|{p}': (round(valor_tot(inp(c, p)), 3) if kprof == 1 else round(float(np.mean([valor_tot(inp(c, hist_de(p, f))) for f in FILL])), 3)) for c, p in SIT})   # 3T-k: media sobre rellenos"],
     1, 'W del snapshot'),
    (["            prev_sent = (('A', 'B')[int(rng2.integers(2))] if falso else last)"],
     ["            prev_sent = (tuple(('A', 'B')[int(rng2.integers(2))] for _ in range(kprof)) if falso else last)   # 3T-k"], 1, 'canal falso'),
    (["                if last == 'B': prevB[qq] += 1"], ["                if last[-1] == 'B': prevB[qq] += 1"], 1, 'prevB'),
    (["                    (n_AB if last == 'B' else n_AA)[qq] += 1"], ["                    (n_AB if last[-1] == 'B' else n_AA)[qq] += 1"], 1, 'n_AB'),
    (["                    if last == 'B': e_prevB += 1"], ["                    if last[-1] == 'B': e_prevB += 1"], 1, 'e_prevB'),
    (["                        if last == 'B': e_AB += 1"], ["                        if last[-1] == 'B': e_AB += 1"], 1, 'e_AB'),
    (["                last = kk"], ["                last = (kk,) + last[:-1]   # 3T-k: desplaza la historia"], 1, 'historia'),
    (["ft = float(np.abs(dist[6:]).sum()) / a1 if (a1 > 0 and NIN == 12) else 0.0"],
     ["ft = float(np.abs(dist[6:]).sum()) / a1 if (a1 > 0 and NIN > 6) else 0.0"], 2, 'ft'),
    (["split_t.append((t, kk, prev_sent, round(ft, 3)))"], ["split_t.append((t, kk, (prev_sent[0] if kprof == 1 else prev_sent), round(ft, 3)))"], 2, 'split_t'),
    (["        seed=seed, arm=arm,"], ["        seed=seed, arm=arm, k=kprof,"], 1, 'return k'),
]

if __name__ == '__main__':
    if h16(ORIGEN) != 'f9c3169b32f393d4':
        raise SystemExit(f"ORIGEN sha {h16(ORIGEN)} != f9c3169b32f393d4")
    s = open(ORIGEN, encoding='utf-8').read()
    for viejo, nuevo, n, et in PARCHES:
        s = sust(s, NL.join(viejo), NL.join(nuevo), n, et)
    cab = ('"""mundo_temporal_k = mundo_temporal_v13.py (f9c3169b32f393d4) + profundidad de historia k (3T-k). Generado por' + NL +
           'construye_3T_k.py. NO editar. Con k=1 es mundo_temporal_v13 exacto (identidad obligatoria). La regla del mundo' + NL +
           'depende del slot MAS PROFUNDO; los intermedios son distractores. W, sep y solap se promedian sobre los rellenos."""' + NL)
    d = os.path.join(AQUI, 'mundo_temporal_k.py')
    open(d, 'w', encoding='utf-8', newline=NL).write(cab + s)
    print(f"  {os.path.relpath(d, RAIZ):44s} {h16(d)}  {sum(1 for _ in open(d, encoding='utf-8'))} lineas")
