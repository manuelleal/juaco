"""corre_p2.py — RUNNER del peldano 2 de la escalera: COLONIA CLONAL PEGADA (pega) en un mundo con CUELLO que premia el tamano
(30-sep-2026, MODO RAFAGA). Mundo: mundo_colonia.py (por anclas desde generaciones/motor_convive.py). Plan: ESCALERA.md (P2).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

QUE SE CORRE: 9 linajes de O1 (carrera_escuderias/carros/O1.py, sha 99436afa2715f028, se carga por pista.carga_carro) en la PISTA v2 con
generaciones solapadas (quimiostato r 0.03*esc, fundador limpio al extinguirse, diag 0, tope 300), T pasos; por brazo:
    peg    pega 1, cuello CUELLO   EL CANDIDATO: la hija nace pegada; el grupo pasa el cuello con p_suelto / k
    sue    pega 0, cuello CUELLO   control: celulas sueltas en el mismo mundo (pasan el cuello a p_suelto)
    peg0   pega 1, cuello 0        control que puede fallar: pegarse SIN cuello (debe costar: <= base)
    base   pega 0, cuello 0        motor_convive bit a bit (arnes)
MEDIDAS (fisica): persisten (0 fundadores tras t = 10 000) por linaje; refundaciones; descendientes (partos); cuerpos vivos al final; tamano
medio del linaje (tam); colonia: tamano medio de grupo, tamano maximo, muertes por cuello (pegado / suelto), pasos pegado.
SENAL (no se declara): peg > sue en persisten y en partos con tam medio de grupo >= 2; y peg0 <= base (el mundo cobra pegarse).
SEMILLAS NUEVAS 7395xx (disjuntas de p1: 7390xx-7392xx y 7399xx): humo 739590-739595 · explora 739501-739505 · arnes 739550-739589.

  python experimentos/organelos/escalera/corre_p2.py --humo                       # 2 semillas x (peg, sue, peg0), T 30 000: 6 corridas, 1 proceso
  python experimentos/organelos/escalera/corre_p2.py --explora [--T 100000] [--n 2] [--brazos peg,sue,peg0] [--cuello 2000] [--p_suelto 0.5]
  python experimentos/organelos/escalera/corre_p2.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias'); GEN = os.path.join(RAIZ, 'experimentos', 'generaciones')
for _d in (AQUI, GEN, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import pista as P
import mundo_colonia as MCO

DATOS = os.path.join(AQUI, 'datos'); BITACORA = os.path.join(AQUI, 'BITACORA.md')
ECO = os.path.join(RAIZ, 'experimentos', 'juaco_eco')
SHAS = {os.path.join(GEN, 'motor_convive.py'): 'd10cb9021f5d0f41', os.path.join(GEN, 'pista2.py'): None,
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028', os.path.join(ECO, 'carros', 'FAMB_RES0_ECO.py'): None, os.path.join(ECO, 'motor_eco.py'): None}
CUELLO = 2000; P_SUELTO = 0.5
# REAPERTURA (30-sep, tras 3 humos sin senal con O1, que no vive en la pista v2): --carro FAMB_RES0_ECO (la celula nativa de ECO, K 31-39 en
# el mundo de 9; se carga por motor_eco.carga_eco, que solo se LEE) · --p_suelto 0.2 (cuello suave) · --solo_sueltos (el cuello solo mata
# sueltos). Semillas nuevas de la reapertura: humo 739592-739595, explora 739503-739505 (739590-739591 y 739501-739502 ya usados con O1).
CARRO = ['O1']; SOLO_SUELTOS = [0]
BRAZOS = {'peg': dict(pega=1, cuello=CUELLO), 'sue': dict(pega=0, cuello=CUELLO), 'peg0': dict(pega=1, cuello=0), 'base': dict(pega=0, cuello=0)}
ORDEN = ('peg', 'sue', 'peg0', 'base'); RAFAGA = ('peg', 'sue', 'peg0')
SEM = dict(humo=739590, explora=739501)
HUMO = dict(n=2, T=30000); EXPLORA = dict(n=2, T=100000)
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000
T_CORTE = 10000
KW = dict(pizarra=1, compat=0, rep_acum=0, escala=1, telem=True, diag=0, mundo_n=None, fundador_limpio=1, reposicion='fija')
_MOD = [None]; N_LIN = [9]


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None


def carro():
    if _MOD[0] is None:
        if CARRO[0] == 'O1': _MOD[0] = P.carga_carro('O1')
        else:
            if ECO not in sys.path: sys.path.insert(0, ECO)
            import motor_eco as MEC   # solo se LEE: carga_eco carga el carro por ruta (juaco_eco/carros)
            _MOD[0] = MEC.carga_eco(CARRO[0])
    return _MOD[0]


def ruta_carro():
    return os.path.join(PISTA, 'carros', 'O1.py') if CARRO[0] == 'O1' else os.path.join(ECO, 'carros', CARRO[0] + '.py')


def tarea(seed, brazo, T, cuello=None, p_suelto=None):
    mk = dict(BRAZOS[brazo]); mk['p_suelto'] = P_SUELTO if p_suelto is None else p_suelto; mk['reposicion'] = KW['reposicion']
    if cuello is not None and mk['cuello']: mk['cuello'] = cuello
    if SOLO_SUELTOS[0]: mk['solo_sueltos'] = 1
    t0 = time.time()
    r = MCO.run(seed, [(CARRO[0], carro())] * N_LIN[0], T=T, **dict(KW, **mk))
    return r, dict(carro=CARRO[0], sha=h16(ruta_carro()), mundo=mk, seg=round(time.time() - t0, 1))


def fila(r, est, seed, T):
    L = r['linajes']; pz = r['pista']
    fp = [sum(1 for x in d['t_fund'] if x > T_CORTE) for d in L]
    f = dict(seed=seed, T=T, fund=[d['fundadores'] for d in L], fund_post10k=fp, persisten=sum(1 for x in fp if x == 0),
             desc=[d['descendientes'] for d in L], desc_suma=sum(d['descendientes'] for d in L), deaths=[d['deaths'] for d in L],
             vivos_final=[d['vivos_final'] for d in L], tam_med=[med(d['tam']) for d in L], tam_total_final=pz['tam_total'][-1],
             max_vivos=pz['max_vivos'], bloqueados=pz['bloqueados'], nobj_medio=pz['nobj_medio'],
             comp_mundo=pz['comp_mundo'], causas={k: sum(d['_carrera']['causas'][k] for d in L) for k in ('hambre', 'sed', 'veneno', 'sal')},
             vida_med=med([v for d in L for v in d['vidas_muertos']]), estado=est, seg=est['seg'])
    co = pz.get('colonia')
    if co is not None:
        cl = [d['_carrera']['colonia'] for d in L]
        f['colonia'] = dict(info=co, tam_medio=[c['tam_medio'] for c in cl], tam_max=[c['tam_max'] for c in cl],
                            muertes_cuello=sum(c['muertes_cuello'] for c in cl), muertes_cuello_pegado=sum(c['muertes_cuello_pegado'] for c in cl),
                            grupos_fundados=sum(c['grupos_fundados'] for c in cl), pasos_pegado=sum(c['pasos_pegado'] for c in cl),
                            tam_medio_med=med([c['tam_medio'] for c in cl]))
    return f


def trabajo(args):
    i, brazo, base, T, carpeta, reanuda, cuello, p_suelto = args
    fin = os.path.join(carpeta, f"prueba_i{i:02d}_{brazo}.json")
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
    t0 = time.time()
    try:
        r, est = tarea(base + i, brazo, T, cuello, p_suelto)
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=None, **fila(r, est, base + i, T))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo='prueba', i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


def lee(carpeta):
    R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        R[d['brazo']][d['i']] = d
    return R, ab


def resume(R, brazos):
    I = sorted(set.intersection(*[set(R[b]) for b in brazos])) if brazos else []
    out = {}
    for b in brazos:
        xs = [R[b][i] for i in I]
        out[b] = dict(n=len(xs), persisten=sum(x['persisten'] for x in xs), desc_suma=sum(x['desc_suma'] for x in xs),
                      fund_media=med([st.mean(x['fund']) for x in xs]), vivos_final=med([sum(x['vivos_final']) for x in xs]),
                      max_vivos=med([x['max_vivos'] for x in xs]), bloqueados=sum(x['bloqueados'] for x in xs), vida_med=med([x['vida_med'] for x in xs]),
                      tam_grupo=med([(x.get('colonia') or {}).get('tam_medio_med') for x in xs]),
                      muertes_cuello=sum((x.get('colonia') or {}).get('muertes_cuello', 0) for x in xs),
                      muertes_cuello_pegado=sum((x.get('colonia') or {}).get('muertes_cuello_pegado', 0) for x in xs),
                      pasos_pegado=sum((x.get('colonia') or {}).get('pasos_pegado', 0) for x in xs), causas={k: sum(x['causas'][k] for x in xs) for k in ('hambre', 'sed', 'veneno', 'sal')})
    par = {}
    for a, b in (('peg', 'sue'), ('peg0', 'base'), ('peg', 'peg0'), ('sue', 'base')):
        if a in brazos and b in brazos:
            par[f"{a}_vs_{b}"] = dict(persisten=[(R[a][i]['persisten'], R[b][i]['persisten']) for i in I], desc=[(R[a][i]['desc_suma'], R[b][i]['desc_suma']) for i in I])
    return dict(indices=I, brazos=out, pareados=par)


def bitacora(linea):
    nuevo = not os.path.exists(BITACORA)
    with open(BITACORA, 'a', encoding='utf-8') as fh:
        if nuevo: fh.write("# BITACORA de la escalera\n\n| fecha | peldano | que se probo | numero | senal |\n|---|---|---|---|---|\n")
        fh.write(linea + '\n')


def identidad_corta(log, seed=739550, T=1500):
    N = lambda x: json.loads(json.dumps(x, default=str))
    import motor_convive as MC
    base = N(MC.run_solapadas(seed, [(CARRO[0], carro())] * 9, T=T, **KW))
    i1 = N(MCO.run(seed, [(CARRO[0], carro())] * 9, T=T, **KW, pega=0, cuello=0)) == base
    log(f"  IDENTIDAD CORTA (salida ENTERA, 9 {CARRO[0]}, s {seed}, T {T}): mundo pega 0 cuello 0 == motor_convive.run_solapadas {i1}")
    return i1


def identidad_corta_reapertura(log, seed=739551, T=1500):
    """(1) solo_sueltos 0 == sin la perilla (salida ENTERA, con cuello y pega); (2) solo_sueltos 1 != 0 (actua) y ningun pegado muere en el cuello;
    (3) el carro ECO (si se usa) vive en el mundo base (muertes < cuerpos nacidos: no es O1 muriendo a los 200)."""
    N = lambda x: json.loads(json.dumps(x, default=str))
    c = carro(); kw = dict(KW, pega=1, cuello=300, p_suelto=0.5)
    a = N(MCO.run(seed, [(CARRO[0], c)] * 9, T=T, **kw)); b = N(MCO.run(seed, [(CARRO[0], c)] * 9, T=T, **kw, solo_sueltos=0)); d = N(MCO.run(seed, [(CARRO[0], c)] * 9, T=T, **kw, solo_sueltos=1))
    i1 = a == b
    i2 = d != a and sum(x['_carrera']['colonia']['muertes_cuello_pegado'] for x in d['linajes']) == 0 and d['pista']['colonia']['solo_sueltos'] == 1
    log(f"  IDENTIDAD CORTA REAPERTURA (s {seed}, T {T}, {CARRO[0]}): solo_sueltos 0 == sin perilla {i1} · solo_sueltos 1 actua y 0 pegados muertos en el cuello {i2} "
        f"(muertes cuello {sum(x['_carrera']['colonia']['muertes_cuello'] for x in d['linajes'])}, pegados en el 0: {sum(x['_carrera']['colonia']['muertes_cuello_pegado'] for x in a['linajes'])})")
    return i1 and i2


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--T', type=int, default=None); ap.add_argument('--n', type=int, default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--desde', type=int, default=None); ap.add_argument('--nota', default=''); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--cuello', type=int, default=None); ap.add_argument('--p_suelto', type=float, default=None)
    ap.add_argument('--reposicion', default=None, choices=['fija', 'inmediata'])
    ap.add_argument('--n_lin', type=int, default=None); ap.add_argument('--mundo_n', type=int, default=None)   # humo 3: menos linajes en el mismo mundo (menos hacinamiento)   # solo humo/explora: el mundo base se puede mover (queda en estado y bitacora)
    ap.add_argument('--carro', default='O1', choices=['O1', 'FAMB_RES0_ECO']); ap.add_argument('--solo_sueltos', action='store_true')   # reapertura
    a = ap.parse_args(argv)
    CARRO[0] = a.carro; SOLO_SUELTOS[0] = int(a.solo_sueltos)
    if a.lee:
        R, ab = lee(os.path.abspath(a.lee)); brazos = tuple(b for b in ORDEN if R[b])
        print(json.dumps(resume(R, brazos), ensure_ascii=False, indent=1)); print(f"abortos {ab}"); return 0
    modo = 'humo' if a.humo else 'explora'; cfg = HUMO if a.humo else EXPLORA
    n = a.n or cfg['n']; T = a.T or cfg['T']; brazos = tuple(a.brazos.split(',')) if a.brazos else RAFAGA; base = a.desde or SEM[modo]
    if len(brazos) * n > MAX_CORRIDAS_1P or T > MAX_PASOS_1P:
        raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas (hay {len(brazos) * n}) y <= {MAX_PASOS_1P} pasos (T {T})")
    for b in brazos:
        if b not in BRAZOS: raise SystemExit(f"brazo desconocido {b}")
    cu = a.cuello if a.cuello is not None else CUELLO; ps = a.p_suelto if a.p_suelto is not None else P_SUELTO
    if a.reposicion: KW['reposicion'] = a.reposicion
    if a.mundo_n: KW['mundo_n'] = a.mundo_n
    if a.n_lin: N_LIN[0] = a.n_lin
    dest = os.path.join(DATOS, 'p2_' + modo); pre = f"{modo}_s{base}-{base + n - 1}_T{T}_c{cu}_p{ps}_{KW['reposicion']}_n{N_LIN[0]}m{KW['mundo_n']}_{CARRO[0]}{'_ss' if SOLO_SUELTOS[0] else ''}"
    sel = time.strftime('%Y%m%d_%H%M%S')
    prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
    if a.reanuda and not prev: raise SystemExit(f"--reanuda: no hay carpeta {pre}_* en {dest}")
    carpeta = os.path.join(dest, prev[-1]) if (a.reanuda and prev) else os.path.join(dest, pre + '_' + sel)
    BUF = []; LOGF = [None]

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"
        print(s, flush=True)
        if LOGF[0] is None: BUF.append(s)
        else: LOGF[0].write(s + '\n'); LOGF[0].flush()
    t0 = time.time()
    log(f"CORRE_P2 · {modo} · {sel} · python {platform.python_version()} · un proceso · corre_p2.py {h16(os.path.abspath(__file__))} · carpeta {carpeta}")
    log(f"  semillas {base}-{base + n - 1} · T {T} · brazos {list(brazos)} · cuello {cu} p_suelto {ps} solo_sueltos {SOLO_SUELTOS[0]} · carro {CARRO[0]} · reposicion {KW['reposicion']} · nota {a.nota!r}")
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= (sha is None or s == sha); log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if (sha is None or s == sha) else '!= ' + sha + ' FALLA'}")
    log(f"  mundo_colonia: {MCO.construye()[1]}")
    ok &= identidad_corta(log)
    if CARRO[0] != 'O1' or SOLO_SUELTOS[0]: ok &= identidad_corta_reapertura(log)
    if not ok: log("  ALGO FALLA -> no se corre."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    X = []
    for i in range(n):
        for b in brazos:
            x = trabajo((i, b, base, T, carpeta, a.reanuda, cu, ps)); X.append(x)
            co = x.get('colonia') or {}
            log(f"  [{time.time()-t0:7.1f}s] i{i} {b:4s} ({x.get('seg')}s) aborto {x.get('aborto')} persisten {x.get('persisten')}/{N_LIN[0]} fund {x.get('fund')} partos {x.get('desc_suma')} "
                f"vivos fin {x.get('tam_total_final')} max {x.get('max_vivos')} bloq {x.get('bloqueados')} · grupo tam med {co.get('tam_medio_med')} max {co.get('tam_max')} "
                f"muertes cuello {co.get('muertes_cuello')} (pegado {co.get('muertes_cuello_pegado')}) pasos pegado {co.get('pasos_pegado')} · vida {x.get('vida_med')} · causas {x.get('causas')}")
    R, ab = lee(carpeta); res = resume(R, brazos)
    log(f"\n================ RESUMEN ({modo}: NO cuenta, no se declara)")
    for b, v in res['brazos'].items(): log(f"  {b:5s} {v}")
    for k, v in res['pareados'].items(): log(f"  pareado {k}: persisten {v['persisten']} · partos {v['desc']}")
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, resumen=res, abortos=ab, n=n, T=T, brazos=list(brazos), cuello=cu, p_suelto=ps, semillas=[base, base + n - 1], nota=a.nota,
                       sha_runner=h16(os.path.abspath(__file__)), mundo=MCO.construye()[1], seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"  RESUMEN {rj} · abortos {len(ab)} · {time.time()-t0:.1f}s")
    B = res['brazos']
    def gana(a_, b_, k): return a_ in B and b_ in B and B[a_][k] > B[b_][k]
    senal = 'no se lee' if ab or not B else (
        'si' if gana('peg', 'sue', 'persisten') and gana('peg', 'sue', 'desc_suma') and (B.get('peg', {}).get('tam_grupo') or 0) >= 2
        and (('peg0' not in B or 'base' not in B) or not gana('peg0', 'base', 'persisten')) else 'no')
    bitacora(f"| {time.strftime('%Y-%m-%d %H:%M')} | p2 colonia pegada ({CARRO[0]}) | {modo} s{base}-{base + n - 1} T{T} cuello {cu} p_suelto {ps} solo_sueltos {SOLO_SUELTOS[0]} reposicion {KW['reposicion']} linajes {N_LIN[0]} mundo_n {KW['mundo_n']} {list(brazos)} {a.nota} | "
             + ' · '.join(f"{b}: persisten {v['persisten']} partos {v['desc_suma']} fund {v['fund_media']} tam grupo {v['tam_grupo']} m.cuello {v['muertes_cuello']}" for b, v in B.items())
             + f" · abortos {len(ab)} · {os.path.relpath(carpeta, AQUI)} | {senal} |")
    log(f"SENAL (bitacora): {senal}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
