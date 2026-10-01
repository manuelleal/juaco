"""corre_p7.py — RUNNER del peldano 7 de la escalera: COMUNICACION CON SIGNIFICADO DADO por la pizarra (O1_LUGAR_SENAL) en el mundo de P1b
con COSTO DE EMITIR (mundo_tramo_c, c_e). 30-sep-2026, ingeniero genetico Fable. Preregistro: PREREGISTRO_p7.md. Arnes: identidad_p7.py.
Escalera: ESCALERA.md (P7). Carros: construye_p7.py (sobre el texto de O1_LUGAR de construye_p1, sha fijado). Bitacora: BITACORA.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE SE CORRE (cada corrida ES corre_v143.tarea, que se IMPORTA y no se toca = juez.tarea(seed, 9 carros iguales, T, pizarra 1, rep_acum 0,
escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje; con mundo_tramo_c.run en lugar de pista.run (= mundo_escalera.run +
c_e; con c_e 0 es mundo_escalera bit a bit y con oasis 0 la pista). Lo comun de la fila lo arma corre_p1.fila (corre_p1 esta CONGELADO y
commiteado: se importa, su sha se fija aqui; NO se toca). Lo agregado: 'pizarra' (escrituras, cobros: fisica), 'senal' (telemetria del
carro: lee/siembra, no puntua), 'latencia' (fisica: pasos desde el nacimiento hasta el primer bocado dentro, por vida) y 'estado'.
  BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, fundador limpio; mundo P1b + c_e 0.01):
    sen     O1_LUGAR_SENAL      emite (bin, bono) cuando su memoria de lugar supera SN_UMBRAL; lee y SIEMBRA donde no ha estado   EL CANDIDATO
    senbar  O1_LUGAR_SENAL_BAR  emite igual; LEE el bin ANTIPODA (b + 15 mod 30): mismo canal, mismo costo, contenido equivocado  CONTROL
    lug     O1_LUGAR            ni emite ni lee (MUDO): la BASE del peldano (P1)
MEDIDA PRINCIPAL: linajes que cruzan (cruza_real del juez), por semilla y suma. CO-PRINCIPAL (director): FUNDADORES por linaje (menos = el
linaje se establece). MECANISMO (fisica): latencia mediana por vida hasta el primer bocado dentro del oasis (llega ANTES).
SEMILLAS NUEVAS (grep 30-sep: 7396xx-7397xx no aparecen fuera de la escalera): serie 739601-739620 · replica 739651-739670 ·
humo 739790-739795 (739790-739791 usados en los humos 1-2 SIN costo; el humo 3 con costo usa 739792-739793) · explora 739701-739705
(739701-739702 usados en la exploracion 1 SIN costo) · arnes 739750-739759.
MODO RAFAGA: --humo y --explora son de UN proceso (<= 6 corridas, <= 200k pasos); NADA se declara; --serie/--replica (pool <= 2) SOLO el
coordinador, con preregistro y git limpio (candados en guarda()).

  python experimentos/organelos/escalera/corre_p7.py --humo [--desde 739792] [--T 30000] [--n 2] [--brazos sen,senbar,lug] [--c_e 0.01] [--nota '...']
  python experimentos/organelos/escalera/corre_p7.py --explora [--desde 739703]
  python experimentos/organelos/escalera/corre_p7.py --serie --pool 2 [--reanuda]      (solo el coordinador; 20 semillas x 3 brazos)
  python experimentos/organelos/escalera/corre_p7.py --replica --pool 2
  python experimentos/organelos/escalera/corre_p7.py --lee <carpeta>
"""
import argparse, glob, importlib.util, json, math, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path.insert(0, AQUI)
import corre_p1 as CO            # CONGELADO (76dc3d11): se importa, no se toca
import construye_p7 as C7
import mundo_tramo_c as MC
CV = CO.CV; P = CO.P; ME = CO.ME; J = CO.J

SHA_CORRE_P1 = '392b71186cf49b60'
SHA_MUNDO_TRAMO_C = '4a1044a4e0e1d5c9'   # auditoria P7 H-4: el mundo del tramo C se fija por sha (si cambia, no se corre). Re-fijado una vez tras
# agregar la perilla cerrojo_pobre (P9, humo 2; default 1 = bit a bit; P7 no la usa): el 1a423097d67f2203 fue el del humo 3 (declarado en PREREGISTRO sec. 12)
DATOS = os.path.join(AQUI, 'datos'); BITACORA = os.path.join(AQUI, 'BITACORA.md')
CARROS = {n: os.path.join(AQUI, 'carros', n + '.py') for n, _, _ in C7.VARIANTES}
CARROS['O1_LUGAR'] = CO.CARROS['O1_LUGAR']
C_E = 0.01
MUNDO_P7 = dict(CO.MUNDO_OASIS, c_e=C_E)          # oasis 1, extra 0.8, pobre 0.5, dens 0.5, vista_r 20 + costo de emitir
BRAZOS = {'sen': ('O1_LUGAR_SENAL', MUNDO_P7), 'senbar': ('O1_LUGAR_SENAL_BAR', MUNDO_P7), 'lug': ('O1_LUGAR', MUNDO_P7)}
ORDEN = ('sen', 'senbar', 'lug'); CAND = 'sen'; CTRL = 'senbar'; BASE = 'lug'; RAFAGA = ORDEN
SEM = dict(humo=739790, explora=739701, serie=739601, replica=739651)
N_SERIE = 20; T_SERIE = 100000; POOL_MAX = 2
HUMO = dict(n=2, T=30000); EXPLORA = dict(n=2, T=100000)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000
GANA_PAR = 13; DIF_SUMA = 10
h16 = CO.h16; med = CO.med; esc = CO.esc; par = CO.par


# ------------------------------------------------------------------ estado por proceso (cfg por worker)
def fija(brazo):
    """Carga en ESTE proceso el carro del brazo (verificado contra su constructor) y lo registra en corre_v143._MODS; -> estado (V4)."""
    n, mundo = BRAZOS[brazo]
    if n == 'O1_LUGAR':
        est = CO.fija('lug'); est['mundo'] = dict(mundo); est.update(SENAL=0, SN_BARAJA=0); return est
    ruta = CARROS[n]
    if open(ruta, 'rb').read() != C7.todas()[n]: raise SystemExit(f"{ruta} != construye_p7 (correr construye_p7.py)")
    m = CV._MODS.get(n)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{n}", ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    return dict(carro=n, sha=h16(ruta), LUGAR=m.LUGAR, LUGAR_BARAJA=m.LUGAR_BARAJA, LUGAR_W=m.LUGAR_W, SENAL=m.SENAL, SN_BARAJA=m.SN_BARAJA,
                SN_CADA=m.SN_CADA, SN_UMBRAL=m.SN_UMBRAL, SN_W=m.SN_W, mundo=dict(mundo))


def tarea(seed, brazo, T, mundo=None):
    """corre_v143.tarea tal cual (regla 14) con mundo_tramo_c.run en lugar de pista.run; captura la salida cruda (oasis, pizarra, carro)."""
    est = fija(brazo); n = BRAZOS[brazo][0]
    mk = dict(BRAZOS[brazo][1] if mundo is None else mundo); est['mundo'] = dict(mk)
    cap = []; orig = P.run

    def run2(*a, **k):
        r = MC.run(*a, **dict(k, **mk)); cap.append(r); return r
    P.run = run2
    try:
        x = CV.tarea((seed, n, T))
    finally:
        P.run = orig
    r = cap[0]
    for l, d in zip(x['linajes'], r['linajes']): l['_oasis'] = d['_carrera'].get('oasis')
    x['tel'] = [dict(lugar=(dict(d['carro']['lugar'], st_lg_bono=d['carro'].get('lg_bono', 0), st_lg_apr=d['carro'].get('lg_apr', 0), st_lg_viajes=d['carro'].get('lg_viajes', 0))
                            if isinstance(d.get('carro'), dict) and 'lugar' in d['carro'] else None),
                     sn=({k: v for k, v in d['carro'].items() if k.startswith('sn_')} or None) if isinstance(d.get('carro'), dict) else None) for d in r['linajes']]
    x['estado'] = est
    return x


def fila(x, T):
    """corre_p1.fila (comun) + pizarra (fisica), senal (carro, no puntua), latencia (fisica)."""
    f = CO.fila(x, T)
    L = x['linajes']; ol = [l.get('_oasis') or {} for l in L]
    f['pizarra'] = dict(escrituras=[l.get('escrituras') for l in L], escrituras_total=sum(l.get('escrituras') or 0 for l in L),
                        cobros=[o.get('cobros') for o in ol], cobros_total=sum(o.get('cobros') or 0 for o in ol), c_e=(x.get('estado') or {}).get('mundo', {}).get('c_e'))
    sn = [t.get('sn') for t in (x.get('tel') or []) if t and t.get('sn')]
    f['senal'] = ({k: sum(t[k] for t in sn) for k in ('sn_escribe', 'sn_lee', 'sn_siembra')} if sn else None)
    lat = [v for o in ol for v in (o.get('latencia_vida') or [])]
    vidas = sum(l['muertes'] + 1 for l in L)
    # H-6 (auditoria): la latencia solo existe en vidas que LLEGARON a morder dentro (sesgo de supervivencia, conservador); se agrega la fraccion
    f['latencia'] = dict(med=med(lat), n=len(lat), vidas=vidas, frac_vidas=(round(len(lat) / vidas, 4) if vidas else None))
    return f


def trabajo(args):
    """UN trabajo: (i, brazo). Atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54); con reanuda salta el que ya existe."""
    i, brazo, base, T, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"prueba_i{i:02d}_{brazo}.json"); previo = None
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
        previo = x0['aborto']
    t0 = time.time()
    try:
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=None, **fila(tarea(base + i, brazo, T), T))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_p7.md sec. 6)
def par_menor(A, B, I, k):
    a = [A[i][k] for i in I]; b = [B[i][k] for i in I]
    return dict(n=len(I), gana=sum(x < y for x, y in zip(a, b)), empata=sum(x == y for x, y in zip(a, b)), pierde=sum(x > y for x, y in zip(a, b)),
                med_a=med(a), med_b=med(b), por_indice_a=a, por_indice_b=b)


def lee_serie(R, n, abortos, brazos=ORDEN):
    I = list(range(n)); gp = esc(GANA_PAR, n); dsu = math.ceil(DIF_SUMA * n / 20 - 1e-9)
    completo = all(len(R.get(b, {})) == n for b in brazos)
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(R[b][i]['coherente'] for b in brazos for i in R.get(b, {})))
    v['V2_canal_actua'] = bool(all(R[b][i]['pizarra']['escrituras_total'] > 0 and R[b][i]['pizarra']['cobros_total'] > 0 and (R[b][i].get('senal') or {}).get('sn_lee', 0) > 0
                                   for b in (CAND, CTRL) if b in brazos for i in R.get(b, {}))
                               and all((R[CAND][i].get('senal') or {}).get('sn_siembra', 0) > 0 for i in R.get(CAND, {}))
                               and all(R[BASE][i]['pizarra']['escrituras_total'] == 0 for i in R.get(BASE, {})))
    v['V3_mundo_actua'] = bool(all(R[b][i].get('oasis') and R[b][i]['oasis']['mord_AC_dentro'] > 0 and R[b][i]['oasis']['extra'] == ME.EXTRA
                                   and R[b][i]['oasis']['pobre'] == ME.POBRE and R[b][i]['pizarra']['c_e'] == C_E for b in brazos for i in R.get(b, {})))
    est = lambda d: d.get('estado') or {}
    v['V4_estado'] = bool(all(est(R[b][i]).get('carro') == BRAZOS[b][0] and est(R[b][i]).get('mundo') == BRAZOS[b][1] and est(R[b][i]).get('LUGAR') == 1
                              and est(R[b][i]).get('SENAL') == int(b != BASE) and est(R[b][i]).get('SN_BARAJA') == int(b == CTRL) and est(R[b][i]).get('LUGAR_BARAJA') == 0
                              for b in brazos for i in R.get(b, {})))
    valido = all(v.values()); ok = valido or completo
    p = {}; pa = pb = pf = pm = None
    if ok:
        pa = par(R[CAND], R[BASE], I); pb = par(R[CAND], R[CTRL], I)
        pf = par_menor(R[CAND], R[BASE], I, 'fund_media')
        # H-9 (tras el humo 3, antes de datos de serie; candidato a ERR-175): PM = fraccion de vidas que LLEGAN a morder dentro (mayor gana);
        # la latencia (menor gana) queda como descriptivo porque lleva el sesgo de supervivencia declarado en H-6 (en el humo 3 fallo en esa direccion)
        pm = par_menor(R[BASE], R[CAND], I, 'frac_vidas'); pm['med_a'], pm['med_b'] = pm['med_b'], pm['med_a']; pm['por_indice_a'], pm['por_indice_b'] = pm['por_indice_b'], pm['por_indice_a']
        pl = par_menor(R[CAND], R[BASE], I, 'lat_med')
        p['PA_par_lug'] = pa['gana'] >= gp; p['PA_suma_lug'] = pa['dif'] >= dsu
        p['PB_par_senbar'] = pb['gana'] >= gp; p['PB_suma_senbar'] = pb['dif'] >= dsu
        p['PF_fund_par'] = pf['gana'] >= gp
        p['PM_llegan_mas'] = pm['gana'] >= gp
    umbral = bool(ok and (any(abs(q['gana'] - gp) <= 1 for q in (pa, pb, pf, pm)) or any(abs(q['dif'] - dsu) <= 1 for q in (pa, pb))))
    matiz = None
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif ((p['PA_par_lug'] or p['PA_suma_lug']) or p['PF_fund_par']) and (p['PB_par_senbar'] or p['PB_suma_senbar']) and p['PM_llegan_mas']: ver = 'HAY ALGO MODESTO'
    elif ((p['PA_par_lug'] or p['PA_suma_lug']) or p['PF_fund_par']) and (p['PB_par_senbar'] or p['PB_suma_senbar']): ver = 'NO'; matiz = 'gana sin que lleguen mas vidas al oasis (instrumento)'
    else: ver = 'NO'
    desc = {}
    if ok:
        desc['suma_cruzan'] = {b: sum(R[b][i]['cruzan'] for i in I) for b in brazos}
        desc['mayorias'] = {b: sum(R[b][i]['mayoria'] for i in I) for b in brazos}
        desc['R0_med'] = {b: med([R[b][i]['R0_med'] for i in I]) for b in brazos}
        desc['fund_media'] = {b: med([R[b][i]['fund_media'] for i in I]) for b in brazos}
        desc['establecidos_0fund_post10k'] = {b: sum(sum(int(z == 0) for z in R[b][i]['fund_post10k']) for i in I) for b in brazos}
        desc['vida_med'] = {b: med([R[b][i]['vida_med'] for i in I]) for b in brazos}
        desc['latencia_med'] = {b: med([R[b][i]['lat_med'] for i in I]) for b in brazos}
        desc['frac_vidas_con_bocado_dentro'] = {b: med([(R[b][i].get('latencia') or {}).get('frac_vidas') for i in I]) for b in brazos}
        desc['mundo_AC'] = {b: med([R[b][i]['mundo_AC'] for i in I]) for b in brazos}
        desc['ratio_pasos_oasis'] = {b: med([R[b][i]['oasis']['ratio_pasos'] for i in I]) for b in brazos}
        desc['escrituras'] = {b: med([R[b][i]['pizarra']['escrituras_total'] for i in I]) for b in brazos}
        desc['cobros'] = {b: med([R[b][i]['pizarra']['cobros_total'] for i in I]) for b in brazos}
        desc['siembras'] = {b: med([(R[b][i].get('senal') or {}).get('sn_siembra') for i in I]) for b in brazos}
        desc['linajes_que_escriben'] = {b: sum(sum(int(e > 0) for e in R[b][i]['pizarra']['escrituras']) for i in I) for b in brazos}
        desc['pareados'] = {f"{a}_vs_{c}": par(R[a], R[c], I) for a, c in (('sen', 'lug'), ('sen', 'senbar'), ('senbar', 'lug')) if a in brazos and c in brazos}
    return dict(validez=v, puertas=p, veredicto=ver, matiz=matiz, en_umbral=umbral, umbrales=dict(gana_par=gp, dif_suma=dsu),
                pareado_lug=pa, pareado_senbar=pb, pareado_fund=pf, pareado_frac_vidas=pm, pareado_latencia=(pl if ok else None), descriptivo=desc)


def lee(carpeta):
    R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        d['fund_media'] = float(st.mean(d['fund'])); d['lat_med'] = (d.get('latencia') or {}).get('med')
        if d['lat_med'] is None: d['lat_med'] = float(d['T'])
        d['frac_vidas'] = (d.get('latencia') or {}).get('frac_vidas') or 0.0
        R[d['brazo']][d['i']] = d
    return R, ab


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  puertas: {L['puertas']} · umbrales {L['umbrales']} · EN EL UMBRAL (+-1): {L['en_umbral']} · matiz {L['matiz']}")
    for k in ('pareado_lug', 'pareado_senbar'):
        q = L[k]
        if q: log(f"  {k}: gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · suma {q['suma_a']} vs {q['suma_b']} (dif {q['dif']}) · por indice {q['por_indice_a']} vs {q['por_indice_b']}")
    for k, s in (('pareado_fund', 'menor gana'), ('pareado_frac_vidas', 'mayor gana: PM'), ('pareado_latencia', 'menor gana: descriptivo')):
        q = L.get(k)
        if q: log(f"  {k} ({s}): gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · mediana {q['med_a']} vs {q['med_b']}")
    for k, v in L['descriptivo'].items():
        if k != 'pareados': log(f"  [desc] {k}: {v}")


def verifica(log):
    ok = CO.verifica(log)
    s1 = h16(os.path.join(AQUI, 'corre_p1.py')); ok &= s1 == SHA_CORRE_P1; log(f"  sha corre_p1.py {s1} {'OK' if s1 == SHA_CORRE_P1 else '!= ' + SHA_CORRE_P1 + ' FALLA'}")
    s2 = h16(os.path.join(AQUI, 'mundo_tramo_c.py')); ok &= s2 == SHA_MUNDO_TRAMO_C; log(f"  sha mundo_tramo_c.py {s2} {'OK' if s2 == SHA_MUNDO_TRAMO_C else '!= ' + SHA_MUNDO_TRAMO_C + ' FALLA'}")
    for nm, b in C7.todas().items():
        igual = os.path.exists(CARROS[nm]) and open(CARROS[nm], 'rb').read() == b; ok &= igual
        log(f"  carro {nm} == construye_p7: {igual} (sha {h16(CARROS[nm]) if os.path.exists(CARROS[nm]) else 'NO EXISTE'})")
    log(f"  mundo_tramo_c: {MC.construye()[1]}")
    return ok


def identidad_corta(log, seed=739750, T=1500):
    """(1) mundo_tramo_c con c_e 0 == mundo_escalera (salida entera); (2) SENAL0 == O1_LUGAR; (3) SENAL con la pizarra apagada == O1_LUGAR (linajes)."""
    N = lambda x: json.loads(json.dumps(x, default=str))
    fija('lug'); lug = CV._MODS['O1_LUGAR']; fija('sen'); sen = CV._MODS['O1_LUGAR_SENAL']
    spec = importlib.util.spec_from_file_location('carro_O1_LUGAR_SENAL0', CARROS['O1_LUGAR_SENAL0']); s0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(s0)
    kw = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **CO.MUNDO_OASIS)
    base = N(ME.run(seed, [('X', lug)] * 9, **kw))
    i1 = N(MC.run(seed, [('X', lug)] * 9, **kw)) == base
    i2 = N(MC.run(seed, [('X', s0)] * 9, **kw)) == base

    def lin(r):
        r = N(r)['linajes']
        for d in r:
            for k in ('sn_escribe', 'sn_lee', 'sn_siembra'): d['carro'].pop(k, None)
            d['_carrera']['oasis'].pop('latencia_vida', None); d['_carrera']['oasis'].pop('cobros', None)
        return r
    i3 = lin(MC.run(seed, [('X', sen)] * 9, **dict(kw, pizarra=0, c_e=C_E))) == lin(ME.run(seed, [('X', lug)] * 9, **dict(kw, pizarra=0)))
    log(f"  IDENTIDAD CORTA P7 (salida ENTERA, N 9, s {seed}, T {T}): mundo_tramo_c c_e 0 == mundo_escalera {i1} · SENAL0 == O1_LUGAR {i2} · SENAL con pizarra 0 y c_e {C_E} == O1_LUGAR (mudo == base) {i3}")
    return i1 and i2 and i3


def guarda(modo, pre, reanuda):
    """Candados de --serie/--replica (PREREGISTRO_p7.md sec. 7): como corre_p1.guarda, con los archivos de P7 y los de P1 de los que depende."""
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if r.get('modo') == modo and (r.get('letra') or {}).get('veredicto') in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda (cortada o NO SE LEE)"
    if modo == 'replica':
        rsm = sorted(glob.glob(os.path.join(DATOS, f"p7_serie_s{SEM['serie']}-*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto'); um = (rs0.get('letra') or {}).get('en_umbral')
        if not (vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um)):
            return f"REGLA DE PARADA: la replica solo si la serie da FUNCIONA, MODESTO o NO EN EL UMBRAL; serie = {vs} (umbral {um})"
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)): return f"sha_runner de la serie {rs0.get('sha_runner')} != runner actual"
    import subprocess
    archivos = [os.path.join(AQUI, 'PREREGISTRO_p7.md'), os.path.abspath(__file__), os.path.join(AQUI, 'construye_p7.py'), os.path.join(AQUI, 'mundo_tramo_c.py'),
                os.path.join(AQUI, 'construye_p1.py'), os.path.join(AQUI, 'mundo_escalera.py'), os.path.join(AQUI, 'corre_p1.py')] + [CARROS[n] for n, _, _ in C7.VARIANTES] + [CARROS['O1_LUGAR']]
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
    ap.add_argument('--desde', type=int, default=None); ap.add_argument('--nota', default=''); ap.add_argument('--c_e', type=float, default=None)
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX}")
    if a.lee:
        R, ab = lee(os.path.abspath(a.lee)); brazos = tuple(b for b in ORDEN if R[b]); n = max(len(R[b]) for b in brazos)
        L = lee_serie(R, n, len(ab), brazos); imprime(L, print)
        print(f"VEREDICTO ({'parcial/humo, no cuenta' if n != N_SERIE or set(brazos) != set(ORDEN) else 'letra'}): {L['veredicto']} · abortos {ab}")
        return 0
    if a.humo or a.explora:
        if a.pool: raise SystemExit("--humo/--explora: sin Pool (un proceso)")
        modo = 'humo' if a.humo else 'explora'; cfg = HUMO if a.humo else EXPLORA
        n = a.n or cfg['n']; T = a.T or cfg['T']; brazos = tuple(a.brazos.split(',')) if a.brazos else RAFAGA; base = a.desde or SEM[modo]
        if len(brazos) * n > MAX_CORRIDAS_1P or T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(brazos) * n}) y <= {MAX_PASOS_1P} pasos (T {T})")
        if a.c_e is not None:   # solo humo/explora: el costo se puede mover; queda en estado y bitacora
            MUNDO_P7['c_e'] = a.c_e
        dest = os.path.join(DATOS, 'p7_' + modo)
    else:
        if a.T or a.n or a.brazos or a.desde or a.c_e is not None: raise SystemExit("--serie/--replica: T, n, brazos, c_e y semillas los fija el preregistro")
        modo = 'serie' if a.serie else 'replica'; n = N_SERIE; T = T_SERIE; brazos = ORDEN; base = SEM[modo]; dest = DATOS
    for b in brazos:
        if b not in BRAZOS: raise SystemExit(f"brazo desconocido {b}")
    pre = f"{'p7_' if modo in ('serie', 'replica') else ''}{modo}_s{base}-{base + n - 1}_T{T}"
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
    log(f"CORRE_P7 · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_p7.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  semillas {base}-{base + n - 1} · T {T} · brazos {list(brazos)} · mundo {MUNDO_P7} · reanuda {a.reanuda} · nota {a.nota!r}")
    ok = verifica(log) and CO.identidad_corta(log) and identidad_corta(log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    tareas = [(i, b, base, T, carpeta, a.reanuda) for i in range(n) for b in brazos]

    def fmt(x):
        oz = x.get('oasis') or {}; pz = x.get('pizarra') or {}; sn = x.get('senal') or {}; lt = x.get('latencia') or {}
        return (f"  [{time.time()-t0:7.1f}s] i{x['i']} {x['brazo']:6s} ({x.get('seg')}s) aborto {x.get('aborto')} cruzan {x.get('cruzan')}/9 R0 {x.get('R0_med')} "
                f"fund {x.get('fund')} · oasis ratio pasos {oz.get('ratio_pasos')} · escr {pz.get('escrituras_total')} cobros {pz.get('cobros_total')} lee {sn.get('sn_lee')} "
                f"siembra {sn.get('sn_siembra')} · latencia med {lt.get('med')} (n {lt.get('n')}) · mundo AC {x.get('mundo_AC')}")
    X = []
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): X.append(x); log(fmt(x))
    else:
        for tk in tareas:
            x = trabajo(tk); X.append(x); log(fmt(x))
    R, ab = lee(carpeta); L = lee_serie(R, n, len(ab), brazos)
    log(f"\n================ LA LETRA (escalada a n {n})" + (" -- HUMO/EXPLORA: NO cuenta, no se declara" if modo in ('humo', 'explora') else ""))
    imprime(L, log)
    if ab: log(f"  ABORTOS: {ab}")
    ver = (f"{modo.upper()} (no cuenta): " if modo in ('humo', 'explora') else '') + L['veredicto'] + (f" ({L['matiz']})" if L.get('matiz') else '')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, letra=L, abortos=ab, n=n, T=T, brazos=list(brazos), semillas=[base, base + n - 1], veredicto=ver, nota=a.nota,
                       mundo=MUNDO_P7, sha_runner=h16(os.path.abspath(__file__)), sha_corre_p1=h16(os.path.join(AQUI, 'corre_p1.py')),
                       shas={os.path.relpath(k, RAIZ): v for k, v in CO.SHAS.items()}, carros={k: h16(v) for k, v in CARROS.items()},
                       mundo_c=MC.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {len(ab)} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO: {ver}")
    if modo in ('humo', 'explora'):
        d = L['descriptivo']; sc = d.get('suma_cruzan', {}); es = d.get('establecidos_0fund_post10k', {}); pa = L.get('pareado_lug') or {}; pb = L.get('pareado_senbar') or {}
        pf = L.get('pareado_fund') or {}; pm = L.get('pareado_frac_vidas') or {}
        senal = 'no se lee' if not sc else ('si' if (pa.get('dif', 0) > 0 and pb.get('dif', 0) > 0 and pf.get('gana', 0) > pf.get('pierde', 0)) else
                                            'si (fundadores/vidas que llegan; cruce no)' if (pf.get('gana', 0) > pf.get('pierde', 0) and pm.get('gana', 0) > pm.get('pierde', 0)) else 'no')
        bitacora(f"| {time.strftime('%Y-%m-%d %H:%M')} | p7 senal por pizarra (significado dado, linajes clones, costo c_e {MUNDO_P7['c_e']}) | {modo} s{base}-{base + n - 1} T{T} {list(brazos)} carro {h16(CARROS['O1_LUGAR_SENAL'])} {a.nota} | "
                 f"cruzan {sc} · establecidos {es} · R0 {d.get('R0_med')} · fund {d.get('fund_media')} · vidas con bocado dentro {d.get('frac_vidas_con_bocado_dentro')} · latencia {d.get('latencia_med')} · ratio pasos oasis {d.get('ratio_pasos_oasis')} · "
                 f"escr {d.get('escrituras')} cobros {d.get('cobros')} siembras {d.get('siembras')} · sen-lug {pa.get('dif')} sen-senbar {pb.get('dif')} · mundo AC {d.get('mundo_AC')} · "
                 f"abortos {len(ab)} · {os.path.relpath(carpeta, AQUI)} | {senal} |")
    return 0


if __name__ == '__main__':
    sys.exit(main())
