"""corre_p10.py — RUNNER del peldano 10 de la escalera: PREGUNTARSE (ir a donde menos se sabe cuando el oasis se muda; O1_LUGAR_PREG) en el
mundo de P1b con `mueve` (mundo_tramo_c). 30-sep-2026, ingeniero genetico Fable. Preregistro: PREREGISTRO_p10.md. Arnes: identidad_p10.py.
Escalera: ESCALERA.md (P10). Carros: construye_c.py (sobre el texto de O1_LUGAR de construye_p1, sha fijado). Bitacora: BITACORA.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE SE CORRE: cada corrida ES corre_v143.tarea (regla 14; se IMPORTA) con mundo_tramo_c.run en lugar de pista.run (mueve = 20 000: el oasis se
muda cada 20k pasos, 4 veces en T 100k). La tarea y la fila las arma corre_c (tarea, fila_c; se IMPORTA, sha fijado), que a su vez usa
corre_p1.fila (CONGELADO). Lo agregado aqui: la LETRA (lee_serie), los candados de --serie/--replica y la bitacora.
  BRAZOS (monocultivo de 9, L 360, 36 objetos, fundador limpio; mundo P1b + mueve 20000):
    preg     O1_LUGAR_PREG      (a) olvido por presencia; (b) sin blanco y sin recuerdo va al bin que hace MAS tiempo no visita   EL CANDIDATO
    pregbar  O1_LUGAR_PREG_BAR  (a) igual; (b) va al ANTIPODA de ese bin (mismas excursiones, destino fijo y equivocado)           CONTROL
    lug      O1_LUGAR           sin modulo: la BASE (P1)
MEDIDA PRINCIPAL: linajes que cruzan (cruza_real), por semilla y suma. CO-PRINCIPAL: fundadores por linaje (menos = se establece).
MECANISMO (fisica del mundo): latencia = pasos desde cada mudanza hasta el primer bocado A+C dentro del oasis NUEVO, por linaje y mudanza
(nunca = T), mediana por corrida: preg < lug.
SEMILLAS NUEVAS 7398xx: serie 739821-739840 · replica 739851-739870 · humo 739890-739895 (739890-739891 usados: humo 1) · explora
739801-739805 (739801-739802 usados: exploracion 1) · arnes 739880-739889.
  python experimentos/organelos/escalera/corre_p10.py --humo [--desde 739892] [--T 30000] [--n 2] [--mueve 10000] [--nota '...']
  python experimentos/organelos/escalera/corre_p10.py --serie --pool 2 [--reanuda]     (solo el coordinador; 20 semillas x 3 brazos)
  python experimentos/organelos/escalera/corre_p10.py --replica --pool 2
  python experimentos/organelos/escalera/corre_p10.py --lee <carpeta>
"""
import argparse, glob, json, math, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path.insert(0, AQUI)
import corre_c as CR             # tarea, fila_c, modulo (se IMPORTA; sha fijado)
import construye_c as CC
CO = CR.CO; MC = CR.MC; ME = CR.ME; CV = CR.CV; P = CR.P

SHAS_P10 = {'corre_p1.py': '392b71186cf49b60', 'construye_p1.py': '90dc1b6f848fac80', 'mundo_escalera.py': '4f28b372207ba0a6',
            'mundo_tramo_c.py': '4a1044a4e0e1d5c9', 'construye_c.py': '024a89476109b997', 'corre_c.py': '01e4ad94dd06e133'}   # fijados al cerrar el preregistro (30-sep 22:40); si cambian, no corre
DATOS = os.path.join(AQUI, 'datos'); BITACORA = os.path.join(AQUI, 'BITACORA.md')
CARROS = {n: CR.CARROS[n] for n in ('O1_LUGAR_PREG', 'O1_LUGAR_PREG_BAR', 'O1_LUGAR_PREG0')}
CARROS['O1_LUGAR'] = CO.CARROS['O1_LUGAR']
MUEVE = 20000
MUNDO_P10 = dict(CO.MUNDO_OASIS, mueve=MUEVE)
BRAZOS = {'preg': 'O1_LUGAR_PREG', 'pregbar': 'O1_LUGAR_PREG_BAR', 'lug': 'O1_LUGAR'}
ORDEN = ('preg', 'pregbar', 'lug'); CAND = 'preg'; CTRL = 'pregbar'; BASE = 'lug'; RAFAGA = ORDEN
SEM = dict(humo=739890, explora=739801, serie=739821, replica=739851)
N_SERIE = 20; T_SERIE = 100000; POOL_MAX = 2
HUMO = dict(n=2, T=30000, mueve=10000); EXPLORA = dict(n=2, T=100000, mueve=MUEVE)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000
GANA_PAR = 13; DIF_SUMA = 10
h16 = CO.h16; med = CO.med; esc = CO.esc; par = CO.par; par_menor = None


def _par_menor(A, B, I, k):
    a = [A[i][k] for i in I]; b = [B[i][k] for i in I]
    return dict(n=len(I), gana=sum(x < y for x, y in zip(a, b)), empata=sum(x == y for x, y in zip(a, b)), pierde=sum(x > y for x, y in zip(a, b)),
                med_a=med(a), med_b=med(b), por_indice_a=a, por_indice_b=b)


def fila(x, T):
    f = CR.fila_c(x, T, 'preg')
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
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=None, **fila(CR.tarea(base + i, BRAZOS[brazo], T, mundo), T))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_p10.md sec. 6)
def lee_serie(R, n, abortos, brazos=ORDEN, mueve=MUEVE, T=T_SERIE):
    I = list(range(n)); gp = esc(GANA_PAR, n); dsu = math.ceil(DIF_SUMA * n / 20 - 1e-9)
    completo = all(len(R.get(b, {})) == n for b in brazos)
    n_mud = T // mueve - (1 if T % mueve == 0 else 0)
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(R[b][i]['coherente'] for b in brazos for i in R.get(b, {})))
    v['V2_se_muda'] = bool(all((R[b][i].get('preg') or {}).get('mudanzas') == n_mud and (R[b][i].get('oasis_info') or {}).get('mueve') == mueve
                                for b in brazos for i in R.get(b, {})))
    v['V3_mundo_actua'] = bool(all(R[b][i].get('oasis') and R[b][i]['oasis']['mord_AC_dentro'] > 0 and R[b][i]['oasis']['extra'] == ME.EXTRA
                                   and R[b][i]['oasis']['pobre'] == ME.POBRE for b in brazos for i in R.get(b, {})))
    est = lambda d: d.get('estado') or {}
    v['V4_estado'] = bool(all(est(R[b][i]).get('carro') == BRAZOS[b] and est(R[b][i]).get('mundo', {}).get('mueve') == mueve and est(R[b][i]).get('LUGAR') == 1
                              and est(R[b][i]).get('LUGAR_BARAJA') == 0 and (est(R[b][i]).get('PREGUNTA') == 1 if b != BASE else 'PREGUNTA' not in est(R[b][i]))
                              and (est(R[b][i]).get('PG_BARAJA') == int(b == CTRL) if b != BASE else True) for b in brazos for i in R.get(b, {})))
    v['V5_modulo_actua'] = bool(all((R[b][i].get('preg') or {}).get('pg_exc', 0) > 0 and (R[b][i].get('preg') or {}).get('pg_olv', 0) > 0 for b in (CAND, CTRL) if b in brazos for i in R.get(b, {}))
                                and all((R[BASE][i].get('preg') or {}).get('pg_exc', 0) == 0 for i in R.get(BASE, {})))
    valido = all(v.values()); ok = valido or completo
    p = {}; pa = pb = pf = pm = None
    if ok:
        pa = par(R[CAND], R[BASE], I); pb = par(R[CAND], R[CTRL], I)
        pf = _par_menor(R[CAND], R[BASE], I, 'fund_media'); pm = _par_menor(R[CAND], R[BASE], I, 'lat_med'); pmc = _par_menor(R[CAND], R[CTRL], I, 'lat_med')
        p['PA_par_lug'] = pa['gana'] >= gp; p['PA_suma_lug'] = pa['dif'] >= dsu
        p['PB_par_pregbar'] = pb['gana'] >= gp; p['PB_suma_pregbar'] = pb['dif'] >= dsu
        p['PF_fund_par'] = pf['gana'] >= gp
        p['PM_latencia_par'] = pm['gana'] >= gp and pmc['gana'] >= gp
    umbral = bool(ok and (any(abs(q['gana'] - gp) <= 1 for q in (pa, pb, pf, pm)) or any(abs(q['dif'] - dsu) <= 1 for q in (pa, pb))))
    matiz = None
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif ((p['PA_par_lug'] or p['PA_suma_lug']) or p['PF_fund_par']) and (p['PB_par_pregbar'] or p['PB_suma_pregbar']) and p['PM_latencia_par']: ver = 'HAY ALGO MODESTO'
    elif ((p['PA_par_lug'] or p['PA_suma_lug']) or p['PF_fund_par']) and (p['PB_par_pregbar'] or p['PB_suma_pregbar']): ver = 'NO'; matiz = 'gana sin encontrar antes el oasis nuevo (instrumento)'
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
        desc['nunca_llegan'] = {b: sum((R[b][i].get('preg') or {}).get('nunca', 0) for i in I) for b in brazos}
        desc['mundo_AC'] = {b: med([R[b][i]['mundo_AC'] for i in I]) for b in brazos}
        desc['mundo_AC_cand_sobre_base'] = (round(desc['mundo_AC'][CAND] / desc['mundo_AC'][BASE], 3) if desc['mundo_AC'].get(BASE) else None)   # trampa 3: se reporta, no puntua
        desc['ratio_pasos_oasis'] = {b: med([R[b][i]['oasis']['ratio_pasos'] for i in I]) for b in brazos}
        desc['excursiones'] = {b: med([(R[b][i].get('preg') or {}).get('pg_exc') for i in I]) for b in brazos}
        desc['olvidos'] = {b: med([(R[b][i].get('preg') or {}).get('pg_olv') for i in I]) for b in brazos}
        desc['pareados'] = {f"{a}_vs_{c}": par(R[a], R[c], I) for a, c in (('preg', 'lug'), ('preg', 'pregbar'), ('pregbar', 'lug')) if a in brazos and c in brazos}
    return dict(validez=v, puertas=p, veredicto=ver, matiz=matiz, en_umbral=umbral, umbrales=dict(gana_par=gp, dif_suma=dsu),
                pareado_lug=pa, pareado_pregbar=pb, pareado_fund=pf, pareado_latencia=pm, descriptivo=desc)


def lee(carpeta):
    R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        d['fund_media'] = float(st.mean(d['fund'])); d['lat_med'] = (d.get('preg') or {}).get('latencia_med')
        if d['lat_med'] is None: d['lat_med'] = float(d['T'])
        R[d['brazo']][d['i']] = d
    return R, ab


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  puertas: {L['puertas']} · umbrales {L['umbrales']} · EN EL UMBRAL (+-1): {L['en_umbral']} · matiz {L['matiz']}")
    for k in ('pareado_lug', 'pareado_pregbar'):
        q = L[k]
        if q: log(f"  {k}: gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · suma {q['suma_a']} vs {q['suma_b']} (dif {q['dif']}) · por indice {q['por_indice_a']} vs {q['por_indice_b']}")
    for k in ('pareado_fund', 'pareado_latencia'):
        q = L[k]
        if q: log(f"  {k} (menor gana): gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · mediana {q['med_a']} vs {q['med_b']}")
    for k, v in L['descriptivo'].items():
        if k != 'pareados': log(f"  [desc] {k}: {v}")


def verifica(log):
    ok = CO.verifica(log)
    for nm, sha in SHAS_P10.items():
        s = h16(os.path.join(AQUI, nm)); fij = sha is not None; ok &= (s == sha) if fij else True
        log(f"  sha {nm} {s} {'OK' if (not fij or s == sha) else '!= ' + sha + ' FALLA'}{'' if fij else ' (NO FIJADO: solo humo/explora)'}")
    for nm, b in CC.todas('preg').items():
        igual = os.path.exists(CARROS[nm]) and open(CARROS[nm], 'rb').read() == b; ok &= igual
        log(f"  carro {nm} == construye_c: {igual} (sha {h16(CARROS[nm]) if os.path.exists(CARROS[nm]) else 'NO EXISTE'})")
    log(f"  mundo_tramo_c: {MC.construye()[1]}")
    return ok


def identidad_corta(log, seed=739880, T=1500):
    """(1) mundo_tramo_c con mueve 0 == mundo_escalera (salida entera); (2) PREG0 == O1_LUGAR; (3) con mueve el oasis se muda (bins final != inicial)."""
    N = lambda x: json.loads(json.dumps(x, default=str))
    lug, _ = CR.modulo('O1_LUGAR'); p0, _ = CR.modulo('O1_LUGAR_PREG0'); pg, _ = CR.modulo('O1_LUGAR_PREG')
    kw = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **CO.MUNDO_OASIS)
    base = N(ME.run(seed, [('X', lug)] * 9, **kw))
    i1 = N(MC.run(seed, [('X', lug)] * 9, **kw)) == base
    i2 = N(MC.run(seed, [('X', p0)] * 9, **dict(kw, mueve=T // 3))) == N(MC.run(seed, [('X', lug)] * 9, **dict(kw, mueve=T // 3)))
    r = N(MC.run(seed, [('X', pg)] * 9, **dict(kw, mueve=T // 3))); oz = r['pista']['oasis']
    i3 = len(oz['mudanzas']) == 3 and oz['bins30_final'] != oz['bins30']
    log(f"  IDENTIDAD CORTA P10 (salida ENTERA, N 9, s {seed}, T {T}): mundo_tramo_c mueve 0 == mundo_escalera {i1} · PREG0 == O1_LUGAR con mueve {i2} · el oasis se muda (3 epocas, bins {oz['bins30']} -> {oz['bins30_final']}) {i3}")
    return i1 and i2 and i3


def guarda(modo, pre, reanuda):
    """Candados de --serie/--replica (PREREGISTRO_p10.md sec. 7): como corre_p7.guarda; exige los shas FIJADOS (ninguno None)."""
    if any(v is None for v in SHAS_P10.values()): return f"SHAS_P10 sin fijar: {[k for k, v in SHAS_P10.items() if v is None]} (fijar al cerrar el preregistro)"
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if r.get('modo') == modo and (r.get('letra') or {}).get('veredicto') in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda (cortada o NO SE LEE)"
    if modo == 'replica':
        rsm = sorted(glob.glob(os.path.join(DATOS, f"p10_serie_s{SEM['serie']}-*", 'resumen.json')))
        rs0 = json.load(open(rsm[-1], encoding='utf-8')) if rsm else {}
        vs = (rs0.get('letra') or {}).get('veredicto'); um = (rs0.get('letra') or {}).get('en_umbral')
        if not (vs in ('FUNCIONA', 'HAY ALGO MODESTO') or (vs == 'NO' and um)):
            return f"REGLA DE PARADA: la replica solo si la serie da FUNCIONA, MODESTO o NO EN EL UMBRAL; serie = {vs} (umbral {um})"
        if rs0.get('sha_runner') != h16(os.path.abspath(__file__)): return f"sha_runner de la serie {rs0.get('sha_runner')} != runner actual"
    import subprocess
    archivos = [os.path.join(AQUI, 'PREREGISTRO_p10.md'), os.path.abspath(__file__)] + [os.path.join(AQUI, k) for k in SHAS_P10] + list(CARROS.values())
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
        R, ab = lee(os.path.abspath(a.lee)); brazos = tuple(b for b in ORDEN if R[b]); n = max(len(R[b]) for b in brazos)
        x0 = R[brazos[0]][min(R[brazos[0]])]; mv = (x0.get('oasis_info') or {}).get('mueve') or MUEVE
        L = lee_serie(R, n, len(ab), brazos, mueve=mv, T=x0['T']); imprime(L, print)
        print(f"VEREDICTO ({'parcial/humo, no cuenta' if n != N_SERIE or set(brazos) != set(ORDEN) or x0['T'] != T_SERIE else 'letra'}): {L['veredicto']} · abortos {ab}")
        return 0
    if a.humo or a.explora:
        if a.pool: raise SystemExit("--humo/--explora: sin Pool (un proceso)")
        modo = 'humo' if a.humo else 'explora'; cfg = HUMO if a.humo else EXPLORA
        n = a.n or cfg['n']; T = a.T or cfg['T']; brazos = tuple(a.brazos.split(',')) if a.brazos else RAFAGA; base = a.desde or SEM[modo]; mv = a.mueve or cfg['mueve']
        if len(brazos) * n > MAX_CORRIDAS_1P or T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(brazos) * n}) y <= {MAX_PASOS_1P} pasos (T {T})")
        dest = os.path.join(DATOS, 'p10_' + modo)
    else:
        if a.T or a.n or a.brazos or a.desde or a.mueve: raise SystemExit("--serie/--replica: T, n, brazos, mueve y semillas los fija el preregistro")
        modo = 'serie' if a.serie else 'replica'; n = N_SERIE; T = T_SERIE; brazos = ORDEN; base = SEM[modo]; dest = DATOS; mv = MUEVE
    for b in brazos:
        if b not in BRAZOS: raise SystemExit(f"brazo desconocido {b}")
    mundo = dict(CO.MUNDO_OASIS, mueve=mv)
    pre = f"{'p10_' if modo in ('serie', 'replica') else ''}{modo}_s{base}-{base + n - 1}_T{T}_m{mv}"
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
    log(f"CORRE_P10 · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · corre_p10.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  semillas {base}-{base + n - 1} · T {T} · brazos {list(brazos)} · mundo {mundo} · reanuda {a.reanuda} · nota {a.nota!r}")
    ok = verifica(log) and CO.identidad_corta(log) and CR.identidad_corta_c(log) and identidad_corta(log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    tareas = [(i, b, base, T, carpeta, a.reanuda, mundo) for i in range(n) for b in brazos]

    def fmt(x):
        oz = x.get('oasis') or {}; pg = x.get('preg') or {}
        return (f"  [{time.time()-t0:7.1f}s] i{x['i']} {x['brazo']:7s} ({x.get('seg')}s) aborto {x.get('aborto')} cruzan {x.get('cruzan')}/9 R0 {x.get('R0_med')} "
                f"fund {x.get('fund')} · oasis ratio pasos {oz.get('ratio_pasos')} · latencia {pg.get('latencia_med')} nunca {pg.get('nunca')} mudanzas {pg.get('mudanzas')} "
                f"exc {pg.get('pg_exc')} olv {pg.get('pg_olv')} · mundo AC {x.get('mundo_AC')}")
    X = []
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            for x in PL.imap_unordered(trabajo, tareas): X.append(x); log(fmt(x))
    else:
        for tk in tareas:
            x = trabajo(tk); X.append(x); log(fmt(x))
    R, ab = lee(carpeta); L = lee_serie(R, n, len(ab), brazos, mueve=mv, T=T)
    log(f"\n================ LA LETRA (escalada a n {n})" + (" -- HUMO/EXPLORA: NO cuenta, no se declara" if modo in ('humo', 'explora') else ""))
    imprime(L, log)
    if ab: log(f"  ABORTOS: {ab}")
    ver = (f"{modo.upper()} (no cuenta): " if modo in ('humo', 'explora') else '') + L['veredicto'] + (f" ({L['matiz']})" if L.get('matiz') else '')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, letra=L, abortos=ab, n=n, T=T, brazos=list(brazos), semillas=[base, base + n - 1], veredicto=ver, nota=a.nota, mundo=mundo,
                       sha_runner=h16(os.path.abspath(__file__)), shas_p10={k: h16(os.path.join(AQUI, k)) for k in SHAS_P10},
                       shas={os.path.relpath(k, RAIZ): v for k, v in CO.SHAS.items()}, carros={k: h16(v) for k, v in CARROS.items()},
                       mundo_c=MC.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {len(ab)} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO: {ver}")
    if modo in ('humo', 'explora'):
        d = L['descriptivo']; sc = d.get('suma_cruzan', {}); es = d.get('establecidos_0fund_post10k', {}); pa = L.get('pareado_lug') or {}; pb = L.get('pareado_pregbar') or {}
        pf = L.get('pareado_fund') or {}; pm = L.get('pareado_latencia') or {}
        senal = 'no se lee' if not sc else ('si' if (pa.get('dif', 0) > 0 and pb.get('dif', 0) > 0 and pm.get('gana', 0) > pm.get('pierde', 0)) else
                                            'si (establecimiento/latencia; cruce no)' if (pf.get('gana', 0) > pf.get('pierde', 0) and pm.get('gana', 0) > pm.get('pierde', 0)) else 'no')
        bitacora(f"| {time.strftime('%Y-%m-%d %H:%M')} | p10 preguntarse (corre_p10, mueve {mv}) | {modo} s{base}-{base + n - 1} T{T} {list(brazos)} carro {h16(CARROS['O1_LUGAR_PREG'])} {a.nota} | "
                 f"cruzan {sc} · establecidos {es} · R0 {d.get('R0_med')} · fund {d.get('fund_media')} · latencia {d.get('latencia_med')} · nunca {d.get('nunca_llegan')} · "
                 f"mundo AC {d.get('mundo_AC')} (cand/base {d.get('mundo_AC_cand_sobre_base')}) · preg-lug {pa.get('dif')} preg-pregbar {pb.get('dif')} · abortos {len(ab)} · {os.path.relpath(carpeta, AQUI)} | {senal} |")
    return 0


if __name__ == '__main__':
    sys.exit(main())
