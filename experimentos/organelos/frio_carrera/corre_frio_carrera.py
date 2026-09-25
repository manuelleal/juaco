"""corre_frio_carrera.py — RUNNER y LETRA del bloque frio_carrera: F1 ("pasar solo lo que tuvo consecuencia") en la PISTA DE LA CARRERA.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Preregistro: PREREGISTRO_frio_carrera.md (la letra esta AQUI, en veredicto(), y alli).

Pregunta: el principio de F1 (el nacido hereda SOLO lo que tuvo consecuencia, sin lo neutro; FUNCIONA x2 en ECO w90) ¿rompe el muro
H-1 de la carrera con el bicho real v14.3? En la carrera el carro es el cerebro del linaje y lo que hereda el nacido es el NODO del
linaje; V143_RES0 lee el nodo sin las entradas R == 0 (construye_frio_carrera.py).

ENTRADA (regla 14): la corrida ES experimentos/tronco_v14_3/corre_v143.tarea (se IMPORTA, no se toca; sha fijado), que es
juez.tarea(seed, 9 carros iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje (solo
fisica, ERR-96). Los carros nuevos se registran en su cache de modulos (corre_v143._MODS) y en su tabla BRAZOS, en memoria. Lo unico
agregado: 'tel_fc' = la telemetria de SOLO LECTURA de los carros frio_carrera (se captura envolviendo pista.run en memoria; no puntua).
Resumen y pareados: corre_v143.resume y corre_v143.pareado, tal cual.

BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, fundador limpio = ENMIENDA 5):
  v143  V143        (base: el candidato v14.3 de la serie 14301 / replica 14321)
  res0  V143_RES0   (HIPOTESIS: el nacido lee el nodo del linaje sin las entradas neutras)
  bar0  V143_BAR0   (control de CONTENIDO que puede ganar: RES0 con las R permutadas entre entradas en cada lectura)
  o1    O1          (techo escrito por un LLM; ANCLA de la pista)
  tel   V143_TEL    (SOLO humo/arnes: V143 + telemetria; mide cuantas entradas del nodo de V143 son neutras)
SEMILLAS: serie 36001-36020 · replica 36021-36040 · practica 36901-36909 (arnes 36901-36904, humo 36905-36906). El runner se niega a
usar otras.
nube-9: trabajo() atrapa TODA excepcion (SystemExit incluida: la guardia ERR-60 de la pista es un SystemExit) y devuelve un resultado
marcado 'aborto'; ningun trabajador del Pool muere. Cualquier aborto -> la serie es NO EVALUABLE (no se imputa nada).
Cada corrida escribe su JSON en la carpeta de la serie ANTES de volver (ERR-54); --reanuda salta las que ya estan.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN; SOLO el coordinador lanza --serie):
  python experimentos/organelos/frio_carrera/corre_frio_carrera.py --humo                         # 1 proceso: 36905 x (tel, res0, bar0, o1) + 36906 x (tel, res0), T 20 000
  python experimentos/organelos/frio_carrera/corre_frio_carrera.py --serie --desde 36001 --n 20 --pool 6       # serie
  python experimentos/organelos/frio_carrera/corre_frio_carrera.py --serie --desde 36021 --n 20 --pool 6       # replica
  python experimentos/organelos/frio_carrera/corre_frio_carrera.py --serie --desde 36001 --n 20 --pool 6 --reanuda
  python experimentos/organelos/frio_carrera/corre_frio_carrera.py --bloque <resumen serie>.json,<resumen replica>.json
"""
import argparse, hashlib, importlib.util, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV          # tarea, resume, pareado, verifica_todo (se IMPORTA, no se toca)
import construye_frio_carrera as CF
import revisa_carro as RC
P = CV.P; J = CV.J

CARROS = os.path.join(AQUI, 'carros')
DATOS = os.path.join(AQUI, 'datos')
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028'}
BRAZOS = {'v143': 'V143', 'res0': 'V143_RES0', 'bar0': 'V143_BAR0', 'o1': 'O1', 'tel': 'V143_TEL'}
PROPIOS = ('V143_RES0', 'V143_BAR0', 'V143_TEL')
SERIE_BRAZOS = ('v143', 'res0', 'bar0', 'o1')
SERIE = range(36001, 36021); REPLICA = range(36021, 36041); PRACTICA = range(36901, 36910)
HUMO = [(36905, 'tel'), (36905, 'res0'), (36905, 'bar0'), (36905, 'o1'), (36906, 'tel'), (36906, 'res0')]   # tel == v143 en la fisica (arnes 3)
T_DEF = 100000; T_HUMO = 20000
GANA = 15                       # >= 15/20 semillas (la de la carrera: ENMIENDAS 2, 5, 6 y corre_v143.GANA)
DIF_MOD = 0.10                  # diferencia mediana pareada minima para HAY ALGO MODESTO (la de corre_v143.DIF_MOD)
ANCLA_V143 = (0.40, 0.80)       # V143, mediana del R0 real de todos los linajes: 0.536 (14301), 0.63 (14321), 0.587 / 0.637 (nube, 6+6)
BAR_REAL = 0.50                 # V4: fraccion minima de lecturas de BAR0 en que la permutacion cambia alguna R


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def registra():
    """Pone los carros frio_carrera en la cache de modulos de corre_v143 (cargados por ruta) y en su tabla BRAZOS (en memoria)."""
    for n in PROPIOS:
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", os.path.join(CARROS, n + '.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    for k in ('res0', 'bar0', 'tel'): CV.BRAZOS.setdefault(k, BRAZOS[k])


def tarea(args):
    """(seed, carro, T) -> corre_v143.tarea tal cual + 'tel_fc' (telemetria de solo lectura de los carros frio_carrera)."""
    registra()
    cap = []; orig = P.run

    def run2(*a, **k):
        r = orig(*a, **k); cap.append([(d.get('carro') or {}).get('frio_carrera') for d in r['linajes']]); return r
    P.run = run2
    try:
        x = CV.tarea(args)
    finally:
        P.run = orig
    x['tel_fc'] = cap[0] if cap else None
    return x


def trabajo(args):
    """UNA corrida; atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54); con reanuda salta la que ya existe."""
    seed, brazo, T, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: return json.load(fh)
    try:
        x = tarea((seed, BRAZOS[brazo], T)); x.pop('pizarra_log', None); x['brazo'] = brazo; x['aborto'] = None
    except BaseException as e:   # noqa: nube-9 (SystemExit de la guardia ERR-60 incluido)
        x = dict(seed=seed, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


def fc_suma(R):
    """Suma de la telemetria frio_carrera (ultima instancia de cada linaje; fundador limpio = instancia nueva)."""
    tot = {}
    for c in R:
        for t in (c.get('tel_fc') or []):
            if not t: continue
            for k, v in t.items():
                if isinstance(v, (int, float)) and k not in ('res0', 'bar', 'telem'): tot[k] = tot.get(k, 0) + v
    if tot:
        tot['frac_neutras_nodo'] = round(tot['neutras'] / tot['entradas'], 4) if tot.get('entradas') else None
        tot['frac_neutras_leidas'] = round(tot['sel_neutras'] / tot['sel'], 4) if tot.get('sel') else None
        tot['frac_bar_distintas'] = round(tot['bar_distintas'] / tot['bar_lect'], 4) if tot.get('bar_lect') else None
    return tot


def cuerpos(R):
    """Cuerpos que leen nodo (hijos de la cola) contra fundadores limpios (instancias nuevas, nodo vacio), de la fisica."""
    L = [l for c in R for l in c['linajes']]
    return dict(nac_reales=sum(l['nac_reales'] for l in L), fundadores=sum(l['fundadores'] for l in L))


def establece(R):
    """DESCRIPTIVO (propuesta del explorador de trasplantes, HALLAZGOS.md sec. 6): ESTABLECIMIENTO = linajes-semilla con 0 fundadores
    tras t 10 000; y R0 real (mediana) de los ESTABLECIDOS y de los NO establecidos. Solo fisica (juez.resumen_linaje). No puntua."""
    L = [l for c in R for l in c['linajes']]
    e = [l for l in L if l['fund_post10k'] == 0]; ne = [l for l in L if l['fund_post10k'] > 0]
    return dict(linajes=len(L), establecidos=len(e), frac_establecidos=(round(len(e) / len(L), 4) if L else None),
                R0_real_establecidos=CV.med([l['R0_real'] for l in e]), R0_real_no_establecidos=CV.med([l['R0_real'] for l in ne]),
                cruzan_de_establecidos=sum(l['cruza_real'] for l in e))


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_frio_carrera.md sec. 6)
def lee_serie(res, par, fc, completa, abortos):
    """Una serie: validez V1-V4, puertas P1-P3, veredicto de la serie."""
    v = {}
    v['V1_completa'] = bool(completa and abortos == 0 and all(b in res for b in SERIE_BRAZOS)
                            and all(res[b]['coherente'].split('/')[0] == res[b]['coherente'].split('/')[1] for b in SERIE_BRAZOS if b in res))
    v['V2_ancla_O1_gana'] = bool(res.get('o1', {}).get('gana_e5'))
    m = res.get('v143', {}).get('R0_real_med')
    v['V3_ancla_V143'] = m is not None and ANCLA_V143[0] <= m <= ANCLA_V143[1]
    f_r = fc.get('res0', {}); f_b = fc.get('bar0', {})
    v['V4_instrumento'] = bool(f_r.get('sel_neutras', 1) == 0 and (f_b.get('frac_bar_distintas') or 0) >= BAR_REAL)
    valido = all(v.values())
    p = {}
    p['P1_res0_cruza'] = bool(res.get('res0', {}).get('gana_e5'))
    x = par.get(('res0', 'v143')) or {}
    p['P2_res0_gana_v143'] = bool(x.get('semillas') and x['gana'] >= GANA * x['semillas'] / 20)
    p['P3_bar0_no_cruza'] = not bool(res.get('bar0', {}).get('gana_e5'))
    y = par.get(('res0', 'bar0')) or {}
    mod = bool(p['P2_res0_gana_v143'] and x.get('dif_med') is not None and x['dif_med'] >= DIF_MOD - 1e-12
               and y.get('semillas') and y['gana'] >= GANA * y['semillas'] / 20)
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif mod: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    return dict(validez=v, puertas=p, modesto=mod, veredicto=ver)


ORDEN = {'NO SE LEE': -1, 'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}


def bloque(v_serie, v_replica):
    """El bloque se declara solo si serie y replica dan el mismo veredicto; si no, vale el menor (NO SE LEE si alguna no se lee)."""
    if v_serie == v_replica: return v_serie
    return min((v_serie, v_replica), key=lambda z: ORDEN[z])


def valida(humo, desde, n, T, brazos):
    for b in brazos:
        if b not in BRAZOS: return f"brazo desconocido {b!r} (validos {list(BRAZOS)})"
    if n < 1: return "--n >= 1"
    sem = list(range(desde, desde + n))
    if humo:
        if not all(x in PRACTICA for x in sem): return "--humo: solo semillas de practica 36901-36909"
        if T > 30000: return "--humo: T <= 30000"
    else:
        if not (all(x in SERIE for x in sem) or all(x in REPLICA for x in sem)): return "serie: solo 36001-36020 (serie) o 36021-36040 (replica)"
        if T != T_DEF: return "serie: T = 100000 (preregistrado)"
        if tuple(brazos) != SERIE_BRAZOS: return f"serie: brazos {SERIE_BRAZOS} (preregistrado)"
    return None


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for n, b in CF.todas().items():
        ruta = os.path.join(CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = RC.revisa_fuente(b.decode('utf-8'), n) if igual else ['distinto de construye_frio_carrera']
        ok &= igual and not vr
        log(f"  carro {n} sha {CF.h16b(b)} == construye: {igual} · revisa_carro: {'PASA' if not vr else vr[:2]}")
    registra()
    N = lambda x: json.loads(json.dumps(x, default=str))
    m = CV._MODS['V143_RES0']; g = (m.RES0, m.BAR, m.TELEM)
    try:
        m.RES0 = 0; m.BAR = 0; m.TELEM = 0
        a = P.run(36901, [('C', CV.modulo('V143'))] * 9, T=2000, fundador_limpio=1)
        b = P.run(36901, [('C', m)] * 9, T=2000, fundador_limpio=1)
    finally:
        m.RES0, m.BAR, m.TELEM = g
    i1 = N(a) == N(b); ok &= i1
    log(f"  IDENTIDAD CORTA: V143_RES0 con RES0 = BAR = TELEM = 0 == V143 (salida ENTERA, N 9, s 36901, T 2000, fundador limpio): {'OK' if i1 else 'FALLA'}")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true')
    g.add_argument('--serie', action='store_true')
    g.add_argument('--bloque', default=None)
    ap.add_argument('--brazos', default=None)
    ap.add_argument('--desde', type=int, default=None)
    ap.add_argument('--n', type=int, default=None)
    ap.add_argument('--T', type=int, default=None)
    ap.add_argument('--pool', type=int, default=0)
    ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.bloque:
        rs = [json.load(open(x.strip(), encoding='utf-8')) for x in a.bloque.split(',')]
        if len(rs) != 2: raise SystemExit("--bloque: <resumen serie>,<resumen replica>")
        s0 = rs[0]['semillas'][0]; s1 = rs[1]['semillas'][0]
        if not (s0 in SERIE and s1 in REPLICA): raise SystemExit("--bloque: primero la serie 36001-36020 y luego la replica 36021-36040")
        vb = bloque(rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto'])
        print(f"serie {rs[0]['letra']['veredicto']} · replica {rs[1]['letra']['veredicto']} -> BLOQUE: {vb}")
        return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        T = a.T or T_HUMO
        if a.brazos or a.desde or a.n:
            brazos = [s for s in (a.brazos or 'v143,res0,bar0,o1').split(',') if s]; desde = a.desde or 36905; n = a.n or 1
            e = valida(True, desde, n, T, brazos)
            if e: raise SystemExit(e)
            tareas = [(s, b) for s in range(desde, desde + n) for b in brazos]
        else:
            tareas = list(HUMO)
            e = valida(True, 36905, 2, T, list(BRAZOS))
            if e: raise SystemExit(e)
        if len(tareas) > 6: raise SystemExit("--humo: maximo 6 corridas por proceso")
        semillas = sorted({s for s, _ in tareas}); brazos = [b for b in BRAZOS if any(b == x for _, x in tareas)]
        pool = 0; dest = os.path.join(DATOS, 'humo')
    else:
        T = a.T or T_DEF; desde = a.desde or 36001; n = a.n or 20; brazos = [s for s in (a.brazos or ','.join(SERIE_BRAZOS)).split(',') if s]
        e = valida(False, desde, n, T, brazos)
        if e: raise SystemExit(e)
        semillas = list(range(desde, desde + n)); tareas = [(s, b) for b in brazos for s in semillas]; pool = a.pool
        dest = DATOS
    sel = time.strftime('%Y%m%d_%H%M%S')
    pre = f"frio_carrera_{'humo_' if a.humo else ''}s{semillas[0]}-{semillas[-1]}_T{T}"
    carpeta = os.path.join(dest, pre if not a.humo else pre + '_' + sel)
    if a.reanuda and not a.humo:
        prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d)))
        if prev: carpeta = os.path.join(dest, prev[-1])
    elif not a.humo:
        carpeta = carpeta + '_' + sel
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    log(f"CORRE_FRIO_CARRERA · {pre} · {sel} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'} · "
        f"corre_frio_carrera.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  tareas {len(tareas)} · brazos {brazos} · semillas {semillas[0]}-{semillas[-1]} · T {T} · fundador limpio 1 · reanuda {a.reanuda}")
    ok = verifica(log)
    if a.humo:
        ok &= CV.verifica_todo(log, con_entrada=True)   # regla 14: corre_v143.tarea == juez.tarea (9 FABRICA, s 14281, T 2000)
        N = lambda x: json.loads(json.dumps(x, default=str))
        x = tarea((36901, 'V143', 2000)); y = CV.tarea((36901, 'V143', 2000))
        e14 = x.pop('tel_fc') == [None] * 9 and N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in y.items() if k != 'seg'})
        ok &= e14; log(f"  ENTRADA campo a campo (regla 14): tarea de este runner == corre_v143.tarea (V143, s 36901, T 2000): {'OK' if e14 else 'FALLA'}")
    if not ok: log("  ALGO FALLA -> no se corre."); return 1
    args = [(s, b, T, carpeta, a.reanuda) for s, b in tareas]
    R = []
    if pool and pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as PL:
            for x in PL.imap_unordered(trabajo, args):
                R.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} s{x['seed']} ({x.get('seg')}s) R0 pista {x.get('R0_pista')} aborto {x['aborto']}")
    else:
        for ar in args:
            x = trabajo(ar); R.append(x)
            log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} s{x['seed']} ({x.get('seg')}s) R0 pista {x.get('R0_pista')} aborto {x['aborto']} · "
                f"R0 real por linaje {[l['R0_real'] for l in x['linajes']]} · fundadores {[l['fundadores'] for l in x['linajes']]}")
    abortos = sum(1 for x in R if x['aborto'])
    por = {b: sorted([x for x in R if x['brazo'] == b and not x['aborto']], key=lambda z: z['seed']) for b in brazos}
    if a.humo and 'tel' in por and not por.get('v143'):   # HUMO: V143_TEL es V143 en la fisica (arnes (3)); hace de base con telemetria
        por['v143'] = por['tel']
    res = {}; fc = {}; cz = {}
    for b in [x for x in por if por[x]]:
        if not por[b]: continue
        res[b] = CV.resume(por[b], b, log); fc[b] = fc_suma(por[b]); cz[b] = cuerpos(por[b]); cz[b]['establece'] = establece(por[b])
        log(f"  ESTABLECIMIENTO ({b}, descriptivo): {cz[b]['establece']}")
        log(f"  frio_carrera ({b}): telemetria {fc[b] or '-'} · cuerpos que leen nodo (nacimientos reales) {cz[b]['nac_reales']} · "
            f"fundadores limpios (nodo vacio) {cz[b]['fundadores']}")
    PAR = (('res0', 'v143'), ('res0', 'bar0'), ('v143', 'bar0'), ('o1', 'v143'), ('o1', 'res0'))
    par = {k: CV.pareado(por[k[0]], por[k[1]]) for k in PAR if por.get(k[0]) and por.get(k[1])}
    log("\nPAREADOS (por semilla: mediana del R0 real de los 9 linajes; gana = semillas en que el primero supera al segundo)")
    for k, v in par.items(): log(f"  {k[0]} vs {k[1]}: gana {v['gana']}/{v['semillas']} · diferencia mediana {v['dif_med']}")
    completa = True if a.humo else all(len(por.get(b, [])) == len(semillas) for b in SERIE_BRAZOS)
    letra = lee_serie(res, par, fc, completa, abortos)
    log("\n================ LA LETRA (PREREGISTRO_frio_carrera.md sec. 6)" + (" -- HUMO: T corto y semillas de practica, NO cuenta" if a.humo else ""))
    log(f"  validez {letra['validez']}")
    log(f"  puertas {letra['puertas']} · modesto {letra['modesto']}")
    ver = ('HUMO (no cuenta): ' if a.humo else '') + letra['veredicto']
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(brazos=res, pareados={f"{k[0]}_vs_{k[1]}": x for k, x in par.items()}, telemetria=fc, cuerpos=cz, letra=letra,
                       semillas=semillas, T=T, humo=a.humo, abortos=abortos, veredicto=ver,
                       sha_runner=h16(os.path.abspath(__file__)), sha_carros={n: h16(os.path.join(CARROS, n + '.py')) for n in PROPIOS}),
                  fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)})\nTerminado en {time.time()-t0:.1f}s")
    log(f"VEREDICTO DE LA SERIE: {ver}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
