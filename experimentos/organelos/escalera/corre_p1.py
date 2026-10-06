"""corre_p1.py — RUNNER del peldano 1 de la escalera: MEMORIA DE LUGAR (O1_LUGAR) en el mundo con OASIS (30-sep-2026, MODO RAFAGA).
Escalera: ESCALERA.md · mundo: mundo_escalera.py · carros: construye_p1.py · arnes: identidad_p1.py · bitacora: BITACORA.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE SE CORRE (cada corrida ES experimentos/tronco_v14_3/corre_v143.tarea, que se IMPORTA y no se toca = juez.tarea(seed, 9 carros iguales,
T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje; con el mundo mundo_escalera.run en lugar de
pista.run (con oasis 0 es pista.run bit a bit: arnes). Lo unico agregado: 'oasis' (fisica de solo lectura del mundo), 'lugar' (telemetria del
carro, no puntua) y 'estado' (las perillas fijadas en ESTE proceso)):
  BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, fundador limpio):
    lug   O1_LUGAR      en el mundo con oasis (extra 0.8, pobre 0.5)   EL CANDIDATO
    bar   O1_LUGAR_BAR  en el mismo mundo: control de CONTENIDO (lee la memoria en un bin permutado: el mismo sesgo, el lugar equivocado)
    o1    O1            en el mismo mundo: la BASE (sin memoria de lugar)
    o1f   O1            en el mundo SIN oasis (la pista de siempre): ancla de validez (O1_LUGAR alli == O1 bit a bit, arnes: no hace falta brazo)
MEDIDA PRINCIPAL: linajes que cruzan (cruza_real del juez: R0 real >= 0.90 y 0 fundadores tras t = 10 000), por semilla (0-9) y suma.
MECANISMO (fisica): fraccion de pasos DENTRO del oasis / 0.10 (1.0 = al azar) y fraccion de mordidas A+C dentro / 0.10.
SEMILLAS NUEVAS (grep 30-sep: 739xxx no aparece en .py/.md): humo 739990-739995 · explora 739201-739205 · serie 739001-739020 ·
replica 739101-739120 · arnes 739950-739989.
MODO RAFAGA (director 30-sep): --humo y --explora son de UN proceso (<= 6 corridas, <= 200k pasos cada una); NADA se declara; cada humo
escribe su JSON por corrida, un resumen y UNA linea en BITACORA.md. --serie/--replica (pool <= 2) SOLO el coordinador, con preregistro.

  python experimentos/organelos/escalera/corre_p1.py --humo                      # 2 semillas x (lug, bar, o1), T 30 000: 6 corridas
  python experimentos/organelos/escalera/corre_p1.py --explora                   # 2 semillas x (lug, bar, o1), T 100 000: 6 corridas
  python experimentos/organelos/escalera/corre_p1.py --explora --T 60000 --brazos lug,o1 --n 3
  python experimentos/organelos/escalera/corre_p1.py --serie --pool 2 [--reanuda]   (solo el coordinador; 20 semillas x 4 brazos)
  python experimentos/organelos/escalera/corre_p1.py --lee <carpeta>
"""
import argparse, copy, glob, hashlib, importlib.util, json, math, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV          # tarea (se IMPORTA, no se toca)
import construye_p1 as CB
import mundo_escalera as ME
P = CV.P; J = CV.J

DATOS = os.path.join(AQUI, 'datos'); BITACORA = os.path.join(AQUI, 'BITACORA.md')
CARROS = {n: os.path.join(AQUI, 'carros', n + '.py') for n, _, _ in CB.VARIANTES}
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4',
        os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12', os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028'}
DENS = 0.5; VISTA = 20   # P1b (humo 2): fraccion de la reposicion que nace dentro del oasis; radio de vista (0 = global, humo 1)
MUNDO_OASIS = dict(oasis=1, extra=ME.EXTRA, pobre=ME.POBRE, dens=DENS, vista_r=VISTA); MUNDO_LISO = dict(oasis=0, extra=ME.EXTRA, pobre=ME.POBRE, dens=0.0, vista_r=0)
# brazo -> (carro, archivo propio o None, mundo)
BRAZOS = {'lug': ('O1_LUGAR', CARROS['O1_LUGAR'], MUNDO_OASIS), 'bar': ('O1_LUGAR_BAR', CARROS['O1_LUGAR_BAR'], MUNDO_OASIS),
          'o1': ('O1', None, MUNDO_OASIS), 'o1f': ('O1', None, MUNDO_LISO)}
ORDEN = ('lug', 'bar', 'o1', 'o1f'); CAND = 'lug'; CTRL = 'bar'; BASE = 'o1'; ANCLA = 'o1f'
RAFAGA = ('lug', 'bar', 'o1')
SEM = dict(humo=739990, explora=739201, serie=739001, replica=739101)
N_SERIE = 20; T_SERIE = 100000; POOL_MAX = 2
HUMO = dict(n=2, T=30000); EXPLORA = dict(n=2, T=100000)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000
# ------------------------------------------------------------------ constantes de la LETRA (borrador; el preregistro la fija), n = 20
GANA_PAR = 13; DIF_SUMA = 10; O1F_MAY = 16; RATIO_LUG = 2.0; RATIO_O1 = (0.6, 1.5)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None
def esc(k, n): return math.ceil(k * n / 20 - 1e-9)


# ------------------------------------------------------------------ estado por proceso (cfg por worker)
def fija(brazo):
    """Carga en ESTE proceso el carro del brazo si falta (verifica su sha contra construye_p1) y lo registra en corre_v143._MODS."""
    n, ruta, mundo = BRAZOS[brazo]
    if ruta is None:
        CV.modulo(n); return dict(carro=n, sha=h16(os.path.join(PISTA, 'carros', 'O1.py')), LUGAR=None, mundo=dict(mundo))
    esperado = CB.todas()[n]
    if open(ruta, 'rb').read() != esperado: raise SystemExit(f"{ruta} != construye_p1 (correr construye_p1.py)")
    m = CV._MODS.get(n)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{n}", ruta)
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    return dict(carro=n, sha=h16(ruta), LUGAR=m.LUGAR, LUGAR_BARAJA=m.LUGAR_BARAJA, LUGAR_W=m.LUGAR_W, LG_NB=m.LG_NB, LG_ETA=m.LG_ETA,
                LG_MIN=m.LG_MIN, mundo=dict(mundo))


def tarea(seed, brazo, T, mundo=None):
    """corre_v143.tarea tal cual (regla 14) con el mundo de la escalera en lugar de pista.run + 'oasis', 'lugar' y 'estado'."""
    est = fija(brazo); n = BRAZOS[brazo][0]
    mk = dict(BRAZOS[brazo][2] if mundo is None else mundo); est['mundo'] = dict(mk)
    orig = P.run

    def run2(*a, **k):
        return ME.run(*a, **dict(k, **mk))
    P.run = run2
    try:
        x = CV.tarea((seed, n, T))
    finally:
        P.run = orig
    x['estado'] = est
    return x


def fila(x, T):
    """Una fila por corrida: fisica del juez + fisica del oasis + telemetria del carro (no puntua) + estado."""
    L = x['linajes']; pz = x['pista']; oz = pz.get('oasis')
    n = len(L); tel = x.get('tel') or []
    f = dict(seed=x['seed'], T=T, R0_real=[l['R0_real'] for l in L], R0_med=med([l['R0_real'] for l in L]),
             fund=[l['fundadores'] for l in L], fund_post10k=[l['fund_post10k'] for l in L], cruza=[int(l['cruza_real']) for l in L],
             cruzan=sum(int(l['cruza_real']) for l in L), mayoria=int(sum(int(l['cruza_real']) for l in L) * 2 > n),
             coherente=all(l.get('coherente', True) for l in L), nac_reales=[l.get('nac_reales') for l in L],
             muertes=[l['muertes'] for l in L], vida_med=med([l['vida_med'] for l in L]),
             mord_AC=sum(l['mord']['A'] + l['mord']['C'] for l in L), mord_BD=sum(l['mord']['B'] + l['mord']['D'] for l in L),
             mundo_AC=round(pz['comp_mundo']['A'] + pz['comp_mundo']['C'], 4), estado=x.get('estado'), seg=x.get('seg'))
    if oz is not None:
        ol = [l.get('_oasis') for l in L]
        pd = sum(o['pasos_dentro'] for o in ol if o); md = sum(o['mord_dentro']['A'] + o['mord_dentro']['C'] for o in ol if o)
        mf = sum(o['mord_fuera']['A'] + o['mord_fuera']['C'] for o in ol if o)
        f.update(oasis=dict(z0=oz['z0'], W=oz['W'], bins30=oz['bins30'], extra=oz['extra'], pobre=oz['pobre'], dens=oz.get('dens'), vista=oz.get('vista'),
                            frac_pasos_dentro=round(pd / (n * T), 4), ratio_pasos=round(pd / (n * T) / ME.FRAC_ZONA, 3),
                            mord_AC_dentro=md, mord_AC_fuera=mf,
                            ratio_mord=(round(md / (md + mf) / ME.FRAC_ZONA, 3) if md + mf else None)))
    lg = [t.get('lugar') for t in tel if t and t.get('lugar')]
    if lg:
        ob = set((oz or {}).get('bins30') or [])
        f['lugar'] = dict(n_linajes=len(lg), bono_blancos=sum(t['st_lg_bono'] for t in lg), aprendizajes=sum(t['st_lg_apr'] for t in lg),
                          viajes=sum(t.get('st_lg_viajes', 0) for t in lg),
                          max_med=med([t['max'] for t in lg]), bin_max_en_oasis=sum(int(t['bin_max'] in ob) for t in lg),
                          bins_con_bono_med=med([len(t['bins_con_bono']) for t in lg]),
                          bins_con_bono_en_oasis=(round(sum(sum(int(b in ob) for b in t['bins_con_bono']) for t in lg)
                                                        / max(1, sum(len(t['bins_con_bono']) for t in lg)), 3)))
    return f


def tarea_fila(seed, brazo, T):
    """tarea + extraccion de lo nuevo (oasis por linaje y telemetria del carro) sin tocar corre_v143.tarea."""
    x = tarea(seed, brazo, T)
    return x


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
        y = _tarea_completa(base + i, brazo, T)
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=None, **fila(y, T))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


def _tarea_completa(seed, brazo, T):
    """corre_v143.tarea guarda solo la telemetria de v143/apr; aqui se captura ADEMAS, de la salida cruda de la pista, la fisica del
    oasis por linaje (_carrera['oasis']) y la telemetria 'lugar' del carro (d['carro']['lugar'] + st), sin tocar corre_v143."""
    cap = []
    orig_run = ME.run

    def run_cap(*a, **k):
        r = orig_run(*a, **k); cap.append(r); return r
    ME.run = run_cap
    try:
        x = tarea(seed, brazo, T)
    finally:
        ME.run = orig_run
    r = cap[0]
    for l, d in zip(x['linajes'], r['linajes']):
        l['_oasis'] = d['_carrera'].get('oasis')
    x['tel'] = [dict(lugar=(dict(d['carro']['lugar'], st_lg_bono=d['carro'].get('lg_bono', 0), st_lg_apr=d['carro'].get('lg_apr', 0), st_lg_viajes=d['carro'].get('lg_viajes', 0))
                            if isinstance(d.get('carro'), dict) and 'lugar' in d['carro'] else None),
                     sn=({k: v for k, v in d['carro'].items() if k.startswith('sn_')} or None) if isinstance(d.get('carro'), dict) else None) for d in r['linajes']]
    return x


# ------------------------------------------------------------------ LA LETRA (borrador para el preregistro; el humo/explora la imprime ESCALADA y NO cuenta)
def par(A, B, I):
    a = [A[i]['cruzan'] for i in I]; b = [B[i]['cruzan'] for i in I]
    return dict(n=len(I), gana=sum(x > y for x, y in zip(a, b)), empata=sum(x == y for x, y in zip(a, b)), pierde=sum(x < y for x, y in zip(a, b)),
                suma_a=sum(a), suma_b=sum(b), dif=sum(a) - sum(b), por_indice_a=a, por_indice_b=b)


def lee_serie(R, n, abortos, brazos=ORDEN):
    I = list(range(n)); gp = esc(GANA_PAR, n); dsu = math.ceil(DIF_SUMA * n / 20 - 1e-9); om = esc(O1F_MAY, n)
    completo = all(len(R.get(b, {})) == n for b in brazos)
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(R[b][i]['coherente'] for b in brazos for i in R.get(b, {})))
    v['V2_ancla_o1f'] = (sum(R[ANCLA][i]['mayoria'] for i in R.get(ANCLA, {})) >= om) if ANCLA in brazos else None
    oz = [b for b in brazos if BRAZOS[b][2]['oasis']]
    v['V3_mundo_actua'] = all(R[b][i].get('oasis') and R[b][i]['oasis']['mord_AC_dentro'] > 0 and R[b][i]['oasis']['extra'] == ME.EXTRA
                              and R[b][i]['oasis']['pobre'] == ME.POBRE for b in oz for i in R.get(b, {})) \
        and all(R[b][i].get('oasis') is None for b in brazos if not BRAZOS[b][2]['oasis'] for i in R.get(b, {}))
    est = lambda d: d.get('estado') or {}
    v['V4_estado'] = all(est(R[b][i]).get('carro') == BRAZOS[b][0] and est(R[b][i]).get('mundo') == BRAZOS[b][2] for b in brazos for i in R.get(b, {})) \
        and all(est(R[b][i]).get('LUGAR') == 1 and est(R[b][i]).get('LUGAR_W') == CB.LUGAR_W and est(R[b][i]).get('LUGAR_BARAJA') == int(b == CTRL)
                for b in (CAND, CTRL) if b in brazos for i in R.get(b, {}))
    valido = all(x for x in v.values() if x is not None)
    ok = valido or completo
    p = {}; pa = pb = None
    if ok:
        pa = par(R[CAND], R[BASE], I); pb = par(R[CAND], R[CTRL], I)
        p['PA_par_o1'] = pa['gana'] >= gp; p['PA_suma_o1'] = pa['dif'] >= dsu
        p['PB_par_bar'] = pb['gana'] >= gp; p['PB_suma_bar'] = pb['dif'] >= dsu
        rl = med([R[CAND][i]['oasis']['ratio_pasos'] for i in I]); ro = med([R[BASE][i]['oasis']['ratio_pasos'] for i in I])
        p['PM_usa_el_lugar'] = bool(rl is not None and rl >= RATIO_LUG and ro is not None and RATIO_O1[0] <= ro <= RATIO_O1[1])
    umbral = bool(ok and any(abs(q['gana'] - gp) <= 1 or abs(q['dif'] - dsu) <= 1 for q in (pa, pb)))
    matiz = None
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif (p['PA_par_o1'] or p['PA_suma_o1']) and (p['PB_par_bar'] or p['PB_suma_bar']) and p['PM_usa_el_lugar']: ver = 'HAY ALGO MODESTO'
    elif (p['PA_par_o1'] or p['PA_suma_o1']) and (p['PB_par_bar'] or p['PB_suma_bar']): ver = 'NO'; matiz = 'gana sin ir al oasis (instrumento)'
    else: ver = 'NO'
    desc = {}
    if ok:
        desc['suma_cruzan'] = {b: sum(R[b][i]['cruzan'] for i in I) for b in brazos}
        desc['mayorias'] = {b: sum(R[b][i]['mayoria'] for i in I) for b in brazos}
        desc['R0_med'] = {b: med([R[b][i]['R0_med'] for i in I]) for b in brazos}
        desc['fund_media'] = {b: med([st.mean(R[b][i]['fund']) for i in I]) for b in brazos}
        desc['establecidos_0fund_post10k'] = {b: sum(sum(int(z == 0) for z in R[b][i]['fund_post10k']) for i in I) for b in brazos}
        desc['vida_med'] = {b: med([R[b][i]['vida_med'] for i in I]) for b in brazos}
        desc['mundo_AC'] = {b: med([R[b][i]['mundo_AC'] for i in I]) for b in brazos}
        desc['mord_AC'] = {b: med([R[b][i]['mord_AC'] for i in I]) for b in brazos}; desc['mord_BD'] = {b: med([R[b][i]['mord_BD'] for i in I]) for b in brazos}
        desc['ratio_pasos_oasis'] = {b: med([R[b][i]['oasis']['ratio_pasos'] for i in I]) for b in oz}
        desc['ratio_mord_oasis'] = {b: med([R[b][i]['oasis']['ratio_mord'] for i in I]) for b in oz}
        desc['lugar'] = {b: {k: med([(R[b][i].get('lugar') or {}).get(k) for i in I]) for k in
                             ('bono_blancos', 'aprendizajes', 'viajes', 'max_med', 'bin_max_en_oasis', 'bins_con_bono_med', 'bins_con_bono_en_oasis')}
                         for b in (CAND, CTRL) if b in brazos}
        desc['pareados'] = {f"{a}_vs_{b}": par(R[a], R[b], I) for a, b in (('lug', 'o1'), ('lug', 'bar'), ('bar', 'o1'), ('o1', 'o1f')) if a in brazos and b in brazos}
    return dict(validez=v, puertas=p, veredicto=ver, matiz=matiz, en_umbral=umbral, umbrales=dict(gana_par=gp, dif_suma=dsu, o1f_may=om),
                pareado_o1=pa, pareado_bar=pb, descriptivo=desc)


def lee(carpeta):
    R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        R[d['brazo']][d['i']] = d
    return R, ab


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  puertas: {L['puertas']} · umbrales {L['umbrales']} · EN EL UMBRAL (+-1): {L['en_umbral']} · matiz {L['matiz']}")
    for k in ('pareado_o1', 'pareado_bar'):
        q = L[k]
        if q: log(f"  {k}: gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · suma {q['suma_a']} vs {q['suma_b']} (dif {q['dif']}) · por indice {q['por_indice_a']} vs {q['por_indice_b']}")
    for k, v in L['descriptivo'].items():
        if k != 'pareados': log(f"  [desc] {k}: {v}")


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for nm, b in CB.todas().items():
        igual = os.path.exists(CARROS[nm]) and open(CARROS[nm], 'rb').read() == b; ok &= igual
        log(f"  carro {nm} == construye_p1: {igual} (sha {h16(CARROS[nm]) if os.path.exists(CARROS[nm]) else 'NO EXISTE'})")
    mi = ME.construye()[1]; log(f"  mundo_escalera: {mi}")
    return ok


def identidad_corta(log, seed=739950, T=1500):
    """(1) mundo oasis 0 == pista.run bit a bit con O1; (2) O1_LUGAR0 == O1; (3) O1_LUGAR sin oasis == O1 (salida ENTERA, N 9, fundador limpio)."""
    N = lambda x: json.loads(json.dumps(x, default=str))
    o1 = CV.modulo('O1'); fija('lug'); m = CV._MODS['O1_LUGAR']
    spec = importlib.util.spec_from_file_location('carro_O1_LUGAR0', CARROS['O1_LUGAR0']); m0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m0)
    kw = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
    base = N(P.run(seed, [('X', o1)] * 9, **kw))
    i1 = N(ME.run(seed, [('X', o1)] * 9, oasis=0, **kw)) == base
    i2 = N(ME.run(seed, [('X', m0)] * 9, oasis=0, **kw)) == base
    i3 = sin_tel(N(ME.run(seed, [('X', m)] * 9, oasis=0, **kw))) == base
    log(f"  IDENTIDAD CORTA (salida ENTERA, N 9, s {seed}, T {T}, fundador limpio): mundo oasis 0 == pista {i1} · O1_LUGAR0 == O1 {i2} · "
        f"O1_LUGAR sin oasis == O1 (salvo su telemetria 'lugar') {i3}")
    return i1 and i2 and i3


TELEM_LUGAR = ('lugar', 'lg_bono', 'lg_apr', 'lg_viajes')
def sin_tel(r):
    """la salida de pista.run sin la telemetria del modulo (d['carro']['lugar'], lg_bono, lg_apr), que solo existe con LUGAR = 1."""
    r = copy.deepcopy(r)
    for d in r['linajes']:
        if isinstance(d.get('carro'), dict):
            for k in TELEM_LUGAR: d['carro'].pop(k, None)
    return r


def guarda(modo, pre, reanuda):
    """Candados de --serie/--replica (PREREGISTRO_p1.md sec. 7): se niega si ya hay resumen con veredicto; carpetas previas solo con --reanuda;
    la replica solo si la serie dio FUNCIONA, MODESTO o NO en el umbral, y con el mismo sha del runner; preregistro, runner, constructor,
    mundo y carros commiteados y sin cambios respecto de HEAD (git_limpio)."""
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if r.get('modo') == modo and (r.get('letra') or {}).get('veredicto') in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda (cortada o NO SE LEE)"
    if modo == 'replica':
        rsm = sorted(glob.glob(os.path.join(DATOS, f"serie_s{SEM['serie']}-*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto'); um = (rs0.get('letra') or {}).get('en_umbral')
        if not (vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um)):
            return f"REGLA DE PARADA: la replica solo si la serie da FUNCIONA, MODESTO o NO EN EL UMBRAL; serie = {vs} (umbral {um})"
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)): return f"sha_runner de la serie {rs0.get('sha_runner')} != runner actual"
    import subprocess
    for r in [os.path.join(AQUI, 'PREREGISTRO_p1.md'), os.path.abspath(__file__), os.path.join(AQUI, 'construye_p1.py'), os.path.join(AQUI, 'mundo_escalera.py')] + list(CARROS.values()):
        rel = os.path.relpath(r, RAIZ).replace(os.sep, '/')
        t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
        c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
        if not (t and c): return f"git: {rel} commiteado {t} · sin cambios vs HEAD {c} (la serie exige todo commiteado)"
    return None


def bitacora(linea):
    nuevo = not os.path.exists(BITACORA)
    with open(BITACORA, 'a', encoding='utf-8') as fh:
        if nuevo: fh.write("# BITACORA de la escalera (MODO RAFAGA: humos y exploraciones de un proceso; NADA de esto se declara)\n\n| fecha | peldano | que se probo | numero | senal |\n|---|---|---|---|---|\n")
        fh.write(linea + '\n')


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true')
    g.add_argument('--serie', action='store_true'); g.add_argument('--replica', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--n', type=int, default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--desde', type=int, default=None); ap.add_argument('--nota', default='')
    ap.add_argument('--dens', type=float, default=None); ap.add_argument('--vista', type=int, default=None); ap.add_argument('--pobre', type=float, default=None)
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX}")
    if a.lee:
        R, ab = lee(os.path.abspath(a.lee)); brazos = tuple(b for b in ORDEN if R[b])
        n = max(len(R[b]) for b in brazos)
        L = lee_serie(R, n, len(ab), brazos); imprime(L, print)
        print(f"VEREDICTO ({'parcial/humo, no cuenta' if n != N_SERIE or set(brazos) != set(ORDEN) else 'letra'}): {L['veredicto']} · abortos {ab}")
        return 0
    if a.humo or a.explora:
        if a.pool: raise SystemExit("--humo/--explora: sin Pool (un proceso)")
        modo = 'humo' if a.humo else 'explora'; cfg = HUMO if a.humo else EXPLORA
        n = a.n or cfg['n']; T = a.T or cfg['T']; brazos = tuple(a.brazos.split(',')) if a.brazos else RAFAGA
        base = a.desde or SEM[modo]
        if len(brazos) * n > MAX_CORRIDAS_1P or T > MAX_PASOS_1P:
            raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(brazos) * n}) y <= {MAX_PASOS_1P} pasos (T {T})")
        dest = os.path.join(DATOS, modo)
        for k, v in (('dens', a.dens), ('vista_r', a.vista), ('pobre', a.pobre)):   # solo humo/explora: el mundo se puede mover; queda en estado y bitacora
            if v is not None: MUNDO_OASIS[k] = v
    else:
        if a.T or a.n or a.brazos or a.desde or a.dens is not None or a.vista is not None or a.pobre is not None: raise SystemExit("--serie/--replica: T, n, brazos y semillas los fija el preregistro")
        modo = 'serie' if a.serie else 'replica'; n = N_SERIE; T = T_SERIE; brazos = ORDEN; base = SEM[modo]; dest = DATOS
    for b in brazos:
        if b not in BRAZOS: raise SystemExit(f"brazo desconocido {b}")
    pre = f"{modo}_s{base}-{base + n - 1}_T{T}"
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
    log(f"CORRE_P1 · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_p1.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  semillas {base}-{base + n - 1} · T {T} · brazos {list(brazos)} · mundo oasis {MUNDO_OASIS} · reanuda {a.reanuda} · nota {a.nota!r}")
    ok = verifica(log) and identidad_corta(log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    tareas = [(i, b, base, T, carpeta, a.reanuda) for i in range(n) for b in brazos]

    def fmt(x):
        oz = x.get('oasis') or {}; lg = x.get('lugar') or {}
        return (f"  [{time.time()-t0:7.1f}s] i{x['i']} {x['brazo']:4s} ({x.get('seg')}s) aborto {x.get('aborto')} cruzan {x.get('cruzan')}/9 R0 {x.get('R0_med')} "
                f"fund {x.get('fund')} · oasis ratio pasos {oz.get('ratio_pasos')} mord {oz.get('ratio_mord')} · lugar bono {lg.get('bono_blancos')} "
                f"viajes {lg.get('viajes')} binmax en oasis {lg.get('bin_max_en_oasis')}/{lg.get('n_linajes')} bins bono en oasis {lg.get('bins_con_bono_en_oasis')} · mundo AC {x.get('mundo_AC')}")
    X = []
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): X.append(x); log(fmt(x))
    else:
        for tk in tareas:
            x = trabajo(tk); X.append(x); log(fmt(x))
    R, ab = lee(carpeta)
    L = lee_serie(R, n, len(ab), brazos)
    log(f"\n================ LA LETRA (borrador, escalada a n {n})" + (" -- HUMO/EXPLORA: NO cuenta, no se declara" if modo in ('humo', 'explora') else ""))
    imprime(L, log)
    if ab: log(f"  ABORTOS: {ab}")
    ver = (f"{modo.upper()} (no cuenta): " if modo in ('humo', 'explora') else '') + L['veredicto'] + (f" ({L['matiz']})" if L.get('matiz') else '')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, letra=L, abortos=ab, n=n, T=T, brazos=list(brazos), semillas=[base, base + n - 1], veredicto=ver, nota=a.nota,
                       sha_runner=h16(os.path.abspath(__file__)), shas={os.path.relpath(k, RAIZ): v for k, v in SHAS.items()},
                       carros={k: h16(v) for k, v in CARROS.items()}, mundo=ME.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {len(ab)} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO: {ver}")
    d = L['descriptivo']
    if modo in ('humo', 'explora'):
        sc = d.get('suma_cruzan', {}); rp = d.get('ratio_pasos_oasis', {}); pa = L.get('pareado_o1') or {}; pb = L.get('pareado_bar') or {}
        es = d.get('establecidos_0fund_post10k', {})
        gana_cruce = pa.get('dif', 0) > 0 and pb.get('dif', 0) > 0
        gana_est = es.get('lug', 0) > es.get('o1', 0) and es.get('lug', 0) > es.get('bar', 0)
        usa = (rp.get('lug') or 0) >= RATIO_LUG
        senal = ('si (cruce y establecimiento)' if (gana_cruce and gana_est and usa) else 'si (establecimiento; cruce no leido)' if (gana_est and usa and not gana_cruce)
                 else 'no') if sc else 'no se lee'
        bitacora(f"| {time.strftime('%Y-%m-%d %H:%M')} | p1 memoria de lugar | {modo} s{base}-{base + n - 1} T{T} {list(brazos)} mundo {MUNDO_OASIS} carro {h16(CARROS['O1_LUGAR'])} {a.nota} | "
                 f"cruzan {sc} · establecidos {es} · R0 {d.get('R0_med')} · ratio pasos oasis {rp} · lug-o1 {pa.get('dif')} lug-bar {pb.get('dif')} · mundo AC {d.get('mundo_AC')} · "
                 f"abortos {len(ab)} · {os.path.relpath(carpeta, AQUI)} | {senal} |")
    return 0


if __name__ == '__main__':
    sys.exit(main())
