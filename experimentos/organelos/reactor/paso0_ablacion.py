"""paso0_ablacion.py — PASO 0 del borrador PREREGISTRO_F1_reactor_BORRADOR.md (§6d y §7b): calibracion de c con datos VIEJOS.
SONDA: no declara nada. Un proceso, sin Pool, T = 200 000.

Mision: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con controles
y replicas).

Lee los 40 M_BLOQ_V_s*.json registrados (48411-30 serie, 48431-50 replica; esc 90, T 500 000; SOLO lectura) y aplica la letra del
borrador: formas canonicas (§6, codigo copiado campo a campo), clases = formas fijadas en >= 2 semillas de la misma serie, genoma
portador G+ y G- (G+ sin TODAS las reglas de esa (condicion, accion)), los dos como `forzada` con tasas 0 (brazo FORZ_V de
corre_bloques, que se IMPORTA sin tocar), t_corte 100 000, T 200 000, esc 90, semillas 55151-55155, K en [100 000, 200 000].
Funcional = K(G+) > K(G-) en 5/5 y mediana de la diferencia >= 5 % de la mediana de K(G+).
Control que debe fallar (efecto ~0): G+ del organo con una regla TESTIGO de condicion nunca cierta anadida, contra G+.
Control extra (lectura del borrador): la misma con una regla de condicion SIEMPRE cierta (el borrador la llama silenciosa).
Uso: python paso0_ablacion.py --plan | --corre | --tabla
"""
import argparse, glob, hashlib, json, os, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
OPUSM = os.path.join(ORG, 'bloques', 'opusM')
if OPUSM not in sys.path: sys.path.insert(0, OPUSM)
DATOS = os.path.join(AQUI, 'datos', 'paso0')
SERIES = {'serie': 'serie_s48411-48430_T500000', 'replica': 'serie_s48431-48450_T500000'}
SEM_ABL = (55151, 55152, 55153, 55154, 55155)
T_ABL = 200000
UMBRAL = 0.05

# ---------------------------------------------------------------- letra del borrador §6 (copiada campo a campo)
PATM = {'A': (1, 1, 0, 1, 0, 0), 'B': (1, 0, 1, 0, 1, 0), 'C': (0, 1, 1, 0, 0, 1), 'D': (0, 0, 1, 0, 1, 1)}
SENT = ['hambre', 'sed', 'cerca', 'pixF', 'pixM', 'Rult']; ACC = ['boca', 'hacia', 'quieto', 'parir']
W_SIL = 0.25; FRAC_FIJ = 0.5; MIN_VIVOS = 12


def condicion(r):
    s, p, c, th = int(r[0]), int(r[1]), (r[2] > 0.5), float(r[3])
    if s in (3, 4):
        m = tuple(int((PATM[x][p] > th) if c else (PATM[x][p] < th)) for x in 'ABCD')
        if sum(m) in (0, 4): return None
        if m[0] == 1: return (SENT[s], m), 1
        return (SENT[s], tuple(1 - z for z in m)), -1
    if (c and th >= 1.0) or ((not c) and th <= 0.0): return None
    return (SENT[s], '>'), (1 if c else -1)


def formas_cuerpo(reglas):
    W = {}
    for r in reglas:
        cg = condicion(r)
        if cg is None: continue
        k = (cg[0], ACC[int(r[4])]); W[k] = W.get(k, 0.0) + cg[1] * float(r[5])
    return {(k[0], k[1], '+' if w > 0 else '-') for k, w in W.items() if abs(w) >= W_SIL}


def formas_fijadas(vivos):
    if len(vivos) < MIN_VIVOS: return {}
    cnt = {}
    for x in vivos:
        for f in formas_cuerpo(x[3]): cnt[f] = cnt.get(f, 0) + 1
    return {f: c / len(vivos) for f, c in cnt.items() if c / len(vivos) >= FRAC_FIJ}


def nom(f):
    c = f[0]
    cs = (c[0] + '[' + ''.join(x for x, z in zip('ABCD', c[1]) if z) + ']') if isinstance(c[1], tuple) else f'{c[0]}[>]'
    return f'{cs}->{f[1]}{f[2]}'


ORGANO = (('pixF', (1, 0, 1, 0)), 'boca', '+')   # el organo de rechazo de veneno/sal en forma canonica (boca - si B/D)


def carga():
    D = {}
    for etq, car in SERIES.items():
        D[etq] = {}
        for f in sorted(glob.glob(os.path.join(OPUSM, 'datos', car, 'M_BLOQ_V_s*.json'))):
            d = json.load(open(f, encoding='utf-8')); D[etq][d['seed']] = d
    return D


def silenciosas_fijadas(vivos):
    """Testigos del borrador §6b: reglas de condicion constante, clave cruda (sentido, parametro, comparador, accion), >= 50 %."""
    if len(vivos) < MIN_VIVOS: return {}
    cnt = {}
    for x in vivos:
        ks = set((int(r[0]), int(r[1]), int(r[2] > 0.5), int(r[4])) for r in x[3] if condicion(r) is None)
        for k in ks: cnt[k] = cnt.get(k, 0) + 1
    return {k: c / len(vivos) for k, c in cnt.items() if c / len(vivos) >= FRAC_FIJ}


def plan():
    D = carga(); P = dict(series={}, clases=[])
    for etq, S in D.items():
        fij = {s: formas_fijadas((d.get('bloques') or {}).get('vivos_T') or []) for s, d in S.items()}
        sil = {s: silenciosas_fijadas((d.get('bloques') or {}).get('vivos_T') or []) for s, d in S.items()}
        en = {}
        for s, ff in fij.items():
            for f in ff: en.setdefault(f, []).append(s)
        P['series'][etq] = dict(fij={s: {nom(f): round(v, 3) for f, v in ff.items()} for s, ff in fij.items()},
                                sil={s: {str(k): round(v, 3) for k, v in ff.items()} for s, ff in sil.items()},
                                n_fij=[len(fij[s]) for s in sorted(fij)], en={nom(f): sorted(v) for f, v in en.items()})
        for f, ss in sorted(en.items(), key=lambda z: (-len(z[1]), nom(z[0]))):
            if len(ss) < 2: continue
            s0 = sorted(ss, key=lambda s: (-fij[s][f], s))[0]
            vv = S[s0]['bloques']['vivos_T']
            por = {}
            for i, x in enumerate(vv):
                if f in formas_cuerpo(x[3]): por.setdefault(json.dumps(x[3]), []).append((x[1], -i))
            gp = json.loads(sorted(por.items(), key=lambda z: (-len(z[1]), -max(z[1])[0], -max(z[1])[1]))[0][0])
            gm = [r for r in gp if not (condicion(r) is not None and (condicion(r)[0], ACC[int(r[4])]) == (f[0], f[1]))]
            P['clases'].append(dict(serie=etq, forma=nom(f), organo=(f == ORGANO), semillas=sorted(ss), portador=s0, frac=round(fij[s0][f], 3),
                                    n_portan=len(por[json.dumps(gp)]), Gmas=gp, Gmenos=gm))
    # controles: sobre el G+ del organo de la serie
    g0 = next(c for c in P['clases'] if c['organo'] and c['serie'] == 'serie')['Gmas']
    g1 = next(c for c in P['clases'] if c['organo'] and c['serie'] == 'replica')['Gmas']
    P['controles'] = [dict(nombre='testigo NUNCA cierta (pixF0 > 1.0 -> boca -3) sobre G+ del organo (serie): debe dar ~0',
                           Gmas=g0 + [[3, 0, 1, 1.0, 0, -3.0]], Gmenos=g0),
                      dict(nombre='testigo NUNCA cierta (hambre > 1.0 -> parir +3) sobre G+ del organo (replica): debe dar ~0',
                           Gmas=g1 + [[0, 0, 1, 1.0, 3, 3.0]], Gmenos=g1)]
    return P


def gh(G):
    return hashlib.sha256(json.dumps(G).encode()).hexdigest()[:12]


def K_de(G, seed, CB):
    car = os.path.join(DATOS, gh(G)); fn = os.path.join(car, f'M_FORZ_V_s{seed}.json')
    if os.path.exists(fn): return json.load(open(fn, encoding='utf-8'))
    o = CB.corre(seed, 'FORZ_V', T_ABL, car, extra=dict(forzada=[list(map(float, r)) for r in G]))
    return o


def corre():
    import corre_bloques as CB
    CB.verifica()
    P = plan(); os.makedirs(DATOS, exist_ok=True)
    json.dump(P, open(os.path.join(DATOS, 'plan.json'), 'w', encoding='utf-8'))
    t0 = time.time(); n = 0
    for c in P['clases'] + P['controles']:
        for lado in ('Gmas', 'Gmenos'):
            for s in SEM_ABL:
                o = K_de(c[lado], s, CB); n += 1
                print(f"[{time.strftime('%H:%M:%S')}] {c.get('serie', 'control')} {c.get('forma', c.get('nombre'))[:40]} {lado} {gh(c[lado])} s{s}: "
                      f"K {o['K']:.2f} persiste {o['persiste']} ({o['seg']} s; {time.time() - t0:.0f} s)", flush=True)
    tabla()


def tabla():
    P = json.load(open(os.path.join(DATOS, 'plan.json'), encoding='utf-8'))
    def Ks(G):
        return [json.load(open(os.path.join(DATOS, gh(G), f'M_FORZ_V_s{s}.json'), encoding='utf-8')) for s in SEM_ABL]
    func = {}
    print('CLASES (forma fijada en >= 2 semillas de la serie): K(G+) y K(G-) en 55151-55155, T 200 000, K en [100k, 200k]')
    for c in P['clases'] + P['controles']:
        a = Ks(c['Gmas']); b = Ks(c['Gmenos']); ka = [x['K'] for x in a]; kb = [x['K'] for x in b]
        d = [x - y for x, y in zip(ka, kb)]; gana = sum(x > 0 for x in d)
        rel = float(np.median(d)) / float(np.median(ka)) if np.median(ka) else float('nan')
        f = (gana == 5 and rel >= UMBRAL)
        et = c.get('forma') or c['nombre']
        if 'forma' in c: func[(c['serie'], c['forma'])] = f
        print(f"- {c.get('serie', 'CONTROL'):8s} {et:60s} semillas {len(c.get('semillas', []))} portador {c.get('portador')} |G+| {len(c['Gmas'])} |G-| {len(c['Gmenos'])}"
              f"\n    K(G+) {[round(x, 1) for x in ka]} persiste {sum(x['persiste'] for x in a)}/5 · K(G-) {[round(x, 1) for x in kb]} persiste {sum(x['persiste'] for x in b)}/5"
              f"\n    dif {[round(x, 2) for x in d]} · {gana}/5 > 0 · mediana dif / mediana K(G+) = {rel:+.3f} -> {'FUNCIONAL' if f else 'no funcional'}"
              f"{' [ORGANO DE RECHAZO]' if c.get('organo') else ''}")
    print('\nPOR SEMILLA: formas fijadas -> funcionales (F), pasajeras (p: clase probada y no funcional; u: unica en su serie, no probada = no funcional por regla)')
    tot = {}
    for etq, S in P['series'].items():
        for s in sorted(S['fij'], key=int):
            ff = S['fij'][s]; F = [f for f in ff if func.get((etq, f))]
            org = [f for f in F if f == nom(ORGANO)]; Fx = [f for f in F if f != nom(ORGANO)]
            pp = [f for f in ff if (etq, f) in func and not func[(etq, f)]]; uu = [f for f in ff if (etq, f) not in func]
            tot[(etq, s)] = (len(ff), len(F), len(Fx), len(pp), len(uu), len(S['sil'][s]))
            print(f"  {etq:7s} s{s}: fijadas {len(ff)} · funcionales {len(F)} (sin organo {len(Fx)}) · pasajeras {len(pp)} · unicas {len(uu)} · testigos silenciosos fijados {len(S['sil'][s])}"
                  f" | F: {F} p: {pp} u: {uu}")
    print('\nBASE k = semillas con >= c formas funcionales fijadas')
    for nombre, idx in (('contando el organo de rechazo', 1), ('EXCLUYENDO el organo de rechazo', 2), ('sin filtro de funcion (todas las fijadas)', 0)):
        for c in (1, 2, 3):
            ks = {e: sum(1 for (e2, s), v in tot.items() if e2 == e and v[idx] >= c) for e in P['series']}
            print(f"  {nombre:42s} c = {c}: serie {ks['serie']}/20 · replica {ks['replica']}/20 · agrupada {sum(ks.values())}/40")


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--plan', action='store_true'); ap.add_argument('--corre', action='store_true'); ap.add_argument('--tabla', action='store_true')
    a, resto = ap.parse_known_args()
    if resto: raise SystemExit(f'banderas desconocidas: {resto}')
    if a.plan:
        P = plan()
        for etq, S in P['series'].items():
            print(etq, 'formas fijadas por semilla:', S['n_fij']); print('   ', ' | '.join(f'{k} {len(v)}' for k, v in sorted(S['en'].items(), key=lambda z: -len(z[1]))))
            print('    testigos silenciosos fijados por semilla:', [len(S['sil'][s]) for s in sorted(S['sil'])], {s: v for s, v in S['sil'].items() if v})
        for c in P['clases'] + P['controles']:
            print(c.get('serie', 'CONTROL'), c.get('forma', c.get('nombre')), 'semillas', c.get('semillas'), 'portador', c.get('portador'), c.get('frac'), 'n', c.get('n_portan'),
                  '\n   G+', gh(c['Gmas']), c['Gmas'], '\n   G-', gh(c['Gmenos']), c['Gmenos'])
        print('genomas distintos a correr:', len(set(gh(c[l]) for c in P['clases'] + P['controles'] for l in ('Gmas', 'Gmenos'))), 'x 5 semillas')
    elif a.corre: corre()
    elif a.tabla: tabla()
    else: raise SystemExit('usa --plan, --corre o --tabla')


if __name__ == '__main__':
    main()
