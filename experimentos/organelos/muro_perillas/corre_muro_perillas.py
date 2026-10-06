"""corre_muro_perillas.py — RUNNER del bloque "PERILLAS DEL MURO" (1-oct-2026, ingeniero genetico). Dos pasos:
  PASO 1 (--mapa): EL MAPA. En la pista vieja, con GENOMAS FIJOS y sin evolucion, ¿cuanto paga cada mecanismo de O1 desde APAGADO?
          Carro O1_MURO_GEN (construye_muro_perillas.py) con 6 dosis: 0 = mecanismo neutralizado, 1 = O1 de fabrica.
  PASO 2 (--serie/--replica): "perillas del muro": los genes desde apagado, con el montaje de perillas (camara continua, una mutacion
          por parto en un gen, sesgo a la perdida, 5 pasajes de 100k, siembra de establecidos, dos relojes), SOLO si el mapa muestra
          pendiente o valle de un paso (PREREGISTRO_muro_perillas.md). GEN_LETRA se fija tras el mapa; sin el, --serie se niega.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE SE CORRE: cada corrida ES experimentos/tronco_v14_3/corre_v143.tarea (regla 14; se IMPORTA por sha) con pista.run de la pista
vieja (9f47c65e438e0ff4) y juez.resumen_linaje (6a68f640a7832f12): monocultivo de 9 O1_MURO_GEN, L 360, 36 objetos, fundador
limpio 1, pizarra 1, T 100 000. Medidas por corrida: linajes que cruzan (cruza_real del juez) de 9, R0 real mediano de los 9,
fundadores por linaje, establecidos (0 fundadores tras t = 10 000), mayoria, mundo A+C, mordidas, causas.
GENOMAS del mapa (etiquetas, valores CRUDOS): fab (O1) · off (APAGADO provisional del constructor) · 'K=v[+K=v]' sobre fab ·
'off+K=v' sobre off · 'mix:8xPISO=0.2+1xPISO=0.6' = PISTA MIXTA (cada linaje con su genoma fijo; se reporta por linaje quien cruza y quien paga).
SEMILLAS NUEVAS 883xxx (grep 1-oct en .py/.md: no aparecen): mapa 883001-883010 (semillas s1 = 883001, s2 = 883002) · arnes
883950-883959 · humo 883990-883998 · serie: pasaje p de la cadena i -> 883100 + 10 i + p; prueba de i -> 883301 + i ·
replica: 883500 + 10 i + p; prueba 883701 + i.
REGLA DE CPU (encargo): un solo proceso, <= 6 corridas de <= 200 000 pasos por proceso en --humo/--mapa; antes de correr el runner
cuenta los python de trabajo y se NIEGA si hay 6 o mas (--forzar_cpu lo salta SOLO para el coordinador).

  python experimentos/organelos/muro_perillas/corre_muro_perillas.py --humo                       # 1 proceso: off y fab a T 2000 + regla 14; escribe JSON
  python experimentos/organelos/muro_perillas/corre_muro_perillas.py --mapa --lote A              # lotes A..F (<= 6 corridas de 100k cada uno)
  python experimentos/organelos/muro_perillas/corre_muro_perillas.py --mapa --genomas off,fab --seed 883001 [--T 100000]
  python experimentos/organelos/muro_perillas/corre_muro_perillas.py --lee                        # la tabla del mapa (datos/mapa)
  python experimentos/organelos/muro_perillas/corre_muro_perillas.py --serie --pool 2 [--reanuda]  (SOLO el coordinador; PASO 2)
"""
import argparse, copy, glob, hashlib, importlib.util, json, math, os, platform, statistics as st, subprocess, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
TR = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3'); PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, TR, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV      # se IMPORTA (sha fijado): la corrida ES CV.tarea
import construye_muro_perillas as CB
P = CV.P; J = CV.J
_ORIG_RUN = P.run

PRERREGISTRO = 'PREREGISTRO_muro_perillas.md'
DATOS = os.path.join(AQUI, 'datos')
CARRO = 'O1_MURO_GEN'
CARROS = {n: os.path.join(AQUI, 'carros', n + '.py') for n, _ in CB.VARIANTES}
SHAS = {os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028', os.path.join(PISTA, 'carros', 'CTRL_O1_SINLIMPIA.py'): 'be029b0a1b8d6634',
        os.path.join(TR, 'corre_v143.py'): '24100621c450da22'}
SHAS_PROPIOS = {'construye_muro_perillas.py': '1120f56ea5dc2c0f', os.path.join('carros', 'O1_MURO_GEN.py'): '83e7fe2a5eb9efd4', os.path.join('carros', 'O1_MURO_GEN0.py'): 'e6be23e6a74718a6'}   # FIJADOS 5-oct 18:15 (PS_TOPE, brazo pur); si cambian, la serie no corre
GENES = CB.GENES; BASE = dict(zip(GENES, CB.BASE)); DISENO = dict(zip(GENES, CB.DISENO)); SIGMA = CB.SIGMA; DELTA = CB.DELTA
CADENAS = ('sel', 'neu', 'pur'); LEE_CADENA = {'sel': 1, 'neu': 0, 'pur': 1}
TOPE_PUR = 0.045   # brazo pur (5-oct, tras ERR-192): el cuerpo lee min(MARGEN, 0.045): por encima del arranque (0.03: 4/18) y por debajo de la zona que cruza (0.06: 11-15/18)
TOPE_CADENA = {'sel': None, 'neu': None, 'pur': TOPE_PUR}   # las PRUEBAS leen SIN tope (tambien la de pur: ¿cruza su gen heredado?)
ORDEN = ('sel', 'neu', 'pur', 'fab', 'off'); CAND = 'sel'; NEU = 'neu'; PUR = 'pur'; TECHO = 'fab'; PISO_B = 'off'
BASES = {'serie': (883100, 883301), 'replica': (883500, 883701), 'humo': (883990, 883998), 'mapa': (883001, 883001), 'arnes': 883950}
SEM_MAPA = (883001, 883002)
N_IND = 20; NPAS = 5; T_PAS = 100000; T_PRU = 100000; VENT = 5000; POOL_MAX = 3   # pool 3 (5-oct): un trabajador por brazo de cadena; el PC es solo para esto
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000; CPU_TOPE = 6
# ------------------------------------------------------------------ constantes de la LETRA del PASO 2 (se FIJAN tras el mapa, en el preregistro)
GEN_LETRA = 'MARGEN'   # PASO B (5-oct): el gen de la letra = el margen de la boca de O1 (el mapa: rampa 0/0, 0/4, 3/8, 8/9 en 0, .03, .06, .10; fab 4/8)
MARGEN_G = 0.03        # PG: MARGEN mediano de la siembra final de sel > el de neu + 0.03. Nulo de ESTE gen (nulo_margen.py): mediana neutra ~0.007-0.010,
                       #     P(sel > neu + 0.03) por cadena bajo el nulo 0.05-0.06 -> P(>= 13/20) ~1e-11; 0.03 es ademas el primer escalon medido de la rampa
FUNC_MARGEN = 0.06     # descriptivo: zona FUNCIONAL de la rampa (0.06 -> 11/18 linajes; 0.10 -> 17/18); se reporta cuantas cadenas sel llegan
FL_SERIE = 1           # fundador_limpio de la serie: 1 = canonico del muro (ENMIENDA 5: r2o1mono, corre_v143 FL 1, o1_evo, termostato). PASO A decide si se cambia
MAYORIAS_MURO = 16     # frase maxima solo si sel alcanza mayoria (>= 5/9 cruzan) en >= 16/20 pruebas, como O1 (18-20/20)
MUTA_SERIE = CB.MUTA   # auditoria (punto 3): en la serie SOLO MARGEN muta (sel y neu); los otros cinco genes quedan en fabrica. (0,1,2,3,4,5) = los seis
CONSERVA = 'CONSERVA, NO SUBE'   # auditoria (B-1): PG (a) pasa pero (b) no: la seleccion impide que el margen caiga a 0; no lo sube. No es MODESTO; replica solo si (b) a +-1
TRINQUETE = 'TRINQUETE'          # (5-oct, ERR-192): sel llega a la zona funcional pero sel ~ pur: la seleccion purificadora y la deriva lo llevan; no hay evidencia de gradiente
MARGEN_GR = 0.02                 # puerta de GRADIENTE: MARGEN final de sel > pur + 0.02 en >= 13/20 pareado. Nulo (nulo_margen.py (5)): sel y pur intercambiables sin gradiente
GANA_PAR = 13; DIF_SUMA = 10; FAB_GANA = 16; PROF_MIN = 30; REFUND_MIN = 3000; RELOJ_CAD = 16   # los de perillas (a priori)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sin_ids(o, de=CARRO):
    """json del objeto con el NOMBRE del carro en los ids de linaje reemplazado por 'O1' (regla 14: los ids llevan el nombre del carro)."""
    return json.dumps(o, default=str, sort_keys=True).replace(de + '#', 'O1#').replace('"' + de + '"', '"O1"')
def sem_pas(base, i, p): return base[0] + 10 * i + p
def sem_pru(base, i): return base[1] + i
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None
def esc(k, n): return math.ceil(k * n / 20 - 1e-9)


def python_de_trabajo():
    """Regla de CPU del encargo (tope 6): python.exe ajenos a este proceso que TRABAJAN = trabajadores de Pool (multiprocessing-fork) +
    procesos sin Pool; los padres de un Pool (ociosos: esperan a sus hijos) no cuentan. Devuelve (de_trabajo, totales)."""
    try:
        ps = ("Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | ForEach-Object { '{0}|{1}' -f $_.ProcessId, $_.CommandLine }")
        out = subprocess.run(['powershell', '-NoProfile', '-Command', ps], capture_output=True, text=True).stdout
        filas = [l.split('|', 1) for l in out.splitlines() if '|' in l]
        filas = [(int(p), c or '') for p, c in filas if int(p) != os.getpid()]
        padres = {int(c.split('parent_pid=')[1].split(',')[0]) for p, c in filas if 'parent_pid=' in c}
        trabajo = [p for p, c in filas if p not in padres]
        return len(trabajo), len(filas)
    except Exception:
        return -1, -1


# ------------------------------------------------------------------ estado por proceso
def fija():
    ruta = CARROS[CARRO]
    if open(ruta, 'rb').read() != CB.todas()[CARRO]: raise SystemExit(f"{ruta} != construye_muro_perillas (correr construye_muro_perillas.py)")
    m = CV._MODS.get(CARRO)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{CARRO}", ruta)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[CARRO] = m
    if m.PERILLAS != 1: raise SystemExit(f"{CARRO}: PERILLAS {m.PERILLAS} != 1")
    return dict(carro=CARRO, sha=h16(ruta), PERILLAS=m.PERILLAS, PS_BASE=list(m.PS_BASE), PS_APAGADO=list(m.PS_APAGADO), PS_FABRICA=list(m.PS_FABRICA))


def _pon(m, siembra, seed, sigma, delta, lee, camara, por_linaje=None, muta=None, tope=None):
    m.SIEMBRA = copy.deepcopy(siembra); m.PS_SEMILLA = int(seed); m.PS_SIGMA = float(sigma); m.PS_DELTA = float(delta); m.PS_LEE = int(lee); m.PS_CAMARA = int(camara)
    m.PS_MUTA = tuple(int(j) for j in (muta if muta is not None else MUTA_SERIE)); m.PS_TOPE = (None if tope is None else float(tope))
    m.PS_POR_LINAJE = copy.deepcopy(por_linaje)
    m._TEL.clear(); m._PS_CNT.clear(); m._VIVO.clear()


def _quita(m): _pon(m, None, 0, SIGMA, DELTA, 1, 1, None, CB.MUTA, None)


def tarea(seed, T, siembra=None, sigma=SIGMA, lee=1, delta=DELTA, camara=1, por_linaje=None, fl=1, muta=None, tope=None):
    """corre_v143.tarea tal cual (regla 14) + 'tel_ps' (copia de _TEL del carro, solo lectura) + 'estado' (perillas de ESTE proceso).
    por_linaje = lista de 9 genomas (listas de 6) para la PISTA MIXTA (cada linaje con el suyo, fijo)."""
    est = fija(); m = CV._MODS[CARRO]
    _pon(m, siembra, seed, sigma, delta, lee, camara, por_linaje, muta, tope)
    est.update(sigma=float(sigma), delta=float(delta), camara=int(camara), siembra_n=len(siembra or []), lee=int(lee), por_linaje=(por_linaje is not None), fl=int(fl), muta=list(m.PS_MUTA), tope=m.PS_TOPE)
    fl0 = CV.FL; CV.FL = int(fl)   # PASO A (5-oct): fundador_limpio por corrida; corre_v143.tarea lee su global FL en cada llamada; se restaura siempre
    try:
        x = CV.tarea((seed, CARRO, T))
        tel = copy.deepcopy({str(i): v for i, v in m._TEL.items()})
    finally:
        _quita(m); CV.FL = fl0
    if x['pista']['fundador_limpio'] != int(fl): raise RuntimeError(f"fundador_limpio {x['pista']['fundador_limpio']} != {fl}")
    x.pop('pizarra_log', None); x.pop('tel', None)
    x['tel_ps'] = tel; x['estado'] = est
    return x


def fila(x, T):
    """Fisica del juez por corrida (9 linajes) + lo de los genes (telemetria de solo escritura)."""
    L = x['linajes']; tel = x.get('tel_ps') or {}
    fp = [q for v in tel.values() for q in (v or {}).get('fund', [])]
    viv = [g for v in tel.values() for t, g, c, pr in (v or {}).get('vivos', []) if t >= T - VENT]
    prs = [pr for v in tel.values() for t, g, c, pr in (v or {}).get('vivos', []) if t >= T - VENT]
    cz = {k: sum(l['causas'][k] for l in L) for k in ('hambre', 'sed', 'veneno', 'sal')}
    cm = x['pista']['comp_mundo']
    gl = {int(i): ((v or {}).get('fund') or [[None, None]])[0][1] for i, v in tel.items()}
    return dict(seed=x['seed'], seg=x['seg'], cruzan=sum(l['cruza_real'] for l in L), mayoria=int(sum(l['cruza_real'] for l in L) * 2 > len(L)),
                por_linaje=[dict(i=i, genes=gl.get(i), cruza=int(l['cruza_real']), R0_real=l['R0_real'], fund=l['fundadores'], fund_post10k=l['fund_post10k'],
                                 mord_BD=l['mord']['B'] + l['mord']['D'], mord_AC=l['mord']['A'] + l['mord']['C'], muertes=l['muertes'],
                                 limpiezas=(l.get('diag') or {}).get('limpiezas')) for i, l in enumerate(L)],
                R0_med=med([l['R0_real'] for l in L]), R0_real=[l['R0_real'] for l in L], fund=[l['fundadores'] for l in L], fund_med=med([l['fundadores'] for l in L]),
                fund_post10k=[l['fund_post10k'] for l in L], establecidos=sum(1 for l in L if l['fund_post10k'] == 0), persisten=sum(l['persiste'] for l in L),
                evaluables=sum(l['evaluable'] for l in L), muertes=[l['muertes'] for l in L], vida_med=med([l['vida_med'] for l in L]),
                causas=cz, mord_BD=med([l['mord']['B'] + l['mord']['D'] for l in L]), mord_AC=med([l['mord']['A'] + l['mord']['C'] for l in L]),
                mundo_AC=round(cm['A'] + cm['C'], 4), frac_sin_bueno=x['pista']['frac_sin_bueno_mundo'],
                coherente=all(l['coherente'] for l in L) and all(l['t_fund_rec_ok'] for l in L),
                fund_de_siembra=sum(int(q[0] == 1) for q in fp), fund_de_camara=sum(int(q[0] == 2) for q in fp), fund_de_base=sum(int(q[0] == 0) for q in fp),
                fund_n=len(fp), partos_tel=sum((v or {}).get('partos', 0) for v in tel.values()), prof_vivos_fin=med(prs),
                fund_genes_distintos=len({tuple(q[1]) for q in fp}), fund_gen0=(dict(zip(GENES, fp[0][1])) if fp else None),
                genes_vivos_fin={k: med([g[j] for g in viv]) for j, k in enumerate(GENES)} if viv else None, estado=x.get('estado'))


# ------------------------------------------------------------------ PASO 1: EL MAPA (genomas fijos)
def genoma(etq):
    """fab (O1) · off (APAGADO provisional) · 'K=v[+K=v]' sobre fab · 'off+K=v[+K=v]' sobre off. Valores CRUDOS (MARGEN 0.03, PISO 1.0...)."""
    if etq == 'off': return dict(zip(GENES, CB.APAGADO))   # el apagado del mapa (genetista)
    if etq == 'base': return dict(BASE)                     # el arranque de la serie (PASO B)
    if etq == 'fab': return dict(DISENO)
    # (5-oct 16:30, corregido: 'off+' usaba BASE, que ese dia paso a ser el ARRANQUE de la serie; los 12 JSON fl0 del lote D de las 15:48-16:17 quedaron mal
    #  etiquetados y se apartaron a datos/mapa/invalidos_etiqueta_fl0_D/. 'off+' = sobre APAGADO (genetista); 'base+' = sobre BASE (arranque de la serie).)
    partes = etq.split('+'); g = dict(zip(GENES, CB.APAGADO)) if partes[0] == 'off' else (dict(BASE) if partes[0] == 'base' else dict(DISENO))
    for q in (partes[1:] if partes[0] in ('off', 'base') else partes):
        k, v = q.split('='); k = k.strip()
        if k not in GENES: raise SystemExit(f"gen desconocido {k!r} en {etq!r}")
        g[k] = float(v)
    return g


def mixta(etq):
    """'mix:8xPISO=0.2+1xPISO=0.6' -> 9 genomas por linaje (los primeros indices llevan la primera parte)."""
    out = []
    for q in etq[4:].split('+'):
        n, e = q.split('x', 1); out += [genoma(e)] * int(n)
    if len(out) != 9: raise SystemExit(f"mixta {etq!r}: {len(out)} linajes (se exigen 9)")
    return out


# LOTES del mapa (<= 6 corridas de 100k por proceso). Rejilla del genetista (FABLE_gen_perdido.md ficha 1) acotada a un proceso:
#   A: eje MARGEN (acantilado?) · B: eje PISO + un punto de PEN_OTRO y de PRUEBA · C: reglas (LIMPIA, HUECO), pares MARGEN x PISO y todo apagado
#   M: PISTA MIXTA (bien publico: quien limpia paga, los vecinos cobran) · A2/B2/C2: segunda semilla
LOTES = {'A': ['MARGEN=0.0', 'MARGEN=0.03', 'MARGEN=0.06', 'MARGEN=0.1', 'fab', 'MARGEN=0.5'],
         'B': ['PISO=0.0', 'PISO=0.4', 'PISO=0.6', 'PISO=1.0', 'PEN_OTRO=1.0', 'PRUEBA=0.0'],
         'C': ['LIMPIA=0', 'HUECO=0', 'MARGEN=0.1+PISO=0.6', 'MARGEN=0.06+PISO=0.4', 'MARGEN=0.1+PISO=1.0', 'off'],
         'M': ['mix:8xPISO=0.2+1xPISO=0.6', 'mix:8xPISO=0.6+1xPISO=0.2', 'mix:8xfab+1xLIMPIA=0', 'mix:8xLIMPIA=0+1xfab'],
         'X': ['LIMPIA=0', 'fab'],   # PASO A: los dos clonales que deciden, con --fl 0
         'D': ['off+MARGEN=0.25', 'off+PISO=0.2', 'off+LIMPIA=1', 'off+MARGEN=0.25+PISO=0.2', 'off+MARGEN=0.25+LIMPIA=1+PISO=0.2', 'off+MARGEN=0.25+LIMPIA=1+PISO=0.2+PEN_OTRO=0.35']}
LOTE_SEM = {k: 883001 for k in LOTES}
for _k in list(LOTES):   # la segunda semilla: A2..M2
    LOTES[_k + '2'] = list(LOTES[_k]); LOTE_SEM[_k + '2'] = 883002


def corrida_fija(etq, seed, T, carpeta, log, fl=1):
    fin = os.path.join(carpeta, f"fijo_{etq.replace(':', '-').replace('=', '')}_s{seed}_T{T}{'' if fl == 1 else '_fl' + str(fl)}.json")   # fl 1: los nombres del 1-oct, intactos
    if os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x = json.load(fh)
        if not x.get('aborto'): log(f"  (ya estaba) {etq} s{seed}: cruzan {x['cruzan']}/9 R0 {x['R0_med']}"); return x
    es_mix = etq.startswith('mix:'); t0 = time.time()
    g = None if es_mix else genoma(etq); pl = [[q[k] for k in GENES] for q in mixta(etq)] if es_mix else None
    try:
        if es_mix: y = tarea(seed, T, siembra=None, sigma=0.0, lee=1, delta=0.0, camara=0, por_linaje=pl, fl=fl)   # cada linaje con SU genoma fijo
        else: y = tarea(seed, T, siembra=[g], sigma=0.0, lee=1, delta=0.0, camara=0, fl=fl)   # genoma FIJO: sin mutacion, sin camara
        x = dict(tipo='fijo', etq=etq, genoma=g, genomas_linaje=pl, aborto=None, **fila(y, T))
        # (5-oct 16:40) el genoma que LEYO el carro (telemetria del primer fundador) debe ser EL pedido; si no, la corrida es un aborto con la prueba que lo cazo
        leido = x['fund_gen0']; pedido = (g if not es_mix else dict(zip(GENES, pl[0])))
        x['genoma_ok'] = bool(leido == pedido and x['fund_genes_distintos'] == (1 if not es_mix else len({tuple(q) for q in pl})))
        if not x['genoma_ok']: x['aborto'] = f"GENOMA LEIDO {leido} != PEDIDO {pedido} (etiqueta {etq})"
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo='fijo', etq=etq, genoma=g, genomas_linaje=pl, seed=seed, aborto=f"{type(e).__name__}: {e}"[:300])
    x['seg'] = round(time.time() - t0, 1); x['T'] = T; x['fl'] = int(fl)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    if x['aborto']: log(f"  [{x['seg']}s] {etq} s{seed} ABORTO {x['aborto']}")
    else:
        log(f"  [{x['seg']}s] {etq} s{seed} fl{fl} genoma {g if g else 'MIXTA'} · cruzan {x['cruzan']}/9 mayoria {x['mayoria']} R0 real med {x['R0_med']} fund med {x['fund_med']} estab {x['establecidos']}/9 "
            f"· vida {x['vida_med']} · causas {x['causas']} · B+D {x['mord_BD']} A+C {x['mord_AC']} · mundo AC {x['mundo_AC']} sin bueno {x['frac_sin_bueno']} · coherente {x['coherente']}")
        if es_mix:
            for q in x['por_linaje']: log(f"      linaje {q['i']} genes {q['genes']} cruza {q['cruza']} R0 {q['R0_real']} fund {q['fund']} B+D {q['mord_BD']} A+C {q['mord_AC']} limpiezas {q['limpiezas']}")
    return x


def lee_mapa(carpeta, log=print):
    R = {}
    for f in sorted(glob.glob(os.path.join(carpeta, 'fijo_*.json'))):
        x = json.load(open(f, encoding='utf-8'))
        if x.get('aborto'): log(f"  ABORTO {f}: {x['aborto']}"); continue
        R.setdefault(x['etq'] + ('' if x.get('fl', 1) == 1 else f" (fl {x['fl']})"), {})[x['seed']] = x
    orden = [e + suf for suf in ('', ' (fl 0)') for k in sorted(LOTES) if not k.endswith('2') for e in LOTES[k]] + sorted(R)
    orden = [e for j, e in enumerate(orden) if e in R and e not in orden[:j]]
    log(f"MAPA (genomas fijos, pista vieja, 9 linajes por corrida, T {next(iter(next(iter(R.values())).values()))['T'] if R else '?'}) · {carpeta}")
    log(f"  {'genoma':26s} {'semillas':>9} {'cruzan/9 por semilla':>22} {'suma':>5} {'R0 real med':>12} {'fund med':>9} {'estab':>7} {'vida':>6}  causas h/s/v/sal  B+D  A+C  mundoAC")
    for k in orden:
        if k not in R: continue
        xs = [R[k][s] for s in sorted(R[k])]
        cz = {c: sum(x['causas'][c] for x in xs) for c in ('hambre', 'sed', 'veneno', 'sal')}
        log(f"  {k:26s} {str(sorted(R[k])):>9} {str([x['cruzan'] for x in xs]):>22} {sum(x['cruzan'] for x in xs):>5} {str(med([x['R0_med'] for x in xs])):>12} "
            f"{str(med([x['fund_med'] for x in xs])):>9} {str([x['establecidos'] for x in xs]):>7} {str(med([x['vida_med'] for x in xs])):>6}  "
            f"{cz['hambre']}/{cz['sed']}/{cz['veneno']}/{cz['sal']}  {med([x['mord_BD'] for x in xs])}  {med([x['mord_AC'] for x in xs])}  {med([x['mundo_AC'] for x in xs])}")
        if k.startswith('mix:'):
            for x in xs:
                for q in x['por_linaje']: log(f"      s{x['seed']} linaje {q['i']} genes {q['genes']} cruza {q['cruza']} R0 {q['R0_real']} fund {q['fund']} B+D {q['mord_BD']} A+C {q['mord_AC']} limpiezas {q['limpiezas']}")
    return R


# ------------------------------------------------------------------ PASO 2: cadenas (el montaje de perillas, generico en los genes)
def siembra(tel, T, vent=VENT):
    cand = {}
    for i in sorted(tel or {}, key=lambda z: int(z)):
        vv = (tel[i] or {}).get('vivos', [])
        fin = [(g, pr) for t, g, c, pr in vv if t >= T - vent]
        if not fin: continue
        cand[int(i)] = (len({c for t, g, c, pr in vv if t >= T // 2}), fin)
    if not cand: return None, dict(n_est=0, respaldo=True, idx=[], n=0)
    est = [i for i in cand if cand[i][0] == 1]
    idx = est if est else [i for i in cand if cand[i][0] == min(v[0] for v in cand.values())]
    out = [dict({k: float(v) for k, v in zip(GENES, g)}, prof=int(pr)) for i in idx for g, pr in cand[i][1]]
    return (out or None), dict(n_est=len(est), respaldo=bool(not est), idx=idx, n=len(out))


def genoma_mediano(sie):
    return {k: float(st.median([s[k] for s in sie])) for k in GENES} if sie else None


def prof_de(sie): return float(st.median([s['prof'] for s in sie])) if sie else None


def cadena(i, base, npas, T, carpeta, reanuda, brazo, log=None):
    sie = None; F = []; lee = LEE_CADENA[brazo]
    for p in range(npas):
        fin = os.path.join(carpeta, f"pasaje_i{i:02d}_{brazo}_p{p:02d}.json")
        if reanuda and os.path.exists(fin):
            with open(fin, encoding='utf-8') as fh: d = json.load(fh)
        else:
            x = tarea(sem_pas(base, i, p), T, siembra=sie, sigma=SIGMA, lee=lee, delta=DELTA, camara=1, fl=FL_SERIE, tope=TOPE_CADENA[brazo])
            sig, info = siembra(x['tel_ps'], T)
            f = fila(x, T); gm = genoma_mediano(sig)
            f.update(p=p, sembrado=int(sie is not None), moneda=info, prof=prof_de(sig), genes_siembra=({k: round(v, 4) for k, v in gm.items()} if gm else None),
                     frac_on=(round(sum(1 for s in sig if s[GEN_LETRA] > MARGEN_G) / len(sig), 3) if (sig and GEN_LETRA) else None))
            d = dict(fila=f, siembra_sig=sig)
            tmp = fin + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as fh: json.dump(d, fh, ensure_ascii=False)
            os.replace(tmp, fin)
        F.append(d['fila']); sie = d['siembra_sig']
        if log: log(f"    cadena i{i} {brazo} p{p} s{d['fila']['seed']} cruzan {d['fila']['cruzan']}/9 moneda {d['fila']['moneda']} prof {d['fila']['prof']} refund camara {d['fila']['fund_de_camara']} genes {d['fila']['genes_siembra']}")
        if not sie: raise RuntimeError(f"pasaje {p}: siembra vacia")
    return dict(pasajes=F, siembra_final=sie, genoma_final=genoma_mediano(sie), prof_final=prof_de(sie), refund_camara=sum(q['fund_de_camara'] for q in F),
                partos=sum(q['partos_tel'] for q in F))


def genoma_de(brazo, i, carpeta):
    if brazo == TECHO: return dict(DISENO)
    if brazo == PISO_B: return dict(BASE)
    with open(os.path.join(carpeta, f"cadena_i{i:02d}_{brazo}.json"), encoding='utf-8') as fh: c = json.load(fh)
    if c.get('aborto') or not c.get('genoma_final'): raise RuntimeError("cadena sin genoma final")
    return c['genoma_final']


def trabajo(args):
    tipo, i, brazo, base, npas, T_pas, T_pru, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{tipo}_i{i:02d}_{brazo}.json"); previo = None
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
        previo = x0['aborto']
    t0 = time.time()
    try:
        if tipo == 'cadena':
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, **cadena(i, base, npas, T_pas, carpeta, reanuda, brazo))
        else:
            g = genoma_de(brazo, i, carpeta)
            y = tarea(sem_pru(base, i), T_pru, siembra=[g], sigma=0.0, lee=1, delta=0.0, camara=0, fl=FL_SERIE, tope=None)   # la prueba lee SIN tope en todos los brazos
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, genoma=g, **fila(y, T_pru))
            x['genoma_ok'] = bool(x['fund_gen0'] == g and x['fund_genes_distintos'] == 1)   # el genoma que LEYO el carro == el pedido (cubre sel, neu, pur, fab, off)
            if not x['genoma_ok']: raise RuntimeError(f"GENOMA LEIDO {x['fund_gen0']} != PEDIDO {g} (prueba {brazo})")
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo=tipo, i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


def par(A, B, I):
    a = [A[i]['cruzan'] for i in I]; b = [B[i]['cruzan'] for i in I]
    return dict(n=len(I), gana=sum(x > y for x, y in zip(a, b)), empata=sum(x == y for x, y in zip(a, b)), pierde=sum(x < y for x, y in zip(a, b)),
                suma_a=sum(a), suma_b=sum(b), dif=sum(a) - sum(b), por_indice_a=a, por_indice_b=b)


def par_gen(C, I, k, margen=MARGEN_G, otro=NEU):
    a = [C[CAND][i]['genoma_final'][k] for i in I]; b = [C[otro][i]['genoma_final'][k] for i in I]
    return dict(gen=k, otro=otro, margen=margen, n=len(I), gana=sum(x > y + margen for x, y in zip(a, b)), pierde=sum(x < y - margen for x, y in zip(a, b)),   # 'med_neu'/'por_cadena_neu' = el brazo 'otro' (neu o pur)
                med_sel=med(a), med_neu=med(b), por_cadena_sel=[round(x, 4) for x in a], por_cadena_neu=[round(y, 4) for y in b])


def lee_serie(C, R, n, abortos, npas=NPAS):
    """LA LETRA del PASO 2 (misma forma que perillas): validez V1-V5, V7a/b (relojes del neutro); PG (GEN_LETRA sube) y PC (cruza mas que neu)."""
    if GEN_LETRA is None: raise SystemExit("lee_serie: GEN_LETRA no fijado (PASO 2 no construido)")
    I = list(range(n)); gp = esc(GANA_PAR, n); dsu = math.ceil(DIF_SUMA * n / 20 - 1e-9); fg = esc(FAB_GANA, n); rc = esc(RELOJ_CAD, n)
    completo = all(len(C.get(b, {})) == n and all(len(C[b][i]['pasajes']) == npas for i in C[b]) for b in CADENAS) and all(len(R.get(b, {})) == n for b in ORDEN)
    est = lambda d: d.get('estado') or {}
    pas = lambda b: [q for i in C.get(b, {}) for q in C[b][i]['pasajes']]
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(R[b][i]['coherente'] for b in ORDEN for i in R.get(b, {})) and all(q['coherente'] for b in CADENAS for q in pas(b)))
    pf = par(R[TECHO], R[PISO_B], I) if completo else None
    v['V2_fab_gana_a_off'] = bool(pf and pf['gana'] >= fg)
    filas = [R[b][i] for b in ORDEN for i in R.get(b, {})] + [q for b in CADENAS for q in pas(b)]
    gen_ok = lambda q, g: q.get('genoma') == g and q['fund_n'] > 0 and q['fund_de_siembra'] == q['fund_n'] and q['fund_genes_distintos'] == 1 and q['fund_gen0'] == g
    v['V4_estado'] = bool(completo and all(est(q).get('carro') == CARRO and est(q).get('PERILLAS') == 1 and est(q).get('fl') == FL_SERIE for q in filas)
                          and all(est(q).get('lee') == LEE_CADENA[b] and est(q).get('sigma') == SIGMA and est(q).get('delta') == DELTA and est(q).get('camara') == 1 and est(q).get('muta') == list(MUTA_SERIE) and est(q).get('tope') == TOPE_CADENA[b] for b in CADENAS for q in pas(b))
                          and all(est(R[b][i]).get('lee') == 1 and est(R[b][i]).get('sigma') == 0.0 and est(R[b][i]).get('delta') == 0.0 and est(R[b][i]).get('camara') == 0
                                  and est(R[b][i]).get('siembra_n') == 1 and est(R[b][i]).get('tope') is None for b in ORDEN for i in I)
                          and all(gen_ok(R[b][i], C[b][i]['genoma_final']) for b in CADENAS for i in I)
                          and all(gen_ok(R[TECHO][i], DISENO) and gen_ok(R[PISO_B][i], BASE) for i in I))
    nl = 9
    v['V5_desde_cero'] = bool(completo and all(C[b][i]['pasajes'][0]['sembrado'] == 0 and C[b][i]['pasajes'][0]['fund_de_base'] == nl and C[b][i]['pasajes'][0]['fund_de_siembra'] == 0 for b in CADENAS for i in I)
                               and all(q['sembrado'] == 1 and q['fund_de_siembra'] == nl and q['fund_de_base'] == 0 for b in CADENAS for i in I for q in C[b][i]['pasajes'][1:])
                               and all(q['fund_de_camara'] == q['fund_n'] - nl for b in CADENAS for q in pas(b)))
    rl = {b: dict(prof=[C[b][i].get('prof_final') for i in sorted(C.get(b, {}))], refund=[C[b][i].get('refund_camara') for i in sorted(C.get(b, {}))]) for b in CADENAS}
    sobre = lambda xs, m_: sum(1 for z in xs if z is not None and z >= m_)
    # auditoria (B-2): los dos relojes sobre el NEUTRO y sobre SEL; si sel no llega es NO SE LEE, no NO. Profundidad EFECTIVA sobre el gen de la letra =
    # profundidad x (fraccion de los eventos que caen en MARGEN) = profundidad x (1/len(MUTA_SERIE) si 0 in MUTA_SERIE)
    fe = (1.0 / len(MUTA_SERIE)) if 0 in MUTA_SERIE else 0.0
    v['V7a_profundidad_mutacional_neu_sel_pur'] = bool(completo and all(sobre(rl[b]['prof'], PROF_MIN) >= rc for b in CADENAS))
    v['V7b_refundaciones_por_camara_neu_sel_pur'] = bool(completo and all(sobre(rl[b]['refund'], REFUND_MIN) >= rc for b in CADENAS))
    valido = all(v.values()); ok = valido or completo
    p = {}; pg = pc = None
    if ok:
        pg = par_gen(C, I, GEN_LETRA); pc = par(R[CAND], R[NEU], I)
        nb = sum(1 for i in I if C[CAND][i]['genoma_final'][GEN_LETRA] >= FUNC_MARGEN)   # (b): cadenas sel cuyo MARGEN final esta en la zona funcional
        p['PG_a_sel_sobre_neu'] = pg['gana'] >= gp; p['PG_b_sel_en_zona_funcional'] = nb >= gp; p['PG_gen_sube'] = p['PG_a_sel_sobre_neu'] and p['PG_b_sel_en_zona_funcional']
        p['PC_par_neu'] = pc['gana'] >= gp; p['PC_suma_neu'] = pc['dif'] >= dsu; p['n_sel_en_zona'] = nb
        pgr = par_gen(C, I, GEN_LETRA, MARGEN_GR, PUR); p['GR_sel_sobre_pur'] = pgr['gana'] >= gp; p['n_gr'] = pgr['gana']   # puerta de GRADIENTE (5-oct)
    umbral = bool(ok and (abs(pg['gana'] - gp) <= 1 or abs(nb - gp) <= 1 or abs(pc['gana'] - gp) <= 1 or abs(pc['dif'] - dsu) <= 1 or abs(pgr['gana'] - gp) <= 1))
    umbral_b = bool(ok and abs(nb - gp) <= 1)   # (b) a +-1: lo unico que dispara replica desde CONSERVA
    umbral_gr = bool(ok and abs(pgr['gana'] - gp) <= 1)   # H-1 (auditor corto): GR a +-1: lo unico que dispara replica desde TRINQUETE
    matiz = None
    if not valido: ver = 'NO SE LEE'
    else:
        A = p['PG_a_sel_sobre_neu']; B = p['PG_b_sel_en_zona_funcional']; Cz = p['PC_par_neu'] and p['PC_suma_neu']; GR = p['GR_sel_sobre_pur']
        if A and B and Cz and GR: ver = 'FUNCIONA'; matiz = 'la seleccion sube el margen porque un margen mayor persiste mas (sel > pur) y el genoma cruza mas que la deriva'
        elif A and B and not GR: ver = TRINQUETE; matiz = 'la seleccion purificadora y la deriva llevan el margen a la zona funcional; no hay evidencia de gradiente (sel ~ pur)' + (' (y cruza mas que la deriva)' if Cz else ' (y no cruza mas que la deriva)')
        elif A and B: ver = 'HAY ALGO MODESTO'; matiz = 'el gen sube con gradiente (sel > pur) pero no cruza mas que la deriva'
        elif A: ver = CONSERVA; matiz = 'la seleccion impide que el margen caiga a 0; no lo sube' + (' (y el genoma cruza mas que el de la deriva)' if Cz else ' (y no cruza mas que la deriva)')
        elif Cz: ver = 'HAY ALGO MODESTO'; matiz = 'cruza mas que la deriva sin que el gen suba por la letra'
        else: ver = 'NO'
    desc = {}
    if ok:
        desc['suma_cruzan'] = {b: sum(R[b][i]['cruzan'] for i in I) for b in ORDEN}
        desc['mayorias_(>=5/9)'] = {b: sum(R[b][i]['mayoria'] for i in I) for b in ORDEN}   # la definicion del muro, por brazo
        desc['sel_mayoria_como_O1'] = bool(sum(R[CAND][i]['mayoria'] for i in I) >= esc(MAYORIAS_MURO, n))
        desc['mord_BD_med'] = {b: med([R[b][i]['mord_BD'] for i in I]) for b in ORDEN}; desc['mord_AC_med'] = {b: med([R[b][i]['mord_AC'] for i in I]) for b in ORDEN}
        desc['frac_sin_bueno_med'] = {b: med([R[b][i]['frac_sin_bueno'] for i in I]) for b in ORDEN}; desc['fund_med'] = {b: med([R[b][i]['fund_med'] for i in I]) for b in ORDEN}
        desc['sel_MARGEN_en_zona_funcional'] = sum(1 for i in I if C[CAND][i]['genoma_final'][GEN_LETRA] >= FUNC_MARGEN)
        desc['fl_serie'] = FL_SERIE; desc['muta_serie'] = list(MUTA_SERIE)
        desc['UNA_EVIDENCIA'] = 'PG y PC son UNA evidencia: neu cae a ~0.01 y con MARGEN ~0 nadie pare; PC con neu es casi off vs sel'
        desc['sel_cadenas_LIMPIA_le_0.5'] = sum(1 for i in I if C[CAND][i]['genoma_final']['LIMPIA'] <= 0.5)   # sujetas a la regalia de ERR-191
        desc['sel_pruebas_BD_le_5'] = sum(1 for i in I if R[CAND][i]['mord_BD'] <= 5)   # cruzar sin morder nada malo = limpieza regalada (ERR-191)
        desc['sel_MARGEN_final_por_cadena'] = [round(C[CAND][i]['genoma_final'][GEN_LETRA], 4) for i in I]
        desc['R0_med'] = {b: med([R[b][i]['R0_med'] for i in I]) for b in ORDEN}
        desc['establecidos'] = {b: sum(R[b][i]['establecidos'] for i in I) for b in ORDEN}
        desc['mundo_AC'] = {b: med([R[b][i]['mundo_AC'] for i in I]) for b in ORDEN}
        desc['genes'] = {k: par_gen(C, I, k) for k in GENES}
        desc['gradiente_sel_vs_pur'] = pgr
        raz = {i: ((C[CAND][i]['prof_final'] / C[PUR][i]['prof_final']) if C[PUR][i].get('prof_final') else None) for i in I}   # H-4: razon de profundidad sel/pur
        Ie = [i for i in I if raz[i] is not None and 0.7 <= raz[i] <= 1.3]
        desc['GR_estratificado_profundidad'] = dict(razon_sel_pur_por_cadena=[(round(raz[i], 3) if raz[i] is not None else None) for i in I], n_dentro_30pct=len(Ie),
                                                  GR_solo_en_ellas=(par_gen(C, Ie, GEN_LETRA, MARGEN_GR, PUR) if Ie else None), nota='descriptivo; no toca la letra')
        desc['gradiente_sel_vs_pur_dup'] = None; desc['pur_prueba_sin_tope'] = dict(suma_cruzan=sum(R[PUR][i]['cruzan'] for i in I), mayorias=sum(R[PUR][i]['mayoria'] for i in I), R0_med=med([R[PUR][i]['R0_med'] for i in I]))
        desc['pareados'] = {f"{a}_vs_{b}": par(R[a], R[b], I) for a, b in (('sel', 'neu'), ('sel', 'pur'), ('pur', 'neu'), ('sel', 'off'), ('sel', 'fab'), ('neu', 'off'), ('fab', 'off'))}
    for b in CADENAS:
        Cb = C.get(b, {})
        if not Cb: continue
        np_ = max(len(Cb[i]['pasajes']) for i in Cb)
        col = lambda q, f: [f(Cb[i]['pasajes'][q]) for i in Cb if len(Cb[i]['pasajes']) > q]
        desc[f'{b}_trayectoria_gen_mediana_por_pasaje'] = {k: [med(col(q, lambda z: (z['genes_siembra'] or {}).get(k))) for q in range(np_)] for k in GENES}
        desc[f'{b}_cruzan_por_pasaje_mediana'] = [med(col(q, lambda z: z['cruzan'])) for q in range(np_)]
        desc[f'{b}_establecidos_en_pasaje_mediana'] = [med(col(q, lambda z: z['moneda']['n_est'])) for q in range(np_)]
    desc['relojes'] = {b: dict(profundidad_mutacional_mediana=med(rl[b]['prof']), profundidad_EFECTIVA_sobre_MARGEN_mediana=(round(med(rl[b]['prof']) * fe, 1) if med(rl[b]['prof']) is not None else None),
                               refundaciones_por_camara_mediana=med(rl[b]['refund']), cadenas_prof_sobre_min=sobre(rl[b]['prof'], PROF_MIN), cadenas_refund_sobre_min=sobre(rl[b]['refund'], REFUND_MIN)) for b in CADENAS}
    return dict(validez=v, puertas=p, veredicto=ver, matiz=matiz, en_umbral=umbral, conserva_b_umbral=umbral_b, trinquete_gr_umbral=umbral_gr, pareado_gen=pg, pareado_neu=pc, pareado_fab_off=pf, descriptivo=desc)


def casos_sinteticos():
    """Casos sinteticos de la letra (arnes (F)); se construyen con GEN_LETRA fijado."""
    def cad(gf, prof=60, ref=4000):
        pas = [dict(sembrado=int(p > 0), fund_de_base=(9 if p == 0 else 0), fund_de_siembra=(0 if p == 0 else 9), fund_de_camara=20, fund_n=29, coherente=True,
                    estado=dict(carro=CARRO, PERILLAS=1, lee=None, sigma=SIGMA, delta=DELTA, camara=1, fl=FL_SERIE, muta=list(MUTA_SERIE)), moneda=dict(n_est=5, respaldo=False), genes_siembra=dict(gf), cruzan=3) for p in range(NPAS)]
        return dict(pasajes=pas, genoma_final=dict(gf), prof_final=prof, refund_camara=ref)
    def pru(g, cr):
        return dict(cruzan=cr, mayoria=int(cr >= 5), coherente=True, genoma=dict(g), fund_n=9, fund_de_siembra=9, fund_genes_distintos=1, fund_gen0=dict(g), R0_med=0.9, establecidos=5, mundo_AC=7.0,
                    mord_BD=300, mord_AC=600, frac_sin_bueno=0.03, fund_med=0.0, estado=dict(carro=CARRO, PERILLAS=1, lee=1, sigma=0.0, delta=0.0, camara=0, siembra_n=1, fl=FL_SERIE, tope=None))
    def arma(gs, gn, cs, cn, cf=8, co=1, gp_=None, cp=1):
        gp_ = dict(gs) if gp_ is None else gp_
        C = {'sel': {}, 'neu': {}, 'pur': {}}; R = {b: {} for b in ORDEN}
        for i in range(20):
            C['sel'][i] = cad(gs); C['neu'][i] = cad(gn); C['pur'][i] = cad(gp_)
            for b in CADENAS:
                for q in C[b][i]['pasajes']: q['estado']['lee'] = LEE_CADENA[b]; q['estado']['tope'] = TOPE_CADENA[b]
            R['sel'][i] = pru(gs, cs); R['neu'][i] = pru(gn, cn); R['pur'][i] = pru(gp_, cp); R['fab'][i] = pru(DISENO, cf); R['off'][i] = pru(BASE, co)
        return C, R
    alto = dict(BASE, **{GEN_LETRA: 0.10}); medio = dict(BASE, **{GEN_LETRA: 0.045}); bajo = dict(BASE, **{GEN_LETRA: 0.008}); zona = dict(BASE, **{GEN_LETRA: 0.07})
    out = [('FUNCIONA (gen sube a la zona funcional, sel > pur + 0.02, y cruza mas)', arma(alto, bajo, 5, 1, gp_=zona) + (20, 0), 'FUNCIONA'),
           ('TRINQUETE (sel en zona pero sel ~ pur; cruza mas)', arma(alto, bajo, 5, 1, gp_=alto) + (20, 0), TRINQUETE),
           ('TRINQUETE (sel en zona, sel ~ pur, no cruza mas)', arma(alto, bajo, 1, 1, gp_=dict(BASE, **{GEN_LETRA: 0.09})) + (20, 0), TRINQUETE),
           ('MODESTO (gen sube con gradiente, no cruza mas)', arma(alto, bajo, 1, 1, gp_=zona) + (20, 0), 'HAY ALGO MODESTO'),
           ('CONSERVA, NO SUBE (sel > neu + 0.03 pero sel < 0.06; cruza igual)', arma(medio, bajo, 1, 1) + (20, 0), CONSERVA),
           ('CONSERVA, NO SUBE (y cruza mas que neu)', arma(medio, bajo, 5, 1) + (20, 0), CONSERVA),
           ('MODESTO (cruza mas sin que el gen suba)', arma(bajo, bajo, 5, 1) + (20, 0), 'HAY ALGO MODESTO'),
           ('NO (ni sube ni cruza)', arma(bajo, bajo, 1, 1) + (20, 0), 'NO'),
           ('NO SE LEE (aborto)', arma(alto, bajo, 5, 1) + (20, 1), 'NO SE LEE'),
           ('NO SE LEE (fab no gana a off)', arma(alto, bajo, 5, 1, cf=1, co=1) + (20, 0), 'NO SE LEE')]
    C, R = arma(alto, bajo, 5, 1)
    for i in range(20): C['neu'][i]['prof_final'] = 10
    out.append(('NO SE LEE (reloj neutro corto)', (C, R, 20, 0), 'NO SE LEE'))
    C, R = arma(alto, bajo, 5, 1)
    for i in range(20): C['sel'][i]['refund_camara'] = 100
    out.append(('NO SE LEE (reloj de sel corto: B-2)', (C, R, 20, 0), 'NO SE LEE'))
    C, R = arma(alto, bajo, 5, 1, gp_=alto)   # H-1: TRINQUETE con GR a +-1 (12/20 cadenas sel > pur + 0.02) -> replica; con GR 0/20 -> no
    for i in range(12):
        g13 = dict(BASE, **{GEN_LETRA: 0.13}); C['sel'][i]['genoma_final'] = g13; R['sel'][i]['genoma'] = dict(g13); R['sel'][i]['fund_gen0'] = dict(g13)
    out.append(('TRINQUETE con GR a +-1 (12/20): dispara replica', (C, R, 20, 0), (TRINQUETE, True)))
    out.append(('TRINQUETE con GR 0/20: NO dispara replica', arma(alto, bajo, 5, 1, gp_=alto) + (20, 0), (TRINQUETE, False)))
    return out


# ------------------------------------------------------------------ verificaciones y candados
def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for nm, sha in SHAS_PROPIOS.items():
        s = h16(os.path.join(AQUI, nm)); fij = sha is not None; ok &= (s == sha) if fij else True
        log(f"  sha muro_perillas/{nm} {s} {'OK' if (not fij or s == sha) else '!= ' + sha + ' FALLA'}{'' if fij else ' (NO FIJADO: solo humo/mapa)'}")
    for nm, b in CB.todas().items():
        igual = os.path.exists(CARROS[nm]) and open(CARROS[nm], 'rb').read() == b; ok &= igual
        log(f"  carro {nm} == construye_muro_perillas: {igual}")
    return ok


def identidad_corta(log, seed=None, T=1500):
    """O1_MURO_GEN con dosis de fabrica, sigma 0 == O1 (salida ENTERA) · con LIMPIA 0 == CTRL_O1_SINLIMPIA · todo apagado != O1."""
    seed = seed or BASES['arnes']; fija(); m = CV._MODS[CARRO]; o1 = CV.modulo('O1'); sl = P.carga_carro('CTRL_O1_SINLIMPIA')
    N = lambda x: json.loads(json.dumps(x, default=str))
    rr = lambda mod: N(P.run(seed, [('X', mod)] * 9, T=T, fundador_limpio=1))
    def cc(g, sigma, lee):
        try:
            _pon(m, [g] if g is not None else None, seed, sigma, (DELTA if sigma else 0.0), lee, 1); return rr(m)
        finally: _quita(m)
    ro = rr(o1)
    i1 = cc(dict(DISENO), 0.0, 1) == ro; i2 = cc(dict(DISENO, LIMPIA=0.0), 0.0, 1) == rr(sl); i3 = cc(None, SIGMA, 0) == ro; i4 = cc(dict(BASE), 0.0, 1) != ro
    log(f"  IDENTIDAD CORTA MURO_PERILLAS (salida ENTERA, N 9, s {seed}, T {T}): GEN dosis 1 sigma 0 == O1 {i1} · GEN LIMPIA 0 == CTRL_O1_SINLIMPIA {i2} · "
        f"GEN PS_LEE 0 sigma {SIGMA} camara 1 desde la base == O1 {i3} · control todo apagado != O1 {i4}")
    return i1 and i2 and i3 and i4


def guarda(modo, pre, reanuda):
    if GEN_LETRA is None: return "GEN_LETRA no fijado: el PASO 2 no esta construido (primero el mapa y el preregistro)"
    if FL_SERIE not in (0, 1): return 'FL_SERIE no fijado'
    if any(x is None for x in SHAS_PROPIOS.values()): return f"SHAS_PROPIOS sin fijar: {[k for k, x in SHAS_PROPIOS.items() if x is None]}"
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if r.get('modo') == modo and (r.get('letra') or {}).get('veredicto') in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda"
    if modo == 'replica':
        rsm = sorted(glob.glob(os.path.join(DATOS, f"serie_i{BASES['serie'][1]}-*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto'); um = (rs0.get('letra') or {}).get('en_umbral')
        ub = (rs0.get('letra') or {}).get('conserva_b_umbral'); ug = (rs0.get('letra') or {}).get('trinquete_gr_umbral')
        if not (vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um) or (vs == CONSERVA and ub) or (vs == TRINQUETE and ug)):
            return f"REGLA DE PARADA: serie = {vs} (umbral {um}; (b) a +-1: {ub}; GR a +-1: {ug})"
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)): return "sha_runner de la serie != runner actual"
    for r in [os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), os.path.join(AQUI, 'construye_muro_perillas.py'), os.path.join(AQUI, 'identidad_muro_perillas.py'), os.path.join(AQUI, 'nulo_margen.py')] + list(CARROS.values()):
        rel = os.path.relpath(r, RAIZ).replace(os.sep, '/')
        t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
        c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
        if not (t and c): return f"git: {rel} commiteado {t} · sin cambios vs HEAD {c}"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--mapa', action='store_true'); g.add_argument('--lee', action='store_true')
    g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true'); g.add_argument('--lee_serie', default=None)
    g.add_argument('--humo_serie', action='store_true'); g.add_argument('--humo_cadena', action='store_true')
    ap.add_argument('--lote', default=None); ap.add_argument('--genomas', default=None); ap.add_argument('--seed', type=int, default=None)
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--forzar_cpu', action='store_true'); ap.add_argument('--nota', default='')
    ap.add_argument('--fl', type=int, default=1)   # PASO A: fundador_limpio del mapa (1 = canonico ENMIENDA 5; 0 = el de la sellada 5001-5020)
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX}")
    if a.lee: lee_mapa(os.path.join(DATOS, 'mapa')); return 0
    if a.lee_serie:
        C, R, ab = carga(os.path.abspath(a.lee_serie)); n = max([len(x) for x in C.values()] + [len(x) for x in R.values()] + [0])
        L = lee_serie(C, R, n, len(ab)); print(json.dumps(dict(veredicto=L['veredicto'], validez=L['validez'], puertas=L['puertas'], en_umbral=L['en_umbral'], pareado_gen=L['pareado_gen'], pareado_neu=L['pareado_neu']), indent=1)); return 0
    t0 = time.time(); sel = time.strftime('%Y%m%d_%H%M%S')
    BUF = []; LOGF = [None]
    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    log(f"CORRE_MURO_PERILLAS · {'humo' if a.humo else 'mapa' if a.mapa else 'serie' if a.serie else 'replica' if a.replica else 'humo_serie' if a.humo_serie else 'humo_cadena'} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · runner {h16(os.path.abspath(__file__))} · nota {a.nota!r}")
    if a.humo or a.mapa:
        if a.pool: raise SystemExit("--humo/--mapa: sin Pool (un proceso)")
        if a.humo:
            T = 2000; trabajos = [('off', BASES['humo'][0]), ('fab', BASES['humo'][0])]; carpeta = os.path.join(DATOS, 'humo', f"humo_{sel}")
        else:
            T = a.T or 100000
            if a.lote:
                if a.lote not in LOTES: raise SystemExit(f"--lote: {sorted(LOTES)}")
                trabajos = [(e, LOTE_SEM[a.lote]) for e in LOTES[a.lote]]
            elif a.genomas and a.seed:
                trabajos = [(e.strip(), a.seed) for e in a.genomas.split(',') if e.strip()]
            else: raise SystemExit("--mapa: --lote X, o --genomas a,b --seed s")
            if not all(883001 <= s <= 883010 for _, s in trabajos): raise SystemExit("--mapa: semillas 883001-883010")
            carpeta = os.path.join(DATOS, 'mapa')
        if len(trabajos) > MAX_CORRIDAS_1P or T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(trabajos)}) y <= {MAX_PASOS_1P} pasos (T {T})")
        npy, ntot = python_de_trabajo()
        log(f"  REGLA DE CPU: python.exe ajenos de TRABAJO {npy} (totales {ntot}; los padres ociosos de Pool no cuentan) · tope {CPU_TOPE}")
        if npy >= CPU_TOPE and not a.forzar_cpu: log("  >= tope: NO SE CORRE (construye, lee y espera)."); return 2
        for e, _ in trabajos: (mixta(e) if e.startswith('mix:') else genoma(e))   # valida las etiquetas antes de correr
        ok = verifica(log) and identidad_corta(log)
        if not ok: log("  ALGO FALLA -> no se corre."); return 1
        os.makedirs(carpeta, exist_ok=True); LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n')
        if a.fl not in (0, 1): raise SystemExit('--fl 0 o 1')
        X = [corrida_fija(e, s, T, carpeta, log, fl=a.fl) for e, s in trabajos]
        if a.humo:   # regla 14 en el humo: fab fijo == corre_v143.tarea('O1') campo a campo
            N = lambda x: json.loads(json.dumps(x, default=str)); s0 = BASES['humo'][0]
            x = tarea(s0, T, siembra=[dict(DISENO)], sigma=0.0, delta=0.0, lee=1, camara=0); y = CV.tarea((s0, 'O1', T))
            r14 = sin_ids(x['linajes']) == sin_ids(y['linajes']) and sin_ids(x['pista']) == sin_ids(y['pista'])   # corregido 12:35: los ids llevan el nombre del carro
            log(f"  regla 14 (ENTRADA campo a campo, salvo el nombre del carro en los ids): fab fijo == corre_v143.tarea('O1') (s {s0}, T {T}): {'OK' if r14 else 'FALLA'}")
            rj = os.path.join(carpeta, 'resumen.json')
            with open(rj, 'w', encoding='utf-8') as fh: json.dump(dict(modo='humo', T=T, regla14=r14, corridas=[{k: x[k] for k in ('etq', 'seed', 'cruzan', 'R0_med', 'fund_med', 'establecidos', 'aborto', 'seg')} for x in X],
                                                                    sha_runner=h16(os.path.abspath(__file__)), seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
            log(f"  RESUMEN {rj} · HUMO (no cuenta) · {time.time() - t0:.1f}s")
        else:
            lee_mapa(carpeta, log); log(f"  {time.time() - t0:.1f}s")
        return 0
    if a.humo_cadena:   # ¿una cadena que nace en el ARRANQUE (MARGEN de BASE) muta antes de extinguirse? 1 pasaje sel de T 20 000 + lectura de la siembra
        if a.pool: raise SystemExit('--humo_cadena: un proceso')
        T = a.T or 20000; carpeta = os.path.join(DATOS, 'humo', f'humo_cadena_{sel}')
        if not (verifica(log) and identidad_corta(log)): log('  ALGO FALLA -> no se corre.'); return 1
        os.makedirs(carpeta, exist_ok=True); LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write(chr(10).join(BUF) + chr(10))
        c = cadena(0, BASES['humo'], 1, T, carpeta, False, 'sel', log)
        q = c['pasajes'][0]
        log(f"  HUMO CADENA desde BASE {BASE}: T {T} · fundadores {q['fund_n']} (base {q['fund_de_base']}, camara {q['fund_de_camara']}) · partos {q['partos_tel']} · moneda {q['moneda']} · "
            f"genes de los vivos al final {q['genes_vivos_fin']} · siembra mediana {c['genoma_final']} · prof {c['prof_final']} · cruzan {q['cruzan']}/9 · R0 {q['R0_med']} · vida {q['vida_med']} · B+D {q['mord_BD']}")
        ext = q['fund_de_camara'] == 0 and q['partos_tel'] == 0
        log(f"  ¿se extingue sin mutar? {'SI (ni partos ni refundaciones: la cadena no muta)' if ext else 'NO: hubo ' + str(q['partos_tel']) + ' partos y ' + str(q['fund_de_camara']) + ' refundaciones (cada una es una mutacion)'}")
        json.dump(dict(modo='humo_cadena', T=T, base=BASE, cadena=c, sha_runner=h16(os.path.abspath(__file__))), open(os.path.join(carpeta, 'resumen.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return 0
    # ------------------------------------------------------------ PASO 2: serie / replica (SOLO el coordinador) · --humo_serie: main de punta a punta (ERR-42) en 1 proceso
    if a.humo_serie:
        if a.T: raise SystemExit('--humo_serie: configuracion fija (T); --pool <= 2 permitido para ejercitar la rama Pool (ERR-42)')
        modo = 'humo_serie'; base = BASES['humo']; n = 1; npas = 2; T_pas, T_pru = 5000, 20000; pre = 'humo_serie'; dest = os.path.join(DATOS, 'humo')
    else:
        modo = 'serie' if a.serie else 'replica'; base = BASES[modo]; n = N_IND; npas = NPAS; T_pas, T_pru = T_PAS, T_PRU; dest = DATOS
        pre = f"{modo}_i{sem_pru(base, 0)}-{sem_pru(base, n - 1)}"
    os.makedirs(dest, exist_ok=True)
    prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d)))
    if a.reanuda and not prev: raise SystemExit(f'--reanuda: no hay carpeta {pre}_* en {dest}')
    if modo != 'humo_serie':
        e = guarda(modo, pre, a.reanuda)
        if e: raise SystemExit(f"NO SE CORRE (candado): {e}")
    carpeta = os.path.join(dest, prev[-1]) if (a.reanuda and prev) else os.path.join(dest, pre + '_' + sel)
    shp = h16(os.path.join(AQUI, PRERREGISTRO))
    log(f"  preregistro {PRERREGISTRO} {shp} · base {base} · pasajes T {T_pas} x {npas} · pruebas T {T_pru} · n {n} · sigma {SIGMA} delta {DELTA} · GEN_LETRA {GEN_LETRA} margen {MARGEN_G} zona {FUNC_MARGEN} · BASE {BASE} · mutan {list(MUTA_SERIE)} · fundador_limpio {FL_SERIE} · carpeta {carpeta}")
    if not (verifica(log) and identidad_corta(log)): log("  ALGO FALLA -> no se corre."); return 1
    os.makedirs(carpeta, exist_ok=True); LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n')
    f1 = [('cadena', i, b) for i in range(n) for b in CADENAS] + [('prueba', i, b) for i in range(n) for b in (TECHO, PISO_B)]
    if modo == 'humo_serie' and not a.reanuda: f1 = [('cadena', 0, b) for b in CADENAS]   # 1er proceso: 3 cadenas x 2 pasajes de 5k + pruebas sel/neu/pur de 20k = 9 corridas (pool 3 las reparte); 2o (--reanuda): fab y off y la letra
    mk = lambda t: (t[0], t[1], t[2], base, npas, T_pas, T_pru, carpeta, a.reanuda)
    def fmt(x):
        if x['tipo'] == 'cadena':
            ps = x.get('pasajes') or []
            return f"  [{time.time()-t0:7.1f}s] cadena i{x['i']} {x['brazo']} ({x['seg']}s) aborto {x['aborto']} · cruzan {[q['cruzan'] for q in ps]} · estab {[q['moneda']['n_est'] for q in ps]} · prof {[q.get('prof') for q in ps]} · refund {[q['fund_de_camara'] for q in ps]} · genoma final {x.get('genoma_final')}"
        return f"  [{time.time()-t0:7.1f}s] {x['tipo']} i{x['i']} {x['brazo']:4s} ({x['seg']}s) aborto {x['aborto']} · genoma {x.get('genoma')} · cruzan {x.get('cruzan')}/9 mayoria {x.get('mayoria')} R0 {x.get('R0_med')} estab {x.get('establecidos')} B+D {x.get('mord_BD')} A+C {x.get('mord_AC')}"
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            pend = {PL.apply_async(trabajo, (mk(t),)): t for t in f1}
            while pend:
                listos = [r for r in pend if r.ready()]
                if not listos: time.sleep(2); continue
                for r in listos:
                    t = pend.pop(r); x = r.get(); log(fmt(x))
                    if t[0] == 'cadena': pend[PL.apply_async(trabajo, (mk(('prueba', t[1], t[2])),))] = ('prueba', t[1], t[2])
    else:
        for t in f1 + [('prueba', t[1], t[2]) for t in f1 if t[0] == 'cadena']: log(fmt(trabajo(mk(t))))
        if modo == 'humo_serie' and a.reanuda:
            for t in [('prueba', 0, TECHO), ('prueba', 0, PISO_B)]: log(fmt(trabajo(mk(t))))
    C, R, ab = carga(carpeta); L = None
    if all(len(R[b]) == n for b in ORDEN) and all(len(C[b]) == n for b in CADENAS):
        L = lee_serie(C, R, n, len(ab), npas)
        log(f"\n================ LA LETRA ({PRERREGISTRO})"); log(f"  validez {L['validez']} · puertas {L['puertas']} · umbral {L['en_umbral']} · matiz {L['matiz']}")
        log(f"  pareado_gen {L['pareado_gen']}"); log(f"  pareado_neu {L['pareado_neu']}"); log(f"  fab vs off {L['pareado_fab_off']}")
        for k, v in L['descriptivo'].items(): log(f"  [desc] {k}: {v}")
    ver = ('HUMO (no cuenta): ' if modo == 'humo_serie' else '') + ((L['veredicto'] + (f" ({L['matiz']})" if L.get('matiz') else '')) if L else 'parcial')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, letra=L, abortos=ab, n=n, npas=npas, T_pas=T_pas, T_pru=T_pru, veredicto=ver, nota=a.nota, sigma=SIGMA, delta=DELTA, gen_letra=GEN_LETRA, margen_gen=MARGEN_G, func_margen=FUNC_MARGEN, muta_serie=list(MUTA_SERIE), base=BASE, fl_serie=FL_SERIE,
                       preregistro=PRERREGISTRO, sha_preregistro=shp, sha_runner=h16(os.path.abspath(__file__)), shas={os.path.relpath(k, RAIZ): h16(k) for k in SHAS},
                       shas_propios={k: h16(os.path.join(AQUI, k)) for k in SHAS_PROPIOS}, seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"  RESUMEN {rj} · abortos {len(ab)} · {time.time()-t0:.1f}s"); log(f"VEREDICTO: {ver}")
    return 0


def carga(carpeta):
    C = {b: {} for b in CADENAS}; R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'cadena_i*_*.json')) + glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"{d['tipo']} i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        (C if d['tipo'] == 'cadena' else R)[d['brazo']][d['i']] = d
    return C, R, ab


if __name__ == '__main__':
    sys.exit(main())
