"""corre_c.py — RUNNER DE RAFAGA del TRAMO C (peldanos 8 componer, 9 planear, 10 preguntarse) sobre O1_LUGAR en mundo_tramo_c
(30-sep-2026, ingeniero genetico Fable, MODO RAFAGA: solo --humo / --explora de UN proceso; NADA se declara; cada humo escribe su JSON por
corrida, un resumen y UNA linea en BITACORA.md). Plan: ESCALERA.md. Mundo: mundo_tramo_c.py. Carros: construye_c.py. Arnes: identidad_c.py.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE SE CORRE: cada corrida ES corre_v143.tarea (se IMPORTA, no se toca; regla 14: la de corre_p1) con mundo_tramo_c.run en lugar de
pista.run. Lo comun (cruzan, R0, fundadores, oasis, lugar) lo arma corre_p1.fila (se IMPORTA; corre_p1 esta CONGELADO y commiteado).
PELDANOS (--peldano), cada uno con su mundo (MUNDO_C + su perilla) y tres brazos (candidato, control de contenido, base lug):
  comp  P8  mundo: letra E (+0.3, -0.1), p_x 0.10.   comp O1_LUGAR_COMP · compbar O1_LUGAR_COMP_BAR (lee el antipoda) · lug O1_LUGAR
        medida (fisica, mundo_tramo_c.expone): J_frio = c1 + p1 - 1 con c1 = fraccion de exposiciones FRIAS a E dentro del oasis que se
        muerden, p1 = fraccion de primeras exposiciones a E fuera (ya conocida) que NO se muerden; y B dentro rechazada. SENAL: J(comp) >=
        0.5 y J(comp) > J(compbar) + 0.3 y B dentro rechazada >= 0.9 en comp.
  plan  P9  mundo: letra K (0, 0), p_x 0.10, cerrojo 1, d_llave 1500.   plan · planbar (credito a la penultima) · lug
        medida: fraccion de mordidas A+C dentro CON llave (>= 0.6 en plan), K mordidas por linaje, cruzan. SENAL: plan > lug y plan >
        planbar en cruzan y establecidos, con fraccion con llave >= 0.6.
  preg  P10 mundo: mueve (humo 10 000; explora 20 000).   preg · pregbar (antipoda del bin menos visitado) · lug
        medida: latencia = pasos hasta el primer bocado A+C dentro de cada oasis NUEVO (por linaje y mudanza; None = nunca -> se cuenta
        como T), mediana por brazo; cruzan. SENAL: latencia(preg) < latencia(lug) y < latencia(pregbar), y cruzan preg >= lug.
SEMILLAS NUEVAS (grep 30-sep: 7393xx, 7394xx, 7398xx no aparecen): comp humo 739390- explora 739301- · plan humo 739490- explora 739401- ·
preg humo 739890- explora 739801- · arnes 739950-739989 (las de P1, practica).
  python experimentos/organelos/escalera/corre_c.py --peldano plan --humo [--T 30000 --n 2 --brazos plan,planbar,lug --nota '...']
  python experimentos/organelos/escalera/corre_c.py --peldano preg --explora [--mueve 20000] [--d_llave 1500] [--p_x 0.1]
  python experimentos/organelos/escalera/corre_c.py --lee <carpeta>
"""
import argparse, glob, importlib.util, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path.insert(0, AQUI)
import corre_p1 as CO            # CONGELADO (76dc3d11): se importa, no se toca; su sha se fija
import construye_c as CC
import mundo_tramo_c as MC
CV = CO.CV; P = CO.P; ME = CO.ME

SHA_CORRE_P1 = '392b71186cf49b60'
DATOS = os.path.join(AQUI, 'datos'); BITACORA = os.path.join(AQUI, 'BITACORA.md')
CARROS = {n: os.path.join(AQUI, 'carros', n + '.py') for n, _, _, _, _ in CC.VARIANTES}
MUNDO_C = dict(CO.MUNDO_OASIS)   # oasis 1, extra 0.8, pobre 0.5, dens 0.5, vista_r 20 (P1b)
PELDANOS = {
    'comp': dict(mundo=dict(letra_x='E', efecto_x=(0.3, -0.1), p_x=0.1), brazos={'comp': 'O1_LUGAR_COMP', 'compbar': 'O1_LUGAR_COMP_BAR', 'lug': 'O1_LUGAR'},
                 sem=dict(humo=739390, explora=739301), nombre='p8 componer (letra E en el oasis)'),
    'plan': dict(mundo=dict(letra_x='K', efecto_x=(0.0, 0.0), p_x=0.1, cerrojo=1, d_llave=MC.D_LLAVE), brazos={'plan': 'O1_LUGAR_PLAN', 'planbar': 'O1_LUGAR_PLAN_BAR', 'lug': 'O1_LUGAR'},
                 sem=dict(humo=739490, explora=739401), nombre='p9 planear (cerrojo con llave K)'),
    'preg': dict(mundo=dict(mueve=10000), brazos={'preg': 'O1_LUGAR_PREG', 'pregbar': 'O1_LUGAR_PREG_BAR', 'lug': 'O1_LUGAR'},
                 sem=dict(humo=739890, explora=739801), nombre='p10 preguntarse (el oasis se muda)'),
}
HUMO = dict(n=2, T=30000); EXPLORA = dict(n=2, T=100000)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000
h16 = CO.h16; med = CO.med
RUN = [MC.run]   # el run del mundo; --mundo_k (p9 humo 3) lo cambia por mundo_k.run


def modulo(nombre):
    """carga el carro del tramo C (o O1_LUGAR via corre_p1.fija) en ESTE proceso, verificado contra su constructor; lo registra en CV._MODS."""
    if nombre == 'O1_LUGAR':
        est = CO.fija('lug'); return CV._MODS['O1_LUGAR'], est
    ruta = CARROS[nombre]
    if open(ruta, 'rb').read() != CC.todas()[nombre]: raise SystemExit(f"{ruta} != construye_c (correr construye_c.py)")
    m = CV._MODS.get(nombre)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{nombre}", ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[nombre] = m
    est = dict(carro=nombre, sha=h16(ruta), LUGAR=m.LUGAR, LUGAR_BARAJA=m.LUGAR_BARAJA, LUGAR_W=m.LUGAR_W)
    for k in ('COMPONE', 'PLAN', 'PLAN_BARAJA', 'PLAN_W', 'PL_LAM', 'PREGUNTA', 'PG_BARAJA', 'PG_OLVIDO'):
        if hasattr(m, k): est[k] = getattr(m, k)
    return m, est


def tarea(seed, nombre, T, mundo):
    """corre_v143.tarea tal cual con mundo_tramo_c.run en lugar de pista.run; captura la salida cruda (oasis por linaje, carro)."""
    _, est = modulo(nombre); est['mundo'] = dict(mundo)
    cap = []; orig = P.run

    def run2(*a, **k):
        r = RUN[0](*a, **dict(k, **mundo)); cap.append(r); return r
    P.run = run2
    try:
        x = CV.tarea((seed, nombre, T))
    finally:
        P.run = orig
    r = cap[0]
    for l, d in zip(x['linajes'], r['linajes']): l['_oasis'] = d['_carrera'].get('oasis')
    x['tel'] = [dict(lugar=(dict(d['carro']['lugar'], st_lg_bono=d['carro'].get('lg_bono', 0), st_lg_apr=d['carro'].get('lg_apr', 0), st_lg_viajes=d['carro'].get('lg_viajes', 0))
                            if isinstance(d.get('carro'), dict) and 'lugar' in d['carro'] else None),
                     carro={k: v for k, v in d['carro'].items() if k.startswith(('pl_', 'pg_')) or k in ('plan', 'pregunta', 'mord')} if isinstance(d.get('carro'), dict) else None)
                for d in r['linajes']]
    x['estado'] = est; x['oasis_info'] = r['pista'].get('oasis')
    return x


def fila_c(x, T, peldano):
    f = CO.fila(x, T)
    L = x['linajes']; ol = [l.get('_oasis') or {} for l in L]; oi = x.get('oasis_info') or {}
    f['oasis_info'] = {k: oi.get(k) for k in ('letra_x', 'efecto_x', 'p_x', 'cerrojo', 'd_llave', 'mueve', 'mudanzas', 'c_e')}
    if peldano == 'comp':
        s = lambda k: [sum(o['x'][k][0] for o in ol if o.get('x')), sum(o['x'][k][1] for o in ol if o.get('x'))]
        fr, fo, bi, ei, eo = s('exp_frio'), s('exp_fuera_conoce'), s('exp_b_dentro'), s('exp_dentro'), s('exp_fuera')
        c1 = fr[1] / fr[0] if fr[0] else None; p1 = 1 - fo[1] / fo[0] if fo[0] else None
        f['comp'] = dict(exp_frio=fr, exp_fuera_conoce=fo, exp_b_dentro=bi, exp_dentro=ei, exp_fuera=eo, c1=c1, p1=p1,
                         J=(round(c1 + p1 - 1, 3) if c1 is not None and p1 is not None else None),
                         b_rechazada=(round(1 - bi[1] / bi[0], 3) if bi[0] else None), mord_E=sum(o['x']['mord'] for o in ol if o.get('x')),
                         mord_E_dentro=sum(o['x']['mord_dentro'] for o in ol if o.get('x')))
    elif peldano == 'plan':
        con = sum(o['llave']['con'] for o in ol if o.get('llave')); sin = sum(o['llave']['sin'] for o in ol if o.get('llave'))
        tel = x.get('tel') or []
        f['plan'] = dict(con_llave=con, sin_llave=sin, frac_llave=(round(con / (con + sin), 3) if con + sin else None),
                         mord_K=sum(o['x']['mord'] for o in ol if o.get('x')), llaves=sum(o['llave']['llaves'] for o in ol if o.get('llave')),
                         hab_K=med([((t.get('carro') or {}).get('plan') or {}).get('hab', {}).get('K') for t in tel]),
                         pl_cred=sum(((t.get('carro') or {}).get('pl_cred') or 0) for t in tel))
    elif peldano == 'preg':
        lat = []; nunca = 0
        for o in ol:
            for j, v in enumerate((o.get('latencias') or [])[1:]):
                if v is None: nunca += 1; lat.append(T)
                else: lat.append(v)
        tel = x.get('tel') or []
        f['preg'] = dict(latencia_med=med(lat), latencias_n=len(lat), nunca=nunca, mudanzas=len(oi.get('mudanzas') or []) - 1,
                         pg_exc=sum(((t.get('carro') or {}).get('pg_exc') or 0) for t in tel), pg_olv=sum(((t.get('carro') or {}).get('pg_olv') or 0) for t in tel))
    return f


def trabajo(args):
    i, brazo, nombre, base, T, carpeta, mundo, peldano = args
    fin = os.path.join(carpeta, f"prueba_i{i:02d}_{brazo}.json"); t0 = time.time()
    try:
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=None, **fila_c(tarea(base + i, nombre, T, mundo), T, peldano))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


def lee(carpeta):
    R = {}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        R.setdefault(d['brazo'], {})[d['i']] = d
    return R, ab


def resume(R, peldano):
    B = list(R); I = sorted(set.intersection(*[set(R[b]) for b in B])) if B else []
    out = {}
    for b in B:
        xs = [R[b][i] for i in I]
        d = dict(n=len(xs), cruzan=sum(x['cruzan'] for x in xs), R0_med=med([x['R0_med'] for x in xs]), fund_media=med([st.mean(x['fund']) for x in xs]),
                 establecidos=sum(sum(int(z == 0) for z in x['fund_post10k']) for x in xs), vida_med=med([x['vida_med'] for x in xs]),
                 mundo_AC=med([x['mundo_AC'] for x in xs]), ratio_pasos_oasis=med([(x.get('oasis') or {}).get('ratio_pasos') for x in xs]))
        if peldano in xs[0] if xs else False:
            ks = xs[0][peldano].keys()
            for k in ks:
                vs = [x[peldano][k] for x in xs]
                if all(isinstance(v, (int, float)) or v is None for v in vs): d[k] = (sum(v for v in vs if v is not None) if k.startswith(('exp', 'mord', 'con', 'sin', 'llaves', 'pl_', 'pg_', 'nunca', 'latencias_n')) else med(vs))
                else: d[k] = [sum(v[j] for v in vs if v) for j in range(2)] if vs and isinstance(vs[0], list) else vs
        out[b] = d
    par = {}
    for a in B:
        for b in B:
            if a != b: par[f"{a}_vs_{b}"] = CO.par(R[a], R[b], I)
    return dict(indices=I, brazos=out, pareados=par)


def senal(res, peldano, cand, ctrl):
    B = res['brazos']
    if not all(b in B for b in (cand, ctrl, 'lug')): return 'no se lee'
    c, k, l = B[cand], B[ctrl], B['lug']
    if peldano == 'comp':
        return 'si' if (c.get('J') is not None and c['J'] >= 0.5 and (k.get('J') is None or c['J'] > k['J'] + 0.3) and (c.get('b_rechazada') or 0) >= 0.9) else 'no'
    if peldano == 'plan':
        return 'si' if (c['cruzan'] > l['cruzan'] and c['cruzan'] > k['cruzan'] and c['establecidos'] > l['establecidos'] and (c.get('frac_llave') or 0) >= 0.6) else 'no'
    if peldano == 'preg':
        return 'si' if (c.get('latencia_med') is not None and l.get('latencia_med') is not None and c['latencia_med'] < l['latencia_med']
                        and c['latencia_med'] < (k.get('latencia_med') or 1e18) and c['cruzan'] >= l['cruzan']) else 'no'
    return 'no'


def bitacora(linea):
    with open(BITACORA, 'a', encoding='utf-8') as fh: fh.write(linea + '\n')


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--peldano', choices=sorted(PELDANOS), default=None)
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--n', type=int, default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--desde', type=int, default=None); ap.add_argument('--nota', default='')
    ap.add_argument('--mueve', type=int, default=None); ap.add_argument('--d_llave', type=int, default=None); ap.add_argument('--p_x', type=float, default=None)
    ap.add_argument('--efecto_x', default=None, help='dE,dAg de la letra nueva (solo humo/explora)')
    ap.add_argument('--cerrojo_pobre', type=int, default=None, choices=[0, 1], help='p9 humo 2: 0 = sin llave el oasis vale lo nominal (no pobre)')
    ap.add_argument('--mundo_k', action='store_true', help='p9 humo 3: mundo_k (la K vieja se retira: K_VIDA pasos); solo humo/explora')
    ap.add_argument('--pool', type=int, default=0)
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool: raise SystemExit("corre_c: solo un proceso (modo rafaga)")
    if a.lee:
        R, ab = lee(os.path.abspath(a.lee)); pe = a.peldano or next((p for p in PELDANOS if p in (list(R.values())[0][min(list(R.values())[0])] if R else {})), None)
        print(json.dumps(resume(R, pe), ensure_ascii=False, indent=1)); print(f"abortos {ab}"); return 0
    if not a.peldano: raise SystemExit("--peldano comp|plan|preg")
    pe = PELDANOS[a.peldano]; modo = 'humo' if a.humo else 'explora'; cfg = HUMO if a.humo else EXPLORA
    n = a.n or cfg['n']; T = a.T or cfg['T']; brazos = tuple(a.brazos.split(',')) if a.brazos else tuple(pe['brazos']); base = a.desde or pe['sem'][modo]
    if len(brazos) * n > MAX_CORRIDAS_1P or T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(brazos) * n}) y <= {MAX_PASOS_1P} pasos (T {T})")
    for b in brazos:
        if b not in pe['brazos']: raise SystemExit(f"brazo desconocido {b} (hay {list(pe['brazos'])})")
    mundo = dict(MUNDO_C, **pe['mundo'])
    if a.mueve is not None: mundo['mueve'] = a.mueve
    if a.d_llave is not None: mundo['d_llave'] = a.d_llave
    if a.p_x is not None: mundo['p_x'] = a.p_x
    if a.efecto_x: mundo['efecto_x'] = tuple(float(z) for z in a.efecto_x.split(','))
    if a.cerrojo_pobre is not None: mundo['cerrojo_pobre'] = a.cerrojo_pobre
    if a.mundo_k:
        import mundo_k as MK
        RUN[0] = MK.run; a.nota = f"[mundo_k K_VIDA {MK.K_VIDA}] " + a.nota
    if a.explora and a.peldano == 'preg' and a.mueve is None: mundo['mueve'] = 20000
    cand, ctrl = list(pe['brazos'])[:2]
    dest = os.path.join(DATOS, f"{a.peldano}_{modo}"); pre = f"{modo}_s{base}-{base + n - 1}_T{T}"
    sel = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(dest, pre + '_' + sel)
    BUF = []; LOGF = [None]

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"
        print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    t0 = time.time()
    log(f"CORRE_C · {a.peldano} · {modo} · {sel} · python {platform.python_version()} · un proceso · corre_c.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  semillas {base}-{base + n - 1} · T {T} · brazos {list(brazos)} · mundo {mundo} · nota {a.nota!r}")
    ok = CO.verifica(log)
    s1 = h16(os.path.join(AQUI, 'corre_p1.py')); ok &= s1 == SHA_CORRE_P1; log(f"  sha corre_p1.py {s1} {'OK' if s1 == SHA_CORRE_P1 else '!= ' + SHA_CORRE_P1 + ' FALLA'}")
    for nm, b in CC.todas().items():
        igual = open(CARROS[nm], 'rb').read() == b; ok &= igual; log(f"  carro {nm} == construye_c: {igual} (sha {h16(CARROS[nm])})")
    log(f"  mundo_tramo_c: {MC.construye()[1]}")
    ok &= CO.identidad_corta(log)
    ok &= identidad_corta_c(log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    for i in range(n):
        for b in brazos:
            x = trabajo((i, b, pe['brazos'][b], base, T, carpeta, mundo, a.peldano))
            oz = x.get('oasis') or {}; ex = x.get(a.peldano) or {}
            log(f"  [{time.time()-t0:7.1f}s] i{i} {b:7s} ({x.get('seg')}s) aborto {x.get('aborto')} cruzan {x.get('cruzan')}/9 R0 {x.get('R0_med')} fund {x.get('fund')} · "
                f"oasis ratio pasos {oz.get('ratio_pasos')} · mundo AC {x.get('mundo_AC')} · {a.peldano}: {ex}")
    R, ab = lee(carpeta); res = resume(R, a.peldano)
    log(f"\n================ RESUMEN ({modo}: NO cuenta, no se declara)")
    for b, v in res['brazos'].items(): log(f"  {b:7s} {v}")
    for k, v in res['pareados'].items(): log(f"  pareado {k}: gana {v['gana']} empata {v['empata']} pierde {v['pierde']} · suma {v['suma_a']} vs {v['suma_b']}")
    sn = senal(res, a.peldano, cand, ctrl)
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, peldano=a.peldano, resumen=res, abortos=ab, n=n, T=T, brazos=list(brazos), semillas=[base, base + n - 1], mundo={k: (list(v) if isinstance(v, tuple) else v) for k, v in mundo.items()},
                       nota=a.nota, senal=sn, sha_runner=h16(os.path.abspath(__file__)), carros={k: h16(v) for k, v in CARROS.items()},
                       mundo_c=MC.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"  RESUMEN {rj} · abortos {len(ab)} · {time.time()-t0:.1f}s")
    B = res['brazos']
    cl = {b: v['cruzan'] for b, v in B.items()}; es = {b: v['establecidos'] for b, v in B.items()}
    extra = {b: {k: v[k] for k in v if k not in ('n', 'cruzan', 'R0_med', 'fund_media', 'establecidos', 'vida_med', 'mundo_AC', 'ratio_pasos_oasis')} for b, v in B.items()}
    bitacora(f"| {time.strftime('%Y-%m-%d %H:%M')} | {pe['nombre']} | {modo} s{base}-{base + n - 1} T{T} {list(brazos)} mundo {{{', '.join(f'{k}: {v}' for k, v in pe['mundo'].items())}}}"
             f"{' ' + str({k: mundo[k] for k in ('mueve', 'd_llave', 'p_x', 'efecto_x', 'cerrojo_pobre') if k in mundo and mundo[k] != pe['mundo'].get(k, 1 if k == 'cerrojo_pobre' else None)}) if any(k in mundo and mundo[k] != pe['mundo'].get(k, 1 if k == 'cerrojo_pobre' else None) for k in ('mueve', 'd_llave', 'p_x', 'efecto_x', 'cerrojo_pobre')) else ''}"
             f" {a.nota} | cruzan {cl} · establecidos {es} · R0 {{{', '.join(f'{b}: {v['R0_med']}' for b, v in B.items())}}} · fund {{{', '.join(f'{b}: {v['fund_media']}' for b, v in B.items())}}}"
             f" · ratio pasos oasis {{{', '.join(f'{b}: {v['ratio_pasos_oasis']}' for b, v in B.items())}}} · {a.peldano}: {extra} · abortos {len(ab)} · {os.path.relpath(carpeta, AQUI)} | {sn} |")
    log(f"SENAL (bitacora, no se declara): {sn}")
    return 0


def identidad_corta_c(log, seed=739955, T=1200):
    """(1) mundo_tramo_c con las perillas apagadas == mundo_escalera (salida ENTERA); (2) COMP0/PLAN0/PREG0 == O1_LUGAR en mundo_escalera."""
    N = lambda x: json.loads(json.dumps(x, default=str))
    lug, _ = modulo('O1_LUGAR')
    kw = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **CO.MUNDO_OASIS)
    base = N(ME.run(seed, [('X', lug)] * 9, **kw))
    i1 = N(MC.run(seed, [('X', lug)] * 9, **kw)) == base
    ok = i1; z = {}
    for n0 in ('O1_LUGAR_COMP0', 'O1_LUGAR_PLAN0', 'O1_LUGAR_PREG0'):
        m0, _ = modulo(n0); z[n0] = N(MC.run(seed, [('X', m0)] * 9, **kw)) == base; ok &= z[n0]
    log(f"  IDENTIDAD CORTA C (salida ENTERA, N 9, s {seed}, T {T}): mundo_tramo_c apagado == mundo_escalera {i1} · promotores 0 == O1_LUGAR {z}")
    return ok


if __name__ == '__main__':
    sys.exit(main())
