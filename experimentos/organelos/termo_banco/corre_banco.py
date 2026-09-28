"""corre_banco.py — RUNNER y LETRA del bloque TERMO_BANCO (28-sep-2026). Preregistro: PREREGISTRO_termo_banco.md (la letra esta AQUI, en
lee_serie(), y alli en la sec. 6). Encargo para la nube: ENCARGO_NUBE.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros.

Pregunta: con el margen del termostato como gen g heredable (TERMO_EVO de la nube), si el FUNDADOR nuevo sale del BANCO DE SEMILLAS del
propio linaje (los g de sus cuerpos que parieron, + la mutacion de siempre) en vez de la distribucion inicial, el linaje cruza el R0
real de 0.90 por la letra del muro (construye_banco.py: la pieza)?

ENTRADA (regla 14): la corrida ES la de la nube: corre_evo.tarea (traido por sha, trae_nube.py) = corre_v143.tarea (juez.tarea(seed,
9 carros iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje) + 'tel_evo'. Esta tarea
hace lo mismo y ADEMAS borra el _BANCO del modulo antes de cada pista.run (el carro tambien se reinicia solo: dos cerrojos). El arnes
compara campo a campo esta tarea con corre_evo.tarea (evo) y con corre_v143.tarea (V143).

BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, fundador limpio = ENMIENDA 5). SERIE = los 6:
  v143      V143                base: el bicho real (tronco_v14_3)
  evo       V143_EVO_BAJO       REFERENCIA de la nube (sin banco: el fundador sortea de U[-0.10, 0.10])
  banco     V143_EVO_BANCO      CANDIDATO: el fundador sale del banco del PROPIO linaje (+ N(0, 0.03))
  bancobar  V143_EVO_BANCOBAR   CONTROL: el fundador sale del banco de OTRO linaje (germoplasma, pero no el propio)
  m40       V143_EVO_M40        techo DISENADO de la nube (g = 0.40 fijo)
  o1        O1                  techo escrito por un LLM; ANCLA de la pista
SEMILLAS: serie 42001-42020 · replica 42021-42040 · practica (humo, arnes) 42911-42914 (grep del repo y de las 10 ramas remotas el 28-sep:
sin choques).
SHAS de TODO lo que corre, fijados ANTES del humo (SHAS abajo): si uno cambia, verifica() falla y no se corre nada.
nube-9: trabajo() atrapa TODA excepcion y devuelve un resultado marcado 'aborto'. Cualquier aborto -> NO SE LEE. Cada corrida escribe su
JSON ANTES de volver (ERR-54); --reanuda salta las que ya estan.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN):
  python experimentos/organelos/termo_banco/corre_banco.py --humo                                   # 1 proceso, 6 corridas, T 20 000
  python experimentos/organelos/termo_banco/corre_banco.py --serie --desde 42001 --n 20 --pool 3    # serie   (120 corridas)
  python experimentos/organelos/termo_banco/corre_banco.py --serie --desde 42021 --n 20 --pool 3    # replica (solo si la serie no da NO)
  python experimentos/organelos/termo_banco/corre_banco.py --serie --desde 42001 --n 20 --pool 3 --reanuda
  python experimentos/organelos/termo_banco/corre_banco.py --bloque <resumen serie>.json,<resumen replica>.json
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
import corre_evo as CE           # el runner de la nube (traido por sha): curva de g, paisaje, P3, contadores de la pieza
import construye_banco as CBB
import revisa_carro as RC
CV = CE.CV; P = CV.P; J = CV.J

PRERREGISTRO = 'PREREGISTRO_termo_banco.md'
CARROS = os.path.join(AQUI, 'carros')
DATOS = os.path.join(AQUI, 'datos')
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028', os.path.join(PISTA, 'revisa_carro.py'): '1c8a789f7427ab96',
        os.path.join(AQUI, 'construye_evo.py'): '6cdd7dd10e9a0594', os.path.join(AQUI, 'corre_evo.py'): '7d8e660a1b0e1a71',
        os.path.join(CARROS, 'V143_EVO_BAJO.py'): '3187b373654e119f', os.path.join(CARROS, 'V143_EVO_M40.py'): '713cd55ed465cc82',
        os.path.join(AQUI, 'construye_banco.py'): 'ead46623e70d13f6',
        os.path.join(CARROS, 'V143_EVO_BANCO.py'): '9862ba0b8324cf3c', os.path.join(CARROS, 'V143_EVO_BANCOBAR.py'): '8458fb27a28236e0',
        os.path.join(CARROS, 'V143_EVO_BANCO_M40.py'): '20c411944ec07183'}
BRAZOS = {'v143': 'V143', 'evo': 'V143_EVO_BAJO', 'banco': 'V143_EVO_BANCO', 'bancobar': 'V143_EVO_BANCOBAR', 'm40': 'V143_EVO_M40', 'o1': 'O1'}
PROPIOS = ('V143_EVO_BANCO', 'V143_EVO_BANCOBAR', 'V143_EVO_BANCO_M40')
EVOS = ('V143_EVO_BAJO', 'V143_EVO_M40') + PROPIOS          # carros con gen g (telemetria _TEL)
CAND = 'banco'; CTRL = 'bancobar'; REF = 'evo'
SERIE_BRAZOS = ('v143', 'evo', 'banco', 'bancobar', 'm40', 'o1')
SERIE = range(42001, 42021); REPLICA = range(42021, 42041); PRACTICA = range(42911, 42915)
HUMO = [(42911, 'banco'), (42911, 'bancobar'), (42911, 'evo'), (42912, 'banco'), (42912, 'bancobar'), (42912, 'evo')]
T_DEF = 100000; T_HUMO = 20000
GANA = CV.GANA                  # 15: >= 15/20 semillas (ENMIENDAS 2, 5, 6; la letra del muro)
DIF_MOD = CV.DIF_MOD            # 0.10: diferencia mediana pareada minima para HAY ALGO MODESTO
ANCLA_V143 = CE.ANCLA_V143      # (0.40, 0.80): V143, mediana del R0 real (la del muro, TERMO y TERMO_EVO)
BANDA_G = CE.BANDA_G            # (0.10, 0.60): P3, la de TERMO_EVO (por encima de 0.10 no se llega sin acumular: la inicial acaba ahi)
VENTANAS = CE.VENTANAS          # 10: la ultima ventana es [0.9 T, T)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def registra():
    CE.registra()                                  # los carros de la nube (V143_EVO_BAJO, ..._M40, ...) desde esta carpeta
    for n in PROPIOS:
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", os.path.join(CARROS, n + '.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    for k in BRAZOS:
        if k not in ('v143', 'o1'): CV.BRAZOS.setdefault(k, BRAZOS[k])


def tarea(args):
    """(seed, carro, T) -> corre_v143.tarea tal cual + 'tel_evo' (== corre_evo.tarea) ; borra _TEL y _BANCO antes del run."""
    registra()
    seed, ident, T = args
    m = CV._MODS.get(ident) if ident in EVOS else None
    cap = []; orig = P.run

    def run2(*a, **k):
        if m is not None:
            m._TEL.clear()
            if hasattr(m, '_BANCO'): m._BANCO.clear()
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


# ------------------------------------------------------------------ el banco (telemetria de solo lectura)
def fund_origen(R, T):
    """Fundadores por origen (0 inicial, 1 banco propio, 2 banco ajeno), pooled; g medio de los fundadores por origen; y por semilla
    la fraccion de fundadores que salieron de un banco. Las instancias se cuentan en _TEL[indice]['fund_banco'] (una por fundador)."""
    n = [0, 0, 0]; gs = [[], [], []]; por = {}
    for c in R:
        k = [0, 0, 0]
        for lt in (((c.get('tel_evo') or {}).get('tel')) or {}).values():
            for o, g, nb in lt.get('fund_banco', []):
                n[o] += 1; gs[o].append(g); k[o] += 1
        por[c['seed']] = k
    return dict(fundadores=dict(inicial=n[0], propio=n[1], ajeno=n[2]), g_media=dict(inicial=CE._m(gs[0]), propio=CE._m(gs[1]), ajeno=CE._m(gs[2])),
                por_semilla=por)


def g_ultima(R, T):
    """Por semilla: media de g de los PADRES en la ultima ventana (None si no hubo partos)."""
    return {c['seed']: CE.g_semilla(c, T)[-1]['media'] for c in R}


def g_pareado(Ra, Rb, T):
    """S: por semilla, gana el primero si su media de g de padres (ultima ventana) es MAYOR; sin partos cuenta como -inf (pierde)."""
    a = g_ultima(Ra, T); b = g_ultima(Rb, T); com = sorted(set(a) & set(b))
    v = lambda x: -1e9 if x is None else x
    d = [v(a[k]) - v(b[k]) for k in com if a[k] is not None and b[k] is not None]
    return dict(semillas=len(com), gana=sum(1 for k in com if v(a[k]) > v(b[k])), dif_med=(round(float(st.median(d)), 4) if d else None))


def banco_actua(R, origen):
    """V5: el banco ACTUA: al menos un fundador salio de un banco del origen pedido (1 propio, 2 ajeno) en el brazo."""
    return fund_origen(R, 0)['fundadores'][{1: 'propio', 2: 'ajeno'}[origen]] > 0


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_termo_banco.md sec. 6)
def lee_serie(res, par, tm, p3, gpar, actua, completa, abortos, ns=20):
    """res: CV.resume por brazo; par: CV.pareado por par; tm: contadores de la pieza; p3: CE.p3_semillas(banco); gpar: g_pareado(banco,
    bancobar); actua: dict(banco=bool, bancobar=bool) (V5)."""
    v = {}
    v['V1_completa'] = bool(completa and abortos == 0 and all(b in res for b in SERIE_BRAZOS)
                            and all(res[b]['coherente'].split('/')[0] == res[b]['coherente'].split('/')[1] for b in SERIE_BRAZOS if b in res))
    v['V2_ancla_O1_gana'] = bool(res.get('o1', {}).get('gana_e5'))
    m = res.get('v143', {}).get('R0_real_med')
    v['V3_ancla_V143'] = m is not None and ANCLA_V143[0] <= m <= ANCLA_V143[1]
    v['V4_pieza_actua'] = bool(CE.pieza(tm.get(CAND, {})) and CE.pieza(tm.get(CTRL, {})))
    v['V5_banco_actua'] = bool(actua.get(CAND) and actua.get(CTRL))
    valido = all(v.values())
    p = {}
    p['P1_banco_cruza_MURO'] = bool(res.get(CAND, {}).get('gana_e5'))
    y = par.get((CAND, REF)) or {}
    p['P2_banco_gana_evo'] = bool(y.get('semillas') and y['gana'] >= GANA * y['semillas'] / 20)
    sp = sum(1 for z in p3.values() if z['cumple'])
    p['P3_g_en_banda'] = bool(p3 and sp >= GANA * len(p3) / 20)
    s = {}
    s['S_g_propio_mayor_que_ajeno'] = bool(gpar.get('semillas') and gpar['gana'] >= GANA * gpar['semillas'] / 20)
    mod = bool(p['P2_banco_gana_evo'] and p['P3_g_en_banda'] and y.get('dif_med') is not None and y['dif_med'] >= DIF_MOD - 1e-12)
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif mod: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    voc = ('germoplasma DEL PROPIO LINAJE' if s['S_g_propio_mayor_que_ajeno'] else 'germoplasma (no especifico del linaje)')
    return dict(validez=v, puertas=p, seleccion=s, p3_semillas_en_banda=sp, modesto=mod, veredicto=ver, vocabulario=voc)


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
        if not all(x in PRACTICA for x in sem): return "--humo: solo semillas de practica 42911-42914"
        if T > 30000: return "--humo: T <= 30000"
    else:
        if not (all(x in SERIE for x in sem) or all(x in REPLICA for x in sem)): return "serie: solo 42001-42020 (serie) o 42021-42040 (replica)"
        if T != T_DEF: return "serie: T = 100000 (preregistrado)"
        if tuple(brazos) != SERIE_BRAZOS: return f"serie: brazos {SERIE_BRAZOS} (preregistrado)"
    return None


def verifica(log):
    """shas FIJADOS de todo lo que corre + carros == construye_banco + revisa_carro + identidad corta (BANCO = 0 == V143_EVO_BAJO)."""
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for n, b in CBB.todas().items():
        ruta = os.path.join(CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = RC.revisa_fuente(b.decode('utf-8'), n) if igual else ['distinto de construye_banco']
        ok &= igual and not vr
        log(f"  carro {n} sha {CBB.h16b(b)} == construye: {igual} - revisa_carro: {'PASA' if not vr else vr[:2]}")
    registra()
    N = lambda x: json.loads(json.dumps(x, default=str))
    mb = CV._MODS['V143_EVO_BAJO']; mb._TEL.clear()
    base = N(P.run(42913, [('C', mb)] * 9, T=3000, fundador_limpio=1)); tb = N(mb._TEL)
    for n in ('V143_EVO_BANCO', 'V143_EVO_BANCOBAR'):
        m = CV._MODS[n]; g = m.BANCO
        try:
            m.BANCO = 0; m._TEL.clear(); m._BANCO.clear(); xx = N(P.run(42913, [('C', m)] * 9, T=3000, fundador_limpio=1)); tx = N(m._TEL)
        finally:
            m.BANCO = g
        i = xx == base and tx == tb; ok &= i
        log(f"  IDENTIDAD CORTA: {n} con BANCO = 0 == V143_EVO_BAJO (salida ENTERA y _TEL, N 9, s 42913, T 3000, fundador limpio): {'OK' if i else 'FALLA'}")
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
        if not (s0 in SERIE and s1 in REPLICA): raise SystemExit("--bloque: primero la serie 42001-42020 y luego la replica 42021-42040")
        vb = bloque(rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto'])
        sb = rs[0]['letra']['seleccion']['S_g_propio_mayor_que_ajeno'] and rs[1]['letra']['seleccion']['S_g_propio_mayor_que_ajeno']
        print(f"serie {rs[0]['letra']['veredicto']} - replica {rs[1]['letra']['veredicto']} -> BLOQUE: {vb}  ({PRERREGISTRO} sec. 6-7) - "
              f"S (propio > ajeno) en las dos: {sb} -> vocabulario: {'germoplasma DEL PROPIO LINAJE' if sb else 'germoplasma (no especifico del linaje)'}")
        return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        T = a.T or T_HUMO
        if a.brazos or a.desde or a.n:
            brazos = [s for s in (a.brazos or 'banco,bancobar').split(',') if s]; desde = a.desde or 42911; n = a.n or 1
            e = valida(True, desde, n, T, brazos)
            if e: raise SystemExit(e)
            tareas = [(s, b) for s in range(desde, desde + n) for b in brazos]
        else:
            tareas = list(HUMO)
            e = valida(True, 42911, 2, T, list(BRAZOS))
            if e: raise SystemExit(e)
        if len(tareas) > 6: raise SystemExit("--humo: maximo 6 corridas por proceso")
        semillas = sorted({s for s, _ in tareas}); brazos = [b for b in BRAZOS if any(b == x for _, x in tareas)]
        pool = 0; dest = os.path.join(DATOS, 'humo')
    else:
        desde = a.desde or 42001; n = a.n or 20
        T = a.T or T_DEF; brazos = [s for s in (a.brazos or ','.join(SERIE_BRAZOS)).split(',') if s]
        e = valida(False, desde, n, T, brazos)
        if e: raise SystemExit(e)
        semillas = list(range(desde, desde + n)); tareas = [(s, b) for s in semillas for b in brazos]; pool = a.pool
        dest = DATOS
    sel = time.strftime('%Y%m%d_%H%M%S')
    pre = f"banco_{'humo_' if a.humo else ''}s{semillas[0]}-{semillas[-1]}_T{T}"
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
    log(f"CORRE_BANCO - {pre} - {sel} - python {platform.python_version()} - pool {pool or 'NO (un proceso)'} - "
        f"corre_banco.py {h16(os.path.abspath(__file__))} - preregistro {PRERREGISTRO} - carpeta {carpeta}")
    log(f"  tareas {len(tareas)} - brazos {brazos} - semillas {semillas[0]}-{semillas[-1]} - T {T} - fundador limpio 1 - reanuda {a.reanuda}")
    ok = verifica(log)
    if a.humo:
        N = lambda x: json.loads(json.dumps(x, default=str))
        sin_seg = lambda z: N({k: v for k, v in z.items() if k != 'seg'})
        x = tarea((42913, 'V143', 2000)); y = CV.tarea((42913, 'V143', 2000))
        e14 = x.pop('tel_evo') == dict(ult=[None] * 9, tel=None) and sin_seg(x) == sin_seg(y)
        x2 = tarea((42913, 'V143_EVO_BAJO', 2000)); y2 = CE.tarea((42913, 'V143_EVO_BAJO', 2000))
        e14b = sin_seg(x2) == sin_seg(y2)
        ok &= e14 and e14b
        log(f"  ENTRADA campo a campo (regla 14): tarea(V143) == corre_v143.tarea: {'OK' if e14 else 'FALLA'} - "
            f"tarea(V143_EVO_BAJO) == corre_evo.tarea de la nube (s 42913, T 2000): {'OK' if e14b else 'FALLA'}")
    if not ok: log("  ALGO FALLA -> no se corre."); return 1
    args = [(s, b, T, carpeta, a.reanuda) for s, b in tareas]
    R = []

    def lin(x):
        s = f"R0 real por linaje {[l['R0_real'] for l in x['linajes']]} - fundadores {[l['fundadores'] for l in x['linajes']]}"
        if (x.get('tel_evo') or {}).get('tel'):
            s += f" - g padres ultima ventana {CE.g_semilla(x, T)[-1]}"
            fo = fund_origen([x], T)['fundadores']
            if fo['propio'] or fo['ajeno']: s += f" - fundadores por origen {fo}"
        return s
    if pool and pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as PL:
            for x in PL.imap_unordered(trabajo, args):
                R.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} s{x['seed']} ({x.get('seg')}s) R0 pista {x.get('R0_pista')} aborto {x['aborto']}"
                                 + ('' if x['aborto'] else ' - ' + lin(x)))
    else:
        for ar in args:
            x = trabajo(ar); R.append(x)
            log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} s{x['seed']} ({x.get('seg')}s) R0 pista {x.get('R0_pista')} aborto {x['aborto']}"
                + ('' if x['aborto'] else ' - ' + lin(x)))
    abortos = sum(1 for x in R if x['aborto'])
    por = {b: sorted([x for x in R if x['brazo'] == b and not x['aborto']], key=lambda z: z['seed']) for b in brazos}
    res = {}; tm = {}; gc = {}; gp = {}; fo = {}
    for b in [x for x in por if por[x]]:
        res[b] = CV.resume(por[b], b, log); tm[b] = CE.tm_suma(por[b])
        if tm[b]: log(f"  pieza ({b}): contadores de la ultima instancia {tm[b]}")
        if BRAZOS[b] in EVOS:
            gc[b] = CE.g_curva(por[b], T); gp[b] = CE.g_paisaje(por[b]); fo[b] = fund_origen(por[b], T)
            log(f"  FUNDADORES POR ORIGEN ({b}): {fo[b]['fundadores']} - g medio {fo[b]['g_media']}")
            log(f"  CURVA DE g ({b}; por ventana de {T // VENTANAS} pasos: padres media [q10 q50 q90] n - vivos media - muertos hijos/cuerpo)")
            for w in gc[b]:
                pa = w['padres']; vi = w['vivos']; mu = w['muertos']
                log(f"    [{w['t0']:6d},{w['t1']:6d}) padres {pa['media']} [{pa['q10']} {pa['q50']} {pa['q90']}] n {pa['n']} - vivos {vi['media']} "
                    f"[{vi['q10']} {vi['q50']} {vi['q90']}] - muertos n {mu['n']} hijos/cuerpo {mu['hijos_por_cuerpo']}")
            log(f"  PAISAJE ({b}; bin de g: cuerpos, hijos por cuerpo, edad media): "
                + ' - '.join(f"{z['g_desde']:+.2f}: {z['cuerpos']}/{z['hijos_por_cuerpo']}/{z['edad_media']:.0f}" for z in gp[b]))
    p3 = CE.p3_semillas(por.get(CAND, []), T)
    log(f"\n  P3 por semilla ({CAND}: media de g de los padres en [{T - T // VENTANAS}, {T}); banda {BANDA_G}): "
        + ' - '.join(f"{s}: {z['media']} (n {z['n']}){'*' if z['cumple'] else ''}" for s, z in sorted(p3.items())))
    PAR = ((CAND, REF), (CAND, CTRL), (CTRL, REF), (CAND, 'v143'), (REF, 'v143'), ('m40', 'v143'), (CAND, 'm40'), ('o1', 'v143'))
    par = {k: CV.pareado(por[k[0]], por[k[1]]) for k in PAR if por.get(k[0]) and por.get(k[1])}
    gpar = g_pareado(por.get(CAND, []), por.get(CTRL, []), T) if por.get(CAND) and por.get(CTRL) else {}
    gref = g_pareado(por.get(CAND, []), por.get(REF, []), T) if por.get(CAND) and por.get(REF) else {}
    log("\nPAREADOS (por semilla: mediana del R0 real de los 9 linajes; gana = semillas en que el primero supera al segundo)")
    for k, v in par.items(): log(f"  {k[0]} vs {k[1]}: gana {v['gana']}/{v['semillas']} - diferencia mediana {v['dif_med']}")
    log(f"  g de padres (ultima ventana) {CAND} vs {CTRL}: gana {gpar.get('gana')}/{gpar.get('semillas')} - dif mediana {gpar.get('dif_med')} (S)")
    log(f"  g de padres (ultima ventana) {CAND} vs {REF}: gana {gref.get('gana')}/{gref.get('semillas')} - dif mediana {gref.get('dif_med')} (descriptivo)")
    completa = True if a.humo else all(len(por.get(b, [])) == len(semillas) for b in SERIE_BRAZOS)
    actua = {b: (bool(por.get(b)) and banco_actua(por[b], 1 if b == CAND else 2)) for b in (CAND, CTRL)}
    letra = lee_serie(res, par, tm, p3, gpar, actua, completa, abortos)
    log(f"\n================ LA LETRA ({PRERREGISTRO} sec. 6)" + (" -- HUMO: T corto y semillas de practica, NO cuenta" if a.humo else ""))
    log(f"  validez {letra['validez']}")
    log(f"  puertas {letra['puertas']} (P3: {letra['p3_semillas_en_banda']}/{len(p3)} semillas) - modesto {letra['modesto']}")
    log(f"  seleccion {letra['seleccion']} -> vocabulario: {letra['vocabulario']}")
    ver = ('HUMO (no cuenta): ' if a.humo else '') + letra['veredicto']
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(brazos=res, pareados={f"{k[0]}_vs_{k[1]}": x for k, x in par.items()}, g_pareado_banco_vs_bancobar=gpar,
                       g_pareado_banco_vs_evo=gref, telemetria=tm, curva_g=gc, paisaje_g=gp, fundadores_origen=fo, p3=p3, letra=letra,
                       semillas=semillas, T=T, humo=a.humo, abortos=abortos, veredicto=ver, preregistro=PRERREGISTRO,
                       sha_runner=h16(os.path.abspath(__file__)), sha_carros={BRAZOS[b]: h16(os.path.join(CARROS, BRAZOS[b] + '.py'))
                                                                              for b in brazos if BRAZOS[b] in EVOS}),
                  fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)})\nTerminado en {time.time()-t0:.1f}s")
    log(f"VEREDICTO DE LA SERIE: {ver}   (regla de parada: {PRERREGISTRO} sec. 7)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
