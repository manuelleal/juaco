"""corre_juntos.py — RUNNER de "LOS TRES JUNTOS": memoria de lugar (P1) + senal por pizarra con costo (P7) + PREGUNTA (P10) en UN organismo
(O1_TODO), en un mundo que pide las tres (mundo_tramo_c: oasis que se muda cada 20 000 pasos + costo de emitir c_e 0.01). 1-oct-2026.
Preregistro: PREREGISTRO_juntos.md. Arnes: identidad_juntos.py. Carros: construye_juntos.py (anclas de construye_p7 y construye_c sobre el
texto de O1_LUGAR, shas fijados). Bitacora: ../BITACORA.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

PREGUNTA: las tres capacidades, que FUNCIONAN x2 por separado, SE SUMAN en un solo organismo, o se estorban (epistasis)?
QUE SE CORRE: cada corrida ES corre_v143.tarea (regla 14; se IMPORTA) con mundo_tramo_c.run en lugar de pista.run. La fila = corre_c.fila_c
(peldano 'preg': corre_p1.fila + oasis_info + latencias) + los bloques pizarra / senal / latencia por vida de corre_p7.fila (todo IMPORTADO
por sha; aqui no se copia ninguna cuenta). Lo agregado: la LETRA (lee_serie), los candados y la bitacora.
  BRAZOS (monocultivo de 9, L 360, 36 objetos, fundador limpio; mundo P1b + mueve 20000 + c_e 0.01):
    todo     O1_TODO       memoria + senal + pregunta                     EL CANDIDATO
    sen      O1_TODO_SEN   memoria + senal (pregunta apagada)             PAREJA (== O1_LUGAR_SENAL bit a bit, arnes)
    preg     O1_TODO_PREG  memoria + pregunta (senal apagada)             PAREJA (== O1_LUGAR_PREG bit a bit, arnes)
    lug      O1_LUGAR      solo memoria                                   BASE (validez)
    todobar  O1_TODO_SBAR  las tres con la senal leida al ANTIPODA        CONTROL DE CONTENIDO
MEDIDA PRINCIPAL: linajes que cruzan (cruza_real), por semilla y suma. Descriptivo: mayorias, fundadores, latencia tras la mudanza.
LETRA (por codigo, PREREGISTRO sec. 6): SUMAN / SE ESTORBAN / NO SUMAN.
SEMILLAS NUEVAS 7385xx (grep 1-oct: 7385 no aparece en .py/.md): serie 738501-738520 · replica 738551-738570 · explora 738581-738586 ·
humo 738590-738595 · arnes 738530-738539.
  python experimentos/organelos/escalera/juntos/corre_juntos.py --humo [--desde 738590] [--T 30000] [--n 2] [--brazos todo,sen,preg] [--mueve 10000] [--nota '...']
  python experimentos/organelos/escalera/juntos/corre_juntos.py --explora [--brazos ...]
  python experimentos/organelos/escalera/juntos/corre_juntos.py --serie --pool 2 [--reanuda]     (solo el coordinador)
  python experimentos/organelos/escalera/juntos/corre_juntos.py --replica --pool 2
  python experimentos/organelos/escalera/juntos/corre_juntos.py --lee <carpeta>
"""
import argparse, glob, importlib.util, json, math, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(ESC)))
sys.path.insert(0, ESC); sys.path.insert(0, AQUI)
import corre_c as CR             # fila_c, modulo('O1_LUGAR') (se IMPORTA; sha fijado)
import corre_p7 as R7            # fila: bloques pizarra / senal / latencia (se IMPORTA; sha fijado)
import construye_juntos as CJ
CO = CR.CO; MC = CR.MC; ME = CR.ME; CV = CR.CV; P = CR.P

# shas de lo importado de escalera/ (congelado, commit 4154993f); si cambian, no corre
SHAS_ESC = {'corre_p1.py': '392b71186cf49b60', 'construye_p1.py': '90dc1b6f848fac80', 'mundo_escalera.py': '4f28b372207ba0a6',
            'mundo_tramo_c.py': '4a1044a4e0e1d5c9', 'construye_c.py': '024a89476109b997', 'corre_c.py': '01e4ad94dd06e133',
            'construye_p7.py': '50179cf58798120c', 'corre_p7.py': '82c3811c144d1a2b'}
SHA_CONSTRUYE_JUNTOS = 'd469c8f3bf194d64'   # fijado al cerrar el preregistro (1-oct); si cambia, no corre
DATOS = os.path.join(AQUI, 'datos'); BITACORA = os.path.join(ESC, 'BITACORA.md')
CARROS = {n: os.path.join(AQUI, 'carros', n + '.py') for n, _, _, _ in CJ.VARIANTES}
CARROS['O1_LUGAR'] = CO.CARROS['O1_LUGAR']
MUEVE = 20000; C_E = 0.01
MUNDO_J = dict(CO.MUNDO_OASIS, mueve=MUEVE, c_e=C_E)
BRAZOS = {'todo': 'O1_TODO', 'sen': 'O1_TODO_SEN', 'preg': 'O1_TODO_PREG', 'lug': 'O1_LUGAR', 'todobar': 'O1_TODO_SBAR'}
#          SENAL, SN_BARAJA, PREGUNTA
PERILLAS = {'todo': (1, 0, 1), 'sen': (1, 0, 0), 'preg': (0, 0, 1), 'lug': (0, 0, 0), 'todobar': (1, 1, 1)}
ORDEN = ('todo', 'sen', 'preg', 'lug', 'todobar'); CAND = 'todo'; PAREJAS = ('sen', 'preg'); BASE = 'lug'; CTRL = 'todobar'
RAFAGA = ('todo', 'sen', 'preg')
SEM = dict(humo=738590, explora=738581, serie=738501, replica=738551)
N_SERIE = 20; T_SERIE = 100000; POOL_MAX = 2
HUMO = dict(n=2, T=30000, mueve=10000); EXPLORA = dict(n=2, T=100000, mueve=MUEVE)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000
GANA_PAR = 13; DIF_SUMA = 10
# BANDAS de validez (suma de cruzan de 180, n 20; se escalan a n): de las series previas, PREREGISTRO sec. 5
BANDAS = {'lug': (60, 115), 'preg': (140, 180), 'sen': (50, 155)}
h16 = CO.h16; med = CO.med; esc = CO.esc; par = CO.par


def modulo(nombre):
    """carga el carro (juntos/carros, verificado contra construye_juntos; O1_LUGAR via corre_c) en ESTE proceso; -> (modulo, estado)."""
    if nombre == 'O1_LUGAR':
        m, est = CR.modulo('O1_LUGAR'); est = dict(est, SENAL=0, SN_BARAJA=0, PREGUNTA=0); return m, est
    ruta = CARROS[nombre]
    if open(ruta, 'rb').read() != CJ.todas()[nombre]: raise SystemExit(f"{ruta} != construye_juntos (correr construye_juntos.py)")
    m = CV._MODS.get(nombre)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{nombre}", ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[nombre] = m
    est = dict(carro=nombre, sha=h16(ruta), LUGAR=m.LUGAR, LUGAR_BARAJA=m.LUGAR_BARAJA, LUGAR_W=m.LUGAR_W, SENAL=m.SENAL, SN_BARAJA=m.SN_BARAJA,
               SN_CADA=m.SN_CADA, SN_UMBRAL=m.SN_UMBRAL, SN_W=m.SN_W, PREGUNTA=m.PREGUNTA, PG_BARAJA=m.PG_BARAJA, PG_OLVIDO=m.PG_OLVIDO)
    return m, est


def tarea(seed, nombre, T, mundo):
    """corre_v143.tarea tal cual (regla 14) con mundo_tramo_c.run en lugar de pista.run; captura la salida cruda. Es corre_c.tarea con el
    cargador de ESTA carpeta y la telemetria de las dos piezas (carro: pg_*; sn: sn_*), en el formato que esperan corre_c.fila_c y corre_p7.fila."""
    _, est = modulo(nombre); est['mundo'] = dict(mundo)
    cap = []; orig = P.run

    def run2(*a, **k):
        r = MC.run(*a, **dict(k, **mundo)); cap.append(r); return r
    P.run = run2
    try:
        x = CV.tarea((seed, nombre, T))
    finally:
        P.run = orig
    r = cap[0]
    for l, d in zip(x['linajes'], r['linajes']): l['_oasis'] = d['_carrera'].get('oasis')
    x['tel'] = [dict(lugar=(dict(d['carro']['lugar'], st_lg_bono=d['carro'].get('lg_bono', 0), st_lg_apr=d['carro'].get('lg_apr', 0), st_lg_viajes=d['carro'].get('lg_viajes', 0))
                            if isinstance(d.get('carro'), dict) and 'lugar' in d['carro'] else None),
                     carro={k: v for k, v in d['carro'].items() if k.startswith(('pl_', 'pg_')) or k in ('plan', 'pregunta', 'mord')} if isinstance(d.get('carro'), dict) else None,
                     sn=({k: v for k, v in d['carro'].items() if k.startswith('sn_')} or None) if isinstance(d.get('carro'), dict) else None)
                for d in r['linajes']]
    x['estado'] = est; x['oasis_info'] = r['pista'].get('oasis')
    return x


def fila(x, T):
    """corre_c.fila_c('preg') (= corre_p1.fila + oasis_info + latencias tras la mudanza) + pizarra / senal / latencia por vida de corre_p7.fila."""
    f = CR.fila_c(x, T, 'preg')
    f7 = R7.fila(x, T)
    f['pizarra'] = f7['pizarra']; f['senal'] = f7['senal']; f['latencia_vida'] = f7['latencia']
    return f


def trabajo(args):
    """UN trabajo: (i, brazo). Atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54); con reanuda salta el que ya existe."""
    i, brazo, base, T, carpeta, reanuda, mundo = args
    fin = os.path.join(carpeta, f"prueba_i{i:02d}_{brazo}.json"); previo = None
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
        previo = x0['aborto']
    t0 = time.time()
    try:
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=None, **fila(tarea(base + i, BRAZOS[brazo], T, mundo), T))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_juntos.md sec. 6)
def _par_menor(A, B, I, k):
    a = [A[i][k] for i in I]; b = [B[i][k] for i in I]
    return dict(n=len(I), gana=sum(x < y for x, y in zip(a, b)), empata=sum(x == y for x, y in zip(a, b)), pierde=sum(x > y for x, y in zip(a, b)),
                med_a=med(a), med_b=med(b), por_indice_a=a, por_indice_b=b)


def lee_serie(R, n, abortos, brazos=ORDEN, mueve=MUEVE, T=T_SERIE, c_e=C_E):
    I = list(range(n)); gp = esc(GANA_PAR, n); dsu = math.ceil(DIF_SUMA * n / 20 - 1e-9)
    completo = all(len(R.get(b, {})) == n for b in brazos)
    letra_ok = completo and all(b in brazos for b in (CAND,) + PAREJAS)
    n_mud = T // mueve - (1 if T % mueve == 0 else 0)
    X = lambda: ((b, i, R[b][i]) for b in brazos for i in R.get(b, {}))
    est = lambda d: d.get('estado') or {}
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(d['coherente'] for _, _, d in X()))
    v['V2_mundo_pide'] = bool(all((d.get('preg') or {}).get('mudanzas') == n_mud and (d.get('oasis_info') or {}).get('mueve') == mueve
                                  and (d.get('oasis_info') or {}).get('c_e') == c_e for _, _, d in X()))
    v['V3_mundo_actua'] = bool(all(d.get('oasis') and d['oasis']['mord_AC_dentro'] > 0 and d['oasis']['extra'] == ME.EXTRA and d['oasis']['pobre'] == ME.POBRE for _, _, d in X()))
    v['V4_estado'] = bool(all(est(d).get('carro') == BRAZOS[b] and est(d).get('LUGAR') == 1 and est(d).get('LUGAR_BARAJA') == 0
                              and (est(d).get('SENAL'), est(d).get('SN_BARAJA'), est(d).get('PREGUNTA')) == PERILLAS[b] and est(d).get('PG_BARAJA', 0) == 0
                              and est(d).get('mundo', {}).get('mueve') == mueve and est(d).get('mundo', {}).get('c_e') == c_e for b, _, d in X()))

    def actua(b, d):
        s, _, p = PERILLAS[b]; pz = d['pizarra']; sn = d.get('senal') or {}; pg = d.get('preg') or {}
        a = (pz['escrituras_total'] > 0 and pz['cobros_total'] > 0 and sn.get('sn_lee', 0) > 0) if s else (pz['escrituras_total'] == 0 and (pz['cobros_total'] or 0) == 0)
        c = (pg.get('pg_exc', 0) > 0 and pg.get('pg_olv', 0) > 0) if p else (pg.get('pg_exc', 0) == 0)
        return a and c
    v['V5_modulos_actuan'] = bool(all(actua(b, d) for b, _, d in X()))
    suma = {b: sum(R[b][i]['cruzan'] for i in R.get(b, {})) for b in brazos}
    ban = {b: (math.floor(lo * n / 20), math.ceil(hi * n / 20)) for b, (lo, hi) in BANDAS.items()}
    v['V6_bandas'] = bool(completo and all(ban[b][0] <= suma[b] <= ban[b][1] for b in ban if b in brazos))
    valido = all(v.values())
    p = {}; q = {}; mejor = None; matiz = None; techo = None
    if letra_ok:
        for k in PAREJAS:
            q[k] = par(R[CAND], R[k], I); q[k + '_inv'] = par(R[k], R[CAND], I)
            p[f'S_par_{k}'] = q[k]['gana'] >= gp; p[f'S_suma_{k}'] = q[k]['dif'] >= dsu
        if CTRL in brazos:
            q[CTRL] = par(R[CAND], R[CTRL], I); p['C_par_todobar'] = q[CTRL]['gana'] >= gp; p['C_suma_todobar'] = q[CTRL]['dif'] >= dsu
        sm = max(suma[k] for k in PAREJAS); mejores = [k for k in PAREJAS if suma[k] == sm]; mejor = mejores if len(mejores) > 1 else mejores[0]
        p['E_estorban'] = all(q[k + '_inv']['gana'] >= gp for k in mejores)     # todo < la mejor pareja (empate de sumas: contra las dos)
        # TECHO (trampa declarada): semillas donde la pareja ya tiene 9/9 no se pueden ganar; alcanzable = n - esas
        techo = {k: dict(semillas_en_9=sum(R[k][i]['cruzan'] == 9 for i in I), ganables=n - sum(R[k][i]['cruzan'] == 9 for i in I), margen_suma=9 * n - suma[k]) for k in PAREJAS}
        techo['SUMAN_alcanzable'] = bool(all(techo[k]['ganables'] >= gp and techo[k]['margen_suma'] >= dsu for k in PAREJAS))
    S = letra_ok and all(p[f'S_par_{k}'] and p[f'S_suma_{k}'] for k in PAREJAS)
    Cc = letra_ok and p.get('C_par_todobar', False) and p.get('C_suma_todobar', False)
    if not valido or not letra_ok: ver = 'NO SE LEE'
    elif S and Cc: ver = 'SUMAN'
    elif p['E_estorban']: ver = 'SE ESTORBAN'
    else:
        ver = 'NO SUMAN'
        if S and not Cc: matiz = 'gana a las parejas pero no al control de contenido (la senal no suma por su contenido)'
        elif not techo['SUMAN_alcanzable']: matiz = 'TECHO: SUMAN no era alcanzable con estas parejas (ver techo)'
    umbral = bool(letra_ok and (any(abs(q[k]['gana'] - gp) <= 1 or abs(q[k]['dif'] - dsu) <= 1 for k in PAREJAS)
                                or any(abs(q[k + '_inv']['gana'] - gp) <= 1 for k in ([mejor] if isinstance(mejor, str) else mejor))))
    sombra = {}; desc = {}
    if letra_ok:
        # SOMBRA (no cambia la letra): donde cruzan satura, el establecimiento y la busqueda tienen recorrido (menor gana)
        for k in PAREJAS:
            sombra[f'fund_todo_menor_que_{k}'] = _par_menor(R[CAND], R[k], I, 'fund_media')
            sombra[f'latencia_todo_menor_que_{k}'] = _par_menor(R[CAND], R[k], I, 'lat_med')
        sombra['SUMAN_en_sombra'] = bool(all(sombra[f'fund_todo_menor_que_{k}']['gana'] >= gp or sombra[f'latencia_todo_menor_que_{k}']['gana'] >= gp for k in PAREJAS))
        D = lambda f: {b: f(b) for b in brazos}
        desc['suma_cruzan'] = suma
        desc['mayorias'] = D(lambda b: sum(R[b][i]['mayoria'] for i in I))
        desc['R0_med'] = D(lambda b: med([R[b][i]['R0_med'] for i in I]))
        desc['fund_media'] = D(lambda b: med([R[b][i]['fund_media'] for i in I]))
        desc['establecidos_0fund_post10k'] = D(lambda b: sum(sum(int(z == 0) for z in R[b][i]['fund_post10k']) for i in I))
        desc['vida_med'] = D(lambda b: med([R[b][i]['vida_med'] for i in I]))
        desc['latencia_mudanza_med'] = D(lambda b: med([R[b][i]['lat_med'] for i in I]))
        desc['nunca_llegan'] = D(lambda b: sum((R[b][i].get('preg') or {}).get('nunca', 0) for i in I))
        desc['mundo_AC'] = D(lambda b: med([R[b][i]['mundo_AC'] for i in I]))
        desc['mundo_AC_todo_sobre_lug'] = (round(desc['mundo_AC'][CAND] / desc['mundo_AC'][BASE], 3) if desc['mundo_AC'].get(BASE) else None)   # trampa 3: se reporta
        desc['ratio_pasos_oasis'] = D(lambda b: med([R[b][i]['oasis']['ratio_pasos'] for i in I]))
        desc['escrituras'] = D(lambda b: med([R[b][i]['pizarra']['escrituras_total'] for i in I]))
        desc['siembras'] = D(lambda b: med([(R[b][i].get('senal') or {}).get('sn_siembra', 0) for i in I]))
        desc['excursiones'] = D(lambda b: med([(R[b][i].get('preg') or {}).get('pg_exc') for i in I]))
        desc['olvidos'] = D(lambda b: med([(R[b][i].get('preg') or {}).get('pg_olv') for i in I]))
        desc['bandas'] = {b: dict(banda=ban[b], suma=suma[b]) for b in ban if b in brazos}
        desc['pareados'] = {f"{a}_vs_{c}": par(R[a], R[c], I) for a in brazos for c in brazos if a != c and (a == CAND or c == BASE)}
    return dict(validez=v, puertas=p, veredicto=ver, matiz=matiz, en_umbral=umbral, umbrales=dict(gana_par=gp, dif_suma=dsu), mejor_pareja=mejor, techo=techo,
                pareados={k: q[k] for k in q}, sombra=sombra, descriptivo=desc)


def lee(carpeta):
    R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        d['fund_media'] = float(st.mean(d['fund'])); d['lat_med'] = (d.get('preg') or {}).get('latencia_med')
        if d['lat_med'] is None: d['lat_med'] = float(d['T'])
        R.setdefault(d['brazo'], {})[d['i']] = d
    return R, ab


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  puertas: {L['puertas']} · umbrales {L['umbrales']} · mejor pareja {L['mejor_pareja']} · EN EL UMBRAL (+-1): {L['en_umbral']} · matiz {L['matiz']}")
    log(f"  techo: {L['techo']}")
    for k, q in L['pareados'].items():
        if not k.endswith('_inv'): log(f"  todo vs {k}: gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · suma {q['suma_a']} vs {q['suma_b']} (dif {q['dif']}) · por indice {q['por_indice_a']} vs {q['por_indice_b']}")
    for k, q in L['sombra'].items():
        log(f"  [sombra] {k}: " + (f"gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · mediana {q['med_a']} vs {q['med_b']}" if isinstance(q, dict) else str(q)))
    for k, v in L['descriptivo'].items():
        if k != 'pareados': log(f"  [desc] {k}: {v}")


def verifica(log):
    ok = CO.verifica(log)
    for nm, sha in SHAS_ESC.items():
        s = h16(os.path.join(ESC, nm)); ok &= s == sha; log(f"  sha {nm} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    s = h16(os.path.join(AQUI, 'construye_juntos.py')); fij = SHA_CONSTRUYE_JUNTOS is not None; ok &= (s == SHA_CONSTRUYE_JUNTOS) if fij else True
    log(f"  sha construye_juntos.py {s} {'OK' if (not fij or s == SHA_CONSTRUYE_JUNTOS) else '!= ' + SHA_CONSTRUYE_JUNTOS + ' FALLA'}{'' if fij else ' (NO FIJADO: solo humo/explora)'}")
    for nm, b in CJ.todas().items():
        igual = os.path.exists(CARROS[nm]) and open(CARROS[nm], 'rb').read() == b; ok &= igual
        log(f"  carro {nm} == construye_juntos: {igual} (sha {h16(CARROS[nm]) if os.path.exists(CARROS[nm]) else 'NO EXISTE'})")
    log(f"  mundo_tramo_c: {MC.construye()[1]}")
    return ok


def identidad_corta(log, seed=738530, T=1500):
    """En el mundo de la serie (mueve + c_e; salida ENTERA): TODO0 == O1_LUGAR; TODO_SEN == O1_LUGAR_SENAL; TODO_PREG == O1_LUGAR_PREG; TODO != cada pareja."""
    N = lambda x: json.loads(json.dumps(x, default=str))
    kw = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **dict(MUNDO_J, mueve=T // 3))
    run = lambda m: N(MC.run(seed, [('X', m)] * 9, **kw))
    lug, _ = CR.modulo('O1_LUGAR'); pg, _ = CR.modulo('O1_LUGAR_PREG'); R7.fija('sen'); sn = CV._MODS['O1_LUGAR_SENAL']
    t0, _ = modulo('O1_TODO0'); ts, _ = modulo('O1_TODO_SEN'); tp, _ = modulo('O1_TODO_PREG'); tt, _ = modulo('O1_TODO')
    rs = run(ts); rp = run(tp); rt = run(tt)
    i1 = run(t0) == run(lug); i2 = rs == run(sn); i3 = rp == run(pg); i4 = rt != rs and rt != rp
    log(f"  IDENTIDAD CORTA JUNTOS (salida ENTERA, N 9, s {seed}, T {T}, mueve {T // 3}, c_e {C_E}): TODO0 == O1_LUGAR {i1} · TODO_SEN == O1_LUGAR_SENAL {i2} · TODO_PREG == O1_LUGAR_PREG {i3} · TODO != parejas {i4}")
    return i1 and i2 and i3 and i4


def guarda(modo, pre, reanuda):
    """Candados de --serie/--replica (PREREGISTRO_juntos.md sec. 7): como corre_p10.guarda."""
    if SHA_CONSTRUYE_JUNTOS is None: return "SHA_CONSTRUYE_JUNTOS sin fijar (fijar al cerrar el preregistro)"
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if r.get('modo') == modo and (r.get('letra') or {}).get('veredicto') in ('SUMAN', 'SE ESTORBAN', 'NO SUMAN'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda (cortada o NO SE LEE)"
    if modo == 'replica':
        rsm = sorted(glob.glob(os.path.join(DATOS, f"juntos_serie_s{SEM['serie']}-*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto'); um = (rs0.get('letra') or {}).get('en_umbral')
        if not (vs in ('SUMAN', 'SE ESTORBAN') or (vs == 'NO SUMAN' and um)):
            return f"REGLA DE PARADA: la replica solo si la serie da SUMAN, SE ESTORBAN o NO SUMAN EN EL UMBRAL; serie = {vs} (umbral {um})"
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)): return f"sha_runner de la serie {rs0.get('sha_runner')} != runner actual"
    import subprocess
    archivos = ([os.path.join(AQUI, 'PREREGISTRO_juntos.md'), os.path.abspath(__file__), os.path.join(AQUI, 'construye_juntos.py')]
                + [os.path.join(ESC, k) for k in SHAS_ESC] + list(CARROS.values()))
    for r in archivos:
        rel = os.path.relpath(r, RAIZ).replace(os.sep, '/')
        t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
        c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
        if not (t and c): return f"git: {rel} commiteado {t} · sin cambios vs HEAD {c} (la serie exige todo commiteado)"
    return None


def bitacora(linea):
    with open(BITACORA, 'a', encoding='utf-8') as fh: fh.write(linea + '\n')


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true')
    g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--n', type=int, default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--desde', type=int, default=None); ap.add_argument('--nota', default=''); ap.add_argument('--mueve', type=int, default=None)
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX}")
    if a.lee:
        R, ab = lee(os.path.abspath(a.lee)); brazos = tuple(b for b in ORDEN if R.get(b))
        if not brazos: raise SystemExit(f"--lee: no hay prueba_i*_*.json validos en {a.lee} (abortos {ab})")
        n = max(len(R[b]) for b in brazos)
        x0 = R[brazos[0]][min(R[brazos[0]])]; mv = (x0.get('oasis_info') or {}).get('mueve') or MUEVE
        L = lee_serie(R, n, len(ab), brazos, mueve=mv, T=x0['T']); imprime(L, print)
        print(f"VEREDICTO ({'parcial/humo, no cuenta' if n != N_SERIE or set(brazos) != set(ORDEN) or x0['T'] != T_SERIE or mv != MUEVE else 'letra'}): {L['veredicto']} · abortos {ab}")
        return 0
    if a.humo or a.explora:
        if a.pool: raise SystemExit("--humo/--explora: sin Pool (un proceso)")
        modo = 'humo' if a.humo else 'explora'; cfg = HUMO if a.humo else EXPLORA
        n = a.n or cfg['n']; T = a.T or cfg['T']; brazos = tuple(a.brazos.split(',')) if a.brazos else RAFAGA; base = a.desde or SEM[modo]; mv = a.mueve or cfg['mueve']
        if len(brazos) * n > MAX_CORRIDAS_1P or T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(brazos) * n}) y <= {MAX_PASOS_1P} pasos (T {T})")
        dest = os.path.join(DATOS, modo)
    else:
        if a.T or a.n or a.brazos or a.desde or a.mueve: raise SystemExit("--serie/--replica: T, n, brazos, mueve y semillas los fija el preregistro")
        modo = 'serie' if a.serie else 'replica'; n = N_SERIE; T = T_SERIE; brazos = ORDEN; base = SEM[modo]; dest = DATOS; mv = MUEVE
    for b in brazos:
        if b not in BRAZOS: raise SystemExit(f"brazo desconocido {b}")
    mundo = dict(MUNDO_J, mueve=mv)
    pre = f"{'juntos_' if modo in ('serie', 'replica') else ''}{modo}_s{base}-{base + n - 1}_T{T}_m{mv}"
    sel = time.strftime('%Y%m%d_%H%M%S')
    prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
    if a.reanuda and not prev: raise SystemExit(f"--reanuda: no hay carpeta {pre}_* en {dest}")
    if modo in ('serie', 'replica'):
        e = guarda(modo, pre, a.reanuda)
        if e: raise SystemExit(f"NO SE CORRE (candado): {e}")
    carpeta = os.path.join(dest, prev[-1]) if (a.reanuda and prev) else os.path.join(dest, pre + '_' + sel)
    BUF = []; LOGF = [None]

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"
        print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    t0 = time.time()
    log(f"CORRE_JUNTOS · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_juntos.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  semillas {base}-{base + n - 1} · T {T} · brazos {list(brazos)} · mundo {mundo} · reanuda {a.reanuda} · nota {a.nota!r}")
    ok = verifica(log) and CO.identidad_corta(log) and CR.identidad_corta_c(log) and identidad_corta(log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    tareas = [(i, b, base, T, carpeta, a.reanuda, mundo) for i in range(n) for b in brazos]

    def fmt(x):
        oz = x.get('oasis') or {}; pg = x.get('preg') or {}; pz = x.get('pizarra') or {}; sn = x.get('senal') or {}
        return (f"  [{time.time()-t0:7.1f}s] i{x['i']} {x['brazo']:7s} ({x.get('seg')}s) aborto {x.get('aborto')} cruzan {x.get('cruzan')}/9 R0 {x.get('R0_med')} "
                f"fund {x.get('fund')} · oasis ratio pasos {oz.get('ratio_pasos')} · latencia {pg.get('latencia_med')} nunca {pg.get('nunca')} mudanzas {pg.get('mudanzas')} "
                f"exc {pg.get('pg_exc')} olv {pg.get('pg_olv')} · escribe {pz.get('escrituras_total')} cobros {pz.get('cobros_total')} lee {sn.get('sn_lee')} siembra {sn.get('sn_siembra')} · mundo AC {x.get('mundo_AC')}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): log(fmt(x))
    else:
        for tk in tareas: log(fmt(trabajo(tk)))
    R, ab = lee(carpeta); L = lee_serie(R, n, len(ab), brazos, mueve=mv, T=T)
    log(f"\n================ LA LETRA (escalada a n {n})" + (" -- HUMO/EXPLORA: NO cuenta, no se declara" if modo in ('humo', 'explora') else ""))
    imprime(L, log)
    if ab: log(f"  ABORTOS: {ab}")
    ver = (f"{modo.upper()} (no cuenta): " if modo in ('humo', 'explora') else '') + L['veredicto'] + (f" ({L['matiz']})" if L.get('matiz') else '')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, letra=L, abortos=ab, n=n, T=T, brazos=list(brazos), semillas=[base, base + n - 1], veredicto=ver, nota=a.nota, mundo=mundo,
                       sha_runner=h16(os.path.abspath(__file__)), sha_construye_juntos=h16(os.path.join(AQUI, 'construye_juntos.py')),
                       shas_esc={k: h16(os.path.join(ESC, k)) for k in SHAS_ESC},
                       shas={os.path.relpath(k, RAIZ): v for k, v in CO.SHAS.items()}, carros={k: h16(v) for k, v in CARROS.items()},
                       mundo_c=MC.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {len(ab)} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO: {ver}")
    if modo in ('humo', 'explora'):
        d = L['descriptivo']
        if not d:   # brazos parciales (sin las tres de la letra): descriptivo minimo
            bs = [b for b in brazos if R.get(b)]
            d = dict(suma_cruzan={b: sum(x['cruzan'] for x in R[b].values()) for b in bs}, fund_media={b: med([x['fund_media'] for x in R[b].values()]) for b in bs},
                     latencia_mudanza_med={b: med([x['lat_med'] for x in R[b].values()]) for b in bs}, mayorias={b: sum(x['mayoria'] for x in R[b].values()) for b in bs})
        q = L.get('pareados') or {}
        bitacora(f"| {time.strftime('%Y-%m-%d %H:%M')} | JUNTOS p1+p7+p10 (corre_juntos, mueve {mv}, c_e {C_E}) | {modo} s{base}-{base + n - 1} T{T} {list(brazos)} carro {h16(CARROS['O1_TODO'])} {a.nota} | "
                 f"cruzan {d.get('suma_cruzan')} · mayorias {d.get('mayorias')} · fund {d.get('fund_media')} · latencia {d.get('latencia_mudanza_med')} · nunca {d.get('nunca_llegan')} · "
                 f"mundo AC {d.get('mundo_AC')} · todo-sen {(q.get('sen') or {}).get('dif')} todo-preg {(q.get('preg') or {}).get('dif')} todo-todobar {(q.get('todobar') or {}).get('dif')} · techo {L.get('techo')} · "
                 f"abortos {len(ab)} · {os.path.relpath(carpeta, ESC)} | {L['veredicto'] if L['veredicto'] != 'NO SE LEE' else 'no se lee (parcial)'} |")
    return 0


if __name__ == '__main__':
    sys.exit(main())
