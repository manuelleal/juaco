"""Nivel 6, bloque SUBIDA_N6B — DOS metas en el mundo partido, mapa COMPLETO por exploracion saciada, sobre el TRONCO v14.2.
Corredor de PREREGISTRO_n6b.md.

Mundo D (principal): toro 11 x 11 partido por dos murallas de veneno (fila 0 con UN hueco; fila -5 entera), r_vis=1,
regen=50, T=100000. DOS comidas: A1 arriba, A2 abajo. 40 episodios por corrida (20 'cruza' + 20 'desvia', balanceados
por construccion), sin aprendizaje y sin boca. Mundo P (puerta de port): el mundo de subida_n6 (una comida).
Organismo: TRONCO v14.2 (kwargs leidos con inspect de organismo/organismo_v142.run), salvo GFX_13 (v13).

Brazos (11): CIEGO · GF (lectura de subida_n6) · GFV (+vista) · GFX (CANDIDATO: +explora) · GFVX (+vista+explora) ·
BRUJULA (GFX; el veneno recordado no bloquea el campo: control que puede ganar en 'cruza' si el mapa no importa) ·
BARAJADO · INVERTIDO · PLACEBO (GFX + 3 sorteos descartados) · GFX_13 (GFX sobre v13, reportado) · UNA (GFX en el mundo P).

Uso (banderas desconocidas o abreviadas -> ABORTA; ERR-115):
  python experimentos/subida_n6b/corre_subida_b.py --humo                          (1 proceso, 6 corridas, T=100000, semilla 14641)
  python experimentos/subida_n6b/corre_subida_b.py --desde 14601 --n 20 --pool 6   (SOLO el coordinador)
  python experimentos/subida_n6b/corre_subida_b.py --desde 14621 --n 20 --pool 6   (SOLO el coordinador)
  python experimentos/subida_n6b/corre_subida_b.py --lee <serie.json> --sello <sha16> [--lee_replica <rep.json> --sello_replica <sha16>]
"""
import argparse, datetime, hashlib, inspect, json, os, statistics, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))          # ERR-28: organismo/ SIEMPRE primero
sys.path.insert(1, AQUI)

SHA_MUNDO = '214d5763758473fa'          # mundo_subida_b.py (construye_subida_b.py)
SHA_TRONCO = '17528d767fcebaf6'         # organismo/organismo_v142.py (CONGELADO)
TRONCO_DECLARADO = dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05,
                        puerta_pat=5, pat_shuf=0, pat_min=1, desambiguar=1)   # PREREGISTRO §3; se contrasta con inspect
MUNDOS = {   # PREREGISTRO §3: fijados ANTES del humo
    'D': dict(ancho=11, alto=11, cierre=5, d_ini=4, metas2=True, min_salidas=3, margen=2, p_max=18),
    'P': dict(ancho=11, alto=11, cierre=5, d_ini=4),
}
R_VIS, REGEN, T_DEF, N_TEL, MAX_PASOS, E_TEST = 1, 50, 100000, 40, 60, 0.3
GF = dict(usa_M=True, camino=1, grad=1, filtro=1)
BRAZOS = {   # nombre -> (mundo, organismo, kwargs de run, extras de prueba)
    'CIEGO':     ('D', 'v142', dict(usa_M=False, camino=0), {}),
    'GF':        ('D', 'v142', dict(GF), {}),
    'GFV':       ('D', 'v142', dict(GF, vista=1), {}),
    'GFX':       ('D', 'v142', dict(GF, explora=1), {}),
    'GFVX':      ('D', 'v142', dict(GF, vista=1, explora=1), {}),
    'BRUJULA':   ('D', 'v142', dict(GF, explora=1, brujula=1), {}),
    'BARAJADO':  ('D', 'v142', dict(GF, explora=1), dict(barajar=True)),
    'INVERTIDO': ('D', 'v142', dict(GF, explora=1), dict(invertir=True)),
    'PLACEBO':   ('D', 'v142', dict(GF, explora=1, placebo=3), {}),
    'GFX_13':    ('D', 'v13', dict(GF, explora=1), {}),
    'UNA':       ('P', 'v142', dict(GF, explora=1), {}),
}
ORDEN = tuple(BRAZOS)
HUMO_BRAZOS = ('CIEGO', 'GF', 'GFX', 'BRUJULA', 'INVERTIDO', 'UNA')   # <= 6 corridas
SEMILLA_HUMO = 14641

# ---------- umbrales preregistrados (una linea por puerta) ----------
U = dict(D1_ABS=0.60, D2_J=0.50, D3_BRUJ=0.25, D4_MAPA=0.25, D5_HUYE=0.20, R4_COMIDA=0.90, R5_MUERTES=1.25,
         INV_MAX=0.20, PLAC=0.15, V1_MIN=1.00, PORT_ABS=0.60, PORT_J=0.50)
PRINCIPALES = ('D-1a', 'D-1b', 'D-2', 'D-3', 'D-4', 'D-5', 'R-4', 'R-5', 'C1', 'PLACEBO', 'V1', 'PORT-a', 'PORT-b')
NUCLEO = ('D-1a', 'D-1b', 'D-2', 'D-3')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def tronco_kw():
    """Los kwargs del tronco que DIFIEREN del defecto de mundo_subida_b (leidos de organismo_v142.run con inspect).
    Aborta si un defecto compartido que no es del delta difiere, o si no coinciden con lo declarado."""
    import organismo_v142 as TR, mundo_subida_b as M
    if h16(TR.__file__) != SHA_TRONCO:
        raise SystemExit(f"organismo_v142.py sha {h16(TR.__file__)} != {SHA_TRONCO}")
    dt = {k: v.default for k, v in inspect.signature(TR.run).parameters.items() if v.default is not inspect.Parameter.empty}
    dm = {k: v.default for k, v in inspect.signature(M.run).parameters.items() if v.default is not inspect.Parameter.empty}
    falta = sorted(set(dt) - set(dm))
    if falta:
        raise SystemExit(f"perillas del tronco ausentes en mundo_subida_b: {falta}")
    kw = {k: dt[k] for k in dt if dt[k] != dm[k]}
    for k, v in TRONCO_DECLARADO.items():
        if dt[k] != v:
            raise SystemExit(f"tronco {k}={dt[k]} != declarado {v}")
    if set(kw) - set(TRONCO_DECLARADO):
        raise SystemExit(f"el tronco difiere del mundo en perillas no declaradas: {sorted(set(kw) - set(TRONCO_DECLARADO))}")
    return kw


def kw_de(brazo, T, tkw=None):
    mu, org, br, pex = BRAZOS[brazo]
    w = dict(MUNDOS[mu])
    pr = dict(modo='muralla', n_tel=N_TEL, max_pasos=MAX_PASOS, E_test=E_TEST, **{k: v for k, v in w.items() if k not in ('ancho', 'alto')}, **pex)
    kw = dict(T=T, ancho=w['ancho'], alto=w['alto'], r_vis=R_VIS, sitios=('B',), regen=REGEN, prueba=pr, **br)
    if org == 'v142':
        kw.update(tronco_kw() if tkw is None else tkw)
    return kw


def plano(d, pre=''):
    o = {}
    for k, v in d.items():
        if isinstance(v, dict): o.update(plano(v, pre + k + '.'))
        else: o[pre + k] = v
    return o


def compara_entradas(log, tkw):
    """Regla 14: las entradas contra subida_n6 (corre_subida.kw_de) CAMPO A CAMPO; solo difieren las declaradas."""
    sys.path.insert(2, os.path.join(RAIZ, 'experimentos', 'subida_n6'))
    import corre_subida as V
    if h16(V.__file__) != '374846482660917d':
        raise SystemExit('corre_subida.py de subida_n6 cambio: abortado')
    base = set(tkw) | {'prueba.metas2', 'prueba.min_salidas', 'prueba.margen', 'prueba.p_max'}
    pares = (('CIEGO', 'CIEGO', base), ('GF', 'GF', base), ('GF', 'GFX', base | {'explora'}),
             ('GF', 'UNA', set(tkw) | {'explora'}), ('GF', 'GFX_13', {'prueba.metas2', 'prueba.min_salidas', 'prueba.margen', 'prueba.p_max', 'explora'}))
    for bv, bn, permitidas in pares:
        pa, pn = plano(V.kw_de(bv, 100000)), plano(kw_de(bn, 100000, tkw))
        dif = sorted(k for k in set(pa) | set(pn) if pa.get(k, '<falta>') != pn.get(k, '<falta>'))
        malas = [k for k in dif if k not in permitidas]
        log(f"  regla 14 {bn:7s} vs subida_n6 {bv:5s}: {len(pa)} campos; difieren {dif} "
            + ('(todas declaradas)' if not malas else f"NO DECLARADAS {malas}"))
        if malas:
            raise SystemExit('regla 14: entrada distinta no declarada; abortado')


def una(args):
    brazo, seed, T, tkw = args
    import mundo_subida_b as M
    t0 = time.time()
    r = M.run(seed, **kw_de(brazo, T, tkw))
    t = r['tel'] or {}
    return brazo, seed, dict(
        limpio=t.get('limpio', {}), elige=t.get('elige', {}), a_la_otra=t.get('a_la_otra', {}), come=t.get('come', {}),
        pisa=t.get('pisa', {}), huye=t.get('huye', {}), pasos_cens=t.get('pasos_cens', {}), n=t.get('n', {}),
        n_salidas=t.get('n_salidas'), sin_mover=t.get('sin_mover'), ciego_al_llegar=t.get('ciego_al_llegar'),
        v_A=t.get('v_A'), v_B=t.get('v_B'), geo=t.get('geo'), n_ven=t.get('n_ven'), n_com=t.get('n_com', 1),
        M_comida=t.get('M_comida'), M_veneno=t.get('M_veneno'), orientacion=t.get('orientacion'),
        comida=int(sum(r['mord']['A'])), veneno=int(sum(r['mord']['B'])), muertes=int(r['deaths']),
        M_llenas=int(r['M_llenas']), W=r['W'], celdas=int(r['celdas']), splits=int(r['splits']),
        seg=round(time.time() - t0, 1), casos=t.get('casos', []))


def med(vs):
    vs = [v for v in vs if v is not None]
    return round(statistics.median(vs), 3) if vs else None


def lee_json(ruta, sello=None):
    """ERR-87: por ruta + SELLO EXACTO."""
    b = open(ruta, 'rb').read()
    s = hashlib.sha256(b).hexdigest()[:16]
    if sello is not None and s != sello:
        raise SystemExit(f"SELLO {s} != {sello} en {ruta}")
    return s, json.loads(b.decode('utf-8'))


def valido(d):
    return d['M_comida'] == d.get('n_com', 1) and d['M_veneno'] == d['n_ven']


def media2(d):   # por semilla: limpio medio de las dos clases (balanceado por construccion)
    a, b = d['limpio'].get('cruza'), d['limpio'].get('desvia')
    return None if (a is None or b is None) else (a + b) / 2


def veredicto(POR, seeds, log, et=''):
    def g(b, campo, cs):
        return [POR[b][s][campo].get(cs) for s in seeds] if b in POR else []

    def gv(b, campo):
        return [POR[b][s][campo] for s in seeds] if b in POR else []

    def gm(b):
        return med([media2(POR[b][s]) for s in seeds]) if b in POR else None
    L = []

    def linea(nom, val, umbral, pasa, extra=''):
        L.append(dict(puerta=nom, valor=val, umbral=umbral, pasa=bool(pasa)))
        log(f"  {et}[{'PASA' if pasa else 'CAE '}] {nom:60s} {val}  (umbral {umbral}) {extra}")

    cz = med(g('GFX', 'limpio', 'cruza')); dv = med(g('GFX', 'limpio', 'desvia'))
    otros = '  '.join(f"{b} {med(g(b, 'limpio', 'cruza'))}/{med(g(b, 'limpio', 'desvia'))}" for b in ('CIEGO', 'GF', 'GFV', 'GFVX', 'BRUJULA', 'BARAJADO', 'GFX_13') if b in POR)
    linea('D-1a cruza (elige la del otro lado y rodea): limpio GFX >=', cz, U['D1_ABS'], cz is not None and cz >= U['D1_ABS'], otros)
    linea('D-1b desvia (elige la del mismo lado): limpio GFX >=', dv, U['D1_ABS'], dv is not None and dv >= U['D1_ABS'],
          f"a_la_otra(desvia) BRUJULA {med(g('BRUJULA', 'a_la_otra', 'desvia'))} [la trampa funciona si es alto]")
    J = None if (cz is None or dv is None) else round(cz + dv - 1, 3)
    linea('D-2 balanceada: J = limpio(cruza)+limpio(desvia)-1 >=', J, U['D2_J'], J is not None and J >= U['D2_J'])
    mg, mb = gm('GFX'), gm('BRUJULA')
    linea('D-3 es el VENENO recordado: media GFX - BRUJULA >=', None if (mg is None or mb is None) else round(mg - mb, 3),
          U['D3_BRUJ'], mg is not None and mb is not None and (mg - mb) >= U['D3_BRUJ'],
          f"pisa BRUJULA {med(g('BRUJULA', 'pisa', 'cruza'))}/{med(g('BRUJULA', 'pisa', 'desvia'))}")
    mc, mz = gm('CIEGO'), gm('BARAJADO')
    mx = max([v for v in (mc, mz) if v is not None] or [0])
    linea('D-4 es el mapa: media GFX - max(CIEGO, BARAJADO) >=', None if mg is None else round(mg - mx, 3), U['D4_MAPA'],
          mg is not None and (mg - mx) >= U['D4_MAPA'], f"CIEGO {mc} BARAJADO {mz}")
    hu = med(g('GFX', 'huye', 'cruza'))
    linea('D-5 no es huida: huye(cruza) GFX <=', hu, U['D5_HUYE'], hu is not None and hu <= U['D5_HUYE'])
    kc = med(gv('GFX', 'comida')); kz = med(gv('CIEGO', 'comida'))
    rz = None if (kc is None or not kz) else round(kc / kz, 3)
    linea('R-4 no regresion: comida GFX/CIEGO >=', rz, U['R4_COMIDA'], rz is not None and rz >= U['R4_COMIDA'],
          f"GFX {kc} CIEGO {kz} GF {med(gv('GF', 'comida'))}")
    dc = med(gv('GFX', 'muertes')); dz = med(gv('CIEGO', 'muertes'))
    rm = None if (dc is None or dz is None) else round(dc / max(dz, 1), 3)   # divisor max(CIEGO, 1): declarado
    linea('R-5 muertes GFX/max(CIEGO,1) <=', rm, U['R5_MUERTES'], rm is not None and rm <= U['R5_MUERTES'], f"GFX {dc} CIEGO {dz}")
    iv = gm('INVERTIDO')
    linea('C1 INVERTIDO decisivo: media limpio <=', iv, U['INV_MAX'], iv is not None and iv <= U['INV_MAX'])
    pp = gm('PLACEBO')
    linea('PLACEBO validez: |GFX - PLACEBO| (media) <= (si no, NO se lee)', None if (pp is None or mg is None) else round(abs(pp - mg), 3),
          U['PLAC'], pp is not None and mg is not None and abs(pp - mg) <= U['PLAC'])
    v1 = sum(1 for s in seeds if 'GFX' in POR and valido(POR['GFX'][s]))
    linea(f'V1 memoria COMPLETA: las 2 comidas y las 2 murallas en M de GFX ({v1}/{len(seeds)})', round(v1 / len(seeds), 3),
          U['V1_MIN'], v1 == len(seeds), '  '.join(f"{b} {sum(1 for s in seeds if valido(POR[b][s]))}/{len(seeds)}"
                                                    for b in ('GF', 'GFV', 'GFVX', 'GFX_13', 'UNA') if b in POR))
    ur = med(g('UNA', 'limpio', 'rodeo')); ua = med(g('UNA', 'limpio', 'atajo'))
    linea('PORT-a v14.2 en el mundo de subida_n6: limpio(rodeo) UNA >=', ur, U['PORT_ABS'], ur is not None and ur >= U['PORT_ABS'])
    uj = None if (ur is None or ua is None) else round(ur + ua - 1, 3)
    linea('PORT-b v14.2 en el mundo de subida_n6: J UNA >=', uj, U['PORT_J'], uj is not None and uj >= U['PORT_J'])
    if 'GFX' in POR and 'BRUJULA' in POR and 'GF' in POR:
        pj = sum(1 for s in seeds if (media2(POR['GFX'][s]) or 0) > (media2(POR['BRUJULA'][s]) or 0))
        pg = sum(1 for s in seeds if (media2(POR['GFX'][s]) or 0) > (media2(POR['GF'][s]) or 0))
        log(f"  {et}pareado (reportado): GFX > BRUJULA en {pj}/{len(seeds)}; GFX > GF en {pg}/{len(seeds)}")
    return L


def resumen(puertas):
    pri = [p for p in puertas if p['puerta'].split(' ')[0] in PRINCIPALES]
    nuc = all(p['pasa'] for p in pri if p['puerta'].split(' ')[0] in NUCLEO)
    plac = all(p['pasa'] for p in pri if p['puerta'].split(' ')[0] == 'PLACEBO')
    n = sum(p['pasa'] for p in pri)
    if not plac:
        v = 'NO SE LEE (PLACEBO cae)'
    elif n == len(pri):
        v = 'TODAS LAS PRINCIPALES PASAN'
    elif nuc:
        v = 'NUCLEO PASA, cae alguna principal'
    else:
        v = 'NUCLEO CAE'
    return dict(n=n, tot=len(pri), nucleo=nuc, placebo=plac, texto=f"{n}/{len(pri)} principales -> {v}",
                caen=[p['puerta'].split(' ')[0] for p in pri if not p['pasa']])


def letra(rs, rr=None):
    """Veredicto POR LA LETRA (PREREGISTRO §8). Con una sola serie no hay FUNCIONA: hace falta la replica."""
    if not rs['placebo'] or (rr is not None and not rr['placebo']):
        return 'NO SE LEE (PLACEBO)'
    if not rs['nucleo']:
        return 'NO (el nucleo cae en la serie)'
    if rr is None:
        return ('TODAS PASAN EN LA SERIE -> falta la replica para FUNCIONA' if rs['n'] == rs['tot']
                else f"NUCLEO PASA EN LA SERIE, caen {rs['caen']} -> a lo sumo HAY ALGO MODESTO; falta la replica")
    if rs['n'] == rs['tot'] and rr['n'] == rr['tot']:
        return 'FUNCIONA (todas las principales en serie y replica)'
    if rr['nucleo']:
        return f"HAY ALGO MODESTO (nucleo en las dos; caen serie {rs['caen']} replica {rr['caen']})"
    return 'NO (el nucleo no se replica)'


def main():
    global ORDEN
    ap = argparse.ArgumentParser(allow_abbrev=False)   # ERR-115: nada de abreviaturas
    ap.add_argument('--desde', type=int, default=None)
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--T', type=int, default=T_DEF)
    ap.add_argument('--pool', type=int, default=0)
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--lee', default=None)
    ap.add_argument('--sello', default=None)
    ap.add_argument('--lee_replica', default=None)
    ap.add_argument('--sello_replica', default=None)
    a, resto = ap.parse_known_args()
    if resto:   # ERR-115: una bandera desconocida ABORTA (antes de importar nada ni de lanzar nada)
        raise SystemExit(f"BANDERAS DESCONOCIDAS {resto}: abortado (ERR-115). Validas: --humo | --desde N --n 20 --pool 6 | --lee/--sello")

    if a.lee:
        s, d = lee_json(a.lee, a.sello)
        print(f"serie   sello {s}  semillas {d['semillas'][0]}-{d['semillas'][-1]}")
        for ln in d['puertas']:
            print(f"  [{'PASA' if ln['pasa'] else 'CAE '}] {ln['puerta']:60s} {ln['valor']} (umbral {ln['umbral']})")
        rr = None
        if a.lee_replica:
            s2, d2 = lee_json(a.lee_replica, a.sello_replica)
            print(f"replica sello {s2}  semillas {d2['semillas'][0]}-{d2['semillas'][-1]}")
            for ln in d2['puertas']:
                print(f"  [{'PASA' if ln['pasa'] else 'CAE '}] {ln['puerta']:60s} {ln['valor']} (umbral {ln['umbral']})")
            rr = d2['resumen']
        print(f"VEREDICTO POR LA LETRA: {letra(d['resumen'], rr)}")
        return
    if a.humo == (a.desde is not None):
        raise SystemExit('elige EXACTAMENTE uno: --humo o --desde N (abortado)')

    import mundo_subida_b
    sm = h16(mundo_subida_b.__file__)
    if sm != SHA_MUNDO:
        raise SystemExit(f"mundo_subida_b.py sha {sm} != {SHA_MUNDO} (reconstruir o re-preregistrar)")
    if a.humo:
        a.desde, a.n, a.T, a.pool = SEMILLA_HUMO, 1, T_DEF, 0
        ORDEN = HUMO_BRAZOS
    seeds = list(range(a.desde, a.desde + a.n))
    if not a.humo and (seeds[0] < 14601 or seeds[-1] > 14640):
        raise SystemExit(f"semillas {seeds[0]}-{seeds[-1]} fuera de las preregistradas (14601-14620 serie, 14621-14640 replica)")
    tkw = tronco_kw()
    tag = ('subida_b_humo' if a.humo else f"subida_b_s{seeds[0]}-{seeds[-1]}") + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    dest = os.path.join(AQUI, 'datos', 'humo', tag) if a.humo else os.path.join(AQUI, 'datos', tag)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    flog = open(dest + '.log', 'w', encoding='utf-8')

    def log(m):
        s = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {m}"
        print(s); flog.write(s + '\n'); flog.flush()

    log(f"SUBIDA N6B — mundos {MUNDOS} r_vis={R_VIS} T={a.T} n_tel={N_TEL} semillas {seeds[0]}-{seeds[-1]} "
        f"brazos {len(ORDEN)} pool={a.pool} pid={os.getpid()} mundo_subida_b {sm}")
    log(f"  tronco v14.2 (inspect, difiere del defecto del mundo): {tkw}")
    compara_entradas(log, tkw)
    tareas = [(b, s, a.T, tkw) for b in ORDEN for s in seeds]
    t0 = time.time(); res = []
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as P:
            for i, r in enumerate(P.imap_unordered(una, tareas), 1):
                res.append(r); log(f"  {i}/{len(tareas)}  {r[0]} s{r[1]}  {r[2]['seg']}s")
    else:
        for i, tk in enumerate(tareas, 1):
            r = una(tk); res.append(r); d = r[2]
            log(f"  {i}/{len(tareas)}  {r[0]:9s} s{r[1]}  limpio {d['limpio']}  elige {d['elige']}  otra {d['a_la_otra']}  "
                f"pisa {d['pisa']}  comida {d['comida']} muertes {d['muertes']}  vA {d['v_A']} vB {d['v_B']}  "
                f"M {d['M_comida']}/{d['n_com']} {d['M_veneno']}/{d['n_ven']}  salidas {d['n_salidas']}  {d['seg']}s")
    POR = {b: {} for b in ORDEN}
    for b, s, d in res:
        POR[b][s] = d
    log(f"--- {len(tareas)} corridas en {round(time.time() - t0, 1)} s ---")
    log("PUERTAS (una linea por puerta, umbral al lado):")
    puertas = veredicto(POR, seeds, log)
    rs = resumen(puertas)
    log('RESUMEN ' + rs['texto'] + ("  (HUMO: una semilla y 6 brazos; NO es la serie, no se interpreta)" if a.humo else ""))
    sub = None
    if 'GFX' in POR:   # regla 10 automatica: si V1 cae pero >= 60 % la cumple, subconjunto valido con los umbrales ORIGINALES
        ok = [s for s in seeds if valido(POR['GFX'][s])]
        if len(ok) < len(seeds) and len(ok) >= 0.6 * len(seeds):
            log(f"REGLA 10: V1 {len(ok)}/{len(seeds)} -> subconjunto valido {ok} (se reporta JUNTO al completo; NO cambia la letra)")
            sub = dict(semillas=ok, puertas=veredicto(POR, ok, log, et='[sub] '))
            sub['resumen'] = resumen(sub['puertas']); log('RESUMEN SUBCONJUNTO ' + sub['resumen']['texto'])
    salida = dict(tag=tag, humo=bool(a.humo), semillas=seeds, T=a.T, mundo_subida_b=sm, tronco_kw=tkw, mundos=MUNDOS,
                  comun=dict(r_vis=R_VIS, regen=REGEN, n_tel=N_TEL, max_pasos=MAX_PASOS, E_test=E_TEST),
                  umbrales=U, brazos={b: kw_de(b, a.T, tkw) for b in ORDEN}, puertas=puertas, resumen=rs,
                  subconjunto=sub, por={b: {str(s): POR[b][s] for s in seeds} for b in ORDEN})
    with open(dest + '.json', 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, default=str)
    log(f"JSON {os.path.relpath(dest + '.json', RAIZ)}  sha {h16(dest + '.json')}")
    log(f"VEREDICTO POR LA LETRA (esta corrida sola): {letra(rs) if not a.humo else 'HUMO: no hay veredicto (una semilla, 6 de 11 brazos)'}")
    flog.close()


if __name__ == '__main__':
    main()
