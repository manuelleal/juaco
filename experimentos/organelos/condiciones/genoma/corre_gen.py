"""corre_gen.py — CONDICIONES / GENOMA (30-sep-2026, creador; DIAGNOSTICO EXPLORATORIO). Preregistro: PREREGISTRO_genoma.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

PREGUNTA (junta Fable, ingeniero genetico): "la seleccion no inventa combinaciones" puede ser un artefacto de CAPACIDAD: con las tasas de
fabrica de V143_BQ2 (inicial 2, dup 0.02, del 0.07, ins 0.05) el cambio de largo esperado por parto es 0 y el genoma queda en ~2 reglas; la
regla PRUEBA de O1 escrita en reglas necesita 2 ("desconocida -> boca -" + "reserva -> boca +"). Brazos con CAPACIDAD: inicial 6, p_dup 0.06
(delta largo +0.04 por parto), el resto igual.

ENTRADA (regla 14): TODA corrida ES bloques_pista/corre_bp.tarea(seed, carro, T, cfg=<cfg del brazo>, forzada=None, siembra) (se IMPORTA
por sentidos_muro, no se toca; sha fijado). Cadena = la de bq2_pas de sentidos_muro (corre_bp.siembra_de / corre_bp.prepara): NPAS pasajes
de T_PAS, el pasaje 0 sin siembra, la siembra siguiente = union de los bancos finales; luego PRUEBA a T_PRU con la siembra final.
BRAZOS:
  fab        V143_BQ2, CFG de fabrica                                  CONTROL (es bq2_pas de sentidos_muro en semillas nuevas; arnes F)
  cap        V143_BQ2, CAP = inicial 6, p_dup 0.06 (resto de fabrica)  CANDIDATO
  aza_largo  V143_BQ2AZA, CAP (mismas tasas, SIN herencia)             CONTROL que puede fallar
Con TASAS = 'fabrica' (SOLO arnes) cap y aza_largo usan CFG: fab == sentidos_muro bq2_pas y aza_largo == corre_bp 'bloq2aza' bit a bit.

SEMILLAS NUEVAS (grep 30-sep: 635xxx no aparece en .py/.md/.txt de PROYECTOS/JUACO/organelos salvo cifras de floats en un log):
  pasaje p del indice i (1..5): 635000 + 10 i + p (635010-635059), LAS MISMAS en los tres brazos (pareado) · prueba: 635100 + i
  humo: pasaje 635090, prueba 635190 · arnes 635192.
Pool: MAXIMO 2. Cada trabajo registra los carros y fija cfg al entrar, atrapa TODO y escribe cada JSON ANTES de volver (ERR-54).
--reanuda sigue la ultima carpeta y REINTENTA los JSON con aborto (los buenos no se recorren). ERR-115: banderas exactas.

  python experimentos/organelos/condiciones/genoma/identidad_gen.py                    # arnes (escribe identidad_gen_salida.txt)
  python experimentos/organelos/condiciones/genoma/corre_gen.py --humo                 # 1 proceso, 6 corridas, 150 000 pasos
  python experimentos/organelos/condiciones/genoma/corre_gen.py --explora --pool 2     # 15 cadenas (10 x 25k) + 15 pruebas 100k
  python experimentos/organelos/condiciones/genoma/corre_gen.py --explora --pool 2 --reanuda
  python experimentos/organelos/condiciones/genoma/corre_gen.py --lee datos/explora_<fecha>
"""
import argparse, hashlib, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
SMD = os.path.join(RAIZ, 'experimentos', 'organelos', 'sentidos_muro')
BPD = os.path.join(RAIZ, 'experimentos', 'organelos', 'bloques_pista')
for _d in (AQUI, SMD, BPD):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_sentidos_muro as SM   # registra, verifica, CFG, tarea, trabajo (se IMPORTA, no se toca; sha fijado)
CBP = SM.CBP; CV = SM.CV

PRERREGISTRO = 'PREREGISTRO_genoma.md'
DATOS = os.path.join(AQUI, 'datos')
SMEXP = os.path.join(SMD, 'datos', 'explora_20260929_110024')
SHAS = {os.path.join(SMD, 'corre_sentidos_muro.py'): '4776b80e18733079', os.path.join(BPD, 'corre_bp.py'): '6b9c11a6639d3948',
        os.path.join(BPD, 'carros', 'V143_BQ2.py'): '183fb81cf6ad520c', os.path.join(BPD, 'carros', 'V143_BQ2AZA.py'): 'aa88b32e4b4de152'}
REF_P0 = (os.path.join(SMEXP, 'pasaje_bq2_pas_i1_p0.json'), '52c220e41ed445f7')   # arnes F: reproduccion bit a bit (s 614010, T 25 000)

CFG = dict(SM.CFG)
CAP = dict(CFG, inicial=6, p_dup=0.06)   # delta largo esperado por parto: 0.06 + 0.05 - 0.07 = +0.04 (fabrica: 0)
# tasas -> brazo -> (carro, cfg)
TASAS = {'cap': {'fab': ('V143_BQ2', CFG), 'cap': ('V143_BQ2', CAP), 'aza_largo': ('V143_BQ2AZA', CAP)},
         'fabrica': {'fab': ('V143_BQ2', CFG), 'cap': ('V143_BQ2', CFG), 'aza_largo': ('V143_BQ2AZA', CFG)}}   # SOLO arnes
BR = ('fab', 'cap', 'aza_largo')
MODOS = {'explora': dict(ind=[1, 2, 3, 4, 5], npas=10, T_pas=25000, T_pru=100000, base_pas=635000, base_pru=635100, tasas='cap'),
         'humo': dict(ind=[9], npas=1, T_pas=25000, T_pru=25000, base_pas=635000, base_pru=635181, tasas='cap')}
SEM_ARNES = 635192
POOL_MAX = 2
# LA LETRA (PREREGISTRO sec. 6)
LARGO_UMB = 4.0; GANA_N = 4; PURGA_N = 3; ACTUA_DIF = 1.0; COMPONE_X = 2.0; COMPONE_N = 3; COMPONE_AZA_N = 4
NQ = 2 / 27   # P(una regla al azar lee el sentido 7 u 8 y actua en la boca) = 2/9 * 1/3 (V143_BQ2: NSEN 9, NACC 3)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sem_pas(m, i, p): return m['base_pas'] + 10 * i + p
def sem_pru(m, i): return m['base_pru'] + i


def es_q(r): return int(r[0]) in (7, 8) and int(r[4]) == 0
def es_doble(R):
    """ENCARGO: las dos reglas tipo 'prueba' juntas = en la MISMA lista, >= 1 regla (sentido 7 u 8, boca, w < 0) y >= 1 (sentido 7 u 8, boca, w > 0)."""
    q = [r for r in R if es_q(r)]
    return any(r[5] < 0 for r in q) and any(r[5] > 0 for r in q)
def es_o1(R):
    """Descriptivo estricto: la forma de PRUEBA_O1 (corre_bp): 'sentido 7 < th -> boca -' y 'sentido 8 > th -> boca +'."""
    return any(int(r[0]) == 7 and r[2] <= 0.5 and int(r[4]) == 0 and r[5] < 0 for r in R) and \
        any(int(r[0]) == 8 and r[2] > 0.5 and int(r[4]) == 0 and r[5] > 0 for r in R)
def p_azar(n, q=NQ):
    """P(es_doble) de una lista de n reglas al azar (_bq_azar: sentido, accion uniformes; w ~ U(-3, 3): signo 1/2)."""
    return 1 - 2 * (1 - q / 2) ** n + (1 - q) ** n


def frac(S, pred):
    return round(sum(1 for R in S if pred(R)) / len(S), 4) if S else None
def largo(S): return round(st.mean(len(R) for R in S), 3) if S else None


def tarea(seed, brazo, T, siembra=None, tasas='cap'):
    """UNA corrida: corre_bp.tarea(seed, carro, T, cfg del brazo, forzada None, siembra)."""
    SM.registra()
    carro, cfg = TASAS[tasas][brazo]
    x = CBP.tarea(seed, carro, T, cfg=dict(cfg), forzada=None, siembra=siembra)
    x['brazo'] = brazo; x['carro'] = carro
    return x


def _guarda(fin, x):
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)


def _ok_previo(fin):
    if not os.path.exists(fin): return None
    try:
        with open(fin, encoding='utf-8') as fh: x = json.load(fh)
    except Exception: return None
    return None if x.get('aborto') else x


def _corrida(fin, seed, brazo, T, siembra, extra, tasas):
    x = _ok_previo(fin)
    if x is not None: return x
    reint = os.path.exists(fin); t0 = time.time()
    try:
        x = tarea(seed, brazo, T, siembra, tasas); x['aborto'] = None
    except BaseException as e:   # noqa: nube-9
        x = dict(seed=seed, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    x.update(extra); x['T'] = T; x['seg_trabajo'] = round(time.time() - t0, 1)
    if siembra is not None: x['siembra_n'] = len(siembra)
    if reint: x['reintento_de'] = 'aborto'
    _guarda(fin, x)
    return x


def trabajo(args):
    """UN trabajo = una cadena (brazo, indice): NPAS pasajes + la prueba. cfg fijado en CADA worker (registra + cfg explicito)."""
    brazo, i, carpeta, modo = args
    m = MODOS[modo]; tz = m['tasas']; t0 = time.time(); aborto = None; out = dict(brazo=brazo, i=i); lg = []
    try:
        SM.registra()
        sb = None
        for p in range(m['npas']):
            x = _corrida(os.path.join(carpeta, f"pasaje_{brazo}_i{i}_p{p}.json"), sem_pas(m, i, p), brazo, m['T_pas'], sb,
                         dict(i=i, p=p, tipo='pasaje'), tz)
            if x.get('aborto'): aborto = f"pasaje {p}: {x['aborto']}"; break
            sb = CBP.siembra_de(x); lg.append(largo(sb))
            if not sb: aborto = f"pasaje {p}: siembra vacia (ningun linaje pario)"; break
        if aborto is None:
            x = _corrida(os.path.join(carpeta, f"{brazo}_s{sem_pru(m, i)}.json"), sem_pru(m, i), brazo, m['T_pru'], sb,
                         dict(i=i, tipo='prueba', siembra_final=sb), tz)
            aborto = x.get('aborto'); L = x.get('linajes', [])
            out.update(cruzan=sum(int(l['cruza_real']) for l in L), R0=[l['R0_real'] for l in L])
        else:
            _guarda(os.path.join(carpeta, f"{brazo}_s{sem_pru(m, i)}.json"),
                    dict(seed=sem_pru(m, i), brazo=brazo, aborto=aborto, linajes=[], i=i, tipo='prueba'))
        out.update(aborto=aborto, largo_siembra=lg)
    except BaseException as e:   # noqa: nube-9
        out.update(aborto=f"{type(e).__name__}: {e}"[:300], largo_siembra=lg)
    out['seg'] = round(time.time() - t0, 1)
    return out


# ------------------------------------------------------------------ lectura y LA LETRA
def _med(xs):
    xs = [x for x in xs if x is not None]; return round(float(st.median(xs)), 4) if xs else None


def cadena(carpeta, m, brazo, i):
    """Lee la cadena y su prueba. Por pasaje: largo medio de la siembra, fraccion doble y o1, partos. Prueba: la fila."""
    lg = []; db = []; o1 = []; partos = []
    for p in range(m['npas']):
        fin = os.path.join(carpeta, f"pasaje_{brazo}_i{i}_p{p}.json")
        if not os.path.exists(fin): return None, f"falta {os.path.basename(fin)}"
        x = json.load(open(fin, encoding='utf-8'))
        if x.get('aborto'): return None, f"{brazo} i{i} p{p}: {x['aborto']}"
        S = CBP.siembra_de(x); lg.append(largo(S)); db.append(frac(S, es_doble)); o1.append(frac(S, es_o1))
        partos.append(sum(t['partos'] for t in x['bq']['tel'].values()))
    fin = os.path.join(carpeta, f"{brazo}_s{sem_pru(m, i)}.json")
    if not os.path.exists(fin): return None, f"falta prueba {brazo} i{i}"
    x = json.load(open(fin, encoding='utf-8'))
    if x.get('aborto'): return None, f"prueba {brazo} i{i}: {x['aborto']}"
    L = x['linajes']; cz = sum(int(l['cruza_real']) for l in L)
    lin = [B for B in x['bq']['banco'].values() if B]
    lm = [st.mean(len(R) for R in B[-10:]) for B in lin]   # = corre_bp.resumen 'largo_med' (ultimas 10 listas de cada banco)
    Bf = [R for B in lin for R in B]
    return dict(largo_siembra=lg, doble_siembra=db, o1_siembra=o1, partos=partos,
                cruzan=cz, mayoria=int(cz * 2 > len(L)), R0_med=_med([l['R0_real'] for l in L]), fund_med=_med([l['fundadores'] for l in L]),
                fund_media=round(sum(l['fundadores'] for l in L) / max(1, len(L)), 1), coherente=all(l.get('coherente', True) for l in L),
                largo_med=_med(lm), lin_con_banco=len(lin), doble_lin=sum(1 for B in lin if any(es_doble(R) for R in B[-10:])),
                o1_lin=sum(1 for B in lin if any(es_o1(R) for R in B[-10:])), doble_banco_final=frac(Bf, es_doble),
                fund_de_banco=sum(ff[1] == 1 for t in x['bq']['tel'].values() for ff in t['fund']),
                fund_n=sum(len(t['fund']) for t in x['bq']['tel'].values())), None


def carga(carpeta, modo):
    m = MODOS[modo]; C = {}; abortos = []
    for b in BR:
        C[b] = {}
        for i in m['ind']:
            c, ab = cadena(carpeta, m, b, i)
            if c is None: abortos.append(ab); continue
            C[b][i] = c
    return C, abortos


def gana(C, a, b, ind, k='cruzan'):
    I = [i for i in ind if i in C.get(a, {}) and i in C.get(b, {})]
    return dict(n=len(I), gana=sum(1 for i in I if C[a][i][k] > C[b][i][k]), dif_suma=round(sum(C[a][i][k] - C[b][i][k] for i in I), 4))


def letra(C, ind, abortos, arnes_ok):
    """PREREGISTRO sec. 6. Veredicto: CAPACIDAD PAGA / CAPACIDAD PURGADA / CAPACIDAD SIN USO / INDETERMINADO / NO SE LEE. COMPONE: descriptivo."""
    n = len(ind)
    act = sum(1 for i in ind if i in C.get('cap', {}) and i in C.get('fab', {})
              and C['cap'][i]['largo_siembra'][0] >= C['fab'][i]['largo_siembra'][0] + ACTUA_DIF)
    val = dict(abortos_0=(len(abortos) == 0), completas=all(len(C.get(b, {})) == n for b in BR),
               coherentes=all(c['coherente'] for b in C for c in C[b].values()), tasas_actuan=(act == n), arnes=bool(arnes_ok))
    valido = all(val.values())
    g_fab = gana(C, 'cap', 'fab', ind); g_aza = gana(C, 'cap', 'aza_largo', ind); r0 = gana(C, 'cap', 'fab', ind, 'R0_med')
    lc = {i: C['cap'][i]['largo_med'] for i in C.get('cap', {})}
    largo_ok = sum(1 for v in lc.values() if v is not None and v >= LARGO_UMB); largo_bajo = sum(1 for v in lc.values() if v is None or v < LARGO_UMB)
    if not valido: ver = 'NO SE LEE'
    elif g_fab['gana'] >= GANA_N and g_aza['gana'] >= GANA_N: ver = 'CAPACIDAD PAGA'
    elif largo_bajo >= PURGA_N: ver = 'CAPACIDAD PURGADA'
    elif largo_ok >= GANA_N: ver = 'CAPACIDAD SIN USO'
    else: ver = 'INDETERMINADO'
    pa6 = p_azar(6)
    dc = {i: C['cap'][i]['doble_siembra'][-1] for i in C.get('cap', {})}
    da = {i: C['aza_largo'][i]['doble_siembra'][-1] for i in C.get('aza_largo', {})}
    comp_alto = sum(1 for v in dc.values() if v is not None and v >= COMPONE_X * pa6)
    comp_aza = sum(1 for i in dc if i in da and dc[i] is not None and da[i] is not None and dc[i] > da[i])
    compone = comp_alto >= COMPONE_N and comp_aza >= COMPONE_AZA_N
    S = {b: sum(c['cruzan'] for c in C.get(b, {}).values()) for b in BR}
    return dict(validez=val, veredicto=ver, compone=compone, compone_detalle=dict(p_azar6=round(pa6, 4), umbral=round(COMPONE_X * pa6, 4),
                                                                                 cap_sobre_umbral=f"{comp_alto}/{len(dc)}", cap_mayor_que_aza=f"{comp_aza}/{len(dc)}"),
                tasas_actuan_n=f"{act}/{n}", cap_gana_fab=g_fab, cap_gana_aza=g_aza, R0_cap_gana_fab=r0, suma_cruzan=S,
                largo_med={b: {str(i): C[b][i]['largo_med'] for i in C.get(b, {})} for b in BR},
                cap_largo_ge4=f"{largo_ok}/{len(lc)}", doble_lin={b: sum(c['doble_lin'] for c in C.get(b, {}).values()) for b in BR},
                o1_lin={b: sum(c['o1_lin'] for c in C.get(b, {}).values()) for b in BR},
                lin_total={b: sum(c['lin_con_banco'] for c in C.get(b, {}).values()) for b in BR},
                doble_siembra_p9={b: {str(i): C[b][i]['doble_siembra'][-1] for i in C.get(b, {})} for b in BR},
                mayorias={b: sum(c['mayoria'] for c in C.get(b, {}).values()) for b in BR})


def predicciones(C, L):
    ind = MODOS['explora']['ind']
    lok = int(L['cap_largo_ge4'].split('/')[0]); dl = L['doble_lin'].get('cap', 0); r0 = L['R0_cap_gana_fab']['gana']
    S = L['suma_cruzan']
    return [('I1', 'ingeniero: largo_med de cap >= 4.0 en >= 4/5', L['cap_largo_ge4'], lok >= 4, 0.85),
            ('I2', 'ingeniero: doble regla en >= 1/45 linajes de cap (prueba, ultimas 10 listas del banco)', dl, dl >= 1, 0.30),
            ('I3', 'ingeniero: R0 sube (R0 mediano cap > fab, pareado, en >= 4/5)', f"{r0}/{L['R0_cap_gana_fab']['n']}", r0 >= 4, 0.15),
            ('K1', 'creador: largo_med de cap >= 4.0 en >= 4/5 (= I1)', L['cap_largo_ge4'], lok >= 4, 0.85),
            ('K2', 'creador: doble regla en >= 1/45 linajes de cap (= I2; piso de azar alto)', dl, dl >= 1, 0.70),
            ('K3', 'creador: veredicto CAPACIDAD SIN USO', L['veredicto'], L['veredicto'] == 'CAPACIDAD SIN USO', 0.60),
            ('K4', 'creador: veredicto CAPACIDAD PAGA', L['veredicto'], L['veredicto'] == 'CAPACIDAD PAGA', 0.07),
            ('K5', 'creador: COMPONE (descriptivo)', L['compone'], bool(L['compone']), 0.10),
            ('K6', 'creador: suma cruzan cap <= suma cruzan fab', f"{S.get('cap')} vs {S.get('fab')}", S.get('cap', 0) <= S.get('fab', 0), 0.55)]


def arnes_pasado():
    f = os.path.join(AQUI, 'identidad_gen_salida.txt')
    if not os.path.exists(f): return False, 'sin salida del arnes'
    t = open(f, encoding='utf-8').read()
    need = [h16(os.path.abspath(__file__)), h16(os.path.join(AQUI, 'identidad_gen.py'))]
    ok = 'ARNES: PASA' in t and all(s in t for s in need)
    return ok, ('PASA con los shas actuales' if ok else f'no PASA o no cita los shas actuales {need}')


def lee(carpeta, log=print, modo=None):
    modo = modo or ('humo' if os.path.basename(carpeta).startswith('humo') else 'explora')
    m = MODOS[modo]; C, abortos = carga(carpeta, modo)
    aok, atxt = arnes_pasado()
    L = letra(C, m['ind'], abortos, aok)
    log(f"\n================ LECTURA genoma (capacidad) · {modo} · {carpeta}")
    log(f"  arnes: {atxt} · abortos: {abortos}")
    for b in BR:
        for i in sorted(C.get(b, {})):
            c = C[b][i]
            log(f"  {b:9s} i{i}: largo siembra p0..p{len(c['largo_siembra'])-1} {c['largo_siembra']} · partos {c['partos']}")
            log(f"  {'':9s}     doble en la siembra {c['doble_siembra']} · forma O1 {c['o1_siembra']}")
            log(f"  {'':9s}     PRUEBA: cruzan {c['cruzan']}/9 · mayoria {c['mayoria']} · R0 med {c['R0_med']} · fund med {c['fund_med']} media {c['fund_media']} "
                f"· largo_med {c['largo_med']} · doble linajes {c['doble_lin']}/{c['lin_con_banco']} · O1 linajes {c['o1_lin']} · doble banco {c['doble_banco_final']} "
                f"· fund de banco {c['fund_de_banco']}/{c['fund_n']}")
    for k in ('validez', 'tasas_actuan_n', 'suma_cruzan', 'mayorias', 'cap_gana_fab', 'cap_gana_aza', 'R0_cap_gana_fab', 'largo_med', 'cap_largo_ge4',
              'doble_lin', 'o1_lin', 'lin_total', 'doble_siembra_p9', 'compone', 'compone_detalle'):
        log(f"  {k}: {L[k]}")
    pq = predicciones(C, L) if modo == 'explora' else []
    for q in pq: log(f"  {q[0]} {q[1]} (p {q[4]}): medido {q[2]} -> {'CUMPLE' if q[3] else 'REFUTADA'}")
    ver = ('HUMO (no cuenta; 1 pasaje, prueba 25k): ' if modo == 'humo' else '') + L['veredicto']
    out = os.path.join(carpeta, 'lectura_gen.json')
    json.dump(dict(modo=modo, letra=L, cadenas={b: {str(i): c for i, c in d.items()} for b, d in C.items()}, abortos=abortos,
                   predicciones=[[q[0], q[1], q[2], bool(q[3]), q[4]] for q in pq], preregistro=PRERREGISTRO, sha_runner=h16(os.path.abspath(__file__))),
              open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    log(f"  LECTURA {out}")
    log(f"VEREDICTO ({PRERREGISTRO} sec. 6): {ver}")
    return L


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    log("  -- verifica de sentidos_muro (shas de corre_bp, V143_BQ2, TERMO, pista, juez, O1, V143; carros == construye_sm):")
    ok &= SM.verifica(lambda s: log('  ' + s))
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115
    if a.pool > POOL_MAX: raise SystemExit(f"--pool: maximo {POOL_MAX}")
    if a.humo and a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
    if a.lee:
        c = a.lee if os.path.isabs(a.lee) else os.path.join(AQUI, a.lee)
        LOGF = open(os.path.join(c, 'lectura.txt'), 'w', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        lee(c, log); return 0
    modo = 'humo' if a.humo else 'explora'
    m = MODOS[modo]; os.makedirs(DATOS, exist_ok=True)
    prev = sorted(d for d in os.listdir(DATOS) if d.startswith(modo + '_'))
    carpeta = os.path.join(DATOS, prev[-1] if (a.reanuda and prev) else time.strftime(f'{modo}_%Y%m%d_%H%M%S'))
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time()
    log(f"CORRE_GEN · {modo} · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {platform.python_version()} · pool {a.pool or 'NO'} · "
        f"runner {h16(os.path.abspath(__file__))} · {PRERREGISTRO} · indices {m['ind']} · npas {m['npas']} · T_pas {m['T_pas']} · T_pru {m['T_pru']} · "
        f"pasajes {sem_pas(m, m['ind'][0], 0)}.. · prueba {[sem_pru(m, i) for i in m['ind']]} · CFG {CFG} · CAP {CAP} · {carpeta}")
    if not verifica(log): log("  ALGO FALLA -> no se corre."); return 1
    if modo == 'explora':
        aok, atxt = arnes_pasado(); log(f"  arnes: {atxt}")
        if not aok: log("  el arnes no esta pasado con los shas actuales -> no se corre."); return 1
    tareas = [(b, i, carpeta, modo) for b in ('cap', 'aza_largo', 'fab') for i in m['ind']]   # las lentas (6+ reglas) primero
    X = []

    def informa(x):
        X.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} i{x['i']} ({x['seg']}s) aborto {x['aborto']} · largo siembra {x.get('largo_siembra')} · "
                         f"cruzan {x.get('cruzan')} · R0 {x.get('R0')}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): informa(x)
    else:
        for t in tareas: informa(trabajo(t))
    log(f"  {len(X)} trabajos · abortos {sum(1 for x in X if x['aborto'])} · {time.time()-t0:.1f}s")
    lee(carpeta, log, modo)
    return 0


if __name__ == '__main__':
    sys.exit(main())
