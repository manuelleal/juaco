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
        os.path.join(AQUI, 'motor_bloques.py'): 'ce66d09804660588'}
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


def corre(seed, brazo, T, carpeta, extra=None):
    MB = usa_bloques()
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(DEF); MB.BQ_CFG.update(BQ[brazo]); MB.BQ_CFG.update(extra or {})
    os.makedirs(carpeta, exist_ok=True)
    res = NS.trabajo((seed, brazo, T, NS.tc_de(brazo, T), NS.FRIO['T_lect'], carpeta, False))
    out = dict(K=NS_kbar(res), K_nac=res.get('K_nac'), fund_2a=res.get('fund_2a'), persiste=res.get('persiste'),
               bloqueados=res.get('bloqueados'), aborto=res.get('aborto'), seg=res.get('seg'), n_nac=res.get('n_nac'),
               n_refund=res.get('n_refund'), genes_vivos_T=res.get('genes_vivos_T'), causas_2a=res.get('causas_2a'),
               vida_media_muertos_2a=res.get('vida_media_muertos_2a'), nac_2a=res.get('nac_2a'))
    out['mundo'] = dict(MUNDO_ULT); out['t_ext'] = res.get('t_ext'); out['K_fund'] = res.get('K_fund')
    out['bloques'] = json.loads(json.dumps(MB.BQ_OUT, default=float)) if MB.BQ_CFG.get('on') else None
    fn = os.path.join(carpeta, f'M_{brazo}_s{seed}.json')
    with open(fn + '.tmp', 'w', encoding='utf-8') as f: json.dump(dict(seed=seed, brazo=brazo, T=T, **out), f)
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


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--explora', action='store_true')
    ap.add_argument('--semillas', default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--T', type=int, default=200000); ap.add_argument('--carpeta', default=None); ap.add_argument('--lee', default=None)
    a, resto = ap.parse_known_args()
    if resto: raise SystemExit(f'banderas desconocidas: {resto}')
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
