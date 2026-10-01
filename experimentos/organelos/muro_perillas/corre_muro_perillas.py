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
SHAS_PROPIOS = {'construye_muro_perillas.py': None, os.path.join('carros', 'O1_MURO_GEN.py'): None, os.path.join('carros', 'O1_MURO_GEN0.py'): None}   # se fijan al cerrar el preregistro
GENES = CB.GENES; BASE = dict(zip(GENES, CB.BASE)); DISENO = dict(zip(GENES, CB.DISENO)); SIGMA = CB.SIGMA; DELTA = CB.DELTA
CADENAS = ('sel', 'neu'); LEE_CADENA = {'sel': 1, 'neu': 0}
ORDEN = ('sel', 'neu', 'fab', 'off'); CAND = 'sel'; NEU = 'neu'; TECHO = 'fab'; PISO_B = 'off'
BASES = {'serie': (883100, 883301), 'replica': (883500, 883701), 'humo': (883990, 883998), 'mapa': (883001, 883001), 'arnes': 883950}
SEM_MAPA = (883001, 883002)
N_IND = 20; NPAS = 5; T_PAS = 100000; T_PRU = 100000; VENT = 5000; POOL_MAX = 2
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000; CPU_TOPE = 6
# ------------------------------------------------------------------ constantes de la LETRA del PASO 2 (se FIJAN tras el mapa, en el preregistro)
GEN_LETRA = None       # el gen de la letra (PG): el que el mapa muestre con pendiente desde apagado; None = PASO 2 no construido
MARGEN_G = 0.05; GANA_PAR = 13; DIF_SUMA = 10; FAB_GANA = 16; PROF_MIN = 30; REFUND_MIN = 3000; RELOJ_CAD = 16   # los de perillas (a priori)


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


def _pon(m, siembra, seed, sigma, delta, lee, camara, por_linaje=None):
    m.SIEMBRA = copy.deepcopy(siembra); m.PS_SEMILLA = int(seed); m.PS_SIGMA = float(sigma); m.PS_DELTA = float(delta); m.PS_LEE = int(lee); m.PS_CAMARA = int(camara)
    m.PS_POR_LINAJE = copy.deepcopy(por_linaje)
    m._TEL.clear(); m._PS_CNT.clear(); m._VIVO.clear()


def _quita(m): _pon(m, None, 0, SIGMA, DELTA, 1, 1, None)


def tarea(seed, T, siembra=None, sigma=SIGMA, lee=1, delta=DELTA, camara=1, por_linaje=None):
    """corre_v143.tarea tal cual (regla 14) + 'tel_ps' (copia de _TEL del carro, solo lectura) + 'estado' (perillas de ESTE proceso).
    por_linaje = lista de 9 genomas (listas de 6) para la PISTA MIXTA (cada linaje con el suyo, fijo)."""
    est = fija(); m = CV._MODS[CARRO]
    _pon(m, siembra, seed, sigma, delta, lee, camara, por_linaje)
    est.update(sigma=float(sigma), delta=float(delta), camara=int(camara), siembra_n=len(siembra or []), lee=int(lee), por_linaje=(por_linaje is not None))
    try:
        x = CV.tarea((seed, CARRO, T))
        tel = copy.deepcopy({str(i): v for i, v in m._TEL.items()})
    finally:
        _quita(m)
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
    if etq == 'off': return dict(BASE)
    if etq == 'fab': return dict(DISENO)
    partes = etq.split('+'); g = dict(BASE if partes[0] == 'off' else DISENO)
    for q in (partes[1:] if partes[0] == 'off' else partes):
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
         'D': ['off+MARGEN=0.25', 'off+PISO=0.2', 'off+LIMPIA=1', 'off+MARGEN=0.25+PISO=0.2', 'off+MARGEN=0.25+LIMPIA=1+PISO=0.2', 'off+MARGEN=0.25+LIMPIA=1+PISO=0.2+PEN_OTRO=0.35']}
LOTE_SEM = {k: 883001 for k in LOTES}
for _k in list(LOTES):   # la segunda semilla: A2..M2
    LOTES[_k + '2'] = list(LOTES[_k]); LOTE_SEM[_k + '2'] = 883002


def corrida_fija(etq, seed, T, carpeta, log):
    fin = os.path.join(carpeta, f"fijo_{etq.replace(':', '-').replace('=', '')}_s{seed}_T{T}.json")
    if os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x = json.load(fh)
        if not x.get('aborto'): log(f"  (ya estaba) {etq} s{seed}: cruzan {x['cruzan']}/9 R0 {x['R0_med']}"); return x
    es_mix = etq.startswith('mix:'); t0 = time.time()
    g = None if es_mix else genoma(etq); pl = [[q[k] for k in GENES] for q in mixta(etq)] if es_mix else None
    try:
        if es_mix: y = tarea(seed, T, siembra=None, sigma=0.0, lee=1, delta=0.0, camara=0, por_linaje=pl)   # cada linaje con SU genoma fijo
        else: y = tarea(seed, T, siembra=[g], sigma=0.0, lee=1, delta=0.0, camara=0)   # genoma FIJO: sin mutacion, sin camara
        x = dict(tipo='fijo', etq=etq, genoma=g, genomas_linaje=pl, aborto=None, **fila(y, T))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo='fijo', etq=etq, genoma=g, genomas_linaje=pl, seed=seed, aborto=f"{type(e).__name__}: {e}"[:300])
    x['seg'] = round(time.time() - t0, 1); x['T'] = T
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    if x['aborto']: log(f"  [{x['seg']}s] {etq} s{seed} ABORTO {x['aborto']}")
    else:
        log(f"  [{x['seg']}s] {etq} s{seed} genoma {g if g else 'MIXTA'} · cruzan {x['cruzan']}/9 mayoria {x['mayoria']} R0 real med {x['R0_med']} fund med {x['fund_med']} estab {x['establecidos']}/9 "
            f"· vida {x['vida_med']} · causas {x['causas']} · B+D {x['mord_BD']} A+C {x['mord_AC']} · mundo AC {x['mundo_AC']} sin bueno {x['frac_sin_bueno']} · coherente {x['coherente']}")
        if es_mix:
            for q in x['por_linaje']: log(f"      linaje {q['i']} genes {q['genes']} cruza {q['cruza']} R0 {q['R0_real']} fund {q['fund']} B+D {q['mord_BD']} A+C {q['mord_AC']} limpiezas {q['limpiezas']}")
    return x


def lee_mapa(carpeta, log=print):
    R = {}
    for f in sorted(glob.glob(os.path.join(carpeta, 'fijo_*.json'))):
        x = json.load(open(f, encoding='utf-8'))
        if x.get('aborto'): log(f"  ABORTO {f}: {x['aborto']}"); continue
        R.setdefault(x['etq'], {})[x['seed']] = x
    orden = [e for k in sorted(LOTES) if not k.endswith('2') for e in LOTES[k]] + sorted(R)
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
            x = tarea(sem_pas(base, i, p), T, siembra=sie, sigma=SIGMA, lee=lee, delta=DELTA, camara=1)
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
            y = tarea(sem_pru(base, i), T_pru, siembra=[g], sigma=0.0, lee=1, delta=0.0, camara=0)
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, genoma=g, **fila(y, T_pru))
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


def par_gen(C, I, k, margen=MARGEN_G):
    a = [C[CAND][i]['genoma_final'][k] for i in I]; b = [C[NEU][i]['genoma_final'][k] for i in I]
    return dict(gen=k, margen=margen, n=len(I), gana=sum(x > y + margen for x, y in zip(a, b)), pierde=sum(x < y - margen for x, y in zip(a, b)),
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
    v['V4_estado'] = bool(completo and all(est(q).get('carro') == CARRO and est(q).get('PERILLAS') == 1 for q in filas)
                          and all(est(q).get('lee') == LEE_CADENA[b] and est(q).get('sigma') == SIGMA and est(q).get('delta') == DELTA and est(q).get('camara') == 1 for b in CADENAS for q in pas(b))
                          and all(est(R[b][i]).get('lee') == 1 and est(R[b][i]).get('sigma') == 0.0 and est(R[b][i]).get('delta') == 0.0 and est(R[b][i]).get('camara') == 0
                                  and est(R[b][i]).get('siembra_n') == 1 for b in ORDEN for i in I)
                          and all(gen_ok(R[b][i], C[b][i]['genoma_final']) for b in CADENAS for i in I)
                          and all(gen_ok(R[TECHO][i], DISENO) and gen_ok(R[PISO_B][i], BASE) for i in I))
    nl = 9
    v['V5_desde_cero'] = bool(completo and all(C[b][i]['pasajes'][0]['sembrado'] == 0 and C[b][i]['pasajes'][0]['fund_de_base'] == nl and C[b][i]['pasajes'][0]['fund_de_siembra'] == 0 for b in CADENAS for i in I)
                               and all(q['sembrado'] == 1 and q['fund_de_siembra'] == nl and q['fund_de_base'] == 0 for b in CADENAS for i in I for q in C[b][i]['pasajes'][1:])
                               and all(q['fund_de_camara'] == q['fund_n'] - nl for b in CADENAS for q in pas(b)))
    rl = {b: dict(prof=[C[b][i].get('prof_final') for i in sorted(C.get(b, {}))], refund=[C[b][i].get('refund_camara') for i in sorted(C.get(b, {}))]) for b in CADENAS}
    sobre = lambda xs, m_: sum(1 for z in xs if z is not None and z >= m_)
    v['V7a_profundidad_mutacional_neutra'] = bool(completo and sobre(rl[NEU]['prof'], PROF_MIN) >= rc)
    v['V7b_refundaciones_por_camara_neutra'] = bool(completo and sobre(rl[NEU]['refund'], REFUND_MIN) >= rc)
    valido = all(v.values()); ok = valido or completo
    p = {}; pg = pc = None
    if ok:
        pg = par_gen(C, I, GEN_LETRA); pc = par(R[CAND], R[NEU], I)
        p['PG_gen_sube'] = pg['gana'] >= gp; p['PC_par_neu'] = pc['gana'] >= gp; p['PC_suma_neu'] = pc['dif'] >= dsu
    umbral = bool(ok and (abs(pg['gana'] - gp) <= 1 or abs(pc['gana'] - gp) <= 1 or abs(pc['dif'] - dsu) <= 1))
    matiz = None
    if not valido: ver = 'NO SE LEE'
    else:
        G = p['PG_gen_sube']; Cz = p['PC_par_neu'] and p['PC_suma_neu']
        if G and Cz: ver = 'FUNCIONA'
        elif G or Cz: ver = 'HAY ALGO MODESTO'; matiz = 'el gen sube pero no cruza mas que la deriva' if G else 'cruza mas que la deriva sin que el gen suba por la letra'
        else: ver = 'NO'
    desc = {}
    if ok:
        desc['suma_cruzan'] = {b: sum(R[b][i]['cruzan'] for i in I) for b in ORDEN}
        desc['R0_med'] = {b: med([R[b][i]['R0_med'] for i in I]) for b in ORDEN}
        desc['establecidos'] = {b: sum(R[b][i]['establecidos'] for i in I) for b in ORDEN}
        desc['mundo_AC'] = {b: med([R[b][i]['mundo_AC'] for i in I]) for b in ORDEN}
        desc['genes'] = {k: par_gen(C, I, k) for k in GENES}
        desc['pareados'] = {f"{a}_vs_{b}": par(R[a], R[b], I) for a, b in (('sel', 'neu'), ('sel', 'off'), ('sel', 'fab'), ('neu', 'off'), ('fab', 'off'))}
    for b in CADENAS:
        Cb = C.get(b, {})
        if not Cb: continue
        np_ = max(len(Cb[i]['pasajes']) for i in Cb)
        col = lambda q, f: [f(Cb[i]['pasajes'][q]) for i in Cb if len(Cb[i]['pasajes']) > q]
        desc[f'{b}_trayectoria_gen_mediana_por_pasaje'] = {k: [med(col(q, lambda z: (z['genes_siembra'] or {}).get(k))) for q in range(np_)] for k in GENES}
        desc[f'{b}_cruzan_por_pasaje_mediana'] = [med(col(q, lambda z: z['cruzan'])) for q in range(np_)]
        desc[f'{b}_establecidos_en_pasaje_mediana'] = [med(col(q, lambda z: z['moneda']['n_est'])) for q in range(np_)]
    desc['relojes'] = {b: dict(profundidad_mutacional_mediana=med(rl[b]['prof']), refundaciones_por_camara_mediana=med(rl[b]['refund'])) for b in CADENAS}
    return dict(validez=v, puertas=p, veredicto=ver, matiz=matiz, en_umbral=umbral, pareado_gen=pg, pareado_neu=pc, pareado_fab_off=pf, descriptivo=desc)


def casos_sinteticos():
    """Casos sinteticos de la letra (arnes (F)); se construyen con GEN_LETRA fijado."""
    def cad(gf, prof=60, ref=4000):
        pas = [dict(sembrado=int(p > 0), fund_de_base=(9 if p == 0 else 0), fund_de_siembra=(0 if p == 0 else 9), fund_de_camara=20, fund_n=29, coherente=True,
                    estado=dict(carro=CARRO, PERILLAS=1, lee=None, sigma=SIGMA, delta=DELTA, camara=1), moneda=dict(n_est=5, respaldo=False), genes_siembra=dict(gf), cruzan=3) for p in range(NPAS)]
        return dict(pasajes=pas, genoma_final=dict(gf), prof_final=prof, refund_camara=ref)
    def pru(g, cr):
        return dict(cruzan=cr, coherente=True, genoma=dict(g), fund_n=9, fund_de_siembra=9, fund_genes_distintos=1, fund_gen0=dict(g), R0_med=0.9, establecidos=5, mundo_AC=7.0,
                    estado=dict(carro=CARRO, PERILLAS=1, lee=1, sigma=0.0, delta=0.0, camara=0, siembra_n=1))
    def arma(gs, gn, cs, cn, cf=8, co=1):
        C = {'sel': {}, 'neu': {}}; R = {b: {} for b in ORDEN}
        for i in range(20):
            C['sel'][i] = cad(gs); C['neu'][i] = cad(gn)
            for q in C['sel'][i]['pasajes']: q['estado']['lee'] = 1
            for q in C['neu'][i]['pasajes']: q['estado']['lee'] = 0
            R['sel'][i] = pru(gs, cs); R['neu'][i] = pru(gn, cn); R['fab'][i] = pru(DISENO, cf); R['off'][i] = pru(BASE, co)
        return C, R
    alto = dict(BASE, **{GEN_LETRA: 0.4}); bajo = dict(BASE)
    out = [('FUNCIONA (gen sube y cruza mas)', arma(alto, bajo, 5, 1) + (20, 0), 'FUNCIONA'),
           ('MODESTO (gen sube, no cruza mas)', arma(alto, bajo, 1, 1) + (20, 0), 'HAY ALGO MODESTO'),
           ('NO (ni sube ni cruza)', arma(bajo, bajo, 1, 1) + (20, 0), 'NO'),
           ('NO SE LEE (aborto)', arma(alto, bajo, 5, 1) + (20, 1), 'NO SE LEE'),
           ('NO SE LEE (fab no gana a off)', arma(alto, bajo, 5, 1, cf=1, co=1) + (20, 0), 'NO SE LEE')]
    C, R = arma(alto, bajo, 5, 1)
    for i in range(20): C['neu'][i]['prof_final'] = 10
    out.append(('NO SE LEE (reloj neutro corto)', (C, R, 20, 0), 'NO SE LEE'))
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
        if not (vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um)): return f"REGLA DE PARADA: serie = {vs} (umbral {um})"
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)): return "sha_runner de la serie != runner actual"
    for r in [os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), os.path.join(AQUI, 'construye_muro_perillas.py')] + list(CARROS.values()):
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
    ap.add_argument('--lote', default=None); ap.add_argument('--genomas', default=None); ap.add_argument('--seed', type=int, default=None)
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--forzar_cpu', action='store_true'); ap.add_argument('--nota', default='')
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
    log(f"CORRE_MURO_PERILLAS · {'humo' if a.humo else 'mapa' if a.mapa else 'serie' if a.serie else 'replica'} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · runner {h16(os.path.abspath(__file__))} · nota {a.nota!r}")
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
        X = [corrida_fija(e, s, T, carpeta, log) for e, s in trabajos]
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
    # ------------------------------------------------------------ PASO 2: serie / replica (SOLO el coordinador)
    modo = 'serie' if a.serie else 'replica'; base = BASES[modo]; n = N_IND; npas = NPAS
    pre = f"{modo}_i{sem_pru(base, 0)}-{sem_pru(base, n - 1)}"
    prev = sorted(d for d in os.listdir(DATOS) if d.startswith(pre + '_') and os.path.isdir(os.path.join(DATOS, d))) if os.path.isdir(DATOS) else []
    e = guarda(modo, pre, a.reanuda)
    if e: raise SystemExit(f"NO SE CORRE (candado): {e}")
    carpeta = os.path.join(DATOS, prev[-1]) if (a.reanuda and prev) else os.path.join(DATOS, pre + '_' + sel)
    shp = h16(os.path.join(AQUI, PRERREGISTRO))
    log(f"  preregistro {PRERREGISTRO} {shp} · base {base} · pasajes T {T_PAS} x {npas} · pruebas T {T_PRU} · n {n} · sigma {SIGMA} delta {DELTA} · GEN_LETRA {GEN_LETRA} · carpeta {carpeta}")
    if not (verifica(log) and identidad_corta(log)): log("  ALGO FALLA -> no se corre."); return 1
    os.makedirs(carpeta, exist_ok=True); LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n')
    f1 = [('cadena', i, b) for i in range(n) for b in CADENAS] + [('prueba', i, b) for i in range(n) for b in (TECHO, PISO_B)]
    mk = lambda t: (t[0], t[1], t[2], base, npas, T_PAS, T_PRU, carpeta, a.reanuda)
    def fmt(x):
        if x['tipo'] == 'cadena':
            ps = x.get('pasajes') or []
            return f"  [{time.time()-t0:7.1f}s] cadena i{x['i']} {x['brazo']} ({x['seg']}s) aborto {x['aborto']} · cruzan {[q['cruzan'] for q in ps]} · estab {[q['moneda']['n_est'] for q in ps]} · prof {[q.get('prof') for q in ps]} · refund {[q['fund_de_camara'] for q in ps]} · genoma final {x.get('genoma_final')}"
        return f"  [{time.time()-t0:7.1f}s] {x['tipo']} i{x['i']} {x['brazo']:4s} ({x['seg']}s) aborto {x['aborto']} · genoma {x.get('genoma')} · cruzan {x.get('cruzan')}/9 R0 {x.get('R0_med')} estab {x.get('establecidos')}"
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
    C, R, ab = carga(carpeta); L = None
    if all(len(R[b]) == n for b in ORDEN) and all(len(C[b]) == n for b in CADENAS):
        L = lee_serie(C, R, n, len(ab), npas)
        log(f"\n================ LA LETRA ({PRERREGISTRO})"); log(f"  validez {L['validez']} · puertas {L['puertas']} · umbral {L['en_umbral']} · matiz {L['matiz']}")
        log(f"  pareado_gen {L['pareado_gen']}"); log(f"  pareado_neu {L['pareado_neu']}"); log(f"  fab vs off {L['pareado_fab_off']}")
        for k, v in L['descriptivo'].items(): log(f"  [desc] {k}: {v}")
    ver = (L['veredicto'] + (f" ({L['matiz']})" if L.get('matiz') else '')) if L else 'parcial'
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, letra=L, abortos=ab, n=n, npas=npas, T_pas=T_PAS, T_pru=T_PRU, veredicto=ver, nota=a.nota, sigma=SIGMA, delta=DELTA, gen_letra=GEN_LETRA,
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
