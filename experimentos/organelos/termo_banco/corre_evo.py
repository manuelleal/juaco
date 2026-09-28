"""corre_evo.py — RUNNER y LETRA del bloque TERMO_EVO (nube, 28-sep-2026). Preregistro: PREREGISTRO_termo_evo.md (la letra esta AQUI,
en lee_serie(), y alli en la sec. 6). Encargo: ENCARGO_NUBE.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros.

Pregunta: si el margen del termostato de boca es un GEN g por cuerpo, heredable con mutacion, la seleccion lo lleva sola desde la zona
letal (g ~ U[-0.10, 0.10]) a la banda que funciona y el linaje cruza el R0 real de 0.90? (construye_evo.py: la pieza y el gen)

ENTRADA (regla 14): la corrida ES experimentos/tronco_v14_3/corre_v143.tarea (se IMPORTA, no se toca; sha fijado) = juez.tarea(seed,
9 carros iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje (solo fisica, ERR-96).
Los carros nuevos se registran en su cache de modulos (corre_v143._MODS) y en su tabla BRAZOS, en memoria. Lo unico agregado:
'tel_evo' = telemetria de SOLO LECTURA del gen: el dict de modulo _TEL de los carros EVO (se BORRA antes de cada pista.run y se copia
despues; tiene las instancias de todas las refundaciones) y d['carro']['evo'] de la ultima instancia de cada linaje. No puntua.

BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, fundador limpio = ENMIENDA 5). SERIE = los 6:
  v143      V143              base: el bicho real (tronco_v14_3)
  evo       V143_EVO_BAJO     CANDIDATO: g heredable, sigma 0.03, fundador g ~ U[-0.10, 0.10] (zona letal)
  sinher    V143_EVO_SINHER   CONTROL: misma fisica y misma distribucion, el hijo sortea g de nuevo (sin herencia)
  ancho     V143_EVO_ANCHO    secundario (descriptivo): g heredable, fundador g ~ U[-0.10, 0.60]
  m40       V143_EVO_M40      techo DISENADO: g = 0.40 fijo (== HIBB m40 en la fisica; arnes)
  o1        O1                techo escrito por un LLM; ANCLA de la pista
SEMILLAS: serie 41001-41020 · replica 41021-41040 · humo/arnes 41911-41914 (sin choques en el repo: grep del 28-sep).
SHAS de TODO lo que corre, fijados ANTES del humo (SHAS abajo): si uno cambia, verifica() falla y no se corre nada.
nube-9: trabajo() atrapa TODA excepcion y devuelve un resultado marcado 'aborto'. Cualquier aborto -> NO SE LEE. Cada corrida escribe su
JSON ANTES de volver (ERR-54); --reanuda salta las que ya estan.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN):
  python experimentos/organelos/termo_evo/corre_evo.py --humo                                   # 1 proceso, 6 corridas, T 20 000
  python experimentos/organelos/termo_evo/corre_evo.py --serie --desde 41001 --n 20 --pool 3    # serie   (120 corridas)
  python experimentos/organelos/termo_evo/corre_evo.py --serie --desde 41021 --n 20 --pool 3    # replica (solo si la serie no da NO)
  python experimentos/organelos/termo_evo/corre_evo.py --serie --desde 41001 --n 20 --pool 3 --reanuda
  python experimentos/organelos/termo_evo/corre_evo.py --serie --desde 41041 --n 10 --pool 3    # larga DESCRIPTIVA (T 300 000, evo y sinher)
  python experimentos/organelos/termo_evo/corre_evo.py --bloque <resumen serie>.json,<resumen replica>.json
"""
import argparse, copy, hashlib, importlib.util, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV          # tarea, resume, pareado (se IMPORTA, no se toca)
import construye_evo as CB
import revisa_carro as RC
P = CV.P; J = CV.J

PRERREGISTRO = 'PREREGISTRO_termo_evo.md'
CARROS = os.path.join(AQUI, 'carros')
DATOS = os.path.join(AQUI, 'datos')
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028', os.path.join(PISTA, 'revisa_carro.py'): '1c8a789f7427ab96',
        os.path.join(AQUI, 'construye_evo.py'): '6cdd7dd10e9a0594',
        os.path.join(CARROS, 'V143_EVO_BAJO.py'): '3187b373654e119f', os.path.join(CARROS, 'V143_EVO_ANCHO.py'): '1ff17bf4c6e32382',
        os.path.join(CARROS, 'V143_EVO_SINHER.py'): 'a11989a3b04d13d6', os.path.join(CARROS, 'V143_EVO_M40.py'): '713cd55ed465cc82'}
BRAZOS = {'v143': 'V143', 'evo': 'V143_EVO_BAJO', 'sinher': 'V143_EVO_SINHER', 'ancho': 'V143_EVO_ANCHO', 'm40': 'V143_EVO_M40', 'o1': 'O1'}
PROPIOS = ('V143_EVO_BAJO', 'V143_EVO_ANCHO', 'V143_EVO_SINHER', 'V143_EVO_M40')
CAND = 'evo'; CTRL = 'sinher'
SERIE_BRAZOS = ('v143', 'evo', 'sinher', 'ancho', 'm40', 'o1')
SERIE = range(41001, 41021); REPLICA = range(41021, 41041); PRACTICA = range(41911, 41915)
LARGA = range(41041, 41051); T_LARGA = 300000; LARGA_BRAZOS = ('evo', 'sinher')   # DESCRIPTIVA (sin letra): mas generaciones
HUMO = [(41911, 'evo'), (41911, 'sinher'), (41911, 'm40'), (41911, 'v143'), (41912, 'evo'), (41912, 'ancho')]
T_DEF = 100000; T_HUMO = 20000
GANA = 15                       # >= 15/20 semillas (la de la carrera: ENMIENDAS 2, 5, 6 y corre_v143.GANA)
DIF_MOD = 0.10                  # diferencia mediana pareada minima para HAY ALGO MODESTO (la de corre_v143.DIF_MOD)
ANCLA_V143 = (0.40, 0.80)       # V143, mediana del R0 real (la del muro y la de TERMO)
BANDA_G = (0.10, 0.60)          # P3: la media de g de los padres en la ULTIMA ventana cae aqui (ENCARGO_NUBE sec. 3)
VENTANAS = 10                   # curva de g: T/10 pasos por ventana; la ultima ventana es [0.9 T, T)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def registra():
    for n in PROPIOS:
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", os.path.join(CARROS, n + '.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    for k in BRAZOS:
        if k not in ('v143', 'o1'): CV.BRAZOS.setdefault(k, BRAZOS[k])


def tarea(args):
    """(seed, carro, T) -> corre_v143.tarea tal cual + 'tel_evo' (telemetria de solo lectura del gen)."""
    registra()
    seed, ident, T = args
    m = CV._MODS.get(ident) if ident in PROPIOS else None
    cap = []; orig = P.run

    def run2(*a, **k):
        if m is not None: m._TEL.clear()
        r = orig(*a, **k)
        cap.append(dict(ult=[(d.get('carro') or {}).get('evo') for d in r['linajes']],
                        tel=(copy.deepcopy({str(i): v for i, v in m._TEL.items()}) if m is not None else None)))
        return r
    P.run = run2
    try:
        x = CV.tarea(args)
    finally:
        P.run = orig
    x['tel_evo'] = cap[0] if cap else None
    return x


def trabajo(args):
    """UNA corrida; atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54); con reanuda salta la que ya existe."""
    seed, brazo, T, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: return json.load(fh)
    try:
        x = tarea((seed, BRAZOS[brazo], T)); x.pop('pizarra_log', None); x['brazo'] = brazo; x['aborto'] = None
    except BaseException as e:   # noqa: nube-9
        x = dict(seed=seed, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


def tm_suma(R):
    """Contadores de la pieza (ultima instancia de cada linaje): dec, a_no, a_si, mord."""
    tot = {}
    for c in R:
        for t in ((c.get('tel_evo') or {}).get('ult') or []):
            if not t: continue
            for k in ('dec', 'a_no', 'a_si', 'mord'): tot[k] = tot.get(k, 0) + t.get(k, 0)
    return tot


def pieza(t):
    """V4: la pieza del brazo ACTUO (ultima instancia): cambio al menos una decision de la boca de v14.3."""
    return (t.get('a_no', 0) + t.get('a_si', 0)) > 0


# ------------------------------------------------------------------ la curva de g (P3 y descriptivos)
def _q(xs, p):
    xs = sorted(xs); return round(xs[min(len(xs) - 1, int(p * len(xs)))], 4) if xs else None


def _m(xs): return round(sum(xs) / len(xs), 4) if xs else None


def g_semilla(c, T):
    """Por corrida: media de g de los PADRES (partos) por ventana, pooled sobre los 9 linajes. La ultima ventana es la de P3."""
    tel = (c.get('tel_evo') or {}).get('tel') or {}
    W = T // VENTANAS; out = []
    for w in range(VENTANAS):
        gp = [g for lt in tel.values() for t, g in lt['partos'] if w * W <= t < (w + 1) * W]
        out.append(dict(n=len(gp), media=_m(gp)))
    return out


def g_curva(R, T):
    """Por ventana, pooled sobre semillas y linajes: g de los PADRES al parir, g de los VIVOS (muestra cada 1000 pasos) y g de los
    cuerpos que MUEREN (con sus hijos). Media y cuantiles 10/50/90."""
    W = T // VENTANAS; out = []
    for w in range(VENTANAS):
        gp = []; gv = []; gm = []; hm = []
        for c in R:
            for lt in (((c.get('tel_evo') or {}).get('tel')) or {}).values():
                gp += [g for t, g in lt['partos'] if w * W <= t < (w + 1) * W]
                gv += [g for t, g in lt['vivos'] if w * W <= t < (w + 1) * W]
                for t, g, e, h, o in lt['muertes']:
                    if w * W <= t < (w + 1) * W: gm.append(g); hm.append(h)
        out.append(dict(t0=w * W, t1=(w + 1) * W, padres=dict(n=len(gp), media=_m(gp), q10=_q(gp, .1), q50=_q(gp, .5), q90=_q(gp, .9)),
                        vivos=dict(n=len(gv), media=_m(gv), q10=_q(gv, .1), q50=_q(gv, .5), q90=_q(gv, .9)),
                        muertos=dict(n=len(gm), media=_m(gm), hijos_por_cuerpo=_m(hm))))
    return out


def g_paisaje(R):
    """Por bin de g (ancho 0.05 desde -0.2): cuerpos muertos, hijos por cuerpo y edad media (todas las corridas del brazo)."""
    acc = {}
    for c in R:
        for lt in (((c.get('tel_evo') or {}).get('tel')) or {}).values():
            for b, (n, h, e) in lt['gbin'].items():
                x = acc.setdefault(int(b), [0, 0, 0]); x[0] += n; x[1] += h; x[2] += e
    return [dict(g_desde=round(-0.2 + 0.05 * b, 2), cuerpos=n, hijos_por_cuerpo=round(h / n, 3), edad_media=round(e / n, 1))
            for b, (n, h, e) in sorted(acc.items()) if n]


def p3_semillas(R, T):
    """P3 por semilla: media de g de los padres en la ULTIMA ventana dentro de BANDA_G (sin partos en esa ventana = no cumple)."""
    out = {}
    for c in R:
        u = g_semilla(c, T)[-1]
        out[c['seed']] = dict(n=u['n'], media=u['media'], cumple=bool(u['media'] is not None and BANDA_G[0] <= u['media'] <= BANDA_G[1]))
    return out


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_termo_evo.md sec. 6)
def lee_serie(res, par, tm, p3, completa, abortos, ns=20):
    v = {}
    v['V1_completa'] = bool(completa and abortos == 0 and all(b in res for b in SERIE_BRAZOS)
                            and all(res[b]['coherente'].split('/')[0] == res[b]['coherente'].split('/')[1] for b in SERIE_BRAZOS if b in res))
    v['V2_ancla_O1_gana'] = bool(res.get('o1', {}).get('gana_e5'))
    m = res.get('v143', {}).get('R0_real_med')
    v['V3_ancla_V143'] = m is not None and ANCLA_V143[0] <= m <= ANCLA_V143[1]
    v['V4_pieza_actua'] = bool(pieza(tm.get(CAND, {})) and pieza(tm.get(CTRL, {})))
    valido = all(v.values())
    p = {}
    p['P1_evo_cruza'] = bool(res.get(CAND, {}).get('gana_e5'))
    y = par.get((CAND, CTRL)) or {}
    p['P2_evo_gana_sinher'] = bool(y.get('semillas') and y['gana'] >= GANA * y['semillas'] / 20)
    sp = sum(1 for z in p3.values() if z['cumple'])
    p['P3_g_en_banda'] = bool(p3 and sp >= GANA * len(p3) / 20)
    mod = bool(p['P3_g_en_banda'] and y.get('semillas') and y['gana'] * 2 > y['semillas']
               and y.get('dif_med') is not None and y['dif_med'] >= DIF_MOD - 1e-12)
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif mod: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    return dict(validez=v, puertas=p, p3_semillas_en_banda=sp, modesto=mod, veredicto=ver)


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
        if not all(x in PRACTICA for x in sem): return "--humo: solo semillas de practica 41911-41914"
        if T > 30000: return "--humo: T <= 30000"
    else:
        if all(x in LARGA for x in sem):
            if T != T_LARGA: return "larga: T = 300000 (preregistrado)"
            if tuple(brazos) != LARGA_BRAZOS: return f"larga: brazos {LARGA_BRAZOS} (preregistrado)"
            return None
        if not (all(x in SERIE for x in sem) or all(x in REPLICA for x in sem)): return "serie: solo 41001-41020 (serie) o 41021-41040 (replica); larga 41041-41050"
        if T != T_DEF: return "serie: T = 100000 (preregistrado)"
        if tuple(brazos) != SERIE_BRAZOS: return f"serie: brazos {SERIE_BRAZOS} (preregistrado)"
    return None


def verifica(log):
    """shas FIJADOS de todo lo que corre + carros == construye_evo + revisa_carro + identidad corta (EVO = 0 == V143)."""
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for n, b in CB.todas().items():
        ruta = os.path.join(CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = RC.revisa_fuente(b.decode('utf-8'), n) if igual else ['distinto de construye_evo']
        ok &= igual and not vr
        log(f"  carro {n} sha {CB.h16b(b)} == construye: {igual} · revisa_carro: {'PASA' if not vr else vr[:2]}")
    registra()
    N = lambda x: json.loads(json.dumps(x, default=str))
    base = N(P.run(41913, [('C', CV.modulo('V143'))] * 9, T=2000, fundador_limpio=1))
    for n in PROPIOS:
        m = CV._MODS[n]; g = m.EVO
        try:
            m.EVO = 0; xx = N(P.run(41913, [('C', m)] * 9, T=2000, fundador_limpio=1))
        finally:
            m.EVO = g
        i = xx == base; ok &= i
        log(f"  IDENTIDAD CORTA: {n} con EVO = 0 == V143 (salida ENTERA, N 9, s 41913, T 2000, fundador limpio): {'OK' if i else 'FALLA'}")
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
        if not (s0 in SERIE and s1 in REPLICA): raise SystemExit("--bloque: primero la serie 41001-41020 y luego la replica 41021-41040")
        vb = bloque(rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto'])
        print(f"serie {rs[0]['letra']['veredicto']} · replica {rs[1]['letra']['veredicto']} -> BLOQUE: {vb}  ({PRERREGISTRO} sec. 6-7)")
        return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        T = a.T or T_HUMO
        if a.brazos or a.desde or a.n:
            brazos = [s for s in (a.brazos or 'evo,sinher').split(',') if s]; desde = a.desde or 41911; n = a.n or 1
            e = valida(True, desde, n, T, brazos)
            if e: raise SystemExit(e)
            tareas = [(s, b) for s in range(desde, desde + n) for b in brazos]
        else:
            tareas = list(HUMO)
            e = valida(True, 41911, 2, T, list(BRAZOS))
            if e: raise SystemExit(e)
        if len(tareas) > 6: raise SystemExit("--humo: maximo 6 corridas por proceso")
        semillas = sorted({s for s, _ in tareas}); brazos = [b for b in BRAZOS if any(b == x for _, x in tareas)]
        pool = 0; dest = os.path.join(DATOS, 'humo')
    else:
        desde = a.desde or 41001; n = a.n or 20; lg = desde in LARGA
        T = a.T or (T_LARGA if lg else T_DEF); brazos = [s for s in (a.brazos or ','.join(LARGA_BRAZOS if lg else SERIE_BRAZOS)).split(',') if s]
        e = valida(False, desde, n, T, brazos)
        if e: raise SystemExit(e)
        semillas = list(range(desde, desde + n)); tareas = [(s, b) for s in semillas for b in brazos]; pool = a.pool
        dest = DATOS
    sel = time.strftime('%Y%m%d_%H%M%S')
    pre = f"evo_{'humo_' if a.humo else ''}s{semillas[0]}-{semillas[-1]}_T{T}"
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
    log(f"CORRE_EVO · {pre} · {sel} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'} · "
        f"corre_evo.py {h16(os.path.abspath(__file__))} · preregistro {PRERREGISTRO} · carpeta {carpeta}")
    log(f"  tareas {len(tareas)} · brazos {brazos} · semillas {semillas[0]}-{semillas[-1]} · T {T} · fundador limpio 1 · reanuda {a.reanuda}")
    ok = verifica(log)
    if a.humo:
        N = lambda x: json.loads(json.dumps(x, default=str))
        x = tarea((41913, 'V143', 2000)); y = CV.tarea((41913, 'V143', 2000))
        e14 = x.pop('tel_evo') == dict(ult=[None] * 9, tel=None) and N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in y.items() if k != 'seg'})
        ok &= e14; log(f"  ENTRADA campo a campo (regla 14): tarea de este runner == corre_v143.tarea (V143, s 41913, T 2000): {'OK' if e14 else 'FALLA'}")
    if not ok: log("  ALGO FALLA -> no se corre."); return 1
    args = [(s, b, T, carpeta, a.reanuda) for s, b in tareas]
    R = []
    lin = lambda x: (f"R0 real por linaje {[l['R0_real'] for l in x['linajes']]} · fundadores {[l['fundadores'] for l in x['linajes']]}"
                     + (f" · g padres ultima ventana {g_semilla(x, T)[-1]}" if (x.get('tel_evo') or {}).get('tel') else ''))
    if pool and pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as PL:
            for x in PL.imap_unordered(trabajo, args):
                R.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} s{x['seed']} ({x.get('seg')}s) R0 pista {x.get('R0_pista')} aborto {x['aborto']}"
                                 + ('' if x['aborto'] else ' · ' + lin(x)))
    else:
        for ar in args:
            x = trabajo(ar); R.append(x)
            log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} s{x['seed']} ({x.get('seg')}s) R0 pista {x.get('R0_pista')} aborto {x['aborto']}"
                + ('' if x['aborto'] else ' · ' + lin(x)))
    abortos = sum(1 for x in R if x['aborto'])
    por = {b: sorted([x for x in R if x['brazo'] == b and not x['aborto']], key=lambda z: z['seed']) for b in brazos}
    res = {}; tm = {}; gc = {}; gp = {}
    for b in [x for x in por if por[x]]:
        res[b] = CV.resume(por[b], b, log); tm[b] = tm_suma(por[b])
        if tm[b]: log(f"  pieza ({b}): contadores de la ultima instancia {tm[b]}")
        if BRAZOS[b] in PROPIOS:
            gc[b] = g_curva(por[b], T); gp[b] = g_paisaje(por[b])
            log(f"  CURVA DE g ({b}; por ventana de {T // VENTANAS} pasos: padres media [q10 q50 q90] n · vivos media · muertos hijos/cuerpo)")
            for w in gc[b]:
                pa = w['padres']; vi = w['vivos']; mu = w['muertos']
                log(f"    [{w['t0']:6d},{w['t1']:6d}) padres {pa['media']} [{pa['q10']} {pa['q50']} {pa['q90']}] n {pa['n']} · vivos {vi['media']} "
                    f"[{vi['q10']} {vi['q50']} {vi['q90']}] · muertos n {mu['n']} hijos/cuerpo {mu['hijos_por_cuerpo']}")
            log(f"  PAISAJE ({b}; bin de g: cuerpos, hijos por cuerpo, edad media): "
                + ' · '.join(f"{z['g_desde']:+.2f}: {z['cuerpos']}/{z['hijos_por_cuerpo']}/{z['edad_media']:.0f}" for z in gp[b]))
    p3 = p3_semillas(por.get(CAND, []), T)
    log(f"\n  P3 por semilla ({CAND}: media de g de los padres en [{T - T // VENTANAS}, {T}); banda {BANDA_G}): "
        + ' · '.join(f"{s}: {z['media']} (n {z['n']}){'*' if z['cumple'] else ''}" for s, z in sorted(p3.items())))
    PAR = ((CAND, CTRL), (CAND, 'v143'), (CTRL, 'v143'), ('ancho', CTRL), ('ancho', 'v143'), ('m40', 'v143'), (CAND, 'm40'), ('o1', 'v143'))
    par = {k: CV.pareado(por[k[0]], por[k[1]]) for k in PAR if por.get(k[0]) and por.get(k[1])}
    log("\nPAREADOS (por semilla: mediana del R0 real de los 9 linajes; gana = semillas en que el primero supera al segundo)")
    for k, v in par.items(): log(f"  {k[0]} vs {k[1]}: gana {v['gana']}/{v['semillas']} · diferencia mediana {v['dif_med']}")
    larga = semillas[0] in LARGA
    completa = True if (a.humo or larga) else all(len(por.get(b, [])) == len(semillas) for b in SERIE_BRAZOS)
    letra = lee_serie(res, par, tm, p3, completa, abortos)
    if larga: letra['veredicto'] = 'DESCRIPTIVA (sin letra: T 300 000, solo evo y sinher)'
    log(f"\n================ LA LETRA ({PRERREGISTRO} sec. 6)" + (" -- HUMO: T corto y semillas de practica, NO cuenta" if a.humo else ""))
    log(f"  validez {letra['validez']}")
    log(f"  puertas {letra['puertas']} (P3: {letra['p3_semillas_en_banda']}/{len(p3)} semillas) · modesto {letra['modesto']}")
    ver = ('HUMO (no cuenta): ' if a.humo else '') + letra['veredicto']
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(brazos=res, pareados={f"{k[0]}_vs_{k[1]}": x for k, x in par.items()}, telemetria=tm, curva_g=gc, paisaje_g=gp,
                       p3=p3, letra=letra, semillas=semillas, T=T, humo=a.humo, abortos=abortos, veredicto=ver, preregistro=PRERREGISTRO,
                       sha_runner=h16(os.path.abspath(__file__)), sha_carros={n: h16(os.path.join(CARROS, n + '.py')) for n in PROPIOS}),
                  fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)})\nTerminado en {time.time()-t0:.1f}s")
    log(f"VEREDICTO DE LA SERIE: {ver}   (regla de parada: {PRERREGISTRO} sec. 7)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
