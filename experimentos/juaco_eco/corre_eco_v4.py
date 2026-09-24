"""corre_eco_v4.py — RUNNER de JUACO-ECO v4: EL PAQUETE herencia (= el organo de ensenar) + interruptor, en el mundo mediano (nube, 24-sep-2026).

MISION: llegar a la AGI por este camino.

Preregistro: experimentos/juaco_eco/PREREGISTRO_eco_v4.md (la letra esta AQUI, en veredicto(), y alli).
Es corre_eco_v3.py (sha 7bb44da802508b37) con TRES cambios, nada mas:
  - de los 7 organos del Frankenstein como genes, solo MUTAN los 2 del paquete: herencia (el padre pasa su tabla en el parto: subida_n10b
    'res' verbatim, el MISMO organo que 'ensena' de ECO v2.1) e interruptor (explorar/explotar por necesidad). Los otros 5 (b5, mapa,
    curiosidad, modelo, lenta) nacen apagados y NO mutan, ni en el genoma real ni en las sombras (motor_eco3: 'mutables');
  - los DOS mundos de v3 (w30 y w9). (Se penso en w90, el de ECO v2.1, pero el arnes midio el costo del Frankenstein en Python ahi:
    ~19 ms por paso con ~100 cuerpos, unas 12 h por serie con Pool 3; en w30 + w9 v3 tardo 80 min por serie);
  - la letra es la del paquete (veredicto()).
Motor Python (motor_eco3 + carros/FRANK_ECO; el Frankenstein no tiene gemelo). Brazos VIDA y AZAR; T 120 000, corte 60 000.
Uso (ERR-115: banderas desconocidas o abreviadas abortan):
  python experimentos/juaco_eco/corre_eco_v4.py --humo
  python experimentos/juaco_eco/corre_eco_v4.py --prueba_pool --pool 2
  python experimentos/juaco_eco/corre_eco_v4.py --serie --ventana serie --pool 3      # semillas 20311-20330
  python experimentos/juaco_eco/corre_eco_v4.py --serie --ventana replica --pool 3    # semillas 20331-20350
  python experimentos/juaco_eco/corre_eco_v4.py --serie --ventana serie --pool 3 --reanuda
  python experimentos/juaco_eco/corre_eco_v4.py --lee <carpeta>
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
MUNDOS = {'w30': dict(esc=30, n0=30, tope=3000), 'w9': dict(esc=9, n0=9, tope=3000)}   # los grandes primero
BRAZOS = ('VIDA', 'AZAR')
VENTANAS = {'serie': 20311, 'replica': 20331}
N = 20
PRUEBA = dict(desde=20397, n=2, T=4000, t_corte=2500)
HUMO = dict(semilla=20396, mundo='w30', T=20000, t_corte=10000)
ORGANOS = ('b5', 'mapa', 'curiosidad', 'modelo', 'lenta', 'herencia', 'interruptor')
IORG = {g: ME2.NOMBRES.index(g) for g in ORGANOS}
PAQUETE = ('herencia', 'interruptor')                    # ECO v4: los dos organos que mutan (herencia = 'ensena' de v2.1)
FIJOS = tuple(g for g in ORGANOS if g not in PAQUETE)    # nacen apagados y NO mutan (real y sombras)
MUTABLES = tuple(g for g in ME2.NOMBRES if g not in FIJOS)   # las 18 perillas + los 2 del paquete
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


def usa_gemelo():
    """ECO v4 no tiene gemelo (el Frankenstein corre en Python): no cambia nada."""
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


def cfg_v4(brazo, t_corte, guarda, estado, cb):
    """ECO v4: la configuracion de v3 (CR.eco_cfg) con los 5 organos FIJOS fuera de la mutacion, en VIDA y en AZAR por igual."""
    c = CR.eco_cfg(brazo, t_corte, ckpt_cada=SERIE['ckpt_cada'], ckpt_fn=guarda, estado=estado, ind_cb=cb)
    c['mutables'] = MUTABLES
    return c


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
                               eco=cfg_v4(brazo, t_corte, guarda, estado, cb))
    E = r['eco']; P = r['pista']
    if list(E['genes']) != list(ME2.NOMBRES): raise SystemExit(f"ECO v4: genoma inesperado {E['genes']}")
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
               motor='PYTHON motor_eco3', mutables=E.get('mutables'))
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f: json.dump(res, f)
    os.replace(tmp, fin)
    if os.path.exists(ck): os.remove(ck)
    return res


# ================================================================================ LA LETRA (PREREGISTRO_eco_v4.md §6)
def veredicto(R, n_esperado=N):
    """ECO v4: por organo g del PAQUETE y mundo m, ELEGIDO si en VIDA la fraccion del banco del corte que EXPRESA g supera a la media de
    las de sus 8 sombras (estricto) en >= 15/20 (O1*) y el banco de VIDA lo expresa mas que el de AZAR (pareado, estricto) en >= 15/20
    (O2); 'sube' = uno de los dos. FUNCIONA si los DOS organos del paquete quedan ELEGIDOS en un mismo mundo; MODESTO si alguno queda
    ELEGIDO o los dos 'suben'; NO en otro caso. NO EVALUABLE: serie incompleta, bloqueados, un organo FIJO expresado, o AZAR con falsos
    positivos (> 8/20 en algun gen por la media contra sombras, o >= 15/20 de expresion sobre sombras en un organo del paquete)."""
    L = []
    completo = all(sum(1 for x in R if x['mundo'] == m and x['brazo'] == b) == n_esperado for m in MUNDOS for b in BRAZOS)
    bloq = sum(x['bloqueados'] for x in R)
    fijo_on = [(x['mundo'], x['brazo'], x['seed'], g) for x in R for g in FIJOS
               if (x['banco_on'].get(g) or 0) > 0 or (x['vivos_on'].get(g) or 0) > 0]
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
        eA = {g: expr('AZAR', g) for g in PAQUETE}
        guardia += [(m, g, 'expresion', eA[g][:2]) for g in PAQUETE if eA[g][0] >= 15]
        perfil[m] = {}
        for g in PAQUETE:
            cv = cuenta('VIDA', g); ev = expr('VIDA', g)
            mas = menos = k = 0
            for s_ in sorted(set(by['VIDA']) & set(by['AZAR'])):
                a_, b_ = by['VIDA'][s_]['banco_on'][g], by['AZAR'][s_]['banco_on'][g]
                if a_ is None or b_ is None: continue
                k += 1; mas += int(a_ > b_); menos += int(a_ < b_)
            est = ('ELEGIDO' if (ev[0] >= 15 and mas >= 15) else 'sube' if (ev[0] >= 15 or mas >= 15) else
                   'baja' if (ev[1] >= 15 and menos >= 15) else 'neutro')
            perfil[m][g] = est
            med = lambda br: (float(np.median([x['banco_on'][g] for x in by[br].values() if x['banco_on'][g] is not None]))
                              if any(x['banco_on'][g] is not None for x in by[br].values()) else None)
            medv = lambda br: (float(np.median([x['vivos_on'][g] for x in by[br].values() if x['vivos_on'][g] is not None]))
                               if any(x['vivos_on'][g] is not None for x in by[br].values()) else None)
            L.append(f"[{m}] {g:11s} VIDA expresa sobre la media de sus sombras {ev[0]}/{ev[2]} (debajo {ev[1]}) · AZAR {eA[g][0]}/{eA[g][2]} · "
                     f"banco con el organo (mediana) VIDA {med('VIDA')} · AZAR {med('AZAR')} · VIDA > AZAR {mas}/{k} (VIDA < AZAR {menos}) · "
                     f"vivos en T con el organo VIDA {medv('VIDA')} · AZAR {medv('AZAR')} · descriptivo media contra sombras VIDA {cv} AZAR {cA[g]} -> {est}")
        pers = {b: sum(x['persiste'] for x in by[b].values()) for b in BRAZOS}
        L.append(f"[{m}] perillas seleccionadas en VIDA (>= 15/20, sin organos): "
                 f"{[(g, cuenta('VIDA', g)) for g in genes if g not in ORGANOS and max(cuenta('VIDA', g)) >= 15]} · persisten en T: {pers}")
    ok = {m: [g for g in PAQUETE if perfil[m][g] == 'ELEGIDO'] for m in MUNDOS}
    arman = [m for m in MUNDOS if len(ok[m]) == len(PAQUETE)]
    alguno = sorted(set(g for m in MUNDOS for g in ok[m]))
    suben = [m for m in MUNDOS if all(perfil[m][g] in ('ELEGIDO', 'sube') for g in PAQUETE)]
    L.append(f"PAQUETE por mundo: { {m: perfil[m] for m in MUNDOS} }")
    if not completo: v = 'NO EVALUABLE (serie incompleta)'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos alcanzado: bloqueados = {bloq})'
    elif fijo_on: v = f'NO EVALUABLE (instrumento: un organo FIJO se expreso: {fijo_on[:5]})'
    elif guardia: v = f'NO EVALUABLE (AZAR da falsos positivos contra sombras: {guardia})'
    elif arman: v = f'FUNCIONA: LA SELECCION ARMA EL PAQUETE (en esta serie): herencia e interruptor ELEGIDOS en {arman}'
    elif alguno or suben: v = f'HAY ALGO MODESTO (en esta serie): ELEGIDO {alguno}; los dos suben en {suben}'
    else: v = 'NO (en esta serie)'
    L.append(f"VEREDICTO ECO v4 POR LA LETRA (una serie; el del bloque exige serie + replica con el mismo veredicto): {v}")
    return v, L, dict(perfil=perfil, arman=arman, alguno=alguno, suben=suben, guardia=guardia, fijo_on=fijo_on)


def lee(carpeta, n_esperado=N):
    R = [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(carpeta, 'w*_s*.json')))]
    v, L, d = veredicto(R, n_esperado)
    for l in L: print(l, flush=True)
    return v, L, d, R


def SHAS():
    f = lambda p: hashlib.sha256(open(os.path.join(AQUI, p), 'rb').read()).hexdigest()[:16]
    d = {p: f(p) for p in ('corre_eco_v4.py', 'corre_eco.py', 'motor_eco3.py', 'carros/FRANK_ECO.py', 'construye_eco_frank.py',
                           'PREREGISTRO_eco_v4.md') if os.path.exists(os.path.join(AQUI, p))}
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
        raise BanderaMala('ECO v4: banderas mal formadas')
    if resto: raise BanderaMala(f"ECO v4: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('ECO v4: sin la forma --bandera=valor')
    if len(argv) != len(set(x for x in argv if x.startswith('--'))) + sum(1 for x in argv if not x.startswith('--')):
        raise BanderaMala('ECO v4: bandera repetida')
    if int(a.humo) + int(a.serie) + int(a.prueba_pool) + int(a.lee is not None) != 1:
        raise BanderaMala('ECO v4: exactamente uno de --humo, --serie, --prueba_pool, --lee')
    if a.humo and (a.ventana is not None or a.pool is not None or a.reanuda): raise BanderaMala('ECO v4: --humo va solo')
    if a.lee is not None and (a.ventana is not None or a.pool is not None or a.reanuda): raise BanderaMala('ECO v4: --lee va solo')
    if a.prueba_pool and (a.ventana is not None or a.pool != 2 or a.reanuda): raise BanderaMala('ECO v4: --prueba_pool --pool 2')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 3):
        raise BanderaMala('ECO v4: --serie --ventana serie|replica --pool 1..3')
    return a


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.lee is not None:
        lee(a.lee); return
    if a.humo:
        ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"eco_v4_humo_python_{ts}")
        os.makedirs(carpeta, exist_ok=True); t0 = time.time()
        print(f"[{time.strftime('%H:%M:%S')}] HUMO ECO v4 (Python) · shas {SHAS()}", flush=True)
        for b in BRAZOS:
            x = trabajo((HUMO['semilla'], HUMO['mundo'], b, HUMO['T'], HUMO['t_corte'], carpeta, False))
            print(f"[{time.strftime('%H:%M:%S')}] {HUMO['mundo']} {b}: {x['seg']} s · persiste {x['persiste']} (vivos {x['vivos_T']}, max {x['max_vivos']}) · "
                  f"banco con el organo {x['banco_on']} · sel {dict((g, x['sel_corte'][IORG[g]]) for g in ORGANOS) if x['sel_corte'] else None}", flush=True)
        print(f"HUMO: {round(time.time() - t0, 1)} s (numeros sin valor) · {os.path.relpath(carpeta, RAIZ)}")
        return
    usa_gemelo()
    if a.prueba_pool:
        semillas = range(PRUEBA['desde'], PRUEBA['desde'] + PRUEBA['n']); T, tc = PRUEBA['T'], PRUEBA['t_corte']; etq = 'eco_v4_prueba_pool'
    else:
        d0 = VENTANAS[a.ventana]; semillas = range(d0, d0 + N); T, tc = V2['T'], V2['t_corte']; etq = f"eco_v4_{a.ventana}_s{d0}-{d0 + N - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, 'w*_s*.json')):
        raise SystemExit(f"ECO v4: {carpeta} ya tiene resultados; --reanuda (no se pisa nada)")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')

    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"ECO v4 {etq} · T {T} · corte {tc} · mundos {MUNDOS} · pool {a.pool} · motor PYTHON · shas {SHAS()}")
    # los mundos grandes primero: el Pool termina antes
    jobs = [(s, m, b, T, tc, carpeta, a.reanuda) for m in MUNDOS for s in semillas for b in BRAZOS]
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
