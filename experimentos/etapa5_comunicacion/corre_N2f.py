"""Etapa 5, N2f (version 3): N2b en un mundo que REAPARECE EN SITIO, ROTA EL TIPO y CADUCA (regen=50, regen_rota=True,
vida), con un receptor que NO SE DEJA DESENSENAR (escucha_si_no_sabe). Ejecuta PREREGISTRO_N2f.md (bloque 5, dia 6).
Derivado de corre_N2.py (variante b). REGLA 10: log desde el arranque. REGLA 11: procesos vivos. JSON con sha.

Tres perillas del mundo/receptor, las tres apagadas por defecto en el instrumento (identidad 8/8, identidad_n2f.py):
  regen_rota           el tipo se vuelve a sortear al reaparecer  -> flujo de patrones
  vida                 el objeto caduca aunque nadie lo muerda    -> el VENENO tambien sale (si no, el mundo se absorbe)
  escucha_si_no_sabe   el simbolo no reescribe un valor propio mas informado
Brazos de simbolos, separables:
  CONV        = mundo (rotacion + vida) + escucha_si_no_sabe=True  -> el brazo que decide E1-E5
  CONV_MUNDO  = mundo (rotacion + vida) + escucha como N2b (False) -> ATRIBUCION (A1/A2): separa el mundo de la puerta

Precisiones escritas ANTES de correr:
- Progenitor del experto: mundo_social_n3.run(seed, n=1, mundo='regla', regla='azar', T=200000, regen=None,
  devolver_estado=True). SIN regen ni rotacion, como en N2b: con n=1 el mundo usa el RNG del propio organismo
  (compat=True), asi que un progenitor con regen viviria en un mundo DISTINTO del de la corrida (seed+900000).
- Novato = organismo 0; experto = organismo 1 (estado heredado; Pq y M NO se heredan).
- veneno_total = mordidas propias sobre los 10 patrones veneno; veneno_q1/q4 = sum(mord[k][0]) / sum(mord[k][3]).
- "presentes" = patrones que el organismo llego a VISITAR (sum(vis[k]) > 0); con el mundo congelado de la v1 eran 5 de
  20, asi que "8 de 10 venenos conocidos" no significaba nada: se reporta tambien /presentes.
- s_rech / s_mord = argmax de Pq[0] / Pq[1] del EXPERTO al final. C[s] = M[s] - media(M) (ENMIENDA 1 de N2).
- emisiones por estado = sum(simbolos['emis'][st]) del EXPERTO (st=0 rechaza, st=1 muerde).

Uso:  python experimentos/etapa5_comunicacion/corre_N2f.py [--desde N] [--n N]
      python experimentos/etapa5_comunicacion/corre_N2f.py --humo [--semilla N]   (UN proceso, sin Pool)
Identidad de las perillas contra el modulo anterior: experimentos/etapa5_comunicacion/identidad_n2f.py
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 81
_n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 20
SEEDS = list(range(_desde, _desde + _n)); T = 200000; REGLA = 'azar'
REGEN = 50; REGEN_ROTA = True                                  # N2f v2: reaparicion en el mismo sitio Y rotacion del tipo
VIDA = int(sys.argv[sys.argv.index('--vida') + 1]) if '--vida' in sys.argv else 100   # N2f v3: FIJADO POR EL HUMO en 100 (unico que pasa K3+K4+K5; PREREGISTRO_N2f.md ENMIENDA 2)
VIDAS_HUMO = (50, 100, 200)                                    # barrido del humo pedido por el coordinador
VAR_KW = dict(gamma_sim=1.2, baseline_q=True, u_m=1.0)         # variante b de corre_N2.py, letra por letra (PREREGISTRO_N2b.md)
T_PROG = 200000                                                # como en N2b
PREF = 'N2f'
CONDS = {'SOLO': dict(n=1), 'N0': dict(n=2), 'INNATO': dict(n=2, senal='conducta'),
         'CONV': dict(n=2, senal='simbolo', escucha_si_no_sabe=True),          # decide E1-E5
         'CONV_MUNDO': dict(n=2, senal='simbolo'),                             # atribucion: rotacion sola, escucha como N2b
         'SHUF': dict(n=2, senal='simbolo_barajado', escucha_si_no_sabe=True)}
DECIDE = 'CONV'; ATRIB = 'CONV_MUNDO'
IDENT_B = dict(T=60000, mundo='regla', regla=REGLA, n=2, senal='simbolo', **VAR_KW)   # K1b: la via de simbolos, con regen=None
N_PARALELO = 14
_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def N(x):
    return json.loads(json.dumps(x, default=str))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def _anota(o, seed):
    """Medidas derivadas, con la precision del mundo congelado: tambien restringidas a los patrones PRESENTES."""
    import organismo_v13g as g
    vr = g.split_regla(seed, REGLA)[3]
    ven = [k for k in vr if vr[k] == 'veneno']; com = [k for k in vr if vr[k] == 'comida']
    pres = {k for k in o['vis'] if sum(o['vis'][k]) > 0}
    o['veneno_total'] = int(sum(o['veneno_propio'][k] for k in ven))
    o['veneno_q1'] = int(sum(o['mord'][k][0] for k in ven)); o['veneno_q4'] = int(sum(o['mord'][k][3] for k in ven))
    o['venenos_conocidos'] = int(sum(o['W'][k] <= -2.5 for k in ven)); o['comidas_conocidas'] = int(sum(o['W'][k] >= 0.5 for k in com))
    o['venenos_presentes'] = int(len([k for k in ven if k in pres])); o['comidas_presentes'] = int(len([k for k in com if k in pres]))
    o['venenos_conocidos_pres'] = int(sum(o['W'][k] <= -2.5 for k in ven if k in pres))
    o['comidas_conocidas_pres'] = int(sum(o['W'][k] >= 0.5 for k in com if k in pres))
    o['patrones_presentes'] = int(len(pres))
    o['vis_comida'] = int(sum(sum(o['vis'][k]) for k in com)); o['vis_veneno'] = int(sum(sum(o['vis'][k]) for k in ven))
    o['vis_q'] = [[int(sum(o['vis'][k][q] for k in com)), int(sum(o['vis'][k][q] for k in ven))] for q in range(4)]   # comida/veneno por cuarto
    s = o.get('simbolos')
    o['emis_rechaza'] = int(sum(s['emis'][0])) if s else 0       # estado 0 = rechazo
    o['emis_muerde'] = int(sum(s['emis'][1])) if s else 0        # estado 1 = mordida
    return o


def tarea(args):
    tipo = args[0]
    import mundo_social_n3 as ms
    if tipo == 'K1a':   # tronco: con regen=None y n=1 sigue siendo organismo_v13g con los defectos del TRONCO
        _, seed = args
        import organismo_v13g as g
        a = g.run(seed, T=100000, mundo='regla', regla=REGLA, fase2_en=0, eta_s=0.015, puerta=3)
        b = ms.run(seed, n=1, T=100000, mundo='regla', regla=REGLA, regen=None)[0]
        claves = ['W', 'mord', 'vis', 'deaths', 'splits', 'split_t', 'celdas']
        dif = [k for k in claves if N(a[k]) != N(b[k])]
        return dict(tipo=tipo, seed=seed, identico=not dif, difieren=dif)
    if tipo == 'K1b':   # la via de SIMBOLOS intacta: con regen=None, mundo_social_n3 == mundo_social en todas las claves
        _, seed = args
        import mundo_social as m0
        a = m0.run(seed, **IDENT_B); b = ms.run(seed, regen=None, **IDENT_B)
        dif = [(j, k) for j in range(len(a)) for k in a[j] if N(a[j][k]) != N(b[j][k])]
        return dict(tipo=tipo, seed=seed, identico=not dif, difieren=dif[:6])
    if tipo == 'P':
        _, seed = args
        r = ms.run(seed, n=1, T=T_PROG, mundo='regla', regla=REGLA, regen=None, devolver_estado=True)[0]
        return dict(tipo=tipo, seed=seed, estado=r['estado'], W=r['W'])
    _, cond, seed, estado, vida = args
    kw = CONDS[cond]
    estados = None if kw['n'] == 1 else [None, estado]
    out = ms.run(seed, T=T, mundo='regla', regla=REGLA, regen=REGEN, regen_rota=REGEN_ROTA, vida=vida, estados=estados, **VAR_KW, **kw)
    for o in out:
        o.pop('estado', None); _anota(o, seed)
    return dict(tipo='R', cond=cond, seed=seed, vida=vida, orgs=out)


def med(xs):
    return float(np.median(xs))


def C_de(o_n):
    M = np.asarray(o_n['M'], float)
    return [float(m - M.mean()) for m in M]


def analiza(res, seeds, nsem):
    """Analisis unico (lo usan la corrida completa y el humo). Devuelve (V, lineas)."""
    V = {}; L_ = []
    G = lambda c: {r['seed']: r['orgs'] for r in res if r['cond'] == c}
    hay = lambda c: len(G(c)) > 0
    nov = lambda c: [G(c)[s][0] for s in seeds if s in G(c)]
    exp = lambda c: [G(c)[s][1] for s in seeds if s in G(c) and len(G(c)[s]) > 1]
    L_.append("")
    L_.append(f"  {'cond':7s} {'veneno tot':11s} {'ven Q1':7s} {'ven Q4':7s} {'muert':6s} {'ven.con/pres':13s} {'com.con/pres':13s} {'pat.pres':9s} {'vis com/ven':13s} {'simb.recib':11s} {'decod':6s}")
    for c in CONDS:
        if not hay(c): continue
        n_ = nov(c)
        L_.append(f"  {c:7s} {med([o['veneno_total'] for o in n_]):6.0f}      {med([o['veneno_q1'] for o in n_]):6.0f}  {med([o['veneno_q4'] for o in n_]):6.0f}  "
                  f"{med([o['deaths'] for o in n_]):5.0f}  {med([o['venenos_conocidos_pres'] for o in n_]):4.0f}/{med([o['venenos_presentes'] for o in n_]):<7.0f} "
                  f"{med([o['comidas_conocidas_pres'] for o in n_]):4.0f}/{med([o['comidas_presentes'] for o in n_]):<7.0f} "
                  f"{med([o['patrones_presentes'] for o in n_]):7.0f}  {med([o['vis_comida'] for o in n_]):6.0f}/{med([o['vis_veneno'] for o in n_]):<6.0f} "
                  f"{med([o['simbolos_recibidos'] for o in n_]):9.0f}  {med([o['decodificados'] for o in n_]):5.0f}")
    if not (hay(DECIDE) and hay('N0')):
        return V, L_
    v0 = [o['veneno_total'] for o in nov('N0')]

    def bateria(c):
        """E1-E4 + P1/P2 de un brazo con simbolos, contra N0. Umbrales verbatim de N2/N2b (PREREGISTRO_N2f.md 5.3)."""
        ex_ = exp(c); nv_ = nov(c); vc_ = [o['veneno_total'] for o in nv_]
        e1_ = [(o['simbolos']['distintos'] and o['simbolos']['consistencia_q4'] is not None and o['simbolos']['consistencia_q4'] >= 0.9) for o in ex_]
        e2_ = []; cr_ = []; cm_ = []
        for o_e, o_n in zip(ex_, nv_):
            sr, sm = o_e['simbolos']['simbolo_rechazo'], o_e['simbolos']['simbolo_muerde']
            Cn = C_de(o_n); cr_.append(Cn[sr]); cm_.append(Cn[sm])
            e2_.append(Cn[sr] <= -1.0 and Cn[sm] >= 0.3)
        rech0_ = sum(o['simbolos']['simbolo_rechazo'] == 0 for o in ex_)
        par_ = sum(b < a for a, b in zip(v0, vc_))
        return dict(ex=ex_, nv=nv_, vc=vc_, e1=sum(e1_), e2=sum(e2_), rech0=rech0_, par=par_, c_r=cr_, c_m=cm_,
                    E1=sum(e1_) >= 15, E2=sum(e2_) >= 15, E3=5 <= rech0_ <= 15,
                    E4=(med(vc_) <= 0.7 * med(v0) and par_ >= 14),
                    P1=sum(max(abs(a), abs(b)) >= 0.5 for a, b in zip(cr_, cm_)) >= 10,
                    P2=sum(a >= 1.2 * b for a, b in zip(v0, vc_)) >= 15,
                    p1n=sum(max(abs(a), abs(b)) >= 0.5 for a, b in zip(cr_, cm_)),
                    p2n=sum(a >= 1.2 * b for a, b in zip(v0, vc_)))

    B = {c: bateria(c) for c in (DECIDE, ATRIB) if hay(c)}
    d = B[DECIDE]; ex = d['ex']; nv = d['nv']; vc = d['vc']
    # --- K2 canal, K3 validez del mundo, K4 equilibrio de visitas (PREREGISTRO_N2f.md 5.1 y 5.2)
    V['K2'] = med([o['simbolos_recibidos'] for o in nv]) >= 1000
    V['K3'] = med([o['veneno_q4'] for o in nov('SOLO')]) >= 20 if hay('SOLO') else None
    # K5 (puerta propia de `vida`): el mundo tiene que seguir siendo APRENDIBLE por el novato solo
    k5n = sum(o['veneno_q4'] < o['veneno_q1'] for o in nov('SOLO')) if hay('SOLO') else 0
    V['K5'] = k5n >= 15 if hay('SOLO') else None
    em_r = med([o['emis_rechaza'] for o in ex]); em_m = med([o['emis_muerde'] for o in ex])
    oidas_m = [int(round(o['simbolos_recibidos'] * (o_e['emis_muerde'] / max(o_e['emis_rechaza'] + o_e['emis_muerde'], 1)))) for o_e, o in zip(ex, nv)]
    V['K4'] = (em_m >= em_r / 5.0) and med(oidas_m) >= 500
    for k in ('E1', 'E2', 'E3', 'E4', 'P1', 'P2'):
        V[k] = d[k]
    if hay('SHUF'):
        vs = [o['veneno_total'] for o in nov('SHUF')]
        shuf_M = sum(all(abs(x) < 1.0 for x in C_de(o)) for o in nov('SHUF'))
        V['E5'] = shuf_M >= 15 and med(vs) >= 0.9 * med(v0)
    else:
        vs = []; shuf_M = 0; V['E5'] = None
    # --- A1/A2: atribucion con el brazo CONV_MUNDO (PREREGISTRO_N2f.md 5.4)
    if ATRIB in B:
        V['A1_magnitud_del_mundo'] = B[ATRIB]['E2']
        V['A2_beneficio_por_la_puerta'] = bool(d['E4'] and not B[ATRIB]['E4'])
    L_.append("")
    L_.append(f"  K2 simbolos recibidos ({DECIDE}): mediana {med([o['simbolos_recibidos'] for o in nv]):.0f} (>=1000): {'OK' if V['K2'] else 'FALLA'}")
    L_.append(f"  K3 VALIDEZ queda algo que ensenar: veneno Q4 del novato en SOLO mediana {med([o['veneno_q4'] for o in nov('SOLO')]) if hay('SOLO') else float('nan'):.0f} (>=20): {'OK' if V['K3'] else 'FALLA -> MONTAJE INVALIDO'}")
    L_.append(f"  K5 VALIDEZ de `vida` (el mundo se puede aprender solo): veneno Q4 < Q1 en SOLO {k5n}/{nsem} (>=15)"
              f"   [Q1 {med([o['veneno_q1'] for o in nov('SOLO')]) if hay('SOLO') else float('nan'):.0f} -> Q4 {med([o['veneno_q4'] for o in nov('SOLO')]) if hay('SOLO') else float('nan'):.0f}]: {'OK' if V['K5'] else 'FALLA -> MUNDO INAPRENDIBLE'}")
    L_.append(f"  K4 EQUILIBRIO emisiones del experto por estado: rechaza {em_r:.0f} / muerde {em_m:.0f}"
              f"  (razon {em_m / max(em_r, 1):.3f}, se pide >=0.200; N2d fue 0.016); oidas 'muerde' por el novato {med(oidas_m):.0f} (>=500): {'OK' if V['K4'] else 'FALLA'}")
    for c, b in B.items():
        etq = 'DECIDE' if c == DECIDE else 'ATRIB '
        L_.append(f"  --- {etq} {c}")
        L_.append(f"    E1 convencion: {b['e1']}/{nsem} (>=15): {'SOSTENIDA' if b['E1'] else 'REFUTADA'}"
                  f"   consistencia Q4 mediana {med([o['simbolos']['consistencia_q4'] or 0 for o in b['ex']]):.2f}  distintos {sum(o['simbolos']['distintos'] for o in b['ex'])}/{nsem}")
        L_.append(f"    E2 decodificacion (C[s_rech]<=-1 y C[s_mord]>=+0.3): {b['e2']}/{nsem} (>=15): {'SOSTENIDA' if b['E2'] else 'REFUTADA'}"
                  f"   contraste mediana {med(b['c_r']):+.2f} / {med(b['c_m']):+.2f}"
                  f"  (M crudo {med([o_n['M'][o_e['simbolos']['simbolo_rechazo']] for o_e, o_n in zip(b['ex'], b['nv'])]):+.2f} / {med([o_n['M'][o_e['simbolos']['simbolo_muerde']] for o_e, o_n in zip(b['ex'], b['nv'])]):+.2f})")
        L_.append(f"    E3 arbitrariedad: 'rechazo' = simbolo 0 en {b['rech0']}/{nsem} (5..15): {'SOSTENIDA' if b['E3'] else 'REFUTADA'}")
        L_.append(f"    E4 beneficio: veneno {med(b['vc']):.0f} <= 0.7 x N0 {med(v0):.0f} = {0.7*med(v0):.0f}, pareado {b['par']}/{nsem} (>=14): {'SOSTENIDA' if b['E4'] else 'REFUTADA'}")
        L_.append(f"    P1 |C|>=0.5 en {b['p1n']}/{nsem} (>=10): {b['P1']}   P2 N0 >= 1.2 x arm pareado {b['p2n']}/{nsem} (>=15): {b['P2']}"
                  f"   decodificados {med([o['decodificados'] for o in b['nv']]):.0f}  no_desensena {med([o.get('no_desensena', 0) for o in b['nv']]):.0f}")
        L_.append(f"    refuerzos del experto +/-: {med([o['simbolos']['refuerzos'][0] for o in b['ex']]):.0f} / {med([o['simbolos']['refuerzos'][1] for o in b['ex']]):.0f}"
                  f";  |Pq| mediana {med([abs(x) for o in b['ex'] for fila in o['simbolos']['Pq'] for x in fila]):.2f}")
    L_.append(f"  --- referencias: INNATO {med([o['veneno_total'] for o in nov('INNATO')]) if hay('INNATO') else float('nan'):.0f}"
              f"   SOLO {med([o['veneno_total'] for o in nov('SOLO')]) if hay('SOLO') else float('nan'):.0f}   N0 {med(v0):.0f}")
    if hay('SHUF'):
        L_.append(f"  E5 barajar destruye: |C|<1 en {shuf_M}/{nsem} (>=15) y veneno SHUF {med(vs):.0f} >= 0.9 x N0 {0.9*med(v0):.0f}: {'SOSTENIDA' if V['E5'] else 'REFUTADA'}")
    if ATRIB in B:
        L_.append(f"  A1 la magnitud la da el MUNDO (E2 tambien en {ATRIB}): {V['A1_magnitud_del_mundo']}"
                  f"      A2 el beneficio necesita la PUERTA (E4 en {DECIDE} y no en {ATRIB}): {V['A2_beneficio_por_la_puerta']}")
    return V, L_


def _shas():
    return dict(sha_preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_N2f.md')), sha_script=h16(os.path.abspath(__file__)),
                sha_mundo_social_n3=h16(os.path.join(AQUI, 'mundo_social_n3.py')), sha_mundo_social=h16(os.path.join(AQUI, 'mundo_social.py')),
                sha_v13=h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
                sha_v13g=h16(os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py')))


def humo(semilla):
    """UN proceso, sin Pool (regla 3 para agentes). Barrido de `vida` pedido por el coordinador: progenitor (200k, uno
    solo: no depende de `vida`) + N0 + CONV por cada vida de VIDAS_HUMO. K1a/K1b son identidad y cuentan aparte.
    SOLO no entra: K3 y K5 se miran con el proxy del novato de N0. No ajusta nada: solo mide y reporta."""
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'{PREF}_humo_vida_s{semilla}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"HUMO {PREF} v3 (UN proceso, sin Pool). semilla {semilla}, T={T}, regla {REGLA}, regen={REGEN}, regen_rota={REGEN_ROTA}, "
        f"vidas {VIDAS_HUMO}, kw {VAR_KW}. pid {os.getpid()}")
    log("  " + "  ".join(f"{k}={v}" for k, v in _shas().items()))
    k1 = [tarea(('K1a', semilla)), tarea(('K1b', semilla))]
    for x in k1:
        log(f"  {x['tipo']} s{x['seed']}: {'IDENTICO' if x['identico'] else 'DIFIERE ' + str(x['difieren'])}")
    log("  progenitor del experto (n=1, sin regen ni rotacion ni vida, T=%d)..." % T_PROG)
    p = tarea(('P', semilla))
    import organismo_v13g as g
    vr = g.split_regla(semilla, REGLA)[3]
    log(f"    venenos conocidos por el experto: {sum(p['W'][k] <= -2.5 for k in vr if vr[k] == 'veneno')}/10")
    res = []
    for vida in VIDAS_HUMO:
        log(f"  --- vida = {vida}")
        for cond in ('N0', DECIDE):
            t0 = time.time(); res.append(tarea(('R', cond, semilla, p['estado'], vida))); log(f"      {cond} listo en {time.time()-t0:.0f}s")
    log("")
    log(f"  {'vida':5s} {'pat.pres':9s} {'rech/muerde (razon)':26s} {'vis com/ven (experto)':22s} {'por cuarto com/ven':34s} "
        f"{'contraste C':16s} {'decod':6s} {'no_des':7s} {'veneno novato CONV / N0':24s} {'K3 prox':8s} {'K5 prox':8s} {'caduc':7s}")
    for vida in VIDAS_HUMO:
        rc = [r for r in res if r['cond'] == DECIDE and r['vida'] == vida][0]['orgs']
        r0 = [r for r in res if r['cond'] == 'N0' and r['vida'] == vida][0]['orgs'][0]
        e = rc[1]['simbolos']; C = C_de(rc[0])
        q = " ".join(f"{a}/{b}" for a, b in rc[1]['vis_q'])
        log(f"  {vida:<5d} {rc[0]['patrones_presentes']:<9d} {rc[1]['emis_rechaza']:6d}/{rc[1]['emis_muerde']:<6d} "
            f"({rc[1]['emis_muerde']/max(rc[1]['emis_rechaza'],1):.3f})  {rc[1]['vis_comida']:7d}/{rc[1]['vis_veneno']:<7d}  {q:34s} "
            f"{C[e['simbolo_rechazo']]:+.2f}/{C[e['simbolo_muerde']]:+.2f}   {rc[0]['decodificados']:6d} {rc[0].get('no_desensena', 0):7d} "
            f"{rc[0]['veneno_total']:6d} / {r0['veneno_total']:<6d}          {r0['veneno_q4']:<8d} {'SI' if r0['veneno_q4'] < r0['veneno_q1'] else 'NO':8s} {rc[0].get('caducados', 0):7d}")
        log(f"        consistencia Q4 {e['consistencia_q4']:.3f}  distintos {e['distintos']}  s_rech={e['simbolo_rechazo']} s_mord={e['simbolo_muerde']}  M {rc[0]['M']}"
            f"   N0 veneno Q1->Q4 {r0['veneno_q1']}->{r0['veneno_q4']}, conocidos {r0['venenos_conocidos_pres']}/{r0['venenos_presentes']}, muertes {r0['deaths']}"
            f"   K4: razon >= 0.200 {'OK' if rc[1]['emis_muerde'] >= rc[1]['emis_rechaza'] / 5.0 else 'FALLA'}")
    dj = os.path.join(RAIZ, 'datos', f'{PREF}_humo_vida_s{semilla}_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=True, semilla=semilla, T=T, regla=REGLA, regen=REGEN,
                             regen_rota=REGEN_ROTA, vidas=list(VIDAS_HUMO), conds=N(CONDS), var_kw=VAR_KW, K1=k1,
                             python=platform.python_version(), numpy=np.__version__, **_shas()),
                   corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


if __name__ == '__main__':
    if '--humo' in sys.argv:
        humo(int(sys.argv[sys.argv.index('--semilla') + 1]) if '--semilla' in sys.argv else 81)
        sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'{PREF}_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE {PREF} v3 (reaparicion con rotacion + vida + receptor que no se deja desensenar; regen={REGEN}, regen_rota={REGEN_ROTA}, vida={VIDA}, kw {VAR_KW}; "
        f"brazos {list(CONDS)}; decide {DECIDE}, atribuye {ATRIB}). semillas {SEEDS[0]}..{SEEDS[-1]}, T={T}, regla {REGLA}. Pool({N_PARALELO}).")
    log("  " + "  ".join(f"{k}={v}" for k, v in _shas().items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        k1 = pool.map(tarea, [(t_, s) for t_ in ('K1a', 'K1b') for s in (1, 2, 3)], chunksize=1)
        V['K1'] = all(x['identico'] for x in k1)
        log(f"ETAPA 1/4 — K1a (tronco) y K1b (via de simbolos) con regen=None: {sum(x['identico'] for x in k1)}/6 -> {'OK' if V['K1'] else 'FALLA'}")
        for x in k1:
            if not x['identico']: log(f"      DIFIERE {x['tipo']} s{x['seed']}: {x['difieren']}")
        if not V['K1']:
            log("*** K1 FALLIDO: se para."); sys.exit(1)
        log(f"ETAPA 2/4 — progenitores del experto ({len(SEEDS)}, T={T_PROG}, sin regen)...")
        prog = {r['seed']: r for r in pool.map(tarea, [('P', s) for s in SEEDS], chunksize=1)}
        import organismo_v13g as g
        conoc = [sum(prog[s]['W'][k] <= -2.5 for k in g.split_regla(s, REGLA)[3] if g.split_regla(s, REGLA)[3][k] == 'veneno') for s in SEEDS]
        log(f"  progenitores: venenos conocidos (de 10) mediana {med(conoc):.0f} [{min(conoc)}, {max(conoc)}]")
        trabajos = [('R', c, s, prog[s]['estado'], VIDA) for c in CONDS for s in SEEDS]
        log(f"ETAPA 3/4 — {len(trabajos)} corridas (regen={REGEN}, regen_rota={REGEN_ROTA}, vida={VIDA})...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    log("ETAPA 4/4 — analisis.")
    Ve, lineas = analiza(res, SEEDS, len(SEEDS))
    for l in lineas: log(l)
    V.update(Ve)
    V['MONTAJE_VALIDO'] = bool(V.get('K1') and V.get('K2') and V.get('K3') and V.get('K4') and V.get('K5'))
    V['N2f_EMERGE'] = bool(V['MONTAJE_VALIDO'] and V.get('E1') and V.get('E2') and V.get('E3') and V.get('E4') and V.get('E5'))
    log(); log(f"VEREDICTO {PREF}: " + " ".join(f"{k}={v}" for k, v in V.items()))
    if not V['MONTAJE_VALIDO']:
        log("  *** K3/K4/K5: el montaje NO es valido (PREREGISTRO_N2f.md 4.2): E1-E5 se reportan pero NO cierran ni refutan nada sobre el receptor.")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, regla=REGLA, regen=REGEN, regen_rota=REGEN_ROTA,
                vida=VIDA, conds=N(CONDS), decide=DECIDE, atribuye=ATRIB, var_kw=VAR_KW,
                veredictos=V, K1=k1, procesos_python=ps, python=platform.python_version(), numpy=np.__version__, **_shas())
    dj = os.path.join(RAIZ, 'datos', f'{PREF}_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
