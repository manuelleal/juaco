"""corre_eco_v21.py — RUNNER de JUACO-ECO v2.1: ÓRGANOS COMO GENES con la prueba de EXPRESIÓN contra sombras (nube, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/juaco_eco/PREREGISTRO_eco_v21.md (la letra esta AQUI, en veredicto(), y alli).
ECO v2.1 = ECO v2 (mismo mundo, mismos organos, mismo motor y gemelo) con UN cambio de instrumento (nube-8): O1 mide la EXPRESION del
organo en el banco del corte (tomada del checkpoint del corte, que trae las 8 sombras de cada entrada) contra la MEDIA de sus sombras.
Lo que cambia respecto de ECO v1 (mismo vivero, corte en 60 000, T 120 000, mutacion, banco de 200 y 8 sombras):
  - el genoma tiene 20 genes: los 18 de v1 + los ORGANOS 'ensena' (el padre pasa su tabla) y 'filtra0' (el hijo quita lo neutro), rasgos
    con umbral que nacen APAGADOS (motor_eco2 + carros/FAMB_ORG_ECO; arnes Python identidad_eco_org.py 9/9);
  - TRES MUNDOS de capacidad distinta corren a la vez: esc 30, 90 y 270 (L 1 200 / 3 600 / 10 800; quimiostato 0.9 / 2.7 / 8.1 objetos
    por paso; 30 / 90 / 270 fundadores);
  - brazos VIDA (seleccion) y AZAR (deriva: el genoma de todo cuerpo nuevo sale del banco al azar). Sin juez de colonias: la pregunta es
    si la seleccion PRENDE el organo, y eso se lee en el banco del corte contra sus sombras y contra AZAR.
Motor: --serie y --prueba_pool SOLO con el gemelo motor_eco_rapido_org (vale mientras su arnes de N/N); --humo con el motor Python.

Uso (ERR-115: banderas desconocidas o abreviadas abortan):
  python experimentos/juaco_eco/corre_eco_v21.py --humo [--gemelo]
  python experimentos/juaco_eco/corre_eco_v21.py --prueba_pool --pool 2
  python experimentos/juaco_eco/corre_eco_v21.py --serie --ventana serie --pool 3      # semillas 20211-20230
  python experimentos/juaco_eco/corre_eco_v21.py --serie --ventana replica --pool 3    # semillas 20231-20250
  python experimentos/juaco_eco/corre_eco_v21.py --serie --ventana serie --pool 3 --reanuda
  python experimentos/juaco_eco/corre_eco_v21.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, os, pickle, sys, time, types
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
for _d in (AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_eco as CR          # eco_cfg (brazos VIDA/AZAR, SERIE), sel_genes; NO se usa su motor
import motor_eco2 as ME2

MOTOR = [ME2]                    # el motor en uso (Python hasta que usa_gemelo() enchufe el gemelo)
CARRO = 'FAMB_ORG_ECO'
SERIE = CR.SERIE                 # banco 200, 8 sombras, sigma 0.15, p_mut 0.05, cada_gen 2000, ckpt_cada 10000
V2 = dict(T=120000, t_corte=60000)
MUNDOS = {'w30': dict(esc=30, n0=30, tope=3000), 'w90': dict(esc=90, n0=90, tope=3000), 'w270': dict(esc=270, n0=270, tope=9000)}
BRAZOS = ('VIDA', 'AZAR')
VENTANAS = {'serie': 20211, 'replica': 20231}
N = 20
PRUEBA = dict(desde=20292, n=2, T=12000, t_corte=10000)
HUMO = dict(semilla=20291, mundo='w30', T=20000, t_corte=10000)
ORGANOS = ('ensena', 'filtra0')
IORG = {g: ME2.NOMBRES.index(g) for g in ORGANOS}
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


def usa_gemelo():
    import motor_eco_rapido_org as MR
    g = types.ModuleType('motor_eco2_gemelo')
    g.__dict__.update({k: v for k, v in ME2.__dict__.items() if not k.startswith('__')})
    g.run_solapadas = MR.run_solapadas
    MOTOR[0] = g
    return MR


def expresion_sombras(blob):
    """ENMIENDA 1 (nube-8): del checkpoint del corte (el estado completo, con el banco de pares (genoma, 8 sombras)), la fraccion del
    banco que EXPRESA cada organo (gen >= UMBRAL) en el genoma real y en cada una de sus 8 sombras."""
    B = pickle.loads(blob)['ES']['banco']
    out = {}
    for g in ORGANOS:
        j = IORG[g]
        real = float(np.mean([float(x[0][j]) >= ME2.UMBRAL_ORG for x in B]))
        somb = [float(np.mean([float(x[1][k][j]) >= ME2.UMBRAL_ORG for x in B])) for k in range(len(B[0][1]))]
        out[g] = dict(real=round(real, 4), sombras=[round(v, 4) for v in somb])
    return out


def frac_on(genomas, gen):
    if not genomas: return None
    j = IORG[gen]
    return round(float(np.mean([float(g[j]) >= ME2.UMBRAL_ORG for g in genomas])), 4)


def trabajo(args):
    seed, mundo, brazo, T, t_corte, carpeta, reanuda = args
    W = MUNDOS[mundo]
    fin = os.path.join(carpeta, f"{mundo}_{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin): return json.load(open(fin, encoding='utf-8'))
    ck = os.path.join(carpeta, 'ckpt', f"{mundo}_{brazo}_s{seed}.pkl"); os.makedirs(os.path.dirname(ck), exist_ok=True)
    filas = []

    def cb(li, row, g):
        if row[3] >= t_corte: filas.append([li] + row)

    sombras = {}   # v2.1 (nube-8): expresion del organo en el banco del corte, real contra sus 8 sombras

    def guarda(t, blob):
        if t == t_corte and not sombras: sombras.update(expresion_sombras(blob))
        tmp = ck + '.tmp'
        with open(tmp, 'wb') as f: pickle.dump(dict(t=t, blob=blob, filas=filas, sombras=sombras), f, protocol=pickle.HIGHEST_PROTOCOL)
        os.replace(tmp, ck)
    estado = None
    if reanuda and os.path.exists(ck):
        d = pickle.load(open(ck, 'rb')); estado = d['blob']; filas[:] = d['filas']; sombras.update(d.get('sombras') or {})
    t0 = time.time()
    r = MOTOR[0].run_solapadas(seed, [CARRO] * W['n0'], T=T, diag=0, mundo_n=W['esc'], tope_cuerpos=W['tope'], muestra=1000,
                               eco=CR.eco_cfg(brazo, t_corte, ckpt_cada=SERIE['ckpt_cada'], ckpt_fn=guarda, estado=estado, ind_cb=cb))
    E = r['eco']; P = r['pista']
    if list(E['genes']) != list(ME2.NOMBRES): raise SystemExit(f"ECO v2.1: genoma inesperado {E['genes']}")
    fila_corte = next((f for f in E['gen_t'] if f[0] == t_corte), None)
    banco = (E['corte'] or {}).get('banco') or []
    vivos_g = [v[4:] for v in E['vivos_final']]
    coh = [f for f in filas if f[4] <= T - 20000]
    res = dict(seed=seed, mundo=mundo, brazo=brazo, T=T, t_corte=t_corte, seg=round(time.time() - t0, 1), t_ext=E['t_ext'],
               persiste=int(E['t_ext'] is None and len(E['vivos_final']) > 0), vivos_T=len(E['vivos_final']),
               bloqueados=P['bloqueados'], max_vivos=P['max_vivos'], n_nac=E['n_nac'], n_refund=E['n_refund'], n_banco=E['n_banco'],
               r0_post=(round(float(np.mean([f[6] for f in coh])), 4) if coh else None), n_coh_post=len(coh),
               sel_corte=CR.sel_genes(fila_corte), genes=E['genes'], G0=E['G0'],
               banco_on={g: frac_on(banco, g) for g in ORGANOS}, vivos_on={g: frac_on(vivos_g, g) for g in ORGANOS},
               banco_on_sombras=(dict(sombras) or None),
               corte=E['corte'], gen_t=E['gen_t'], vivos_final=E['vivos_final'][:500], tam_total=P['tam_total'],
               motor=('GEMELO motor_eco_rapido_org' if MOTOR[0] is not ME2 else 'PYTHON motor_eco2'))
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck): os.remove(ck)
    return res


# ================================================================================ LA LETRA (PREREGISTRO_eco_v21.md §6)
def veredicto(R, n_esperado=N):
    """Por mundo: O1* = en VIDA la fraccion del banco del corte que EXPRESA 'ensena' supera a la MEDIA de las de sus 8 sombras (estricto) en
    >= 15/20; O2 = el banco de VIDA lo expresa mas que el de AZAR (pareado, estricto) en >= 15/20. FUNCIONA si O1* y O2 en >= 2 de 3 mundos."""
    L = []
    completo = all(sum(1 for x in R if x['mundo'] == m and x['brazo'] == b) == n_esperado for m in MUNDOS for b in BRAZOS)
    bloq = sum(x['bloqueados'] for x in R)
    genes = list(ME2.NOMBRES)
    guardia = []; O1 = {}; O2 = {}; F = {}; ok_mundo = {}
    for m in MUNDOS:
        by = {b: {x['seed']: x for x in R if x['mundo'] == m and x['brazo'] == b} for b in BRAZOS}

        def cuenta(b, g):
            j = genes.index(g); s_ = [x['sel_corte'][j] for x in by[b].values() if x['sel_corte'] is not None]
            return sum(1 for v in s_ if v > 0), sum(1 for v in s_ if v < 0)

        def expr(b, g):
            mas = menos = k = 0
            for x in by[b].values():
                e = (x.get('banco_on_sombras') or {}).get(g)
                if not e: continue
                k += 1; ms = float(np.mean(e['sombras'])); mas += int(e['real'] > ms); menos += int(e['real'] < ms)
            return mas, menos, k
        cA = {g: cuenta('AZAR', g) for g in genes}
        guardia += [(m, g, cA[g]) for g in genes if max(cA[g]) > 8]
        guardia += [(m, g, 'expresion AZAR', expr('AZAR', g)[:2]) for g in ORGANOS if expr('AZAR', g)[0] >= 15]
        eV = {g: expr('VIDA', g) for g in ORGANOS}; eA = {g: expr('AZAR', g) for g in ORGANOS}
        O1[m] = eV['ensena'][0] >= 15
        F[m] = eV['filtra0'][0] >= 15
        w = k = 0
        for s_ in sorted(set(by['VIDA']) & set(by['AZAR'])):
            a, b = by['VIDA'][s_]['banco_on']['ensena'], by['AZAR'][s_]['banco_on']['ensena']
            if a is None or b is None: continue
            k += 1; w += int(a > b)
        O2[m] = w >= 15
        med = lambda b, g, clave: (float(np.median([x[clave][g] for x in by[b].values() if x[clave][g] is not None]))
                                   if any(x[clave][g] is not None for x in by[b].values()) else None)
        pers = {b: sum(x['persiste'] for x in by[b].values()) for b in BRAZOS}
        L.append(f"[{m}] ensena: VIDA expresa sobre la media de sus sombras {eV['ensena'][0]}/{eV['ensena'][2]} · AZAR {eA['ensena'][0]}/{eA['ensena'][2]} · "
                 f"filtra0: VIDA {eV['filtra0'][0]}/{eV['filtra0'][2]} · AZAR {eA['filtra0'][0]}/{eA['filtra0'][2]} · descriptivo media contra sombras "
                 f"VIDA ensena {cuenta('VIDA', 'ensena')} filtra0 {cuenta('VIDA', 'filtra0')}")
        L.append(f"[{m}] banco con ensena (mediana): VIDA {med('VIDA', 'ensena', 'banco_on')} · AZAR {med('AZAR', 'ensena', 'banco_on')}; VIDA > AZAR {w}/{k} · "
                 f"con filtra0: VIDA {med('VIDA', 'filtra0', 'banco_on')} · AZAR {med('AZAR', 'filtra0', 'banco_on')} · vivos en T con ensena: VIDA "
                 f"{med('VIDA', 'ensena', 'vivos_on')} · AZAR {med('AZAR', 'ensena', 'vivos_on')}")
        L.append(f"[{m}] otros genes seleccionados en VIDA (>= 15/20): {[(g, cuenta('VIDA', g)) for g in genes if max(cuenta('VIDA', g)) >= 15 and g not in ORGANOS]} · "
                 f"persisten en T: {pers} · O1* {'SI' if O1[m] else 'NO'} · O2 {'SI' if O2[m] else 'NO'} · F {'SI' if F[m] else 'NO'}")
        ok_mundo[m] = O1[m] and O2[m]
    n_ok = sum(ok_mundo.values()); n_uno = sum(1 for m in MUNDOS if O1[m] or O2[m]); n_f = sum(F.values())
    if not completo: v = 'NO EVALUABLE (serie incompleta)'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq})'
    elif guardia: v = f'NO EVALUABLE (AZAR da falsos positivos contra sombras: {guardia})'
    elif n_ok >= 2: v = f'FUNCIONA: LA SELECCION PRENDE EL ORGANO DE ENSENAR (en esta serie; O1* y O2 en {n_ok} de 3 mundos)'
    elif n_uno >= 2 or n_ok == 1: v = f'HAY ALGO MODESTO (en esta serie; O1* y O2 juntos en {n_ok} mundo(s), alguno de los dos en {n_uno})'
    else: v = 'NO (en esta serie)'
    L.append(f"secundario: filtra0 expresado sobre sus sombras (>= 15/20) en {n_f} de 3 mundos")
    L.append(f"VEREDICTO ECO v2.1 POR LA LETRA (una serie; el del bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(O1=O1, O2=O2, F=F, n_ok=n_ok, n_uno=n_uno, guardia=guardia)


def lee(carpeta, n_esperado=N):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, 'w*_s*.json')))]
    v, L, d = veredicto(R, n_esperado)
    for l in L: print(l, flush=True)
    return v, L, d, R


def SHAS():
    f = lambda p: hashlib.sha256(open(os.path.join(AQUI, p), 'rb').read()).hexdigest()[:16]
    return {p: f(p) for p in ('corre_eco_v21.py', 'corre_eco.py', 'motor_eco2.py', 'motor_eco_rapido_org.py', 'carros/FAMB_ORG_ECO.py',
                              'construye_eco_org.py', 'PREREGISTRO_eco_v21.md') if os.path.exists(os.path.join(AQUI, p))}


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--prueba_pool', action='store_true'); ap.add_argument('--lee', default=None)
    ap.add_argument('--ventana', default=None); ap.add_argument('--pool', type=int)
    ap.add_argument('--reanuda', action='store_true'); ap.add_argument('--gemelo', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('ECO v2.1: banderas mal formadas')
    if resto: raise BanderaMala(f"ECO v2.1: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('ECO v2.1: sin la forma --bandera=valor')
    if len(argv) != len(set(x for x in argv if x.startswith('--'))) + sum(1 for x in argv if not x.startswith('--')):
        raise BanderaMala('ECO v2.1: bandera repetida')
    if int(a.humo) + int(a.serie) + int(a.prueba_pool) + int(a.lee is not None) != 1:
        raise BanderaMala('ECO v2.1: exactamente uno de --humo, --serie, --prueba_pool, --lee')
    if a.humo and (a.ventana is not None or a.pool is not None or a.reanuda): raise BanderaMala('ECO v2.1: --humo solo admite --gemelo')
    if a.lee is not None and (a.ventana is not None or a.pool is not None or a.reanuda or a.gemelo): raise BanderaMala('ECO v2.1: --lee va solo')
    if a.prueba_pool and (a.ventana is not None or a.pool != 2 or a.reanuda or a.gemelo): raise BanderaMala('ECO v2.1: --prueba_pool --pool 2')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 3 or a.gemelo):
        raise BanderaMala('ECO v2.1: --serie --ventana serie|replica --pool 1..3 (siempre con el gemelo)')
    return a


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.lee is not None:
        lee(a.lee); return
    if a.humo:
        if a.gemelo: usa_gemelo()
        ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"eco_v21_humo_{'gemelo' if a.gemelo else 'python'}_{ts}")
        os.makedirs(carpeta, exist_ok=True); t0 = time.time()
        print(f"[{time.strftime('%H:%M:%S')}] HUMO ECO v2.1 ({'gemelo' if a.gemelo else 'Python'}) · shas {SHAS()}", flush=True)
        for b in BRAZOS:
            x = trabajo((HUMO['semilla'], HUMO['mundo'], b, HUMO['T'], HUMO['t_corte'], carpeta, False))
            print(f"[{time.strftime('%H:%M:%S')}] {HUMO['mundo']} {b}: {x['seg']} s · persiste {x['persiste']} (vivos {x['vivos_T']}, max {x['max_vivos']}) · "
                  f"banco con ensena {x['banco_on']['ensena']} · filtra0 {x['banco_on']['filtra0']} · vivos con ensena {x['vivos_on']['ensena']} · "
                  f"sel ensena {x['sel_corte'][IORG['ensena']] if x['sel_corte'] else None}", flush=True)
        print(f"HUMO: {round(time.time() - t0, 1)} s (numeros sin valor) · {os.path.relpath(carpeta, RAIZ)}")
        return
    usa_gemelo()
    if a.prueba_pool:
        semillas = range(PRUEBA['desde'], PRUEBA['desde'] + PRUEBA['n']); T, tc = PRUEBA['T'], PRUEBA['t_corte']; etq = 'eco_v21_prueba_pool'
    else:
        d0 = VENTANAS[a.ventana]; semillas = range(d0, d0 + N); T, tc = V2['T'], V2['t_corte']; etq = f"eco_v21_{a.ventana}_s{d0}-{d0 + N - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, 'w*_s*.json')):
        raise SystemExit(f"ECO v2.1: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ECO v2.1 {etq} · T {T} · corte {tc} · mundos {MUNDOS} · pool {a.pool} · motor GEMELO · shas {SHAS()}")
    # los mundos grandes primero: el Pool termina antes
    jobs = [(s, m, b, T, tc, carpeta, a.reanuda) for m in ('w270', 'w90', 'w30') for s in semillas for b in BRAZOS]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool, initializer=usa_gemelo) as pool:
        for k, x in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] {x['mundo']} {x['brazo']} s{x['seed']}: persiste {x['persiste']} (vivos {x['vivos_T']}, max {x['max_vivos']}) · "
                f"banco con ensena {x['banco_on']['ensena']} · filtra0 {x['banco_on']['filtra0']} ({x['seg']} s; {round(time.time() - t0)} s)")
    v, L, d, R = lee(carpeta, len(semillas))
    for l in L: flog.write(l + '\n')
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d=d, seg=round(time.time() - t0), V2=V2, MUNDOS=MUNDOS, SERIE=SERIE, shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    log(f"VEREDICTO: {v}")
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
