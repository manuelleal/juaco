"""corre_mut.py — CONDICIONES / MUTACION (30-sep-2026, creador; DIAGNOSTICO EXPLORATORIO). Preregistro: PREREGISTRO_mutacion.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

PREGUNTA (junta Fable, genetista): "la seleccion no inventa combinaciones" puede ser CARGA MUTACIONAL. En `moneda` (29-sep) la perdida por
regla es ~0.11 por generacion, cerca del umbral de error. Replica de `moneda` con TODAS las tasas / 10 (p_campo 0.01, p_dup 0.002,
p_del 0.007, p_ins 0.005). Todo lo demas igual: brazos moneda / neutra / cero, 10 pasajes de 25k, la misma medida (fraccion de listas de
clase A en la siembra), la misma prueba descriptiva a 100k.

ENTRADA (regla 14): TODA corrida ES bloques_pista/corre_bp.tarea(seed, 'V143_BQ3', T, cfg=<cfg del brazo>, forzada=None, siembra) (la
misma entrada que usa moneda/corre_moneda.tarea; se IMPORTA corre_moneda, no se toca; sha fijado). Las tasas son CONFIGURACION del runner
(cfg explicito en cada tarea: corre_bp.prepara fija BQ_C del carro); el carro V143_BQ3 no se toca.
Con TASAS = 'fabrica' (SOLO arnes) este runner ES corre_moneda bit a bit (arnes F).

SEMILLAS NUEVAS (grep 30-sep: 634xxx no aparece en .py/.md/.txt de PROYECTOS/JUACO/organelos salvo como cifras de floats en un log):
  pasaje p del indice i (1..5): 634100 + 10 i + p (634110-634159), LAS MISMAS en los tres brazos (pareado)
  prueba (solo moneda, descriptiva): 59201-59205 = las de moneda (29-sep), pareada con su prueba a tasas x1 y con forzada3 / bq3_pas GUARDADOS
  humo: pasajes 634180 + p, prueba 634191 · arnes 634192.
Pool: MAXIMO 2. Cada trabajo registra los carros y fija cfg al entrar, atrapa TODO y escribe cada JSON ANTES de volver (ERR-54).
--reanuda sigue la ultima carpeta y REINTENTA los JSON con aborto (los buenos no se recorren). ERR-115: banderas exactas.

  python experimentos/organelos/condiciones/mutacion/identidad_mut.py                    # arnes (escribe identidad_mut_salida.txt)
  python experimentos/organelos/condiciones/mutacion/corre_mut.py --humo                 # 1 proceso, 6 corridas, 135 000 pasos
  python experimentos/organelos/condiciones/mutacion/corre_mut.py --explora --pool 2     # 15 cadenas (10 x 25k) + 5 pruebas 100k
  python experimentos/organelos/condiciones/mutacion/corre_mut.py --explora --pool 2 --reanuda
  python experimentos/organelos/condiciones/mutacion/corre_mut.py --lee datos/explora_<fecha>
"""
import argparse, hashlib, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(AQUI))))
MOND = os.path.join(RAIZ, 'experimentos', 'organelos', 'moneda')
for _d in (AQUI, MOND):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_moneda as M   # siembra0, frac, es_A, cadena, fila_prueba, verifica, REFS (se IMPORTA, no se toca; sha fijado)
SM = M.SM; CBP = M.CBP

PRERREGISTRO = 'PREREGISTRO_mutacion.md'
DATOS = os.path.join(AQUI, 'datos')
MEXP = os.path.join(MOND, 'datos', 'explora_20260929_121648')
SHAS = {os.path.join(MOND, 'corre_moneda.py'): '0441aa7bf5b94316', os.path.join(MOND, 'identidad_moneda.py'): 'ceede3d6458597ac'}
# prueba de moneda a tasas x1 (29-sep), pareada por semilla con la de este runner; y la lectura de moneda (finales p9 a tasas x1)
REF_MX1 = ['76887fd3a09e9b5b', '74c62698acbe9f42', '381e0d9c233d2906', 'c38771be6759281c', 'a0a181996f3401a0']
REF_LECT = (os.path.join(MEXP, 'lectura_moneda.json'), '45d316a8de26cf20')
REF_P0 = (os.path.join(MEXP, 'pasaje_moneda_i1_p0.json'), 'fe9dc0379be9aa70')   # arnes F: reproduccion bit a bit a tasas de fabrica

CFG = dict(M.CFG); CERO = dict(M.CERO)
CFG10 = dict(CFG, p_campo=0.01, p_dup=0.002, p_del=0.007, p_ins=0.005)   # TODAS / 10; inicial y banco sin cambio
A = M.A; A0 = M.A0; B = M.B
# tasas -> brazo -> (fila marcada, cfg, prueba)
TASAS = {'div10': {'moneda': (A, CFG10, True), 'neutra': (A0, CFG10, False), 'cero': (A0, CERO, False)},
         'fabrica': {b: tuple(v) for b, v in M.BRAZOS.items()}}   # SOLO arnes: == corre_moneda.BRAZOS
MODOS = {'explora': dict(ind=[1, 2, 3, 4, 5], npas=10, T_pas=25000, T_pru=100000, base_pas=634100, base_pru=59200,
                         brazos=('moneda', 'neutra', 'cero'), tasas='div10'),
         'humo': dict(ind=[8], npas=2, T_pas=25000, T_pru=10000, base_pas=634100, base_pru=634183, brazos=('moneda', 'neutra', 'cero'),
                      npas_por_brazo={'cero': 1}, tasas='div10')}
SEM_ARNES = 634192
POOL_MAX = 2
# LA LETRA (PREREGISTRO sec. 6)
PAGA_N = 4; PURGA_N = 4; MITAD = 0.5; NEUTRA_MIN = 0.10; CERO_BANDA = (0.25, 0.75); INTACTA_MIN = 0.80; MARGEN = 0.05


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sem_pas(m, i, p): return m['base_pas'] + 10 * i + p
def sem_pru(m, i): return m['base_pru'] + i
def npas(m, b): return m.get('npas_por_brazo', {}).get(b, m['npas'])


def siembra0(brazo, tasas='div10'):
    a = TASAS[tasas][brazo][0]
    return [[list(a)] if k % 2 == 0 else [list(B)] for k in range(M.NSIE)]


def intacta(S, brazo):
    """Fraccion de listas de la siembra que son EXACTAMENTE un genotipo inyectado ([marcada] o [B]): mide la carga (cuanto muto)."""
    g = {json.dumps(L) for L in siembra0(brazo)}
    return round(sum(json.dumps(R) in g for R in S) / len(S), 4) if S else None


def tarea(seed, brazo, T, siembra, tasas='div10'):
    """UNA corrida: corre_bp.tarea(seed, 'V143_BQ3', T, cfg del brazo, forzada None, siembra) (la entrada de corre_moneda)."""
    SM.registra()
    cfg = TASAS[tasas][brazo][1]
    x = CBP.tarea(seed, 'V143_BQ3', T, cfg=dict(cfg), forzada=None, siembra=siembra)
    x['brazo'] = brazo; x['carro'] = 'V143_BQ3'
    return x


def _corrida(fin, seed, brazo, T, siembra, extra, tasas):
    x = M._ok_previo(fin)
    if x is not None: return x
    reint = os.path.exists(fin); t0 = time.time()
    try:
        x = tarea(seed, brazo, T, siembra, tasas); x['aborto'] = None
    except BaseException as e:   # noqa: nube-9
        x = dict(seed=seed, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    x.update(extra); x['T'] = T; x['seg_trabajo'] = round(time.time() - t0, 1); x['siembra_n'] = len(siembra)
    x['frac_A_entra'] = M.frac(siembra)
    if reint: x['reintento_de'] = 'aborto'
    M._guarda(fin, x)
    return x


def trabajo(args):
    """UN trabajo = una cadena (brazo, indice): NPAS pasajes + (solo moneda) la prueba. cfg fijado en CADA worker (registra + cfg explicito)."""
    brazo, i, carpeta, modo = args
    m = MODOS[modo]; tz = m['tasas']; t0 = time.time(); fr = []; aborto = None; out = dict(brazo=brazo, i=i)
    try:
        SM.registra()
        sb = siembra0(brazo, tz); fr.append(M.frac(sb))
        for p in range(npas(m, brazo)):
            x = _corrida(os.path.join(carpeta, f"pasaje_{brazo}_i{i}_p{p}.json"), sem_pas(m, i, p), brazo, m['T_pas'], sb,
                         dict(i=i, p=p, tipo='pasaje'), tz)
            if x.get('aborto'): aborto = f"pasaje {p}: {x['aborto']}"; break
            sb = CBP.siembra_de(x); fr.append(M.frac(sb))
            if not sb: aborto = f"pasaje {p}: siembra vacia"; break
        if aborto is None and TASAS[tz][brazo][2]:
            x = _corrida(os.path.join(carpeta, f"{brazo}_s{sem_pru(m, i)}.json"), sem_pru(m, i), brazo, m['T_pru'], sb,
                         dict(i=i, tipo='prueba', siembra_final=sb), tz)
            aborto = x.get('aborto'); L = x.get('linajes', [])
            out.update(cruzan=sum(int(l['cruza_real']) for l in L), R0=[l['R0_real'] for l in L])
        out.update(aborto=aborto, frac_A=fr)
    except BaseException as e:   # noqa: nube-9
        out.update(aborto=f"{type(e).__name__}: {e}"[:300], frac_A=fr)
    out['seg'] = round(time.time() - t0, 1)
    return out


# ------------------------------------------------------------------ lectura y LA LETRA
def _med(xs):
    xs = [x for x in xs if x is not None]; return round(float(st.median(xs)), 4) if xs else None


def cadena(carpeta, m, brazo, i):
    """corre_moneda.cadena (fracciones, arrastre, partos, vivos, solo_inyectadas) + intacta por pasaje + genotipos nuevos."""
    c, ab = M.cadena(carpeta, m, brazo, i)   # usa corre_moneda.siembra0(brazo): mismas filas marcadas (arnes I)
    if c is None: return c, ab
    it = []; nuevos = 0; g = {json.dumps(L) for L in siembra0(brazo)}
    for p in range(npas(m, brazo)):
        x = json.load(open(os.path.join(carpeta, f"pasaje_{brazo}_i{i}_p{p}.json"), encoding='utf-8'))
        S = CBP.siembra_de(x); it.append(intacta(S, brazo)); nuevos += sum(1 for R in S if json.dumps(R) not in g)
    c['intacta'] = it; c['listas_mutadas_total'] = nuevos
    return c, None


def carga(carpeta, modo):
    m = MODOS[modo]; C = {}; abortos = []; P_ = {}; refs = {b: {} for b in list(M.REFS) + ['moneda_x1']}; ref_ok = True; ref_txt = []
    for b in m['brazos']:
        C[b] = {}
        for i in m['ind']:
            c, ab = cadena(carpeta, m, b, i)
            if c is None: abortos.append(ab); continue
            C[b][i] = c
    for i in m['ind']:
        fin = os.path.join(carpeta, f"moneda_s{sem_pru(m, i)}.json")
        if not os.path.exists(fin): abortos.append(f"falta prueba moneda i{i}"); continue
        x = json.load(open(fin, encoding='utf-8'))
        if x.get('aborto'): abortos.append(f"prueba moneda i{i}: {x['aborto']}"); continue
        P_[i] = M.fila_prueba(x)
    lect = None
    if modo == 'explora':
        todos = dict(M.REFS); todos['moneda_x1'] = REF_MX1
        for b, shas in todos.items():
            d = MEXP if b == 'moneda_x1' else M.SMEXP; nb = 'moneda' if b == 'moneda_x1' else b
            for i, sh in zip(m['ind'], shas):
                fin = os.path.join(d, f"{nb}_s{sem_pru(m, i)}.json"); s = h16(fin) if os.path.exists(fin) else None
                if s != sh: ref_ok = False; ref_txt.append(f"{b} s{sem_pru(m, i)} sha {s} != {sh}"); continue
                refs[b][i] = M.fila_prueba(json.load(open(fin, encoding='utf-8')))
        s = h16(REF_LECT[0]) if os.path.exists(REF_LECT[0]) else None
        if s != REF_LECT[1]: ref_ok = False; ref_txt.append(f"lectura moneda sha {s} != {REF_LECT[1]}")
        else: lect = json.load(open(REF_LECT[0], encoding='utf-8'))['letra']['final']
    return C, P_, refs, abortos, ref_ok, ref_txt, lect


def letra(C, ind, abortos, ref_ok, arnes_ok, n_pru=None):
    """PREREGISTRO sec. 6. C[brazo][i] = cadena. Veredicto: PAGA / PURGA / OTRA MONEDA / NO SE LEE."""
    n = len(ind)
    fin = {b: {i: C[b][i]['f'][-1] for i in C.get(b, {})} for b in C}
    cero = [fin['cero'][i] for i in fin.get('cero', {})]
    it_neu = [C['neutra'][i]['intacta'][-1] for i in C.get('neutra', {})]
    mut = sum(C[b][i].get('listas_mutadas_total', 0) for b in ('moneda', 'neutra') for i in C.get(b, {}))
    val = dict(abortos_0=(len(abortos) == 0),
               completas=all(len(C.get(b, {})) == n for b in ('moneda', 'neutra', 'cero')) and (n_pru is None or n_pru == n),
               f_ini_05=all(c['f_ini'] == 0.5 for b in C for c in C[b].values()),
               cero_solo_inyectadas=all(c['solo_inyectadas'] for c in C.get('cero', {}).values()) and len(C.get('cero', {})) == n,
               cero_banda=(len(cero) == n and CERO_BANDA[0] <= st.mean(cero) <= CERO_BANDA[1]),
               carga_baja=(len(it_neu) == n and _med(it_neu) >= INTACTA_MIN),
               tasas_actuan=(mut > 0),
               refs_sha=bool(ref_ok), arnes=bool(arnes_ok))
    valido = all(val.values())
    I = [i for i in ind if i in fin.get('moneda', {}) and i in fin.get('neutra', {})]
    mayor = sum(1 for i in I if fin['moneda'][i] > fin['neutra'][i])
    mitad = sum(1 for i in I if fin['moneda'][i] <= MITAD * fin['neutra'][i])
    margen = sum(1 for i in I if fin['moneda'][i] - fin['neutra'][i] >= MARGEN)   # descriptivo
    neu_med = _med(list(fin.get('neutra', {}).values()))
    if not valido: ver = 'NO SE LEE'
    elif mayor >= PAGA_N: ver = 'PAGA'
    elif mitad >= PURGA_N and neu_med is not None and neu_med >= NEUTRA_MIN: ver = 'PURGA'
    else: ver = 'OTRA MONEDA'
    return dict(validez=val, veredicto=ver, moneda_mayor_que_neutra=f"{mayor}/{len(I)}", moneda_le_mitad_neutra=f"{mitad}/{len(I)}",
                moneda_mayor_con_margen_005=f"{margen}/{len(I)}", neutra_mediana_p9=neu_med, moneda_mediana_p9=_med(list(fin.get('moneda', {}).values())),
                dif_mediana_moneda_menos_neutra=_med([fin['moneda'][i] - fin['neutra'][i] for i in I]),
                final={b: {str(i): v for i, v in d.items()} for b, d in fin.items()},
                cero_media=(round(st.mean(cero), 4) if cero else None), cero_mediana=_med(cero), intacta_neutra_p9_mediana=_med(it_neu),
                listas_mutadas_moneda_neutra=mut)


def predicciones(C, P_, L):
    ne = list(L['final'].get('neutra', {}).values())
    cz = sum(f['cruzan'] for f in P_.values()) if P_ else None
    dnc = None
    if L['neutra_mediana_p9'] is not None and L['cero_mediana'] is not None: dnc = round(L['neutra_mediana_p9'] - L['cero_mediana'], 4)
    return [('G1', 'genetista: neutra, mediana de la fraccion A en p9 en [0.30, 0.45] (p asignada por el creador)', _med(ne),
             _med(ne) is not None and 0.30 <= _med(ne) <= 0.45, 0.55),
            ('K1', 'veredicto OTRA MONEDA', L['veredicto'], L['veredicto'] == 'OTRA MONEDA', 0.65),
            ('K2', 'veredicto PAGA', L['veredicto'], L['veredicto'] == 'PAGA', 0.20),
            ('K3', 'veredicto PURGA', L['veredicto'], L['veredicto'] == 'PURGA', 0.10),
            ('K4', '|mediana neutra - mediana cero| en p9 < 0.10', dnc, dnc is not None and abs(dnc) < 0.10, 0.65),
            ('K5', 'intacta de la neutra en p9 (mediana) >= 0.85', L['intacta_neutra_p9_mediana'],
             (L['intacta_neutra_p9_mediana'] or 0) >= 0.85, 0.75),
            ('K6', 'prueba moneda / 10: suma de cruzan (de 45) en [8, 24]', cz, cz is not None and 8 <= cz <= 24, 0.60)]


def arnes_pasado():
    f = os.path.join(AQUI, 'identidad_mut_salida.txt')
    if not os.path.exists(f): return False, 'sin salida del arnes'
    t = open(f, encoding='utf-8').read()
    need = [h16(os.path.abspath(__file__)), h16(os.path.join(AQUI, 'identidad_mut.py'))]
    ok = 'ARNES: PASA' in t and all(s in t for s in need)
    return ok, ('PASA con los shas actuales' if ok else f'no PASA o no cita los shas actuales {need}')


def lee(carpeta, log=print, modo=None):
    modo = modo or ('humo' if os.path.basename(carpeta).startswith('humo') else 'explora')
    m = MODOS[modo]; C, P_, refs, abortos, ref_ok, ref_txt, lect = carga(carpeta, modo)
    aok, atxt = arnes_pasado()
    L = letra(C, m['ind'], abortos, ref_ok, aok, n_pru=len(P_))
    log(f"\n================ LECTURA mutacion (tasas / 10) · {modo} · {carpeta}")
    log(f"  arnes: {atxt} · refs: {'sha OK' if ref_ok else ref_txt} · abortos: {abortos}")
    for b in m['brazos']:
        for i in sorted(C.get(b, {})):
            c = C[b][i]
            log(f"  {b:6s} i{i}: fraccion A  ini {c['f_ini']} -> p0..p{len(c['f'])-1} {c['f']}")
            log(f"  {'':6s}     intacta {c['intacta']} · listas mutadas (suma) {c['listas_mutadas_total']} · vivos con A {c['vivos_A']}")
            log(f"  {'':6s}     arrastre>= {c['arrastre']} · partos {c['partos']} · solo inyectadas {c['solo_inyectadas']}")
    for i in sorted(P_):
        f = P_[i]; ex = ' · '.join(f"{b} {refs[b][i]['cruzan']}/9" for b in refs if i in refs[b])
        log(f"  prueba moneda/10 i{i} s{f['seed']}: cruzan {f['cruzan']}/9 · mayoria {f['mayoria']} · R0 med {f['R0_med']} · fund med {f['fund_med']} "
            f"· descendientes {f['desc']} || guardados: {ex}")
    sumas = {'moneda_div10': sum(f['cruzan'] for f in P_.values())}
    sumas.update({b: sum(f['cruzan'] for f in refs[b].values()) for b in refs})
    log(f"  suma cruzan (de {9 * len(m['ind'])}): {sumas}")
    if lect: log(f"  referencia moneda a tasas x1 (29-sep), fraccion A en p9: {lect}")
    for k in ('validez', 'final', 'cero_media', 'cero_mediana', 'intacta_neutra_p9_mediana', 'listas_mutadas_moneda_neutra', 'moneda_mayor_que_neutra',
              'moneda_le_mitad_neutra', 'moneda_mayor_con_margen_005', 'neutra_mediana_p9', 'moneda_mediana_p9', 'dif_mediana_moneda_menos_neutra'):
        log(f"  {k}: {L[k]}")
    pq = predicciones(C, P_, L) if modo == 'explora' else []
    for q in pq: log(f"  {q[0]} {q[1]} (p {q[4]}): medido {q[2]} -> {'CUMPLE' if q[3] else 'REFUTADA'}")
    ver = ('HUMO (no cuenta; sin referencias, 2 pasajes): ' if modo == 'humo' else '') + L['veredicto']
    out = os.path.join(carpeta, 'lectura_mut.json')
    json.dump(dict(modo=modo, letra=L, cadenas={b: {str(i): {k: v for k, v in c.items() if k != 'siembra_final'} for i, c in d.items()}
                                                 for b, d in C.items()},
                   prueba={str(i): f for i, f in P_.items()}, refs={b: {str(i): f for i, f in d.items()} for b, d in refs.items()},
                   ref_moneda_x1_p9=lect, sumas=sumas, abortos=abortos, predicciones=[[q[0], q[1], q[2], bool(q[3]), q[4]] for q in pq],
                   preregistro=PRERREGISTRO, sha_runner=h16(os.path.abspath(__file__))),
              open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    log(f"  LECTURA {out}")
    log(f"VEREDICTO ({PRERREGISTRO} sec. 6): {ver}")
    return L


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    log("  -- verifica de corre_moneda (shas de sentidos_muro, corre_bp, V143_BQ3; pista, juez, carros):")
    ok &= M.verifica(lambda s: log('  ' + s))
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
    log(f"CORRE_MUT · {modo} · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {platform.python_version()} · pool {a.pool or 'NO'} · "
        f"runner {h16(os.path.abspath(__file__))} · {PRERREGISTRO} · indices {m['ind']} · npas {m['npas']} · T_pas {m['T_pas']} · T_pru {m['T_pru']} · "
        f"pasajes {sem_pas(m, m['ind'][0], 0)}.. · prueba {[sem_pru(m, i) for i in m['ind']]} · CFG10 {CFG10} · CERO {CERO} · {carpeta}")
    if not verifica(log): log("  ALGO FALLA -> no se corre."); return 1
    if modo == 'explora':
        aok, atxt = arnes_pasado(); log(f"  arnes: {atxt}")
        if not aok: log("  el arnes no esta pasado con los shas actuales -> no se corre."); return 1
    tareas = [(b, i, carpeta, modo) for b in m['brazos'] for i in m['ind']]
    tareas.sort(key=lambda t: 0 if t[0] == 'moneda' else 1)   # las largas (con prueba) primero
    X = []

    def informa(x):
        X.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} i{x['i']} ({x['seg']}s) aborto {x['aborto']} · fraccion A {x.get('frac_A')} · "
                         f"cruzan {x.get('cruzan')}")
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
