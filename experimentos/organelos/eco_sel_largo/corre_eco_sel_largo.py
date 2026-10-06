"""corre_eco_sel_largo.py — RUNNER y LETRA de ECO_SEL LARGO (frente 2; 28-sep-2026). Encargo: eco_sel/ENCARGO_NUBE_largo.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas); el metodo manda sobre el como. Principio del director: que la evolucion construya el organo, no nosotros.

Preregistro: PREREGISTRO_eco_sel_largo.md (la letra esta AQUI, en veredicto(), y alli, §6).
La corrida es nucleo_eco_sel_largo.trabajo (construido POR ANCLAS desde eco_sel/nucleo_eco_sel.py, sha 6a36e47ce61db3e1, por
construye_eco_sel_largo.py): el mismo mundo que F1 y eco_sel (ECO w90: esc 90, 90 fundadores, quimiostato, tope 3000), el mismo carro de
la familia (FAMB_RES0_ECO), frio en todos los brazos (t_corte = 1), el gemelo motor_frio_rapido importado sin tocar, T = 1e7. Brazos:
  F1      MUT0      sin mutacion (== eco_sel F1 bit a bit a T 1e6; arnes (A))
  SEL_C   CEREBRO   los 15 genes del cerebro heredables (== eco_sel SEL_C bit a bit a T 1e6)
  SEL_MC  MC        rep_umbral + los 15 del cerebro heredables (16 genes; dote y rep_X fijos)
  AZA_MC  MC_AZAR   los mismos 16 genes SIN herencia (donante 'azar')
  SEL_M   MARGEN    solo rep_umbral heredable (DESCRIPTIVO: no entra en la letra; se corre porque el costo lo permite, §10)
DOS PREGUNTAS, DOS VEREDICTOS (no se combinan): L (¿K sigue subiendo de T 1e6 a T 1e7?) y MC (¿SEL_MC supera a SEL_C?).

Uso (ERR-115: banderas desconocidas o abreviadas abortan; --help no existe; SOLO el coordinador lanza --serie):
  python experimentos/organelos/eco_sel_largo/corre_eco_sel_largo.py --humo                                   # 1 proceso, 45491, T 200 000
  python experimentos/organelos/eco_sel_largo/corre_eco_sel_largo.py --serie --desde 45401 --n 20 --pool 3    # serie
  python experimentos/organelos/eco_sel_largo/corre_eco_sel_largo.py --serie --desde 45421 --n 20 --pool 3    # replica
  python experimentos/organelos/eco_sel_largo/corre_eco_sel_largo.py --serie --desde 45401 --n 20 --pool 3 --reanuda
  python experimentos/organelos/eco_sel_largo/corre_eco_sel_largo.py --lee <carpeta de la serie>
"""
import argparse, glob, hashlib, json, os, pickle, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import nucleo_eco_sel_largo as N      # inserta en sys.path juaco_eco y frio; CR.ME = motor Python hasta usa_gemelo()
CR = N.CR
RAIZ = N.RAIZ
MUNDO = N.MUNDO
ECO_SEL_DIR = os.path.join(RAIZ, 'experimentos', 'organelos', 'eco_sel')
T_LARGO = 10_000_000
BRAZOS_L = ('F1', 'SEL_C', 'SEL_MC', 'AZA_MC', 'SEL_M')   # SEL_M: descriptivo (§10 del preregistro)
BRAZOS = {b: N.BRAZOS[b] for b in BRAZOS_L}
DATOS = os.path.join(AQUI, 'datos')
# L-1/L-2/L-3 y MC-1/MC-2 (§6 del preregistro). Ventanas: base [T/20, T/10] (== la K de eco_sel a T 1e6) y final [9T/10, T].
UMB = dict(V1=17, V3_mut=18, BLOQ_max=2, L_n=15, L_d=2.0, L2_n=15, L3_n=15, MC_n=15, MC_d=1.5, MC2_n=15)
PREG_BRAZOS = {'L': ('SEL_C', 'AZA_MC', 'F1'), 'MC': ('SEL_MC', 'SEL_C', 'AZA_MC')}
GENES_CLAVE = ('alpha', 'aversion', 'tau_e', 'hambre_boca', 'NK', 'rep_umbral')   # descriptivo en consola (todo va en el JSON)


class BanderaMala(SystemExit):
    pass


def usa_gemelo():
    return N.usa_gemelo()


def trabajo(args):
    return N.trabajo(args)


def kvent(x, a, b, T):
    """K de una ventana: media de los cuerpos vivos (tam_total, una muestra cada MUESTRA pasos, al inicio del paso) en las muestras de
    t = a .. b INCLUSIVE; tras la extincion cuenta 0. kvent(x, T/2, T, T) es EXACTAMENTE kbar de corre_eco_sel (arnes)."""
    tt = x.get('tam_total')
    if tt is None: return None
    m = MUNDO['muestra']; n = T // m + 1
    v = (list(tt) + [0] * max(0, n - len(tt)))[a // m:b // m + 1]
    return float(np.mean(v))


def kbar(x, T):
    return kvent(x, T // 2, T, T)


def kbase(x, T): return kvent(x, T // 20, T // 10, T)      # [0.5e6, 1e6] a T 1e7
def kfin(x, T): return kvent(x, 9 * T // 10, T, T)          # [9e6, 1e7] a T 1e7
def kcurva(x, T): return [kvent(x, k * T // 10, (k + 1) * T // 10, T) for k in range(10)]


def rango(x, g, t):
    """Rango (1..9; empates a medias) de la media del gen g en el BANCO real entre ella y sus 8 sombras, fila de gen_t de t (descriptivo)."""
    f = next((r for r in (x.get('gen_t') or []) if r[0] == t), None)
    if f is None or len(f) < 8 or f[6] is None or not f[7]: return None
    j = x['genes'].index(g); r = f[6][j]; S = [s[j] for s in f[7]]
    return 1.0 + sum(1 for v in S if v < r) + 0.5 * sum(1 for v in S if v == r)


def _med(v):
    v = [z for z in v if z is not None]
    return round(float(np.median(v)), 3) if v else None


def _q(v, q):
    v = [z for z in v if z is not None]
    return round(float(np.quantile(v, q)), 3) if v else None


# ================================================================================ LA LETRA (PREREGISTRO_eco_sel_largo.md §6)
def veredicto(R, n_esperado=20, T_esperado=None):
    T = T_LARGO if T_esperado is None else T_esperado
    L = []; by = {b: sorted([x for x in R if x['brazo'] == b], key=lambda x: x['seed']) for b in BRAZOS}
    n = {b: len(v) for b, v in by.items()}
    pers = {b: sum(int(x.get('persiste') or 0) for x in v) for b, v in by.items()}
    abortos = [(x['brazo'], x['seed'], x.get('aborto')) for x in R if x.get('aborto')]
    tc_mal = [(x['brazo'], x['seed']) for x in R if x['brazo'] in BRAZOS and x.get('t_corte') != BRAZOS[x['brazo']][2]]
    ajenos = [(x['brazo'], x['seed']) for x in R if x['brazo'] not in BRAZOS]
    sem = {b: tuple(x['seed'] for x in v) for b, v in by.items()}
    completo = (all(n[b] == n_esperado for b in BRAZOS) and all(x['T'] == T for x in R) and not abortos and not tc_mal and not ajenos
                and len({(x['brazo'], x['seed']) for x in R}) == len(R) and len(set(sem.values())) == 1)
    semillas = sorted(set(x['seed'] for x in R))
    # bloqueados: la semilla con el tope de cuerpos alcanzado en CUALQUIER brazo es NO EVALUABLE (cuenta como fallo en toda puerta)
    s_bloq = sorted({x['seed'] for x in R if int(x.get('bloqueados') or 0) > 0})
    sucio = [(x['brazo'], x['seed'], x.get('n_refund'), x.get('fundadores_rep')) for x in R
             if x.get('n_refund') != 0 or x.get('fundadores_rep') != 0]
    ev = [s for s in semillas if s not in s_bloq]
    KB = {b: {x['seed']: kbase(x, T) for x in v} for b, v in by.items()}
    KF = {b: {x['seed']: kfin(x, T) for x in v} for b, v in by.items()}
    DK = {b: {s: (KF[b][s] - KB[b][s]) for s in KF[b] if KF[b][s] is not None and KB[b][s] is not None} for b in BRAZOS}
    L.append(f"semillas por brazo: {n}; persiste en T = {T}: {pers}; abortos: {abortos[:5]}; t_corte distinto de 1: {tc_mal[:5]}; "
             f"semillas con bloqueados (NO EVALUABLES): {s_bloq}")
    L.append(f"K BASE [T/20, T/10] (== K de eco_sel a T 1e6 si T = 1e7), mediana: { {b: _med(KB[b].values()) for b in BRAZOS} } · "
             f"K FINAL [9T/10, T], mediana: { {b: _med(KF[b].values()) for b in BRAZOS} } · dK = final - base, mediana: "
             f"{ {b: _med(DK[b].values()) for b in BRAZOS} }")
    esperado = {b: (list(N.GENETICAS[BRAZOS[b][0]]['mutables'] or []) if N.GENETICAS[BRAZOS[b][0]]['p'] else []) for b in BRAZOS}
    v3 = {}
    for b, v in by.items():
        mal_mut = [x['seed'] for x in v if x.get('mutables') is None or list(x['mutables']) != esperado[b]]
        fuera = [x['seed'] for x in v if (x.get('fuera_mutables') or 0) != 0]
        con_mut = sum(1 for x in v if (x.get('tasa_mut') or 0) > 0)
        ok = not mal_mut and not fuera and (con_mut == 0 if b == 'F1' else con_mut >= UMB['V3_mut'])
        v3[b] = (ok, mal_mut[:3], fuera[:3], con_mut)
    V1 = pers['F1'] >= UMB['V1']
    V2 = not sucio
    VB = len(s_bloq) <= UMB['BLOQ_max']
    L.append(f"V1 F1 persiste >= {UMB['V1']}/20: {'SE CUMPLE' if V1 else 'NO'} ({pers['F1']}) · V2 frio limpio (0 refundados, 0 fundadores "
             f"repuestos, todos los brazos): {'SE CUMPLE' if V2 else 'NO'} {sucio[:5]} · VB semillas bloqueadas <= {UMB['BLOQ_max']}: "
             f"{'SE CUMPLE' if VB else 'NO'} ({len(s_bloq)})")
    L.append(f"V3 genetica declarada (mutables, 0 genes fuera, mutacion en >= {UMB['V3_mut']}/20; F1 sin mutacion): { {b: v3[b] for b in BRAZOS} }")
    if not completo: base = 'NO EVALUABLE (serie incompleta, abortos, T, t_corte o semillas distintas)'
    elif not V2: base = 'NO EVALUABLE (un brazo tuvo fundadores repuestos: el frio no es frio)'
    elif not V1: base = 'NO EVALUABLE (el ancla F1 no persiste >= 17/20 a T 1e7)'
    elif not VB: base = f'NO EVALUABLE (tope de cuerpos alcanzado en {len(s_bloq)} semillas > {UMB["BLOQ_max"]})'
    else: base = None
    out = {}
    D = dict(completo=completo, s_bloq=s_bloq, V1=V1, V2=V2, VB=VB, pers=pers, v3=v3, abortos=abortos, sucio=sucio,
             KB={b: KB[b] for b in BRAZOS}, KF={b: KF[b] for b in BRAZOS})

    def cuenta(f):   # sobre las semillas evaluables; una semilla bloqueada o sin dato cuenta como fallo
        c = 0; ds = []
        for s in ev:
            d = f(s)
            if d is None: continue
            ds.append(d); c += int(d > 0)
        return c, (float(np.median(ds)) if ds else None)
    # ---------------- L: ¿sigue subiendo?
    nL1, mL1 = cuenta(lambda s: DK['SEL_C'].get(s))
    L1a = nL1 >= UMB['L_n']; L1b = mL1 is not None and mL1 >= UMB['L_d']
    nA, mA = cuenta(lambda s: DK['AZA_MC'].get(s))
    L2a = not (nA >= UMB['L_n'] and mA is not None and mA >= UMB['L_d'])
    nL2, mL2 = cuenta(lambda s: (DK['SEL_C'][s] - DK['AZA_MC'][s]) if s in DK['SEL_C'] and s in DK['AZA_MC'] else None)
    L2b = nL2 >= UMB['L2_n']
    nL3, mL3 = cuenta(lambda s: (DK['SEL_C'][s] - DK['F1'][s]) if s in DK['SEL_C'] and s in DK['F1'] else None)
    L3 = nL3 >= UMB['L3_n']
    V3L = all(v3[b][0] for b in PREG_BRAZOS['L'])
    r2 = lambda z: None if z is None else round(z, 2)
    L.append(f"[L] L-1 SEL_C sube (K final > K base) en >= {UMB['L_n']}/20: {'SE CUMPLE' if L1a else 'NO'} ({nL1}/{len(ev)}) y mediana de dK >= "
             f"+{UMB['L_d']}: {'SE CUMPLE' if L1b else 'NO'} ({r2(mL1)}) · L-2 no es deriva: AZA_MC NO cumple L-1: {'SE CUMPLE' if L2a else 'NO'} "
             f"({nA}/{len(ev)}, mediana {r2(mA)}) y dK(SEL_C) > dK(AZA_MC) pareado >= {UMB['L2_n']}/20: {'SE CUMPLE' if L2b else 'NO'} ({nL2}, "
             f"mediana {r2(mL2)}) · L-3 no es el tiempo: dK(SEL_C) > dK(F1) pareado >= {UMB['L3_n']}/20: {'SE CUMPLE' if L3 else 'NO'} ({nL3}, "
             f"mediana {r2(mL3)})")
    if base is not None: v = base
    elif not V3L: v = 'NO EVALUABLE (la genetica de SEL_C, AZA_MC o F1 no es la declarada)'
    elif L1a and L1b and L2a and L2b and L3:
        v = 'FUNCIONA: CON 10x MAS TIEMPO LA SELECCION SIGUE SUBIENDO K (SEL_C, >= +2 cuerpos); NI LA DERIVA NI EL TIEMPO SOLO LO HACEN (en esta serie)'
    elif L1a and L2a and L2b and L3:
        v = 'HAY ALGO MODESTO: K DE SEL_C SIGUE SUBIENDO CON EL TIEMPO, PERO MENOS DE +2 CUERPOS (en esta serie)'
    else: v = 'NO: K DE SEL_C NO SIGUE SUBIENDO POR LA LETRA (se estanca, baja, o lo explican la deriva o el tiempo) (en esta serie)'
    L.append(f"VEREDICTO L POR LA LETRA (una serie; el del bloque exige serie + replica con el mismo veredicto): {v}")
    out['L'] = v
    D['L'] = dict(L1a=L1a, L1b=L1b, L2a=L2a, L2b=L2b, L3=L3, V3=V3L, nL1=nL1, mL1=mL1, nA=nA, mA=mA, nL2=nL2, mL2=mL2, nL3=nL3, mL3=mL3)
    # ---------------- MC: ¿margen + cerebro supera al cerebro solo?
    nM1, mM1 = cuenta(lambda s: (KF['SEL_MC'][s] - KF['SEL_C'][s]) if s in KF['SEL_MC'] and s in KF['SEL_C'] else None)
    M1a = nM1 >= UMB['MC_n']; M1b = mM1 is not None and mM1 >= UMB['MC_d']
    nM2, mM2 = cuenta(lambda s: (KF['SEL_MC'][s] - KF['AZA_MC'][s]) if s in KF['SEL_MC'] and s in KF['AZA_MC'] else None)
    M2 = nM2 >= UMB['MC2_n']
    V3M = all(v3[b][0] for b in PREG_BRAZOS['MC']) and v3['F1'][0]
    L.append(f"[MC] MC-1 K final SEL_MC > SEL_C pareado >= {UMB['MC_n']}/20: {'SE CUMPLE' if M1a else 'NO'} ({nM1}/{len(ev)}) y mediana >= "
             f"+{UMB['MC_d']}: {'SE CUMPLE' if M1b else 'NO'} ({r2(mM1)}) · MC-2 K final SEL_MC > AZA_MC (los mismos 16 genes sin herencia) "
             f"pareado >= {UMB['MC2_n']}/20: {'SE CUMPLE' if M2 else 'NO'} ({nM2}/{len(ev)}, mediana {r2(mM2)})")
    if base is not None: v = base
    elif not V3M: v = 'NO EVALUABLE (la genetica de SEL_MC, SEL_C, AZA_MC o F1 no es la declarada)'
    elif M1a and M1b and M2:
        v = 'FUNCIONA: CON EL MARGEN Y EL CEREBRO HEREDABLES A LA VEZ LA SELECCION SUBE K POR ENCIMA DEL CEREBRO SOLO; SIN HERENCIA NO (en esta serie)'
    elif M1a and M2:
        v = 'HAY ALGO MODESTO: SEL_MC SUPERA A SEL_C EN >= 15/20, PERO POR MENOS DE +1.5 CUERPOS (en esta serie)'
    else: v = 'NO: SEL_MC NO SUPERA A SEL_C POR LA LETRA (o el mismo genoma sin herencia hace lo mismo) (en esta serie)'
    L.append(f"VEREDICTO MC POR LA LETRA (una serie; el del bloque exige serie + replica con el mismo veredicto): {v}")
    out['MC'] = v
    D['MC'] = dict(M1a=M1a, M1b=M1b, M2=M2, V3=V3M, nM1=nM1, mM1=mM1, nM2=nM2, mM2=mM2)
    # ---------------- descriptivo (no decide)
    curva = {b: [[_q([kcurva(x, T)[k] for x in by[b]], q) for q in (0.1, 0.5, 0.9)] for k in range(10)] for b in BRAZOS}
    D['curva_K'] = curva
    L.append("descriptivo, CURVA de K por ventana de T/10 (mediana [q10, q90] sobre semillas):")
    for b in BRAZOS:
        L.append(f"    {b:7s} " + ' '.join(f"{c[1]}[{c[0]},{c[2]}]" for c in curva[b]))
    L.append(f"descriptivo, K [T/2, T] (la de eco_sel aplicada a T), mediana: { {b: _med([kbar(x, T) for x in by[b]]) for b in BRAZOS} }")
    GV = {}
    for b in BRAZOS:
        mut = esperado[b]
        GV[b] = {g: [_med([((x.get('ventanas') or {}).get('genes', {}).get(g, {}).get('media') or [None] * 10)[k] for x in by[b]])
                     for k in range(10)] for g in mut}
    D['genes_ventana'] = GV
    L.append("descriptivo, GENES por ventana (mediana sobre semillas de la media de los vivos en el borde W_k; W_1, W_5, W_10; todo en el JSON):")
    for b in BRAZOS:
        if GV[b]:
            L.append(f"    {b:7s} " + ' · '.join(f"{g} {GV[b][g][0]}/{GV[b][g][4]}/{GV[b][g][9]}" for g in GENES_CLAVE if g in GV[b]))

    def fvs(x, k):
        m = ((x.get('ventanas') or {}).get('muertes') or [None] * 10)[k]
        return None if not m or not sum(m) else (m[2] + m[3]) / sum(m)
    CM = {b: [_med([fvs(x, k) for x in by[b]]) for k in range(10)] for b in BRAZOS}
    D['veneno_sal_ventana'] = CM
    L.append(f"descriptivo, fraccion de muertes por veneno + sal por ventana (mediana): { {b: CM[b] for b in BRAZOS} }")
    rk = {b: {g: (_med([rango(x, g, N.T_SEL) for x in by[b]]), _med([rango(x, g, T) for x in by[b]])) for g in ('alpha', 'aversion', 'tau_e', 'rep_umbral')
              if g in esperado[b]} for b in BRAZOS if b != 'F1'}
    L.append(f"descriptivo, rango del banco contra sus 8 sombras (mediana; en t = {N.T_SEL} y en T; la deriva de las sombras llena el rango a T largo): {rk}")
    L.append(f"descriptivo, nacimientos totales (mediana): { {b: _med([x.get('n_nac') for x in by[b]]) for b in BRAZOS} }; R0 de nacidos "
             f"{ {b: _med([x.get('r0_nac') for x in by[b]]) for b in BRAZOS} } (~1 por construccion en el quimiostato: no informa)")
    return out, L, D


def lee(carpeta, n_esperado=20, T=None):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))]
    v, L, d = veredicto(R, n_esperado, T)
    for l in L: print(l, flush=True)
    return v, L, d, R


def _h(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def SHAS():
    ECO = N.ECO; FR = N.FRIO_DIR; ES = ECO_SEL_DIR
    ps = {'corre_eco_sel_largo.py': os.path.join(AQUI, 'corre_eco_sel_largo.py'),
          'nucleo_eco_sel_largo.py': os.path.join(AQUI, 'nucleo_eco_sel_largo.py'),
          'construye_eco_sel_largo.py': os.path.join(AQUI, 'construye_eco_sel_largo.py'),
          'PREREGISTRO_eco_sel_largo.md': os.path.join(AQUI, 'PREREGISTRO_eco_sel_largo.md'),
          'eco_sel/nucleo_eco_sel.py': os.path.join(ES, 'nucleo_eco_sel.py'), 'eco_sel/construye_eco_sel.py': os.path.join(ES, 'construye_eco_sel.py'),
          'frio/corre_frio.py': os.path.join(FR, 'corre_frio.py'), 'frio/motor_frio_rapido.py': os.path.join(FR, 'motor_frio_rapido.py'),
          'juaco_eco/corre_eco_v12.py': os.path.join(ECO, 'corre_eco_v12.py'), 'juaco_eco/corre_eco.py': os.path.join(ECO, 'corre_eco.py'),
          'juaco_eco/motor_eco.py': os.path.join(ECO, 'motor_eco.py'), 'juaco_eco/carros/FAMB_RES0_ECO.py': os.path.join(ECO, 'carros', 'FAMB_RES0_ECO.py')}
    return {k: _h(p) for k, p in ps.items() if os.path.exists(p)}


FIJOS = {'nucleo_eco_sel_largo.py': '69f2b652ac46cd1b',
         'eco_sel/nucleo_eco_sel.py': '6a36e47ce61db3e1', 'eco_sel/construye_eco_sel.py': 'f2f5ed3c54d1b2c5',
         'frio/corre_frio.py': '3ba8b0f5cf1fbbfa', 'frio/motor_frio_rapido.py': 'ff9d890a5cce9dec',
         'juaco_eco/corre_eco_v12.py': '1340d268e1fd93d8', 'juaco_eco/corre_eco.py': '47d9cee4d6462116',
         'juaco_eco/motor_eco.py': 'bca3033878b59622', 'juaco_eco/carros/FAMB_RES0_ECO.py': '94ea78589bc2ce24'}


def verifica():
    """Antes de correr: el nucleo en disco == el construido por anclas (y el de eco_sel == el suyo), y todo lo que corre con su sha."""
    if ECO_SEL_DIR not in sys.path: sys.path.insert(0, ECO_SEL_DIR)
    import construye_eco_sel_largo as CL
    import construye_eco_sel as CE
    sh = SHAS()
    mal = {k: (sh.get(k), v) for k, v in FIJOS.items() if sh.get(k) != v}
    if mal: raise SystemExit(f"LARGO: archivos con otro sha {mal}")
    if not CE.main(['--verifica']): raise SystemExit('LARGO: eco_sel/nucleo_eco_sel.py no es el construido por anclas')
    if not CL.main(['--verifica']): raise SystemExit('LARGO: nucleo_eco_sel_largo.py no es el construido por anclas')
    return sh


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--lee', default=None)
    ap.add_argument('--desde', type=int); ap.add_argument('--n', type=int); ap.add_argument('--pool', type=int)
    ap.add_argument('--reanuda', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('LARGO: banderas mal formadas')
    if resto: raise BanderaMala(f"LARGO: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('LARGO: sin la forma --bandera=valor')
    if len(argv) != len(set(x for x in argv if x.startswith('--'))) + sum(1 for x in argv if not x.startswith('--')):
        raise BanderaMala('LARGO: bandera repetida')
    modos = int(a.humo) + int(a.serie) + int(a.lee is not None)
    if modos != 1: raise BanderaMala('LARGO: exactamente uno de --humo, --serie, --lee')
    if a.humo and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda): raise BanderaMala('LARGO: --humo va solo')
    if a.lee is not None and (a.desde is not None or a.n is not None or a.pool is not None or a.reanuda):
        raise BanderaMala('LARGO: --lee va solo')
    if a.serie and (a.desde not in N.VENTANAS or a.n != 20 or a.pool is None or not 1 <= a.pool <= 6):
        raise BanderaMala(f"LARGO: --serie --desde {N.VENTANAS[0]} (serie) o {N.VENTANAS[1]} (replica) --n 20 --pool 1..6")
    return a


def _mide_ckpt(reg):
    """SOLO el humo: envuelve CR.ME.run_solapadas para medir el checkpoint (t, bytes del blob, segundos de guarda). No toca la corrida."""
    orig = CR.ME.run_solapadas

    def envuelto(*a, _o=orig, **k):
        fn = k['eco']['ckpt_fn']

        def fn2(t, blob):
            t0 = time.time(); fn(t, blob); reg.append((t, len(blob), round(time.time() - t0, 3)))
        k['eco'] = dict(k['eco'], ckpt_fn=fn2)
        return _o(*a, **k)
    CR.ME.run_solapadas = envuelto
    return orig


def humo():
    """UN proceso, sin Pool: semilla de practica 45491, los 5 brazos, T 200 000 (regla 3: <= 6 corridas, <= 200 000 pasos). Escribe su JSON."""
    import resource
    sh = verifica()
    usa_gemelo()
    os.makedirs(os.path.join(DATOS, 'humo'), exist_ok=True)
    ts = time.strftime('%Y%m%d_%H%M%S'); etq = f"eco_sel_largo_humo_s{N.HUMO['semilla']}_T{N.HUMO['T']}_{ts}"
    carpeta = os.path.join(DATOS, 'humo', etq); os.makedirs(carpeta, exist_ok=True); t0 = time.time()
    flog = open(os.path.join(DATOS, 'humo', etq + '.log'), 'w', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"HUMO ECO_SEL LARGO (gemelo motor_frio_rapido, 1 proceso; la maquina comparte CPU con otra serie Pool 3: tiempos CONTAMINADOS) · shas {sh}")
    R = []; ck = {}
    Th = N.HUMO['T']
    for b in BRAZOS_L:
        reg = []; orig = _mide_ckpt(reg)
        try:
            r = trabajo((N.HUMO['semilla'], b, Th, BRAZOS[b][2], N.FRIO['T_lect'], carpeta, False))
        finally:
            CR.ME.run_solapadas = orig
        R.append(r); ck[b] = reg
        vt = r.get('ventanas') or {}
        log(f"{b} ({BRAZOS[b][0]}) s{r['seed']}: {r['seg']} s · persiste {r['persiste']} (vivos {r.get('vivos_T')}) · K base "
            f"{round(kbase(r, Th), 2)} · K final {round(kfin(r, Th), 2)} · K [T/2,T] {round(kbar(r, Th), 2)} · n_nac {r.get('n_nac')} · refundados "
            f"{r.get('n_refund')} · fund_rep {r.get('fundadores_rep')} · bloq {r.get('bloqueados')} · mutables {len(r.get('mutables') or [])} · fuera "
            f"{r.get('fuera_mutables')} · tasa_mut {r.get('tasa_mut')} · checkpoints (t, bytes, s) {reg} · vivos por borde {vt.get('vivos')} · "
            f"muertes por ventana {vt.get('muertes')} · aborto {r.get('aborto')}")
    v, L, d = veredicto(R, n_esperado=20, T_esperado=Th)
    for l in L: log('  ' + l)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024
    seg = {x['brazo']: x['seg'] for x in R}
    ext = {b: round(s * T_LARGO / Th / 60, 1) for b, s in seg.items()}
    tot = sum(ext.values())
    log(f"COSTO (contaminado): s por corrida a T {Th}: {seg}; extrapolado LINEAL a T 1e7 (min/corrida): {ext}; 20 semillas x {len(BRAZOS_L)} "
        f"brazos = {round(tot * 20 / 60, 1)} h de CPU; con Pool 3 ~{round(tot * 20 / 60 / 3, 1)} h por serie (sin contar el checkpoint, que crece con t: "
        f"ver arnes) · memoria maxima del proceso {round(rss)} MB")
    ruta = os.path.join(DATOS, 'humo', etq + '.json')
    json.dump(dict(humo=N.HUMO, BRAZOS=BRAZOS, GENETICAS={k: dict(v_, mutables=list(v_['mutables'] or [])) for k, v_ in N.GENETICAS.items()},
                   R=R, veredicto_de_prueba=v, lineas=L, seg=round(time.time() - t0, 1), seg_por_brazo=seg, min_1e7_lineal=ext, ckpt=ck,
                   rss_mb=round(rss), shas=sh), open(ruta, 'w', encoding='utf-8'), default=str)
    log(f"JSON: {os.path.relpath(ruta, RAIZ)}  ({round(time.time() - t0, 1)} s)")
    log(f"VEREDICTO (humo, una semilla, T corto: no decide): {v}")
    flog.close()
    return ruta


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.humo: return humo()
    if a.lee is not None:
        lee(a.lee); return
    etq = f"eco_sel_largo_serie_s{a.desde}-{a.desde + a.n - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*_s*.json')):
        raise SystemExit(f"LARGO: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ECO_SEL LARGO {etq}: arranca (verifica shas y anclas)")
    sh = verifica()
    usa_gemelo()
    T, tl = T_LARGO, N.FRIO['T_lect']
    log(f"T {T} · brazos {BRAZOS} · pool {a.pool} · reanuda {a.reanuda} · checkpoint cada {N.CKPT_LARGO} · motor GEMELO motor_frio_rapido · shas {sh}")
    orden = ('SEL_MC', 'SEL_C', 'SEL_M', 'F1', 'AZA_MC')   # los caros primero
    jobs = [(s, b, T, BRAZOS[b][2], tl, carpeta, a.reanuda) for b in orden for s in range(a.desde, a.desde + a.n)]
    t0 = time.time()
    from multiprocessing import Pool, TimeoutError as TE
    with Pool(a.pool, initializer=usa_gemelo) as pool:
        it = pool.imap_unordered(trabajo, jobs); k = 0
        while k < len(jobs):
            try:
                r = it.next(timeout=300)
            except TE:   # latido cada 5 min (regla 10): corridas terminadas y checkpoints en disco
                cks = glob.glob(os.path.join(carpeta, 'ckpt', '*.pkl'))
                log(f"latido: {k}/{len(jobs)} terminadas; checkpoints vivos {len(cks)} "
                    f"({', '.join(os.path.basename(c) + ' ' + str(round(os.path.getsize(c) / 1e6, 1)) + ' MB' for c in cks[:6])}); {round(time.time() - t0)} s")
                continue
            k += 1
            log(f"[{k}/{len(jobs)}] {r['brazo']} s{r['seed']}: persiste {r['persiste']} (vivos {r.get('vivos_T')}) · K base "
                f"{None if r.get('tam_total') is None else round(kbase(r, T), 2)} · K final {None if r.get('tam_total') is None else round(kfin(r, T), 2)} · "
                f"t_ext {r.get('t_ext')} · refundados {r.get('n_refund')} · bloq {r.get('bloqueados')} · n_nac {r.get('n_nac')} · aborto {r.get('aborto')} "
                f"({r['seg']} s; {round(time.time() - t0)} s)")
    v, L, d, R = lee(carpeta, a.n)
    for l in L: flog.write(l + '\n')
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d=d, seg=round(time.time() - t0), MUNDO=MUNDO, SERIE=N.SERIE, FRIO=N.FRIO, T=T,
                   BRAZOS=BRAZOS, UMB=UMB, shas=sh), open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    log(f"VEREDICTOS: {v}")
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
