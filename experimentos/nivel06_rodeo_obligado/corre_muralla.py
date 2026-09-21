"""Bloque nivel 6 — RODEO OBLIGADO. Corredor del preregistro PREREGISTRO_rodeo_obligado.md.

Mundo: rejilla toroidal 11 x 9 (99 celdas), r_vis=1. UNA muralla de VENENO que ocupa la FILA COMPLETA menos
UN hueco, y UNA comida al otro lado. Geometria sorteada POR SEMILLA con rng independiente (columna del hueco,
columna y fila de la comida) + origen azaroso + espejo por paridad: ningun sitio es fijo entre semillas.
Alejarse no sirve: el toro esta partido en dos por la muralla y el episodio tiene presupuesto de pasos.

Brazos (6): CIEGO (sin mapa) · MAPA (lectura H1, la refutada en nivel6_2d) · CAMINO (misma tabla M leida por
difusion local: el veneno recordado BLOQUEA) · BARAJADO · INVERTIDO · PLACEBO (CAMINO + k sorteos descartados).

Uso:
  python experimentos/nivel06_rodeo_obligado/corre_muralla.py --humo          (1 proceso, 6 corridas, T=20000)
  python experimentos/nivel06_rodeo_obligado/corre_muralla.py --desde 1701 --n 20 --pool 6
  python experimentos/nivel06_rodeo_obligado/corre_muralla.py --lee datos/humo/<archivo>.json --sello <sha16>
"""
import argparse, datetime, hashlib, json, os, statistics, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))          # ERR-28: organismo/ SIEMPRE primero
sys.path.insert(1, AQUI)

ANCHO, ALTO, R_VIS, REGEN = 11, 9, 1, 50   # r_vis=1 y d_ini=5 fijados en el PREREGISTRO §10(a) ANTES de la serie
T_DEF, N_TEL, MAX_PASOS, D_INI, E_TEST = 100000, 40, 60, 5, 0.3

BRAZOS = {                    # nombre -> (kwargs de run, extras de prueba)
    'CIEGO':     (dict(usa_M=False, camino=0), {}),
    'MAPA':      (dict(usa_M=True, camino=0), {}),
    'CAMINO':    (dict(usa_M=True, camino=1), {}),
    'BARAJADO':  (dict(usa_M=True, camino=1), dict(barajar=True)),
    'INVERTIDO': (dict(usa_M=True, camino=1), dict(invertir=True)),
    'PLACEBO':   (dict(usa_M=True, camino=1, placebo=3), {}),
}
ORDEN = ('CIEGO', 'MAPA', 'CAMINO', 'BARAJADO', 'INVERTIDO', 'PLACEBO')

# ---------- umbrales preregistrados (una linea por puerta; ERR-89) ----------
U = dict(R1_ABS=0.60, R1_MARGEN=0.25, R2_HUYE=0.20, R2_J=0.50, R3_RAZON=0.70,
         R4_COMIDA=0.90, R5_MUERTES=1.25, V1_MIN=1.00, INV_MAX=0.20)


def kw_de(brazo, T):
    br, pex = BRAZOS[brazo]
    prueba = dict(modo='muralla', n_tel=N_TEL, max_pasos=MAX_PASOS, E_test=E_TEST, d_ini=D_INI, **pex)
    return dict(T=T, ancho=ANCHO, alto=ALTO, r_vis=R_VIS, sitios=('B',), regen=REGEN, prueba=prueba, **br)


def una(args):
    brazo, seed, T = args
    import mundo_muralla as M
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
    """ERR-87: por prefijo + SELLO EXACTO. Nunca 'el ultimo archivo que empieza por...' sin verificar el sha."""
    b = open(ruta, 'rb').read()
    s = hashlib.sha256(b).hexdigest()[:16]
    if sello is not None and s != sello:
        raise SystemExit(f"SELLO {s} != {sello} en {ruta}")
    return s, json.loads(b.decode('utf-8'))


def veredicto(POR, seeds, log):
    def g(b, campo, cs):   # ERR-42: un brazo ausente (diagnostico con --brazos) nunca debe tumbar el veredicto y perder el JSON
        return [POR[b][s][campo].get(cs) for s in seeds] if b in POR else []

    def gv(b, campo):
        return [POR[b][s][campo] for s in seeds] if b in POR else []
    L = []

    def linea(nom, val, umbral, pasa, extra=''):
        L.append(dict(puerta=nom, valor=val, umbral=umbral, pasa=bool(pasa)))
        log(f"  [{'PASA' if pasa else 'CAE '}] {nom:52s} {val}  (umbral {umbral}) {extra}")

    r1 = med(g('CAMINO', 'limpio', 'rodeo')); r1c = med(g('CIEGO', 'limpio', 'rodeo'))
    r1b = med(g('BARAJADO', 'limpio', 'rodeo')); r1p = med(g('PLACEBO', 'limpio', 'rodeo'))
    r1m = med(g('MAPA', 'limpio', 'rodeo'))
    linea('R-1a rodea (limpio|rodeo) CAMINO >= abs', r1, U['R1_ABS'], r1 is not None and r1 >= U['R1_ABS'],
          f"CIEGO {r1c} MAPA {r1m} BARAJADO {r1b} PLACEBO {r1p}")
    mx = max([v for v in (r1c, r1b) if v is not None] or [0])
    linea('R-1b margen sobre max(CIEGO,BARAJADO)', None if r1 is None else round(r1 - mx, 3), U['R1_MARGEN'],
          r1 is not None and (r1 - mx) >= U['R1_MARGEN'])
    hu = med(g('CAMINO', 'huye', 'rodeo'))
    linea('R-2a no es huida (huye|rodeo) <=', hu, U['R2_HUYE'], hu is not None and hu <= U['R2_HUYE'])
    c1 = med(g('CAMINO', 'limpio', 'atajo'))   # PREREGISTRO §10(b): el control balanceado es limpio(atajo); 'recto' se REPORTA y no es puerta
    J = None if (r1 is None or c1 is None) else round(r1 + c1 - 1, 3)
    linea('R-2b balanceada J = limpio(rodeo)+limpio(atajo)-1 >=', J, U['R2_J'], J is not None and J >= U['R2_J'],
          f"p1 {r1} c1 {c1}  [recto(atajo) reportado: {med(g('CAMINO', 'recto', 'atajo'))}]")
    pc = med(g('CAMINO', 'pasos_cens', 'rodeo')); pz = med(g('CIEGO', 'pasos_cens', 'rodeo'))
    pb = med(g('BARAJADO', 'pasos_cens', 'rodeo'))
    raz = None if (pc is None or not pz) else round(pc / pz, 3)
    linea('R-3 pasos censurados CAMINO/CIEGO <=', raz, U['R3_RAZON'], raz is not None and raz <= U['R3_RAZON'],
          f"CAMINO {pc} CIEGO {pz} BARAJADO {pb}")
    kc = med(gv('CAMINO', 'comida')); kz = med(gv('CIEGO', 'comida'))
    rz = None if (kc is None or not kz) else round(kc / kz, 3)
    linea('R-4 comida CAMINO/CIEGO (mundo muralla) >=', rz, U['R4_COMIDA'], rz is not None and rz >= U['R4_COMIDA'])
    mc = med(gv('CAMINO', 'muertes')); mz = med(gv('CIEGO', 'muertes'))
    rm = None if (mc is None or not mz) else round(mc / mz, 3)
    linea('R-5 muertes CAMINO/CIEGO <=', rm, U['R5_MUERTES'], rm is not None and rm <= U['R5_MUERTES'])
    pp = med(g('PLACEBO', 'limpio', 'rodeo'))
    linea('PLACEBO ~ CAMINO en R-1a (|dif| <= 0.15; si no, la serie NO se lee)',
          None if (pp is None or r1 is None) else round(abs(pp - r1), 3), 0.15,
          pp is not None and r1 is not None and abs(pp - r1) <= 0.15)
    iv = med(g('INVERTIDO', 'limpio', 'rodeo'))
    linea('C1 INVERTIDO decisivo (limpio|rodeo) <=', iv, U['INV_MAX'], iv is not None and iv <= U['INV_MAX'],
          f"pisa {med(g('INVERTIDO', 'pisa', 'rodeo'))}")
    v1 = sum(1 for s in seeds if 'CAMINO' in POR and POR['CAMINO'][s]['M_comida'] == 1 and
             POR['CAMINO'][s]['M_veneno'] == POR['CAMINO'][s]['n_ven'])
    linea(f'V1 validez: comida y muralla ENTERA en M ({v1}/{len(seeds)})', round(v1 / len(seeds), 3),
          U['V1_MIN'], v1 == len(seeds))
    return L


def main():
    global R_VIS, D_INI, ORDEN
    ap = argparse.ArgumentParser()
    ap.add_argument('--desde', type=int, default=1701)
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--T', type=int, default=T_DEF)
    ap.add_argument('--pool', type=int, default=int(os.environ.get('JUACO_POOL', '0')))
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--lee', default=None)
    ap.add_argument('--sello', default=None)
    ap.add_argument('--rvis', type=int, default=R_VIS)      # instrumento: radio de vision (declarado en el preregistro)
    ap.add_argument('--dini', type=int, default=D_INI)      # instrumento: distancia inicial a la muralla
    ap.add_argument('--brazos', default=','.join(ORDEN))    # diagnostico: subconjunto de brazos (la serie corre los 6)
    a = ap.parse_args()
    R_VIS, D_INI = a.rvis, a.dini
    ORDEN = tuple(b for b in a.brazos.split(',') if b in BRAZOS)

    if a.lee:
        s, d = lee_json(a.lee, a.sello)
        print(f"sello {s}  brazos {list(d['por'])}  semillas {d['semillas']}")
        for ln in d['puertas']:
            print(f"  [{'PASA' if ln['pasa'] else 'CAE '}] {ln['puerta']:52s} {ln['valor']} (umbral {ln['umbral']})")
        return

    if a.humo:
        a.n, a.T, a.pool = 1, 20000, 0
    seeds = list(range(a.desde, a.desde + a.n))
    tag = ('muralla_humo' if a.humo else f"muralla_s{seeds[0]}-{seeds[-1]}") + '_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    dest = os.path.join(RAIZ, 'datos', 'humo' if a.humo else '', tag)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    flog = open(dest + '.log', 'w', encoding='utf-8')

    def log(m):
        s = f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {m}"
        print(s); flog.write(s + '\n'); flog.flush()

    log(f"RODEO OBLIGADO (nivel 6) — rejilla {ANCHO}x{ALTO} r_vis={R_VIS} T={a.T} n_tel={N_TEL} "
        f"semillas {seeds[0]}-{seeds[-1]} brazos {len(ORDEN)} pool={a.pool} pid={os.getpid()}")
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
            log(f"  {i}/{len(tareas)}  {r[0]} s{r[1]}  limpio {r[2]['limpio']}  huye {r[2]['huye']}  "
                f"pasos {r[2]['pasos_cens']}  comida {r[2]['comida']} muertes {r[2]['muertes']}  "
                f"M {r[2]['M_comida']}/1 {r[2]['M_veneno']}/{r[2]['n_ven']}  {r[2]['seg']}s")
    POR = {b: {} for b in ORDEN}
    for b, s, d in res:
        POR[b][s] = d
    log(f"--- {len(tareas)} corridas en {round(time.time() - t0, 1)} s ---")
    for b in ORDEN:
        log(f"  {b:10s} limpio(rodeo) {med([POR[b][s]['limpio'].get('rodeo') for s in seeds])}  "
            f"recto(atajo) {med([POR[b][s]['recto'].get('atajo') for s in seeds])}  "
            f"huye(rodeo) {med([POR[b][s]['huye'].get('rodeo') for s in seeds])}  "
            f"pisa(rodeo) {med([POR[b][s]['pisa'].get('rodeo') for s in seeds])}  "
            f"pasos_c {med([POR[b][s]['pasos_cens'].get('rodeo') for s in seeds])}  "
            f"comida {med([POR[b][s]['comida'] for s in seeds])}  muertes {med([POR[b][s]['muertes'] for s in seeds])}")
    log("PUERTAS (una linea por puerta, umbral al lado):")
    puertas = veredicto(POR, seeds, log)
    log(f"VEREDICTO {sum(p['pasa'] for p in puertas)}/{len(puertas)}"
        + ("  (HUMO: no es la serie, no se interpreta)" if a.humo else ""))
    salida = dict(tag=tag, humo=bool(a.humo), semillas=seeds, T=a.T, mundo=dict(ancho=ANCHO, alto=ALTO, r_vis=R_VIS,
                  regen=REGEN, n_tel=N_TEL, max_pasos=MAX_PASOS, d_ini=D_INI, E_test=E_TEST),
                  umbrales=U, brazos={b: kw_de(b, a.T) for b in ORDEN}, puertas=puertas,
                  por={b: {str(s): POR[b][s] for s in seeds} for b in ORDEN})
    with open(dest + '.json', 'w', encoding='utf-8') as f:
        json.dump(salida, f, ensure_ascii=False, default=str)
    log(f"JSON {os.path.relpath(dest + '.json', RAIZ)}  sha {hashlib.sha256(open(dest + '.json', 'rb').read()).hexdigest()[:16]}")
    flog.close()


if __name__ == '__main__':
    main()
