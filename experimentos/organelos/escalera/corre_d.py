"""corre_d.py — RUNNER DE RAFAGA del TRAMO D ("sexo y familia": D1 reproduccion de a dos, D2 eleccion de pareja, D3 inversion parental,
D4 reduccion de camada) con la celula nativa de ECO (FAMB_RES0_ECO) en mundo_familia (motor_eco por anclas). 30-sep-2026, Fable, MODO RAFAGA:
solo --humo / --explora de UN proceso; NADA se declara; JSON por corrida, resumen y UNA linea en BITACORA.md. Plan: ESCALERA.md (tramo D).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

MUNDO (todos los brazos): ECO de 9 fundadores FAMB_RES0_ECO en el mundo de 9 (L 360, 36 objetos, quimiostato r 0.03*9), diag 0, tope 300,
eco = dict(refunda 1, t_corte T/2 (vivero: hasta ahi el mundo repone fundadores desde el banco; despues nadie), p_mut 0.05, sigma 0.15,
banco 50, cada_gen T/20): el esquema de ECO_SEL. familia = la perilla del peldano.
PELDANOS (--peldano) y brazos (candidato, control, base):
  d1  sexo (sexo 1, recombina 1, pareja azar) · clon (sexo 1, recombina 0: pareja obligatoria, hijo = madre) · base (familia None = ECO)
  d2  fuerte (sexo 1, recombina 1, pareja fuerte) · azar (= sexo de d1) · base
  d3  dote (sexo 1, recombina 1, dote_doble 1) · sexo · base
  d4  camada (camada 1, a_quien padre) · base
MEDIDAS (fisica): persiste (vivos en T tras el corte), vivos_T, K_post (media de cuerpos vivos tras el corte), partos, NIETOS (cuerpos de
generacion >= 2; y los nacidos tras el corte), sin_pareja, trofico, rumbo de los genes (media de |log(g/G0)| en la ultima muestra de gen_t),
causas de muerte. SENAL (no se declara): candidato > control en persiste o nietos (pareado), con el mecanismo > 0.
SEMILLAS NUEVAS 7392xx (disjuntas de la exploracion de P1 739201-739206): humo 739290-739295 · explora 739250-739255 · arnes 739280-739289.
  python experimentos/organelos/escalera/corre_d.py --peldano d1 --humo [--T 50000 --n 2 --brazos sexo,clon,base --r_par 10 --nota '...']
  python experimentos/organelos/escalera/corre_d.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, os, platform, statistics as st, sys, time
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path.insert(0, AQUI)
import mundo_familia as MF
MEC = MF.MEC

DATOS = os.path.join(AQUI, 'datos'); BITACORA = os.path.join(AQUI, 'BITACORA.md')
CARRO = 'FAMB_RES0_ECO'; ESC = 9; N_LIN = 9; TOPE = 300; MUESTRA = 100
SEXO = dict(sexo=1, recombina=1, pareja='azar')
PELDANOS = {
    'd1': dict(brazos={'sexo': SEXO, 'clon': dict(sexo=1, recombina=0, pareja='azar'), 'base': None}, nombre='d1 reproduccion de a dos (recombinacion)'),
    'd2': dict(brazos={'fuerte': dict(sexo=1, recombina=1, pareja='fuerte'), 'azar': SEXO, 'base': None}, nombre='d2 eleccion de pareja (fuerte vs azar)'),
    'd3': dict(brazos={'dote': dict(SEXO, dote_doble=1), 'sexo': SEXO, 'base': None}, nombre='d3 inversion parental (dote doble)'),
    'd4': dict(brazos={'camada': dict(camada=1, a_quien='padre'), 'base': None}, nombre='d4 reduccion de camada'),
}
SEM = dict(humo=739290, explora=739250)
HUMO = dict(n=2, T=50000); EXPLORA = dict(n=2, T=150000)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None


def eco_cfg(T): return dict(refunda=1, t_corte=T // 2, p_mut=0.05, sigma=0.15, banco=50, cada_gen=max(1000, T // 20), n_sombra=0)


def tarea(seed, fam, T, extra=None):
    f = None if fam is None else dict(fam, **(extra or {}))
    t0 = time.time()
    r = MF.run(seed, [CARRO] * N_LIN, T=T, diag=0, mundo_n=ESC, tope_cuerpos=TOPE, muestra=MUESTRA, eco=eco_cfg(T), familia=f)
    return r, dict(carro=CARRO, familia=f, eco=eco_cfg(T), seg=round(time.time() - t0, 1))


def fila(r, est, seed, T):
    L = r['linajes']; pz = r['pista']; E = r['eco']; tc = E['t_corte']
    tt = pz['tam_total']; post = [v for j, v in enumerate(tt) if j * MUESTRA >= tc]
    ind = [row for d in L for row in d['individuos']]
    nietos = sum(1 for row in ind if row[1] >= 2); nietos_post = sum(1 for row in ind if row[1] >= 2 and row[3] >= tc)
    g = E['gen_t'][-1] if E['gen_t'] else None
    rumbo = (round(float(np.mean(np.abs(g[4]))), 4) if g and g[4] else None)
    f = dict(seed=seed, T=T, t_corte=tc, t_ext=E['t_ext'], persiste=int(E['t_ext'] is None and len(E['vivos_final']) > 0), vivos_T=len(E['vivos_final']),
             K_post=(round(float(np.mean(post)), 2) if post else None), max_vivos=pz['max_vivos'], bloqueados=pz['bloqueados'], partos=sum(d['descendientes'] for d in L),
             nietos=nietos, nietos_post=nietos_post, fund=[d['fundadores'] for d in L], n_refund=E['n_refund'], nobj_medio=pz['nobj_medio'],
             causas={k: sum(d['_carrera']['causas'][k] for d in L) for k in ('hambre', 'sed', 'veneno', 'sal')},
             vida_med=med([v for d in L for v in d['vidas_muertos']]), rumbo=rumbo, gen_ult=(g[4] if g else None), estado=est, seg=est['seg'])
    fa = pz.get('familia')
    if fa is not None:
        fl = [d['_carrera']['familia'] for d in L]
        f['familia'] = dict(info=fa, sin_pareja=sum(x['sin_pareja'] for x in fl), con_pareja=sum(x['con_pareja'] for x in fl), recomb=sum(x['recombinaciones'] for x in fl),
                            pagos=sum(x['pagos_dobles'] for x in fl), trofico=sum(x['trofico'] for x in fl), fuerza=med([x['fuerza_pareja_media'] for x in fl]),
                            tipos=[sum(x['tipos_nacidos'][0] for x in fl), sum(x['tipos_nacidos'][1] for x in fl)])
    return f


def trabajo(args):
    i, brazo, fam, base, T, carpeta, extra = args
    fin = os.path.join(carpeta, f"prueba_i{i:02d}_{brazo}.json"); t0 = time.time()
    try:
        r, est = tarea(base + i, fam, T, extra)
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=None, **fila(r, est, base + i, T))
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


def resume(R):
    B = list(R); I = sorted(set.intersection(*[set(R[b]) for b in B])) if B else []
    out = {}
    for b in B:
        xs = [R[b][i] for i in I]
        out[b] = dict(n=len(xs), persisten=sum(x['persiste'] for x in xs), vivos_T=med([x['vivos_T'] for x in xs]), K_post=med([x['K_post'] for x in xs]),
                      partos=sum(x['partos'] for x in xs), nietos=sum(x['nietos'] for x in xs), nietos_post=sum(x['nietos_post'] for x in xs),
                      rumbo=med([x['rumbo'] for x in xs]), vida_med=med([x['vida_med'] for x in xs]), nobj=med([x['nobj_medio'] for x in xs]),
                      causas={k: sum(x['causas'][k] for x in xs) for k in ('hambre', 'sed', 'veneno', 'sal')},
                      **({k: sum(x['familia'][k] for x in xs) for k in ('sin_pareja', 'con_pareja', 'recomb', 'pagos', 'trofico')} if xs and xs[0].get('familia') else {}))
    par = {}
    for a in B:
        for b in B:
            if a != b:
                par[f"{a}_vs_{b}"] = dict(persiste=[(R[a][i]['persiste'], R[b][i]['persiste']) for i in I], nietos=[(R[a][i]['nietos'], R[b][i]['nietos']) for i in I],
                                          K_post=[(R[a][i]['K_post'], R[b][i]['K_post']) for i in I])
    return dict(indices=I, brazos=out, pareados=par)


def senal(res, cand, ctrl):
    B = res['brazos']
    if cand not in B or ctrl not in B: return 'no se lee'
    c, k = B[cand], B[ctrl]
    mec = {'sexo': 'recomb', 'fuerte': 'con_pareja', 'dote': 'pagos', 'camada': 'trofico'}.get(cand)
    if mec and not c.get(mec): return 'no (el mecanismo no actua)'
    return 'si' if (c['persisten'] > k['persisten'] or (c['persisten'] == k['persisten'] and c['nietos'] > k['nietos'] * 1.1)) else 'no'


def bitacora(linea):
    with open(BITACORA, 'a', encoding='utf-8') as fh: fh.write(linea + '\n')


def identidad_corta(log, seed=739280, T=600):
    """familia None == motor_eco (salida ENTERA, con eco); familia con todo apagado (sexo 0, camada 0) == motor_eco tambien."""
    N = lambda x: json.loads(json.dumps(x, default=str))
    kw = dict(T=T, diag=0, mundo_n=ESC, tope_cuerpos=TOPE, muestra=MUESTRA, eco=eco_cfg(T))
    base = N(MEC.run_solapadas(seed, [CARRO] * N_LIN, **kw))
    i1 = N(MF.run(seed, [CARRO] * N_LIN, **kw)) == base
    r0 = N(MF.run(seed, [CARRO] * N_LIN, **kw, familia=dict(sexo=0, camada=0)))
    for d in r0['linajes']: d['_carrera'].pop('familia', None)
    r0['pista'].pop('familia', None)
    i2 = r0 == base
    log(f"  IDENTIDAD CORTA D (salida ENTERA, 9 {CARRO}, s {seed}, T {T}): familia None == motor_eco {i1} · familia apagada == motor_eco (salvo su telemetria) {i2}")
    return i1 and i2


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--peldano', choices=sorted(PELDANOS), default=None)
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--n', type=int, default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--desde', type=int, default=None); ap.add_argument('--nota', default='')
    ap.add_argument('--r_par', type=int, default=None); ap.add_argument('--u_cam', type=float, default=None); ap.add_argument('--pool', type=int, default=0)
    a = ap.parse_args(argv)
    if a.pool: raise SystemExit("corre_d: solo un proceso (modo rafaga)")
    if a.lee:
        R, ab = lee(os.path.abspath(a.lee)); print(json.dumps(resume(R), ensure_ascii=False, indent=1)); print(f"abortos {ab}"); return 0
    if not a.peldano: raise SystemExit("--peldano d1|d2|d3|d4")
    pe = PELDANOS[a.peldano]; modo = 'humo' if a.humo else 'explora'; cfg = HUMO if a.humo else EXPLORA
    n = a.n or cfg['n']; T = a.T or cfg['T']; brazos = tuple(a.brazos.split(',')) if a.brazos else tuple(pe['brazos']); base = a.desde or SEM[modo]
    if len(brazos) * n > MAX_CORRIDAS_1P or T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(brazos) * n}) y <= {MAX_PASOS_1P} pasos (T {T})")
    for b in brazos:
        if b not in pe['brazos']: raise SystemExit(f"brazo desconocido {b} (hay {list(pe['brazos'])})")
    extra = {}
    if a.r_par is not None: extra['r_par'] = a.r_par
    if a.u_cam is not None: extra['u_cam'] = a.u_cam
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
    log(f"CORRE_D · {a.peldano} · {modo} · {sel} · python {platform.python_version()} · un proceso · corre_d.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  semillas {base}-{base + n - 1} · T {T} · brazos {list(brazos)} · familia {pe['brazos']} extra {extra} · eco {eco_cfg(T)} · nota {a.nota!r}")
    log(f"  mundo_familia: {MF.construye()[1]} · carro {CARRO} sha {h16(os.path.join(MF.ECO_D, 'carros', CARRO + '.py'))}")
    if not identidad_corta(log): log("  ALGO FALLA -> no se corre."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    for i in range(n):
        for b in brazos:
            x = trabajo((i, b, pe['brazos'][b], base, T, carpeta, extra if pe['brazos'][b] is not None else None))
            fa = x.get('familia') or {}
            log(f"  [{time.time()-t0:7.1f}s] i{i} {b:6s} ({x.get('seg')}s) aborto {x.get('aborto')} persiste {x.get('persiste')} vivos_T {x.get('vivos_T')} K_post {x.get('K_post')} "
                f"partos {x.get('partos')} nietos {x.get('nietos')} (post {x.get('nietos_post')}) refund {x.get('n_refund')} rumbo {x.get('rumbo')} vida {x.get('vida_med')} · "
                f"familia: sin_pareja {fa.get('sin_pareja')} con {fa.get('con_pareja')} recomb {fa.get('recomb')} pagos {fa.get('pagos')} trofico {fa.get('trofico')} tipos {fa.get('tipos')} · causas {x.get('causas')}")
    R, ab = lee(carpeta); res = resume(R)
    log(f"\n================ RESUMEN ({modo}: NO cuenta, no se declara)")
    for b, v in res['brazos'].items(): log(f"  {b:6s} {v}")
    for k, v in res['pareados'].items(): log(f"  pareado {k}: persiste {v['persiste']} · nietos {v['nietos']} · K_post {v['K_post']}")
    sn = senal(res, cand, ctrl)
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, peldano=a.peldano, resumen=res, abortos=ab, n=n, T=T, brazos=list(brazos), semillas=[base, base + n - 1], familia=pe['brazos'], extra=extra,
                       eco=eco_cfg(T), nota=a.nota, senal=sn, sha_runner=h16(os.path.abspath(__file__)), mundo=MF.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"  RESUMEN {rj} · abortos {len(ab)} · {time.time()-t0:.1f}s")
    B = res['brazos']
    bitacora(f"| {time.strftime('%Y-%m-%d %H:%M')} | {pe['nombre']} ({CARRO}, ECO) | {modo} s{base}-{base + n - 1} T{T} {list(brazos)} {extra or ''} {a.nota} | "
             + ' · '.join(f"{b}: persisten {v['persisten']} vivos_T {v['vivos_T']} K_post {v['K_post']} partos {v['partos']} nietos {v['nietos']} rumbo {v['rumbo']}"
                          + (f" sin_pareja {v['sin_pareja']} con {v['con_pareja']} recomb {v['recomb']} pagos {v['pagos']} trofico {v['trofico']}" if 'sin_pareja' in v else '') for b, v in B.items())
             + f" · abortos {len(ab)} · {os.path.relpath(carpeta, AQUI)} | {sn} |")
    log(f"SENAL (bitacora, no se declara): {sn}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
