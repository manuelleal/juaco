"""CREADOR B — B-5 DESAMBIGUAR CODIGOS. Ejecuta PREREGISTRO_codigo.md (la LETRA de sus umbrales esta en UMBRALES, ERR-31).
REGLA 10: log desde el arranque, con fsync. REGLA 11: lista los python vivos antes de cualquier Pool; los subprocesos
con Pool van SECUENCIALES (nunca dos a la vez).

ETAPA 1  identidad interna (`identidad_codigo.py 30000`, SUBPROCESO de un proceso). Si no PASA, se para.
ETAPA 2  T1 examen v3' con la perilla ENCENDIDA (`bateria_v14_codigo.py 20 --desde 101 --log`, SUBPROCESO, su Pool)
         + comparacion de las listas `splits` por etapa con el examen de v14.1 en 101-120 (identidad de resultados).
ETAPA 3  T2 generalizacion (`bateria_generaliza_codigo.py organismo_v14_codigo_on 20 --desde 101 --log`, SUBPROCESO)
         + comparacion por semilla y regla con regresion_generaliza_organismo_v14_20260918_054926.json.
ETAPA 4  mundo vivo: 7 brazos x 9 semillas (63 corridas) con Pool AQUI (ya no queda ningun otro Pool vivo).
         Guarda G: los brazos con la perilla APAGADA deben reproducir el bloque de la sal semilla a semilla.
ETAPA 5  umbrales C1-C9, T1-T3 del preregistro. JSON + log en datos/.

Uso:  python experimentos/creacion_B/corre_codigo.py
      python experimentos/creacion_B/corre_codigo.py --humo    (UN proceso, sin Pool: identidad corta + 6 corridas)
"""
import sys, os, json, time, hashlib, platform, subprocess, re, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
NIV11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI, NIV11]   # organismo/ PRIMERO (ERR-28)

import diagnostico_codigos as DC   # seleccion estructural de semillas (nivel 11), importado sin copiar

T = 100000
N_PARALELO = 14
HUMO = '--humo' in sys.argv
ALIAS = [326, 334, 343, 377, 446, 533, 549, 563, 670]
LIMPIAS = [307, 313, 316, 323, 325, 327, 333, 338, 342]
SAL_MUDA = {'comida': (+0.8, 0.0), 'veneno': (-0.4, 0.0), 'agua': (0.0, +0.8), 'sal': (0.0, 0.0)}
BASE = dict(vivo=1, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001, n_nec=2, tabla=SAL_MUDA)   # = NO_INFORMA de mini_vivo
BRAZOS = {   # nombre: (kwargs, semillas)
    'D0-ALIAS':  (dict(BASE, desambiguar=0), ALIAS),
    'D1-ALIAS':  (dict(BASE, desambiguar=1), ALIAS),
    'D0-LIMPIA': (dict(BASE, desambiguar=0), LIMPIAS),
    'D1-LIMPIA': (dict(BASE, desambiguar=1), LIMPIAS),
    'D1-SINSED': (dict(BASE, desambiguar=1, n_nec=1), ALIAS),
    'D0-VIVO':   (dict(vivo=1, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001, n_nec=2, desambiguar=0), ALIAS),
    'D1-VIVO':   (dict(vivo=1, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001, n_nec=2, desambiguar=1), ALIAS),
}
ORDEN = list(BRAZOS)
REF_SAL = os.path.join(RAIZ, 'datos', 'sal_alias9_20260918_081346.json')                       # bloque de la sal (d521f569205ebcfd)
REF_EXAMEN = os.path.join(RAIZ, 'datos', 'examen_v14_e015c10_20260918_053452.log')             # examen de v14.1 en 101-120
REF_GEN = os.path.join(RAIZ, 'datos', 'regresion_generaliza_organismo_v14_20260918_054926.json')   # generalizacion de v14.1 en 101-120
SEIS = ['E1', 'E2', 'E2I', 'E2J', 'E2K', 'E2L']

# ---------------------------------------------------------------- UMBRALES: la LETRA del preregistro (ERR-31)
UMBRALES = {
    'G':  dict(frase="D0-ALIAS y D0-LIMPIA identicos al JSON del bloque de la sal en w_sal, w_veneno, splits, celdas, deaths: 18/18"),
    'C1': dict(frase="D1-ALIAS |W[sal]| <= 0.3 en >= 8/9, mediana <= 0.1", w=0.3, n_min=8, med_max=0.1),
    'C2': dict(frase="D1-ALIAS W_hambre[veneno] <= -2.8 en >= 8/9 y <= -2.5 en 9/9", w1=-2.8, n1=8, w2=-2.5, n2=9),
    'C3': dict(frase="exposiciones a la sal de D1-ALIAS <= 1.5 x la mediana de D1-LIMPIA en >= 8/9", factor=1.5, n_min=8),
    'C4': dict(frase="des_splits >= 1 en D1-ALIAS 9/9; la primera division por R=0 es en una mordida de D en >= 8/9", n1=9, n2=8),
    'C5': dict(frase="D1-ALIAS y D1-LIMPIA celdas <= 45 en 18/18; mediana de celdas <= 40", celdas=45, med_max=40),
    'C6': dict(frase="D1-LIMPIA |W[sal]| <= 0.3 en 9/9 y W_hambre[veneno] <= -2.8 en 9/9", w=0.3, wv=-2.8, n_min=9),
    'C7': dict(frase="D1-SINSED cumple C1 (|W[sal]| <= 0.3) y C2 (W[veneno] <= -2.8) en >= 8/9 cada uno", w=0.3, wv=-2.8, n_min=8),
    'C8': dict(frase="tabla 2x2 en D1-VIVO: |W_h[sal]|<=0.3, W_s[sal]<=-2.5, W_h[ven]<=-2.8, |W_s[ven]|<=0.3 (las cuatro) en >= 7/9; en D0-VIVO falla en >= 7/9",
               n_min=7),
    'C9': dict(frase="muertes D1-ALIAS <= 0.8 x D0-ALIAS (medianas; se reporta A12)", factor=0.8),
    'T1': dict(frase="examen v3' 8/8 en 101-120 con la perilla ON, y listas splits por etapa identicas a v14.1"),
    'T2': dict(frase="G1 >= 0.80, G2 >= 0.85, K 20/20, y acc/ba/splits/celdas/deaths identicos por semilla y regla a v14.1 (40/40)",
               g1=0.80, g2=0.85),
    'T3': dict(frase="coste en el tronco 0 % exacto (se sigue de T1/T2)"),
}

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(np.median(xs)), 3) if xs else None


def resumen(brazo, seed, r):
    W = r['W_nec']
    return dict(tipo='R', brazo=brazo, seed=seed, desambiguar=r['desambiguar'],
                w_sal=round(max(abs(W[n]['D']) for n in range(len(W))), 3),
                w_sal_por_nec=[round(W[n]['D'], 3) for n in range(len(W))],
                w_veneno=round(W[0]['B'], 3),
                w_veneno_por_nec=[round(W[n]['B'], 3) for n in range(len(W))],
                exp_sal=r['exposiciones']['D'], exp_veneno=r['exposiciones']['B'], exposiciones=r['exposiciones'],
                splits=r['splits'], des_splits=r['des_splits'], des_t=r['des_t'][:12], split_t=r['split_t'][:12],
                celdas=r['celdas'], deaths=r['deaths'], muertes_nec=r['muertes_nec'], W_nec=W, exp_hasta=r['exp_hasta'])


def tarea(args):
    _, brazo, seed, Ti = args
    import organismo_vivo_codigo as VC
    return resumen(brazo, seed, VC.run(seed, T=Ti, **BRAZOS[brazo][0]))


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_codigo.md')), script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_codigo.py')), identidad=h16(os.path.join(AQUI, 'identidad_codigo.py')),
    organismo_v14_codigo=h16(os.path.join(AQUI, 'organismo_v14_codigo.py')),
    organismo_v14_codigo_on=h16(os.path.join(AQUI, 'organismo_v14_codigo_on.py')),
    organismo_v14g_codigo_on=h16(os.path.join(AQUI, 'organismo_v14g_codigo_on.py')),
    organismo_vivo_codigo=h16(os.path.join(AQUI, 'organismo_vivo_codigo.py')),
    bateria_v14_codigo=h16(os.path.join(AQUI, 'bateria_v14_codigo.py')),
    bateria_generaliza_codigo=h16(os.path.join(AQUI, 'bateria_generaliza_codigo.py')),
    origen_organismo_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
    origen_organismo_vivo=h16(os.path.join(NIV11, 'organismo_vivo.py')),
    ref_sal=h16(REF_SAL) if os.path.exists(REF_SAL) else None,
    ref_examen=h16(REF_EXAMEN) if os.path.exists(REF_EXAMEN) else None,
    ref_generaliza=h16(REF_GEN) if os.path.exists(REF_GEN) else None)


def guarda_semillas():
    a = [s for s in range(301, 701) if DC.solapamientos(s)['D&B'] >= 3]
    ok_a = (a == ALIAS); ok_l = all(DC.solapamientos(s)['D&B'] == 0 for s in LIMPIAS)
    log(f"    ALIAS recalculadas en 301-700: {a} -> {'coinciden' if ok_a else '*** NO COINCIDEN'}; LIMPIAS |D&B|=0: {'9/9' if ok_l else '*** no'}")
    return ok_a and ok_l


def sub(cmd, etq):
    log(f"   -> SUBPROCESO ({etq}): {' '.join(os.path.basename(c) if i == 0 else c for i, c in enumerate(cmd))}")
    t0 = time.time()
    p = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, cwd=AQUI, encoding='utf-8', errors='replace')
    cola = [l for l in (p.stdout or '').strip().splitlines()[-16:]]
    for l in cola:
        log(f"      | {l}")
    if p.returncode != 0:
        log(f"      *** codigo {p.returncode}; stderr: {(p.stderr or '')[-600:]}")
    log(f"      ({time.time()-t0:.0f}s)")
    return dict(etq=etq, cmd=cmd, returncode=p.returncode, cola=cola)


def splits_por_etapa(ruta_log):
    """Lee del log de una bateria_v14 las listas splits y celdas_max de las seis etapas (identidad de resultados, T1)."""
    out = {}
    lineas = open(ruta_log, encoding='utf-8', errors='replace').read().splitlines()
    for i, l in enumerate(lineas):
        m = re.search(r"\b1 (E1|E2|E2I|E2J|E2K|E2L)\s+(\d+)/(\d+)", l)
        if m and i + 1 < len(lineas):
            m2 = re.search(r"splits=(\[[^\]]*\])\s+celdas_max=(\d+)", lineas[i + 1])
            if m2:
                out[m.group(1)] = dict(pasan=int(m.group(2)), splits=json.loads(m2.group(1)), celdas_max=int(m2.group(2)))
    return out


# ---------------------------------------------------------------- veredicto (umbrales EXACTOS del preregistro)
def veredicto(res, log=log):
    G = {b: {r['seed']: r for r in res if r['brazo'] == b} for b in ORDEN}
    V = {'umbrales': UMBRALES}
    for b in ORDEN:
        g = [G[b][s] for s in sorted(G[b])]
        if not g:
            continue
        log(f"   {b:10s} n={len(g)}  |W[sal]| med {med([r['w_sal'] for r in g])}  W[veneno] med {med([r['w_veneno'] for r in g])}"
            f"  exp sal med {med([r['exp_sal'] for r in g])}  splits med {med([r['splits'] for r in g])} (R=0: {med([r['des_splits'] for r in g])})"
            f"  celdas med {med([r['celdas'] for r in g])}  muertes med {med([r['deaths'] for r in g])}")
        log(f"        |W[sal]| {[r['w_sal'] for r in g]}   W[ven] {[r['w_veneno'] for r in g]}   celdas {[r['celdas'] for r in g]}   des_splits {[r['des_splits'] for r in g]}")
    A0, A1, L0, L1, S1, V0, V1 = (G.get(b, {}) for b in ORDEN)
    hay = lambda *ds: all(d for d in ds)

    # G: guardas contra el bloque de la sal
    if os.path.exists(REF_SAL) and hay(A0, L0):
        ref = json.load(open(REF_SAL, encoding='utf-8'))['principal']
        R = {(r['brazo'], r['seed']): r for r in ref}
        n = 0; difs = []
        for b, bb in (('D0-ALIAS', 'S1-ALIAS'), ('D0-LIMPIA', 'S1-LIMPIA')):
            for s, r in G[b].items():
                q = R.get((bb, s))
                same = q is not None and all(r[k] == q[k] for k in ('w_sal', 'w_veneno', 'splits', 'celdas', 'deaths'))
                n += same
                if not same:
                    difs.append((b, s))
        V['G'] = dict(n=n, difs=difs, pasa=bool(n == 18))
        log(f"   G  {UMBRALES['G']['frase']}  -> {n}/18 {'PASA' if V['G']['pasa'] else 'NO: ' + str(difs[:4])}")

    u = UMBRALES['C1']
    if A1:
        n = sum(r['w_sal'] <= u['w'] for r in A1.values()); m = med([r['w_sal'] for r in A1.values()])
        V['C1'] = dict(n=n, med=m, pasa=bool(n >= u['n_min'] and m is not None and m <= u['med_max']))
        log(f"   C1 {u['frase']}  -> {n}/{len(A1)} (mediana {m})  {'PASA' if V['C1']['pasa'] else 'NO'}")
    u = UMBRALES['C2']
    if A1:
        n1 = sum(r['w_veneno'] <= u['w1'] for r in A1.values()); n2 = sum(r['w_veneno'] <= u['w2'] for r in A1.values())
        V['C2'] = dict(n1=n1, n2=n2, med=med([r['w_veneno'] for r in A1.values()]), pasa=bool(n1 >= u['n1'] and n2 >= u['n2']))
        log(f"   C2 {u['frase']}  -> {n1}/{len(A1)} y {n2}/{len(A1)} (mediana {V['C2']['med']})  {'PASA' if V['C2']['pasa'] else 'NO'}")
    u = UMBRALES['C3']
    if hay(A1, L1):
        ref = med([r['exp_sal'] for r in L1.values()]); n = sum(r['exp_sal'] <= u['factor'] * ref for r in A1.values()) if ref else 0
        V['C3'] = dict(n=n, ref_limpias=ref, med_alias=med([r['exp_sal'] for r in A1.values()]), pasa=bool(ref and n >= u['n_min']))
        log(f"   C3 {u['frase']}  -> limpias {ref}, alias {V['C3']['med_alias']}, {n}/{len(A1)}  {'PASA' if V['C3']['pasa'] else 'NO'}")
    u = UMBRALES['C4']
    if A1:
        n1 = sum(r['des_splits'] >= 1 for r in A1.values())
        n2 = sum(bool(r['des_t']) and r['des_t'][0][1] == 'D' for r in A1.values())
        V['C4'] = dict(n1=n1, n2=n2, primeras=[(r['des_t'][0] if r['des_t'] else None) for r in A1.values()], pasa=bool(n1 >= u['n1'] and n2 >= u['n2']))
        log(f"   C4 {u['frase']}  -> {n1}/{len(A1)} y {n2}/{len(A1)}  {'PASA' if V['C4']['pasa'] else 'NO'}")
    u = UMBRALES['C5']
    if hay(A1, L1):
        cs = [r['celdas'] for r in list(A1.values()) + list(L1.values())]
        n = sum(c <= u['celdas'] for c in cs); m = med(cs)
        V['C5'] = dict(n=n, med=m, max=max(cs), pasa=bool(n == 18 and m <= u['med_max']))
        log(f"   C5 {u['frase']}  -> {n}/18, mediana {m}, max {max(cs)}  {'PASA' if V['C5']['pasa'] else 'NO'}")
    u = UMBRALES['C6']
    if L1:
        n1 = sum(r['w_sal'] <= u['w'] for r in L1.values()); n2 = sum(r['w_veneno'] <= u['wv'] for r in L1.values())
        V['C6'] = dict(n1=n1, n2=n2, des=med([r['des_splits'] for r in L1.values()]), pasa=bool(n1 >= u['n_min'] and n2 >= u['n_min']))
        log(f"   C6 {u['frase']}  -> {n1}/{len(L1)} y {n2}/{len(L1)} (des_splits mediana {V['C6']['des']})  {'PASA' if V['C6']['pasa'] else 'NO'}")
    u = UMBRALES['C7']
    if S1:
        n1 = sum(r['w_sal'] <= u['w'] for r in S1.values()); n2 = sum(r['w_veneno'] <= u['wv'] for r in S1.values())
        V['C7'] = dict(n1=n1, n2=n2, pasa=bool(n1 >= u['n_min'] and n2 >= u['n_min']))
        log(f"   C7 {u['frase']}  -> {n1}/{len(S1)} y {n2}/{len(S1)}  {'PASA' if V['C7']['pasa'] else 'NO'}")
    u = UMBRALES['C8']
    tabla = lambda r: (abs(r['W_nec'][0]['D']) <= 0.3 and r['W_nec'][1]['D'] <= -2.5 and r['W_nec'][0]['B'] <= -2.8 and abs(r['W_nec'][1]['B']) <= 0.3)
    if hay(V1, V0):
        n1 = sum(tabla(r) for r in V1.values()); n0 = sum(not tabla(r) for r in V0.values())
        V['C8'] = dict(n_on=n1, n_off_falla=n0,
                       tabla_on=[[r['W_nec'][0]['D'], r['W_nec'][1]['D'], r['W_nec'][0]['B'], r['W_nec'][1]['B']] for r in V1.values()],
                       tabla_off=[[r['W_nec'][0]['D'], r['W_nec'][1]['D'], r['W_nec'][0]['B'], r['W_nec'][1]['B']] for r in V0.values()],
                       pasa=bool(n1 >= u['n_min'] and n0 >= u['n_min']))
        log(f"   C8 {u['frase']}  -> ON exacta {n1}/{len(V1)}, OFF falla {n0}/{len(V0)}  {'PASA' if V['C8']['pasa'] else 'NO'}")
        log(f"        [W_h[sal], W_s[sal], W_h[ven], W_s[ven]] ON: {V['C8']['tabla_on']}")
        log(f"        OFF: {V['C8']['tabla_off']}")
    u = UMBRALES['C9']
    if hay(A1, A0):
        m1 = med([r['deaths'] for r in A1.values()]); m0 = med([r['deaths'] for r in A0.values()])
        a12 = float(np.mean([[x < y for y in [r['deaths'] for r in A0.values()]] for x in [r['deaths'] for r in A1.values()]]))
        V['C9'] = dict(med_on=m1, med_off=m0, razon=(round(m1 / m0, 3) if m0 else None), A12=round(a12, 3), pasa=bool(m0 and m1 <= u['factor'] * m0))
        log(f"   C9 {u['frase']}  -> {m1} contra {m0} (razon {V['C9']['razon']}, A12 {V['C9']['A12']})  {'PASA' if V['C9']['pasa'] else 'NO'}")
    return V


def frase_final(V):
    c = lambda k: (V.get(k) or {}).get('pasa')
    if not c('G'):
        return "GUARDA G CAIDA: la perilla apagada no reproduce el bloque de la sal; el instrumento cambio. Nada se lee."
    if c('C1') and c('C2'):
        s = ("DESAMBIGUAR FUNCIONA: cuando una celda consolidada recibe R = 0 bajo una retina distinta y divide, el estimulo que no informa "
             "se queda sin valor y el veneno conserva el miedo. ")
    else:
        s = "DESAMBIGUAR NO SEPARA como estaba escrito (C1/C2 caen): se registra el fallo; la siguiente variante va en otro preregistro. "
    s += ("La evitacion desaparece (C3). " if c('C3') else "La evitacion NO desaparece (C3 cae). ")
    s += ("Coste dentro del presupuesto (C5) y sin regresion en semillas limpias (C6). " if (c('C5') and c('C6')) else
          "*** COSTE o REGRESION en limpias (C5/C6): aunque separe, no es candidato tal cual. ")
    s += ("Vale en el tronco con cuatro estimulos (C7). " if c('C7') else "En el tronco con cuatro estimulos no (C7). ")
    s += ("La tabla 2x2 sal/veneno x hambre/sed sale exacta (C8). " if c('C8') else "La tabla 2x2 no sale exacta (C8). ")
    return s + "T1/T2/T3 se leen en sus logs: deben ser IDENTIDAD con v14.1. Nueve semillas por brazo piden replica."


# ---------------------------------------------------------------- humo (UN proceso, sin Pool, regla 3)
def humo():
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'codigo_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO del creador B, UN proceso, sin Pool (regla 3). PREREGISTRO_codigo.md ya escrito (sus umbrales no se tocan).")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    log("1/3 seleccion de semillas (diagnostico estructural, sin correr el organismo)")
    ok = guarda_semillas()
    log("2/3 IDENTIDAD corta (T=20000, subproceso de un proceso)")
    r1 = sub([os.path.join(AQUI, 'identidad_codigo.py'), '20000'], 'identidad')
    log(f"3/3 SEIS corridas, T={T}: ALIAS 326 off/on, LIMPIA 307 off/on, SINSED 326 on, VIVO 326 on")
    res, t_b = [], {}
    for b, s in (('D0-ALIAS', 326), ('D1-ALIAS', 326), ('D0-LIMPIA', 307), ('D1-LIMPIA', 307), ('D1-SINSED', 326), ('D1-VIVO', 326)):
        t1 = time.time(); r = tarea(('R', b, s, T)); t_b[b] = round(time.time() - t1, 2); res.append(r)
        log(f"    {b:10s} s{s}  {t_b[b]:5.2f}s  |W[sal]| {r['w_sal']} {r['w_sal_por_nec']}  W[veneno] {r['w_veneno']} {r['w_veneno_por_nec']}"
            f"  exp sal {r['exp_sal']} (ven {r['exp_veneno']})  splits {r['splits']} (R=0: {r['des_splits']})  celdas {r['celdas']}  muertes {r['deaths']}")
        if r['des_t']:
            log(f"               primeras divisiones por R=0: {r['des_t'][:6]}")
    ref = None
    if os.path.exists(REF_SAL):
        R = {(r['brazo'], r['seed']): r for r in json.load(open(REF_SAL, encoding='utf-8'))['principal']}
        for b, bb in (('D0-ALIAS', 'S1-ALIAS'), ('D0-LIMPIA', 'S1-LIMPIA')):
            r = [x for x in res if x['brazo'] == b][0]; q = R.get((bb, r['seed']))
            same = q is not None and all(r[k] == q[k] for k in ('w_sal', 'w_veneno', 'splits', 'celdas', 'deaths'))
            log(f"    guarda G: {b} s{r['seed']} {'REPRODUCE' if same else '*** NO REPRODUCE'} el bloque de la sal ({bb})")
            ref = (ref is None or ref) and same
    log("HUMO: n=1 por brazo, semillas ya vistas por el bloque de la sal. NO es evidencia: prueba que mide y calibra las predicciones.")
    dj = os.path.join(RAIZ, 'datos', f'codigo_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T=T, semillas_ok=ok, guarda_G=ref,
                             umbrales=UMBRALES, shas=SHAS(), segundos_por_brazo=t_b, python=platform.python_version(), numpy=np.__version__),
                   identidad=r1, brazos=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


# ---------------------------------------------------------------- principal
if __name__ == '__main__':
    if HUMO:
        humo(); sys.exit(0)
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    if '--T' in sys.argv:
        T = int(sys.argv[sys.argv.index('--T') + 1])
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'codigo_alias{len(ALIAS)}_{stamp}'
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE B-5 DESAMBIGUAR (nivel 4): brazos {ORDEN}, ALIAS {ALIAS}, LIMPIAS {LIMPIAS}, T={T}.")
    for k, v in SHAS().items():
        log(f"    sha {k:26s} {v}")
    if not guarda_semillas():
        log("*** La seleccion de semillas del preregistro no se reproduce. Se para."); sys.exit(1)
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    log("ETAPA 1/5 — identidad interna (subproceso de un proceso).")
    r1 = sub([os.path.join(AQUI, 'identidad_codigo.py'), '30000'], 'identidad')
    V['identidad'] = bool(r1['returncode'] == 0 and any('VEREDICTO identidad_codigo: PASA' in l for l in r1['cola']))
    if not V['identidad']:
        log("*** IDENTIDAD NO PASA. Se para."); _log['f'].close(); sys.exit(1)

    log("ETAPA 2/5 — T1: examen v3' con la perilla ENCENDIDA, 101-120 (subproceso; trae su Pool).")
    r2 = sub([os.path.join(AQUI, 'bateria_v14_codigo.py'), '20', '--desde', '101', '--log'], 'T1 examen')
    logs = sorted(glob.glob(os.path.join(RAIZ, 'datos', 'examen_codigo_*.log')))
    if logs and os.path.exists(REF_EXAMEN):
        nuevo = splits_por_etapa(logs[-1]); ref = splits_por_etapa(REF_EXAMEN)
        ocho = any('1_cientificos=True' in l and '4d_causa=True' in l and 'False' not in l for l in r2['cola'])
        iguales = [e for e in SEIS if e in nuevo and e in ref and nuevo[e] == ref[e]]
        V['T1'] = dict(ocho_de_ocho=ocho, etapas_identicas=iguales, pasa=bool(ocho and len(iguales) == 6))
        log(f"   T1 {UMBRALES['T1']['frase']}  -> 8/8: {ocho}; etapas con splits identicos a v14.1: {len(iguales)}/6  {'PASA' if V['T1']['pasa'] else 'NO'}")

    log("ETAPA 3/5 — T2: generalizacion con la perilla ENCENDIDA, 101-120 (subproceso; trae su Pool).")
    r3 = sub([os.path.join(AQUI, 'bateria_generaliza_codigo.py'), 'organismo_v14_codigo_on', '20', '--desde', '101', '--log'], 'T2 generalizacion')
    js = sorted(glob.glob(os.path.join(RAIZ, 'datos', 'regresion_generaliza_codigo_organismo_v14_codigo_on_*.json')))
    if js and os.path.exists(REF_GEN):
        a = json.load(open(js[-1], encoding='utf-8')); b = json.load(open(REF_GEN, encoding='utf-8'))
        A = {(r['regla'], r['seed']): r for r in a['corridas']}; B = {(r['regla'], r['seed']): r for r in b['corridas']}
        n = sum(k in B and all(A[k][f] == B[k][f] for f in ('acc', 'ba', 'cobertura', 'splits', 'celdas', 'deaths')) for k in A)
        ver = a['meta']['veredictos']
        V['T2'] = dict(veredictos=ver, identicas=n, de=len(A), pasa=bool(all(ver.values()) and n == len(A) == 40))
        log(f"   T2 {UMBRALES['T2']['frase']}  -> {ver}; identicas a v14.1: {n}/{len(A)}  {'PASA' if V['T2']['pasa'] else 'NO'}")
    V['T3'] = dict(pasa=bool((V.get('T1') or {}).get('pasa') and (V.get('T2') or {}).get('pasa')), frase="0 % exacto si T1 y T2 son identidad")

    log(f"ETAPA 4/5 — mundo vivo: {sum(len(v[1]) for v in BRAZOS.values())} corridas de {T} pasos ({len(BRAZOS)} brazos). Pool({N_PARALELO}) aqui.")
    res = []
    with mp.Pool(N_PARALELO) as pool:
        tr = [('R', b, s, T) for b, (_, ss) in BRAZOS.items() for s in ss]
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 9 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")
    log()
    log("ETAPA 5/5 — umbrales EXACTOS de PREREGISTRO_codigo.md (ERR-31).")
    V.update(veredicto(res))
    ver = frase_final(V)
    log(); log(f"VEREDICTO: {ver}")
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), T=T, alias=ALIAS, limpias=LIMPIAS,
                brazos={b: {k: (list(v) if isinstance(v, tuple) else v) for k, v in kw.items()} for b, (kw, _) in BRAZOS.items()},
                veredicto=ver, veredictos=V, etapas=[r1, r2, r3], procesos_python=ps, shas=SHAS(),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta, principal=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
