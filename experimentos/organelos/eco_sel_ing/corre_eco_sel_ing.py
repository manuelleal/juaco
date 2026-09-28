"""corre_eco_sel_ing.py — RUNNER y LETRA de ECO_SEL_ING: la seleccion natural de ECO_SEL con el hijo INGENUO (frente 2; 28-sep-2026).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como.

Preregistro: PREREGISTRO_eco_sel_ing.md (la letra esta AQUI, en veredicto(), y alli, §6).
La corrida es nucleo_eco_sel_ing.trabajo (construido POR ANCLAS desde eco_sel/nucleo_eco_sel.py, sha 6a36e47ce61db3e1): mismo mundo
(ECO w90), misma genetica (CEREBRO / CEREBRO_AZAR / MUT0 de ECO_SEL), misma K. Lo que cambia contra ECO_SEL:
  - el carro: FABRICA_ECO (el hijo NO recibe la tabla de la familia; nace ingenuo, como el fundador de la carrera);
  - el vivero: PERMANENTE (t_corte = T). El linaje ingenuo no persiste en frio (FAB_FRIO de F1, 0/20) ni tras un vivero finito
    (MUT0 de ECO v1.1, 0/20 x2 a 1e6): es la base minima que persiste.
Brazos: ING_F1 (MUT0, sin mutacion) · ING_SEL_C (15 genes del cerebro heredables) · ING_AZA_C (los mismos 15 SIN herencia).

Uso (ERR-115: banderas desconocidas o abreviadas abortan; --help no existe; SOLO el coordinador lanza --serie):
  python experimentos/organelos/eco_sel_ing/corre_eco_sel_ing.py --humo                                            # 1 proceso, 46195, 3 brazos, T 200 000
  python experimentos/organelos/eco_sel_ing/corre_eco_sel_ing.py --serie --desde 46101 --n 20 --pool 6 --T 1000000  # serie
  python experimentos/organelos/eco_sel_ing/corre_eco_sel_ing.py --serie --desde 46121 --n 20 --pool 6 --T 1000000  # replica
  (--T 500000 SOLO si la regla de §10 del preregistro lo fija tras el humo; --reanuda para seguir; --lee <carpeta>)
"""
import argparse, glob, hashlib, json, os, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import nucleo_eco_sel_ing as N      # inserta en sys.path juaco_eco y frio; CR.ME = motor Python hasta usa_gemelo()
CR = N.CR
RAIZ = N.RAIZ
MUNDO = N.MUNDO
ING = N.ING
BASE, SEL, AZA = ING
GENES_C = ('alpha', 'aversion', 'tau_e')   # los tres que la seleccion movio en ECO v1 / v1.1 (brazo CEREBRO, carro FABRICA_ECO)
TS = (1_000_000, 500_000)                  # las dos T admitidas (§10: 5e5 solo si el humo lo exige)
DATOS = os.path.join(AQUI, 'datos')
UMB = dict(V1=17, V3_mut=18, P1_lo=3.5, P1_hi=6.5, P2_n=15, P2_d=1.5, P3_n=15, P4_n=15)   # §6 del preregistro


class BanderaMala(SystemExit):
    pass


def usa_gemelo():
    return N.usa_gemelo()


def trabajo(args):
    return N.trabajo(args)


def kbar(x, T):
    """Capacidad del linaje: media de los cuerpos vivos (tam_total, cada MUESTRA pasos) en [T/2, T]; tras la extincion cuenta 0."""
    tt = x.get('tam_total')
    if tt is None: return None
    m = MUNDO['muestra']; n = T // m + 1; i0 = (T // 2) // m
    v = (list(tt) + [0] * max(0, n - len(tt)))[i0:n]
    return float(np.mean(v))


def rango(x, g, t=None):
    """Rango (1..9; empates a medias) de la media del gen g en el BANCO real entre ella y sus 8 sombras, en la fila de gen_t de t = T_SEL
    (log(g/G0), columnas [6] y [7] de motor_eco._muestra_gen). Sin fila, sin banco o sin sombras: 5.0 (lo que espera la nula)."""
    t = N.T_SEL if t is None else t
    f = next((r for r in (x.get('gen_t') or []) if r[0] == t), None)
    if f is None or len(f) < 8 or f[6] is None or not f[7]: return 5.0
    j = x['genes'].index(g); r = f[6][j]; S = [s[j] for s in f[7]]
    return 1.0 + sum(1 for v in S if v < r) + 0.5 * sum(1 for v in S if v == r)


def _gen_T(x, g):
    gv = x.get('genes_vivos_T')
    return None if not gv or g not in gv else gv[g]


def _par(A, B, ss):
    """(ganadas A > B, mediana de A - B) pareado por semilla."""
    d = [A[s] - B[s] for s in ss if A.get(s) is not None and B.get(s) is not None]
    return sum(1 for z in d if z > 0), (float(np.median(d)) if d else None), len(d)


# ================================================================================ LA LETRA (PREREGISTRO_eco_sel_ing.md §6)
def veredicto(R, n_esperado=20, T_esperado=1_000_000):
    L = []; by = {b: sorted([x for x in R if x['brazo'] == b], key=lambda x: x['seed']) for b in ING}
    otros = sorted({x['brazo'] for x in R} - set(ING))
    n = {b: len(v) for b, v in by.items()}
    pers = {b: sum(int(x.get('persiste') or 0) for x in v) for b, v in by.items()}
    abortos = [(x['brazo'], x['seed'], x.get('aborto')) for x in R if x.get('aborto')]
    tc_mal = [(x['brazo'], x['seed']) for x in R if x.get('t_corte') != T_esperado]
    sem = {b: tuple(x['seed'] for x in v) for b, v in by.items()}
    completo = (all(n[b] == n_esperado for b in ING) and not otros and all(x['T'] == T_esperado for x in R) and not abortos and not tc_mal
                and len({(x['brazo'], x['seed']) for x in R}) == len(R) and len(set(sem.values())) == 1)
    bloq = sum(int(x.get('bloqueados') or 0) for x in R)
    carro_mal = [(x['brazo'], x['seed'], x.get('carro')) for x in R if x.get('carro') != 'FABRICA_ECO']
    K = {b: {x['seed']: kbar(x, T_esperado) for x in v} for b, v in by.items()}
    Kn = {b: {x['seed']: x.get('K_nac') for x in v} for b, v in by.items()}
    F2 = {b: {x['seed']: x.get('fund_2a') for x in v} for b, v in by.items()}
    med = lambda d: (round(float(np.median([z for z in d.values() if z is not None])), 2) if any(z is not None for z in d.values()) else None)
    L.append(f"semillas por brazo: {n}; otros brazos: {otros}; persiste en T = {T_esperado}: {pers}; abortos: {abortos[:5]}; "
             f"t_corte distinto de T (vivero permanente): {tc_mal[:5]}; bloqueados: {bloq}; carro distinto de FABRICA_ECO: {carro_mal[:5]}")
    L.append(f"K (media de cuerpos vivos en [T/2, T]), mediana: { {b: med(K[b]) for b in ING} } · K_nac (solo NACIDOS): "
             f"{ {b: med(Kn[b]) for b in ING} } · fund_2a (fundadores repuestos en la 2a mitad): { {b: med(F2[b]) for b in ING} }")
    esperado = {b: (list(N.GENETICAS[N.BRAZOS[b][0]]['mutables'] or []) if N.GENETICAS[N.BRAZOS[b][0]]['p'] else []) for b in ING}
    v3 = {}
    for b, v in by.items():
        mal_mut = [x['seed'] for x in v if x.get('mutables') is not None and list(x['mutables']) != esperado[b]]
        fuera = [x['seed'] for x in v if (x.get('fuera_mutables') or 0) != 0]
        con_mut = sum(1 for x in v if (x.get('tasa_mut') or 0) > 0)
        ok = not mal_mut and not fuera and (con_mut == 0 if b == BASE else con_mut >= UMB['V3_mut'])
        v3[b] = (ok, mal_mut[:3], fuera[:3], con_mut)
    V1 = pers[BASE] >= UMB['V1']
    V2 = not carro_mal
    L.append(f"V1 la base ingenua esta presente (ING_F1 persiste >= {UMB['V1']}/20): {'SE CUMPLE' if V1 else 'NO'} ({pers[BASE]}) · "
             f"V2 los tres brazos nacen ingenuos (carro FABRICA_ECO): {'SE CUMPLE' if V2 else 'NO'}")
    L.append(f"V3 genetica declarada: { {b: v3[b] for b in ING} }")
    if not completo: base = 'NO EVALUABLE (serie incompleta, abortos, T, t_corte, brazos o semillas distintas)'
    elif bloq > 0: base = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq})'
    elif not V2: base = 'NO EVALUABLE (un brazo no nace ingenuo: carro distinto de FABRICA_ECO)'
    elif not V1: base = 'NO EVALUABLE (la base ingenua no esta presente: ING_F1 < 17/20)'
    elif not (v3[SEL][0] and v3[AZA][0] and v3[BASE][0]): base = 'NO EVALUABLE (la genetica no es la declarada)'
    else: base = None
    rS = {g: (round(float(np.mean([rango(x, g) for x in by[SEL]])), 3) if by[SEL] else None) for g in GENES_C}
    rA = {g: (round(float(np.mean([rango(x, g) for x in by[AZA]])), 3) if by[AZA] else None) for g in GENES_C}
    sale = lambda r: r is not None and (r <= UMB['P1_lo'] or r >= UMB['P1_hi'])
    P1 = any(sale(r) for r in rS.values()); G4 = not any(sale(r) for r in rA.values())
    ss = sorted(set(K[SEL]) & set(K[BASE]) & set(K[AZA]))
    nF, mF, npF = _par(K[SEL], K[BASE], ss); nFn, mFn, _ = _par(Kn[SEL], Kn[BASE], ss)
    nA, mA, npA = _par(K[SEL], K[AZA], ss); nAn, mAn, _ = _par(Kn[SEL], Kn[AZA], ss)
    P2 = nF >= UMB['P2_n'] and mF is not None and mF >= UMB['P2_d'] and nFn >= UMB['P2_n']
    P3 = nA >= UMB['P3_n'] and nAn >= UMB['P3_n']
    # P4 (establecimiento, la palanca de la carrera): menos fundadores repuestos en la 2a mitad
    e4F, m4F, _ = _par({s: -z for s, z in F2[SEL].items() if z is not None}, {s: -z for s, z in F2[BASE].items() if z is not None}, ss)
    e4A, m4A, _ = _par({s: -z for s, z in F2[SEL].items() if z is not None}, {s: -z for s, z in F2[AZA].items() if z is not None}, ss)
    P4F = e4F >= UMB['P4_n']; P4A = e4A >= UMB['P4_n']
    L.append(f"P1 firma contra las 8 sombras en t = {N.T_SEL}: rango medio <= {UMB['P1_lo']} o >= {UMB['P1_hi']} en algun gen de "
             f"{list(GENES_C)} en {SEL}: {'SE CUMPLE' if P1 else 'NO'} ({rS}) · guardia: en {AZA} ningun gen sale: {'SE CUMPLE' if G4 else 'NO'} ({rA})")
    L.append(f"P2 {SEL} > {BASE}: K pareado >= {UMB['P2_n']}/20 y mediana >= +{UMB['P2_d']} Y K_nac pareado >= {UMB['P2_n']}/20: "
             f"{'SE CUMPLE' if P2 else 'NO'} (K {nF}/{npF}, mediana {None if mF is None else round(mF, 2)}; K_nac {nFn}/{npF}, mediana "
             f"{None if mFn is None else round(mFn, 2)})")
    L.append(f"P3 {SEL} > {AZA}: K pareado >= {UMB['P3_n']}/20 Y K_nac pareado >= {UMB['P3_n']}/20: {'SE CUMPLE' if P3 else 'NO'} "
             f"(K {nA}/{npA}, mediana {None if mA is None else round(mA, 2)}; K_nac {nAn}/{npA}, mediana {None if mAn is None else round(mAn, 2)})")
    L.append(f"P4 establecimiento, fund_2a {SEL} < {BASE} pareado >= {UMB['P4_n']}/20: {'SE CUMPLE' if P4F else 'NO'} ({e4F}/{npF}, mediana "
             f"{None if m4F is None else -round(m4F, 1)}) · {SEL} < {AZA}: {'SE CUMPLE' if P4A else 'NO'} ({e4A}/{npA}, mediana "
             f"{None if m4A is None else -round(m4A, 1)})")
    if base is not None: vC = vE = base
    elif not G4: vC = vE = f'NO EVALUABLE (el control sin herencia {AZA} sale de sus sombras)'
    else:
        if P1 and P2 and P3: vC = 'FUNCIONA: CON EL HIJO INGENUO LA SELECCION MUEVE EL CEREBRO Y SUBE LA CAPACIDAD SOBRE LA BASE; SIN HERENCIA NO (en esta serie)'
        elif P2 and P3: vC = 'HAY ALGO MODESTO: LA HERENCIA SUBE LA CAPACIDAD DEL LINAJE INGENUO, SIN FIRMA DEL GEN CONTRA SOMBRAS (en esta serie)'
        elif P1 and P3: vC = 'HAY ALGO MODESTO: LA SELECCION MUEVE EL GEN Y GANA A SU CONTROL SIN HERENCIA, PERO NO SUPERA A LA BASE (en esta serie)'
        else: vC = 'NO (en esta serie)'
        vE = ('FUNCIONA: EL LINAJE INGENUO SELECCIONADO NECESITA MENOS FUNDADORES QUE LA BASE Y QUE SU CONTROL SIN HERENCIA (en esta serie)'
              if (P4F and P4A) else 'NO (en esta serie)')
    L.append(f"VEREDICTO C POR LA LETRA (una serie): {vC}")
    L.append(f"VEREDICTO E (establecimiento) POR LA LETRA (una serie): {vE}")
    # ---- descriptivo (no decide)
    def md(b, f):
        v = [f(x) for x in by[b]]; v = [z for z in v if z is not None]
        return (round(float(np.median(v)), 4) if v else None)
    L.append("descriptivo, genes de los vivos en T (mediana sobre semillas): "
             + '; '.join(f"{g} SEL {md(SEL, lambda x, g=g: _gen_T(x, g))} · AZA {md(AZA, lambda x, g=g: _gen_T(x, g))}"
                         for g in ('alpha', 'aversion', 'tau_e', 'eta_s', 'hambre_boca', 'NK')))
    L.append("descriptivo: K_fund " f"{ {b: md(b, lambda x: x.get('K_fund')) for b in ING} } · fundadores repuestos por linaje en toda la corrida "
             f"{ {b: md(b, lambda x: (x.get('fundadores_rep') or 0) / MUNDO['n0']) for b in ING} } · nacimientos 2a mitad "
             f"{ {b: md(b, lambda x: x.get('nac_2a')) for b in ING} } · vida media de los nacidos muertos 2a mitad "
             f"{ {b: md(b, lambda x: x.get('vida_media_muertos_2a')) for b in ING} } · veneno + sal "
             f"{ {b: md(b, lambda x: ((x['causas_2a'][2] + x['causas_2a'][3]) / max(1, sum(x['causas_2a']))) if x.get('causas_2a') else None) for b in ING} }")
    D = dict(completo=completo, bloq=bloq, V1=V1, V2=V2, v3=v3, pers=pers, P1=P1, G4=G4, P2=P2, P3=P3, P4F=P4F, P4A=P4A, rS=rS, rA=rA,
             nF=nF, mF=mF, nFn=nFn, nA=nA, mA=mA, nAn=nAn, e4F=e4F, e4A=e4A)
    return {'C': vC, 'E': vE}, L, D


def lee(carpeta, n_esperado=20, T_esperado=None):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    if T_esperado is None: T_esperado = R[0]['T'] if R and R[0].get('T') in TS else TS[0]
    v, L, d = veredicto(R, n_esperado, T_esperado)
    for l in L: print(l, flush=True)
    return v, L, d, R


def SHAS():
    f = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    ECO = N.ECO; FR = N.FRIO_DIR; ES = os.path.join(RAIZ, 'experimentos', 'organelos', 'eco_sel')
    ps = {'corre_eco_sel_ing.py': os.path.join(AQUI, 'corre_eco_sel_ing.py'), 'nucleo_eco_sel_ing.py': os.path.join(AQUI, 'nucleo_eco_sel_ing.py'),
          'construye_eco_sel_ing.py': os.path.join(AQUI, 'construye_eco_sel_ing.py'),
          'PREREGISTRO_eco_sel_ing.md': os.path.join(AQUI, 'PREREGISTRO_eco_sel_ing.md'),
          'eco_sel/nucleo_eco_sel.py': os.path.join(ES, 'nucleo_eco_sel.py'), 'eco_sel/corre_eco_sel.py': os.path.join(ES, 'corre_eco_sel.py'),
          'frio/corre_frio.py': os.path.join(FR, 'corre_frio.py'), 'frio/motor_frio_rapido.py': os.path.join(FR, 'motor_frio_rapido.py'),
          'juaco_eco/corre_eco_v12.py': os.path.join(ECO, 'corre_eco_v12.py'), 'juaco_eco/corre_eco.py': os.path.join(ECO, 'corre_eco.py'),
          'juaco_eco/motor_eco.py': os.path.join(ECO, 'motor_eco.py'), 'juaco_eco/carros/FAMB_RES0_ECO.py': os.path.join(ECO, 'carros', 'FAMB_RES0_ECO.py'),
          'juaco_eco/carros/FABRICA_ECO.py': os.path.join(ECO, 'carros', 'FABRICA_ECO.py')}
    return {k: f(p) for k, p in ps.items() if os.path.exists(p)}


FIJOS = {'eco_sel/nucleo_eco_sel.py': '6a36e47ce61db3e1', 'eco_sel/corre_eco_sel.py': '74aff2f668c2c97a',
         'frio/corre_frio.py': '3ba8b0f5cf1fbbfa', 'frio/motor_frio_rapido.py': 'ff9d890a5cce9dec',
         'juaco_eco/corre_eco_v12.py': '1340d268e1fd93d8', 'juaco_eco/corre_eco.py': '47d9cee4d6462116',
         'juaco_eco/motor_eco.py': 'bca3033878b59622', 'juaco_eco/carros/FAMB_RES0_ECO.py': '94ea78589bc2ce24',
         'juaco_eco/carros/FABRICA_ECO.py': 'f1163009cb5193a2'}


def verifica():
    """Antes de correr: el nucleo en disco == el construido por anclas y los origenes con su sha (si no, no se corre nada)."""
    import construye_eco_sel_ing as CE
    sh = SHAS()
    mal = {k: (sh.get(k), v) for k, v in FIJOS.items() if sh.get(k) != v}
    if mal: raise SystemExit(f"ECO_SEL_ING: origenes con otro sha {mal}")
    if not CE.main(['--verifica']): raise SystemExit('ECO_SEL_ING: nucleo_eco_sel_ing.py no es el construido por anclas')
    return sh


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--lee', default=None)
    ap.add_argument('--desde', type=int); ap.add_argument('--n', type=int); ap.add_argument('--pool', type=int); ap.add_argument('--T', type=int)
    ap.add_argument('--reanuda', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('ECO_SEL_ING: banderas mal formadas')
    if resto: raise BanderaMala(f"ECO_SEL_ING: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('ECO_SEL_ING: sin la forma --bandera=valor')
    if len(argv) != len(set(x for x in argv if x.startswith('--'))) + sum(1 for x in argv if not x.startswith('--')):
        raise BanderaMala('ECO_SEL_ING: bandera repetida')
    modos = int(a.humo) + int(a.serie) + int(a.lee is not None)
    if modos != 1: raise BanderaMala('ECO_SEL_ING: exactamente uno de --humo, --serie, --lee')
    if (a.humo or a.lee is not None) and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda or a.T is not None):
        raise BanderaMala('ECO_SEL_ING: --humo y --lee van solos')
    if a.serie and (a.desde not in N.VENTANAS or a.n != 20 or a.pool is None or not 1 <= a.pool <= 6 or a.T not in TS):
        raise BanderaMala(f"ECO_SEL_ING: --serie --desde {N.VENTANAS[0]} (serie) o {N.VENTANAS[1]} (replica) --n 20 --pool 1..6 --T {TS[0]}|{TS[1]}")
    return a


def humo():
    """UN proceso, sin Pool: semilla de practica 46195, los 3 brazos, T 200 000 (regla 3: <= 6 corridas, <= 200 000 pasos). Escribe su JSON."""
    sh = verifica()
    usa_gemelo()
    os.makedirs(os.path.join(DATOS, 'humo'), exist_ok=True)
    ts = time.strftime('%Y%m%d_%H%M%S'); etq = f"eco_sel_ing_humo_s{N.HUMO['semilla']}_T{N.HUMO['T']}_{ts}"
    carpeta = os.path.join(DATOS, 'humo', etq); os.makedirs(carpeta, exist_ok=True); t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] HUMO ECO_SEL_ING (gemelo motor_frio_rapido, 1 proceso) · shas {sh}", flush=True)
    R = []; T = N.HUMO['T']
    for b in ING:
        r = trabajo((N.HUMO['semilla'], b, T, N.tc_de(b, T), N.FRIO['T_lect'], carpeta, False))
        R.append(r)
        print(f"[{time.strftime('%H:%M:%S')}] {b} s{r['seed']}: {r['seg']} s · carro {r.get('carro')} · t_corte {r.get('t_corte')} · persiste "
              f"{r['persiste']} (vivos {r.get('vivos_T')}, linajes {r.get('linajes_T')}) · K {None if r.get('tam_total') is None else round(kbar(r, T), 2)} · "
              f"K_nac {r.get('K_nac')} · K_fund {r.get('K_fund')} · fund_2a {r.get('fund_2a')} · fundadores_rep {r.get('fundadores_rep')} · "
              f"n_nac {r.get('n_nac')} · tasa_mut {r.get('tasa_mut')} · fuera {r.get('fuera_mutables')} · movidos {r.get('movidos_mutables')} · "
              f"genes vivos T {r.get('genes_vivos_T')} · sel_100k {r.get('sel_100k')} · vida 2a {r.get('vida_media_muertos_2a')} · "
              f"causas 2a {r.get('causas_2a')} · bloqueados {r.get('bloqueados')} · max_vivos {r.get('max_vivos')} · aborto {r.get('aborto')}", flush=True)
    v, L, d = veredicto(R, n_esperado=20, T_esperado=T)
    for l in L: print('  ' + l, flush=True)
    seg = {x['brazo']: x['seg'] for x in R}
    proy = {Tp: round(sum(seg.values()) * (Tp / T) * 20 / 6 / 60, 1) for Tp in TS}
    print(f"  COSTO: {seg} s a T {T}; proyeccion lineal de una serie (3 brazos x 20, Pool 6, sin contar el PC compartido): "
          f"{ {k: str(z) + ' min' for k, z in proy.items()} }")
    ruta = os.path.join(DATOS, 'humo', etq + '.json')
    json.dump(dict(humo=N.HUMO, BRAZOS={b: N.BRAZOS[b] for b in ING}, R=R, veredicto_de_prueba=v, lineas=L, seg=round(time.time() - t0, 1),
                   seg_por_brazo=seg, proyeccion_serie_min_pool6=proy, shas=sh),
              open(ruta, 'w', encoding='utf-8'), default=str)
    print(f"  JSON: {os.path.relpath(ruta, RAIZ)}  ({round(time.time() - t0, 1)} s)")
    print(f"VEREDICTO (humo, una semilla, T corto: no decide): {v}")
    return ruta


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.humo: return humo()
    if a.lee is not None:
        lee(a.lee); return
    sh = verifica()
    usa_gemelo()
    T, tl = a.T, N.FRIO['T_lect']
    etq = f"eco_sel_ing_serie_s{a.desde}-{a.desde + a.n - 1}_T{T}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"ECO_SEL_ING: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ECO_SEL_ING {etq} · T {T} · brazos { {b: N.BRAZOS[b] for b in ING} } · pool {a.pool} · motor GEMELO motor_frio_rapido · shas {sh}")
    orden = (SEL, AZA, BASE)   # los caros primero
    jobs = [(s, b, T, N.tc_de(b, T), tl, carpeta, a.reanuda) for b in orden for s in range(a.desde, a.desde + a.n)]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool, initializer=usa_gemelo) as pool:
        for k, r in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] {r['brazo']} s{r['seed']}: K {None if r.get('tam_total') is None else round(kbar(r, T), 2)} · K_nac {r.get('K_nac')} · "
                f"fund_2a {r.get('fund_2a')} · persiste {r['persiste']} · bloqueados {r.get('bloqueados')} · aborto {r.get('aborto')} "
                f"({r['seg']} s; {round(time.time() - t0)} s)")
    v, L, d, R = lee(carpeta, a.n, T)
    for l in L: flog.write(l + '\n')
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d=d, seg=round(time.time() - t0), MUNDO=MUNDO, SERIE=N.SERIE, T=T,
                   BRAZOS={b: N.BRAZOS[b] for b in ING}, UMB=UMB, shas=sh),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    log(f"VEREDICTOS: {v}")
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
