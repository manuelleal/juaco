"""corre_veto_muro.py — RUNNER y LETRA del CONFIRMATORIO "TERMO + PATAS + VETO POR RESERVAS" contra el muro de la carrera.
Preregistro: PREREGISTRO_veto_muro.md (la letra esta AQUI, en lee(), y alli en la sec. 5).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE CONFIRMA: el hijo de TERMO muere joven (13 % en <= 200 pasos; 47.5 % de veneno o sal) porque la boca de fabrica muerde lo malo con
hambre. VETO_PISO (el piso de O1._costeable, solo: no morder lo sentido malo si el golpe deja la necesidad golpeada bajo 0.2, o bajo
rep_umbral si la ventana de parto corre) sobre TERMO + PATAS 3 (brazo tpv). Semillas FRESCAS 53701-53740 (grep de colisiones: 0).
Medida principal = SUMA de linajes que cruzan (cruza_real, ENMIENDA 5) sobre 20 x 9 = 180, pareada por semilla; la letra del muro
(mayoria que cruza >= 15/20) es una puerta APARTE.

CARROS:
  tpv    TVPISO_31   experimentos/organelos/veto_muro/carros/TVPISO.py  sha (SHAS)  PATAS 3 VETOP 1   (CANDIDATO: TERMO+PATAS+VETO_PISO)
  tv     TVPISO_01   (mismo archivo)                                                PATAS 0 VETOP 1   (ABLACION sin patas: TERMO+VETO_PISO)
  vinv   TVPISO_32   (mismo archivo)                                                PATAS 3 VETOP 2   (CONTROL desfasado: lee la necesidad que el golpe NO toca)
  pc     TPATAS_3    experimentos/organelos/dinamita/carros/TPATAS.py   1b6272ef4616af8b  PATAS 3   (ABLACION sin veto: TERMO+PATAS)
  termo  V143_TERMO  experimentos/organelos/termo/carros/V143_TERMO.py  3db639cab75641fb        (la BASE)
  o1     O1          carrera_escuderias/carros/O1.py                                           (ANCLA / techo)
  v143   V143        tronco_v14_3/carros_v143/V143.py                                          (ANCLA / el bicho real)
  TVPISO se construye POR ANCLAS desde TPATAS (construye_veto_muro.py). Cada brazo es una instancia de modulo PROPIA; las perillas
  PATAS y VETOP se FIJAN en cada worker dentro de trabajo() (fija()) y se escriben en el JSON ('estado'); lee() lo verifica (V4).

ENTRADA (regla 14): la corrida ES experimentos/tronco_v14_3/corre_v143.tarea (se IMPORTA, no se toca) = juez.tarea(seed, 9 carros
iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje. Lo unico agregado: 'tel_vm'
(telemetria de SOLO LECTURA de la ultima instancia de cada linaje: termo, patas, vpiso) y 'estado'. Arnes: identidad_veto_muro.py.

SEMILLAS: serie 53701-53720 · replica 53721-53740 · arnes 53791-53792 · humo 53793. T 100 000 (humo 20 000).

Uso (banderas desconocidas o abreviadas ABORTAN, ERR-115; --serie/--replica SOLO el coordinador, DESPUES de que termine patas_muro, y SOLO
con el preregistro y este runner commiteados y sin cambios respecto de HEAD):
  python experimentos/organelos/veto_muro/corre_veto_muro.py --humo                       # 1 proceso, 6 corridas (tpv tv vinv pc termo o1), T 20 000
  python experimentos/organelos/veto_muro/corre_veto_muro.py --humo --reanuda             # 2o proceso: la 7a (v143), salta lo escrito y lee
  python experimentos/organelos/veto_muro/corre_veto_muro.py --serie --pool 2             # 140 corridas (7 brazos x 20); se niega si ya hay veredicto
  python experimentos/organelos/veto_muro/corre_veto_muro.py --serie --pool 2 --reanuda
  python experimentos/organelos/veto_muro/corre_veto_muro.py --replica --pool 2           # solo si la serie da FUNCIONA o MODESTO
  python experimentos/organelos/veto_muro/corre_veto_muro.py --lee <carpeta>              # re-lee una carpeta con la letra
  python experimentos/organelos/veto_muro/corre_veto_muro.py --bloque <resumen serie>.json,<resumen replica>.json
"""
import argparse, glob, hashlib, importlib.util, json, math, os, platform, statistics as st, subprocess, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
TERMOD = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')
DINAD = os.path.join(RAIZ, 'experimentos', 'organelos', 'dinamita')
for _d in (AQUI, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV          # tarea, resume, pareado (se IMPORTA, no se toca)
P = CV.P; J = CV.J

PRERREGISTRO = 'PREREGISTRO_veto_muro.md'
DATOS = os.path.join(AQUI, 'datos')
TERMO_PY = os.path.join(TERMOD, 'carros', 'V143_TERMO.py')
TPATAS_PY = os.path.join(DINAD, 'carros', 'TPATAS.py')
TVPISO_PY = os.path.join(AQUI, 'carros', 'TVPISO.py')
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028', os.path.join(PISTA, 'revisa_carro.py'): '1c8a789f7427ab96',
        os.path.join(DINAD, 'construye_patas.py'): '85a8c136aa09491d', TPATAS_PY: '1b6272ef4616af8b', TERMO_PY: '3db639cab75641fb',
        os.path.join(AQUI, 'construye_veto_muro.py'): '779c5cd8bea2db85', TVPISO_PY: '7653cd267790500b'}
# brazo -> (nombre del carro en corre_v143._MODS, archivo propio o None, PATAS o None, VETOP o None)
BRAZOS = {'tpv': ('TVPISO_31', TVPISO_PY, 3, 1), 'tv': ('TVPISO_01', TVPISO_PY, 0, 1), 'vinv': ('TVPISO_32', TVPISO_PY, 3, 2),
          'pc': ('TPATAS_3', TPATAS_PY, 3, None), 'termo': ('V143_TERMO', TERMO_PY, None, None),
          'o1': ('O1', None, None, None), 'v143': ('V143', None, None, None)}
ORDEN = ('tpv', 'tv', 'vinv', 'pc', 'termo', 'o1', 'v143')
VETO_BRAZOS = ('tpv', 'tv', 'vinv'); PATAS_BRAZOS = ('tpv', 'vinv', 'pc')
CAND = 'tpv'; BASE = 'termo'; CTRL = 'vinv'
SERIE = range(53701, 53721); REPLICA = range(53721, 53741); ARNES = (53791, 53792); HUMO_S = (53793,)
HUMO = [(53793, b) for b in ORDEN]          # 7 corridas: --humo corre las 6 primeras (maximo por proceso); --humo --reanuda la 7a (v143)
T_DEF = 100000; T_HUMO = 20000; POOL_MAX = 2
# ------------------------------------------------------------------ constantes de la LETRA (PREREGISTRO sec. 5), para n = 20 semillas
GANA_PAR = 13          # PA/PD: el candidato tiene MAS linajes que cruzan que el otro brazo en >= 13/20 semillas (empates EN CONTRA)
MARGEN = 15            # PB/PD: suma de linajes que cruzan (de 180) del candidato >= la del otro + 15
MAYORIA = 15           # PC (letra del muro, ENMIENDA 5): semillas con mayoria de linajes que cruzan (>= 5/9) >= 15/20
O1_MIN = 17            # V2: O1 con mayoria que cruza en >= 17/20
ANCLA_V143 = (0.40, 0.80)   # V3: V143, mediana del R0 real (historico 0.536-0.634)
BANDA_TERMO = (70, 120)     # V6: termo, suma de linajes que cruzan de 180 (historico 96 y 95; ola 3 44/90)
H200 = 0.05                 # descriptivo: prediccion hijos muertos en <= 200 pasos del candidato


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None
def esc(k, n): return math.ceil(k * n / 20 - 1e-9)   # umbral escalado (solo para el humo, que NO cuenta)


def nombres():
    for b, (n, _, _, _) in BRAZOS.items(): CV.BRAZOS[b] = n   # corre_v143.resume lee su tabla BRAZOS (en memoria)


def fija(brazo):
    """ESTADO fijado en ESTE proceso (worker de Pool, --reanuda o arnes): carga la instancia PROPIA del brazo si falta, verifica el sha del
    archivo y FIJA las perillas PATAS y VETOP siempre (aunque alguien las haya cambiado). Devuelve el estado que se escribe en el JSON."""
    nombres()
    n, ruta, pv, vv = BRAZOS[brazo]
    if ruta is None:
        CV.modulo(n); return dict(carro=n, sha=None, PATAS=None, VETOP=None, TERMO=None)
    s = h16(ruta)
    if s != SHAS[ruta]: raise SystemExit(f"sha {ruta} {s} != {SHAS[ruta]}")
    m = CV._MODS.get(n)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{n}", ruta)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    if pv is not None: m.PATAS = pv
    if vv is not None: m.VETOP = vv
    if m.TERMO != 1: raise SystemExit(f"{n}: TERMO {m.TERMO} != 1")
    return dict(carro=n, sha=s, PATAS=getattr(m, 'PATAS', None), VETOP=getattr(m, 'VETOP', None), TERMO=m.TERMO)


def tarea(args):
    """(seed, brazo, T) -> corre_v143.tarea tal cual + 'tel_vm' (solo lectura) + 'estado'."""
    seed, brazo, T = args
    est = fija(brazo)
    cap = []; orig = P.run

    def run2(*a, **k):
        r = orig(*a, **k)
        cap.append([{kk: (d.get('carro') or {}).get(kk) for kk in ('termo', 'patas', 'vpiso')} for d in r['linajes']])
        return r
    P.run = run2
    try:
        x = CV.tarea((seed, BRAZOS[brazo][0], T))
    finally:
        P.run = orig
    x['tel_vm'] = cap[0] if cap else None; x['estado'] = est
    return x


def trabajo(args):
    """UNA corrida; atrapa TODO (nube-9); escribe su JSON ANTES de volver (ERR-54); con reanuda salta la que ya existe SIN aborto
    (un aborto guardado se reintenta y queda anotado en 'reintento_de')."""
    seed, brazo, T, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json"); previo = None
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
        previo = x0['aborto']
    try:
        x = tarea((seed, brazo, T)); x.pop('pizarra_log', None); x['brazo'] = brazo; x['T'] = T; x['aborto'] = None
    except BaseException as e:   # noqa: nube-9
        x = dict(seed=seed, brazo=brazo, T=T, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    if previo: x['reintento_de'] = previo
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ medidas
def cz(d): return sum(int(l['cruza_real']) for l in d['linajes'])


def par_cruzan(A, B, sem):
    """Pareado por semilla en LINAJES QUE CRUZAN (0-9 por semilla). gana = semillas con A > B (empates EN CONTRA)."""
    a = [cz(A[s]) for s in sem]; b = [cz(B[s]) for s in sem]
    return dict(semillas=len(sem), gana=sum(x > y for x, y in zip(a, b)), empata=sum(x == y for x, y in zip(a, b)),
                pierde=sum(x < y for x, y in zip(a, b)), suma_a=sum(a), suma_b=sum(b), dif=sum(a) - sum(b), por_semilla_a=a, por_semilla_b=b)


def hijos(d):
    """DESCRIPTIVO: los cuerpos HIJOS (origen 1) ya muertos de una corrida: muertos en <= 200 pasos, vida mediana, causa veneno/sal,
    muertos 'de hambre sin comer' (vida <= 620 por hambre o sed: el hijo nace a 0.6 y gasta 0.001 por paso), fraccion que pare."""
    n = h2 = h6 = bs = pa = 0; vid = []
    for l in d['linajes']:
        t = l['telem']
        for i in range(len(t['vidas']) - 1):          # la ultima vida puede estar viva: solo cuerpos ya muertos (causa_cuerpo)
            if t['origen'][i] != 1: continue
            v = t['vidas'][i]; c = t['causa_cuerpo'][i]
            n += 1; vid.append(v); h2 += int(v <= 201); h6 += int(v <= 620 and c in ('hambre', 'sed'))
            bs += int(c in ('veneno', 'sal')); pa += int(t['desc_por_vida'][i] > 0)
    r = lambda k: round(k / n, 4) if n else None
    return dict(n=n, h200=r(h2), h600_hambre=r(h6), veneno_sal=r(bs), paren=r(pa), vida_med=med(vid))


def mundo(D, sem):
    """DESCRIPTIVO por semilla (mediana de los 9 linajes; hijos agregados por corrida)."""
    out = {}
    for s in sem:
        L = D[s]['linajes']
        ac = [l['mord']['A'] + l['mord']['C'] for l in L]; bd = [l['mord']['B'] + l['mord']['D'] for l in L]
        c = D[s]['pista']['comp_mundo']; h = hijos(D[s])
        out[s] = dict(AC=med(ac), BD=med(bd), frac_buena=med([a / (a + b) if a + b else None for a, b in zip(ac, bd)]),
                      mundo_AC=round(c['A'] + c['C'], 4), sin_bueno=D[s]['pista']['frac_sin_bueno_mundo'],
                      fund=med([l['fundadores'] for l in L]), estab=sum(int(l['fund_post10k'] == 0) for l in L),
                      h200=h['h200'], vida_hijo=h['vida_med'], h600=h['h600_hambre'], vs_hijo=h['veneno_sal'])
    return out


def mundo_par(MA, MB, sem, k, mayor=True):
    d = [(MA[s][k], MB[s][k]) for s in sem if MA[s][k] is not None and MB[s][k] is not None]
    return dict(n=len(d), a_gana=sum((x > y) if mayor else (x < y) for x, y in d), med_a=med([x for x, _ in d]), med_b=med([y for _, y in d]))


def carga(carpeta):
    R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, '*_s*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('brazo') not in R: continue
        if d.get('aborto'): ab.append(f"{d['brazo']} s{d['seed']}: {d['aborto']}")
        else: R[d['brazo']][d['seed']] = d
    return R, ab


def suma_tel(d, pieza, k):
    return sum(((t or {}).get(pieza) or {}).get(k, 0) for t in (d.get('tel_vm') or []))


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_veto_muro.md sec. 5)
def lee(carpeta, semillas, humo=False, log=print):
    nombres()
    R, ab = carga(carpeta); n = len(semillas); sem = list(semillas)
    v = {}
    completa = all(s in R[b] for b in ORDEN for s in sem)
    coher = completa and all(l['coherente'] and l['t_fund_rec_ok'] for b in ORDEN for s in sem for l in R[b][s]['linajes'])
    v['V1_completa_0_abortos_coherente'] = bool(completa and not ab and coher and (humo or n == 20))
    if not completa:
        log(f"  INCOMPLETA: faltan {[(b, s) for b in ORDEN for s in sem if s not in R[b]][:12]} · abortos {ab[:5]}")
        return dict(validez=v, veredicto='NO SE LEE', abortos=ab)
    res = {b: CV.resume([R[b][s] for s in sem], b, log) for b in ORDEN}
    v['V2_O1_mayoria'] = res['o1']['sem_cruza_e5'] >= (esc(O1_MIN, n) if humo else O1_MIN)
    m = res['v143']['R0_real_med']
    v['V3_ancla_V143'] = m is not None and ANCLA_V143[0] <= m <= ANCLA_V143[1]
    ok4 = True
    for b in ORDEN:
        nm, ruta, pv, vv = BRAZOS[b]
        for s in sem:
            e = R[b][s].get('estado') or {}
            ok4 &= e.get('carro') == nm and (ruta is None or (e.get('sha') == SHAS[ruta] and e.get('PATAS') == pv and e.get('VETOP') == vv
                                                              and e.get('TERMO') == 1))
    v['V4_carros_por_sha_y_perillas'] = bool(ok4)
    act_v = {b: [suma_tel(R[b][s], 'vpiso', 'a_no') for s in sem] for b in VETO_BRAZOS}
    act_p = {b: [suma_tel(R[b][s], 'patas', 'cambia') for s in sem] for b in PATAS_BRAZOS}
    v['V5_piezas_actuan'] = all(x > 0 for b in VETO_BRAZOS for x in act_v[b]) and all(x > 0 for b in PATAS_BRAZOS for x in act_p[b])
    st_ = sum(cz(R['termo'][s]) for s in sem); bt = (BANDA_TERMO[0] * n / 20, BANDA_TERMO[1] * n / 20)
    v['V6_banda_termo'] = bt[0] <= st_ <= bt[1]
    valido = all(v.values())
    PARES = (('tpv', 'termo'), ('tpv', 'vinv'), ('tpv', 'pc'), ('tpv', 'tv'), ('tv', 'termo'), ('pc', 'termo'), ('vinv', 'termo'),
             ('o1', 'tpv'), ('o1', 'termo'), ('termo', 'v143'))
    pz = {f"{a}_vs_{b}": par_cruzan(R[a], R[b], sem) for a, b in PARES}
    pr = {f"{a}_vs_{b}": CV.pareado([R[a][s] for s in sem], [R[b][s] for s in sem]) for a, b in PARES}
    g = esc(GANA_PAR, n) if humo else GANA_PAR; my = esc(MAYORIA, n) if humo else MAYORIA
    x = pz['tpv_vs_termo']; y = pz['tpv_vs_vinv']
    p = dict(PA_tpv_mas_cruzan_que_termo=x['gana'] >= g, PB_suma_tpv_ge_termo_mas_15=x['dif'] >= MARGEN,
             PD_control_tpv_sobre_vinv=(y['gana'] >= g and y['dif'] >= MARGEN), PC_letra_muro_tpv_mayoria=res['tpv']['sem_cruza_e5'] >= my)
    if not valido: ver = 'NO SE LEE'
    elif p['PA_tpv_mas_cruzan_que_termo'] and p['PB_suma_tpv_ge_termo_mas_15'] and p['PD_control_tpv_sobre_vinv']:
        ver = 'FUNCIONA' if p['PC_letra_muro_tpv_mayoria'] else 'HAY ALGO MODESTO'
    else: ver = 'NO'
    ver_nota = 'NO (inespecifico)' if (ver == 'NO' and valido and p['PA_tpv_mas_cruzan_que_termo'] and p['PB_suma_tpv_ge_termo_mas_15']) else ver
    umbral = dict(PA=x['gana'] == g, PB=MARGEN <= x['dif'] <= MARGEN + 2, PD=(y['gana'] == g or MARGEN <= y['dif'] <= MARGEN + 2),
                  PC=res['tpv']['sem_cruza_e5'] == my)   # auditoria C3: 'en el umbral' se extiende a PD y a PC (PC solo cuenta en FUNCIONA)
    en_umbral = bool(ver in ('FUNCIONA', 'HAY ALGO MODESTO') and (umbral['PA'] or umbral['PB'] or umbral['PD'] or (ver == 'FUNCIONA' and umbral['PC'])))
    # --- ablaciones y secundarias (NO deciden; sec. 6)
    forma = lambda k: bool(pz[k]['gana'] >= g and pz[k]['dif'] >= MARGEN)
    sec = dict(veto_aporta_tpv_sobre_pc=forma('tpv_vs_pc'), patas_aportan_tpv_sobre_tv=forma('tpv_vs_tv'),
               veto_solo_tv_sobre_termo=forma('tv_vs_termo'), patas_solas_pc_sobre_termo=forma('pc_vs_termo'),
               vinv_se_hunde_bajo_termo=pz['vinv_vs_termo']['dif'] <= -MARGEN, vinv_supera_termo=pz['vinv_vs_termo']['dif'] >= MARGEN,
               tv_letra_muro=res['tv']['sem_cruza_e5'] >= my, pc_letra_muro=res['pc']['sem_cruza_e5'] >= my, termo_letra_muro=res['termo']['sem_cruza_e5'] >= my)
    M = {b: mundo(R[b], sem) for b in ORDEN}
    HJ = {b: hijos(dict(linajes=[l for s in sem for l in R[b][s]['linajes']])) for b in ORDEN}
    come = {}
    for a, b in (('tpv', 'termo'), ('tpv', 'pc'), ('tpv', 'vinv'), ('tv', 'termo'), ('pc', 'termo'), ('o1', 'termo')):
        come[f"{a}_vs_{b}"] = dict(hijos_menos_h200=mundo_par(M[a], M[b], sem, 'h200', mayor=False),
                                   hijo_vive_mas=mundo_par(M[a], M[b], sem, 'vida_hijo'),
                                   mas_hijos_mueren_de_hambre_600=mundo_par(M[a], M[b], sem, 'h600'),
                                   come_mas_AC=mundo_par(M[a], M[b], sem, 'AC'), muerde_mas_BD=mundo_par(M[a], M[b], sem, 'BD'),
                                   decide_mejor_frac_buena=mundo_par(M[a], M[b], sem, 'frac_buena'),
                                   mundo_mas_pelado_AC=mundo_par(M[a], M[b], sem, 'mundo_AC', mayor=False),
                                   menos_fundadores=mundo_par(M[a], M[b], sem, 'fund', mayor=False),
                                   mas_establecidos=mundo_par(M[a], M[b], sem, 'estab'))
    mAC = {b: med([M[b][s]['mundo_AC'] for s in sem]) for b in ORDEN}
    tapado = bool(come['tpv_vs_pc']['mundo_mas_pelado_AC']['a_gana'] >= g and pz['tpv_vs_pc']['dif'] < 0)
    desc = dict(h200_tpv_bajo_5pct=(HJ['tpv']['h200'] is not None and HJ['tpv']['h200'] < H200), mundo_tapado_tpv=tapado,
                h200={b: HJ[b]['h200'] for b in ORDEN}, mundo_AC_med=mAC)
    # --- impresion
    log(f"\n================ LECTURA ({PRERREGISTRO} sec. 5-6) · {carpeta}")
    log(f"{'brazo':6s} {'cruzan/' + str(9 * n):>10s} {'mayoria':>8s} {'R0 med':>7s} {'fund med':>8s} {'A+C/lin':>8s} {'B+D/lin':>8s} {'mundo A+C':>9s} "
        f"{'hijos':>6s} {'h<=200':>7s} {'h600 ham':>8s} {'vida h':>7s} {'ven+sal':>7s} {'paren':>6s}")
    for b in ORDEN:
        r = res[b]; h = HJ[b]
        log(f"{b:6s} {r['linajes_cruzan_real']:>10d} {str(r['sem_cruza_e5']) + '/' + str(n):>8s} {r['R0_real_med']!s:>7s} {r['fundadores_med']!s:>8s} "
            f"{r['mord_AC_med']!s:>8s} {r['mord_BD_med']!s:>8s} {mAC[b]!s:>9s} {h['n']:>6d} {h['h200']!s:>7s} {h['h600_hambre']!s:>8s} {h['vida_med']!s:>7s} "
            f"{h['veneno_sal']!s:>7s} {h['paren']!s:>6s}")
    log("PAREADO en linajes que cruzan (gana/empata/pierde por semilla; suma de 9n; dif = suma a - suma b) y R0 real (mediana por semilla)")
    for k, z in pz.items():
        log(f"  {k:14s} gana {z['gana']:2d} empata {z['empata']:2d} pierde {z['pierde']:2d} · suma {z['suma_a']} vs {z['suma_b']} (dif {z['dif']:+d}) · "
            f"R0 gana {pr[k]['gana']}/{pr[k]['semillas']} dif med {pr[k]['dif_med']}")
    log(f"  por semilla tpv {pz['tpv_vs_termo']['por_semilla_a']}\n  por semilla termo {pz['tpv_vs_termo']['por_semilla_b']}\n"
        f"  por semilla vinv {pz['tpv_vs_vinv']['por_semilla_b']}\n  por semilla pc {pz['tpv_vs_pc']['por_semilla_b']}\n  por semilla tv {pz['tpv_vs_tv']['por_semilla_b']}")
    log("HIJOS Y MUNDO (descriptivo; a_gana = semillas en que el primero 'gana' en la medida; umbral de lectura " + str(g) + ")")
    for k, c in come.items():
        log(f"  {k}: " + ' · '.join(f"{kk} {z['a_gana']}/{z['n']} ({z['med_a']} vs {z['med_b']})" for kk, z in c.items()))
    log(f"  piezas actuan (por semilla): vetos { {b: act_v[b][:4] for b in VETO_BRAZOS} } ... · cambios de paso { {b: act_p[b][:4] for b in PATAS_BRAZOS} } ...")
    voc = []
    voc.append('"el veto aporta sobre TERMO+PATAS"' if sec['veto_aporta_tpv_sobre_pc'] else '"sin separar el veto de las patas" (tpv no supera a pc con la forma PA+PB)')
    voc.append('"las patas aportan sobre TERMO+VETO"' if sec['patas_aportan_tpv_sobre_tv'] else '"sin separar las patas del veto" (tpv no supera a tv con la forma PA+PB)')
    if tapado: voc.append('"mundo tapado" (tpv pela el mundo mas que pc en >= 13/20 y cruza menos que pc)')
    log(f"\n  VALIDEZ {v} (termo suma {st_}, banda {bt})\n  PUERTAS {p}\n  ABLACIONES Y SECUNDARIAS (no deciden) {sec}\n  DESCRIPTIVOS {desc}")
    log(f"  VOCABULARIO (sec. 11; aplica solo con FUNCIONA o MODESTO): {' · '.join(voc)}" + (f" · veredicto con nota: {ver_nota}" if ver_nota != ver else '')
        + (f"\n  EN EL UMBRAL (sec. 10): {[k for k, z in umbral.items() if z]} (PA/PD: gana = 13 exacto o dif entre +15 y +17; PC: 15 exacto); "
           "no sostiene estrella sin la replica" if en_umbral else ''))
    return dict(validez=v, puertas=p, secundarias=sec, descriptivos=desc, veredicto=ver, veredicto_nota=ver_nota, en_umbral=en_umbral, umbral=umbral,
                vocabulario=voc,
                brazos=res, hijos=HJ, pareado_cruzan=pz, pareado_R0=pr, mundo_par=come, actua=dict(vetos=act_v, patas=act_p), abortos=ab, n=n, humo=humo)


ORDV = {'NO SE LEE': -1, 'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}


def bloque(a, b):
    return a if a == b else min((a, b), key=lambda z: ORDV[z])


# ------------------------------------------------------------------ verificaciones antes de correr
def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    if AQUI not in sys.path: sys.path.insert(0, AQUI)
    import construye_veto_muro as CVM     # se usa SOLO todas() (no escribe nada)
    b = CVM.todas()['TVPISO']; igual = open(TVPISO_PY, 'rb').read() == b
    ok &= igual; log(f"  carro TVPISO en disco == construye_veto_muro.todas() por anclas desde TPATAS (sin escribir): {'OK' if igual else 'FALLA'}")
    N = lambda z: json.loads(json.dumps(z, default=str))
    run = lambda m: N(P.run(ARNES[0], [('C', m)] * 9, T=2000, fundador_limpio=1))
    base_t = run(CV._MODS[fija('termo')['carro']]); base_p = run(CV._MODS[fija('pc')['carro']])
    for br in VETO_BRAZOS:
        m = CV._MODS[fija(br)['carro']]
        try:
            m.VETOP = 0; pv = m.PATAS; xx = run(m); i1 = xx == (base_p if pv == 3 else base_t)
            m.PATAS = 0; i2 = run(m) == base_t
        finally:
            fija(br)
        ok &= i1 and i2
        log(f"  IDENTIDAD CORTA: {br} con VETOP = 0 == {'TPATAS 3' if pv == 3 else 'V143_TERMO'} y con VETOP = PATAS = 0 == V143_TERMO "
            f"(salida ENTERA, N 9, s {ARNES[0]}, T 2000, fundador limpio): {'OK' if (i1 and i2) else 'FALLA'}")
    return ok


def git_limpio(rutas, log):
    """--serie/--replica: el preregistro, el runner, el constructor y el carro deben estar COMMITEADOS y sin cambios respecto de HEAD."""
    ok = True
    for r in rutas:
        rel = os.path.relpath(r, RAIZ).replace('\\', '/')
        try:
            t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
            c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
            h = subprocess.run(['git', '-C', RAIZ, 'log', '-1', '--format=%h %cI', '--', rel], capture_output=True, text=True).stdout.strip()
        except Exception as e:   # noqa
            t = c = False; h = str(e)
        ok &= t and c; log(f"  git {rel}: commiteado {t} · sin cambios vs HEAD {c} · ultimo commit {h}")
    return ok


def guarda(pre, reanuda):
    """Candados. Si ya hay un resumen.json (no humo) de esta serie/replica con veredicto FUNCIONA, MODESTO o NO: se niega siempre.
    Si hay carpetas previas (cortadas o NO SE LEE): solo --reanuda. Devuelve None si se puede correr, o el motivo."""
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if not r.get('humo') and (r.get('letra') or {}).get('veredicto') in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda (cortada o NO SE LEE)"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true')
    g.add_argument('--bloque', default=None); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX} (contrato del encargo)")
    if a.bloque:
        rs = [json.load(open(x.strip(), encoding='utf-8')) for x in a.bloque.split(',')]
        if len(rs) != 2: raise SystemExit("--bloque: <resumen serie>,<resumen replica>")
        if not (rs[0]['semillas'][0] in SERIE and rs[1]['semillas'][0] in REPLICA) or rs[0]['humo'] or rs[1]['humo']:
            raise SystemExit("--bloque: primero la serie 53701-53720 y luego la replica 53721-53740 (no humo)")
        yo = h16(os.path.abspath(__file__))
        if any(r.get('sha_runner') != yo for r in rs):
            raise SystemExit(f"--bloque: sha_runner de los resumenes {[r.get('sha_runner') for r in rs]} != runner actual {yo}")
        va, vb = rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto']
        print(f"serie {va} · replica {vb} -> BLOQUE: {bloque(va, vb)}  ({PRERREGISTRO} sec. 7)")
        return 0
    if a.lee:
        c = os.path.abspath(a.lee); sems = sorted({json.load(open(f, encoding='utf-8'))['seed'] for f in glob.glob(os.path.join(c, '*_s*.json'))})
        humo = not (sems == list(SERIE) or sems == list(REPLICA))
        L = lee(c, sems, humo=humo); print(f"VEREDICTO ({'HUMO, no cuenta' if humo else 'letra'}): {L['veredicto']}"); return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        tareas = list(HUMO) if a.reanuda else list(HUMO)[:6]   # maximo 6 corridas por proceso; la 7a (v143) con --reanuda
        T = T_HUMO; semillas = [HUMO_S[0]]; pre = f"humo_s{HUMO_S[0]}_T{T}"; dest = os.path.join(DATOS, 'humo')
    else:
        semillas = list(SERIE if a.serie else REPLICA); T = T_DEF
        tareas = [(s, b) for s in semillas for b in ORDEN]
        pre = f"{'serie' if a.serie else 'replica'}_s{semillas[0]}-{semillas[-1]}_T{T}"; dest = DATOS
    sel = time.strftime('%Y%m%d_%H%M%S')
    prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
    carpeta = os.path.join(dest, prev[-1]) if (a.reanuda and prev) else os.path.join(dest, pre + '_' + sel)
    if a.reanuda and not prev: raise SystemExit(f"--reanuda: no hay carpeta {pre}_* en {dest}")
    BUF = []; LOGF = None   # la carpeta se crea SOLO si todas las verificaciones pasan (no deja carpetas vacias)

    def log(s=''):
        print(s, flush=True)
        if LOGF is None: BUF.append(s)
        else: LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    log(f"CORRE_VETO_MURO · {pre} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · "
        f"corre_veto_muro.py {h16(os.path.abspath(__file__))} · preregistro {PRERREGISTRO} "
        f"{h16(os.path.join(AQUI, PRERREGISTRO)) if os.path.exists(os.path.join(AQUI, PRERREGISTRO)) else 'NO EXISTE'} · carpeta {carpeta}")
    log(f"  tareas {len(tareas)} · brazos {list(ORDEN)} · semillas {semillas[0]}-{semillas[-1]} · T {T} · fundador limpio 1 · reanuda {a.reanuda}")
    if not a.humo:
        e = guarda(pre, a.reanuda)
        if e: log(f"  NO SE CORRE (candado): {e}"); return 1
    if a.replica:
        rsm = sorted(glob.glob(os.path.join(DATOS, f"serie_s{SERIE[0]}-{SERIE[-1]}_T{T_DEF}_*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto')
        if vs not in ('FUNCIONA', 'HAY ALGO MODESTO'):
            log(f"  REGLA DE PARADA (sec. 7): la replica solo se corre si la serie da FUNCIONA o MODESTO; serie = {vs}. No se corre."); return 1
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)):
            log(f"  NO SE CORRE (candado): sha_runner de la serie {rs0.get('sha_runner')} != runner actual {h16(os.path.abspath(__file__))}"); return 1
    ok = verifica(log)
    if not a.humo:
        ok &= git_limpio([os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), os.path.join(AQUI, 'construye_veto_muro.py'), TVPISO_PY], log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF.write('\n'.join(BUF) + '\n'); LOGF.flush()
    args = [(s, b, T, carpeta, a.reanuda) for s, b in tareas]
    fmt = lambda x: (f"  [{time.time()-t0:7.1f}s] {x['brazo']:5s} s{x['seed']} ({x.get('seg')}s) cruzan {cz(x) if not x['aborto'] else '-'}/9 "
                     f"R0 real {[l['R0_real'] for l in x['linajes']]} aborto {x['aborto']}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, args): log(fmt(x))
    else:
        for ar in args: log(fmt(trabajo(ar)))
    letra = lee(carpeta, semillas, humo=a.humo, log=log)
    ver = ('HUMO (no cuenta): ' if a.humo else '') + letra['veredicto']
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(letra=letra, semillas=semillas, T=T, humo=a.humo, veredicto=ver, preregistro=PRERREGISTRO,
                       sha_preregistro=(h16(os.path.join(AQUI, PRERREGISTRO)) if os.path.exists(os.path.join(AQUI, PRERREGISTRO)) else None),
                       sha_runner=h16(os.path.abspath(__file__)), shas={os.path.relpath(k, RAIZ): v for k, v in SHAS.items()}),
                  fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)})\nTerminado en {time.time()-t0:.1f}s")
    log(f"VEREDICTO DE LA {'CORRIDA' if a.humo else ('SERIE' if a.serie else 'REPLICA')}: {ver}   (regla de parada: {PRERREGISTRO} sec. 7)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
