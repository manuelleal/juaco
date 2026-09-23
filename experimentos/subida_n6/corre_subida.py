"""Nivel 6, bloque SUBIDA_N6 — rodeo en un mundo que SI obliga. Corredor de PREREGISTRO_n6.md.

Mundo PRINCIPAL: rejilla toroidal 11 x 11, r_vis=1. Muralla 1 = fila completa de veneno menos UN hueco (fila 0);
muralla 2 = fila completa de veneno SIN hueco (fila -5, prueba['cierre']=5): el toro queda PARTIDO en dos bandas y
el hueco es el UNICO cruce (el mundo del 21-sep, con una sola fila, era un cilindro: PREREGISTRO §1). Una comida en
la banda de arriba. Geometria sorteada POR SEMILLA (rng independiente) + origen azaroso + espejo por paridad.
Mundo ESCALA (secundario): 15 x 13, cierre=6, d_ini=5.

Brazos (11): CIEGO · CAMINO (lectura del 21-sep) · GRAD (+signo del gradiente) · FILTRO (+veneno recordado no es
objetivo) · GF (candidato: GRAD+FILTRO) · BRUJULA (GF con el veneno recordado que NO bloquea: control que puede ganar)
· BARAJADO · INVERTIDO · PLACEBO (GF + 3 sorteos descartados) · CIEGO_E y GF_E (mundo ESCALA).

Uso:
  python experimentos/subida_n6/corre_subida.py --humo                (1 proceso, 6 corridas, T=20000, semilla 6641)
  python experimentos/subida_n6/corre_subida.py --desde 6601 --n 20 --pool 6      (serie; SOLO el coordinador)
  python experimentos/subida_n6/corre_subida.py --desde 6621 --n 20 --pool 6      (replica; SOLO el coordinador)
  python experimentos/subida_n6/corre_subida.py --lee <ruta.json> --sello <sha16>
"""
import argparse, datetime, hashlib, json, os, statistics, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))          # ERR-28: organismo/ SIEMPRE primero
sys.path.insert(1, AQUI)

SHA_MUNDO = '484e34db8f2150da'          # mundo_subida.py (construye_subida.py sobre mundo_muralla 6e515713c86d8bf4)
MUNDOS = {   # PREREGISTRO §3: fijados ANTES de la serie
    'P': dict(ancho=11, alto=11, cierre=5, d_ini=4),
    'E': dict(ancho=15, alto=13, cierre=6, d_ini=5),
}
R_VIS, REGEN, T_DEF, N_TEL, MAX_PASOS, E_TEST = 1, 50, 100000, 40, 60, 0.3

BRAZOS = {   # nombre -> (mundo, kwargs de run, extras de prueba)
    'CIEGO':     ('P', dict(usa_M=False, camino=0), {}),
    'CAMINO':    ('P', dict(usa_M=True, camino=1), {}),
    'GRAD':      ('P', dict(usa_M=True, camino=1, grad=1), {}),
    'FILTRO':    ('P', dict(usa_M=True, camino=1, filtro=1), {}),
    'GF':        ('P', dict(usa_M=True, camino=1, grad=1, filtro=1), {}),
    'BRUJULA':   ('P', dict(usa_M=True, camino=1, grad=1, filtro=1, brujula=1), {}),
    'BARAJADO':  ('P', dict(usa_M=True, camino=1, grad=1, filtro=1), dict(barajar=True)),
    'INVERTIDO': ('P', dict(usa_M=True, camino=1, grad=1, filtro=1), dict(invertir=True)),
    'PLACEBO':   ('P', dict(usa_M=True, camino=1, grad=1, filtro=1, placebo=3), {}),
    'CIEGO_E':   ('E', dict(usa_M=False, camino=0), {}),
    'GF_E':      ('E', dict(usa_M=True, camino=1, grad=1, filtro=1), {}),
}
ORDEN = tuple(BRAZOS)
HUMO_BRAZOS = ('CIEGO', 'CAMINO', 'GF', 'BRUJULA', 'BARAJADO', 'INVERTIDO')   # regla 3: <= 6 corridas

# ---------- umbrales preregistrados (una linea por puerta; ERR-89; los de R-1a..V1 son los del 21-sep, sin tocar) ----------
U = dict(R1_ABS=0.60, R1_MARGEN=0.25, R1_BRUJ=0.25, R2_HUYE=0.20, R2_J=0.50, R3_RAZON=0.70,
         R4_COMIDA=0.90, R5_MUERTES=1.25, V1_MIN=1.00, INV_MAX=0.20, PLAC=0.15, E_ABS=0.60, E_MARGEN=0.25)


def kw_de(brazo, T):
    mu, br, pex = BRAZOS[brazo]
    w = MUNDOS[mu]
    prueba = dict(modo='muralla', n_tel=N_TEL, max_pasos=MAX_PASOS, E_test=E_TEST, d_ini=w['d_ini'], cierre=w['cierre'], **pex)
    return dict(T=T, ancho=w['ancho'], alto=w['alto'], r_vis=R_VIS, sitios=('B',), regen=REGEN, prueba=prueba, **br)


def compara_entradas(log):
    """Regla 14 (ERR-38/41): las entradas de CIEGO y CAMINO son las del bloque del 21-sep CAMPO A CAMPO, salvo lo que el
    preregistro cambia a proposito (mundo: ancho/alto/d_ini/cierre). Si aparece otra diferencia, se aborta."""
    sys.path.insert(2, os.path.join(RAIZ, 'experimentos', 'nivel06_rodeo_obligado'))
    import corre_muralla as V
    permitidas = {'alto', 'prueba.d_ini', 'prueba.cierre'}
    for b in ('CIEGO', 'CAMINO'):
        a = V.kw_de(b, 100000); n = kw_de(b, 100000)

        def plano(d, pre=''):
            o = {}
            for k, v in d.items():
                if isinstance(v, dict): o.update(plano(v, pre + k + '.'))
                else: o[pre + k] = v
            return o
        pa, pn = plano(a), plano(n)
        dif = sorted(k for k in set(pa) | set(pn) if pa.get(k, '<falta>') != pn.get(k, '<falta>'))
        malas = [k for k in dif if k not in permitidas]
        log(f"  regla 14 {b:7s}: {len(pa)} campos del 21-sep; difieren {dif} "
            + ('(todas declaradas en PREREGISTRO §3)' if not malas else f"NO DECLARADAS {malas}"))
        if malas:
            raise SystemExit('regla 14: entrada distinta no declarada; abortado')


def una(args):
    brazo, seed, T = args
    import mundo_subida as M
    t0 = time.time()
    r = M.run(seed, **kw_de(brazo, T))
    t = r['tel'] or {}
    return brazo, seed, dict(
        limpio=t.get('limpio', {}), come=t.get('come', {}), pisa=t.get('pisa', {}), huye=t.get('huye', {}),
        recto=t.get('recto', {}), pasos_cens=t.get('pasos_cens', {}), n=t.get('n', {}),
        sin_mover=t.get('sin_mover'), ciego_al_llegar=t.get('ciego_al_llegar'),
        v_A=t.get('v_A'), v_B=t.get('v_B'), geo=t.get('geo'), n_ven=t.get('n_ven'),
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


def valido(POR, s):
    d = POR['GF'][s]
    return d['M_comida'] == 1 and d['M_veneno'] == d['n_ven']


def veredicto(POR, seeds, log, et=''):
    def g(b, campo, cs):   # ERR-42: un brazo ausente nunca tumba el veredicto ni pierde el JSON
        return [POR[b][s][campo].get(cs) for s in seeds] if b in POR else []

    def gv(b, campo):
        return [POR[b][s][campo] for s in seeds] if b in POR else []
    L = []

    def linea(nom, val, umbral, pasa, extra=''):
        L.append(dict(puerta=nom, valor=val, umbral=umbral, pasa=bool(pasa)))
        log(f"  {et}[{'PASA' if pasa else 'CAE '}] {nom:58s} {val}  (umbral {umbral}) {extra}")

    r1 = med(g('GF', 'limpio', 'rodeo')); r1c = med(g('CIEGO', 'limpio', 'rodeo'))
    r1b = med(g('BARAJADO', 'limpio', 'rodeo')); r1j = med(g('BRUJULA', 'limpio', 'rodeo'))
    linea('R-1a rodea: limpio(rodeo) GF >=', r1, U['R1_ABS'], r1 is not None and r1 >= U['R1_ABS'],
          f"CIEGO {r1c} CAMINO {med(g('CAMINO', 'limpio', 'rodeo'))} GRAD {med(g('GRAD', 'limpio', 'rodeo'))} "
          f"FILTRO {med(g('FILTRO', 'limpio', 'rodeo'))} BARAJADO {r1b} BRUJULA {r1j}")
    mx = max([v for v in (r1c, r1b) if v is not None] or [0])
    linea('R-1b es el mapa: GF - max(CIEGO,BARAJADO) >=', None if r1 is None else round(r1 - mx, 3), U['R1_MARGEN'],
          r1 is not None and (r1 - mx) >= U['R1_MARGEN'])
    linea('R-1c es el VENENO recordado: GF - BRUJULA >=', None if (r1 is None or r1j is None) else round(r1 - r1j, 3),
          U['R1_BRUJ'], r1 is not None and r1j is not None and (r1 - r1j) >= U['R1_BRUJ'],
          f"pisa(rodeo) BRUJULA {med(g('BRUJULA', 'pisa', 'rodeo'))}")
    hu = med(g('GF', 'huye', 'rodeo'))
    linea('R-2a no es huida: huye(rodeo) GF <=', hu, U['R2_HUYE'], hu is not None and hu <= U['R2_HUYE'])
    c1 = med(g('GF', 'limpio', 'atajo'))
    J = None if (r1 is None or c1 is None) else round(r1 + c1 - 1, 3)
    linea('R-2b balanceada: J = limpio(rodeo)+limpio(atajo)-1 >=', J, U['R2_J'], J is not None and J >= U['R2_J'],
          f"p1 {r1} c1 {c1}  [recto(atajo) reportado, no es puerta: {med(g('GF', 'recto', 'atajo'))}]")
    pc = med(g('GF', 'pasos_cens', 'rodeo')); pz = med(g('CIEGO', 'pasos_cens', 'rodeo'))
    raz = None if (pc is None or not pz) else round(pc / pz, 3)
    linea('R-3 cuesta menos: pasos_cens(rodeo) GF/CIEGO <=', raz, U['R3_RAZON'], raz is not None and raz <= U['R3_RAZON'],
          f"GF {pc} CIEGO {pz}")
    kc = med(gv('GF', 'comida')); kz = med(gv('CIEGO', 'comida'))
    rz = None if (kc is None or not kz) else round(kc / kz, 3)
    linea('R-4 no regresion: comida GF/CIEGO >=', rz, U['R4_COMIDA'], rz is not None and rz >= U['R4_COMIDA'],
          f"GF {kc} CIEGO {kz} CAMINO {med(gv('CAMINO', 'comida'))}")
    mc = med(gv('GF', 'muertes')); mz = med(gv('CIEGO', 'muertes'))
    rm = None if (mc is None or not mz) else round(mc / mz, 3)
    linea('R-5 muertes GF/CIEGO <=', rm, U['R5_MUERTES'], rm is not None and rm <= U['R5_MUERTES'],
          f"GF {mc} CIEGO {mz} CAMINO {med(gv('CAMINO', 'muertes'))}")
    iv = med(g('INVERTIDO', 'limpio', 'rodeo'))
    linea('C1 INVERTIDO decisivo: limpio(rodeo) <=', iv, U['INV_MAX'], iv is not None and iv <= U['INV_MAX'],
          f"pisa {med(g('INVERTIDO', 'pisa', 'rodeo'))}")
    pp = med(g('PLACEBO', 'limpio', 'rodeo'))
    linea('PLACEBO validez: |GF - PLACEBO| <= (si no, NO se lee)', None if (pp is None or r1 is None) else round(abs(pp - r1), 3),
          U['PLAC'], pp is not None and r1 is not None and abs(pp - r1) <= U['PLAC'])
    v1 = sum(1 for s in seeds if 'GF' in POR and valido(POR, s))
    linea(f'V1 validez: comida y las DOS murallas enteras en M ({v1}/{len(seeds)})', round(v1 / len(seeds), 3),
          U['V1_MIN'], v1 == len(seeds))
    re = med(g('GF_E', 'limpio', 'rodeo')); rce = med(g('CIEGO_E', 'limpio', 'rodeo'))
    linea('E-1 (secundaria) escala 15x13: limpio(rodeo) GF_E >=', re, U['E_ABS'], re is not None and re >= U['E_ABS'],
          f"CIEGO_E {rce}")
    linea('E-2 (secundaria) escala: GF_E - CIEGO_E >=', None if (re is None or rce is None) else round(re - rce, 3),
          U['E_MARGEN'], re is not None and rce is not None and (re - rce) >= U['E_MARGEN'])
    # pareado (reportado): semillas con limpio(rodeo) GF > BRUJULA y GF > CIEGO
    if 'GF' in POR and 'BRUJULA' in POR and 'CIEGO' in POR:
        pj = sum(1 for s in seeds if POR['GF'][s]['limpio'].get('rodeo', 0) > POR['BRUJULA'][s]['limpio'].get('rodeo', 0))
        pz2 = sum(1 for s in seeds if POR['GF'][s]['limpio'].get('rodeo', 0) > POR['CIEGO'][s]['limpio'].get('rodeo', 0))
        log(f"  {et}pareado (reportado): GF > BRUJULA en {pj}/{len(seeds)}; GF > CIEGO en {pz2}/{len(seeds)}")
    return L


PRINCIPALES = ('R-1a', 'R-1b', 'R-1c', 'R-2a', 'R-2b', 'R-3', 'R-4', 'R-5', 'C1', 'PLACEBO', 'V1')


def resumen(puertas):
    pri = [p for p in puertas if p['puerta'].split(' ')[0] in PRINCIPALES]
    sec = [p for p in puertas if p['puerta'].split(' ')[0] in ('E-1', 'E-2')]
    nucleo = all(p['pasa'] for p in pri if p['puerta'].split(' ')[0] in ('R-1a', 'R-1c', 'R-2b'))
    if all(p['pasa'] for p in pri):
        v = 'PASA TODAS LAS PRINCIPALES (FUNCIONA si la replica repite)'
    elif nucleo:
        v = 'NUCLEO (R-1a, R-1c, R-2b) PASA, alguna principal cae: HAY ALGO MODESTO'
    else:
        v = 'NUCLEO CAE: NO'
    return f"{sum(p['pasa'] for p in pri)}/{len(pri)} principales, {sum(p['pasa'] for p in sec)}/{len(sec)} secundarias -> {v}"


def main():
    global ORDEN
    ap = argparse.ArgumentParser()
    ap.add_argument('--desde', type=int, default=6601)
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--T', type=int, default=T_DEF)
    ap.add_argument('--pool', type=int, default=0)
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--lee', default=None)
    ap.add_argument('--sello', default=None)
    ap.add_argument('--brazos', default=None)   # diagnostico; la serie corre los 11
    a = ap.parse_args()

    if a.lee:
        s, d = lee_json(a.lee, a.sello)
        print(f"sello {s}  brazos {list(d['por'])}  semillas {d['semillas'][0]}-{d['semillas'][-1]}")
        for ln in d['puertas']:
            print(f"  [{'PASA' if ln['pasa'] else 'CAE '}] {ln['puerta']:58s} {ln['valor']} (umbral {ln['umbral']})")
        print('  ' + d.get('resumen', ''))
        return

    import mundo_subida
    sm = hashlib.sha256(open(mundo_subida.__file__, 'rb').read()).hexdigest()[:16]
    if sm != SHA_MUNDO:
        raise SystemExit(f"mundo_subida.py sha {sm} != {SHA_MUNDO} (reconstruir o re-preregistrar)")
    if a.humo:
        a.desde, a.n, a.T, a.pool = 6641, 1, 20000, 0
        ORDEN = HUMO_BRAZOS
    if a.brazos:
        ORDEN = tuple(b for b in a.brazos.split(',') if b in BRAZOS)
    seeds = list(range(a.desde, a.desde + a.n))
    tag = ('subida_humo' if a.humo else f"subida_s{seeds[0]}-{seeds[-1]}") + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    dest = os.path.join(AQUI, 'datos', 'humo' if a.humo else '', tag)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    flog = open(dest + '.log', 'w', encoding='utf-8')

    def log(m):
        s = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {m}"
        print(s); flog.write(s + '\n'); flog.flush()

    log(f"SUBIDA N6 — mundos {MUNDOS} r_vis={R_VIS} T={a.T} n_tel={N_TEL} semillas {seeds[0]}-{seeds[-1]} "
        f"brazos {len(ORDEN)} pool={a.pool} pid={os.getpid()} mundo_subida {sm}")
    compara_entradas(log)
    tareas = [(b, s, a.T) for b in ORDEN for s in seeds]
    t0 = time.time(); res = []
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as P:
            for i, r in enumerate(P.imap_unordered(una, tareas), 1):
                res.append(r); log(f"  {i}/{len(tareas)}  {r[0]} s{r[1]}  {r[2]['seg']}s")
    else:
        for i, tk in enumerate(tareas, 1):
            r = una(tk); res.append(r)
            log(f"  {i}/{len(tareas)}  {r[0]:9s} s{r[1]}  limpio {r[2]['limpio']}  pisa {r[2]['pisa']}  huye {r[2]['huye']}  "
                f"pasos {r[2]['pasos_cens']}  comida {r[2]['comida']} muertes {r[2]['muertes']}  vA {r[2]['v_A']} vB {r[2]['v_B']}  "
                f"M {r[2]['M_comida']}/1 {r[2]['M_veneno']}/{r[2]['n_ven']}  {r[2]['seg']}s")
    POR = {b: {} for b in ORDEN}
    for b, s, d in res:
        POR[b][s] = d
    log(f"--- {len(tareas)} corridas en {round(time.time() - t0, 1)} s ---")
    for b in ORDEN:
        log(f"  {b:10s} limpio(rodeo) {med([POR[b][s]['limpio'].get('rodeo') for s in seeds])}  "
            f"limpio(atajo) {med([POR[b][s]['limpio'].get('atajo') for s in seeds])}  "
            f"huye(rodeo) {med([POR[b][s]['huye'].get('rodeo') for s in seeds])}  "
            f"pisa(rodeo) {med([POR[b][s]['pisa'].get('rodeo') for s in seeds])}  "
            f"pasos_c {med([POR[b][s]['pasos_cens'].get('rodeo') for s in seeds])}  "
            f"comida {med([POR[b][s]['comida'] for s in seeds])}  muertes {med([POR[b][s]['muertes'] for s in seeds])}")
    log("PUERTAS (una linea por puerta, umbral al lado):")
    puertas = veredicto(POR, seeds, log)
    res_txt = resumen(puertas)
    log('RESUMEN ' + res_txt + ("  (HUMO: no es la serie, no se interpreta)" if a.humo else ""))
    sub = None
    if 'GF' in POR:   # regla 10 automatica: si V1 cae pero >= 60 % la cumple, subconjunto valido con los umbrales ORIGINALES
        ok = [s for s in seeds if valido(POR, s)]
        if len(ok) < len(seeds) and len(ok) >= 0.6 * len(seeds):
            log(f"REGLA 10: V1 {len(ok)}/{len(seeds)} -> subconjunto valido {ok} (se reporta JUNTO al completo)")
            sub = dict(semillas=ok, puertas=veredicto(POR, ok, log, et='[sub] '))
            sub['resumen'] = resumen(sub['puertas']); log('RESUMEN SUBCONJUNTO ' + sub['resumen'])
    salida = dict(tag=tag, humo=bool(a.humo), semillas=seeds, T=a.T, mundo_subida=sm, mundos=MUNDOS,
                  comun=dict(r_vis=R_VIS, regen=REGEN, n_tel=N_TEL, max_pasos=MAX_PASOS, E_test=E_TEST),
                  umbrales=U, brazos={b: kw_de(b, a.T) for b in ORDEN}, puertas=puertas, resumen=res_txt,
                  subconjunto=sub, por={b: {str(s): POR[b][s] for s in seeds} for b in ORDEN})
    with open(dest + '.json', 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, default=str)
    log(f"JSON {os.path.relpath(dest + '.json', RAIZ)}  sha {hashlib.sha256(open(dest + '.json', 'rb').read()).hexdigest()[:16]}")
    flog.close()


if __name__ == '__main__':
    main()
