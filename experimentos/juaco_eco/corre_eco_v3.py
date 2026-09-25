"""corre_eco_v3.py — RUNNER de JUACO-ECO v3: LOS 7 ÓRGANOS DEL FRANKENSTEIN COMO GENES, en DOS MUNDOS a la vez (nube, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/juaco_eco/PREREGISTRO_eco_v3.md (la letra esta AQUI, en veredicto(), y alli).
Es ECO v2 (corre_eco_v2.py) con OTRO organismo y otros mundos; la letra por organo es la misma idea:
  - el genoma tiene 25 genes: los 18 de v1 + las 7 perillas del Frankenstein del PC (b5, mapa, curiosidad, modelo, lenta, herencia,
    interruptor) como rasgos con umbral que nacen APAGADOS (motor_eco3 + carros/FRANK_ECO; arnes identidad_eco_frank.py 9/9);
  - DOS MUNDOS a la vez: esc 9 (el tamano de la carrera) y esc 30; el Frankenstein no tiene gemelo y corre en Python;
  - brazos VIDA y AZAR; T 120 000, corte 60 000; sin juez de colonias.
Uso (ERR-115: banderas desconocidas o abreviadas abortan):
  python experimentos/juaco_eco/corre_eco_v3.py --humo
  python experimentos/juaco_eco/corre_eco_v3.py --prueba_pool --pool 2
  python experimentos/juaco_eco/corre_eco_v3.py --serie --ventana serie --pool 3      # semillas 20111-20130
  python experimentos/juaco_eco/corre_eco_v3.py --serie --ventana replica --pool 3    # semillas 20131-20150
  python experimentos/juaco_eco/corre_eco_v3.py --serie --ventana serie --pool 3 --reanuda
  python experimentos/juaco_eco/corre_eco_v3.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, os, pickle, sys, time, types
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
for _d in (AQUI, os.path.join(RAIZ, 'experimentos', 'generaciones')):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_eco as CR          # eco_cfg (brazos VIDA/AZAR, SERIE), sel_genes; NO se usa su motor
import motor_eco3 as ME2    # (el nombre ME2 se conserva del runner de v2: aqui es motor_eco3)

MOTOR = [ME2]                    # el motor en uso: Python (el Frankenstein no tiene gemelo)
CARRO = 'FRANK_ECO'
SERIE = CR.SERIE                 # banco 200, 8 sombras, sigma 0.15, p_mut 0.05, cada_gen 2000, ckpt_cada 10000
V2 = dict(T=120000, t_corte=60000)
MUNDOS = {'w9': dict(esc=9, n0=9, tope=3000), 'w30': dict(esc=30, n0=30, tope=3000)}
BRAZOS = ('VIDA', 'AZAR')
VENTANAS = {'serie': 20111, 'replica': 20131}
N = 20
PRUEBA = dict(desde=20197, n=2, T=4000, t_corte=2500)
HUMO = dict(semilla=20196, mundo='w30', T=20000, t_corte=10000)
ORGANOS = ('b5', 'mapa', 'curiosidad', 'modelo', 'lenta', 'herencia', 'interruptor')
IORG = {g: ME2.NOMBRES.index(g) for g in ORGANOS}
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


def usa_gemelo():
    """ECO v3 no tiene gemelo (el Frankenstein corre en Python): no cambia nada."""
    return None


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

    sombras = {}   # ENMIENDA 1 (nube-8): expresion del organo en el banco del corte, real contra sus 8 sombras

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
    if list(E['genes']) != list(ME2.NOMBRES): raise SystemExit(f"ECO v3: genoma inesperado {E['genes']}")
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
               motor='PYTHON motor_eco3')
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck): os.remove(ck)
    return res


# ================================================================================ LA LETRA (PREREGISTRO_eco_v3.md §6, con la ENMIENDA 1)
def veredicto(R, n_esperado=N):
    """ENMIENDA 1 (nube-8, antes de cualquier serie de v3): por organo g y mundo m, ELEGIDO si en VIDA la fraccion del banco del corte que
    EXPRESA g supera a la media de las fracciones de sus 8 sombras (estricto) en >= 15/20 (O1*) y el banco de VIDA lo expresa mas que el de
    AZAR (pareado, estricto) en >= 15/20 (O2). La media contra sombras (O1 original) y el DESCARTADO quedan como DESCRIPTIVOS."""
    L = []
    completo = all(sum(1 for x in R if x['mundo'] == m and x['brazo'] == b) == n_esperado for m in MUNDOS for b in BRAZOS)
    bloq = sum(x['bloqueados'] for x in R)
    genes = list(ME2.NOMBRES)
    guardia = []; perfil = {}
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
        eA = {g: expr('AZAR', g) for g in ORGANOS}
        guardia += [(m, g, 'expresion', eA[g][:2]) for g in ORGANOS if eA[g][0] >= 15]   # AZAR no puede "expresar por encima" 15/20
        perfil[m] = {}
        for g in ORGANOS:
            cv = cuenta('VIDA', g); ev = expr('VIDA', g)
            mas = menos = k = 0
            for s_ in sorted(set(by['VIDA']) & set(by['AZAR'])):
                a, b = by['VIDA'][s_]['banco_on'][g], by['AZAR'][s_]['banco_on'][g]
                if a is None or b is None: continue
                k += 1; mas += int(a > b); menos += int(a < b)
            est = ('ELEGIDO' if (ev[0] >= 15 and mas >= 15) else 'sube' if (ev[0] >= 15 or mas >= 15) else
                   'baja' if (ev[1] >= 15 and menos >= 15) else 'neutro')
            perfil[m][g] = est
            med = lambda br: (float(np.median([x['banco_on'][g] for x in by[br].values() if x['banco_on'][g] is not None]))
                              if any(x['banco_on'][g] is not None for x in by[br].values()) else None)
            L.append(f"[{m}] {g:11s} VIDA expresa sobre la media de sus sombras {ev[0]}/{ev[2]} (debajo {ev[1]}) · AZAR {eA[g][0]}/{eA[g][2]} · "
                     f"banco con el organo (mediana) VIDA {med('VIDA')} · AZAR {med('AZAR')} · VIDA > AZAR {mas}/{k} (VIDA < AZAR {menos}) · "
                     f"descriptivo media contra sombras VIDA {cv} AZAR {cA[g]} -> {est}")
        pers = {b: sum(x['persiste'] for x in by[b].values()) for b in BRAZOS}
        L.append(f"[{m}] perillas seleccionadas en VIDA (>= 15/20, sin organos): "
                 f"{[(g, cuenta('VIDA', g)) for g in genes if g not in ORGANOS and max(cuenta('VIDA', g)) >= 15]} · persisten en T: {pers}")
    elegidos = {m: [g for g, e in perfil[m].items() if e == 'ELEGIDO'] for m in MUNDOS}
    en_todos = [g for g in ORGANOS if all(perfil[m][g] == 'ELEGIDO' for m in MUNDOS)]
    alguno = sorted(set(g for m in MUNDOS for g in elegidos[m]))
    sube_todos = [g for g in ORGANOS if all(perfil[m][g] in ('ELEGIDO', 'sube') for m in MUNDOS)]
    L.append(f"ANATOMIA por mundo: { {m: perfil[m] for m in MUNDOS} }")
    if not completo: v = 'NO EVALUABLE (serie incompleta)'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq})'
    elif guardia: v = f'NO EVALUABLE (AZAR da falsos positivos contra sombras: {guardia})'
    elif en_todos: v = f'FUNCIONA: LA SELECCION ELIGE ORGANOS (en esta serie): {en_todos} ELEGIDO en los {len(MUNDOS)} mundos'
    elif alguno or sube_todos: v = f'HAY ALGO MODESTO (en esta serie): ELEGIDO en algun mundo {alguno}; sube en todos {sube_todos}'
    else: v = 'NO (en esta serie)'
    L.append(f"VEREDICTO ECO v3 POR LA LETRA (una serie; el del bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(perfil=perfil, en_todos=en_todos, alguno=alguno, sube_todos=sube_todos, guardia=guardia)


def lee(carpeta, n_esperado=N):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, 'w*_s*.json')))]
    v, L, d = veredicto(R, n_esperado)
    for l in L: print(l, flush=True)
    return v, L, d, R


def SHAS():
    f = lambda p: hashlib.sha256(open(os.path.join(AQUI, p), 'rb').read()).hexdigest()[:16]
    d = {p: f(p) for p in ('corre_eco_v3.py', 'corre_eco.py', 'motor_eco3.py', 'carros/FRANK_ECO.py', 'construye_eco_frank.py',
                           'PREREGISTRO_eco_v3.md') if os.path.exists(os.path.join(AQUI, p))}
    d['organismo_frankenstein.py'] = hashlib.sha256(open(os.path.join(RAIZ, 'experimentos', 'frankenstein', 'organismo_frankenstein.py'), 'rb').read()).hexdigest()[:16]
    return d


def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--prueba_pool', action='store_true'); ap.add_argument('--lee', default=None)
    ap.add_argument('--ventana', default=None); ap.add_argument('--pool', type=int)
    ap.add_argument('--reanuda', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('ECO v3: banderas mal formadas')
    if resto: raise BanderaMala(f"ECO v3: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('ECO v3: sin la forma --bandera=valor')
    if len(argv) != len(set(x for x in argv if x.startswith('--'))) + sum(1 for x in argv if not x.startswith('--')):
        raise BanderaMala('ECO v3: bandera repetida')
    if int(a.humo) + int(a.serie) + int(a.prueba_pool) + int(a.lee is not None) != 1:
        raise BanderaMala('ECO v3: exactamente uno de --humo, --serie, --prueba_pool, --lee')
    if a.humo and (a.ventana is not None or a.pool is not None or a.reanuda): raise BanderaMala('ECO v3: --humo va solo')
    if a.lee is not None and (a.ventana is not None or a.pool is not None or a.reanuda): raise BanderaMala('ECO v3: --lee va solo')
    if a.prueba_pool and (a.ventana is not None or a.pool != 2 or a.reanuda): raise BanderaMala('ECO v3: --prueba_pool --pool 2')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 3):
        raise BanderaMala('ECO v3: --serie --ventana serie|replica --pool 1..3')
    return a


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.lee is not None:
        lee(a.lee); return
    if a.humo:
        ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"eco_v3_humo_python_{ts}")
        os.makedirs(carpeta, exist_ok=True); t0 = time.time()
        print(f"[{time.strftime('%H:%M:%S')}] HUMO ECO v3 (Python) · shas {SHAS()}", flush=True)
        for b in BRAZOS:
            x = trabajo((HUMO['semilla'], HUMO['mundo'], b, HUMO['T'], HUMO['t_corte'], carpeta, False))
            print(f"[{time.strftime('%H:%M:%S')}] {HUMO['mundo']} {b}: {x['seg']} s · persiste {x['persiste']} (vivos {x['vivos_T']}, max {x['max_vivos']}) · "
                  f"banco con el organo {x['banco_on']} · sel {dict((g, x['sel_corte'][IORG[g]]) for g in ORGANOS) if x['sel_corte'] else None}", flush=True)
        print(f"HUMO: {round(time.time() - t0, 1)} s (numeros sin valor) · {os.path.relpath(carpeta, RAIZ)}")
        return
    usa_gemelo()
    if a.prueba_pool:
        semillas = range(PRUEBA['desde'], PRUEBA['desde'] + PRUEBA['n']); T, tc = PRUEBA['T'], PRUEBA['t_corte']; etq = 'eco_v3_prueba_pool'
    else:
        d0 = VENTANAS[a.ventana]; semillas = range(d0, d0 + N); T, tc = V2['T'], V2['t_corte']; etq = f"eco_v3_{a.ventana}_s{d0}-{d0 + N - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, 'w*_s*.json')):
        raise SystemExit(f"ECO v3: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ECO v3 {etq} · T {T} · corte {tc} · mundos {MUNDOS} · pool {a.pool} · motor PYTHON · shas {SHAS()}")
    # los mundos grandes primero: el Pool termina antes
    jobs = [(s, m, b, T, tc, carpeta, a.reanuda) for m in ('w30', 'w9') for s in semillas for b in BRAZOS]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool, initializer=usa_gemelo) as pool:
        for k, x in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] {x['mundo']} {x['brazo']} s{x['seed']}: persiste {x['persiste']} (vivos {x['vivos_T']}, max {x['max_vivos']}) · "
                f"banco con organo {x['banco_on']} ({x['seg']} s; {round(time.time() - t0)} s)")
    v, L, d, R = lee(carpeta, len(semillas))
    for l in L: flog.write(l + '\n')
    json.dump(dict(etiqueta=etq, veredicto=v, lineas=L, d=d, seg=round(time.time() - t0), V3=V2, MUNDOS=MUNDOS, SERIE=SERIE, shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    log(f"VEREDICTO: {v}")
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
