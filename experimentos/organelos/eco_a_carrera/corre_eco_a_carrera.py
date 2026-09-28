"""corre_eco_a_carrera.py — RUNNER y LETRA del bloque eco_a_carrera: el genoma que la SELECCION NATURAL produjo en ECO_SEL (SEL_C,
FUNCIONA x2: K de ~31 a ~39; veneno+sal de 82 % a 2-3.5 % de las muertes) puesto en la PISTA DE LA CARRERA (el muro).

MISION: llegar a la AGI por este camino. Principio del director: que la evolucion construya el organo, no nosotros.

Pregunta: el genoma evolucionado (15 genes del cerebro; ni una linea de codigo nueva) ¿baja las muertes de fundadores por veneno y sal
y sube el R0 real y P1 frente al genoma de fabrica (G0 / F1) y frente al genoma del brazo sin herencia (AZA_C)?

ENTRADA (regla 14): la corrida ES experimentos/organelos/frio_carrera/corre_frio_carrera.tarea (se IMPORTA, no se toca; sha fijado), que
ES corre_v143.tarea (juez.tarea con 9 carros iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador limpio 1 +
juez.resumen_linaje, solo fisica, ERR-96). Lo unico agregado: (1) antes de cada corrida el runner fija GENOMA en el modulo del carro (el
genoma de la semilla ECO emparejada; genomas_eco_sel.json, construido por extrae_genomas.py) y lo devuelve a None al terminar;
(2) 'tel_eac' = la telemetria de SOLO LECTURA d['carro']['eco_a_carrera'] (no puntua).

BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, fundador limpio):
  g0    EAC_G0   + GENOMA = G0      (F1/G0: la base de frio_carrera, V143_RES0, con el genoma de fabrica por el mismo camino)
  sel   EAC_SEL  + GENOMA SEL_C     (HIPOTESIS)
  aza   EAC_AZA  + GENOMA AZA_C     (CONTROL: el genoma sin herencia; varia igual)
  selv  EAC_SELV + GENOMA SEL_C     (EXPLORATORIO: el genoma sobre V143 sin RES0)
  v143  V143                        (base del muro)
  o1    O1                          (techo; ancla de la pista)
SEMILLAS (grep 28-sep: 394xx libre en *.py/*.md/*.txt/*.log de organelos y bundle y en las ramas remotas):
  explora 39401-39410 -> genomas ECO serie 45301-45310 · serie 39421-39440 -> ECO serie 45301-45320 ·
  replica 39441-39460 -> ECO replica 45321-45340 · practica 39491-39499 -> ECO replica 45331-45339 (arnes 39491-39494, humo 39495-39496).
nube-9: trabajo() atrapa TODO; JSON por corrida ANTES de volver (ERR-54); --reanuda salta las hechas. NADA de Pool: --explora corre en
UN proceso la lista de tareas que se le da (el creador lanza a lo sumo 4 procesos en paralelo, cada uno con sus semillas).

CRITERIO EXPLORATORIO (escrito ANTES de correr 39401-39410; decide solo si se escribe el preregistro confirmatorio):
  "SEL mejora claramente" = SEL > G0 pareado (mediana del R0 real de los 9 linajes) en >= 8/10 con diferencia mediana >= +0.05,
  Y SEL > AZA en >= 8/10, Y la fraccion de muertes de FUNDADORES por veneno+sal de SEL por debajo de la de G0 (agregado).
PREDICCIONES DEL CREADOR (firmadas antes del humo y del exploratorio, 28-sep ~15:50):
  R0 real mediano: v143 [0.55, 0.65]; g0 [0.50, 0.62]; sel [0.45, 0.70]; aza = g0 +- 0.05. P("mejora claramente") = 0.20.
  Fraccion de muertes de fundadores por veneno+sal: g0 ~0.93; sel >= 0.85 con p 0.70 (la caida de ECO, 82 % -> 3 %, NO transfiere:
  en la carrera el fundador es una instancia nueva que muere al primer encuentro, y el genoma cambia como aprende, no lo que ya sabe).
  SEL cruza (mayoria de linajes en >= 8/10 semillas): p 0.03.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN):
  python .../corre_eco_a_carrera.py --humo                                     # 1 proceso, 6 corridas, T 20 000, escribe su JSON
  python .../corre_eco_a_carrera.py --explora --semillas 39401,39402 [--brazos g0,sel,...]   # 1 proceso, JSON por corrida
  python .../corre_eco_a_carrera.py --lee <carpeta>                            # resume una carpeta (explora o serie)
  python .../corre_eco_a_carrera.py --serie --desde 39421 --n 20 --pool 6      # SOLO el coordinador, si hay preregistro
"""
import argparse, hashlib, importlib.util, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
FCD = os.path.join(os.path.dirname(AQUI), 'frio_carrera')
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, FCD, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_frio_carrera as FC   # tarea (== corre_v143.tarea + tel_fc), establece; se IMPORTA, no se toca
import construye_eco_a_carrera as CE
import extrae_genomas as XG
import revisa_carro as RC
CV = FC.CV; P = FC.P; J = FC.J

CARROS = os.path.join(AQUI, 'carros')
DATOS = os.path.join(AQUI, 'datos')
GENOMAS = os.path.join(AQUI, 'genomas_eco_sel.json')
SHAS = {os.path.join(FCD, 'corre_frio_carrera.py'): '49de4dd28a8f3c3a', os.path.join(FCD, 'carros', 'V143_RES0.py'): 'fab1d8068fe901a5',
        os.path.join(FCD, 'carros', 'V143_TEL.py'): 'f73f8ea41399bb79', os.path.join(V143D, 'corre_v143.py'): '24100621c450da22',
        os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5', os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4',
        os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12', os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028'}
SHA_GENOMAS = '84b64bf54acff2b0'
BRAZOS = {'g0': 'EAC_G0', 'sel': 'EAC_SEL', 'aza': 'EAC_AZA', 'selv': 'EAC_SELV', 'v143': 'V143', 'o1': 'O1'}
FUENTE = {'g0': 'G0', 'sel': 'SEL_C', 'aza': 'AZA_C', 'selv': 'SEL_C'}
PROPIOS = ('EAC_G0', 'EAC_SEL', 'EAC_AZA', 'EAC_SELV')
SERIE_BRAZOS = ('v143', 'g0', 'sel', 'aza', 'o1')          # la confirmatoria (si la hay) NO lleva selv
EXPLORA_BRAZOS = ('v143', 'g0', 'sel', 'aza', 'selv', 'o1')
EXPLORA = range(39401, 39411); SERIE = range(39421, 39441); REPLICA = range(39441, 39461); PRACTICA = range(39491, 39500)
HUMO = [(39495, 'g0'), (39495, 'sel'), (39495, 'aza'), (39495, 'v143'), (39496, 'g0'), (39496, 'sel')]
T_DEF = 100000; T_HUMO = 20000
GANA = 15; DIF_MOD = 0.10; ANCLA_V143 = (0.40, 0.80)   # la letra del muro (PREREGISTRO_muro.md sec. 6 / termo sec. 6), sin cambios


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def eco_de(seed):
    """Semilla de la carrera -> (corrida ECO, semilla ECO) cuyo genoma lleva."""
    if seed in EXPLORA: return 'serie', 45301 + seed - 39401
    if seed in SERIE: return 'serie', 45301 + seed - 39421
    if seed in REPLICA: return 'replica', 45321 + seed - 39441
    if seed in PRACTICA: return 'replica', 45331 + seed - 39491
    raise SystemExit(f"semilla {seed} fuera de los rangos de eco_a_carrera")


_GEN = [None]


def genomas():
    if _GEN[0] is None:
        raw = open(GENOMAS, 'rb').read()
        if hashlib.sha256(raw).hexdigest()[:16] != SHA_GENOMAS: raise SystemExit(f"genomas_eco_sel.json sha != {SHA_GENOMAS}")
        _GEN[0] = json.loads(raw)
    return _GEN[0]


def genoma_de(brazo, seed):
    """El dict de 15 genes que lleva el brazo en esa semilla (G0 para g0; None para v143 y o1)."""
    if brazo not in FUENTE: return None, None
    G = genomas()
    if FUENTE[brazo] == 'G0': return dict(G['G0']), 'G0'
    c, s = eco_de(seed); x = G['corridas'][c][FUENTE[brazo]][str(s)]
    return dict(x['genoma']), f"{c}:{FUENTE[brazo]}:{s}" + (f"(sust {x['sustituye']})" if x.get('sustituye') else '')


def registra():
    for n in PROPIOS:
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", os.path.join(CARROS, n + '.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    for k, v in BRAZOS.items(): CV.BRAZOS.setdefault(k, v)


def tarea(args):
    """(seed, brazo, T) -> corre_frio_carrera.tarea((seed, carro, T)) con GENOMA fijado en el modulo + 'tel_eac' (solo lectura)."""
    seed, brazo, T = args
    registra()
    carro = BRAZOS[brazo]; g, orig_g = genoma_de(brazo, seed)
    m = CV._MODS.get(carro) if carro in PROPIOS else None
    if m is not None:
        if m.FUENTE != FUENTE[brazo]: raise SystemExit(f"{carro}: FUENTE {m.FUENTE} != {FUENTE[brazo]}")
        m.GENOMA = g
    cap = []; orig = P.run

    def run2(*a, **k):
        r = orig(*a, **k); cap.append([(d.get('carro') or {}).get('eco_a_carrera') for d in r['linajes']]); return r
    P.run = run2
    try:
        x = FC.tarea((seed, carro, T))
    finally:
        P.run = orig
        if m is not None: m.GENOMA = None
    x['tel_eac'] = cap[0] if cap else None; x['genoma'] = g; x['genoma_de'] = orig_g
    return x


def trabajo(args):
    seed, brazo, T, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: return json.load(fh)
    try:
        x = tarea((seed, brazo, T)); x.pop('pizarra_log', None); x['brazo'] = brazo; x['aborto'] = None
    except BaseException as e:   # noqa: nube-9
        x = dict(seed=seed, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ medidas nuevas (solo fisica: juez.resumen_linaje -> telem)
def fundadores(R):
    """Cuerpos FUNDADORES (origen 0 en la fisica) que murieron: causa, si pario, vida. Agregado sobre linajes y semillas."""
    cz = dict(hambre=0, sed=0, veneno=0, sal=0); n = 0; sin_hijos = 0; vidas = []; nf_lin = []; cz_hijos = dict(hambre=0, sed=0, veneno=0, sal=0)
    for c in R:
        for l in c['linajes']:
            t = l['telem']; o = t['origen']; cc = t['causa_cuerpo']; dpv = t['desc_por_vida']; v = t['vidas']
            if len(cc) != l['muertes'] or len(o) != l['muertes'] + 1: raise SystemExit("fundadores: telemetria truncada")
            nf_lin.append(sum(1 for g in o if not g))
            for i, ca in enumerate(cc):
                if not o[i]:
                    cz[ca] += 1; n += 1; sin_hijos += int(dpv[i] == 0); vidas.append(v[i])
                else: cz_hijos[ca] += 1
    nh = sum(cz_hijos.values())
    return dict(muertes_fundadores=n, causas_fundadores=cz, frac_BD_fundadores=(round((cz['veneno'] + cz['sal']) / n, 4) if n else None),
                frac_fundadores_sin_parir=(round(sin_hijos / n, 4) if n else None), vida_fundador_med=CV.med(vidas),
                fundadores_por_linaje_med=CV.med(nf_lin), causas_nacidos=cz_hijos,
                frac_BD_nacidos=(round((cz_hijos['veneno'] + cz_hijos['sal']) / nh, 4) if nh else None))


def genoma_ok(R, brazo):
    """V4: el genoma declarado es el APLICADO en todos los linajes de todas las corridas del brazo (telemetria de solo lectura)."""
    if brazo not in FUENTE: return True
    for c in R:
        tel = c.get('tel_eac') or []
        if len(tel) != 9 or c.get('genoma') is None: return False
        g = c['genoma']
        for t in tel:
            if not t or t['fuente'] != FUENTE[brazo]: return False
            a = t['aplicado']
            for k, v in g.items():
                w = int(round(v)) if k in ('memoria_rechazo', 'NK') else float(v)
                if a[k] != w: return False
    return True


# ------------------------------------------------------------------ LA LETRA (la del muro, sin cambios; PREREGISTRO_eco_a_carrera.md sec. 6)
def lee_serie(res, par, gok, completa, abortos, n=20):
    v = {}
    v['V1_completa'] = bool(completa and abortos == 0 and all(b in res for b in SERIE_BRAZOS)
                            and all(res[b]['coherente'].split('/')[0] == res[b]['coherente'].split('/')[1] for b in SERIE_BRAZOS if b in res))
    v['V2_ancla_O1_gana'] = bool(res.get('o1', {}).get('gana_e5'))
    m = res.get('v143', {}).get('R0_real_med')
    v['V3_ancla_V143'] = m is not None and ANCLA_V143[0] <= m <= ANCLA_V143[1]
    v['V4_genoma_aplicado'] = bool(gok.get('sel') and gok.get('aza') and gok.get('g0'))
    valido = all(v.values())
    p = {}
    p['P1_sel_cruza'] = bool(res.get('sel', {}).get('gana_e5'))
    x = par.get(('sel', 'v143')) or {}
    p['P2_sel_gana_v143'] = bool(x.get('semillas') and x['gana'] >= GANA * x['semillas'] / 20)
    p['P3_aza_no_cruza'] = not bool(res.get('aza', {}).get('gana_e5'))
    y = par.get(('sel', 'aza')) or {}
    mod = bool(p['P2_sel_gana_v143'] and x.get('dif_med') is not None and x['dif_med'] >= DIF_MOD - 1e-12
               and y.get('semillas') and y['gana'] > 10 * y['semillas'] / 20)
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif mod: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    return dict(validez=v, puertas=p, modesto=mod, veredicto=ver)


def criterio_explora(par, fz):
    a = par.get(('sel', 'g0')) or {}; b = par.get(('sel', 'aza')) or {}
    n = a.get('semillas') or 0
    c1 = bool(n and a['gana'] >= 0.8 * n and a['dif_med'] >= 0.05 - 1e-12)
    c2 = bool(b.get('semillas') and b['gana'] >= 0.8 * b['semillas'])
    fs = (fz.get('sel') or {}).get('frac_BD_fundadores'); fg = (fz.get('g0') or {}).get('frac_BD_fundadores')
    c3 = fs is not None and fg is not None and fs < fg
    return dict(sel_gana_g0=c1, sel_gana_aza=c2, sel_menos_BD_fundadores=c3, mejora_claramente=bool(c1 and c2 and c3))


PAR = (('sel', 'g0'), ('sel', 'aza'), ('sel', 'v143'), ('g0', 'v143'), ('aza', 'g0'), ('selv', 'v143'), ('selv', 'sel'), ('o1', 'sel'),
       ('o1', 'v143'))


def resume_carpeta(R, brazos, semillas, log, completa, abortos, humo):
    por = {b: sorted([x for x in R if x['brazo'] == b and not x['aborto']], key=lambda z: z['seed']) for b in brazos}
    res = {}; fz = {}; es = {}; gok = {}
    for b in [x for x in brazos if por.get(x)]:
        res[b] = CV.resume(por[b], b, log); fz[b] = fundadores(por[b]); es[b] = FC.establece(por[b]); gok[b] = genoma_ok(por[b], b)
        log(f"  FUNDADORES ({b}): {fz[b]}")
        log(f"  ESTABLECIMIENTO ({b}, descriptivo): {es[b]} · genoma aplicado (V4): {gok[b]}")
    par = {k: CV.pareado(por[k[0]], por[k[1]]) for k in PAR if por.get(k[0]) and por.get(k[1])}
    log("\nPAREADOS (por semilla: mediana del R0 real de los 9 linajes; gana = semillas en que el primero supera al segundo)")
    for k, v in par.items(): log(f"  {k[0]} vs {k[1]}: gana {v['gana']}/{v['semillas']} · diferencia mediana {v['dif_med']}")
    letra = lee_serie(res, par, gok, completa, abortos)
    ce = criterio_explora(par, fz)
    log(f"\n  LETRA DEL MURO (sobre {len(semillas)} semillas; con n < 20 las puertas escalan GANA*n/20 y NO cuenta): {letra}")
    log(f"  CRITERIO EXPLORATORIO (decide si se escribe el preregistro): {ce}")
    return dict(brazos=res, fundadores=fz, establece=es, genoma_aplicado=gok, pareados={f"{k[0]}_vs_{k[1]}": x for k, x in par.items()},
                letra=letra, criterio_explora=ce, semillas=semillas, abortos=abortos, humo=humo)


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    s = h16(GENOMAS); ok &= s == SHA_GENOMAS; log(f"  sha genomas_eco_sel.json {s} {'OK' if s == SHA_GENOMAS else 'FALLA'}")
    for n, b in CE.todas().items():
        ruta = os.path.join(CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = RC.revisa_fuente(b.decode('utf-8'), n) if igual else ['distinto de construye_eco_a_carrera']
        ok &= igual and not vr
        log(f"  carro {n} sha {CE.h16b(b)} == construye: {igual} · revisa_carro: {'PASA' if not vr else vr[:2]}")
    registra()
    N = lambda x: json.loads(json.dumps(x, default=str))
    FC.registra()
    a = P.run(39491, [('C', CV._MODS['V143_RES0'])] * 9, T=2000, fundador_limpio=1)
    m = CV._MODS['EAC_G0']; m.GENOMA = None
    b = P.run(39491, [('C', m)] * 9, T=2000, fundador_limpio=1)
    i1 = N(a) == N(b); ok &= i1
    log(f"  IDENTIDAD CORTA: EAC_G0 con GENOMA None == V143_RES0 de frio_carrera (salida ENTERA, N 9, s 39491, T 2000): {'OK' if i1 else 'FALLA'}")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true')
    g.add_argument('--explora', action='store_true')
    g.add_argument('--serie', action='store_true')
    g.add_argument('--lee', default=None)
    ap.add_argument('--brazos', default=None)
    ap.add_argument('--semillas', default=None)
    ap.add_argument('--desde', type=int, default=None)
    ap.add_argument('--n', type=int, default=None)
    ap.add_argument('--T', type=int, default=None)
    ap.add_argument('--pool', type=int, default=0)
    ap.add_argument('--carpeta', default=None)
    ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115
    if a.lee:
        registra()   # enmienda de instrumento (antes de leer ningun numero): CV.resume necesita los brazos EAC en CV.BRAZOS
        carpeta = a.lee
        R = [json.load(open(os.path.join(carpeta, f), encoding='utf-8')) for f in sorted(os.listdir(carpeta))
             if f.endswith('.json') and '_s' in f and not f.startswith('resumen')]
        brazos = [b for b in BRAZOS if any(x['brazo'] == b for x in R)]
        semillas = sorted({x['seed'] for x in R}); abortos = sum(1 for x in R if x['aborto'])
        LOGF = open(os.path.join(carpeta, 'lee.txt'), 'w', encoding='utf-8')

        def log(s=''):
            print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        log(f"LEE {carpeta} · {len(R)} corridas · brazos {brazos} · semillas {semillas} · abortos {abortos}")
        completa = all(sum(1 for x in R if x['brazo'] == b) == len(semillas) for b in brazos)
        out = resume_carpeta(R, brazos, semillas, log, completa, abortos, False)
        out['sha_runner'] = h16(os.path.abspath(__file__))
        rj = os.path.join(carpeta, 'resumen.json')
        with open(rj, 'w', encoding='utf-8') as fh: json.dump(out, fh, ensure_ascii=False, indent=1)
        log(f"\n  RESUMEN {rj} (sha {h16(rj)})")
        return 0
    if a.pool and not a.serie: raise SystemExit("Pool solo con --serie (y solo el coordinador)")
    if a.humo:
        T = a.T or T_HUMO
        if T > 30000: raise SystemExit("--humo: T <= 30000")
        tareas = list(HUMO); dest = os.path.join(DATOS, 'humo')
    elif a.explora:
        T = a.T or T_DEF
        if T != T_DEF: raise SystemExit("--explora: T = 100000")
        sem = [int(s) for s in (a.semillas or '').split(',') if s]
        if not sem or not all(s in EXPLORA for s in sem): raise SystemExit("--explora: --semillas dentro de 39401-39410")
        brazos = [s for s in (a.brazos or ','.join(EXPLORA_BRAZOS)).split(',') if s]
        if any(b not in EXPLORA_BRAZOS for b in brazos): raise SystemExit(f"--explora: brazos en {EXPLORA_BRAZOS}")
        tareas = [(s, b) for s in sem for b in brazos]; dest = DATOS
    else:
        T = a.T or T_DEF; desde = a.desde; n = a.n or 20
        sem = list(range(desde, desde + n)) if desde else []
        if not sem or not (all(s in SERIE for s in sem) or all(s in REPLICA for s in sem)): raise SystemExit("--serie: 39421-39440 o 39441-39460")
        if T != T_DEF: raise SystemExit("--serie: T = 100000")
        tareas = [(s, b) for b in SERIE_BRAZOS for s in sem]; dest = DATOS
    if len(tareas) > 6 and a.humo: raise SystemExit("--humo: maximo 6 corridas")
    semillas = sorted({s for s, _ in tareas}); brazos = [b for b in BRAZOS if any(b == x for _, x in tareas)]
    sel_ = time.strftime('%Y%m%d_%H%M%S')
    if a.carpeta: carpeta = a.carpeta
    elif a.humo: carpeta = os.path.join(dest, f"eac_humo_s{semillas[0]}-{semillas[-1]}_T{T}_{sel_}")
    elif a.explora: carpeta = os.path.join(dest, f"eac_explora_s39401-39410_T{T}")
    else: carpeta = os.path.join(dest, f"eac_{'serie' if semillas[0] in SERIE else 'replica'}_s{semillas[0]}-{semillas[-1]}_T{T}")
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, f"log_{sel_}_{os.getpid()}.txt"), 'a', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time()
    modo = 'humo' if a.humo else ('explora' if a.explora else 'serie')
    log(f"CORRE_ECO_A_CARRERA · {modo} · {sel_} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · "
        f"corre_eco_a_carrera.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  tareas {len(tareas)} · brazos {brazos} · semillas {semillas} · T {T} · fundador limpio 1 · reanuda {a.reanuda}")
    ok = verifica(log)
    if a.humo:
        ok &= CV.verifica_todo(log, con_entrada=True)   # regla 14 de corre_v143: corre_v143.tarea == juez.tarea
        N = lambda x: json.loads(json.dumps(x, default=str))
        x = tarea((39491, 'v143', 2000)); y = CV.tarea((39491, 'V143', 2000))
        e14 = (x.pop('tel_eac') == [None] * 9 and x.pop('tel_fc') == [None] * 9 and x.pop('genoma') is None and x.pop('genoma_de') is None
               and N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in y.items() if k != 'seg'}))
        ok &= e14; log(f"  ENTRADA campo a campo (regla 14): tarea de este runner == corre_v143.tarea (V143, s 39491, T 2000): {'OK' if e14 else 'FALLA'}")
    if not ok: log("  ALGO FALLA -> no se corre."); return 1
    args = [(s, b, T, carpeta, a.reanuda) for s, b in tareas]
    R = []
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, args):
                R.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} s{x['seed']} ({x.get('seg')}s) R0 pista {x.get('R0_pista')} aborto {x['aborto']}")
    else:
        for ar in args:
            x = trabajo(ar); R.append(x)
            log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} s{x['seed']} ({x.get('seg')}s) genoma {x.get('genoma_de')} aborto {x['aborto']} · "
                f"R0 real por linaje {[l['R0_real'] for l in x['linajes']]} · fundadores {[l['fundadores'] for l in x['linajes']]}")
    abortos = sum(1 for x in R if x['aborto'])
    if a.explora:
        log(f"\n  EXPLORA: {len(R)} corridas escritas en {carpeta}; se resume con --lee cuando terminen todos los procesos.")
        return 0
    completa = all(sum(1 for x in R if x['brazo'] == b) == len(semillas) for b in brazos) if not a.humo else True
    out = resume_carpeta(R, brazos, semillas, log, completa, abortos, a.humo)
    out.update(T=T, sha_runner=h16(os.path.abspath(__file__)), sha_carros={n: h16(os.path.join(CARROS, n + '.py')) for n in PROPIOS},
               veredicto=('HUMO (no cuenta): ' if a.humo else '') + out['letra']['veredicto'])
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh: json.dump(out, fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)})\nTerminado en {time.time()-t0:.1f}s")
    log(f"VEREDICTO: {out['veredicto']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
