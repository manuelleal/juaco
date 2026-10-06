"""corre_p8.py — P8 PROTOCOLO COMPLETO: "componer en celda retenida" (1-oct-2026). Preregistro: PREREGISTRO_p8.md. Constructor: construye_p8.py.
Nulo: nulo_p8.py. Instrumento: el de la sonda 2 (sondas/corre_s2.py y sondas/mundo_ret.py, que se IMPORTAN con sha fijado y no se tocan).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y replicas).

QUE SE CORRE. (a) CRIANZA: cada corrida ES corre_v143.tarea (se importa) con mundo_ret.run (P1b + letra E (+0.3, -0.1) a p_x 0.15 que NUNCA nace
dentro del oasis) y 9 linajes del mismo carro. TRES brazos de crianza, pareados por semilla, cada uno con SU memoria:
     comp   O1_LUGAR_COMP    (la composicion de la rafaga)      lug   O1_LUGAR (sin composicion)      comp2  O1_LUGAR_COMP2 (el candidato)
(b) PREGUNTA (sin mundo, sin resultado()): por linaje se reconstruye el carro con nace(memoria) y se llama actua() con observaciones sinteticas
(cuerpo a un paso del objeto, rejilla 5x5 de niveles, 4 celdas dentro del oasis y sus antipodas, una A a la vista = limpieza apagada).
     sobre la memoria de comp :  comp (O1_LUGAR_COMP)   comp_perm (idem con la memoria de lugar PERMUTADA entre bins, media de NPERM permutaciones)
     sobre la memoria de lug  :  lug (O1_LUGAR)         comp_s (O1_LUGAR_COMP sobre memoria de lug: el instrumento exacto de la sonda; descriptivo)
     sobre la memoria de comp2:  comp2 (O1_LUGAR_COMP2) comp2_perm   comp2sg (sin compuerta; descriptivo)   lug2 (O1_LUGAR; descriptivo)
LETRA (por codigo, lee_letra; unidad = SEMILLA): D de la semilla = mediana, sobre sus linajes validos, de D = P(muerde E dentro) - P(muerde E fuera).
SEMILLAS NUEVAS: serie 737500-737519 · replica 737520-737539 · humo 737490- · arnes 737402.
  python experimentos/organelos/escalera/p8/corre_p8.py --identidad
  python experimentos/organelos/escalera/p8/corre_p8.py --humo [--n 2 --T 60000 --desde 737490 --nota '...']
  python experimentos/organelos/escalera/p8/corre_p8.py --serie   --pool 2 [--reanuda]
  python experimentos/organelos/escalera/p8/corre_p8.py --replica --pool 2 [--reanuda]
  python experimentos/organelos/escalera/p8/corre_p8.py --lee <carpeta>
"""
import argparse, glob, importlib.util, json, math, os, platform, statistics as st, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI); SON = os.path.join(ESC, 'sondas')
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(ESC)))
for _d in (ESC, SON, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_c as RC             # se importa (no se toca)
import corre_s2 as S2            # el instrumento de la sonda 2 (Capta, memoria, carro_de, pregunta, muerde, elige)
import mundo_ret as MR
import construye_p8 as CP8
CO = RC.CO; CV = RC.CV; P = RC.P; ME = RC.ME; MC = RC.MC
h16 = CO.h16; med = CO.med

SHAS_P8 = {os.path.join(SON, 'mundo_ret.py'): '0b0d84552d176569', os.path.join(SON, 'corre_s2.py'): '6977e4869261f3da',
           os.path.join(ESC, 'corre_c.py'): '01e4ad94dd06e133'}
DATOS = os.path.join(AQUI, 'datos')
CARROS8 = {n: os.path.join(AQUI, 'carros', n + '.py') for n, _, _ in CP8.VARIANTES}
MUNDO = dict(S2.MUNDO)   # P1b + letra E (+0.3, -0.1) p_x 0.15; retenida 1 la fija cria()
CRIA = {'comp': 'O1_LUGAR_COMP', 'lug': 'O1_LUGAR', 'comp2': 'O1_LUGAR_COMP2'}
ORDEN = ('comp', 'lug', 'comp2')
# brazo de crianza -> [(brazo de pregunta, carro que pregunta, permutada)]
PREG = {'comp': [('comp', 'O1_LUGAR_COMP', 0), ('comp_perm', 'O1_LUGAR_COMP', 1)],
        'lug': [('lug', 'O1_LUGAR', 0), ('comp_s', 'O1_LUGAR_COMP', 0)],
        'comp2': [('comp2', 'O1_LUGAR_COMP2', 0), ('comp2_perm', 'O1_LUGAR_COMP2', 1), ('comp2sg', 'O1_LUGAR_COMP2SG', 0), ('lug2', 'O1_LUGAR', 0)]}
DE = {q: c for c, L in PREG.items() for q, _, _ in L}
NPERM = 8; ETQ_PERM = 7
SEM = dict(serie=737500, replica=737520, humo=737490, arnes=737402)
N_SERIE = 20; T_SERIE = 60000; POOL_MAX = 2
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000
# ---- la letra (PREREGISTRO_p8.md sec. 6; sobre 20 semillas, se escala con esc)
MIN_VAL = 3          # linajes validos minimos para que una semilla cuente en un brazo
SEM_VAL = 17         # semillas validas minimas por brazo de crianza (validez)
K_POS = 15           # semillas con D > 0
MED_FUN = 0.4; MED_MOD = 0.25
PERM_MAX = 0.1; FGEN_MAX = 0.05; B_MAX = 0.1
ELIGE_MIN = 0.75     # ENMIENDA 1 (ERR-179): P7 se mide en el MISMO bin y balanceada (nulo sin preferencia de letra = 0.5); antes: 0.9 sobre S2.elige
NB = 30; LADO_B = 5  # bins del carro (LG_NB) y distancia de A y E al cuerpo en la eleccion en el mismo bin
PAR_GANA = 14; PAR_MED = 0.2
CLAVES = ('L_E_dentro', 'L_E_fuera', 'L_E_fgen', 'L_D', 'L_A_dentro', 'L_B_dentro', 'S_E_dentro', 'S_E_fuera', 'elige_A', 'elige_E', 'eligeB_A', 'eligeB_E')


def esc(k, n): return math.ceil(k * n / 20 - 1e-9)


def modulo(nombre):
    if nombre in CARROS8:
        ruta = CARROS8[nombre]
        if open(ruta, 'rb').read() != CP8.todas()[nombre]: raise SystemExit(f"{ruta} != construye_p8 (correr construye_p8.py)")
        m = CV._MODS.get(nombre)
        if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
            spec = importlib.util.spec_from_file_location(f"carro_{nombre}", ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[nombre] = m
        return m, dict(carro=nombre, sha=h16(ruta), LUGAR=m.LUGAR, LUGAR_BARAJA=m.LUGAR_BARAJA, LUGAR_W=m.LUGAR_W, COMPONE=m.COMPONE, LG2=m.LG2)
    return RC.modulo(nombre)


def cria(seed, nombre, T, mundo, ret=1):
    """una corrida de crianza con el carro `nombre` -> (x de corre_v143.tarea, memorias por linaje, salida cruda)."""
    m, est = modulo(nombre); cap = S2.Capta(m); crudo = []; orig = P.run; MR.RETENIDA[0] = int(ret)
    est = dict(est, mundo={k: (list(v) if isinstance(v, tuple) else v) for k, v in mundo.items()}, retenida=int(ret))

    def run2(*a, **k):
        r = MR.run(*a, **dict(k, **mundo)); crudo.append(r); return r
    P.run = run2; CV._MODS[nombre] = cap
    try:
        x = CV.tarea((seed, nombre, T))
    finally:
        P.run = orig; CV._MODS[nombre] = m; MR.RETENIDA[0] = 0
    r = crudo[0]
    for l, d in zip(x['linajes'], r['linajes']): l['_oasis'] = d['_carrera'].get('oasis')
    x['tel'] = [dict(lugar=(dict(d['carro']['lugar'], st_lg_bono=d['carro'].get('lg_bono', 0), st_lg_apr=d['carro'].get('lg_apr', 0), st_lg_viajes=d['carro'].get('lg_viajes', 0))
                            if isinstance(d.get('carro'), dict) and 'lugar' in d['carro'] else None)) for d in r['linajes']]
    x['estado'] = est; x['oasis_info'] = r['pista'].get('oasis'); x['L'] = r['pista']['L']
    x['lg2_omit'] = sum((d['carro'].get('lg2_omit') or 0) for d in r['linajes'] if isinstance(d.get('carro'), dict))
    return x, [S2.memoria(cap.ult[i]) for i in range(len(r['linajes']))], r


def bins_enteros(L, z0, W=36):
    """bins (de NB) cuyas celdas estan TODAS dentro del oasis [z0, z0 + W)."""
    w = L // NB; cel = {(z0 + j) % L for j in range(W)}
    return [b for b in range(NB) if all((b * w + j) in cel for j in range(w))]


def elige_bin(mod, mem, L, z0):
    """ENMIENDA 1 (ERR-179): A contra E dentro del oasis EN EL MISMO BIN (mismo bono de lugar para las dos) y BALANCEADA: el cuerpo en el centro del bin,
    una letra a +LADO_B y la otra a -LADO_B, en los dos ordenes (lado y orden del diccionario): una preferencia de lado o un empate dan 0.5."""
    c = S2.carro_de(mod, mem, L); w = L // NB; nA = nE = n = 0
    for b in bins_enteros(L, z0):
        p = b * w + w // 2
        for e in S2.NIVELES:
            for g in S2.NIVELES:
                for k1, k2 in (('A', 'E'), ('E', 'A')):
                    a = c.actua(dict(t=0, pos=p, E=e, Ag=g, objs={(p + LADO_B) % L: k1, (p - LADO_B) % L: k2}, cuerpos=(('yo', p, None, None),), pizarra=()))
                    k = {1: k1, -1: k2}.get(int(a['mov'])); n += 1; nA += k == 'A'; nE += k == 'E'
    return dict(eligeB_A=round(nA / n, 4), eligeB_E=round(nE / n, 4)) if n else dict(eligeB_A=0.0, eligeB_E=0.0)


def _una(mod, mem, L, z0):
    return dict(S2.pregunta({'x': mod}, mem, L, z0)['x'], **elige_bin(mod, mem, L, z0))


def responde(mod, mem, L, z0, perm, seed, i):
    """las respuestas de un carro sobre una memoria; perm = 1: media sobre NPERM permutaciones de la memoria de lugar entre bins."""
    if not perm: return _una(mod, mem, L, z0)
    rg = np.random.default_rng([int(seed), int(i), ETQ_PERM]); acc = None
    for _ in range(NPERM):
        p = [int(z) for z in rg.permutation(len(mem['lugar']))]
        f = _una(mod, dict(mem, lugar=[mem['lugar'][j] for j in p], nl=[mem['nl'][j] for j in p]), L, z0)
        acc = f if acc is None else {k: acc[k] + f[k] for k in f}
    return {k: round(v / NPERM, 4) for k, v in acc.items()}


def no_cambia(mod, mem, L, z0):
    """validez: preguntar NO cambia la memoria (no hay resultado())."""
    c = S2.carro_de(mod, mem, L); antes = S2.memoria(c)
    for off in S2.DENTRO_OFF:
        for lev in ((0.3, 0.9), (0.9, 0.3), (0.7, 0.7)):
            for k in ('E', 'A', 'B'): S2.muerde(c, L, z0 + off, k, lev, True); S2.muerde(c, L, z0 + off + L // 2, k, lev, False)
            S2.elige(c, L, z0 + 18, lev)
    return S2.memoria(c) == antes and antes == mem


def linaje_fila(i, l, mem, oi, L, seed, qs):
    ob = oi['bins30']; lg = np.asarray(mem['lugar'], float); ox = (l.get('_oasis') or {}).get('x') or {}
    val = lambda k: ([round(s / mem['letras'][k][1], 4) for s in mem['letras'][k][0]] if k in mem['letras'] else None)
    cE = 'E' in mem['letras']; cA = 'A' in mem['letras']; est = int(l['fund_post10k'] == 0)
    d = dict(i=i, establecido=est, cruza=int(l['cruza_real']), conoce_E=int(cE), conoce_A=int(cA), mord_E=ox.get('mord'), mord_E_dentro=ox.get('mord_dentro'),
             recuerda_oasis=int(any((lg[b] > 0.05).any() for b in ob)), v_E=val('E'), v_A=val('A'), v_C=val('C'), v_B=val('B'),
             bono_oasis=[[round(float(z), 4) for z in lg[b]] for b in ob],
             valido=int(est and cE and cA and (ox.get('mord_dentro') or 0) == 0))
    d['resp'] = {q: responde(mod, mem, L, oi['z0'], perm, seed, i) for q, mod, perm in qs}
    return d


def trabajo(args):
    """UN trabajo (i, brazo de crianza): cria + pregunta; atrapa todo; escribe su JSON antes de volver; con reanuda salta el que ya existe sin aborto."""
    i, brazo, base, T, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"prueba_i{i:02d}_{brazo}.json"); previo = None
    if reanuda and os.path.exists(fin):
        try:
            x0 = json.load(open(fin, encoding='utf-8'))
            if not x0.get('aborto'): return x0
            previo = x0['aborto']
        except Exception as e: previo = f"json ilegible: {e}"[:200]
    t0 = time.time(); seed = base + i
    try:
        qs = [(q, modulo(n)[0], perm) for q, n, perm in PREG[brazo]]
        x, mems, r = cria(seed, CRIA[brazo], T, MUNDO)
        oi = x['oasis_info']; L = x['L']
        y = dict(tipo='prueba', i=i, brazo=brazo, aborto=None, **CO.fila(x, T))
        y['oasis_info'] = {k: oi.get(k) for k in ('z0', 'W', 'bins30', 'letra_x', 'efecto_x', 'p_x', 'retenida', 'ret_n', 'comp_dentro', 'comp_fuera')}
        y['L'] = L; y['memorias'] = mems; y['lg2_omit'] = x['lg2_omit']
        y['establecidos'] = sum(int(z == 0) for z in y['fund_post10k'])
        y['linajes_p8'] = [linaje_fila(j, l, mems[j], oi, L, seed, qs) for j, l in enumerate(x['linajes'])]
        y['E_dentro_fisica'] = dict(comp=oi['comp_dentro'].get('E'), mordidas=sum((d['mord_E_dentro'] or 0) for d in y['linajes_p8']))
        y['preg_no_cambia'] = bool(all(no_cambia(mod, mems[j], L, oi['z0']) for _, mod, _ in qs for j in range(len(mems))))
    except BaseException as e:   # noqa: nube-9
        y = dict(tipo='prueba', i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: y['reintento_de'] = previo
    y['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(y, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return y


def lee(carpeta):
    R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        R[d['brazo']][d['i']] = d
    return R, ab


def _spearman(a, b):
    if len(a) < 3 or len(set(a)) < 2 or len(set(b)) < 2: return None
    rk = lambda v: np.argsort(np.argsort(np.asarray(v, float), kind='stable'), kind='stable').astype(float)
    return round(float(np.corrcoef(rk(a), rk(b))[0, 1]), 3)


def brazo_q(R, q, I):
    """estadisticas de un brazo de pregunta, unidad = semilla. Semilla sin MIN_VAL linajes validos: D = None (cuenta EN CONTRA: 0)."""
    c = DE[q]; Ds = []; nv = []; extra = {k: [] for k in CLAVES}; todo_cero = True
    for i in I:
        x = R[c].get(i); ls = [l for l in (x['linajes_p8'] if x else []) if l['valido']]
        nv.append(len(ls))
        if len(ls) < MIN_VAL: Ds.append(None); continue
        Ds.append(round(st.median(l['resp'][q]['L_D'] for l in ls), 4))
        for k in CLAVES: extra[k].append(st.mean(l['resp'][q][k] for l in ls))
        todo_cero &= all(l['resp'][q]['L_D'] == 0 and l['resp'][q]['L_E_dentro'] == 0 for l in ls)
    D0 = [0.0 if d is None else d for d in Ds]; ok = [d for d in Ds if d is not None]
    return dict(n=len(I), semillas_validas=len(ok), linajes_validos=sum(nv), validos_por_semilla=nv, D_semilla=Ds, k_pos=sum(d > 0 for d in D0),
                D_mediana=(round(st.median(D0), 4) if D0 else None), D_media=(round(st.mean(D0), 4) if D0 else None), D_cero_exacto=bool(todo_cero and ok),
                spearman_D_vs_validos=_spearman([d for d in Ds if d is not None], [v for d, v in zip(Ds, nv) if d is not None]),
                **{k: (round(st.median(v), 4) if v else None) for k, v in extra.items()})


def lee_letra(R, n, abortos):
    I = list(range(n)); completo = all(len(R.get(b, {})) == n for b in ORDEN)
    X = [R[b][i] for b in ORDEN for i in R.get(b, {})]
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(x['coherente'] for x in X))
    v['V2_celda_retenida'] = bool(X and all(x['E_dentro_fisica']['mordidas'] == 0 and x['E_dentro_fisica']['comp'] == 0 and (x['oasis_info'].get('ret_n') or 0) > 0 and x['oasis_info'].get('retenida') == 1 for x in X))
    v['V3_preguntar_no_cambia'] = bool(X and all(x['preg_no_cambia'] for x in X))
    v['V4_estado'] = bool(X and all((x.get('estado') or {}).get('carro') == CRIA[x['brazo']] and (x.get('estado') or {}).get('retenida') == 1
                                    and (x.get('estado') or {}).get('mundo') == {k: (list(z) if isinstance(z, tuple) else z) for k, z in MUNDO.items()} for x in X)
                      and all((x['estado'].get('LG2', 0), x['estado'].get('COMPONE', 0)) == {'comp': (0, 1), 'lug': (0, 0), 'comp2': (1, 2)}[x['brazo']] for x in X))
    Q = {q: brazo_q(R, q, I) for q in DE} if completo else {}
    sv = esc(SEM_VAL, n)
    v['V5_semillas_validas'] = bool(Q and all(Q[b]['semillas_validas'] >= sv for b in ORDEN))
    valido = all(v.values())
    kp = esc(K_POS, n); out = dict(validez=v, umbrales=dict(k_pos=kp, semillas_validas=sv, par_gana=esc(PAR_GANA, n), MIN_VAL=MIN_VAL, MED_FUN=MED_FUN, MED_MOD=MED_MOD,
                                                          PERM_MAX=PERM_MAX, FGEN_MAX=FGEN_MAX, B_MAX=B_MAX, ELIGE_MIN=ELIGE_MIN, PAR_MED=PAR_MED), brazos=Q)
    if not completo:
        out.update(veredictos={'comp': 'NO SE LEE', 'comp2': 'NO SE LEE'}, mejora='NO SE LEE', en_umbral=False, puertas={}); return out
    P_ = {}; V = {}; um = False
    for c in ('comp', 'comp2'):
        a = Q[c]; pm = Q[c + '_perm']; lg = Q['lug']
        p = dict(P1_semillas_D_pos=a['k_pos'] >= kp, P2_mediana_fun=a['D_mediana'] >= MED_FUN, P2m_mediana_mod=a['D_mediana'] >= MED_MOD,
                 P3_permutada=abs(pm['D_mediana']) <= PERM_MAX, P4_sin_composicion_cero=bool(lg['D_cero_exacto']),
                 P5_fuera_general=(a['L_E_fgen'] is not None and a['L_E_fgen'] <= FGEN_MAX), P6_B_dentro_rechazada=(a['L_B_dentro'] is not None and a['L_B_dentro'] <= B_MAX),
                 P7_A_sobre_E=(a['eligeB_A'] is not None and a['eligeB_A'] >= ELIGE_MIN))
        ctrl = p['P3_permutada'] and p['P4_sin_composicion_cero'] and p['P5_fuera_general'] and p['P6_B_dentro_rechazada'] and p['P7_A_sobre_E']
        V[c] = ('NO SE LEE' if not valido else 'FUNCIONA' if (p['P1_semillas_D_pos'] and p['P2_mediana_fun'] and ctrl)
                else 'HAY ALGO MODESTO' if (p['P1_semillas_D_pos'] and p['P2m_mediana_mod'] and ctrl) else 'NO')
        P_[c] = p; um |= abs(a['k_pos'] - kp) <= 1
    d1 = [0.0 if d is None else d for d in Q['comp']['D_semilla']]; d2 = [0.0 if d is None else d for d in Q['comp2']['D_semilla']]
    dif = [round(b - a, 4) for a, b in zip(d1, d2)]; pg = esc(PAR_GANA, n)
    par = dict(gana=sum(x > 0 for x in dif), empata=sum(x == 0 for x in dif), pierde=sum(x < 0 for x in dif), dif_mediana=round(st.median(dif), 4), dif=dif)
    mejora = 'NO SE LEE' if not valido else ('COMP2 MEJORA' if (par['gana'] >= pg and par['dif_mediana'] >= PAR_MED) else 'COMP2 NO MEJORA')
    um |= abs(par['gana'] - pg) <= 1
    S = lambda b, k: sum(R[b][i][k] for i in I)
    tr = {b: dict(cruzan=S(b, 'cruzan'), establecidos=S(b, 'establecidos'), mundo_AC=med([R[b][i]['mundo_AC'] for i in I]), vida_med=med([R[b][i]['vida_med'] for i in I]),
                  R0_med=med([R[b][i]['R0_med'] for i in I]), mord_AC=S(b, 'mord_AC'), mord_BD=S(b, 'mord_BD'), lg2_omit=S(b, 'lg2_omit'),
                  linajes_validos=Q[b]['linajes_validos'], ratio_pasos_oasis=med([(R[b][i].get('oasis') or {}).get('ratio_pasos') for i in I])) for b in ORDEN}
    tr['pareado_cruzan'] = {f"{a}_vs_{b}": {k: z for k, z in CO.par(R[a], R[b], I).items() if k in ('gana', 'empata', 'pierde', 'suma_a', 'suma_b')} for a, b in (('comp2', 'lug'), ('comp2', 'comp'), ('comp', 'lug'))}
    out.update(puertas=P_, veredictos=V, pareado_comp2_vs_comp=par, mejora=mejora, en_umbral=bool(um), trampas=tr)
    return out


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  umbrales: {L['umbrales']}")
    for q, a in L['brazos'].items():
        log(f"  [{q:10s}] sem validas {a['semillas_validas']}/{a['n']} · linajes validos {a['linajes_validos']} · D>0 en {a['k_pos']} · D mediana {a['D_mediana']} media {a['D_media']} · "
            f"E dentro {a['L_E_dentro']} fuera {a['L_E_fuera']} fgen {a['L_E_fgen']} · B dentro {a['L_B_dentro']} · A dentro {a['L_A_dentro']} · A sobre E mismo bin {a['eligeB_A']} (E {a['eligeB_E']}; entre bins distintos {a['elige_A']}) · "
            f"sola E {a['S_E_dentro']}/{a['S_E_fuera']} · rho(D, validos) {a['spearman_D_vs_validos']} · D por semilla {a['D_semilla']}")
    for c, p in (L.get('puertas') or {}).items(): log(f"  puertas {c}: {p}")
    if L.get('pareado_comp2_vs_comp'): log(f"  pareado comp2 vs comp (D por semilla): {L['pareado_comp2_vs_comp']}")
    for b, t in (L.get('trampas') or {}).items(): log(f"  [trampa 5] {b}: {t}")


def verifica(log):
    ok = CO.verifica(log)
    for ruta, sha in SHAS_P8.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for nm, b in RC.CC.todas().items():
        if nm in ('O1_LUGAR_COMP', 'O1_LUGAR_COMP0'):
            igual = open(RC.CARROS[nm], 'rb').read() == b; ok &= igual; log(f"  carro {nm} == construye_c: {igual} (sha {h16(RC.CARROS[nm])})")
    for nm, b in CP8.todas().items():
        igual = os.path.exists(CARROS8[nm]) and open(CARROS8[nm], 'rb').read() == b; ok &= igual; log(f"  carro {nm} == construye_p8: {igual} (sha {h16(CARROS8[nm]) if os.path.exists(CARROS8[nm]) else 'NO EXISTE'})")
    log(f"  mundo_ret: {MR.construye()[1]}")
    return ok


def identidad(log, seed=SEM['arnes'], T=1500, largo=False):
    """ARNES: lo apagado == la base bit a bit (salida ENTERA de run, N 9, fundador limpio) + la celda retenida + el instrumento de pregunta."""
    N = lambda x: json.loads(json.dumps(x, default=str))
    lug, _ = modulo('O1_LUGAR'); comp, _ = modulo('O1_LUGAR_COMP'); c20, _ = modulo('O1_LUGAR_COMP2_0'); c2, _ = modulo('O1_LUGAR_COMP2'); c2sg, _ = modulo('O1_LUGAR_COMP2SG')
    kwE = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **MUNDO)
    R = {}; MR.RETENIDA[0] = 0
    bE = N(MC.run(seed, [('X', comp)] * 9, **kwE))
    R['M1 mundo_ret apagado == mundo_tramo_c (COMP, con E)'] = N(MR.run(seed, [('X', comp)] * 9, **kwE)) == bE
    R['M2 COMP2_0 (LG2 0, COMPONE 1) == O1_LUGAR_COMP (mundo_tramo_c con E)'] = N(MC.run(seed, [('X', c20)] * 9, **kwE)) == bE
    MR.RETENIDA[0] = 1
    rc = N(MR.run(seed, [('X', comp)] * 9, **kwE)); R['E1 retenida ENCIENDE'] = rc != bE
    R['M3 COMP2_0 == O1_LUGAR_COMP (mundo_ret, retenida 1)'] = N(MR.run(seed, [('X', c20)] * 9, **kwE)) == rc
    cap = S2.Capta(c2); r2 = MR.run(seed, [('X', cap)] * 9, **kwE); n2 = N(r2)
    R['E2 COMP2 ENCIENDE (difiere de COMP)'] = n2 != rc
    R['M4 COMP2 con el envoltorio Capta == sin el'] = N(MR.run(seed, [('X', c2)] * 9, **kwE)) == n2
    R['E3 LG2 actua (alguna mordida no actualizo la tabla)'] = sum((d['carro'].get('lg2_omit') or 0) for d in r2['linajes']) > 0
    MR.RETENIDA[0] = 0
    oi = r2['pista']['oasis']; L = r2['pista']['L']; z0 = oi['z0']
    R['F1 fisica: E nunca dentro (composicion 0, re-sorteos > 0) y 0 mordidas de E dentro'] = (oi['comp_dentro']['E'] == 0 and oi['ret_n'] > 0
                                                                                              and all(d['_carrera']['oasis']['x']['mord_dentro'] == 0 for d in r2['linajes']))
    mems = json.loads(json.dumps([S2.memoria(cap.ult[i]) for i in range(9)]))
    ok6 = True
    for i in range(9):
        c = S2.carro_de(c2, mems[i], L); o = cap.ult[i]
        ok6 &= set(c.n) == set(o.n) and all(c.n[k] == o.n[k] and (c.suma[k] == o.suma[k]).all() for k in o.n) and (c.lugar == o.lugar).all() and (c.nl == o.nl).all()
    R['M5 la memoria de COMP2 pasa por JSON y nace(memoria) la reconstruye bit a bit (cero memoria nueva)'] = bool(ok6)
    R['M6 COMP2 no guarda nada fuera de suma, n, lugar, nl (mismos atributos de instancia que COMP)'] = set(vars(c2.crea(dict(id='y', indice=0, L=L, rep_umbral=1.0, rng=None)))) == set(vars(comp.crea(dict(id='y', indice=0, L=L, rep_umbral=1.0, rng=None))))
    R['M7 preguntar NO cambia la memoria (los 4 carros)'] = all(no_cambia(m, mems[i], L, z0) for m in (c2, c2sg, comp, lug) for i in range(9))
    R['M8 en la pregunta, COMP2_0 == O1_LUGAR_COMP'] = all(responde(c20, mems[i], L, z0, 0, seed, i) == responde(comp, mems[i], L, z0, 0, seed, i) for i in range(9))
    be = bins_enteros(L, z0); w = L // NB; cel = {(z0 + j) % L for j in range(36)}
    R['B1 eleccion en el mismo bin: hay >= 2 bins enteros dentro del oasis y A y E caen en el mismo bin, dentro'] = (len(be) >= 2 and all(
        ((b * w + w // 2 + s * LADO_B) * NB) // L == b and (b * w + w // 2 + s * LADO_B) in cel for b in be for s in (1, -1)) and oi['W'] == 36 and c2.LG_NB == NB)
    R['B2 eleccion en el mismo bin: sin composicion (O1_LUGAR) elige A siempre; con memoria vacia de E... A = 1.0'] = all(elige_bin(lug, mems[i], L, z0)['eligeB_A'] == 1.0 for i in range(9) if 'A' in mems[i]['letras'] and 'E' in mems[i]['letras'])
    R['R1 la pregunta y la permutada son deterministas'] = all(responde(c2, mems[i], L, z0, p, seed, i) == responde(c2, mems[i], L, z0, p, seed, i) for i in range(9) for p in (0, 1))
    sin = dict(mems[0], lugar=[[0.0, 0.0] for _ in mems[0]['lugar']])
    R['C1 sin memoria de lugar D = 0 exacto en COMP y COMP2 (el instrumento no inventa D)'] = all(responde(m, sin, L, z0, 0, seed, 0)['L_D'] == 0 for m in (comp, c2))
    # candados y reanuda (en una carpeta temporal del arnes)
    import tempfile, shutil
    tmp = tempfile.mkdtemp(prefix='p8_arnes_')
    try:
        a1 = trabajo((0, 'comp2', seed, T, tmp, False)); t1 = os.path.getmtime(os.path.join(tmp, 'prueba_i00_comp2.json'))
        a2 = trabajo((0, 'comp2', seed, T, tmp, True))
        R['K1 trabajo escribe su JSON sin aborto y --reanuda NO lo re-corre (devuelve el mismo)'] = (a1.get('aborto') is None and os.path.getmtime(os.path.join(tmp, 'prueba_i00_comp2.json')) == t1
                                                                                                    and {k: v for k, v in a2.items()} == json.loads(json.dumps(a1)))
        json.dump(dict(tipo='prueba', i=0, brazo='lug', aborto='X: cortado'), open(os.path.join(tmp, 'prueba_i00_lug.json'), 'w'))
        a3 = trabajo((0, 'lug', seed, T, tmp, True))
        R['K2 --reanuda SI re-corre un JSON con aborto (y anota reintento_de)'] = a3.get('aborto') is None and a3.get('reintento_de') == 'X: cortado'
        open(os.path.join(tmp, 'prueba_i00_comp.json'), 'w').write('{"tipo": "pru')
        a4 = trabajo((0, 'comp', seed, T, tmp, True))
        R['K3 --reanuda re-corre un JSON truncado (corte de luz a mitad de escritura)'] = a4.get('aborto') is None and 'ilegible' in (a4.get('reintento_de') or '')
        Rr, ab = lee(tmp); Lt = lee_letra(Rr, 1, len(ab))
        R['K4 lee_letra corre de punta a punta sobre las 3 corridas del arnes (veredictos y mejora presentes)'] = set(Lt['veredictos']) == {'comp', 'comp2'} and 'mejora' in Lt
        R['K5 candado: guarda() niega la serie mientras algo no este commiteado (o todo esta limpio)'] = (guarda('serie', 'serie_arnes', False) is not None) or _git_limpio()
        R['K6 regla de parada: replica solo con FUNCIONA/MODESTO en algun brazo o NO en el umbral'] = (not parada([], None) and not parada(['NO', 'NO'], False) and parada(['NO', 'NO'], True)
                                                                                                    and parada(['NO', 'HAY ALGO MODESTO'], False) and parada(['FUNCIONA', 'NO'], False) and not parada(['NO SE LEE', 'NO SE LEE'], True))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = all(R.values())
    for k, v in R.items(): log(f"  {'OK   ' if v else 'FALLA'} {k}")
    log(f"  (T {T}: E retenidas {oi['ret_n']} · lg2_omit {sum((d['carro'].get('lg2_omit') or 0) for d in r2['linajes'])})")
    log(f"  ARNES P8: {sum(R.values())}/{len(R)} {'TODO OK' if ok else 'FALLA'} (s {seed}, T {T})")
    return ok


ARCHIVOS = lambda: [os.path.join(AQUI, 'PREREGISTRO_p8.md'), os.path.abspath(__file__), os.path.join(AQUI, 'construye_p8.py'), os.path.join(AQUI, 'nulo_p8.py'),
                    os.path.join(SON, 'mundo_ret.py'), os.path.join(SON, 'corre_s2.py')] + list(CARROS8.values())


def _git_limpio():
    import subprocess
    for r in ARCHIVOS():
        rel = os.path.relpath(r, RAIZ).replace(os.sep, '/')
        t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
        c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
        if not (t and c): return False
    return True


def parada(vs, um):
    """True = la replica SE PUEDE correr."""
    return bool(any(v in ('FUNCIONA', 'HAY ALGO MODESTO') for v in vs) or (vs and all(v == 'NO' for v in vs) and um))


def guarda(modo, pre, reanuda):
    """Candados de --serie/--replica: no se re-corre una carpeta con veredicto; carpetas previas solo con --reanuda; la replica solo si la serie dio
    FUNCIONA o MODESTO en algun brazo, o NO en el umbral (+-1), y con el mismo sha del runner; todo commiteado y sin cambios respecto de HEAD."""
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8')); vs = ((r.get('letra') or {}).get('veredictos') or {}).values()
            if r.get('modo') == modo and vs and all(v in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO') for v in vs): return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {list(vs)}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda (cortada o NO SE LEE)"
    if modo == 'replica':
        rsm = sorted(glob.glob(os.path.join(DATOS, f"serie_s{SEM['serie']}-*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = list(((rs0.get('letra') or {}).get('veredictos') or {}).values()); um = (rs0.get('letra') or {}).get('en_umbral')
        if not parada(vs, um):
            return f"REGLA DE PARADA: la replica solo si la serie da FUNCIONA o MODESTO en algun brazo, o NO EN EL UMBRAL; serie = {vs} (umbral {um})"
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)): return f"sha_runner de la serie {rs0.get('sha_runner')} != runner actual"
    if not _git_limpio(): return "git: preregistro, runner, constructor, nulo, mundo_ret, corre_s2 y carros deben estar commiteados y sin cambios vs HEAD"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--identidad', action='store_true')
    g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--n', type=int, default=None); ap.add_argument('--desde', type=int, default=None); ap.add_argument('--nota', default='')
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX}")
    if a.lee:
        R, ab = lee(os.path.abspath(a.lee)); n = max((len(R[b]) for b in ORDEN), default=0)
        L = lee_letra(R, n, len(ab)); imprime(L, print)
        print(f"VEREDICTO ({'parcial/humo, no cuenta' if n != N_SERIE else 'letra'}): {L['veredictos']} · {L['mejora']} · en umbral {L['en_umbral']} · abortos {ab}"); return 0
    BUF = []; LOGF = [None]

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    t0 = time.time()
    if a.identidad:
        log(f"CORRE_P8 · identidad · python {platform.python_version()} · corre_p8.py {h16(os.path.abspath(__file__))}")
        ok = verifica(log) and CO.identidad_corta(log) and RC.identidad_corta_c(log) and identidad(log)
        return 0 if ok else 1
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        modo = 'humo'; n = a.n or 2; T = a.T or T_SERIE; base = a.desde or SEM['humo']; dest = os.path.join(DATOS, 'humo')
        if len(ORDEN) * n > MAX_CORRIDAS_1P or T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(ORDEN) * n}) y <= {MAX_PASOS_1P} pasos")
    else:
        if a.T or a.n or a.desde: raise SystemExit("--serie/--replica: T, n y semillas los fija el preregistro")
        modo = 'serie' if a.serie else 'replica'; n = N_SERIE; T = T_SERIE; base = SEM[modo]; dest = DATOS
    pre = f"{modo}_s{base}-{base + n - 1}_T{T}"; sel = time.strftime('%Y%m%d_%H%M%S')
    prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
    if a.reanuda and not prev: raise SystemExit(f"--reanuda: no hay carpeta {pre}_* en {dest}")
    if modo in ('serie', 'replica'):
        e = guarda(modo, pre, a.reanuda)
        if e: raise SystemExit(f"NO SE CORRE (candado): {e}")
    carpeta = os.path.join(dest, prev[-1]) if (a.reanuda and prev) else os.path.join(dest, pre + '_' + sel)
    log(f"CORRE_P8 · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_p8.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  semillas {base}-{base + n - 1} · T {T} · crianza {CRIA} · mundo {MUNDO} + retenida 1 · reanuda {a.reanuda} · nota {a.nota!r}")
    ok = verifica(log) and CO.identidad_corta(log) and RC.identidad_corta_c(log) and identidad(log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    tareas = [(i, b, base, T, carpeta, a.reanuda) for i in range(n) for b in ORDEN]

    def fmt(x):
        if x.get('aborto'): return f"  [{time.time()-t0:7.1f}s] i{x['i']} {x['brazo']:5s} ABORTO {x['aborto']}"
        v = [l for l in x['linajes_p8'] if l['valido']]; q0 = PREG[x['brazo']][0][0]
        m = lambda k: (round(st.mean(l['resp'][q0][k] for l in v), 3) if v else None)
        return (f"  [{time.time()-t0:7.1f}s] i{x['i']} {x['brazo']:5s} ({x.get('seg')}s) cruzan {x['cruzan']}/9 estab {x['establecidos']} vida {x['vida_med']} mundo AC {x['mundo_AC']} · E dentro {x['E_dentro_fisica']} · "
                f"validos {len(v)}/9 · {q0}: E dentro {m('L_E_dentro')} fuera {m('L_E_fuera')} D {m('L_D')} B dentro {m('L_B_dentro')} A sobre E mismo bin {m('eligeB_A')} · no cambia {x['preg_no_cambia']}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): log(fmt(x))
    else:
        for tk in tareas: log(fmt(trabajo(tk)))
    R, ab = lee(carpeta); L = lee_letra(R, n, len(ab))
    log(f"\n================ LA LETRA (escalada a n {n})" + (" -- HUMO: NO cuenta, no se declara" if modo == 'humo' else ""))
    imprime(L, log)
    if ab: log(f"  ABORTOS: {ab}")
    pre_v = f"{modo.upper()} (no cuenta): " if modo == 'humo' else ''
    ver = f"{pre_v}COMP {L['veredictos']['comp']} · COMP2 {L['veredictos']['comp2']} · {L['mejora']}" + (' · EN EL UMBRAL (+-1)' if L['en_umbral'] else '')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, letra=L, abortos=ab, n=n, T=T, semillas=[base, base + n - 1], veredicto=ver, nota=a.nota, crianza=CRIA, preguntas={k: [list(z) for z in v] for k, v in PREG.items()},
                       mundo={k: (list(v) if isinstance(v, tuple) else v) for k, v in MUNDO.items()}, retenida=1, sha_runner=h16(os.path.abspath(__file__)),
                       shas={os.path.relpath(k, RAIZ): v for k, v in list(CO.SHAS.items()) + list(SHAS_P8.items())}, carros={**{k: h16(v) for k, v in CARROS8.items()}, 'O1_LUGAR_COMP': h16(RC.CARROS['O1_LUGAR_COMP'])},
                       mundo_ret=MR.construye()[1], pool=a.pool, seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {len(ab)} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO: {ver}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
