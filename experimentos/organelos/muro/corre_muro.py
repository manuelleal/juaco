"""corre_muro.py — RUNNER y LETRA del bloque MURO: ¿cruza H-1 el bicho real v14.3 + UNA pieza local (PAGA)?

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Preregistro: PREREGISTRO_muro.md (la letra esta AQUI, en lee_serie(), y alli).

Pieza (construye_muro.py, perilla GLOT = 3): GLOTU, "no comas para lo que ya tienes de sobra". La boca no muerde una letra cuyo dS
SENTIDO por el linaje (_adS, ya en v14.3) solo sube una necesidad j, si j es la MAS LLENA de las dos y ya esta en el umbral de
reproduccion o encima (rep_umbral del mundo, en ctx). Lo demas, v14.3 tal cual (patas, FILTRO con meta, opcion TD, sorteos). Estado
presente, cero memoria nueva. Exploratorio previo (37901-37905, declarado en INFORME.md): CTA / LIMPIA / SINEST / DESF / GLOT / GLOTCTA /
GLOTFILA / PATAS / PATASDESF pierden o empatan con V143; GLOTU gana 3/5 (+0.016); GLOTU + PATAS 4/5 (+0.03, dos piezas: no se preregistra).

ENTRADA (regla 14): la corrida ES experimentos/tronco_v14_3/corre_v143.tarea (se IMPORTA, no se toca; sha fijado) = juez.tarea(seed,
9 carros iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje (solo fisica, ERR-96).
Los carros nuevos se registran en su cache de modulos (corre_v143._MODS) y en su tabla BRAZOS, en memoria. Lo unico agregado:
'tel_muro' = telemetria de SOLO LECTURA (d['carro']['muro'] de la ULTIMA instancia de cada linaje; se captura envolviendo pista.run en
memoria; no puntua). Resumen y pareados: corre_v143.resume y corre_v143.pareado, tal cual.

BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, fundador limpio = ENMIENDA 5). SERIE = los 4 primeros:
  v143        V143            base: el bicho real (tronco_v14_3)
  glotu       V143_GLOTU      CANDIDATO (GLOT 3)
  glotuinv    V143_GLOTUINV   CONTROL que puede fallar, DESFASADO: la misma regla con la necesidad al reves (veta lo que solo sube la
                              MENOS llena cuando esa ya esta en el umbral). Misma memoria, misma lectura, mismos pasos.
  o1          O1              techo escrito por un LLM; ANCLA de la pista
  mtel        V143_MTEL       solo humo/arnes: V143 + telemetria (fisica identica a V143)
  Solo exploratorio (explora_muro.py): cta, desf, limpia, sinest (PAGA 1-4), glot, glotfila, glotcta (GLOT 1-2), patas, patasdesf
  (PATAS 1-2), glotupatas (GLOT 3 + PATAS 1).
SEMILLAS: serie 37001-37020 · replica 37021-37040 · practica 37901-37909 (exploratorio 37901-37905, humo 37906-37907, arnes 37908-37909).
nube-9: trabajo() atrapa TODA excepcion (SystemExit incluida) y devuelve un resultado marcado 'aborto'; ningun trabajador del Pool muere.
Cualquier aborto -> la serie es NO SE LEE. Cada corrida escribe su JSON ANTES de volver (ERR-54); --reanuda salta las que ya estan.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN; SOLO el coordinador lanza --serie):
  python experimentos/organelos/muro/corre_muro.py --humo                                   # 1 proceso, 6 corridas, T 20 000
  python experimentos/organelos/muro/corre_muro.py --serie --desde 37001 --n 20 --pool 6    # serie   (80 corridas)
  python experimentos/organelos/muro/corre_muro.py --serie --desde 37021 --n 20 --pool 6    # replica (80 corridas)
  python experimentos/organelos/muro/corre_muro.py --serie --desde 37001 --n 20 --pool 6 --reanuda
  python experimentos/organelos/muro/corre_muro.py --bloque <resumen serie>.json,<resumen replica>.json
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
import construye_muro as CB
import revisa_carro as RC
P = CV.P; J = CV.J

CARROS = os.path.join(AQUI, 'carros')
DATOS = os.path.join(AQUI, 'datos')
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028'}
BRAZOS = {'v143': 'V143', 'cta': 'V143_CTA', 'desf': 'V143_DESF', 'o1': 'O1', 'limpia': 'V143_LIMPIA', 'sinest': 'V143_SINEST',
          'glot': 'V143_GLOT', 'glotcta': 'V143_GLOTCTA', 'glotfila': 'V143_GLOTFILA', 'patas': 'V143_PATAS', 'patasdesf': 'V143_PATASDESF',
          'glotu': 'V143_GLOTU', 'glotuinv': 'V143_GLOTUINV', 'glotupatas': 'V143_GLOTUPATAS', 'mtel': 'V143_MTEL'}
PROPIOS = ('V143_CTA', 'V143_LIMPIA', 'V143_SINEST', 'V143_DESF', 'V143_GLOT', 'V143_GLOTCTA', 'V143_GLOTFILA', 'V143_PATAS',
           'V143_PATASDESF', 'V143_GLOTU', 'V143_GLOTUINV', 'V143_GLOTUPATAS', 'V143_MTEL')
CAND = 'glotu'; CTRL = 'glotuinv'
SERIE_BRAZOS = ('v143', 'glotu', 'glotuinv', 'o1')
SERIE = range(37001, 37021); REPLICA = range(37021, 37041); PRACTICA = range(37901, 37910)
HUMO = [(37906, 'mtel'), (37906, 'glotu'), (37906, 'glotuinv'), (37906, 'o1'), (37907, 'mtel'), (37907, 'glotu')]   # mtel == v143 en la fisica
T_DEF = 100000; T_HUMO = 20000
GANA = 15                       # >= 15/20 semillas (la de la carrera: ENMIENDAS 2, 5, 6 y corre_v143.GANA)
DIF_MOD = 0.10                  # diferencia mediana pareada minima para HAY ALGO MODESTO (la de corre_v143.DIF_MOD)
ANCLA_V143 = (0.40, 0.80)       # V143, mediana del R0 real: 0.536 (14301), 0.63 (14321), 0.602 (36001)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def registra():
    for n in PROPIOS:
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", os.path.join(CARROS, n + '.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    for k in BRAZOS:
        if k not in ('v143', 'o1'): CV.BRAZOS.setdefault(k, BRAZOS[k])


def tarea(args):
    """(seed, carro, T) -> corre_v143.tarea tal cual + 'tel_muro' (telemetria de solo lectura de los carros del muro)."""
    registra()
    cap = []; orig = P.run

    def run2(*a, **k):
        r = orig(*a, **k); cap.append([(d.get('carro') or {}).get('muro') for d in r['linajes']]); return r
    P.run = run2
    try:
        x = CV.tarea(args)
    finally:
        P.run = orig
    x['tel_muro'] = cap[0] if cap else None
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


def tm_suma(R):
    """Suma de la telemetria del muro (ULTIMA instancia de cada linaje; con fundador limpio es solo la ultima)."""
    tot = {}
    for c in R:
        for t in (c.get('tel_muro') or []):
            if not t: continue
            for k, v in t.items():
                if isinstance(v, (int, float)) and k not in ('paga', 'glot', 'patas', 'telem'): tot[k] = tot.get(k, 0) + v
    return tot


def cuerpos(R):
    """DESCRIPTIVO: hijos de la cola contra fundadores (vida, hijos por cuerpo, causas), de la fisica (telem del juez)."""
    H = dict(n=0, vidas=[], hijos=0, sin_hijos=0, causas={}); F = dict(n=0, vidas=[], hijos=0, sin_hijos=0, causas={})
    for c in R:
        for l in c['linajes']:
            t = l['telem']; m = min(len(t['vidas']), len(t['desc_por_vida']), len(t['causa_cuerpo']), len(t['origen']))
            for i in range(m):
                D = H if t['origen'][i] == 1 else F
                D['n'] += 1; D['vidas'].append(t['vidas'][i]); D['hijos'] += t['desc_por_vida'][i]; D['sin_hijos'] += int(t['desc_por_vida'][i] == 0)
                D['causas'][t['causa_cuerpo'][i]] = D['causas'].get(t['causa_cuerpo'][i], 0) + 1
    out = {}
    for k, D in (('hijos_de_cola', H), ('fundadores', F)):
        out[k] = dict(n=D['n'], vida_med=(CV.med(D['vidas']) if D['vidas'] else None),
                      hijos_por_cuerpo=(round(D['hijos'] / D['n'], 3) if D['n'] else None),
                      frac_sin_hijos=(round(D['sin_hijos'] / D['n'], 3) if D['n'] else None), causas=D['causas'])
    return out


def establece(R):
    """DESCRIPTIVO: ESTABLECIMIENTO = linajes con 0 fundadores tras t 10 000; R0 real (mediana) de establecidos y no establecidos."""
    L = [l for c in R for l in c['linajes']]
    e = [l for l in L if l['fund_post10k'] == 0]; ne = [l for l in L if l['fund_post10k'] > 0]
    return dict(linajes=len(L), establecidos=len(e), frac_establecidos=(round(len(e) / len(L), 4) if L else None),
                R0_real_establecidos=CV.med([l['R0_real'] for l in e]), R0_real_no_establecidos=CV.med([l['R0_real'] for l in ne]),
                cruzan_de_establecidos=sum(l['cruza_real'] for l in e))


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_muro.md sec. 6)
def pieza(t):
    """V4: la pieza del brazo ACTUO (telemetria de la ultima instancia): decidio objetivos (PATAS) o vetos (GLOT / CTA)."""
    return (t.get('patas_meta', 0) + t.get('veto_glot', 0) + t.get('veto_act', 0) + t.get('veto_otra', 0)) > 0


def lee_serie(res, par, tm, completa, abortos):
    v = {}
    v['V1_completa'] = bool(completa and abortos == 0 and all(b in res for b in SERIE_BRAZOS)
                            and all(res[b]['coherente'].split('/')[0] == res[b]['coherente'].split('/')[1] for b in SERIE_BRAZOS if b in res))
    v['V2_ancla_O1_gana'] = bool(res.get('o1', {}).get('gana_e5'))
    m = res.get('v143', {}).get('R0_real_med')
    v['V3_ancla_V143'] = m is not None and ANCLA_V143[0] <= m <= ANCLA_V143[1]
    tc = tm.get(CAND, {}); tk = tm.get(CTRL, {})
    v['V4_pieza_actua'] = bool(pieza(tc) and pieza(tk))
    valido = all(v.values())
    p = {}
    p['P1_cand_cruza'] = bool(res.get(CAND, {}).get('gana_e5'))
    x = par.get((CAND, 'v143')) or {}
    p['P2_cand_gana_v143'] = bool(x.get('semillas') and x['gana'] >= GANA * x['semillas'] / 20)
    p['P3_ctrl_no_cruza'] = not bool(res.get(CTRL, {}).get('gana_e5'))
    y = par.get((CAND, CTRL)) or {}
    mod = bool(p['P2_cand_gana_v143'] and x.get('dif_med') is not None and x['dif_med'] >= DIF_MOD - 1e-12
               and y.get('semillas') and y['gana'] * 2 > y['semillas'])
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif mod: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    return dict(validez=v, puertas=p, modesto=mod, veredicto=ver)


ORDEN = {'NO SE LEE': -1, 'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}


def bloque(v_serie, v_replica):
    if v_serie == v_replica: return v_serie
    return min((v_serie, v_replica), key=lambda z: ORDEN[z])


def valida(humo, desde, n, T, brazos):
    for b in brazos:
        if b not in BRAZOS: return f"brazo desconocido {b!r} (validos {list(BRAZOS)})"
    if n < 1: return "--n >= 1"
    sem = list(range(desde, desde + n))
    if humo:
        if not all(x in PRACTICA for x in sem): return "--humo: solo semillas de practica 37901-37909"
        if T > 30000: return "--humo: T <= 30000"
    else:
        if not (all(x in SERIE for x in sem) or all(x in REPLICA for x in sem)): return "serie: solo 37001-37020 (serie) o 37021-37040 (replica)"
        if T != T_DEF: return "serie: T = 100000 (preregistrado)"
        if tuple(brazos) != SERIE_BRAZOS: return f"serie: brazos {SERIE_BRAZOS} (preregistrado)"
    return None


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for n, b in CB.todas().items():
        ruta = os.path.join(CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = RC.revisa_fuente(b.decode('utf-8'), n) if igual else ['distinto de construye_muro']
        ok &= igual and not vr
        log(f"  carro {n} sha {CB.h16b(b)} == construye: {igual} · revisa_carro: {'PASA' if not vr else vr[:2]}")
    registra()
    N = lambda x: json.loads(json.dumps(x, default=str))
    m = CV._MODS['V143_CTA']; g = (m.PAGA, m.GLOT, m.PATAS, m.TELEM)
    try:
        m.PAGA = 0; m.GLOT = 0; m.PATAS = 0; m.TELEM = 0
        a = P.run(37908, [('C', CV.modulo('V143'))] * 9, T=2000, fundador_limpio=1)
        b = P.run(37908, [('C', m)] * 9, T=2000, fundador_limpio=1)
    finally:
        m.PAGA, m.GLOT, m.PATAS, m.TELEM = g
    i1 = N(a) == N(b); ok &= i1
    log(f"  IDENTIDAD CORTA: V143_CTA con PAGA = GLOT = TELEM = 0 == V143 (salida ENTERA, N 9, s 37908, T 2000, fundador limpio): {'OK' if i1 else 'FALLA'}")
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
        if not (s0 in SERIE and s1 in REPLICA): raise SystemExit("--bloque: primero la serie 37001-37020 y luego la replica 37021-37040")
        vb = bloque(rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto'])
        print(f"serie {rs[0]['letra']['veredicto']} · replica {rs[1]['letra']['veredicto']} -> BLOQUE: {vb}")
        return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        T = a.T or T_HUMO
        if a.brazos or a.desde or a.n:
            brazos = [s for s in (a.brazos or 'mtel,glotu,glotuinv,o1').split(',') if s]; desde = a.desde or 37906; n = a.n or 1
            e = valida(True, desde, n, T, brazos)
            if e: raise SystemExit(e)
            tareas = [(s, b) for s in range(desde, desde + n) for b in brazos]
        else:
            tareas = list(HUMO)
            e = valida(True, 37906, 2, T, list(BRAZOS))
            if e: raise SystemExit(e)
        if len(tareas) > 6: raise SystemExit("--humo: maximo 6 corridas por proceso")
        semillas = sorted({s for s, _ in tareas}); brazos = [b for b in BRAZOS if any(b == x for _, x in tareas)]
        pool = 0; dest = os.path.join(DATOS, 'humo')
    else:
        T = a.T or T_DEF; desde = a.desde or 37001; n = a.n or 20; brazos = [s for s in (a.brazos or ','.join(SERIE_BRAZOS)).split(',') if s]
        e = valida(False, desde, n, T, brazos)
        if e: raise SystemExit(e)
        semillas = list(range(desde, desde + n)); tareas = [(s, b) for b in brazos for s in semillas]; pool = a.pool
        dest = DATOS
    sel = time.strftime('%Y%m%d_%H%M%S')
    pre = f"muro_{'humo_' if a.humo else ''}s{semillas[0]}-{semillas[-1]}_T{T}"
    carpeta = os.path.join(dest, pre if not a.humo else pre + '_' + sel)
    if a.reanuda and not a.humo:
        prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
        carpeta = os.path.join(dest, prev[-1]) if prev else carpeta + '_' + sel
    elif not a.humo:
        carpeta = carpeta + '_' + sel
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    log(f"CORRE_MURO · {pre} · {sel} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'} · "
        f"corre_muro.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  tareas {len(tareas)} · brazos {brazos} · semillas {semillas[0]}-{semillas[-1]} · T {T} · fundador limpio 1 · reanuda {a.reanuda}")
    ok = verifica(log)
    if a.humo:
        ok &= CV.verifica_todo(log, con_entrada=True)   # regla 14: corre_v143.tarea == juez.tarea (9 FABRICA, s 14281, T 2000)
        N = lambda x: json.loads(json.dumps(x, default=str))
        x = tarea((37908, 'V143', 2000)); y = CV.tarea((37908, 'V143', 2000))
        e14 = x.pop('tel_muro') == [None] * 9 and N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in y.items() if k != 'seg'})
        ok &= e14; log(f"  ENTRADA campo a campo (regla 14): tarea de este runner == corre_v143.tarea (V143, s 37908, T 2000): {'OK' if e14 else 'FALLA'}")
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
    if a.humo and 'mtel' in por and not por.get('v143'):   # HUMO: V143_MTEL es V143 en la fisica (arnes); hace de base
        por['v143'] = por['mtel']
    res = {}; tm = {}; cz = {}
    for b in [x for x in por if por[x]]:
        res[b] = CV.resume(por[b], b, log); tm[b] = tm_suma(por[b]); cz[b] = cuerpos(por[b]); cz[b]['establece'] = establece(por[b])
        log(f"  ESTABLECIMIENTO ({b}, descriptivo): {cz[b]['establece']}")
        log(f"  CUERPOS ({b}, descriptivo): {cz[b]['hijos_de_cola']} · fundadores {cz[b]['fundadores']}")
        if tm[b]: log(f"  muro ({b}): telemetria de la ultima instancia {tm[b]}")
    PAR = ((CAND, 'v143'), (CAND, CTRL), (CTRL, 'v143'), ('o1', 'v143'), ('o1', CAND))
    par = {k: CV.pareado(por[k[0]], por[k[1]]) for k in PAR if por.get(k[0]) and por.get(k[1])}
    log("\nPAREADOS (por semilla: mediana del R0 real de los 9 linajes; gana = semillas en que el primero supera al segundo)")
    for k, v in par.items(): log(f"  {k[0]} vs {k[1]}: gana {v['gana']}/{v['semillas']} · diferencia mediana {v['dif_med']}")
    completa = True if a.humo else all(len(por.get(b, [])) == len(semillas) for b in SERIE_BRAZOS)
    letra = lee_serie(res, par, tm, completa, abortos)
    log("\n================ LA LETRA (PREREGISTRO_muro.md sec. 6)" + (" -- HUMO: T corto y semillas de practica, NO cuenta" if a.humo else ""))
    log(f"  validez {letra['validez']}")
    log(f"  puertas {letra['puertas']} · modesto {letra['modesto']}")
    ver = ('HUMO (no cuenta): ' if a.humo else '') + letra['veredicto']
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(brazos=res, pareados={f"{k[0]}_vs_{k[1]}": x for k, x in par.items()}, telemetria=tm, cuerpos=cz, letra=letra,
                       semillas=semillas, T=T, humo=a.humo, abortos=abortos, veredicto=ver,
                       sha_runner=h16(os.path.abspath(__file__)), sha_carros={n: h16(os.path.join(CARROS, n + '.py')) for n in PROPIOS}),
                  fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)})\nTerminado en {time.time()-t0:.1f}s")
    log(f"VEREDICTO DE LA SERIE: {ver}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
