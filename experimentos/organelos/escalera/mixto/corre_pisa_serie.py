"""corre_pisa_serie.py — RUNNER DE PROTOCOLO del peldano PISA: "la senal leida puede pisar memoria de lugar caducada", en el mundo con
oasis que se muda (mundo_tramo_c: oasis + mueve 20000 + c_e 0.01). 1-oct-2026. Preregistro: PREREGISTRO_pisa.md. Es DISENO, no seleccion.
NO reemplaza al carro de P7 (O1_LUGAR_SENAL queda como esta).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE SE CORRE: cada corrida ES corre_juntos.tarea (IMPORTADO por sha; a su vez corre_v143.tarea, regla 14) con UNA diferencia: la lista de
carros que recibe mundo_tramo_c.run es mixta (1 explorador + 8 lectores). Sondas de SOLO LECTURA sobre los carros PISA (ganchos en memoria:
que bin se piso y cuando; adopciones de _lg_hereda) — el arnes comprueba que la corrida con ganchos == la corrida sin ganchos.
  BRAZOS (9 linajes, L 360, fundador limpio; el EXPLORADOR va en el indice e = i mod 9, i = indice de la semilla: ROTADO, igual en los 4 brazos):
    pmix     explorador O1_TODO (memoria + senal + pregunta, ORIGINAL) · 8 lectores O1_SEN_PISA                    EL CANDIDATO
    mix      explorador O1_TODO · 8 lectores O1_TODO_SEN (ORIGINALES)                                              AISLA LA VARIANTE
    pmixbar  explorador O1_TODO · 8 lectores O1_SEN_PISA_BAR (leen la senal al ANTIPODA, tambien pisan)            CONTROL DE CONTENIDO
    pmudo    explorador O1_TODO_PREG (explora; ni emite ni lee) · 8 lectores O1_SEN_PISA                           CONTROL: EXPLORADOR MUDO
    sen9     9 x O1_TODO_SEN        (descriptivo, solo serie, primeras N_DESC semillas)
    pisa9    9 x O1_SEN_PISA        (descriptivo, idem: la variante SIN explorador)
MEDIDA PRINCIPAL: por semilla, la mediana de la latencia de los 8 LECTORES (pasos desde cada mudanza hasta su primer bocado A+C dentro del
oasis nuevo; nunca -> T). LETRA (por codigo, lee_serie; PREREGISTRO sec. 6): FUNCIONA / HAY ALGO MODESTO / NO / NO SE LEE.
SEMILLAS NUEVAS 7386xx (grep 1-oct): serie 738641-738660 · replica 738671-738690 · humo de main 738695-738698 · arnes 738632.
  python experimentos/organelos/escalera/mixto/corre_pisa_serie.py --identidad
  python experimentos/organelos/escalera/mixto/corre_pisa_serie.py --humo [--T 20000] [--mueve 5000] [--n 1] [--brazos pmix,mix,pmixbar,pmudo]
  python experimentos/organelos/escalera/mixto/corre_pisa_serie.py --serie --pool 2 [--reanuda]      (solo el coordinador)
  python experimentos/organelos/escalera/mixto/corre_pisa_serie.py --replica --pool 2 [--reanuda]
  python experimentos/organelos/escalera/mixto/corre_pisa_serie.py --lee <carpeta>
"""
import argparse, collections, glob, json, math, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(ESC)))
sys.path.insert(0, AQUI)
import corre_pisa as PZ          # cargador de los carros PISA (verificados contra construye_pisa); importa corre_mixto y corre_juntos
CM = PZ.CM; RJ = PZ.RJ; CP = PZ.CP; CV = RJ.CV; MC = RJ.MC; h16 = RJ.h16

SHAS = {os.path.join(AQUI, 'corre_pisa.py'): '445c27054bfdc82a', os.path.join(AQUI, 'corre_mixto.py'): 'f27edde098cf7a1a',
        os.path.join(AQUI, 'construye_pisa.py'): '85de025f95740bb0', os.path.join(AQUI, 'carros', 'O1_SEN_PISA.py'): 'bca8f97bcb6cb353',
        os.path.join(AQUI, 'carros', 'O1_SEN_PISA_BAR.py'): '95cda0103eb80b40', os.path.join(AQUI, 'carros', 'O1_SEN_PISA0.py'): '362a150ded4ff12d'}
# brazo -> (explorador o None, lector)
BRAZOS = {'pmix': ('O1_TODO', 'O1_SEN_PISA'), 'mix': ('O1_TODO', 'O1_TODO_SEN'), 'pmixbar': ('O1_TODO', 'O1_SEN_PISA_BAR'),
          'pmudo': ('O1_TODO_PREG', 'O1_SEN_PISA'), 'sen9': (None, 'O1_TODO_SEN'), 'pisa9': (None, 'O1_SEN_PISA'), 'pisa0': (None, 'O1_SEN_PISA0')}
LETRA = ('pmix', 'mix', 'pmixbar', 'pmudo'); DESC = ('sen9', 'pisa9'); ORDEN = LETRA + DESC
CAND = 'pmix'; VAR = 'mix'; CONT = 'pmixbar'; MUDO = 'pmudo'
PISAN = ('pmix', 'pmixbar', 'pmudo', 'pisa9')
N = 9; NB = 30; W_OASIS = 36
MUEVE = RJ.MUEVE; C_E = RJ.C_E; MUNDO = dict(RJ.MUNDO_J)
SEM = dict(serie=738641, replica=738671, humo=738695, arnes=738632)
N_SERIE = 20; N_DESC = 10; T_SERIE = 100000; POOL_MAX = 2
HUMO = dict(n=1, T=20000, mueve=5000)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000
GANA_PAR = 14; RAZON_MAX = 0.85; FRAC_EXPL = 0.9
DATOS = os.path.join(AQUI, 'datos')


def med(xs, nd=4):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), nd) if xs else None


def esc(k, n): return math.ceil(k * n / 20 - 1e-9)


def carros_de(brazo, i):
    """-> (lista de 9 nombres, indice del explorador o None). El explorador ROTA con el indice de la semilla (e = i mod 9)."""
    ex, le = BRAZOS[brazo]
    if ex is None: return [le] * N, None
    e = i % N; L = [le] * N; L[e] = ex
    return L, e


def ruta(n):
    if n in PZ.PROPIOS: return PZ.PROPIOS[n]
    if n in RJ.CARROS: return RJ.CARROS[n]
    raise SystemExit(f"carro desconocido {n}")


def tarea(seed, nombres, T, mundo, sondas=True, cap_kw=None):
    """corre_juntos.tarea con la lista de carros sustituida por `nombres` (cada carro cargado y verificado por el cargador de su duenno).
    sondas: ganchos de SOLO LECTURA sobre los modulos PISA (no escriben estado del carro; arnes: con == sin)."""
    mods = {n: PZ.carga(n) for n in dict.fromkeys(nombres)}
    carros = [(n, mods[n]) for n in nombres]
    ev = collections.Counter(); her = dict(adopta=0, tras_vivir=0); orig_m = {}
    mv = int(mundo.get('mueve') or 0)
    if sondas:
        for n, m in mods.items():
            if not getattr(m, 'SN_PISA', 0): continue
            o_lee = m.Carro._sn_lee; o_her = m.Carro._lg_hereda; orig_m[n] = (m, o_lee, o_her)

            def g_lee(self, obs, _o=o_lee, _m=m):
                visto = set()
                for e in (obs.get('pizarra') or ()):
                    t, quien, c = e[0], e[1], e[2]
                    if t <= self._sn_ult or quien == self.yo or len(c) < 3: continue
                    b = int(c[0])
                    if not 0 <= b < _m.LG_NB: continue
                    if _m.SN_BARAJA: b = (b + _m.LG_NB // 2) % _m.LG_NB
                    if b not in visto and self.nl[b] > 0 and self.lugar[b].sum() <= _m.LG_MIN:
                        visto.add(b); ev[((int(obs['t']) // mv) if mv else 0, b)] += 1
                return _o(self, obs)

            def g_her(self, mm, _o=o_her):
                if self.nl.sum() == 0:
                    her['adopta'] += 1
                    if self.st.get('lg_apr', 0) > 0: her['tras_vivir'] += 1   # ya habia vivido y aprendido: en el ORIGINAL nl.sum() no vuelve a 0
                return _o(self, mm)
            m.Carro._sn_lee = g_lee; m.Carro._lg_hereda = g_her
    orig = MC.run

    def run_mixto(s, _carros, **k):
        if cap_kw is not None: cap_kw.append(dict(k))
        return orig(s, carros, **k)
    MC.run = run_mixto
    try:
        x = RJ.tarea(seed, nombres[0] if nombres[0] in RJ.CARROS else 'O1_TODO_SEN', T, mundo)
    finally:
        MC.run = orig
        for n, (m, o_lee, o_her) in orig_m.items(): m.Carro._sn_lee = o_lee; m.Carro._lg_hereda = o_her
    x['estado'] = dict(carros=list(nombres), shas={n: h16(ruta(n)) for n in mods}, mundo=dict(mundo),
                       perillas={n: [getattr(m, 'SENAL', 0), getattr(m, 'SN_BARAJA', 0), getattr(m, 'PREGUNTA', 0), getattr(m, 'SN_PISA', 0)] for n, m in mods.items()})
    x['sonda'] = dict(activa=bool(sondas), pisa=sorted([p, b, c] for (p, b), c in ev.items()), hereda=her) if sondas else None
    return x


def fila(x, T, nombres, e):
    """corre_juntos.fila (fisica del juez + oasis + pizarra + senal) + la medida de los LECTORES + las sondas clasificadas."""
    f = RJ.fila(x, T)
    L = x['linajes']; tel = x.get('tel') or []; oi = x.get('oasis_info') or {}
    cr = [((l.get('_oasis') or {}).get('latencias') or [])[1:] for l in L]
    lat = [[(T if v is None else v) for v in c] for c in cr]; nun = [sum(v is None for v in c) for c in cr]
    lec = [i for i in range(len(L)) if i != e]; nm = len(lat[0])
    mud = oi.get('mudanzas') or []; Lr = 40 * len(L)
    bins = [{(((z + j) % Lr) * NB) // Lr for j in range(W_OASIS)} for _, z in mud]
    sd = x.get('sonda') or {}; pz = dict(total=0, per0=0, nuevo=0, viejo=0, otro=0)
    for p, b, c in (sd.get('pisa') or []):
        pz['total'] += c
        if p == 0 or p >= len(bins): pz['per0'] += c
        elif b in bins[p]: pz['nuevo'] += c
        elif b in bins[p - 1]: pz['viejo'] += c
        else: pz['otro'] += c
    tm = pz['total'] - pz['per0']
    pz['frac_viejo'] = round(pz['viejo'] / tm, 4) if tm else None; pz['frac_nuevo'] = round(pz['nuevo'] / tm, 4) if tm else None
    sn = [(t.get('sn') or None) for t in tel]
    f['lectores'] = dict(carros=list(nombres), explorador=e, lat_por_linaje=lat, nunca_por_linaje=nun,
                         lat_med=med([v for i in lec for v in lat[i]], 1), lat_n=sum(len(lat[i]) for i in lec), nunca=sum(nun[i] for i in lec),
                         lat_por_mudanza=[med([lat[i][j] for i in lec], 1) for j in range(nm)],
                         lat_explorador=(lat[e] if e is not None else None), lat_explorador_med=(med(lat[e], 1) if e is not None else None),
                         cruza=sum(f['cruza'][i] for i in lec), fund=[f['fund'][i] for i in lec], fund_media=round(float(st.mean(f['fund'][i] for i in lec)), 4),
                         sn_lee=sum((sn[i] or {}).get('sn_lee', 0) for i in lec), sn_siembra=sum((sn[i] or {}).get('sn_siembra', 0) for i in lec),
                         sn_pisa_tel=[((s or {}).get('sn_pisa')) for s in sn], pg_exc=[((t.get('carro') or {}).get('pg_exc')) for t in tel],
                         escrituras=f['pizarra']['escrituras'])
    f['sonda'] = dict(activa=bool(sd.get('activa')), pisa=pz, hereda=sd.get('hereda'))
    f['estado'] = x['estado']
    return f


def trabajo(args):
    """UN trabajo: (i, brazo). Atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54); con reanuda salta el que ya existe y no aborto."""
    i, brazo, base, T, carpeta, reanuda, mundo = args
    fin = os.path.join(carpeta, f"prueba_i{i:02d}_{brazo}.json"); previo = None
    if reanuda and os.path.exists(fin):
        try:
            with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
            if not x0.get('aborto'): return x0
            previo = x0['aborto']
        except Exception as e_:   # JSON truncado por un corte: se re-corre
            previo = f"json ilegible: {e_}"[:120]
    t0 = time.time()
    try:
        nombres, e = carros_de(brazo, i)
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=None, **fila(tarea(base + i, nombres, T, mundo), T, nombres, e))
    except BaseException as ex:   # noqa: nube-9
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=f"{type(ex).__name__}: {ex}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_pisa.md sec. 6)
def _par(R, a, b, I):
    """pareado por semilla, MENOR gana (latencia); el empate cuenta EN CONTRA del candidato."""
    xa = [R[a][i]['lectores']['lat_med'] for i in I]; xb = [R[b][i]['lectores']['lat_med'] for i in I]
    rz = [round(p / q, 4) for p, q in zip(xa, xb) if q]
    return dict(n=len(I), gana=sum(p < q for p, q in zip(xa, xb)), empata=sum(p == q for p, q in zip(xa, xb)), pierde=sum(p > q for p, q in zip(xa, xb)),
                med_a=med(xa, 1), med_b=med(xb, 1), razon_med=med(rz), por_indice_a=xa, por_indice_b=xb)


def lee_serie(R, n, abortos, mueve=MUEVE, T=T_SERIE, c_e=C_E):
    I = list(range(n)); gp = esc(GANA_PAR, n); brazos = [b for b in ORDEN if R.get(b)]
    completo = all(len(R.get(b, {})) == n and set(R[b]) == set(I) for b in LETRA)
    n_mud = T // mueve - (1 if T % mueve == 0 else 0)
    X = lambda bs=None: ((b, i, R[b][i]) for b in (bs or brazos) for i in sorted(R.get(b, {})))
    lc = lambda d: d['lectores']
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(d['coherente'] for _, _, d in X()))
    v['V2_mundo'] = bool(all((d.get('preg') or {}).get('mudanzas') == n_mud and (d.get('oasis_info') or {}).get('mueve') == mueve
                             and (d.get('oasis_info') or {}).get('c_e') == c_e and len(lc(d)['lat_por_mudanza']) == n_mud for _, _, d in X()))
    v['V3_estado'] = bool(all(d['estado']['carros'] == carros_de(b, i)[0] and lc(d)['explorador'] == carros_de(b, i)[1]
                              and all(d['estado']['shas'][k] == h16(ruta(k)) for k in d['estado']['shas']) and d['sonda']['activa'] for b, i, d in X()))
    ex_b = [b for b in LETRA if R.get(b)]
    antes = {b: sum(lc(d)['lat_explorador_med'] < lc(d)['lat_med'] for _, _, d in X([b])) for b in ex_b}
    v['V4_explorador_antes'] = bool(completo and all(antes[b] >= math.ceil(FRAC_EXPL * n - 1e-9) for b in ex_b))
    v['V5_pisadas'] = bool(all((d['sonda']['pisa']['total'] > 0 and sum(z or 0 for z in lc(d)['sn_pisa_tel']) <= d['sonda']['pisa']['total']) if b in PISAN
                               else (d['sonda']['pisa']['total'] == 0 and all(z is None for z in lc(d)['sn_pisa_tel'])) for b, _, d in X()))
    v['V6_senal_viva'] = bool(all(lc(d)['sn_lee'] > 0 and lc(d)['sn_siembra'] > 0 and d['pizarra']['escrituras_total'] > 0 for _, _, d in X()))

    def explora_ok(b, d):
        e = lc(d)['explorador']; pg = lc(d)['pg_exc']
        if e is None: return all(not z for z in pg)
        return (pg[e] or 0) > 0 and all(not pg[j] for j in range(len(pg)) if j != e)
    v['V7_solo_uno_pregunta'] = bool(all(explora_ok(b, d) for b, _, d in X()))
    valido = all(v.values())
    q = {}; p = {}; coord = None
    if completo:
        q = {k: _par(R, CAND, k, I) for k in (VAR, CONT, MUDO)}
        p['G_var_pares'] = q[VAR]['gana'] >= gp
        p['G_var_magnitud'] = q[VAR]['razon_med'] is not None and q[VAR]['razon_med'] <= RAZON_MAX
        p['G_contenido'] = q[CONT]['gana'] >= gp
        p['G_mudo'] = q[MUDO]['gana'] >= gp
        coord = ('FUNCIONA' if all(p.values()) else 'MODESTO' if (p['G_contenido'] and (p['G_var_pares'] or p['G_mudo'])) else 'NO')
    if not valido or not completo: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif p['G_contenido'] and p['G_var_pares']: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    umbral = bool(completo and any(abs(q[k]['gana'] - gp) <= 1 for k in q))
    desc = {}
    if brazos:
        D = lambda f, bs=None: {b: f(b) for b in (bs or brazos)}
        Id = lambda b: sorted(R[b])
        desc['n_por_brazo'] = D(lambda b: len(R[b]))
        desc['lat_lectores_med'] = D(lambda b: med([lc(R[b][i])['lat_med'] for i in Id(b)], 1))
        desc['lat_explorador_med'] = D(lambda b: med([lc(R[b][i])['lat_explorador_med'] for i in Id(b)], 1))
        desc['explorador_antes_que_lectores'] = antes
        desc['nunca_llegan_lectores'] = D(lambda b: sum(lc(R[b][i])['nunca'] for i in Id(b)))
        # TRAMPAS que se reportan SIEMPRE junto al veredicto (no entran en la letra)
        desc['TRAMPA_mundo_AC'] = D(lambda b: med([R[b][i]['mundo_AC'] for i in Id(b)]))
        desc['TRAMPA_cruce_lectores'] = D(lambda b: [sum(lc(R[b][i])['cruza'] for i in Id(b)), sum(len(lc(R[b][i])['fund']) for i in Id(b))])
        desc['TRAMPA_fund_lectores_media'] = D(lambda b: med([lc(R[b][i])['fund_media'] for i in Id(b)]))
        desc['TRAMPA_rumor_frac_pisadas_al_oasis_VIEJO'] = D(lambda b: med([R[b][i]['sonda']['pisa']['frac_viejo'] for i in Id(b)]), [b for b in brazos if b in PISAN])
        desc['pisadas_frac_al_oasis_NUEVO'] = D(lambda b: med([R[b][i]['sonda']['pisa']['frac_nuevo'] for i in Id(b)]), [b for b in brazos if b in PISAN])
        desc['pisadas_total'] = D(lambda b: sum(R[b][i]['sonda']['pisa']['total'] for i in Id(b)), [b for b in brazos if b in PISAN])
        desc['TRAMPA_lg_hereda_tras_vivir'] = D(lambda b: sum((R[b][i]['sonda']['hereda'] or {}).get('tras_vivir', 0) for i in Id(b)), [b for b in brazos if b in PISAN])
        desc['lg_hereda_adopta'] = D(lambda b: sum((R[b][i]['sonda']['hereda'] or {}).get('adopta', 0) for i in Id(b)), [b for b in brazos if b in PISAN])
        desc['siembras_lectores'] = D(lambda b: med([lc(R[b][i])['sn_siembra'] for i in Id(b)]))
        desc['lecturas_lectores'] = D(lambda b: med([lc(R[b][i])['sn_lee'] for i in Id(b)]))
        desc['cruzan_total'] = D(lambda b: sum(R[b][i]['cruzan'] for i in Id(b)))
        desc['R0_med'] = D(lambda b: med([R[b][i]['R0_med'] for i in Id(b)]))
        desc['ratio_pasos_oasis'] = D(lambda b: med([R[b][i]['oasis']['ratio_pasos'] for i in Id(b)]))
        desc['letra_propuesta_por_el_coordinador (no decide)'] = coord
    return dict(validez=v, puertas=p, veredicto=ver, en_umbral=umbral, umbrales=dict(gana_par=gp, razon_max=RAZON_MAX, frac_explorador=FRAC_EXPL),
                pareados=q, descriptivo=desc)


def lee(carpeta):
    R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        try: d = json.load(open(f, encoding='utf-8'))
        except Exception as e: ab.append(f"{os.path.basename(f)}: json ilegible {e}"[:160]); continue
        if d.get('aborto'): ab.append(f"i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        R.setdefault(d['brazo'], {})[d['i']] = d
    return R, ab


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  puertas: {L['puertas']} · umbrales {L['umbrales']} · EN EL UMBRAL (+-1 par): {L['en_umbral']}")
    for k, q in L['pareados'].items():
        log(f"  pmix < {k}: gana {q['gana']} empata {q['empata']} pierde {q['pierde']} de {q['n']} · mediana {q['med_a']} vs {q['med_b']} · razon mediana {q['razon_med']} · por indice {q['por_indice_a']} vs {q['por_indice_b']}")
    for k, v in L['descriptivo'].items(): log(f"  [{'TRAMPA' if k.startswith('TRAMPA') else 'desc'}] {k}: {v}")


def verifica(log):
    ok = CM.verifica(log)
    for r, s in SHAS.items():
        h = h16(r); ok &= h == s; log(f"  sha {os.path.relpath(r, ESC)} {h} {'OK' if h == s else '!= ' + s + ' FALLA'}")
    for n, b in CP.todas().items():
        i = os.path.exists(PZ.PROPIOS[n]) and open(PZ.PROPIOS[n], 'rb').read() == b; ok &= i; log(f"  carro {n} == construye_pisa: {i}")
    log(f"  mundo_tramo_c: {MC.construye()[1]}")
    return ok


def identidad(log, seed=SEM['arnes'], T=3000, corta=False):
    """ARNES. Salida ENTERA (json canonico) salvo 'seg' (reloj), 'estado' y 'sonda' (metadatos de este runner).
      A1 variante APAGADA: [O1_SEN_PISA0]*9 == corre_juntos.tarea('O1_TODO_SEN'), con mudanza y sin mudanza
      A2 pista mixta con 9 iguales == corre_juntos.tarea homogenea (O1_TODO_SEN, O1_TODO, O1_TODO_PREG)
      A3 las SONDAS no perturban: pmix / pmixbar / pmudo con ganchos == sin ganchos
      A4 regla 14, entrada campo a campo: los kwargs que recibe mundo_tramo_c.run son los de corre_juntos.tarea (== corre_v143.tarea + mundo)
      A5 el arnes PUEDE fallar: pmix != mix · pmixbar != pmix · pmudo != pmix · rotar el explorador cambia la corrida
      A6 la sonda de pisadas cuenta >= la telemetria del carro (sn_pisa) y > 0 en pmix; 0 en mix
      A7 semillas: serie, replica, humo y arnes disjuntas, dentro de 7386xx, fuera de las del humo de rafaga (738611-12, 738621-23, 738630-31)"""
    def Nz(x, quita=('seg', 'estado', 'sonda')):
        return json.loads(json.dumps({k: v for k, v in x.items() if k not in quita}, default=str, sort_keys=True))
    ok = True; mv = T // 3; mundo = dict(MUNDO, mueve=mv)
    for m_ in ((mv, 0) if not corta else (mv,)):
        mu = dict(MUNDO, mueve=m_)
        a = json.loads(json.dumps(Nz(tarea(seed, ['O1_SEN_PISA0'] * 9, T, mu))).replace('O1_SEN_PISA0', 'O1_TODO_SEN')); c = Nz(RJ.tarea(seed, 'O1_TODO_SEN', T, mu))
        i = a == c; ok &= i; log(f"  A1 [O1_SEN_PISA0]*9 == corre_juntos.tarea(O1_TODO_SEN) · s {seed} T {T} mueve {m_}: {i} ({len(json.dumps(c))} bytes)")
    kws = {}
    for n in (('O1_TODO_SEN', 'O1_TODO', 'O1_TODO_PREG') if not corta else ('O1_TODO',)):
        kw = []; a = Nz(tarea(seed, [n] * 9, T, mundo, cap_kw=kw)); kw0 = []; o = MC.run

        def espia(s, c_, **k):
            kw0.append(dict(k)); return o(s, c_, **k)
        MC.run = espia
        try: c = Nz(RJ.tarea(seed, n, T, mundo))
        finally: MC.run = o
        i = a == c; ok &= i; kws[n] = (kw, kw0); log(f"  A2 mixto([{n}]*9) == corre_juntos.tarea({n}) · mueve {mv}: {i} ({len(json.dumps(c))} bytes)")
    X = {}
    for b in (('pmix', 'pmixbar', 'pmudo') if not corta else ('pmix',)):
        nom, e = carros_de(b, 0)
        con = tarea(seed, nom, T, mundo); sin = tarea(seed, nom, T, mundo, sondas=False); X[b] = con
        i = Nz(con) == Nz(sin); ok &= i; log(f"  A3 sondas no perturban · {b}: con ganchos == sin ganchos {i}")
    k1, k0 = next(iter(kws.values())); esperado = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **mundo)
    i = bool(k1 and k0 and k1[0] == k0[0] == esperado); ok &= i; log(f"  A4 regla 14: kwargs de mundo_tramo_c.run == corre_juntos == {{T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1}} + mundo: {i} · {k1[0] if k1 else None}")
    mixx = tarea(seed, carros_de('mix', 0)[0], T, mundo); L_ = lambda x: Nz(x)['linajes']
    d = [L_(X['pmix']) != L_(mixx)]
    if not corta: d += [L_(X['pmixbar']) != L_(X['pmix']), L_(X['pmudo']) != L_(X['pmix']), L_(tarea(seed, carros_de('pmix', 4)[0], T, mundo)) != L_(X['pmix'])]
    i = all(d); ok &= i; log(f"  A5 el arnes puede fallar (pmix != mix{'' if corta else ' · pmixbar != pmix · pmudo != pmix · explorador en 4 != en 0'}): {d}")
    f = fila(X['pmix'], T, *carros_de('pmix', 0)); fm = fila(mixx, T, *carros_de('mix', 0))
    tel = sum(z or 0 for z in f['lectores']['sn_pisa_tel']); son = f['sonda']['pisa']['total']
    i = son > 0 and son >= tel and fm['sonda']['pisa']['total'] == 0 and all(z is None for z in fm['lectores']['sn_pisa_tel']) and f['lectores']['sn_pisa_tel'][0] is None
    ok &= i; log(f"  A6 sonda de pisadas: pmix sonda {son} >= telemetria {tel} (fund {f['fund']}) · clasificacion {f['sonda']['pisa']} · hereda {f['sonda']['hereda']} · mix 0: {i}")
    S = [set(range(SEM['serie'], SEM['serie'] + N_SERIE)), set(range(SEM['replica'], SEM['replica'] + N_SERIE)), set(range(SEM['humo'], SEM['humo'] + 4)), {SEM['arnes']},
         {738611, 738612, 738621, 738622, 738623, 738630, 738631}]
    i = all(not (a & b) for j, a in enumerate(S) for b in S[j + 1:]) and all(738600 < s < 738700 for s in set.union(*S)); ok &= i
    log(f"  A7 semillas disjuntas y nuevas (7386xx): {i}")
    log(f"  ARNES {'OK' if ok else 'FALLA'}")
    return ok


def guarda(modo, pre, reanuda):
    """Candados de --serie/--replica (PREREGISTRO_pisa.md sec. 8)."""
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if r.get('modo') == modo and (r.get('letra') or {}).get('veredicto') in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda (cortada o NO SE LEE)"
    if modo == 'replica':
        rsm = sorted(glob.glob(os.path.join(DATOS, f"pisa_serie_s{SEM['serie']}-*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto'); um = (rs0.get('letra') or {}).get('en_umbral')
        if not (vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um)):
            return f"REGLA DE PARADA: la replica solo si la serie da FUNCIONA, HAY ALGO MODESTO o NO en el umbral (+-1); serie = {vs} (umbral {um})"
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)): return f"sha_runner de la serie {rs0.get('sha_runner')} != runner actual"
    import subprocess
    archivos = ([os.path.join(AQUI, 'PREREGISTRO_pisa.md'), os.path.abspath(__file__)] + list(SHAS) + list(CM.SHAS))
    for r in archivos:
        rel = os.path.relpath(r, RAIZ).replace(os.sep, '/')
        t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
        c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
        if not (t and c): return f"git: {rel} commiteado {t} · sin cambios vs HEAD {c} (la serie exige todo commiteado)"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--identidad', action='store_true')
    g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--n', type=int, default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--desde', type=int, default=None); ap.add_argument('--mueve', type=int, default=None); ap.add_argument('--nota', default='')
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX}")
    if a.lee:
        R, ab = lee(os.path.abspath(a.lee))
        pres = [b for b in ORDEN if R.get(b)]
        if not pres: raise SystemExit(f"--lee: no hay prueba_i*_*.json validos en {a.lee} (abortos {ab})")
        n = max(len(R[b]) for b in pres if b in LETRA) if any(b in LETRA for b in pres) else max(len(R[b]) for b in pres)
        x0 = R[pres[0]][min(R[pres[0]])]; mv = (x0.get('oasis_info') or {}).get('mueve') or MUEVE
        L = lee_serie(R, n, len(ab), mueve=mv, T=x0['T']); imprime(L, print)
        print(f"VEREDICTO ({'letra' if (n == N_SERIE and x0['T'] == T_SERIE and mv == MUEVE) else 'parcial/humo, no cuenta'}): {L['veredicto']} · abortos {ab}")
        return 0
    BUF = []; LOGF = [None]

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"
        print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    if a.identidad:
        log(f"CORRE_PISA_SERIE · identidad · un proceso · corre_pisa_serie.py {h16(os.path.abspath(__file__))}")
        return 0 if (verifica(log) and identidad(log)) else 1
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        modo = 'humo'; n = a.n or HUMO['n']; T = a.T or HUMO['T']; mv = a.mueve or HUMO['mueve']; base = a.desde or SEM['humo']
        brazos = tuple(a.brazos.split(',')) if a.brazos else LETRA; dest = os.path.join(DATOS, 'humo_prot'); tareas_b = [(i, b) for i in range(n) for b in brazos]
        if len(tareas_b) > MAX_CORRIDAS_1P or T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(tareas_b)}) y <= {MAX_PASOS_1P} pasos")
    else:
        if a.T or a.n or a.brazos or a.desde or a.mueve: raise SystemExit("--serie/--replica: T, n, brazos, mueve y semillas los fija el preregistro")
        modo = 'serie' if a.serie else 'replica'; n = N_SERIE; T = T_SERIE; mv = MUEVE; base = SEM[modo]; dest = DATOS
        # primero los 4 brazos de la LETRA (por semilla), al final los descriptivos (solo serie, primeras N_DESC semillas)
        tareas_b = [(i, b) for i in range(n) for b in LETRA] + ([(i, b) for i in range(N_DESC) for b in DESC] if modo == 'serie' else [])
    for _, b in tareas_b:
        if b not in BRAZOS: raise SystemExit(f"brazo desconocido {b}")
    mundo = dict(MUNDO, mueve=mv)
    pre = f"pisa_{modo}_s{base}-{base + n - 1}_T{T}_m{mv}"
    sel = time.strftime('%Y%m%d_%H%M%S')
    prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
    if a.reanuda and not prev: raise SystemExit(f"--reanuda: no hay carpeta {pre}_* en {dest}")
    if modo in ('serie', 'replica'):
        e = guarda(modo, pre, a.reanuda)
        if e: raise SystemExit(f"NO SE CORRE (candado): {e}")
    carpeta = os.path.join(dest, prev[-1]) if (a.reanuda and prev) else os.path.join(dest, pre + '_' + sel)
    t0 = time.time()
    log(f"CORRE_PISA_SERIE · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_pisa_serie.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  semillas {base}-{base + n - 1} · T {T} · corridas {len(tareas_b)} · mundo {mundo} · reanuda {a.reanuda} · nota {a.nota!r}")
    if not (verifica(log) and identidad(log, T=1500, corta=True)): log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    tareas = [(i, b, base, T, carpeta, a.reanuda, mundo) for i, b in tareas_b]

    def fmt(x):
        if x.get('aborto'): return f"  [{time.time()-t0:7.1f}s] i{x['i']} {x['brazo']:7s} ({x.get('seg')}s) ABORTO {x['aborto']}"
        lc = x['lectores']; pz = x['sonda']['pisa']
        return (f"  [{time.time()-t0:7.1f}s] i{x['i']} {x['brazo']:7s} ({x.get('seg')}s) e{lc['explorador']} LECTORES lat {lc['lat_med']} (nunca {lc['nunca']}) por mudanza {lc['lat_por_mudanza']} · "
                f"explorador {lc['lat_explorador_med']} · cruzan {x['cruzan']}/9 (lect {lc['cruza']}) fund lect {lc['fund_media']} · lee {lc['sn_lee']} siembra {lc['sn_siembra']} · "
                f"pisa {pz['total']} (nuevo {pz['frac_nuevo']} viejo {pz['frac_viejo']}) hereda {x['sonda']['hereda']} · mundo AC {x.get('mundo_AC')}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): log(fmt(x))
    else:
        for tk in tareas: log(fmt(trabajo(tk)))
    R, ab = lee(carpeta); L = lee_serie(R, n, len(ab), mueve=mv, T=T)
    log(f"\n================ LA LETRA (escalada a n {n})" + (" -- HUMO: NO cuenta, no se declara" if modo == 'humo' else ""))
    imprime(L, log)
    if ab: log(f"  ABORTOS: {ab}")
    ver = ('HUMO (no cuenta): ' if modo == 'humo' else '') + L['veredicto'] + (' (EN EL UMBRAL)' if L['en_umbral'] else '')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, letra=L, abortos=ab, n=n, T=T, semillas=[base, base + n - 1], veredicto=ver, nota=a.nota, mundo=mundo,
                       sha_runner=h16(os.path.abspath(__file__)), shas={os.path.relpath(k, ESC): h16(k) for k in list(SHAS) + list(CM.SHAS)},
                       mundo_c=MC.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {len(ab)} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO: {ver}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
