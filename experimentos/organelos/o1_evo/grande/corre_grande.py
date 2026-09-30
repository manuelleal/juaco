"""corre_grande.py — RUNNER y LECTURA del EXPLORATORIO "MUNDO MAS GRANDE Y CON MAS COSAS" (grande, 30-sep-2026).
Preregistro: PREREGISTRO_grande.md (la lectura esta AQUI, en lee(), y alli en la sec. 5). Mundo: pista_grande.py. Arnes: identidad_grande.py.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Pregunta: ¿el orden O1 > termo > v143 se mantiene en un mundo mas rico, y cuanto margen queda (que falla O1)?

QUE SE CORRE: cada corrida ES experimentos/tronco_v14_3/corre_v143.tarea (se IMPORTA, no se toca = juez.tarea(seed, 9 carros iguales, T,
pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje) con pista.run SUSTITUIDA, SOLO durante la llamada,
por pista_grande.run con los mismos argumentos + las perillas del mundo del brazo. Regla 14: el arnes (I1) verifica que con el mundo de
FABRICA esta tarea da la MISMA salida (cruda y resumida) que corre_v143.tarea. Lo unico agregado: 'grande' (fisica de las zonas, solo
lectura), 'tel_ps' (solo o1pas) y 'estado'.
MUNDOS: grande = G 2 (L 720, 72 objetos, 18 sorteos de olvido), oasis + pantano · liso = G 2 sin cosas nuevas (control de tamano).
BRAZOS (9 carros iguales, fundador limpio):
  o1      O1 de fabrica                       (carrera_escuderias/carros/O1.py)                mundo grande
  termo   V143_TERMO                          (organelos/termo/carros/V143_TERMO.py)           mundo grande
  v143    V143 (el bicho real)                (tronco_v14_3/carros_v143/V143.py)               mundo grande
  pc      TPATAS con PATAS = 3 (UTIL+CEDE)    (organelos/dinamita/carros/TPATAS.py)            mundo grande
  o1liso  O1 de fabrica                                                                         mundo liso (separa tamano de cosas)
  o1pas   O1_PAS (o1_evo, parte A) con SIEMBRA evolucionada: SOLO con --siembra <ruta>          mundo grande (OPCIONAL)
SEMILLAS (grep 30-sep en .py/.md de todo JUACO: 718xxx no aparece): explora 718001-718005 · arnes 718080-718089 · humo 718090-718099.
T 100 000 (humo 20 000). nube-9: trabajo() atrapa TODO; JSON por trabajo ANTES de volver (ERR-54); --reanuda salta lo hecho.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN; --explora SOLO el coordinador, con preregistro, runner y pista_grande
COMMITEADOS y sin cambios respecto de HEAD):
  python experimentos/organelos/o1_evo/grande/corre_grande.py --humo                         # 1 proceso: 5 corridas (6 con --siembra), T 20 000
  python experimentos/organelos/o1_evo/grande/corre_grande.py --explora --pool 4             # 25 corridas (30 con --siembra)
  python experimentos/organelos/o1_evo/grande/corre_grande.py --explora --pool 4 --reanuda
  python experimentos/organelos/o1_evo/grande/corre_grande.py --explora --pool 4 --siembra <ruta>   # ruta: cadena_*.json, carpeta de la parte A,
                                                                                                    # lista JSON de genomas o resumen.json de o1_evo
  python experimentos/organelos/o1_evo/grande/corre_grande.py --lee <carpeta>
"""
import argparse, copy, glob, hashlib, importlib.util, json, math, os, platform, statistics as st, subprocess, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV          # tarea (se IMPORTA, no se toca)
import pista_grande as PG
P = CV.P; J = CV.J
if P is not PG.P: raise SystemExit("corre_grande: corre_v143 y pista_grande no ven el MISMO modulo pista")

PRERREGISTRO = 'PREREGISTRO_grande.md'
DATOS = os.path.join(AQUI, 'datos')
TERMO_PY = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo', 'carros', 'V143_TERMO.py')
TPATAS_PY = os.path.join(RAIZ, 'experimentos', 'organelos', 'dinamita', 'carros', 'TPATAS.py')
O1PAS_PY = os.path.join(RAIZ, 'experimentos', 'organelos', 'o1_evo', 'carros', 'O1_PAS.py')
PG_PY = os.path.join(AQUI, 'pista_grande.py')
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028', TERMO_PY: '3db639cab75641fb', TPATAS_PY: '1b6272ef4616af8b',
        PG_PY: None}
SHA_PG = '15fea5afb19fdde4'              # pista_grande.py (se fija al cerrar el archivo; el arnes lo imprime)
SHAS[PG_PY] = SHA_PG
# o1pas (OPCIONAL): O1_PAS.py de la parte A. Si la parte A lo cambia tras su auditoria, el coordinador actualiza ESTA linea (y la del
# preregistro, sec. 3) ANTES de correr; si no calza, --siembra ABORTA (los demas brazos no dependen de el).
SHA_O1PAS = 'c5377ada6b28bee0'
MUNDOS = {'grande': dict(G=2, rica=1, lento=1), 'liso': dict(G=2, rica=0, lento=0), 'fabrica': dict(PG.FABRICA_MUNDO)}
# brazo -> (nombre del carro en corre_v143._MODS, archivo propio o None, PATAS o None, mundo)
BRAZOS = {'o1': ('O1', None, None, 'grande'), 'termo': ('V143_TERMO', TERMO_PY, None, 'grande'), 'v143': ('V143', None, None, 'grande'),
          'pc': ('TPATAS_3', TPATAS_PY, 3, 'grande'), 'o1liso': ('O1', None, None, 'liso'), 'o1pas': ('O1_PAS', O1PAS_PY, None, 'grande')}
ORDEN = ('o1', 'termo', 'v143', 'pc', 'o1liso'); OPCIONAL = 'o1pas'
EXPLORA = range(718001, 718006); ARNES = range(718080, 718090); HUMO_S = 718090
T_DEF = 100000; T_HUMO = 20000; POOL_MAX = 4; N_LIN = 9
ZONA = PG.FRAC_ZONA
PS_SIGMA = 0.03                  # la sigma de o1pas en la prueba de la parte A


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None


# ------------------------------------------------------------------ estado por proceso (cfg por worker)
def nombres():
    for b, (n, _, _, _) in BRAZOS.items(): CV.BRAZOS[b] = n


def fija(brazo):
    """Carga en ESTE proceso la instancia PROPIA del carro del brazo si falta (verifica su sha) y FIJA sus perillas (PATAS). Devuelve el
    estado que se escribe en el JSON."""
    nombres()
    n, ruta, v, mundo = BRAZOS[brazo]
    if ruta is None:
        CV.modulo(n); return dict(carro=n, sha=None, PATAS=None, mundo=mundo)
    s = h16(ruta); esp = SHA_O1PAS if brazo == 'o1pas' else SHAS[ruta]
    if s != esp: raise SystemExit(f"sha {ruta} {s} != {esp}")
    m = CV._MODS.get(n)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{n}", ruta)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    if v is not None: m.PATAS = v
    if n in ('V143_TERMO', 'TPATAS_3') and m.TERMO != 1: raise SystemExit(f"{n}: TERMO {m.TERMO} != 1")
    if n == 'O1_PAS' and m.PASAJE != 1: raise SystemExit(f"{n}: PASAJE {m.PASAJE} != 1")
    return dict(carro=n, sha=s, PATAS=getattr(m, 'PATAS', None), TERMO=getattr(m, 'TERMO', None), mundo=mundo)


def tarea(seed, brazo, T, siembra=None, mundo=None):
    """corre_v143.tarea tal cual (regla 14), con pista.run -> pista_grande.run(+ mundo) SOLO durante la llamada.
    mundo None -> el del brazo ('fabrica' SOLO en el arnes). Devuelve la salida de corre_v143.tarea + grande + tel_ps + estado + _crudo."""
    est = fija(brazo); mw = MUNDOS[mundo or BRAZOS[brazo][3]]; est['mundo_kw'] = dict(mw)
    n = BRAZOS[brazo][0]; m = CV._MODS.get(n) if n == 'O1_PAS' else None
    if m is not None:
        if not siembra: raise SystemExit("o1pas sin siembra")
        m.SIEMBRA = copy.deepcopy(siembra); m.PS_SEMILLA = int(seed); m.PS_SIGMA = PS_SIGMA; m.PS_LEE = 1
        est.update(sigma=PS_SIGMA, siembra_n=len(siembra))
    cap = []; orig = P.run

    def run2(*a, **k):
        if k != dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1) or len(a) != 2:
            raise SystemExit(f"corre_grande: corre_v143.tarea llamo a pista.run con {k} (esperado el de juez.tarea con fundador limpio)")
        if m is not None: m._TEL.clear(); m._PS_CNT.clear()
        r = PG.run(*a, **k, **mw)
        cap.append(dict(crudo=r, tel=(copy.deepcopy({str(i): v for i, v in m._TEL.items()}) if m is not None else None)))
        return r
    P.run = run2
    try:
        x = CV.tarea((seed, n, T))
    finally:
        P.run = orig
        if m is not None: m.SIEMBRA = None; m.PS_SEMILLA = 0; m.PS_SIGMA = 0.03
    r = cap[0]['crudo']
    x['grande'] = dict(pista=r['pista'].get('grande'), L=r['pista']['L'], nobj=r['pista']['nobj'],
                       linajes=[d['_carrera'].get('grande') for d in r['linajes']])
    x['tel_ps'] = cap[0]['tel']; x['estado'] = est; x['_crudo'] = r
    return x


def resumen_grande(g, T):
    """Descriptivos fisicos de las zonas (suma de los 9 linajes). frac_* contra la parte del anillo de cada zona (0.10)."""
    Ls = [x for x in g['linajes'] if x]
    if not Ls: return None
    s = lambda f: sum(f(x) for x in Ls)
    ac_tot = s(lambda x: x['mord_total']['A'] + x['mord_total']['C'])
    ac_oa = s(lambda x: x['mord_oasis']['A'] + x['mord_oasis']['C']); ac_pa = s(lambda x: x['mord_pantano']['A'] + x['mord_pantano']['C'])
    mu = s(lambda x: x['muertes'])
    return dict(frac_pasos_oasis=round(s(lambda x: x['pasos_oasis']) / (len(Ls) * T), 4),
                frac_pasos_pantano=round(s(lambda x: x['pasos_pantano']) / (len(Ls) * T), 4),
                frac_AC_oasis=(round(ac_oa / ac_tot, 4) if ac_tot else None), frac_AC_pantano=(round(ac_pa / ac_tot, 4) if ac_tot else None),
                mord_AC=ac_tot, mord_AC_oasis=ac_oa, mord_AC_pantano=ac_pa, cargas=s(lambda x: x['cargas']),
                drenado=round(s(lambda x: x['drenado']), 3), muertes=mu, muertes_con_carga=s(lambda x: x['muertes_con_carga']),
                frac_muertes_con_carga=(round(s(lambda x: x['muertes_con_carga']) / mu, 4) if mu else None),
                max_cargas=max(x['max_cargas'] for x in Ls))


def fila(x, T):
    L = x['linajes']; tel = x.get('tel_ps') or {}
    fp = [f for v in tel.values() for f in (v or {}).get('fund', [])]
    cz = {k: sum(l['causas'][k] for l in L) for k in ('hambre', 'sed', 'veneno', 'sal')}
    return dict(seed=x['seed'], T=T, R0_real=[l['R0_real'] for l in L], R0_med=med([l['R0_real'] for l in L]),
                fund=[l['fundadores'] for l in L], fund_post10k=[l['fund_post10k'] for l in L], cruza=[int(l['cruza_real']) for l in L],
                cruzan=sum(int(l['cruza_real']) for l in L), mayoria=int(sum(int(l['cruza_real']) for l in L) * 2 > len(L)),
                persisten=sum(int(l['persiste']) for l in L), casi_inmortales=sum(int(l['casi_inmortal']) for l in L), vida_med=med([l['vida_med'] for l in L]), muertes=sum(l['muertes'] for l in L),
                causas=cz, mord_BD=sum(l['mord']['B'] + l['mord']['D'] for l in L), mord_AC=sum(l['mord']['A'] + l['mord']['C'] for l in L),
                coherente=all(l.get('coherente', True) for l in L), t_fund_rec=all(l.get('t_fund_rec_ok', True) for l in L),
                nac_reales=[l.get('nac_reales') for l in L], fund_de_siembra=sum(f[0] for f in fp), fund_n=len(fp),
                mundo_AC=round(x['pista']['comp_mundo']['A'] + x['pista']['comp_mundo']['C'], 4),
                frac_sin_bueno_mundo=x['pista'].get('frac_sin_bueno_mundo'),
                zonas=resumen_grande(x['grande'], T), grande_pista=x['grande']['pista'], L=x['grande']['L'], nobj=x['grande']['nobj'],
                estado=x.get('estado'))


# ------------------------------------------------------------------ siembra (brazo opcional o1pas)
GENES = ('MARGEN', 'PRUEBA', 'PEN_OTRO', 'PISO')


def carga_siembra(ruta):
    """-> (lista de siembras [una por cadena, o una sola], sha de la entrada). Acepta: carpeta de la parte A (cadena_i*_o1pas.json con
    'siembra_final'), un cadena_*.json, una lista JSON de genomas, o un resumen.json de o1_evo (genes del ultimo pasaje por cadena)."""
    ruta = os.path.abspath(ruta)
    if os.path.isdir(ruta):
        fs = sorted(glob.glob(os.path.join(ruta, 'cadena_i*_o1pas.json')))
        if not fs: raise SystemExit(f"--siembra: {ruta} no tiene cadena_i*_o1pas.json")
        S = []
        for f in fs:
            d = json.load(open(f, encoding='utf-8'))
            if d.get('aborto') or not d.get('siembra_final'): raise SystemExit(f"--siembra: {f} abortada o sin siembra_final")
            S.append(d['siembra_final'])
        sha = hashlib.sha256(''.join(h16(f) for f in fs).encode()).hexdigest()[:16]
    else:
        d = json.load(open(ruta, encoding='utf-8')); sha = h16(ruta)
        if isinstance(d, list): S = [d]
        elif isinstance(d, dict) and d.get('siembra_final'): S = [d['siembra_final']]
        elif isinstance(d, dict) and ((d.get('letra') or {}).get('descriptivo') or {}).get('genes_siembra_ultimo_por_cadena'):
            u = d['letra']['descriptivo']['genes_siembra_ultimo_por_cadena']
            S = [[u[k]] for k in sorted(u, key=lambda z: int(z)) if u[k]]
        else: raise SystemExit(f"--siembra: formato no reconocido en {ruta}")
    for s in S:
        if not s or not all(isinstance(g, dict) and set(g) == set(GENES) and all(math.isfinite(float(g[k])) for k in GENES) for g in s):
            raise SystemExit(f"--siembra: genoma invalido (claves {GENES})")
    return S, sha


# ------------------------------------------------------------------ trabajo
def trabajo(args):
    """UNA corrida (seed, brazo). Atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54); con reanuda salta la que ya existe SIN
    aborto (un aborto guardado se reintenta y queda anotado en 'reintento_de')."""
    seed, brazo, T, carpeta, reanuda, siembra, sha_sie = args
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json"); previo = None
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
        previo = x0['aborto']
    t0 = time.time()
    try:
        x = tarea(seed, brazo, T, siembra=siembra); x.pop('_crudo'); x.pop('pizarra_log', None)
        x = dict(brazo=brazo, T=T, aborto=None, fila=fila(x, T), crudo=x, siembra_sha=sha_sie)
    except BaseException as e:   # noqa: nube-9
        x = dict(brazo=brazo, T=T, seed=seed, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False, default=str)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ LA LECTURA (PREREGISTRO_grande.md sec. 5)
def par(A, B, S):
    a = [A[s]['cruzan'] for s in S]; b = [B[s]['cruzan'] for s in S]
    return dict(n=len(S), gana=sum(x > y for x, y in zip(a, b)), empata=sum(x == y for x, y in zip(a, b)), pierde=sum(x < y for x, y in zip(a, b)),
                suma_a=sum(a), suma_b=sum(b), dif=sum(a) - sum(b))


def lee(R, brazos, n, abortos, T):
    """R[brazo][seed] = fila. n = semillas esperadas. EXPLORATORIO: lectura, no veredicto de tronco."""
    S = sorted(set.intersection(*[set(R.get(b, {})) for b in brazos])) if brazos else []
    tot = N_LIN * len(S)
    v = {}
    v['V1_completa'] = bool(abortos == 0 and len(S) == n and all(R[b][s]['coherente'] and R[b][s]['t_fund_rec'] for b in brazos for s in S))
    v['V2_cosas_actuan'] = all(R[b][s]['zonas'] and R[b][s]['zonas']['mord_AC_oasis'] > 0 and R[b][s]['zonas']['cargas'] > 0
                               and (R[b][s]['grande_pista'] or {}).get('rica') == 1 and R[b][s]['grande_pista'].get('lento') == 1
                               for b in brazos if BRAZOS[b][3] == 'grande' for s in S)
    v['V2b_liso_sin_cosas'] = all(R[b][s]['grande_pista'] == {'G': 2} and R[b][s]['zonas'] is None for b in brazos if BRAZOS[b][3] == 'liso' for s in S)
    v['V3_estado'] = all((R[b][s].get('estado') or {}).get('carro') == BRAZOS[b][0] and R[b][s]['estado'].get('PATAS') == BRAZOS[b][2]
                         and R[b][s]['estado'].get('mundo') == BRAZOS[b][3] for b in brazos for s in S)
    v['V4_tamano'] = all(R[b][s]['L'] == 720 and R[b][s]['nobj'] == 72 for b in brazos for s in S)
    if OPCIONAL in brazos:
        v['V5_siembra_actua'] = all(R[OPCIONAL][s]['fund_n'] > 0 and R[OPCIONAL][s]['fund_de_siembra'] == R[OPCIONAL][s]['fund_n'] for s in S)
    valido = all(v.values())
    suma = {b: sum(R[b][s]['cruzan'] for s in S) for b in brazos}
    may = {b: sum(R[b][s]['mayoria'] for s in S) for b in brazos}
    out = dict(validez=v, valido=valido, semillas=S, total_linajes=tot, suma_cruzan=suma, mayorias=may)
    if not S: out['lectura'] = 'NO SE LEE'; return out
    # L1 ORDEN (principal): estricto por sumas de linajes que cruzan
    o1, te, vv = suma['o1'], suma['termo'], suma['v143']
    orden = o1 > te > vv
    out['L1_orden'] = dict(se_mantiene=orden, o1=o1, termo=te, v143=vv,
                           invertido=[p for p, ok in (('o1>termo', o1 > te), ('termo>v143', te > vv)) if not ok])
    out['L2_par_o1_termo'] = par(R['o1'], R['termo'], S); out['L2_par_termo_v143'] = par(R['termo'], R['v143'], S)
    out['L3_margen_o1'] = dict(no_cruzan=tot - o1, frac_cruzan=round(o1 / tot, 4) if tot else None, mayorias=may['o1'])
    out['L4_cosas_en_o1'] = dict(o1liso=suma.get('o1liso'), o1=o1, dif_liso_menos_grande=(suma['o1liso'] - o1) if 'o1liso' in suma else None,
                                 par=(par(R['o1liso'], R['o1'], S) if 'o1liso' in R else None))
    Z = {b: [R[b][s]['zonas'] for s in S if R[b][s]['zonas']] for b in brazos if BRAZOS[b][3] == 'grande'}
    out['L5_oasis'] = {b: dict(ratio_pasos=med([z['frac_pasos_oasis'] / ZONA for z in zs]), ratio_mord_AC=med([(z['frac_AC_oasis'] or 0) / ZONA for z in zs]))
                       for b, zs in Z.items()}
    out['L6_pantano'] = {b: dict(ratio_pasos=med([z['frac_pasos_pantano'] / ZONA for z in zs]), ratio_mord_AC=med([(z['frac_AC_pantano'] or 0) / ZONA for z in zs]),
                                 frac_muertes_con_carga=med([z['frac_muertes_con_carga'] for z in zs]), cargas_med=med([z['cargas'] for z in zs]),
                                 drenado_med=med([z['drenado'] for z in zs]))
                         for b, zs in Z.items()}
    out['L7_pc_termo'] = par(R['pc'], R['termo'], S)
    if OPCIONAL in brazos: out['L8_o1pas_o1'] = par(R[OPCIONAL], R['o1'], S)
    out['desc'] = {b: dict(R0_med=med([R[b][s]['R0_med'] for s in S]), fund_media=med([st.mean(R[b][s]['fund']) for s in S]),
                           fund_mediana=med([med(R[b][s]['fund']) for s in S]), persisten=sum(R[b][s]['persisten'] for s in S),
                           vida_med=med([R[b][s]['vida_med'] for s in S]), muertes=sum(R[b][s]['muertes'] for s in S),
                           causas={k: sum(R[b][s]['causas'][k] for s in S) for k in ('hambre', 'sed', 'veneno', 'sal')},
                           mord_BD_med=med([R[b][s]['mord_BD'] for s in S]), mord_AC_med=med([R[b][s]['mord_AC'] for s in S]),
                           mundo_AC=med([R[b][s]['mundo_AC'] for s in S]), sin_bueno=med([R[b][s]['frac_sin_bueno_mundo'] for s in S]))
                   for b in brazos}
    # PREDICCIONES (sec. 4; escaladas a 45 linajes / 5 semillas; con n distinto (humo) NO cuentan)
    k = tot / 45 if tot else 1
    pr = {}
    pr['P1_orden_se_mantiene'] = orden
    pr['P2_o1_suma_en_22_40'] = 22 * k <= o1 <= 40 * k
    pr['P3_o1_mayoria_ge_3de5'] = may['o1'] >= math.ceil(3 * len(S) / 5 - 1e-9)
    if 'o1liso' in suma: pr['P4_liso_menos_grande_en_m3_10'] = -3 * k <= suma['o1liso'] - o1 <= 10 * k
    pr['P5_oasis_no_se_usa'] = all(x['ratio_pasos'] is not None and 0.7 <= x['ratio_pasos'] <= 1.4 for x in out['L5_oasis'].values())
    pr['P6_pantano_no_se_evita'] = all(x['ratio_mord_AC'] is not None and 0.6 <= x['ratio_mord_AC'] <= 1.4 for x in out['L6_pantano'].values())
    pr['P7_pc_igual_termo'] = abs(suma['pc'] - suma['termo']) <= 6 * k
    out['predicciones'] = pr
    # RESERVA (sec. 5bis, escrita tras el humo y ANTES de la exploracion): la letra no ve a los casi inmortales (< 5 muertes: ni cruzan
    # ni fallan). Si o1, termo o v143 tiene >= 10 de 45 casi inmortales, L1 se lee CON RESERVA y se reporta L1b (cruzan + casi inmortales).
    ci = {b: sum(R[b][s]['casi_inmortales'] for s in S) for b in brazos}
    out['casi_inmortales'] = ci
    out['reserva_inmortales'] = [b for b in ('o1', 'termo', 'v143') if ci[b] >= math.ceil(10 * tot / 45 - 1e-9)]
    out['L1b_cruzan_mas_inmortales'] = {b: suma[b] + ci[b] for b in brazos}
    # H-2 (auditoria, antes de datos): L4 y P4 llevan CON RESERVA si o1liso tiene >= 10 de 45 casi inmortales
    if 'o1liso' in ci:
        r4 = ci['o1liso'] >= math.ceil(10 * tot / 45 - 1e-9)
        out['L4_cosas_en_o1']['reserva_inmortales_o1liso'] = r4
        out['P4_con_reserva'] = r4
    out['lectura'] = 'NO SE LEE' if not valido else (('ORDEN SE MANTIENE' if orden else 'ORDEN NO SE MANTIENE')
                                                     + (f" (CON RESERVA: casi inmortales en {out['reserva_inmortales']})" if out['reserva_inmortales'] else ''))
    return out


def carga(carpeta):
    R = {}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, '*_s*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"{os.path.basename(f)}: {d['aborto']}"); continue
        f0 = d['fila']
        if 'casi_inmortales' not in f0: f0['casi_inmortales'] = sum(int(l['casi_inmortal']) for l in d['crudo']['linajes'])
        R.setdefault(d['brazo'], {})[f0['seed']] = f0
    return R, ab


def imprime(Lr, log):
    for k, v in Lr.items():
        if k in ('semillas',): continue
        log(f"  {k}: {v}")


# ------------------------------------------------------------------ verificaciones y candados
def verifica(log, con_o1pas):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    if con_o1pas:
        s = h16(O1PAS_PY); ok &= s == SHA_O1PAS; log(f"  sha {os.path.relpath(O1PAS_PY, RAIZ)} {s} {'OK' if s == SHA_O1PAS else '!= ' + SHA_O1PAS + ' FALLA'}")
    _, info = PG.construye(); log(f"  pista_grande construida por anclas: {info}")
    return ok


def identidad_corta(log, seed=718089, T=800):
    """Mundo de FABRICA: tarea() == corre_v143.tarea (salida resumida ENTERA y crudo ENTERO), O1 x9, fundador limpio."""
    N = lambda x: json.dumps(x, default=str, sort_keys=True)
    cap = []; orig = P.run

    def spy(*a, **k):
        r = orig(*a, **k); cap.append(r); return r
    P.run = spy
    try:
        a = CV.tarea((seed, 'O1', T))
    finally:
        P.run = orig
    b = tarea(seed, 'o1', T, mundo='fabrica'); rb = b.pop('_crudo')
    for k in ('seg',): a.pop(k); b.pop(k)
    extra = {k: b.pop(k) for k in ('grande', 'tel_ps', 'estado')}
    i1 = N(a) == N(b); i2 = N(cap[0]) == N(rb); i3 = extra['grande']['pista'] is None and all(x is None for x in extra['grande']['linajes'])
    log(f"  IDENTIDAD CORTA (O1 x9, s {seed}, T {T}, fundador limpio, mundo de fabrica): tarea == corre_v143.tarea {i1} · crudo == pista.run {i2} · "
        f"sin claves nuevas {i3}")
    return i1 and i2 and i3


def git_limpio(rutas, log):
    ok = True
    for r in rutas:
        rel = os.path.relpath(r, RAIZ).replace('\\', '/')
        try:
            t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
            c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
        except Exception:   # noqa
            t = c = False
        ok &= t and c; log(f"  git {rel}: commiteado {t} · sin cambios vs HEAD {c}")
    return ok


def guarda(pre, reanuda):
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if not r.get('humo') and str((r.get('lectura') or {}).get('lectura', '')).startswith('ORDEN'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene lectura {r['lectura']['lectura']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true'); ap.add_argument('--siembra', default=None)
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX} (contrato del encargo)")
    if a.lee:
        c = os.path.abspath(a.lee); R, ab = carga(c)
        br = [b for b in ORDEN + (OPCIONAL,) if b in R]; n = max(len(v) for v in R.values()) if R else 0
        T = next(iter(next(iter(R.values())).values()))['T'] if R else 0
        Lr = lee(R, br, n, len(ab), T); imprime(Lr, print)
        print(f"LECTURA ({'humo/parcial, no cuenta' if n != len(EXPLORA) else 'exploratorio'}): {Lr['lectura']} · abortos {ab}")
        return 0
    siembras, sha_sie = (carga_siembra(a.siembra) if a.siembra else (None, None))
    brazos = ORDEN + ((OPCIONAL,) if siembras else ())
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        modo = 'humo'; semillas = [HUMO_S]; T = T_HUMO; pre = f"humo_s{HUMO_S}_T{T}"; dest = os.path.join(DATOS, 'humo')
    else:
        modo = 'explora'; semillas = list(EXPLORA); T = T_DEF; pre = f"explora_s{EXPLORA[0]}-{EXPLORA[-1]}"; dest = DATOS
    sel = time.strftime('%Y%m%d_%H%M%S')
    prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
    if a.reanuda and not prev: raise SystemExit(f"--reanuda: no hay carpeta {pre}_* en {dest}")
    carpeta = os.path.join(dest, prev[-1]) if (a.reanuda and prev) else os.path.join(dest, pre + '_' + sel)
    BUF = []; LOGF = [None]

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"
        print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    t0 = time.time()
    shp = h16(os.path.join(AQUI, PRERREGISTRO)) if os.path.exists(os.path.join(AQUI, PRERREGISTRO)) else 'NO EXISTE'
    log(f"CORRE_GRANDE · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_grande.py "
        f"{h16(os.path.abspath(__file__))} · preregistro {PRERREGISTRO} {shp} · carpeta {carpeta}")
    log(f"  semillas {semillas} · T {T} · brazos {list(brazos)} · mundos {MUNDOS['grande']} / liso {MUNDOS['liso']} · siembra {a.siembra} ({sha_sie}) · reanuda {a.reanuda}")
    if not a.humo:
        e = guarda(pre, a.reanuda)
        if e: log(f"  NO SE CORRE (candado): {e}"); return 1
    ok = verifica(log, bool(siembras)) and identidad_corta(log)
    if not a.humo:
        ok &= git_limpio([os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), PG_PY], log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    # H-4 (auditoria): con --reanuda, la siembra (sha) y los brazos deben ser los de la corrida previa
    meta_p = os.path.join(carpeta, 'meta.json')
    if a.reanuda:
        if os.path.exists(meta_p):
            mp = json.load(open(meta_p, encoding='utf-8')); sha0 = mp.get('siembra_sha'); br0 = mp.get('brazos')
        else:   # carpeta anterior a meta.json: se infiere de los JSON de o1pas
            fo = sorted(glob.glob(os.path.join(carpeta, f'{OPCIONAL}_s*.json')))
            sha0 = json.load(open(fo[0], encoding='utf-8')).get('siembra_sha') if fo else None
            br0 = list(ORDEN) + ([OPCIONAL] if fo else [])
        if sha0 != sha_sie or br0 != list(brazos):
            log(f"  NO SE CORRE (H-4): --reanuda con siembra {sha_sie} / brazos {list(brazos)} != corrida previa {sha0} / {br0}"); return 1
        log(f"  H-4: --reanuda con la MISMA siembra ({sha_sie}) y brazos que la corrida previa: OK")
    os.makedirs(carpeta, exist_ok=True)
    if not os.path.exists(meta_p):
        with open(meta_p, 'w', encoding='utf-8') as fh: json.dump(dict(siembra=a.siembra, siembra_sha=sha_sie, brazos=list(brazos)), fh)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')
    for s in BUF: LOGF[0].write(s + '\n')
    tareas = []
    for j, s in enumerate(semillas):
        for b in brazos:
            sie = siembras[j % len(siembras)] if (b == OPCIONAL and siembras) else None
            tareas.append((s, b, T, carpeta, a.reanuda, sie, sha_sie if b == OPCIONAL else None))
    if a.humo and len(tareas) > 6: raise SystemExit("--humo: maximo 6 corridas por proceso")
    X = []
    if a.pool:
        from multiprocessing import Pool
        with Pool(a.pool) as pool:
            for x in pool.imap_unordered(trabajo, tareas):
                X.append(x); f = x.get('fila') or {}
                log(f"  [{time.time() - t0:7.1f}s] {x['brazo']:6s} s{f.get('seed', x.get('seed'))} ({x['seg']}s) cruzan {f.get('cruzan')}/9 "
                    f"zonas {(f.get('zonas') or {}).get('frac_pasos_oasis')}/{(f.get('zonas') or {}).get('frac_AC_pantano')} aborto {x.get('aborto')}")
    else:
        for tt in tareas:
            x = trabajo(tt); X.append(x); f = x.get('fila') or {}
            log(f"  [{time.time() - t0:7.1f}s] {x['brazo']:6s} s{f.get('seed', x.get('seed'))} ({x['seg']}s) cruzan {f.get('cruzan')}/9 "
                f"R0 real {f.get('R0_real')} fund {f.get('fund')} zonas {f.get('zonas')} aborto {x.get('aborto')}")
    R, ab = carga(carpeta)
    Lr = lee(R, list(brazos), len(semillas), len(ab), T); imprime(Lr, log)
    res = dict(modo=modo, humo=bool(a.humo), semillas=semillas, T=T, brazos=list(brazos), sha_runner=h16(os.path.abspath(__file__)),
               sha_preregistro=shp, sha_pista_grande=h16(PG_PY), siembra=a.siembra, siembra_sha=sha_sie, lectura=Lr,
               seg_por_corrida={f"{x['brazo']}_s{(x.get('fila') or {}).get('seed', x.get('seed'))}": x['seg'] for x in X},
               seg_total=round(time.time() - t0, 1))
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh: json.dump(res, fh, ensure_ascii=False, indent=1, default=str)
    log(f"  RESUMEN {os.path.relpath(rj, RAIZ)} (sha {h16(rj)}) · terminado en {time.time() - t0:.1f}s")
    log(f"LECTURA DE LA CORRIDA: {'HUMO (no cuenta): ' if a.humo else ''}{Lr['lectura']}")
    LOGF[0].close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
