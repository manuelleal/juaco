"""corre_sentidos_muro.py — SENTIDOS CONTRA EL MURO (29-sep-2026, creador; EXPLORATORIO). Preregistro: PREREGISTRO_sentidos_muro.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la seleccion construya el organo, no nosotros.

ENTRADA (regla 14): TODA corrida ES experimentos/organelos/bloques_pista/corre_bp.tarea (se IMPORTA, no se toca; sha fijado) =
corre_termo.tarea = corre_v143.tarea = juez.tarea(seed, 9 carros iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None,
fundador limpio 1) + telemetria de solo lectura del genoma (x['bq']). La pista y el juez son los de la carrera (shas fijados abajo).

BRAZOS (prueba en la pista vieja, T 100 000, semillas 59201-59205 = indices 1..5):
  bq3_pas   CANDIDATO: V143_BQ3 (sentidos 9 y 10) + SELECCION por pasajes: cadena de NPAS pasajes de T_PAS; la siembra del pasaje siguiente
            = union de los bancos finales de los 9 linajes (en el banco solo entra quien PARIO: corre_bp.siembra_de). La prueba arranca los
            bancos con la siembra final (corre_bp.prepara, rng del runner).
  bq2_pas   CONTROL sin sentidos nuevos, MISMA seleccion y MISMAS semillas de pasaje: V143_BQ2.
  bq3       CONTROL sin seleccion: V143_BQ3, banco vacio (lo que hace una sola corrida).
  forzada3  DIAGNOSTICO (no decide): V143_BQ3, tasas 0, todo cuerpo con UNA regla "riesgo (10) > 0.5 -> boca -3". Dice si el sentido nuevo
            CONTIENE una politica que cruza.
  Referencias (JSON GUARDADOS, sha16 fijado por archivo; mismos codigos: pista/juez/corre_termo/TERMO/O1/BQ2/V143 sin cambios desde que se
  escribieron; el arnes reproduce bloq2 s59201 T 100k BIT A BIT por este runner): v143 (pista_pob), termo, o1, bloq2 (bloques_pista).
SEMILLAS NUEVAS (grep 29-sep: 614xxx no aparece en .py/.md de PROYECTOS/JUACO; en .json solo como cifras de floats):
  pasaje p (0..NPAS-1) del indice i (1..5): 614000 + 10 i + p (614010-614059) · humo: pasajes 614900 + p, prueba 614991 · arnes 614992.
Pool: MAXIMO 2 (lo lanza el coordinador; ajuste 29-sep). Cada trabajo fija cfg al entrar (registra + CFG explicito), atrapa TODO (nube-9) y escribe su JSON
ANTES de volver (ERR-54; tambien cada pasaje). --reanuda sigue la ultima carpeta y REINTENTA los JSON con aborto. ERR-115: banderas exactas.

  python experimentos/organelos/sentidos_muro/corre_sentidos_muro.py --humo                 # 1 proceso, 6 corridas, 50 000 pasos
  python experimentos/organelos/sentidos_muro/corre_sentidos_muro.py --explora --pool 2     # 20 trabajos (10 cadenas + 10 pruebas)
  python experimentos/organelos/sentidos_muro/corre_sentidos_muro.py --explora --pool 2 --reanuda
  python experimentos/organelos/sentidos_muro/corre_sentidos_muro.py --lee datos/explora_<fecha>
"""
import argparse, copy, hashlib, importlib.util, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
BPD = os.path.join(RAIZ, 'experimentos', 'organelos', 'bloques_pista')
for _d in (AQUI, BPD):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_bp as CBP            # tarea, prepara, siembra_de, registra (se IMPORTA, no se toca; sha fijado)
import construye_sm as CSM
CT = CBP.CT; CV = CBP.CV; P = CBP.P; RC = CBP.RC

PRERREGISTRO = 'PREREGISTRO_sentidos_muro.md'
CARROS = os.path.join(AQUI, 'carros'); DATOS = os.path.join(AQUI, 'datos')
PROPIOS = ('V143_BQ3', 'V143_BQ3_0')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias'); TERMOD = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')
SHAS = {os.path.join(BPD, 'corre_bp.py'): '6b9c11a6639d3948', os.path.join(BPD, 'carros', 'V143_BQ2.py'): '183fb81cf6ad520c',
        os.path.join(TERMOD, 'corre_termo.py'): '66f1f2539f1030ef', os.path.join(TERMOD, 'carros', 'V143_TERMO.py'): '3db639cab75641fb',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028',
        os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'corre_v143.py'): '24100621c450da22',
        os.path.join(RAIZ, 'experimentos', 'tronco_v14_3', 'carros_v143', 'V143.py'): '2a03048a7f1525e5'}
EXP = os.path.join(BPD, 'datos', 'explora_T100000'); POB = os.path.join(RAIZ, 'experimentos', 'organelos', 'pista_pob', 'datos', 'explora')
REFS = {'termo': (EXP, ['eecf5d9335a6dde8', 'bbd11cb11ca63e32', 'dc7532a72db3da4d', '37132eb55a72aa0d', '0cd8266c052947e3']),
        'o1': (EXP, ['1cd9ea0af1b1d43e', '5e24d69de1d6e876', '29b382dc3287a854', 'ecea9f53481020e3', '50dd1773faaa7200']),
        'bloq2': (EXP, ['37df1c9a35a878b9', '37d2f3f7b82b3487', '72ef16ef23935921', '36fb34937c3ac914', 'b60e5a3bb2006914']),
        'v143': (POB, ['a2f57a40b271c46a', 'f55726c5257a7d0c', '20eb68a0cbb10e0a', '6566984601a2bdbb', '2470508fedc7ef9d'])}

CFG = dict(inicial=2, p_campo=0.10, p_dup=0.02, p_del=0.07, p_ins=0.05, banco=50)   # == BQ_C del carro y corre_bp.CFG0 (arnes)
CERO = dict(inicial=0, p_campo=0.0, p_dup=0.0, p_del=0.0, p_ins=0.0, banco=50)
FORZADA3 = [[10.0, 0.0, 1.0, 0.5, 0.0, -3.0]]    # "riesgo > 0.5 -> boca -3" (solo el brazo diagnostico)
# brazo -> (carro, pasajes, cfg, forzada)
BRAZOS = {'bq3_pas': ('V143_BQ3', True, CFG, None), 'bq2_pas': ('V143_BQ2', True, CFG, None),
          'bq3': ('V143_BQ3', False, CFG, None), 'forzada3': ('V143_BQ3', False, CERO, FORZADA3)}
PROPIOS_BRAZOS = ('bq3_pas', 'bq2_pas', 'bq3', 'forzada3')
MODOS = {'explora': dict(ind=[1, 2, 3, 4, 5], npas=10, T_pas=25000, T_pru=100000, base_pas=614000, base_pru=59200),
         'humo': dict(ind=[0], npas=1, T_pas=5000, T_pru=10000, base_pas=614900, base_pru=614991)}
SEM_ARNES = 614992
POOL_MAX = 2   # ajuste del coordinador (29-sep): tres lineas a la vez -> pool 2 como maximo
# LA LETRA (PREREGISTRO sec. 6)
GANA_F = 4; GANA_M = 3; MAY_F = 4; SUMA_M = 5; ANCLA_V143 = (0.40, 0.80); O1_MIN = 4


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sem_pas(m, i, p): return m['base_pas'] + 10 * i + p
def sem_pru(m, i): return m['base_pru'] + i


def registra():
    CBP.registra()
    for n in PROPIOS:
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", os.path.join(CARROS, n + '.py'))
            mm = importlib.util.module_from_spec(spec); spec.loader.exec_module(mm); CV._MODS[n] = mm
    if CBP.CFG0 is None: CBP._cfg_carro()


def tarea(seed, brazo, T, siembra=None):
    """UNA corrida por corre_bp.tarea con cfg y forzada FIJADOS aqui (nunca el global del modulo)."""
    registra()
    carro, _, cfg, forz = BRAZOS[brazo]
    x = CBP.tarea(seed, carro, T, cfg=dict(cfg), forzada=copy.deepcopy(forz), siembra=siembra)
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


def _corrida(fin, seed, brazo, T, siembra, extra):
    x = _ok_previo(fin)
    if x is not None: return x
    reint = os.path.exists(fin)
    t0 = time.time()
    try:
        x = tarea(seed, brazo, T, siembra); x['aborto'] = None
    except BaseException as e:   # noqa: nube-9
        x = dict(seed=seed, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    x.update(extra); x['T'] = T; x['seg_trabajo'] = round(time.time() - t0, 1)
    if siembra is not None: x['siembra_n'] = len(siembra)
    if reint: x['reintento_de'] = 'aborto'
    _guarda(fin, x)
    return x


def trabajo(args):
    """UN trabajo: ('pas', i, brazo, carpeta, modo) = cadena de pasajes + su prueba; ('uno', i, brazo, carpeta, modo) = una prueba."""
    tipo, i, brazo, carpeta, modo = args
    m = MODOS[modo]; t0 = time.time()
    try:
        registra()   # cfg fijado en CADA worker: carros cargados, CFG explicito en cada tarea
        sb = None; aborto = None; sie_tam = []
        if tipo == 'pas':
            for p in range(m['npas']):
                x = _corrida(os.path.join(carpeta, f"pasaje_{brazo}_i{i}_p{p}.json"), sem_pas(m, i, p), brazo, m['T_pas'], sb,
                             dict(i=i, p=p, tipo='pasaje'))
                if x.get('aborto'): aborto = f"pasaje {p}: {x['aborto']}"; break
                sb = CBP.siembra_de(x); sie_tam.append(len(sb))
                if not sb: aborto = f"pasaje {p}: siembra vacia (ningun linaje pario)"; break
        if aborto is None:
            x = _corrida(os.path.join(carpeta, f"{brazo}_s{sem_pru(m, i)}.json"), sem_pru(m, i), brazo, m['T_pru'], sb,
                         dict(i=i, tipo='prueba', siembra_tam_por_pasaje=sie_tam,
                              siembra_final=(sb if tipo == 'pas' else None)))
            aborto = x.get('aborto')
            L = x.get('linajes', [])
            out = dict(tipo=tipo, i=i, brazo=brazo, aborto=aborto, cruzan=sum(int(l['cruza_real']) for l in L),
                       R0=[l['R0_real'] for l in L], fund=[l['fundadores'] for l in L], siembra=sie_tam)
        else:
            out = dict(tipo=tipo, i=i, brazo=brazo, aborto=aborto)
            _guarda(os.path.join(carpeta, f"{brazo}_s{sem_pru(m, i)}.json"),
                    dict(seed=sem_pru(m, i), brazo=brazo, aborto=aborto, linajes=[], i=i, tipo='prueba'))
    except BaseException as e:   # noqa: nube-9
        out = dict(tipo=tipo, i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    out['seg'] = round(time.time() - t0, 1)
    return out


# ------------------------------------------------------------------ lectura y LA LETRA
def _med(xs):
    xs = [x for x in xs if x is not None]; return round(float(st.median(xs)), 4) if xs else None


def es_riesgo(r): return int(r[0]) == 10 and r[2] > 0.5 and int(r[4]) == 0 and r[5] < 0
def usa_s3(r): return int(r[0]) in (9, 10)


def fila(x):
    L = x['linajes']; cz = sum(int(l['cruza_real']) for l in L)
    f = dict(seed=x['seed'], cruzan=cz, mayoria=int(cz * 2 > len(L)), R0_med=_med([l['R0_real'] for l in L]),
             fund_med=_med([l['fundadores'] for l in L]), fund_media=round(sum(l['fundadores'] for l in L) / max(1, len(L)), 1),
             coherente=all(l.get('coherente', True) for l in L), n_lin=len(L))
    sf = x.get('siembra_final')
    if sf: f['siembra_riesgo'] = round(sum(any(es_riesgo(r) for r in R) for R in sf) / len(sf), 3); f['siembra_s3'] = round(
        sum(any(usa_s3(r) for r in R) for R in sf) / len(sf), 3)
    if 'bq' in x:
        B = [R for v in x['bq']['banco'].values() for R in v if R]
        f['banco_riesgo'] = round(sum(any(es_riesgo(r) for r in R) for R in B) / len(B), 3) if B else None
        f['fund_de_banco'] = sum(ff[1] == 1 for t in x['bq']['tel'].values() for ff in t['fund'])
        f['fund_n'] = sum(len(t['fund']) for t in x['bq']['tel'].values())
    return f


def carga(carpeta, modo):
    m = MODOS[modo]; tab = {}; abortos = []; ref_ok = True; ref_txt = []
    for b in PROPIOS_BRAZOS:
        tab[b] = {}
        for i in m['ind']:
            fin = os.path.join(carpeta, f"{b}_s{sem_pru(m, i)}.json")
            if not os.path.exists(fin): continue
            x = json.load(open(fin, encoding='utf-8'))
            if x.get('aborto'): abortos.append(f"{b} i{i}: {x['aborto']}"); continue
            tab[b][i] = fila(x)
    for b, (d, shas) in REFS.items():
        tab[b] = {}
        if modo != 'explora': continue
        for i, sh in zip(m['ind'], shas):
            fin = os.path.join(d, f"{b}_s{sem_pru(m, i)}.json")
            s = h16(fin) if os.path.exists(fin) else None
            if s != sh: ref_ok = False; ref_txt.append(f"{b} s{sem_pru(m, i)} sha {s} != {sh}"); continue
            tab[b][i] = fila(json.load(open(fin, encoding='utf-8')))
    return tab, abortos, ref_ok, ref_txt


def gana(tab, a, b, ind):
    I = [i for i in ind if i in tab[a] and i in tab[b]]
    return dict(n=len(I), gana=sum(1 for i in I if tab[a][i]['cruzan'] > tab[b][i]['cruzan']),
                dif_suma=sum(tab[a][i]['cruzan'] - tab[b][i]['cruzan'] for i in I))


def letra(tab, ind, abortos, ref_ok, arnes_ok):
    """PREREGISTRO sec. 6. tab[brazo][i] = fila. Devuelve validez, puertas y veredicto (FUNCIONA / HAY ALGO MODESTO / NO / NO SE LEE)."""
    n = len(ind); S = {b: sum(tab[b][i]['cruzan'] for i in tab.get(b, {})) for b in tab}
    v143 = _med([tab['v143'][i]['R0_med'] for i in tab.get('v143', {})])
    val = dict(abortos_0=(len(abortos) == 0), completos=all(len(tab.get(b, {})) == n for b in PROPIOS_BRAZOS + tuple(REFS)),
               coherentes=all(f['coherente'] for b in tab for f in tab[b].values()), refs_sha=bool(ref_ok),
               ancla_v143=(v143 is not None and ANCLA_V143[0] <= v143 <= ANCLA_V143[1]),
               ancla_o1=(sum(tab.get('o1', {})[i]['mayoria'] for i in tab.get('o1', {})) >= O1_MIN), arnes=bool(arnes_ok))
    valido = all(val.values())
    g2 = gana(tab, 'bq3_pas', 'bq2_pas', ind); g3 = gana(tab, 'bq3_pas', 'bq3', ind)
    may = sum(tab['bq3_pas'][i]['mayoria'] for i in tab.get('bq3_pas', {}))
    pu = dict(F1_mayoria_bq3_pas=may >= MAY_F, F2_gana_bq2_pas=g2['gana'] >= GANA_F, F3_gana_bq3=g3['gana'] >= GANA_F)
    mod = bool((g2['gana'] >= GANA_M and g3['gana'] >= GANA_M)
               or (S.get('bq3_pas', 0) >= max(S.get('bq2_pas', 0), S.get('bq3', 0)) + SUMA_M))
    if not valido: ver = 'NO SE LEE'
    elif all(pu.values()): ver = 'FUNCIONA'
    elif mod: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    return dict(validez=val, v143_R0_med=v143, puertas=pu, modesto=mod, veredicto=ver, suma_cruzan=S,
                mayorias={b: sum(tab[b][i]['mayoria'] for i in tab[b]) for b in tab},
                pareados=dict(bq3_pas_vs_bq2_pas=g2, bq3_pas_vs_bq3=g3, bq3_pas_vs_bloq2=gana(tab, 'bq3_pas', 'bloq2', ind),
                              bq3_pas_vs_termo=gana(tab, 'bq3_pas', 'termo', ind), bq3_pas_vs_o1=gana(tab, 'bq3_pas', 'o1', ind),
                              bq3_vs_bloq2=gana(tab, 'bq3', 'bloq2', ind), forzada3_vs_termo=gana(tab, 'forzada3', 'termo', ind)))


def predicciones(tab, L):
    S = L['suma_cruzan']; my = L['mayorias']
    sr = [tab['bq3_pas'][i].get('siembra_riesgo') for i in tab.get('bq3_pas', {})]
    return [('S1', 'forzada3 mayoria >= 3/5', my.get('forzada3'), (my.get('forzada3') or 0) >= 3, 0.50),
            ('S2', 'suma cruzan bq3_pas en [18, 32]', S.get('bq3_pas'), 18 <= S.get('bq3_pas', -1) <= 32, 0.60),
            ('S3', 'suma cruzan bq2_pas en [14, 27]', S.get('bq2_pas'), 14 <= S.get('bq2_pas', -1) <= 27, 0.65),
            ('S4', 'suma cruzan bq3 en [14, 27]', S.get('bq3'), 14 <= S.get('bq3', -1) <= 27, 0.60),
            ('S5', 'siembra final de bq3_pas con regla riesgo en >= 25 % de las listas en >= 3/5 cadenas', sr,
             sum(1 for z in sr if z is not None and z >= 0.25) >= 3, 0.35),
            ('S6', 'mayoria bq3_pas >= 3/5', my.get('bq3_pas'), (my.get('bq3_pas') or 0) >= 3, 0.30),
            ('S7', 'veredicto NO', L['veredicto'], L['veredicto'] == 'NO', 0.62)]


def arnes_pasado():
    f = os.path.join(AQUI, 'identidad_sentidos_muro_salida.txt')
    if not os.path.exists(f): return False, 'sin salida del arnes'
    t = open(f, encoding='utf-8').read()
    need = [h16(os.path.abspath(__file__)), h16(os.path.join(CARROS, 'V143_BQ3.py')), h16(os.path.join(AQUI, 'construye_sm.py'))]
    ok = 'ARNES: PASA' in t and all(s in t for s in need)
    return ok, ('PASA con los shas actuales' if ok else f'no PASA o no cita los shas actuales {need}')


def lee(carpeta, log=print, modo=None):
    modo = modo or ('humo' if os.path.basename(carpeta).startswith('humo') else 'explora')
    m = MODOS[modo]; tab, abortos, ref_ok, ref_txt = carga(carpeta, modo)
    aok, atxt = arnes_pasado()
    L = letra(tab, m['ind'], abortos, ref_ok, aok)
    log(f"\n================ LECTURA sentidos_muro · {modo} · {carpeta}")
    log(f"  arnes: {atxt} · refs: {'sha OK' if ref_ok else ref_txt} · abortos: {abortos}")
    for b in PROPIOS_BRAZOS + tuple(REFS):
        for i in sorted(tab.get(b, {})):
            f = tab[b][i]
            log(f"  {b:9s} i{i} s{f['seed']}: cruzan {f['cruzan']}/9 · mayoria {f['mayoria']} · R0 med {f['R0_med']} · fund med {f['fund_med']} "
                f"media {f['fund_media']}" + (f" · siembra riesgo {f.get('siembra_riesgo')} s9/10 {f.get('siembra_s3')}" if 'siembra_riesgo' in f else '')
                + (f" · banco riesgo {f.get('banco_riesgo')} · fund de banco {f.get('fund_de_banco')}/{f.get('fund_n')}" if 'fund_n' in f else ''))
    for k in ('validez', 'v143_R0_med', 'suma_cruzan', 'mayorias', 'pareados', 'puertas', 'modesto'): log(f"  {k}: {L[k]}")
    pq = predicciones(tab, L) if modo == 'explora' else []
    for q in pq: log(f"  {q[0]} {q[1]} (p {q[4]}): medido {q[2]} -> {'CUMPLE' if q[3] else 'REFUTADA'}")
    ver = ('HUMO (no cuenta; sin referencias): ' if modo == 'humo' else '') + L['veredicto']
    out = os.path.join(carpeta, 'lectura_sentidos_muro.json')
    json.dump(dict(modo=modo, letra=L, tabla={b: {str(i): f for i, f in v.items()} for b, v in tab.items()}, abortos=abortos,
                   predicciones=[[q[0], q[1], q[2], bool(q[3]), q[4]] for q in pq], preregistro=PRERREGISTRO,
                   sha_runner=h16(os.path.abspath(__file__))), open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    log(f"  LECTURA {out}")
    log(f"VEREDICTO ({PRERREGISTRO} sec. 6): {ver}")
    return L


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for n, b in CSM.todas().items():
        ruta = os.path.join(CARROS, n + '.py'); i = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = RC.revisa_fuente(b.decode('utf-8'), n); ok &= i and not vr
        log(f"  carro {n} sha {CSM.h16b(b)} == construye_sm: {i} · revisa_carro: {'PASA' if not vr else vr[:2]}")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115
    if a.lee:
        c = a.lee if os.path.isabs(a.lee) else os.path.join(AQUI, a.lee)
        LOGF = open(os.path.join(c, 'lectura.txt'), 'w', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        lee(c, log); return 0
    modo = 'humo' if a.humo else 'explora'
    if a.humo and a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
    if a.pool > POOL_MAX: raise SystemExit(f"--pool: maximo {POOL_MAX}")
    m = MODOS[modo]; os.makedirs(DATOS, exist_ok=True)
    prev = sorted(d for d in os.listdir(DATOS) if d.startswith(modo + '_'))
    carpeta = os.path.join(DATOS, prev[-1] if (a.reanuda and prev) else time.strftime(f'{modo}_%Y%m%d_%H%M%S'))
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time()
    log(f"CORRE_SENTIDOS_MURO · {modo} · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {platform.python_version()} · pool {a.pool or 'NO'} · "
        f"runner {h16(os.path.abspath(__file__))} · {PRERREGISTRO} · indices {m['ind']} · npas {m['npas']} · T_pas {m['T_pas']} · T_pru {m['T_pru']} · "
        f"pasajes {sem_pas(m, m['ind'][0], 0)}.. · prueba {[sem_pru(m, i) for i in m['ind']]} · CFG {CFG} · {carpeta}")
    if not verifica(log): log("  ALGO FALLA -> no se corre."); return 1
    if modo == 'explora':
        aok, atxt = arnes_pasado(); log(f"  arnes: {atxt}")
        if not aok: log("  el arnes no esta pasado con los shas actuales -> no se corre."); return 1
    tareas = [('pas', i, b, carpeta, modo) for b in ('bq3_pas', 'bq2_pas') for i in m['ind']]
    tareas += [('uno', i, b, carpeta, modo) for b in ('bq3', 'forzada3') for i in m['ind']]
    X = []

    def informa(x):
        X.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['tipo']} i{x['i']} {x['brazo']} ({x['seg']}s) aborto {x['aborto']} · cruzan "
                         f"{x.get('cruzan')} · R0 {x.get('R0')} · fund {x.get('fund')} · siembra por pasaje {x.get('siembra')}")
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
