"""corre_bloques.py — runner EXPLORATORIO de BLOQUES (Opus M, 28-sep-2026, canal experimentos/organelos/bloques/CANAL.md).

Mision: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros, y solo con seleccion natural.

Base: ECO con hijos ingenuos (eco_sel_ing). Se IMPORTA experimentos/organelos/eco_sel_ing/nucleo_eco_sel_ing.py (sha c2189f9d22b72386,
sin tocarlo): trabajo(), K, K_nac, fund_2a, vivero permanente, 90 fundadores, w90. Lo unico que cambia: el gemelo enchufado en CR.ME
es motor_bloques (construido por anclas desde frio/motor_frio_rapido.py) y la configuracion de reglas por brazo.
Brazos (todos: carro FABRICA_ECO, t_corte = T):
  ING_F1     MUT0,    sin reglas (base)            | ING_SEL_C  CEREBRO (15 genes), sin reglas (referencia)
  BLOQ       MUT0,    reglas heredables (padre)    | BLOQ_AZA   MUT0, reglas SIN herencia (cada cuerpo nuevo: entrada al azar del
  BLOQ_C     CEREBRO + reglas heredables           |            banco de listas NUEVAS, mutada; misma tasa de operadores)
Uso (un proceso cada llamada; sin Pool):
  python corre_bloques.py --humo                                  # 48495, T 200 000, BLOQ y BLOQ_AZA (2 corridas); escribe JSON
  python corre_bloques.py --explora --semillas 48401,48402 --brazos BLOQ,BLOQ_AZA --T 200000 --carpeta <nombre>
  python corre_bloques.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, os, sys, time, types
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(os.path.dirname(AQUI))
ING_DIR = os.path.join(ORG, 'eco_sel_ing')
for _d in (ING_DIR, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
import nucleo_eco_sel_ing as NS   # noqa: E402  (importa corre_eco_v12, deja CR.ME = motor Python)

SHAS = {os.path.join(ING_DIR, 'nucleo_eco_sel_ing.py'): 'c2189f9d22b72386',
        os.path.join(ORG, 'frio', 'motor_frio_rapido.py'): 'ff9d890a5cce9dec',
        os.path.join(AQUI, 'motor_bloques.py'): 'ff782697e54585a5'}
DATOS = os.path.join(AQUI, 'datos')
FAB = NS.FAB
NS.BRAZOS.update({'BLOQ': ('MUT0', FAB, None), 'BLOQ_AZA': ('MUT0', FAB, None), 'BLOQ_C': ('CEREBRO', FAB, None)})
BQ = {'ING_F1': dict(on=0), 'ING_SEL_C': dict(on=0), 'ING_AZA_C': dict(on=0),
      'BLOQ': dict(on=1, donante='padre'), 'BLOQ_AZA': dict(on=1, donante='azar'), 'BLOQ_C': dict(on=1, donante='padre')}
DEF = dict(on=0, donante='padre', p_campo=0.10, p_dup=0.02, p_ins=0.02, p_hgt=0.01, p_del=0.05, banco=200, inicial=None, forzada=None)
HUMO = dict(semilla=48495, T=200000, brazos=('BLOQ', 'BLOQ_AZA'))
SEM_EXPLORA = (48401, 48402, 48403, 48404, 48405, 48406, 48407, 48408, 48409, 48410)   # 48406-48410: mini-replica declarada 19:36
MUNDO_ULT = {}
# VIVERO FINITO (anadido a las 19:29, ANTES de correrlo, tras ver la exploracion): t_corte = 100 000, sin subsidio de fundadores despues
for _b, _g in (('ING_F1', 'MUT0'), ('ING_SEL_C', 'CEREBRO'), ('BLOQ', 'MUT0'), ('BLOQ_AZA', 'MUT0'), ('BLOQ_C', 'CEREBRO')):
    NS.BRAZOS[_b + '_V'] = (_g, FAB, 100000)
BQ.update({'ING_F1_V': dict(on=0), 'ING_SEL_C_V': dict(on=0), 'BLOQ_V': dict(on=1, donante='padre'),
           'BLOQ_AZA_V': dict(on=1, donante='azar'), 'BLOQ_C_V': dict(on=1, donante='padre')})
# FORZ_V (anadido 19:41, antes de correrlo): REFERENCIA DISENADA POR NOSOTROS, no evolucion: los 90 fundadores con el instinto a mano
# "pixel 4 del foco > 0.5 -> boca -3", tasas 0 (se hereda intacto). Pregunta: el organo que armo la seleccion rinde lo que el disenado?
NS.BRAZOS['FORZ_V'] = ('MUT0', FAB, 100000)
# FORZ2_V (anadido 19:43, antes de correrlo): el genoma EVOLUCIONADO del linaje 66 de BLOQ_V s48402 trasplantado a mano (dos copias de
# "pixel 1 del foco < 0.06 -> boca -2.97"), tasas 0. Separa 'el contenido de la regla (peso y duplicacion)' de 'la evolucion que sigue'.
NS.BRAZOS['FORZ2_V'] = ('MUT0', FAB, 100000)
BQ['FORZ2_V'] = dict(on=1, donante='padre', p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0,
                     forzada=[[3, 1, 0, 0.06, 0, -2.97], [3, 1, 0, 0.06, 0, -2.97]])
# FORZ3_V (anadido 19:44, antes de correrlo): MI regla (pixel 4 > 0.5 -> boca -3) DUPLICADA (2 copias), tasas 0: la duplicacion como
# volumen (cada peso esta recortado a |3|; dos copias suman -6).
NS.BRAZOS['FORZ3_V'] = ('MUT0', FAB, 100000)
BQ['FORZ3_V'] = dict(on=1, donante='padre', p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0,
                     forzada=[[3, 4, 1, 0.5, 0, -3.0], [3, 4, 1, 0.5, 0, -3.0]])
BQ['FORZ_V'] = dict(on=1, donante='padre', p_campo=0, p_dup=0, p_ins=0, p_hgt=0, p_del=0, forzada=[[3, 4, 1, 0.5, 0, -3.0]])
SENT = ['hambre', 'sed', 'cerca', 'pixF', 'pixM', 'Rult']
ACC = ['boca', 'hacia', 'quieto', 'parir']


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica():
    for p, h in SHAS.items():
        if h16(p) != h: raise SystemExit(f'{os.path.relpath(p, ORG)} cambio: {h16(p)} != {h}')


def usa_bloques():
    """Como NS.usa_gemelo, pero con motor_bloques."""
    import motor_bloques as MB
    g = types.ModuleType('motor_bloques_gemelo')
    g.__dict__.update({k: v for k, v in NS.ME_PY.__dict__.items() if not k.startswith('__')})
    def _rs(*a, **k):   # misma llamada; solo guarda la composicion del mundo de la ultima corrida (diagnostico, no cambia nada)
        r = MB.run_solapadas(*a, **k); P = r['pista']
        MUNDO_ULT.clear(); MUNDO_ULT.update(comp_mundo=P['comp_mundo'], nobj_medio=P['nobj_medio'], llegadas=P['llegadas'],
                                            perdidas=P['llegadas_perdidas'])
        return r
    g.run_solapadas = _rs
    g._MF = MB
    NS.CR.ME = g
    return MB


def corre(seed, brazo, T, carpeta, extra=None, reanuda=False):
    fn = os.path.join(carpeta, f'M_{brazo}_s{seed}.json')
    if reanuda and os.path.exists(fn): return json.load(open(fn, encoding='utf-8'))
    MB = usa_bloques()
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(DEF); MB.BQ_CFG.update(BQ[brazo]); MB.BQ_CFG.update(extra or {})
    os.makedirs(carpeta, exist_ok=True)
    res = NS.trabajo((seed, brazo, T, NS.tc_de(brazo, T), NS.FRIO['T_lect'], carpeta, bool(reanuda)))
    out = dict(K=NS_kbar(res), K_nac=res.get('K_nac'), fund_2a=res.get('fund_2a'), persiste=res.get('persiste'),
               bloqueados=res.get('bloqueados'), aborto=res.get('aborto'), seg=res.get('seg'), n_nac=res.get('n_nac'),
               n_refund=res.get('n_refund'), genes_vivos_T=res.get('genes_vivos_T'), causas_2a=res.get('causas_2a'),
               vida_media_muertos_2a=res.get('vida_media_muertos_2a'), nac_2a=res.get('nac_2a'))
    out['mundo'] = dict(MUNDO_ULT); out['t_ext'] = res.get('t_ext'); out['K_fund'] = res.get('K_fund')
    out.update(carro=res.get('carro'), t_corte=res.get('t_corte'), genetica=res.get('genetica'), motor=res.get('motor'))
    out['bloques'] = json.loads(json.dumps(MB.BQ_OUT, default=float)) if MB.BQ_CFG.get('on') else None
    out['frac_rechazo'] = frac_rechazo(out)
    out = dict(seed=seed, brazo=brazo, T=T, **out)
    with open(fn + '.tmp', 'w', encoding='utf-8') as f: json.dump(out, f)
    os.replace(fn + '.tmp', fn)
    return out


def NS_kbar(res):
    """K = media de tam_total en [T/2, T] (la expresion de corre_eco_sel.kbar: tam_total muestreado cada MUNDO['muestra'])."""
    tt = res.get('tam_total')
    if not tt: return None
    m = NS.MUNDO['muestra']; T = res['T']; n = T // m + 1; i0 = (T // 2) // m   # copia de corre_eco_sel_ing.kbar
    v = (list(tt) + [0] * max(0, n - len(tt)))[i0:n]
    return float(np.mean(v))


def tipo(r):
    """La 'forma' de una regla: sentido(parametro) comparador accion signo."""
    s, p, c, th, a, w = r
    s = int(s); a = int(a)
    sen = SENT[s] + (f'{int(p)}' if s in (3, 4) else '')
    return f"{sen}{'>' if c > 0.5 else '<'}{'θ'} -> {ACC[a]}{'+' if w > 0 else '-'}"


PATM = {'A': (1, 1, 0, 1, 0, 0), 'B': (1, 0, 1, 0, 1, 0), 'C': (0, 1, 1, 0, 0, 1), 'D': (0, 0, 1, 0, 1, 1)}   # pista2.cfg_fabrica PAT


def rechazo(r):
    """La regla es el ORGANO DE RECHAZO si es de boca con w < 0 sobre el pixel del foco y su condicion se cumple EXACTAMENTE en B y D
    (veneno, sal) y no en A ni C (comida, agua)."""
    s, p, c, th, a, w = r
    if int(s) != 3 or int(a) != 0 or w >= 0: return False
    cum = {x: ((PATM[x][int(p)] > th) if c > 0.5 else (PATM[x][int(p)] < th)) for x in 'ABCD'}
    return cum['B'] and cum['D'] and not cum['A'] and not cum['C']


def frac_rechazo(d):
    vv = (d.get('bloques') or {}).get('vivos_T') or []
    return (sum(any(rechazo(r) for r in x[3]) for x in vv) / len(vv)) if vv else None


def lee(carpeta):
    fs = sorted(glob.glob(os.path.join(carpeta, 'M_*.json')))
    D = {}
    for f in fs:
        d = json.load(open(f, encoding='utf-8')); D.setdefault(d['brazo'], {})[d['seed']] = d
    br = list(D)
    print(f'carpeta {carpeta}: brazos {br}')
    print('persiste: ' + ' · '.join(f"{b} {sum(1 for d in D[b].values() if d.get('persiste'))}/{len(D[b])}" for b in br))
    print(f"{'brazo':10s} {'n':>2s} {'K med':>8s} {'K_nac med':>9s} {'fund_2a med':>11s} {'largo T':>8s} {'con regla':>9s}")
    for b in br:
        v = list(D[b].values())
        lar = [np.mean([len(x[3]) for x in d['bloques']['vivos_T']]) for d in v if d.get('bloques') and d['bloques'].get('vivos_T')]
        con = [np.mean([len(x[3]) > 0 for x in d['bloques']['vivos_T']]) for d in v if d.get('bloques') and d['bloques'].get('vivos_T')]
        print(f"{b:10s} {len(v):2d} {np.median([d['K'] for d in v]):8.2f} {np.median([d['K_nac'] for d in v]):9.2f} "
              f"{np.median([d['fund_2a'] for d in v]):11.0f} {(np.median(lar) if lar else float('nan')):8.2f} "
              f"{(np.median(con) if con else float('nan')):9.2f}")
    for b in br:
        fr = [(s, frac_rechazo(D[b][s]), D[b][s].get('persiste')) for s in sorted(D[b]) if D[b][s].get('bloques')]
        if fr: print(f'  organo de rechazo (fraccion de vivos en T) {b}: ' + ' '.join(f's{s}:{"-" if f is None else round(f, 2)}(pers {p_})' for s, f, p_ in fr))
    for a, b in (('BLOQ_V', 'ING_SEL_C_V'), ('BLOQ_V', 'BLOQ_AZA_V'), ('BLOQ_V', 'ING_F1_V'), ('ING_SEL_C_V', 'ING_F1_V'),
                 ('BLOQ', 'ING_SEL_C'), ('BLOQ', 'BLOQ_AZA'), ('BLOQ', 'ING_F1'), ('BLOQ_C', 'ING_SEL_C'), ('ING_SEL_C', 'ING_F1'),
                 ('BLOQ_AZA', 'ING_F1')):
        if a in D and b in D:
            ss = sorted(set(D[a]) & set(D[b]))
            for m in ('K', 'K_nac', 'fund_2a'):
                dd = [D[a][s][m] - D[b][s][m] for s in ss]
                print(f'  {a} - {b} [{m}]: {sum(x > 0 for x in dd)}/{len(dd)} > 0, mediana {np.median(dd):+.2f}  ({[round(x, 2) for x in dd]})')
    for b in br:
        v = [D[b][s] for s in sorted(D[b])]
        if not v[0].get('bloques'): continue
        print(f'--- {b}: reglas (forma) presentes en >= 30 % de los vivos en T, por semilla; operadores')
        for d in v:
            B = d['bloques']; vv = B.get('vivos_T') or []
            cnt = {}
            for x in vv:
                for t_ in set(tipo(r) for r in x[3]): cnt[t_] = cnt.get(t_, 0) + 1
            top = sorted(((c / max(1, len(vv)), t_) for t_, c in cnt.items()), reverse=True)
            s = d['seed']; ser = B['serie']
            lt = [(x[0], x[2]) for x in ser if x[0] % 40000 == 0]
            print(f"  s{s}: vivos {len(vv)} · largo medio en t {lt} · ops hijos {B['n_hijos']} fund {B['n_fund']} ins {B['n_ins']} "
                  f"dup {B['n_dup']} del {B['n_del']} hgt {B['n_hgt']} campo {B['n_campo']} tope {B['n_tope']} igual_padre {B['n_igual_padre']}")
            print('     ' + ' | '.join(f'{t_} {f:.2f}' for f, t_ in top if f >= 0.30))
            por = {}
            for x in vv: por.setdefault(x[0], []).append(x)
            gr = sorted(por.items(), key=lambda z: -len(z[1]))[:3]
            for lin, xs in gr:   # los linajes que prosperan: los de mas cuerpos vivos en T; la lista del cuerpo de mayor generacion
                x = max(xs, key=lambda z: z[1])
                print(f'     linaje {lin}: {len(xs)} vivos, gen max {x[1]}: ' + ' ; '.join(
                    f"{tipo(r)}(θ {r[3]:.2f}, w {r[5]:+.2f})" for r in x[3]))
    return D


# ================================================================ SERIE CONFIRMATORIA (PREREGISTRO_bloques.md §10; escrita ANTES de la serie)
SERIE_BR = ('BLOQ_V', 'ING_SEL_C_V', 'BLOQ_AZA_V', 'ING_F1_V')   # orden de lanzamiento: los caros primero
VENTANAS = (48411, 48431)   # serie y replica, 20 semillas cada una
N_SERIE = 20
T_SERIE = 500000             # fijado en §10 (19:51) tras medir el costo: BLOQ_V 63.5 s, ING_SEL_C_V 43.7 s a T 500 000 (48496)
T_CORTE = 100000
CFG_ESPERADA = {'BLOQ_V': (1, 'padre'), 'BLOQ_AZA_V': (1, 'azar'), 'ING_SEL_C_V': (0, None), 'ING_F1_V': (0, None)}


def veredicto(D, T, n=N_SERIE):
    """La LETRA de §10. D[brazo][seed] = el dict de corre(). Devuelve (veredicto, lineas)."""
    L = []
    ss = sorted(set.intersection(*[set(D.get(b, {})) for b in SERIE_BR])) if all(b in D for b in SERIE_BR) else []
    todo = [D[b][s] for b in SERIE_BR for s in ss]
    v0 = (n == N_SERIE and len(ss) == n and all(len(D[b]) == n for b in SERIE_BR) and all(x.get('T') == T for x in todo)
          and all(x.get('t_corte') == T_CORTE for x in todo) and all(x.get('aborto') is None for x in todo)
          and all(x.get('bloqueados') == 0 for x in todo))

    def cfg_ok(x):
        on, don = CFG_ESPERADA[x['brazo']]; B = x.get('bloques')
        if on == 0: return B is None
        return B is not None and B['cfg'].get('on') == 1 and B['cfg'].get('donante') == don
    v2 = bool(todo) and all(x.get('carro') == FAB for x in todo) and all(cfg_ok(x) for x in todo)
    pers = {b: sum(1 for s in ss if D[b][s].get('persiste')) for b in SERIE_BR} if ss else {}
    v1 = pers.get('ING_F1_V', 99) <= 3
    L.append(f"V0 serie completa ({N_SERIE} semillas x 4 brazos, T {T}, t_corte {T_CORTE}, sin abortos, bloqueados 0): {'SE CUMPLE' if v0 else 'NO SE CUMPLE'}")
    L.append(f"V1 la base sin vivero muere (ING_F1_V persiste <= 3/20): {'SE CUMPLE' if v1 else 'NO SE CUMPLE'} ({pers.get('ING_F1_V')})")
    L.append(f"V2 carro FABRICA_ECO y reglas declaradas por brazo: {'SE CUMPLE' if v2 else 'NO SE CUMPLE'}")
    L.append(f"persiste: {pers}")
    if not (v0 and v1 and v2):
        L.append('VEREDICTO (una serie): NO EVALUABLE'); return 'NO EVALUABLE', L
    K = lambda b, s: D[b][s]['K']
    p1 = pers['BLOQ_V'] >= 17
    d2 = [K('BLOQ_V', s) - K('ING_SEL_C_V', s) for s in ss]
    p2 = sum(x > 0 for x in d2) >= 15 and float(np.median(d2)) >= 10.0
    d3 = [K('BLOQ_V', s) - K('BLOQ_AZA_V', s) for s in ss]
    p3 = sum(x > 0 for x in d3) >= 15 and pers['BLOQ_AZA_V'] <= 5
    fr = [D['BLOQ_V'][s].get('frac_rechazo') for s in ss]
    n4 = sum(1 for f in fr if f is not None and f >= 0.5)
    p4 = n4 >= 12
    L.append(f"P1 BLOQ_V persiste >= 17/20: {'SE CUMPLE' if p1 else 'NO SE CUMPLE'} ({pers['BLOQ_V']})")
    L.append(f"P2 K(BLOQ_V) > K(ING_SEL_C_V) pareado >= 15/20 y mediana >= +10: {'SE CUMPLE' if p2 else 'NO SE CUMPLE'} "
             f"({sum(x > 0 for x in d2)}/20, mediana {np.median(d2):+.2f})")
    L.append(f"P3 K(BLOQ_V) > K(BLOQ_AZA_V) pareado >= 15/20 y BLOQ_AZA_V persiste <= 5/20: {'SE CUMPLE' if p3 else 'NO SE CUMPLE'} "
             f"({sum(x > 0 for x in d3)}/20, mediana {np.median(d3):+.2f}; AZA persiste {pers['BLOQ_AZA_V']})")
    L.append(f"P4 organo de rechazo (boca w<0 que separa exacto B,D de A,C) en >= 50 % de los vivos en T en >= 12/20 semillas de BLOQ_V: "
             f"{'SE CUMPLE' if p4 else 'NO SE CUMPLE'} ({n4}/20)")
    if p1 and p2 and p3 and p4: v = 'FUNCIONA'
    elif p3 and (p1 or p2): v = 'MODESTO'   # el control pasa y pasa al menos una de P1 (persistencia) o P2 (techo)
    else: v = 'NO'
    L.append(f'VEREDICTO (una serie): {v}')
    return v, L


def _job(a):
    seed, brazo, T, car, rean = a
    t0 = time.time()
    try:
        o = corre(seed, brazo, T, car, reanuda=rean)
    except KeyboardInterrupt:
        raise
    except BaseException as ex:   # nunca matar al trabajador del Pool: la serie queda NO EVALUABLE por V0
        o = dict(seed=seed, brazo=brazo, T=T, aborto=f'{type(ex).__name__}: {ex}', K=None, persiste=None, bloqueados=None)
    return seed, brazo, o, round(time.time() - t0, 1)


def serie(desde, n, pool, T, rean):
    from multiprocessing import Pool
    car = os.path.join(DATOS, f'serie_s{desde}-{desde + n - 1}_T{T}')
    os.makedirs(car, exist_ok=True)
    jobs = [(s, b, T, car, rean) for b in SERIE_BR for s in range(desde, desde + n)]
    t0 = time.time(); D = {}
    with Pool(pool) as P:
        for k, (s, b, o, seg) in enumerate(P.imap_unordered(_job, jobs), 1):
            D.setdefault(b, {})[s] = o
            print(f"[{time.strftime('%H:%M:%S')}] [{k}/{len(jobs)}] {b} s{s}: K {o.get('K')} · persiste {o.get('persiste')} · "
                  f"rechazo {o.get('frac_rechazo')} · aborto {o.get('aborto')} ({seg} s; {time.time() - t0:.0f} s)", flush=True)
    v, L = veredicto(D, T, n)
    for x in L: print(x, flush=True)
    with open(os.path.join(car, 'VEREDICTO.json'), 'w', encoding='utf-8') as f:
        json.dump(dict(veredicto=v, lineas=L, T=T, desde=desde, n=n, shas={os.path.basename(p_): h16(p_) for p_ in SHAS}), f, indent=1)


def lee_serie(car, T):
    D = {}
    for f in glob.glob(os.path.join(car, 'M_*.json')):
        d = json.load(open(f, encoding='utf-8')); D.setdefault(d['brazo'], {})[d['seed']] = d
    v, L = veredicto(D, T)
    for x in L: print(x)
    return v


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--explora', action='store_true')
    ap.add_argument('--semillas', default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--carpeta', default=None); ap.add_argument('--lee', default=None)
    ap.add_argument('--serie', action='store_true'); ap.add_argument('--desde', type=int, default=None); ap.add_argument('--n', type=int, default=None)
    ap.add_argument('--pool', type=int, default=None); ap.add_argument('--reanuda', action='store_true')
    a, resto = ap.parse_known_args()
    if resto: raise SystemExit(f'banderas desconocidas: {resto}')
    if a.serie:   # SOLO el coordinador
        if a.desde not in VENTANAS or a.n != N_SERIE or a.T != T_SERIE or not a.pool or a.pool < 1:
            raise SystemExit(f'--serie exige --desde en {VENTANAS}, --n {N_SERIE}, --T {T_SERIE} y --pool')
        verifica(); serie(a.desde, a.n, a.pool, a.T, a.reanuda); return
    if a.T is None: a.T = 200000
    if a.lee: lee(a.lee if os.path.isabs(a.lee) else os.path.join(DATOS, a.lee)); return
    if a.T > 200000: raise SystemExit('T > 200 000 no se corre aqui (regla del creador)')
    verifica()
    if a.humo:
        car = os.path.join(DATOS, 'humo'); sem = [HUMO['semilla']]; brs = HUMO['brazos']; T = HUMO['T']
    elif a.explora:
        car = os.path.join(DATOS, a.carpeta or 'explora'); sem = [int(x) for x in a.semillas.split(',')]; brs = a.brazos.split(','); T = a.T
        for s in sem:
            if s not in SEM_EXPLORA and not (48491 <= s <= 48499): raise SystemExit(f'semilla {s} fuera de las declaradas')
    else:
        raise SystemExit('usa --humo, --explora o --lee')
    for b in brs:
        if b not in BQ: raise SystemExit(f'brazo desconocido {b}')
    t0 = time.time()
    for s in sem:
        for b in brs:
            o = corre(s, b, T, car)
            B = o['bloques']
            lar = (round(float(np.mean([len(x[3]) for x in B['vivos_T']])), 2) if B and B.get('vivos_T') else None)
            print(f"[{time.strftime('%H:%M:%S')}] {b} s{s} T{T}: K {o['K']} · K_nac {o['K_nac']} · fund_2a {o['fund_2a']} · persiste "
                  f"{o['persiste']} · aborto {o['aborto']} · largo medio vivos T {lar} ({o['seg']} s; {time.time() - t0:.0f} s)", flush=True)


if __name__ == '__main__':
    main()
