"""corre_s1.py — SONDA 1 (1-oct-2026, MODO RAFAGA, EXPLORATORIA: NADA se declara): PISO Y TECHO del mundo con llave NO letal (mundo_plus).
UN proceso, <= 6 corridas, <= 200 000 pasos. Cada corrida escribe su JSON; el humo escribe resumen.json. La linea de BITACORA se escribe a mano.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y replicas).

Cada corrida ES corre_v143.tarea (se IMPORTA; regla 14: la de corre_p1 / corre_c) con mundo_plus.run en lugar de pista.run; la fila comun la arma
corre_p1.fila (CONGELADO, se importa). Mundo: MUNDO_OASIS de P1b (oasis 1, extra 0.8, pobre 0.5, dens 0.5, vista_r 20) + letra K (0, 0) a p_x 0.03,
cerrojo 0 + PERILLAS de mundo_plus.
BRAZOS:  piso   O1_LUGAR (sin modulo de secuencia)           techo  O1_LUGAR_ORAC (oraculo a mano: K si no lleva llave, luego oasis; COTA)
         azar   O1_LUGAR_AZAR (va por K por moneda, sin estado)   regalo O1_LUGAR con la llave regalada por el mundo (cota dura)
Un brazo puede llevar sus propias perillas: nombre@k=v+k=v (p. ej. piso@extra_sin=0.4, regalo@plus=0.8).
SEMILLAS NUEVAS: humo 737200-  ·  arnes 737400-
  python experimentos/organelos/escalera/sondas/corre_s1.py --identidad
  python experimentos/organelos/escalera/sondas/corre_s1.py --humo [--T 100000 --n 2 --brazos piso,techo,azar --plus 0.4 --d_plus 600 --extra_sin 0.4 --p_x 0.03 --desde 737200 --nota '...']
"""
import argparse, glob, importlib.util, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
sys.path.insert(0, ESC); sys.path.insert(0, AQUI)
import corre_c as RC             # se importa (no se toca): modulo('O1_LUGAR'), identidad_corta_c
import construye_orac as CORA
import mundo_plus as MP
CO = RC.CO; CV = RC.CV; P = RC.P; ME = RC.ME; MC = RC.MC
h16 = CO.h16; med = CO.med

DATOS = os.path.join(AQUI, 'datos')
CARROS = {n: os.path.join(AQUI, 'carros', n + '.py') for n, _ in CORA.VARIANTES}
MUNDO = dict(RC.MUNDO_C, letra_x='K', efecto_x=(0.0, 0.0), p_x=0.03, cerrojo=0)
BRAZOS = {'mixto': ('MIXTO_0', {}), 'mixto2': ('MIXTO_1', {}), 'piso': ('O1_LUGAR', {}), 'techo': ('O1_LUGAR_ORAC', {}), 'azar': ('O1_LUGAR_AZAR', {}), 'regalo': ('O1_LUGAR', dict(regalo=1))}
SEM = dict(humo=737200, arnes=737400)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000


class Mixto:
    """humo 5-6 (PISTA MIXTA): despachador PASIVO: los linajes de indice con paridad `par` son el oraculo (techo), los demas O1_LUGAR (piso)."""
    def __init__(self, a, b, par): self.a = a; self.b = b; self.par = par; self.__file__ = f'<mixto par {par}>'
    def crea(self, ctx): return (self.a if int(ctx['indice']) % 2 == self.par else self.b).crea(ctx)


def modulo(nombre):
    if nombre == 'O1_LUGAR': return RC.modulo('O1_LUGAR')
    if nombre.startswith('MIXTO_'):
        par = int(nombre[-1]); a, ea = modulo('O1_LUGAR_ORAC'); b, eb = modulo('O1_LUGAR'); CV._MODS[nombre] = Mixto(a, b, par)
        return CV._MODS[nombre], dict(carro=nombre, par=par, techo=ea, piso=eb)
    ruta = CARROS[nombre]
    if open(ruta, 'rb').read() != CORA.todas()[nombre]: raise SystemExit(f"{ruta} != construye_orac (correr construye_orac.py)")
    m = CV._MODS.get(nombre)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{nombre}", ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[nombre] = m
    return m, dict(carro=nombre, sha=h16(ruta), LUGAR=m.LUGAR, LUGAR_BARAJA=m.LUGAR_BARAJA, LUGAR_W=m.LUGAR_W, ORACULO=m.ORACULO, OR_D=m.OR_D)


def parte(tok):
    """'piso@extra_sin=0.4+plus=0.8' -> ('piso', {extra_sin: 0.4, plus: 0.8})"""
    nom, _, resto = tok.partition('@'); kv = {}
    if nom not in BRAZOS: raise SystemExit(f"brazo desconocido {nom} (hay {list(BRAZOS)})")
    for z in filter(None, resto.split('+')):
        k, v = z.split('='); kv[k] = (None if v == 'None' else (int(v) if k in ('d_plus', 'regalo', 'adelanta') else float(v)))
    return nom, kv


def tarea(seed, nombre, T, mundo, perillas):
    _, est = modulo(nombre); est['mundo'] = dict(mundo); est['perillas'] = MP.fija(**perillas)
    cap = []; orig = P.run

    def run2(*a, **k):
        r = MP.run(*a, **dict(k, **mundo)); cap.append(r); return r
    P.run = run2
    try:
        x = CV.tarea((seed, nombre, T))
    finally:
        P.run = orig; MP.fija()
    r = cap[0]
    for l, d in zip(x['linajes'], r['linajes']): l['_oasis'] = d['_carrera'].get('oasis')
    x['tel'] = [dict(lugar=(dict(d['carro']['lugar'], st_lg_bono=d['carro'].get('lg_bono', 0), st_lg_apr=d['carro'].get('lg_apr', 0), st_lg_viajes=d['carro'].get('lg_viajes', 0))
                            if isinstance(d.get('carro'), dict) and 'lugar' in d['carro'] else None),
                     carro={k: v for k, v in d['carro'].items() if k.startswith('or_') or k in ('mord', 'pruebas')} if isinstance(d.get('carro'), dict) else None)
                for d in r['linajes']]
    x['estado'] = est; x['oasis_info'] = r['pista'].get('oasis'); x['comp_mundo'] = r['pista'].get('comp_mundo')
    return x


def fila_s1(x, T):
    f = CO.fila(x, T)
    ol = [l.get('_oasis') or {} for l in x['linajes']]; n = len(ol); oi = x.get('oasis_info') or {}
    pl = [o.get('plus') or {} for o in ol]
    S = lambda k: sum(p.get(k, 0) for p in pl)
    con, sin = S('con'), S('sin')
    f['oasis_info'] = {k: oi.get(k) for k in ('letra_x', 'p_x', 'cerrojo', 'plus', 'd_plus', 'extra_sin', 'regalo', 'adelanta', 'extra', 'pobre')}
    f['plus'] = dict(con=con, sin=sin, frac_llave=(round(con / (con + sin), 4) if con + sin else None), mord_K=S('mord_K'), adel=S('adel'),
                     g_ef_1k=round(S('g_ef') / (n * T) * 1000, 4), g_nom_1k=round(S('g_nom') / (n * T) * 1000, 4),
                     plus_ef_1k=round(S('plus_ef') / (n * T) * 1000, 4), plus_nom_1k=round(S('plus_nom') / (n * T) * 1000, 4),
                     g_ef_linaje=[round(p.get('g_ef', 0) / T * 1000, 3) for p in pl],
                     or_idas=sum(((t.get('carro') or {}).get('or_idas') or 0) for t in x.get('tel') or []),
                     mundo_K=round((oi.get('comp_dentro') or {}).get('K', 0) + (oi.get('comp_fuera') or {}).get('K', 0), 4))
    f['establecidos'] = sum(int(z == 0) for z in f['fund_post10k'])
    par = (x.get('estado') or {}).get('par')
    if par is not None:
        f['roles'] = ['techo' if i % 2 == par else 'piso' for i in range(n)]
        f['con_linaje'] = [p.get('con', 0) for p in pl]; f['sin_linaje'] = [p.get('sin', 0) for p in pl]; f['mord_K_linaje'] = [p.get('mord_K', 0) for p in pl]
        f['vida_linaje'] = [l['vida_med'] for l in x['linajes']]
    return f


def trabajo(i, etq, nombre, seed, T, carpeta, mundo, perillas):
    fin = os.path.join(carpeta, f"prueba_i{i:02d}_{etq.replace('@', '_').replace('=', '').replace('+', '_')}.json"); t0 = time.time()
    try:
        x = dict(tipo='prueba', i=i, brazo=etq, aborto=None, **fila_s1(tarea(seed, nombre, T, mundo, perillas), T))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo='prueba', i=i, brazo=etq, aborto=f"{type(e).__name__}: {e}"[:300])
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


def resume(carpeta):
    R = {}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        R.setdefault(d['brazo'], {})[d['i']] = d
    out = {}
    for b, D in R.items():
        xs = [D[i] for i in sorted(D)]
        out[b] = dict(n=len(xs), linajes=9 * len(xs), cruzan=sum(x['cruzan'] for x in xs), cruzan_por_corrida=[x['cruzan'] for x in xs],
                      establecidos=sum(x['establecidos'] for x in xs), R0_med=med([x['R0_med'] for x in xs]), vida_med=med([x['vida_med'] for x in xs]),
                      fund_media=med([st.mean(x['fund']) for x in xs]), mundo_AC=med([x['mundo_AC'] for x in xs]), mundo_K=med([x['plus']['mundo_K'] for x in xs]),
                      ratio_pasos_oasis=med([(x.get('oasis') or {}).get('ratio_pasos') for x in xs]),
                      g_ef_1k=med([x['plus']['g_ef_1k'] for x in xs]), g_nom_1k=med([x['plus']['g_nom_1k'] for x in xs]),
                      plus_ef_1k=med([x['plus']['plus_ef_1k'] for x in xs]), plus_nom_1k=med([x['plus']['plus_nom_1k'] for x in xs]),
                      frac_llave=med([x['plus']['frac_llave'] for x in xs]), mord_K=sum(x['plus']['mord_K'] for x in xs),
                      con=sum(x['plus']['con'] for x in xs), sin=sum(x['plus']['sin'] for x in xs), adel=sum(x['plus'].get('adel', 0) for x in xs),
                      partos=sum(sum((z or 0) for z in (x.get('nac_reales') or [])) for x in xs), muertes=sum(sum((z or 0) for z in (x.get('muertes') or [])) for x in xs),
                      mord_AC=sum(x['mord_AC'] for x in xs), mord_BD=sum(x['mord_BD'] for x in xs))
    return dict(brazos=out), ab


def resume_mixto(carpeta):
    """pista mixta: por ROL (techo = oraculo, piso = O1_LUGAR) dentro del MISMO mundo, sumando las dos paridades."""
    A = {r: dict(n=0, cruzan=0, establecidos=0, R0=[], g_ef=[], con=0, sin=0, mord_K=0, partos=0, fund=[], vida=[]) for r in ('techo', 'piso')}; por = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_mixto*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto') or 'roles' not in d: continue
        c = {'techo': [0, 0], 'piso': [0, 0]}
        for i, r in enumerate(d['roles']):
            a = A[r]; a['n'] += 1; a['cruzan'] += d['cruza'][i]; a['establecidos'] += int(d['fund_post10k'][i] == 0); a['R0'].append(d['R0_real'][i]); a['g_ef'].append(d['plus']['g_ef_linaje'][i])
            a['con'] += d['con_linaje'][i]; a['sin'] += d['sin_linaje'][i]; a['mord_K'] += d['mord_K_linaje'][i]; a['partos'] += (d['nac_reales'][i] or 0); a['fund'].append(d['fund'][i]); a['vida'].append(d['vida_linaje'][i])
            c[r][0] += d['cruza'][i]; c[r][1] += 1
        por.append({'i': d['i'], 'brazo': d['brazo'], **{r: f"{v[0]}/{v[1]}" for r, v in c.items()}})
    out = {r: dict(n=a['n'], cruzan=a['cruzan'], frac_cruzan=(round(a['cruzan'] / a['n'], 3) if a['n'] else None), establecidos=a['establecidos'], R0_med=med(a['R0']), g_ef_1k_med=med(a['g_ef']),
                   frac_llave=(round(a['con'] / (a['con'] + a['sin']), 3) if a['con'] + a['sin'] else None), mord_K=a['mord_K'], partos=a['partos'], partos_por_linaje=(round(a['partos'] / a['n'], 1) if a['n'] else None),
                   fund_med=med(a['fund']), vida_med=med(a['vida'])) for r, a in A.items()}
    return dict(roles=out, por_corrida=por) if A['techo']['n'] else None


def identidad(log, seed=SEM['arnes'], T=1500):
    """ARNES (salida ENTERA de run, N 9, fundador limpio): lo apagado == la base bit a bit."""
    N = lambda x: json.loads(json.dumps(x, default=str))
    lug, _ = modulo('O1_LUGAR'); or0, _ = modulo('O1_LUGAR_ORAC0'); orc, _ = modulo('O1_LUGAR_ORAC'); azr, _ = modulo('O1_LUGAR_AZAR')
    kw0 = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1, **CO.MUNDO_OASIS)
    kwK = dict(kw0, letra_x='K', efecto_x=(0.0, 0.0), p_x=0.03, cerrojo=0)
    R = {}; MP.fija()
    b0 = N(MC.run(seed, [('X', lug)] * 9, **kw0)); bK = N(MC.run(seed, [('X', lug)] * 9, **kwK))
    R['M1 mundo_plus apagado, sin letra == mundo_tramo_c'] = N(MP.run(seed, [('X', lug)] * 9, **kw0)) == b0
    R['M2 mundo_plus apagado, con K == mundo_tramo_c con K'] = N(MP.run(seed, [('X', lug)] * 9, **kwK)) == bK
    R['M3 ORAC0 == O1_LUGAR (mundo_tramo_c con K)'] = N(MC.run(seed, [('X', or0)] * 9, **kwK)) == bK
    MP.fija(plus=0.4)
    p1 = N(MP.run(seed, [('X', lug)] * 9, **kwK)); R['M4 ORAC0 == O1_LUGAR (mundo_plus plus 0.4)'] = N(MP.run(seed, [('X', or0)] * 9, **kwK)) == p1
    R['E1 plus 0.4 ENCIENDE (difiere de apagado)'] = p1 != bK
    MP.fija(regalo=1); pr = N(MP.run(seed, [('X', lug)] * 9, **kwK)); R['E2 regalo ENCIENDE (difiere de apagado)'] = pr != bK
    MP.fija(extra_sin=0.4); pe = N(MP.run(seed, [('X', lug)] * 9, **kwK)); R['E3 extra_sin 0.4 ENCIENDE'] = pe != bK
    MP.fija(regalo=1, adelanta=250); R['E6 adelanta 250 ENCIENDE (difiere de regalo solo)'] = N(MP.run(seed, [('X', lug)] * 9, **kwK)) != pr
    MP.fija(extra_sin=0.8); R['M5 extra_sin 0.8 (= extra) y plus 0: fisica == apagado (salvo telemetria plus)'] = _sin_plus(N(MP.run(seed, [('X', lug)] * 9, **kwK))) == _sin_plus(bK)
    MP.fija(plus=0.4)
    po = N(MP.run(seed, [('X', orc)] * 9, **kwK)); pa = N(MP.run(seed, [('X', azr)] * 9, **kwK))
    R['E4 ORAC ENCIENDE (difiere de O1_LUGAR)'] = po != p1; R['E5 AZAR ENCIENDE y difiere de ORAC'] = pa != p1 and pa != po
    R['R1 ORAC repetido == ORAC (determinista)'] = N(MP.run(seed, [('X', orc)] * 9, **kwK)) == po
    MP.fija()
    MP.fija(plus=0.4); mxa, _ = modulo('MIXTO_0'); pm = N(MP.run(seed, [('X', mxa)] * 9, **kwK))
    R['X1 pista mixta: difiere de todo-piso y de todo-techo'] = pm != p1 and pm != po
    R['X2 pista mixta con los dos roles = O1_LUGAR == todo O1_LUGAR (el despachador es pasivo)'] = N(MP.run(seed, [('X', Mixto(lug, lug, 0))] * 9, **kwK)) == p1
    MP.fija()
    R['M6 tras fija(): otra vez == mundo_tramo_c con K'] = N(MP.run(seed, [('X', lug)] * 9, **kwK)) == bK
    ok = all(R.values())
    for k, v in R.items(): log(f"  {'OK   ' if v else 'FALLA'} {k}")
    kk = lambda r: (sum((d['_carrera']['oasis'].get('plus') or {}).get('mord_K', 0) for d in r['linajes']), sum((d['_carrera']['oasis'].get('plus') or {}).get('con', 0) for d in r['linajes']))
    log(f"  (mord_K, bocados con llave) en T {T}: O1_LUGAR {kk(p1)} · ORAC {kk(po)} · AZAR {kk(pa)} · regalo {kk(pr)}")
    log(f"  ARNES SONDA 1: {sum(R.values())}/{len(R)} {'TODO OK' if ok else 'FALLA'} (s {seed}, T {T})")
    return ok


def _sin_plus(r):
    for d in r['linajes']: d['_carrera']['oasis'].pop('plus', None)
    for k in ('plus', 'd_plus', 'extra_sin', 'regalo', 'adelanta'): r['pista']['oasis'].pop(k, None)
    return r


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--identidad', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--T', type=int, default=100000); ap.add_argument('--n', type=int, default=2); ap.add_argument('--brazos', default='piso,techo,azar')
    ap.add_argument('--desde', type=int, default=SEM['humo']); ap.add_argument('--nota', default='')
    ap.add_argument('--plus', type=float, default=0.4); ap.add_argument('--d_plus', type=int, default=600); ap.add_argument('--extra_sin', type=float, default=None)
    ap.add_argument('--p_x', type=float, default=None); ap.add_argument('--adelanta', type=int, default=0)
    a = ap.parse_args(argv)
    if a.lee:
        res, ab = resume(os.path.abspath(a.lee)); print(json.dumps(res, ensure_ascii=False, indent=1)); print(f"abortos {ab}"); return 0
    BUF = []; LOGF = [None]

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    t0 = time.time()
    log(f"CORRE_S1 (sonda 1: piso y techo, llave no letal) · python {platform.python_version()} · un proceso · corre_s1.py {h16(os.path.abspath(__file__))}")
    ok = CO.verifica(log)
    for nm, b in CORA.todas().items():
        igual = open(CARROS[nm], 'rb').read() == b; ok &= igual; log(f"  carro {nm} == construye_orac: {igual} (sha {h16(CARROS[nm])})")
    log(f"  mundo_plus: {MP.construye()[1]} · mundo_plus.py {h16(os.path.join(AQUI, 'mundo_plus.py'))}")
    ok &= CO.identidad_corta(log); ok &= RC.identidad_corta_c(log); ok &= identidad(log)
    if a.identidad or not ok:
        if not ok: log("  ALGO FALLA -> no se corre.")
        return 0 if ok else 1
    toks = [parte(z) for z in a.brazos.split(',')]
    if len(toks) * a.n > MAX_CORRIDAS_1P or a.T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(toks) * a.n}) y <= {MAX_PASOS_1P} pasos")
    mundo = dict(MUNDO)
    if a.p_x is not None: mundo['p_x'] = a.p_x
    base_per = dict(plus=a.plus, d_plus=a.d_plus, extra_sin=a.extra_sin, adelanta=a.adelanta)
    sel = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 's1_humo', f"humo_s{a.desde}-{a.desde + a.n - 1}_T{a.T}_{sel}")
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    log(f"  semillas {a.desde}-{a.desde + a.n - 1} · T {a.T} · brazos {a.brazos} · mundo {mundo} · perillas base {base_per} · nota {a.nota!r} · carpeta {carpeta}")
    for i in range(a.n):
        for (nom, kv), tok in zip(toks, a.brazos.split(',')):
            per = dict(base_per, **BRAZOS[nom][1]); per.update(kv)
            x = trabajo(i, tok, BRAZOS[nom][0], a.desde + i, a.T, carpeta, mundo, per)
            log(f"  [{time.time()-t0:7.1f}s] i{i} {tok:22s} ({x.get('seg')}s) aborto {x.get('aborto')} cruzan {x.get('cruzan')}/9 estab {x.get('establecidos')} R0 {x.get('R0_med')} vida {x.get('vida_med')} "
                f"fund {x.get('fund')} · ratio oasis {(x.get('oasis') or {}).get('ratio_pasos')} · mundo AC {x.get('mundo_AC')} · plus {({k: v for k, v in (x.get('plus') or {}).items() if k != 'g_ef_linaje'})}")
    res, ab = resume(carpeta)
    log("\n================ RESUMEN (humo: NO cuenta, no se declara)")
    for b, v in res['brazos'].items(): log(f"  {b:22s} {v}")
    mx = resume_mixto(carpeta); res['mixto'] = mx
    if mx:
        for r, v in mx['roles'].items(): log(f"  [mixta] {r:6s} {v}")
        log(f"  [mixta] por corrida (cruzan/linajes): {mx['por_corrida']}")
    with open(os.path.join(carpeta, 'resumen.json'), 'w', encoding='utf-8') as fh:
        json.dump(dict(sonda=1, resumen=res, abortos=ab, n=a.n, T=a.T, brazos=a.brazos, semillas=[a.desde, a.desde + a.n - 1],
                       mundo={k: (list(v) if isinstance(v, tuple) else v) for k, v in mundo.items()}, perillas_base=base_per, nota=a.nota,
                       sha_runner=h16(os.path.abspath(__file__)), sha_mundo_plus=h16(os.path.join(AQUI, 'mundo_plus.py')), carros={k: h16(v) for k, v in CARROS.items()},
                       mundo_plus=MP.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"  RESUMEN {os.path.join(carpeta, 'resumen.json')} · abortos {len(ab)} · {time.time()-t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
