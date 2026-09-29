"""corre_eco_ing_a_carrera.py — RUNNER y LETRA del bloque eco_ing_a_carrera: el genoma que la SELECCION produjo en ECO_SEL_ING (hijos
INGENUOS, carro FABRICA_ECO; ING_SEL_C = FUNCIONA en la serie 46101-46120: K 101.0 vs 96.3, K_nac 16.1 vs 12.6, fund_2a -32 %, 20/20)
puesto en la PISTA DE LA CARRERA (el muro). A diferencia de SEL_C (eco_a_carrera = NO: R0 0.365 vs G0 0.601; 38.5 fundadores por
linaje), este genoma se selecciono para EMPEZAR DE CERO, como el fundador de la carrera.

MISION: llegar a la AGI por este camino. Principio del director: que la evolucion construya el organo, no nosotros.

Pregunta: el genoma ING_SEL_C (15 genes del cerebro; ni una linea de codigo nueva) ¿baja los fundadores por linaje y sube el R0 real
frente al genoma de fabrica (G0) y frente al genoma del brazo sin herencia (ING_AZA_C)?

LA BASE (decidida ANTES de correr; justificacion):
  ECO_SEL_ING selecciono con FABRICA_ECO = FAMB_RES0_ECO SIN la tabla de la familia. La traduccion de FAMB_RES0_ECO a la carrera es
  V143_RES0 (frio_carrera: F1 = el nacido lee el nodo del linaje SIN neutras); la de FABRICA_ECO es V143 con RES0 0 (el nodo de la
  carrera tal como lo trae FABRICA de la carrera, con neutras). => BASE PRIMARIA = V143 (carros EIC_*V, RES0 0).
  Ademas: (i) con G0 esa base ES V143 bit a bit (arnes, y una identidad LARGA a T 1e5 en 39461: brazo g0v contra v143), asi que
  'ING_SEL > G0' es 'ING_SEL > la base del muro', la comparacion de la P2 del muro; (ii) en eco_a_carrera V143 (0.697; 11.5 fund/lin)
  fue MEJOR que G0 con familia (0.601; 19.5): la primaria es el comparador mas duro.
  Declarado: ni V143 es estrictamente ingenuo. En la carrera el nodo del linaje (las ultimas mordidas de los muertos) lo lee todo
  nacido; en ECO cada cuerpo es una instancia y su nodo no pasa. El fundador si es ingenuo en TODAS las bases (fundador_limpio 1:
  instancia nueva, sin nace()). Un carro sin nodo seria codigo nuevo: NO entra aqui (queda para despues).
  SECUNDARIA (reportada, no decide): la base con familia de eco_a_carrera (EIC_G0/EIC_ING/EIC_AZA, RES0 1) y la REFERENCIA SEL_C
  (EIC_SELC == EAC_SEL: lo que fallo, en semillas nuevas).

ENTRADA (regla 14): la corrida ES frio_carrera/corre_frio_carrera.tarea (se IMPORTA, sha fijado) == corre_v143.tarea (juez.tarea con 9
carros iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador limpio 1). Lo unico agregado (el mismo mecanismo de
eco_a_carrera): el runner fija GENOMA en el modulo del carro antes de la corrida y lo devuelve a None; 'tel_eac' = telemetria de solo
lectura d['carro']['eco_a_carrera'] (no puntua).

BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, fundador limpio):
  v143  V143                          base del muro == G0 de la base primaria
  ingv  EIC_INGV + ING_SEL_C          PRIMARIA, HIPOTESIS
  azav  EIC_AZAV + ING_AZA_C          PRIMARIA, CONTROL (varia igual, no se hereda)
  g0v   EIC_G0V  + G0                 solo 39461: identidad LARGA contra v143 (instrumento)
  g0    EIC_G0   + G0                 secundaria: base con familia (F1)
  ing   EIC_ING  + ING_SEL_C          secundaria
  aza   EIC_AZA  + ING_AZA_C          secundaria
  selc  EIC_SELC + SEL_C (ECO_SEL)    referencia de lo que fallo
  o1    O1                            techo; ancla de la pista
GENOMAS: la semilla de la carrera se empareja con una semilla ECO (genomas_ing_serie.json / genomas_ing_replica.json, de
extrae_genomas_ing.py con el MEDOIDE de eco_a_carrera, importado; SEL_C de eco_a_carrera/genomas_eco_sel.json, solo lectura).
SEMILLAS (grep 28-sep ~18:15: 3946x-3947x y 3950x-3959x libres en *.py/*.md/*.txt/*.log de organelos y bundle, todas las ramas, y
como seed en JSON): explora 39461-39470 -> ING serie 46101-46110 (SEL_C: ECO_SEL serie 45301-45310) ·
  serie 39511-39530 -> ING serie 46101-46120 · replica 39531-39550 -> ING replica 46121-46140 ·
  practica 39561-39569 -> ING serie 46111-46119 (SEL_C: 45311-45319) (arnes 39561-39564, humo 39565-39566).
nube-9: trabajo() atrapa TODO; JSON por corrida ANTES de volver (ERR-54); --reanuda salta las hechas. NADA de Pool fuera de --serie.

CRITERIO EXPLORATORIO (escrito ANTES de correr 39461-39470; decide solo si se escribe el preregistro confirmatorio). En la PRIMARIA:
  C1  ingv > v143 (G0 de la base) en R0 real (mediana de los 9 linajes por semilla) en >= 7/10;
  C2  ingv > azav en R0 real en >= 7/10;
  C3  fundadores por linaje (media de los 9 linajes por semilla, 'fundadores' del juez) de ingv < v143 (estricto) en >= 7/10.
  PASA = C1 y C2 y C3. Se reporta igual en la secundaria (ing vs g0 / aza), sin que decida. P1 (semillas con la mayoria de linajes
  cruzando con R0 real) de cada brazo, y la letra del muro sobre la primaria (con n = 10, NO cuenta).
  Si la primaria no pasa y la secundaria si, se reporta asi y NO se escribe preregistro (lo decide el coordinador).
PREDICCIONES DEL CREADOR (firmadas antes del humo y del exploratorio, 28-sep ~18:05):
  R0 real mediano: v143 [0.60, 0.75]; ingv [0.45, 0.75]; azav = v143 +- 0.07; g0 [0.52, 0.66]; selc [0.30, 0.50].
  Fundadores por linaje (mediana): v143 [8, 16]; ingv [8, 30]. P(PASA primaria) = 0.15: el medoide ING_SEL comparte con SEL_C los
  movimientos grandes (alpha x3.5, tau_e x0.37, memoria_rechazo x2.2) que en eco_a_carrera no transfirieron; la seleccion en ECO
  premia sobrevivir en w90, no el veneno/sal de la carrera (98 % de las muertes de fundadores). P(ingv cruza P1) = 0.03.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN):
  python .../corre_eco_ing_a_carrera.py --humo                                        # 1 proceso, 6 corridas, T 20 000, escribe JSON
  python .../corre_eco_ing_a_carrera.py --explora --semillas 39461,39462 [--brazos v143,ingv,...]   # 1 proceso, JSON por corrida
  python .../corre_eco_ing_a_carrera.py --lee <carpeta>
  python .../corre_eco_ing_a_carrera.py --serie --desde 39511 --n 20 --pool 6         # SOLO el coordinador, si hay preregistro
"""
import argparse, hashlib, importlib.util, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
EAC = os.path.join(os.path.dirname(AQUI), 'eco_a_carrera')
FCD = os.path.join(os.path.dirname(AQUI), 'frio_carrera')
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, FCD, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_frio_carrera as FC   # tarea (== corre_v143.tarea + tel_fc), establece; se IMPORTA, no se toca
import construye_eco_ing_a_carrera as CI
import extrae_genomas_ing as XI
import revisa_carro as RC
CV = FC.CV; P = FC.P; J = FC.J

CARROS = os.path.join(AQUI, 'carros')
DATOS = os.path.join(AQUI, 'datos')
GEN_ING = {'serie': os.path.join(AQUI, 'genomas_ing_serie.json'), 'replica': os.path.join(AQUI, 'genomas_ing_replica.json')}
GEN_SEL = os.path.join(EAC, 'genomas_eco_sel.json')
SHAS = {os.path.join(FCD, 'corre_frio_carrera.py'): '49de4dd28a8f3c3a', os.path.join(FCD, 'carros', 'V143_RES0.py'): 'fab1d8068fe901a5',
        os.path.join(FCD, 'carros', 'V143_TEL.py'): 'f73f8ea41399bb79', os.path.join(V143D, 'corre_v143.py'): '24100621c450da22',
        os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5', os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4',
        os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12', os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028',
        os.path.join(EAC, 'construye_eco_a_carrera.py'): '403c747caaae1c1e', os.path.join(EAC, 'extrae_genomas.py'): '1c8082d17d8e095f',
        os.path.join(EAC, 'corre_eco_a_carrera.py'): '399a52ffcf3456f4', GEN_SEL: '84b64bf54acff2b0'}
SHA_GEN = {'serie': '216a02a83318be8a', 'replica': None}   # replica: se fija cuando la replica 46121-46140 este completa y extraida
BRAZOS = {'v143': 'V143', 'ingv': 'EIC_INGV', 'azav': 'EIC_AZAV', 'g0v': 'EIC_G0V', 'g0': 'EIC_G0', 'ing': 'EIC_ING', 'aza': 'EIC_AZA',
          'selc': 'EIC_SELC', 'o1': 'O1'}
FUENTE = {'ingv': 'ING_SEL_C', 'azav': 'ING_AZA_C', 'g0v': 'G0', 'g0': 'G0', 'ing': 'ING_SEL_C', 'aza': 'ING_AZA_C', 'selc': 'SEL_C'}
PROPIOS = tuple(n for n, _, _ in CI.VARIANTES)
HIP, CTL, BASE = 'ingv', 'azav', 'v143'                    # la PRIMARIA
SERIE_BRAZOS = ('v143', 'ingv', 'azav', 'o1')             # la confirmatoria (si la hay)
EXPLORA_BRAZOS = ('v143', 'ingv', 'azav', 'g0', 'ing', 'aza', 'selc', 'o1', 'g0v')
EXPLORA = range(39461, 39471); SERIE = range(39511, 39531); REPLICA = range(39531, 39551); PRACTICA = range(39561, 39570)
HUMO = [(39565, 'v143'), (39565, 'g0v'), (39565, 'ingv'), (39565, 'azav'), (39566, 'ing'), (39566, 'selc')]
T_DEF = 100000; T_HUMO = 20000
GANA = 15; DIF_MOD = 0.10; ANCLA_V143 = (0.40, 0.80)   # la letra del muro (PREREGISTRO_muro.md sec. 6), SIN cambios
EXPL_MIN = 7                                           # criterio exploratorio: >= 7/10


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def eco_de(seed):
    """Semilla de la carrera -> (corrida ING, semilla ING, semilla ECO_SEL para SEL_C, corrida ECO_SEL)."""
    if seed in EXPLORA: return 'serie', 46101 + seed - 39461, 'serie', 45301 + seed - 39461
    if seed in SERIE: return 'serie', 46101 + seed - 39511, 'serie', 45301 + seed - 39511
    if seed in REPLICA: return 'replica', 46121 + seed - 39531, 'replica', 45321 + seed - 39531
    if seed in PRACTICA: return 'serie', 46111 + seed - 39561, 'serie', 45311 + seed - 39561
    raise SystemExit(f"semilla {seed} fuera de los rangos de eco_ing_a_carrera")


_GEN = {}


def carga(clave, ruta, sha):
    if clave not in _GEN:
        if sha is None: raise SystemExit(f"{os.path.basename(ruta)}: sha no fijado todavia")
        raw = open(ruta, 'rb').read()
        if hashlib.sha256(raw).hexdigest()[:16] != sha: raise SystemExit(f"{os.path.basename(ruta)} sha != {sha}")
        _GEN[clave] = json.loads(raw)
    return _GEN[clave]


def genoma_de(brazo, seed):
    """El dict de 15 genes que lleva el brazo en esa semilla (G0 para g0/g0v; None para v143 y o1)."""
    if brazo not in FUENTE: return None, None
    f = FUENTE[brazo]; ci, si, cs, ss = eco_de(seed)
    if f == 'G0': return dict(carga('serie', GEN_ING['serie'], SHA_GEN['serie'])['G0']), 'G0'
    if f == 'SEL_C':
        x = carga('sel', GEN_SEL, SHAS[GEN_SEL])['corridas'][cs]['SEL_C'][str(ss)]; c, s = cs, ss
    else:
        x = carga(ci, GEN_ING[ci], SHA_GEN[ci])['brazos'][f][str(si)]; c, s = ci, si
    return dict(x['genoma']), f"{c}:{f}:{s}" + (f"(sust {x['sustituye']})" if x.get('sustituye') else '')


def registra():
    for n in PROPIOS:
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", os.path.join(CARROS, n + '.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    for k, v in BRAZOS.items(): CV.BRAZOS.setdefault(k, v)
    for k, v in BRAZOS.items():
        if CV.BRAZOS[k] != v: raise SystemExit(f"CV.BRAZOS[{k}] = {CV.BRAZOS[k]} != {v} (choque de nombres)")


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


# ------------------------------------------------------------------ medidas (solo fisica: juez.resumen_linaje -> telem)
def fundadores(R):
    """Copia textual de eco_a_carrera.fundadores (el arnes lo compara en entradas)."""
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


def fund_media(c): return sum(l['fundadores'] for l in c['linajes']) / len(c['linajes'])


def pareado_fund(Ra, Rb):
    """Por semilla: media de 'fundadores' (juez) de los 9 linajes; menos = gana el primero (estricto)."""
    ma = {c['seed']: fund_media(c) for c in Ra}; mb = {c['seed']: fund_media(c) for c in Rb}
    com = sorted(set(ma) & set(mb)); d = [ma[k] - mb[k] for k in com]
    return dict(semillas=len(com), menos=sum(1 for x in d if x < 0), dif_med=(round(float(st.median(d)), 3) if d else None),
                por_semilla={k: [round(ma[k], 2), round(mb[k], 2)] for k in com})


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


def fisica_igual(x, y, nx, ny):
    """Identidad de la salida de dos corridas salvo telemetria de carro, genoma, tiempo, brazo y el nombre del carro en las etiquetas."""
    q = lambda z, n: json.loads(json.dumps({k: v for k, v in z.items() if k not in ('seg', 'tel_eac', 'tel_fc', 'genoma', 'genoma_de', 'brazo')},
                                           default=str).replace(f'"{n}#', '"@#'))
    return q(x, nx) == q(y, ny)


# ------------------------------------------------------------------ LA LETRA (la del muro, sin cambios; hipotesis = HIP, control = CTL)
def lee_serie(res, par, gok, completa, abortos, n=20):
    v = {}
    v['V1_completa'] = bool(completa and abortos == 0 and all(b in res for b in SERIE_BRAZOS)
                            and all(res[b]['coherente'].split('/')[0] == res[b]['coherente'].split('/')[1] for b in SERIE_BRAZOS if b in res))
    v['V2_ancla_O1_gana'] = bool(res.get('o1', {}).get('gana_e5'))
    m = res.get('v143', {}).get('R0_real_med')
    v['V3_ancla_V143'] = m is not None and ANCLA_V143[0] <= m <= ANCLA_V143[1]
    v['V4_genoma_aplicado'] = bool(gok.get(HIP) and gok.get(CTL))
    valido = all(v.values())
    p = {}
    p['P1_hip_cruza'] = bool(res.get(HIP, {}).get('gana_e5'))
    x = par.get((HIP, 'v143')) or {}
    p['P2_hip_gana_v143'] = bool(x.get('semillas') and x['gana'] >= GANA * x['semillas'] / 20)
    p['P3_ctl_no_cruza'] = not bool(res.get(CTL, {}).get('gana_e5'))
    y = par.get((HIP, CTL)) or {}
    mod = bool(p['P2_hip_gana_v143'] and x.get('dif_med') is not None and x['dif_med'] >= DIF_MOD - 1e-12
               and y.get('semillas') and y['gana'] > 10 * y['semillas'] / 20)
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif mod: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    return dict(validez=v, puertas=p, modesto=mod, veredicto=ver)


def criterio_explora(par, pf, hip, ctl, base):
    a = par.get((hip, base)) or {}; b = par.get((hip, ctl)) or {}; f = pf.get((hip, base)) or {}
    c1 = bool(a.get('semillas') and a['gana'] >= EXPL_MIN * a['semillas'] / 10)
    c2 = bool(b.get('semillas') and b['gana'] >= EXPL_MIN * b['semillas'] / 10)
    c3 = bool(f.get('semillas') and f['menos'] >= EXPL_MIN * f['semillas'] / 10)
    return dict(hip=hip, ctl=ctl, base=base, C1_R0_gana_base=c1, C2_R0_gana_ctl=c2, C3_menos_fundadores=c3, PASA=bool(c1 and c2 and c3),
                detalle=dict(r0_vs_base=f"{a.get('gana')}/{a.get('semillas')}", r0_vs_ctl=f"{b.get('gana')}/{b.get('semillas')}",
                             fund_vs_base=f"{f.get('menos')}/{f.get('semillas')}"))


PAR = (('ingv', 'v143'), ('ingv', 'azav'), ('azav', 'v143'), ('ing', 'g0'), ('ing', 'aza'), ('g0', 'v143'), ('ing', 'v143'),
       ('selc', 'g0'), ('ingv', 'selc'), ('o1', 'v143'), ('o1', 'ingv'))
PARF = (('ingv', 'v143'), ('ingv', 'azav'), ('ing', 'g0'), ('ing', 'aza'), ('selc', 'g0'), ('g0', 'v143'))


def resume_carpeta(R, brazos, semillas, log, completa, abortos, humo):
    por = {b: sorted([x for x in R if x['brazo'] == b and not x['aborto']], key=lambda z: z['seed']) for b in brazos}
    res = {}; fz = {}; es = {}; gok = {}
    for b in [x for x in brazos if por.get(x)]:
        res[b] = CV.resume(por[b], b, log); fz[b] = fundadores(por[b]); es[b] = FC.establece(por[b]); gok[b] = genoma_ok(por[b], b)
        log(f"  FUNDADORES ({b}): {fz[b]}")
        log(f"  ESTABLECIMIENTO ({b}, descriptivo): {es[b]} · genoma aplicado (V4): {gok[b]}")
    par = {k: CV.pareado(por[k[0]], por[k[1]]) for k in PAR if por.get(k[0]) and por.get(k[1])}
    pf = {k: pareado_fund(por[k[0]], por[k[1]]) for k in PARF if por.get(k[0]) and por.get(k[1])}
    log("\nPAREADOS R0 real (por semilla: mediana de los 9 linajes; gana = semillas en que el primero supera al segundo)")
    for k, v in par.items(): log(f"  {k[0]} vs {k[1]}: gana {v['gana']}/{v['semillas']} · diferencia mediana {v['dif_med']}")
    log("PAREADOS FUNDADORES (por semilla: media de los 9 linajes; menos = semillas en que el primero necesita MENOS)")
    for k, v in pf.items(): log(f"  {k[0]} vs {k[1]}: menos {v['menos']}/{v['semillas']} · diferencia mediana {v['dif_med']} · {v['por_semilla']}")
    p1 = {b: f"{res[b]['sem_cruza_e5']}/{res[b]['semillas']}" for b in res}
    log(f"  P1 (semillas con la mayoria de linajes cruzando con R0 real): {p1}")
    iden = None
    x = [c for c in por.get('g0v', []) if c['seed'] in {z['seed'] for z in por.get('v143', [])}]
    if x:
        iden = {c['seed']: fisica_igual(c, [z for z in por['v143'] if z['seed'] == c['seed']][0], 'EIC_G0V', 'V143') for c in x}
        log(f"  IDENTIDAD LARGA (instrumento): g0v (EIC_G0V + G0) == v143 salvo telemetria/etiquetas, por semilla: {iden}")
    letra = lee_serie(res, par, gok, completa, abortos)
    ce = criterio_explora(par, pf, 'ingv', 'azav', 'v143')
    ce2 = criterio_explora(par, pf, 'ing', 'aza', 'g0')
    log(f"\n  LETRA DEL MURO sobre la primaria (con n < 20 las puertas escalan GANA*n/20 y NO cuenta): {letra}")
    log(f"  CRITERIO EXPLORATORIO PRIMARIA (decide si se escribe el preregistro): {ce}")
    log(f"  criterio en la secundaria (con familia; NO decide): {ce2}")
    return dict(brazos=res, fundadores=fz, establece=es, genoma_aplicado=gok, pareados={f"{k[0]}_vs_{k[1]}": x for k, x in par.items()},
                pareados_fund={f"{k[0]}_vs_{k[1]}": x for k, x in pf.items()}, P1=p1, identidad_larga=iden,
                letra=letra, criterio_explora=ce, criterio_secundaria=ce2, semillas=semillas, abortos=abortos, humo=humo)


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for c, sha in SHA_GEN.items():
        if sha is None: log(f"  genomas_ing_{c}.json: sha no fijado (no se usa en este modo)"); continue
        s = h16(GEN_ING[c]); ok &= s == sha; log(f"  sha genomas_ing_{c}.json {s} {'OK' if s == sha else 'FALLA'}")
    for n, b in CI.todas().items():
        ruta = os.path.join(CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = RC.revisa_fuente(b.decode('utf-8'), n) if igual else ['distinto de construye_eco_ing_a_carrera']
        ok &= igual and not vr
        log(f"  carro {n} sha {CI.h16b(b)} == construye: {igual} · revisa_carro: {'PASA' if not vr else vr[:2]}")
    registra(); FC.registra()
    N = lambda x: json.loads(json.dumps(x, default=str))
    a = P.run(39561, [('C', CV._MODS['V143_RES0'])] * 9, T=2000, fundador_limpio=1)
    m = CV._MODS['EIC_G0']; m.GENOMA = None
    b = P.run(39561, [('C', m)] * 9, T=2000, fundador_limpio=1)
    i1 = N(a) == N(b); ok &= i1
    log(f"  IDENTIDAD CORTA: EIC_G0 con GENOMA None == V143_RES0 de frio_carrera (salida ENTERA, N 9, s 39561, T 2000): {'OK' if i1 else 'FALLA'}")
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
        registra()
        carpeta = a.lee
        R = [json.load(open(os.path.join(carpeta, f), encoding='utf-8')) for f in sorted(os.listdir(carpeta))
             if f.endswith('.json') and '_s' in f and not f.startswith('resumen')]
        brazos = [b for b in BRAZOS if any(x['brazo'] == b for x in R)]
        semillas = sorted({x['seed'] for x in R}); abortos = sum(1 for x in R if x['aborto'])
        LOGF = open(os.path.join(carpeta, 'lee.txt'), 'w', encoding='utf-8')

        def log(s=''):
            print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        log(f"LEE {carpeta} · {len(R)} corridas · brazos {brazos} · semillas {semillas} · abortos {abortos}")
        completa = all(sum(1 for x in R if x['brazo'] == b) == len(semillas) for b in brazos if b != 'g0v')
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
        if not sem or not all(s in EXPLORA for s in sem): raise SystemExit("--explora: --semillas dentro de 39461-39470")
        brazos = [s for s in (a.brazos or ','.join(EXPLORA_BRAZOS)).split(',') if s]
        if any(b not in EXPLORA_BRAZOS for b in brazos): raise SystemExit(f"--explora: brazos en {EXPLORA_BRAZOS}")
        tareas = [(s, b) for s in sem for b in brazos if b != 'g0v' or s == 39461]; dest = DATOS
    else:
        T = a.T or T_DEF; desde = a.desde; n = a.n or 20
        sem = list(range(desde, desde + n)) if desde else []
        if not sem or not (all(s in SERIE for s in sem) or all(s in REPLICA for s in sem)): raise SystemExit("--serie: 39511-39530 o 39531-39550")
        if T != T_DEF: raise SystemExit("--serie: T = 100000")
        tareas = [(s, b) for b in SERIE_BRAZOS for s in sem]; dest = DATOS
    if len(tareas) > 6 and a.humo: raise SystemExit("--humo: maximo 6 corridas")
    semillas = sorted({s for s, _ in tareas}); brazos = [b for b in BRAZOS if any(b == x for _, x in tareas)]
    sel_ = time.strftime('%Y%m%d_%H%M%S')
    if a.carpeta: carpeta = a.carpeta
    elif a.humo: carpeta = os.path.join(dest, f"eic_humo_s{semillas[0]}-{semillas[-1]}_T{T}_{sel_}")
    elif a.explora: carpeta = os.path.join(dest, f"eic_explora_s39461-39470_T{T}")
    else: carpeta = os.path.join(dest, f"eic_{'serie' if semillas[0] in SERIE else 'replica'}_s{semillas[0]}-{semillas[-1]}_T{T}")
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, f"log_{sel_}_{os.getpid()}.txt"), 'a', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time()
    modo = 'humo' if a.humo else ('explora' if a.explora else 'serie')
    log(f"CORRE_ECO_ING_A_CARRERA · {modo} · {sel_} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · "
        f"corre_eco_ing_a_carrera.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  tareas {len(tareas)} · brazos {brazos} · semillas {semillas} · T {T} · fundador limpio 1 · reanuda {a.reanuda}")
    ok = verifica(log)
    if a.humo:
        ok &= CV.verifica_todo(log, con_entrada=True)   # regla 14 de corre_v143: corre_v143.tarea == juez.tarea
        N = lambda x: json.loads(json.dumps(x, default=str))
        x = tarea((39561, 'v143', 2000)); y = CV.tarea((39561, 'V143', 2000))
        e14 = (x.pop('tel_eac') == [None] * 9 and x.pop('tel_fc') == [None] * 9 and x.pop('genoma') is None and x.pop('genoma_de') is None
               and N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in y.items() if k != 'seg'}))
        ok &= e14; log(f"  ENTRADA campo a campo (regla 14): tarea de este runner == corre_v143.tarea (V143, s 39561, T 2000): {'OK' if e14 else 'FALLA'}")
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
