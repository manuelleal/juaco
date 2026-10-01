"""corre_s2.py — SONDA 2 (1-oct-2026, MODO RAFAGA, EXPLORATORIA: NADA se declara): P8 (componer) FUERA de la presion de supervivencia, con
CELDA RETENIDA. UN proceso, <= 6 corridas, <= 200 000 pasos. Cada corrida escribe su JSON (fila + memoria por linaje + respuestas); resumen.json.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y replicas).

(a) CRIA: O1_LUGAR (el carro de P1, sin composicion) en mundo_ret (P1b + letra E (+0.3, -0.1) a p_x 0.15 que NUNCA nace dentro del oasis). Cada corrida
    ES corre_v143.tarea (se importa). Un envoltorio PASIVO del modulo del carro (Capta: solo recuerda la ultima instancia creada por linaje) permite
    leer al final la tabla por letra (suma, n) y la memoria de lugar (lugar, nl) a precision completa. El arnes prueba que no cambia la corrida.
(b) PREGUNTA (sin mundo, sin resultado()): para cada linaje se reconstruyen TRES carros con nace(memoria) sobre LA MISMA memoria criada:
      comp     O1_LUGAR_COMP      (el bono de lugar se suma a letras mixtas)
      lug      O1_LUGAR           (sin composicion)
      compbar  O1_LUGAR_COMP_BAR  (composicion leyendo el bono del ANTIPODA)
    y se llama actua() con observaciones sinteticas: el cuerpo a un paso del objeto, rejilla 5x5 de niveles, 4 celdas dentro del oasis y sus antipodas.
    LIMPIA = ademas hay una A a la vista 10 celdas mas alla (la limpieza de O1 queda apagada: medida principal); SOLA = solo el objeto.
    Medida: P(muerde E dentro), P(muerde E fuera), D = dentro - fuera; A dentro, B dentro; eleccion A contra E dentro a igual distancia.
SEMILLAS NUEVAS: crianza 737300-  ·  arnes 737401
  python experimentos/organelos/escalera/sondas/corre_s2.py --identidad
  python experimentos/organelos/escalera/sondas/corre_s2.py --humo [--T 60000 --n 6 --p_x 0.15 --desde 737300 --nota '...']
  python experimentos/organelos/escalera/sondas/corre_s2.py --lee <carpeta>
"""
import argparse, glob, json, os, platform, statistics as st, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
sys.path.insert(0, ESC); sys.path.insert(0, AQUI)
import corre_c as RC             # se importa (no se toca)
import mundo_ret as MR
CO = RC.CO; CV = RC.CV; P = RC.P; ME = RC.ME; MC = RC.MC
h16 = CO.h16; med = CO.med

DATOS = os.path.join(AQUI, 'datos')
MUNDO = dict(RC.MUNDO_C, letra_x='E', efecto_x=(0.3, -0.1), p_x=0.15)
BRAZOS = {'comp': 'O1_LUGAR_COMP', 'lug': 'O1_LUGAR', 'compbar': 'O1_LUGAR_COMP_BAR'}
NIVELES = (0.3, 0.5, 0.7, 0.9, 1.1)
DENTRO_OFF = (4, 13, 22, 31)          # celdas del objeto dentro del oasis (z0 + off; W = 36); fuera = su antipoda (+ L/2)
FUERA_GEN = (60, 120, 240, 300)       # fuera 'general' (desde el centro del oasis): mide si el bono es difuso
ELIGE_OFF = (10, 18, 25); LEJOS = 10; LADO = 5
SEM = dict(humo=737300, arnes=737401)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000


class Capta:
    """envoltorio PASIVO del modulo del carro: recuerda la ultima instancia creada por linaje (la que queda viva al final de la corrida)."""
    def __init__(self, mod): self.mod = mod; self.ult = {}
    def crea(self, ctx):
        c = self.mod.crea(ctx); self.ult[int(ctx['indice'])] = c; return c
    def __getattr__(self, k): return getattr(self.mod, k)


def memoria(c):
    return dict(letras={k: [[float(z) for z in c.suma[k]], int(c.n[k])] for k in c.n}, lugar=[[float(z) for z in f] for f in c.lugar], nl=[int(z) for z in c.nl])


def cria(seed, T, mundo, ret=1):
    """una corrida de crianza -> (x de corre_v143.tarea + crudo, memorias por linaje)."""
    m, est = RC.modulo('O1_LUGAR'); cap = Capta(m); crudo = []; orig = P.run; MR.RETENIDA[0] = int(ret)
    est = dict(est, mundo=dict(mundo), retenida=int(ret))

    def run2(*a, **k):
        r = MR.run(*a, **dict(k, **mundo)); crudo.append(r); return r
    P.run = run2; CV._MODS['O1_LUGAR'] = cap
    try:
        x = CV.tarea((seed, 'O1_LUGAR', T))
    finally:
        P.run = orig; CV._MODS['O1_LUGAR'] = m; MR.RETENIDA[0] = 0
    r = crudo[0]
    for l, d in zip(x['linajes'], r['linajes']): l['_oasis'] = d['_carrera'].get('oasis')
    x['tel'] = [dict(lugar=(dict(d['carro']['lugar'], st_lg_bono=d['carro'].get('lg_bono', 0), st_lg_apr=d['carro'].get('lg_apr', 0), st_lg_viajes=d['carro'].get('lg_viajes', 0))
                            if isinstance(d.get('carro'), dict) and 'lugar' in d['carro'] else None)) for d in r['linajes']]
    x['estado'] = est; x['oasis_info'] = r['pista'].get('oasis'); x['L'] = r['pista']['L']
    return x, [memoria(cap.ult[i]) for i in range(len(r['linajes']))], r


def carro_de(mod, mem, L):
    c = mod.crea(dict(id='yo', indice=0, L=L, rep_umbral=1.0, rng=np.random.default_rng(0)))
    m = {k: (np.asarray(s, float), int(n)) for k, (s, n) in mem['letras'].items()}
    m['_lugar'] = (np.asarray(mem['lugar'], float), np.asarray(mem['nl'], int))
    c.nace(dict(memoria=m))
    return c


def muerde(c, L, x, k, lev, limpia_apagada):
    """el cuerpo en x - 1, el objeto k en x; -> 1 si en ESTE paso llega a x y decide morder."""
    pos = (x - 1) % L; objs = {x % L: k}
    if limpia_apagada: objs[(x + LEJOS) % L] = 'A'
    a = c.actua(dict(t=0, pos=pos, E=lev[0], Ag=lev[1], objs=objs, cuerpos=(('yo', pos, None, None),), pizarra=()))
    return int(bool(a['muerde']) and (pos + int(a['mov'])) % L == x % L)


def elige(c, L, p, lev):
    """A a +LADO y E a -LADO (las dos dentro): -> 'A', 'E' o '-'."""
    a = c.actua(dict(t=0, pos=p % L, E=lev[0], Ag=lev[1], objs={(p + LADO) % L: 'A', (p - LADO) % L: 'E'}, cuerpos=(('yo', p % L, None, None),), pizarra=()))
    return {1: 'A', -1: 'E'}.get(int(a['mov']), '-')


def pregunta(mods, mem, L, z0):
    """-> {brazo: {clave: fraccion}} sobre rejilla x celdas. Claves: <cond>_<objeto>_<sitio>; cond L = limpia apagada (A a la vista), S = sola."""
    G = [(e, a) for e in NIVELES for a in NIVELES]
    din = [(z0 + o) % L for o in DENTRO_OFF]; dout = [(x + L // 2) % L for x in din]; dgen = [(z0 + 18 + o) % L for o in FUERA_GEN]
    out = {}
    for b, mod in mods.items():
        c = carro_de(mod, mem, L); f = {}
        for cond, lim in (('L', True), ('S', False)):
            for k in ('E', 'A', 'B'):
                for sitio, xs in (('dentro', din), ('fuera', dout)) + ((('fgen', dgen),) if k == 'E' else ()):
                    v = [muerde(c, L, x, k, lev, lim) for x in xs for lev in G]
                    f[f"{cond}_{k}_{sitio}"] = round(sum(v) / len(v), 4)
            f[f"{cond}_D"] = round(f[f"{cond}_E_dentro"] - f[f"{cond}_E_fuera"], 4)
        e = [elige(c, L, z0 + o, lev) for o in ELIGE_OFF for lev in G]
        f['elige_A'] = round(e.count('A') / len(e), 4); f['elige_E'] = round(e.count('E') / len(e), 4)
        out[b] = f
    return out


def mods_pregunta():
    return {b: RC.modulo(n)[0] for b, n in BRAZOS.items()}   # verificados contra construye_c / construye_p1


def linaje_fila(i, l, mem, oi, L, mods):
    ob = oi['bins30']; lg = np.asarray(mem['lugar'], float); ox = (l.get('_oasis') or {}).get('x') or {}
    val = lambda k: ([round(s / mem['letras'][k][1], 4) for s in mem['letras'][k][0]] if k in mem['letras'] else None)
    conoce_E = 'E' in mem['letras']; conoce_A = 'A' in mem['letras']
    recuerda = bool(any((lg[b] > 0.05).any() for b in ob))
    d = dict(i=i, establecido=int(l['fund_post10k'] == 0), cruza=int(l['cruza_real']), conoce_E=int(conoce_E), conoce_A=int(conoce_A), recuerda_oasis=int(recuerda),
             mord_E=ox.get('mord'), mord_E_dentro=ox.get('mord_dentro'), n_E=(mem['letras']['E'][1] if conoce_E else 0),
             v_E=val('E'), v_A=val('A'), v_C=val('C'), v_B=val('B'), bono_oasis=[[round(float(z), 4) for z in lg[b]] for b in ob],
             bins_con_bono=[int(b) for b in range(len(lg)) if (lg[b] > 0.05).any()],
             valido=int(conoce_E and conoce_A and recuerda and (ox.get('mord_dentro') or 0) == 0))
    d['resp'] = pregunta(mods, mem, L, oi['z0'])
    return d


def trabajo(i, seed, T, carpeta, mundo, mods):
    fin = os.path.join(carpeta, f"prueba_i{i:02d}_cria.json"); t0 = time.time()
    try:
        x, mems, r = cria(seed, T, mundo)
        oi = x['oasis_info']; L = x['L']
        x2 = dict(tipo='prueba', i=i, brazo='cria', aborto=None, **CO.fila(x, T))
        x2['oasis_info'] = {k: oi.get(k) for k in ('z0', 'W', 'bins30', 'letra_x', 'efecto_x', 'p_x', 'retenida', 'ret_n', 'comp_dentro', 'comp_fuera')}
        x2['L'] = L; x2['memorias'] = mems
        x2['linajes_s2'] = [linaje_fila(j, l, mems[j], oi, L, mods) for j, l in enumerate(x['linajes'])]
        x2['E_dentro_fisica'] = dict(comp=oi['comp_dentro'].get('E'), mordidas=sum((d['mord_E_dentro'] or 0) for d in x2['linajes_s2']))
    except BaseException as e:   # noqa: nube-9
        x2 = dict(tipo='prueba', i=i, brazo='cria', aborto=f"{type(e).__name__}: {e}"[:300])
    x2['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x2, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x2


CLAVES = ('L_E_dentro', 'L_E_fuera', 'L_E_fgen', 'L_D', 'L_A_dentro', 'L_A_fuera', 'L_B_dentro', 'L_B_fuera', 'S_E_dentro', 'S_E_fuera', 'S_D', 'S_B_dentro', 'elige_A', 'elige_E')


def resume(carpeta):
    X = []; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_cria.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"i{d['i']}: {d['aborto']}"); continue
        X.append(d)
    lin = [dict(l, corrida=x['i']) for x in X for l in x['linajes_s2']]
    out = dict(corridas=len(X), linajes=len(lin), validos=sum(l['valido'] for l in lin), establecidos=sum(l['establecido'] for l in lin),
               validos_y_establecidos=sum(l['valido'] and l['establecido'] for l in lin), conocen_E=sum(l['conoce_E'] for l in lin), recuerdan_oasis=sum(l['recuerda_oasis'] for l in lin),
               mordidas_E_dentro_crianza=sum(x['E_dentro_fisica']['mordidas'] for x in X), E_dentro_composicion=[x['E_dentro_fisica']['comp'] for x in X],
               E_retenidas=[x['oasis_info'].get('ret_n') for x in X], cruzan=sum(x['cruzan'] for x in X), vida_med=med([x['vida_med'] for x in X]),
               mundo_AC=med([x['mundo_AC'] for x in X]))
    for nombre, sel in (('validos', [l for l in lin if l['valido']]), ('validos_establecidos', [l for l in lin if l['valido'] and l['establecido']]), ('todos', lin)):
        t = {}
        for b in BRAZOS:
            if not sel: t[b] = None; continue
            D = [l['resp'][b]['L_D'] for l in sel]
            t[b] = dict(n=len(sel), **{k: round(st.mean(l['resp'][b][k] for l in sel), 4) for k in CLAVES},
                        L_D_mediana=round(st.median(D), 4), L_D_ge06=round(sum(d >= 0.6 for d in D) / len(D), 4), L_D_le_m03=round(sum(d <= -0.3 for d in D) / len(D), 4),
                        L_D_cero_exacto=int(all(d == 0 for d in D)), L_D_por_corrida={str(x['i']): round(st.mean([l['resp'][b]['L_D'] for l in sel if l['corrida'] == x['i']] or [float('nan')]), 3) for x in X})
        out[nombre] = t
    return out, ab


def identidad(log, seed=SEM['arnes'], T=1500):
    N = lambda x: json.loads(json.dumps(x, default=str))
    lug, _ = RC.modulo('O1_LUGAR'); mods = mods_pregunta(); c0, _ = RC.modulo('O1_LUGAR_COMP0')
    kw0 = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **CO.MUNDO_OASIS)
    kwE = dict(kw0, letra_x='E', efecto_x=(0.3, -0.1), p_x=0.15)
    R = {}; MR.RETENIDA[0] = 0
    b0 = N(MC.run(seed, [('X', lug)] * 9, **kw0)); bE = N(MC.run(seed, [('X', lug)] * 9, **kwE))
    R['M1 mundo_ret apagado, sin letra == mundo_tramo_c'] = N(MR.run(seed, [('X', lug)] * 9, **kw0)) == b0
    R['M2 mundo_ret apagado, con E == mundo_tramo_c con E'] = N(MR.run(seed, [('X', lug)] * 9, **kwE)) == bE
    MR.RETENIDA[0] = 1; cap = Capta(lug)
    r1 = MR.run(seed, [('X', lug)] * 9, **kwE); n1 = N(r1); r2 = MR.run(seed, [('X', cap)] * 9, **kwE); MR.RETENIDA[0] = 0
    R['E1 retenida ENCIENDE (difiere de apagado)'] = n1 != bE
    R['M3 con el envoltorio Capta == sin el (salida ENTERA)'] = N(r2) == n1
    oi = r1['pista']['oasis']
    R['F1 fisica: E nunca estuvo dentro (composicion dentro = 0) y hubo re-sorteos'] = oi['comp_dentro']['E'] == 0 and oi['ret_n'] > 0 and oi['comp_fuera']['E'] > 0
    R['F2 fisica: 0 mordidas de E dentro en todos los linajes'] = all(d['_carrera']['oasis']['x']['mord_dentro'] == 0 for d in r1['linajes'])
    mems = [memoria(cap.ult[i]) for i in range(9)]; L = r1['pista']['L']; z0 = oi['z0']
    R['M4 la memoria captada == la salida del carro (tabla y lugar, a 3 decimales)'] = all(
        {k: [round(s / n, 3) for s in su] for k, (su, n) in mems[i]['letras'].items()} == r2['linajes'][i]['carro']['tabla']
        and [[round(z, 3) for z in f] for f in mems[i]['lugar']] == r2['linajes'][i]['carro']['lugar']['mem'] for i in range(9))
    mj = json.loads(json.dumps(mems))
    R['M5 la memoria pasa por JSON sin perder un bit'] = mj == mems
    ok5 = True
    for i in range(9):
        c = carro_de(lug, mj[i], L); o = cap.ult[i]
        ok5 &= set(c.n) == set(o.n) and all(c.n[k] == o.n[k] and (c.suma[k] == o.suma[k]).all() for k in o.n) and (c.lugar == o.lugar).all() and (c.nl == o.nl).all()
    R['M6 nace(memoria) reconstruye suma, n, lugar y nl bit a bit'] = bool(ok5)
    q1 = [pregunta(mods, mj[i], L, z0) for i in range(9)]; q2 = [pregunta(mods, mj[i], L, z0) for i in range(9)]
    R['R1 la pregunta es determinista'] = q1 == q2
    c = carro_de(mods['comp'], mj[0], L); antes = memoria(c)
    for x in range(0, L, 7): muerde(c, L, x, 'E', (0.5, 0.9), True); muerde(c, L, x, 'B', (0.9, 0.5), False); elige(c, L, x, (0.5, 0.5))
    R['M7 preguntar NO cambia la memoria (sin resultado())'] = memoria(c) == antes
    R['M8 en la pregunta, COMP0 (promotor 0) == O1_LUGAR'] = all(pregunta({'lug': c0}, mj[i], L, z0) == {'lug': q1[i]['lug']} for i in range(9))
    R['E2 en la pregunta los tres brazos NO son identicos (hay al menos un linaje con respuestas distintas)'] = any(q['comp'] != q['lug'] or q['compbar'] != q['lug'] for q in q1)
    ok = all(R.values())
    for k, v in R.items(): log(f"  {'OK   ' if v else 'FALLA'} {k}")
    log(f"  (T {T}: E retenidas {oi['ret_n']} · E fuera {oi['comp_fuera']['E']} · linajes que conocen E {sum('E' in m['letras'] for m in mems)}/9)")
    log(f"  ARNES SONDA 2: {sum(R.values())}/{len(R)} {'TODO OK' if ok else 'FALLA'} (s {seed}, T {T})")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--identidad', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--T', type=int, default=60000); ap.add_argument('--n', type=int, default=6); ap.add_argument('--p_x', type=float, default=None)
    ap.add_argument('--desde', type=int, default=SEM['humo']); ap.add_argument('--nota', default='')
    a = ap.parse_args(argv)
    if a.lee:
        res, ab = resume(os.path.abspath(a.lee)); print(json.dumps(res, ensure_ascii=False, indent=1)); print(f"abortos {ab}"); return 0
    BUF = []; LOGF = [None]

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    t0 = time.time()
    log(f"CORRE_S2 (sonda 2: componer con celda retenida) · python {platform.python_version()} · un proceso · corre_s2.py {h16(os.path.abspath(__file__))}")
    ok = CO.verifica(log)
    for nm, b in RC.CC.todas().items():
        if nm in BRAZOS.values() or nm == 'O1_LUGAR_COMP0':
            igual = open(RC.CARROS[nm], 'rb').read() == b; ok &= igual; log(f"  carro {nm} == construye_c: {igual} (sha {h16(RC.CARROS[nm])})")
    log(f"  mundo_ret: {MR.construye()[1]} · mundo_ret.py {h16(os.path.join(AQUI, 'mundo_ret.py'))}")
    ok &= CO.identidad_corta(log); ok &= RC.identidad_corta_c(log); ok &= identidad(log)
    if a.identidad or not ok:
        if not ok: log("  ALGO FALLA -> no se corre.")
        return 0 if ok else 1
    if a.n > MAX_CORRIDAS_1P or a.T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas y <= {MAX_PASOS_1P} pasos")
    mundo = dict(MUNDO)
    if a.p_x is not None: mundo['p_x'] = a.p_x
    sel = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 's2_humo', f"humo_s{a.desde}-{a.desde + a.n - 1}_T{a.T}_{sel}")
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    log(f"  semillas {a.desde}-{a.desde + a.n - 1} · T {a.T} · cria O1_LUGAR · mundo {mundo} + retenida 1 · nota {a.nota!r} · carpeta {carpeta}")
    mods = mods_pregunta()
    for i in range(a.n):
        x = trabajo(i, a.desde + i, a.T, carpeta, mundo, mods)
        if x.get('aborto'): log(f"  i{i} ABORTO {x['aborto']}"); continue
        ls = x['linajes_s2']; v = [l for l in ls if l['valido']]
        m = lambda b, k: (round(st.mean(l['resp'][b][k] for l in v), 3) if v else None)
        log(f"  [{time.time()-t0:7.1f}s] i{i} ({x['seg']}s) cruzan {x['cruzan']}/9 estab {sum(l['establecido'] for l in ls)} vida {x['vida_med']} mundo AC {x['mundo_AC']} · E dentro (fisica) {x['E_dentro_fisica']} · "
            f"retenidas {x['oasis_info'].get('ret_n')} · validos {len(v)}/9 · limpia E dentro/fuera/D: " + ' · '.join(f"{b} {m(b, 'L_E_dentro')}/{m(b, 'L_E_fuera')}/{m(b, 'L_D')}" for b in BRAZOS))
    res, ab = resume(carpeta)
    log("\n================ RESUMEN (humo: NO cuenta, no se declara)")
    log(f"  {({k: v for k, v in res.items() if k not in ('validos', 'validos_establecidos', 'todos')})} · validos {res['validos'] and next(iter(res['validos'].values()))['n']}")
    for nombre in ('validos', 'validos_establecidos', 'todos'):
        for b, v in (res[nombre] or {}).items(): log(f"  [{nombre}] {b:8s} {v}")
    with open(os.path.join(carpeta, 'resumen.json'), 'w', encoding='utf-8') as fh:
        json.dump(dict(sonda=2, resumen=res, abortos=ab, n=a.n, T=a.T, semillas=[a.desde, a.desde + a.n - 1], mundo={k: (list(v) if isinstance(v, tuple) else v) for k, v in mundo.items()},
                       retenida=1, brazos=BRAZOS, niveles=NIVELES, nota=a.nota, sha_runner=h16(os.path.abspath(__file__)), sha_mundo_ret=h16(os.path.join(AQUI, 'mundo_ret.py')),
                       carros={n: h16(RC.CARROS[n]) if n in RC.CARROS else h16(os.path.join(ESC, 'carros', n + '.py')) for n in BRAZOS.values()},
                       mundo_ret=MR.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"  RESUMEN {os.path.join(carpeta, 'resumen.json')} · abortos {len(ab)} · {time.time()-t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
