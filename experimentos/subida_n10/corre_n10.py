"""corre_n10.py — SUBIDA DEL NIVEL 10: "la familia que se sostiene por lo que se transmite" (PREREGISTRO_n10.md).

MISION: llegar a la AGI por este camino.

Mundo: pista v2 de generaciones que conviven (experimentos/generaciones/pista2.py, solapadas=1, quimiostato 'fija', r_rep 0.03,
tope 300), SIN CAMBIOS. Organismo: FABRICA (mitad cerebro del brazo REL de organismo_f9c) en cuatro variantes construidas por
anclas (construye_familia.py; arnes identidad_familia.py 26/26):
  NADA (== FABRICA) · PARTO (candidato: el nodo viaja en el parto) · BAR (contenido barajado) · ORACULO (tabla verdadera, techo).
Brazos: monocultivos de 9 fundadores de cada variante + MIX (3 NADA + 3 PARTO + 3 BAR en el MISMO mundo).
Medidas SOLO desde la fisica (ERR-96): resumen_linaje del juez v2 (corre_convive.py, sha fijado; se IMPORTA, no se copia) +
lo propio de esta pregunta: tamano del carro (cuerpos vivos, t >= T/2), nacimientos, R0 de los NACIDOS (no fundadores, cohorte
t <= T/2), vida de nacidos y de fundadores, causas de muerte de los nacidos. Veredicto por la letra del PREREGISTRO_n10.md sec. 6.

Uso:
  humo (un proceso, sin Pool):  python experimentos/subida_n10/corre_n10.py --humo            (semilla 12391, T=20000, 5 brazos)
  identidad:                    python experimentos/subida_n10/identidad_familia.py            (26/26 antes de todo)
  serie (coordinador):          python experimentos/subida_n10/corre_n10.py --serie --desde 12301 --n 20 --pool 6
  replica (coordinador):        python experimentos/subida_n10/corre_n10.py --serie --desde 12321 --n 20 --pool 6
"""
import argparse, gzip, hashlib, importlib.util, json, math, os, platform, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
GEN = os.path.join(RAIZ, 'experimentos', 'generaciones')
sys.path.insert(0, GEN); sys.path.insert(0, AQUI)
import pista2 as P2
import motor_convive as MC
import corre_convive as JV   # juez v2: resumen_linaje (se importa; sha fijado)

SHAS = {os.path.join(GEN, 'pista2.py'): '4d2bee16e7961261', os.path.join(GEN, 'motor_convive.py'): 'd10cb9021f5d0f41',
        os.path.join(GEN, 'corre_convive.py'): 'e6dadfdad9c379cd',
        os.path.join(RAIZ, 'experimentos', 'carrera_escuderias', 'carros', 'FABRICA.py'): '2ebee3e99ea5a33a',
        os.path.join(AQUI, 'carros', 'FAMILIA_NADA.py'): 'f7ae98715f170153',
        os.path.join(AQUI, 'carros', 'FAMILIA_PARTO.py'): 'e8aeb6efd6307162',
        os.path.join(AQUI, 'carros', 'FAMILIA_BAR.py'): '46c09162e6d1ab55',
        os.path.join(AQUI, 'carros', 'FAMILIA_ORACULO.py'): '55df592f57671b54'}
MONO = ('NADA', 'PARTO', 'BAR', 'ORACULO')
BRAZOS = MONO + ('MIX',)
MIX = ['NADA'] * 3 + ['PARTO'] * 3 + ['BAR'] * 3
SEMILLAS = dict(practica=(12391, 12399), serie=(12301, 12320), replica=(12321, 12340))
T_DEF = 100000
DATOS = os.path.join(AQUI, 'datos')
PARES = (('PARTO', 'NADA'), ('PARTO', 'BAR'), ('BAR', 'NADA'), ('ORACULO', 'PARTO'), ('ORACULO', 'NADA'))
PARES_MIX = (('PARTO', 'NADA'), ('PARTO', 'BAR'), ('BAR', 'NADA'))


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica_shas():
    mal = {os.path.basename(p): (h16(p), s) for p, s in SHAS.items() if h16(p) != s}
    if mal: raise SystemExit(f"corre_n10: sha cambiado {mal} (reconstruir y volver a correr identidad_familia.py)")


def carga(et):
    p = os.path.join(AQUI, 'carros', f'FAMILIA_{et}.py')
    spec = importlib.util.spec_from_file_location(f'carro_FAMILIA_{et}', p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def media(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 4) if xs else None


def tarea(args):
    seed, brazo, T = args
    t0 = time.time()
    mods = {et: carga(et) for et in MONO}
    al = [(f'FAMILIA_{e}', mods[e]) for e in MIX] if brazo == 'MIX' else [(f'FAMILIA_{brazo}', mods[brazo])] * 9
    r = P2.run(seed, al, T=T, diag=0, solapadas=1, reposicion='fija', tope_cuerpos=MC.TOPE_DEF, r_rep=MC.R_REP)
    ps = r['pista']; mu = ps['muestra']; i2 = (T // 2) // mu; tc = T // 2
    L = [JV.resumen_linaje(d, T, mu) for d in r['linajes']]
    estr = {}
    for e in sorted(set(l['etiqueta'] for l in L)):
        ix = [j for j, l in enumerate(L) if l['etiqueta'] == e]
        serie = [sum(r['linajes'][j]['tam'][m] for j in ix) for m in range(len(r['linajes'][0]['tam']))]
        ind = [x for j in ix for x in r['linajes'][j]['individuos']]   # [k, gen, padre, t_nace, t_muere, hijos, fundador, causa, vol]
        nac = [x for x in ind if not x[6]]; fun = [x for x in ind if x[6]]
        coh = [x for x in nac if x[3] <= tc]
        mn = [x for x in nac if x[4] >= 0]; mf = [x for x in fun if x[4] >= 0]
        cau = {c: sum(1 for x in mn if x[7] == ic) for ic, c in enumerate(MC.CAUSAS)}   # la pista guarda la causa como INDICE de MC.CAUSAS
        estr[e.replace('FAMILIA_', '')] = dict(
            tam_carro=media(serie[i2:-1] if len(serie) > i2 + 1 else serie), tam_final=serie[-1],
            exceso=(round(media(serie[i2:-1] if len(serie) > i2 + 1 else serie) - len(ix), 4)),   # cuerpos por encima de 1 por linaje
            nac=sum(L[j]['nac'] for j in ix), fundadores=sum(L[j]['fundadores'] for j in ix),
            linajes_sin_ext=sum(L[j]['sin_extincion'] for j in ix), persisten=sum(L[j]['persiste'] for j in ix), n_lin=len(ix),
            persiste_carro=any(L[j]['sin_extincion'] for j in ix),
            R0_nacidos=media([x[5] for x in coh]), n_coh_nacidos=len(coh),
            cens_nacidos=(round(sum(1 for x in coh if x[4] < 0) / len(coh), 4) if coh else None),
            R0_fund=media([x[5] for x in fun if x[3] <= tc]),
            vida_nacidos=med([x[4] - x[3] for x in mn]), vida_fund=med([x[4] - x[3] for x in mf]),
            frac_mala_nacidos=(round((cau['veneno'] + cau['sal']) / len(mn), 4) if mn else None), causas_nacidos=cau,
            gen_max=max((L[j]['gen_max'] for j in ix), default=0), bloqueados=sum(L[j]['bloqueados'] for j in ix))
    crudo = [dict(individuos=d['individuos'], tam=d['tam'], t_fund=d['t_fund'], carro_n10=d.get('carro', {}).get('n10')) for d in r['linajes']]
    return dict(seed=seed, brazo=brazo, T=T, seg=round(time.time() - t0, 1), estr=estr, linajes=L, crudo=crudo,
                pista={k: v for k, v in ps.items() if k not in ('pizarra_final',)})


def signo(g, p):
    n = g + p
    if n == 0: return 1.0
    k = min(g, p)
    return round(min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n), 5)


def pareado(R, a, b, clave, brazo_a=None, brazo_b=None, mix=False):
    """por semilla: clave de a contra b. En monocultivo, a y b son brazos; en MIX, estrategias dentro de la misma corrida."""
    xs = []
    for s in sorted({c['seed'] for c in R}):
        if mix:
            c = [c for c in R if c['seed'] == s and c['brazo'] == 'MIX']
            if not c: continue
            va, vb = c[0]['estr'][a][clave], c[0]['estr'][b][clave]
        else:
            ca = [c for c in R if c['seed'] == s and c['brazo'] == a]; cb = [c for c in R if c['seed'] == s and c['brazo'] == b]
            if not ca or not cb: continue
            va, vb = ca[0]['estr'][a][clave], cb[0]['estr'][b][clave]
        if va is None or vb is None: continue
        xs.append(va - vb)
    g = sum(1 for d in xs if d > 0); p = sum(1 for d in xs if d < 0); e = len(xs) - g - p
    return dict(par=f"{a}-{b}", clave=clave, n=len(xs), gana=g, pierde=p, empata=e, dif_med=med(xs), p_signo=signo(g, p))


def agrega(R):
    A = {}
    for b in MONO:
        cs = [c['estr'][b] for c in R if c['brazo'] == b]
        if not cs: continue
        A[b] = {k: med([c[k] for c in cs]) for k in ('tam_carro', 'exceso', 'nac', 'fundadores', 'linajes_sin_ext', 'persisten', 'R0_nacidos',
                                                    'R0_fund', 'vida_nacidos', 'vida_fund', 'frac_mala_nacidos', 'gen_max')}
        A[b]['semillas'] = len(cs); A[b]['persiste_carro'] = sum(c['persiste_carro'] for c in cs)
        A[b]['bloqueados'] = sum(c['bloqueados'] for c in cs)
        A[b]['sem_R0nac_ge_090'] = sum(1 for c in cs if c['R0_nacidos'] is not None and c['R0_nacidos'] >= 0.90)   # P4b (informativo)
    P = [pareado(R, a, b, k) for a, b in PARES for k in ('R0_nacidos', 'vida_nacidos', 'exceso', 'nac', 'gen_max')]
    PM = [pareado(R, a, b, k, mix=True) for a, b in PARES_MIX for k in ('R0_nacidos', 'exceso', 'nac')]
    return A, P, PM


def veredicto(A, P, PM, n_sem):
    """PREREGISTRO_n10.md sec. 6 (por la letra). Umbral pareado: >= 15/20 (fraccion 0.75 si n != 20). Medida que decide:
    R0_nacidos = hijos por cuerpo NACIDO (no fundador) de la cohorte t <= T/2, pareado por semilla."""
    need = math.ceil(0.75 * n_sem)
    g = lambda lst, par, k: next((x for x in lst if x['par'] == par and x['clave'] == k), None)
    K = 'R0_nacidos'; out = {}
    pn, pb, on = g(P, 'PARTO-NADA', K), g(P, 'PARTO-BAR', K), g(P, 'ORACULO-NADA', K)
    mpn, mpb = g(PM, 'PARTO-NADA', K), g(PM, 'PARTO-BAR', K)
    nada = A.get('NADA') or {}
    k_anc = 'V-ANCLA (mediana R0_nacidos NADA en [0.00, 0.10] y NADA persiste_carro en <= 5/20)'
    k_tec = 'V-TECHO (ORACULO > NADA en R0_nacidos >= 15/20)'
    k1, k2 = 'F-1 (PARTO > NADA en R0_nacidos >= 15/20)', 'F-2 (PARTO > BAR en R0_nacidos >= 15/20)'
    k3, k4 = 'F-3 (MIX: PARTO > NADA en R0_nacidos, mismo mundo, >= 15/20)', 'F-4 (MIX: PARTO > BAR en R0_nacidos, mismo mundo, >= 15/20)'
    out[k_anc] = bool(nada.get(K) is not None and 0.0 <= nada[K] <= 0.10 and nada.get('persiste_carro', 99) <= n_sem - need)
    out[k_tec] = bool(on and on['gana'] >= need)
    out[k1] = bool(pn and pn['gana'] >= need); out[k2] = bool(pb and pb['gana'] >= need)
    out[k3] = bool(mpn and mpn['gana'] >= need); out[k4] = bool(mpb and mpb['gana'] >= need)
    out['C-BAR (el control GANA o empata: BAR >= PARTO en R0_nacidos en >= 10/20)'] = bool(pb and (pb['pierde'] + pb['empata']) >= math.ceil(0.5 * n_sem))
    out['L-PERSISTE (informativo: semillas donde persiste el carro PARTO)'] = (A.get('PARTO') or {}).get('persiste_carro')
    if not out[k_anc]: v = 'NO SE LEE (ancla fuera: el instrumento no reproduce el piso de FABRICA en v2)'
    elif not out[k_tec]: v = 'NO SE LEE COMO CAPACIDAD (ni la tabla verdadera sube el R0 de los nacidos: el contenido no tiene donde actuar en este mundo)'
    elif out[k1] and out[k2] and out[k3] and out[k4]:
        v = 'FUNCIONA (lo que el padre vivo transmite en el parto sube el exito reproductivo de sus hijos, por su CONTENIDO, en monocultivo y compitiendo en el mismo mundo)'
    elif out[k1] and out[k2]:
        v = 'HAY ALGO MODESTO (el contenido transmitido en el parto sube el R0 de los nacidos en monocultivo; no gana la competencia directa en el mismo mundo)'
    elif out[k1]:
        v = 'HAY ALGO MODESTO SIN CONTENIDO (transmitir ayuda, pero el nodo barajado no pierde por la letra: no se declara transmision de contenido)'
    else: v = 'NO (transmitir el nodo en el parto no sube el R0 de los nacidos)'
    out['VEREDICTO'] = v
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true')
    ap.add_argument('--brazo', default=None); ap.add_argument('--desde', type=int, default=None)
    ap.add_argument('--n', type=int, default=20); ap.add_argument('--T', type=int, default=None)
    ap.add_argument('--pool', type=int, default=0)
    a = ap.parse_args()
    if a.humo == a.serie: raise SystemExit("corre_n10: --humo o --serie (uno)")
    verifica_shas()
    brazos = [a.brazo] if a.brazo else list(BRAZOS)
    if a.humo:
        desde = a.desde or SEMILLAS['practica'][0]; n = 1 if a.desde is None else a.n; T = a.T or 20000
        if a.pool: raise SystemExit("corre_n10: el humo es de UN proceso (sin --pool)")
        sal = os.path.join(DATOS, 'humo'); et = f"n10_humo_{'_'.join(brazos) if len(brazos) < 5 else 'todos'}_s{desde}_T{T}"
    else:
        desde = a.desde; n = a.n; T = a.T or T_DEF
        if desde is None: raise SystemExit("corre_n10: --serie exige --desde")
        ok = any(lo <= desde and desde + n - 1 <= hi for k, (lo, hi) in SEMILLAS.items() if k != 'practica')
        if not ok: raise SystemExit(f"corre_n10: semillas {desde}..{desde + n - 1} fuera de las preregistradas {SEMILLAS}")
        sal = DATOS; et = f"n10_serie_s{desde}-{desde + n - 1}_T{T}"
    os.makedirs(sal, exist_ok=True)
    sello = time.strftime('%Y%m%d_%H%M%S'); base = os.path.join(sal, f"{et}_{sello}")
    flog = open(base + '.log', 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"corre_n10 · {et} · {sello} · python {platform.python_version()} · corre_n10.py {h16(os.path.abspath(__file__))}")
    log("shas: " + ' '.join(f"{os.path.basename(p)}={s}" for p, s in SHAS.items()))
    semillas = list(range(desde, desde + n)); tareas = [(s, b, T) for b in brazos for s in semillas]
    t0 = time.time(); R = []
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as pool:
            for r in pool.imap_unordered(tarea, tareas):
                R.append(r); log(f"  {r['brazo']:8s} s{r['seed']} {r['seg']:7.1f} s · " + ' · '.join(
                    f"{e}: tam {v['tam_carro']} nac {v['nac']} sinext {v['linajes_sin_ext']}" for e, v in r['estr'].items()))
    else:
        for tk in tareas:
            r = tarea(tk); R.append(r); log(f"  {r['brazo']:8s} s{r['seed']} {r['seg']:7.1f} s · " + ' · '.join(
                f"{e}: tam {v['tam_carro']} nac {v['nac']} sinext {v['linajes_sin_ext']} R0nac {v['R0_nacidos']} vida nac/fund {v['vida_nacidos']}/{v['vida_fund']}"
                for e, v in r['estr'].items()))
    A, P, PM = agrega(R)
    log(f"\nAGREGADO (medianas por semilla) · {len(semillas)} semillas · {time.time() - t0:.0f} s de pared")
    for b, v in A.items(): log(f"  {b:8s} {v}")
    log("PAREADOS (monocultivo, por semilla):")
    for x in P: log(f"  {x}")
    log("PAREADOS (MIX, dentro del mismo mundo):")
    for x in PM: log(f"  {x}")
    V = veredicto(A, P, PM, len(semillas)) if a.serie else {'VEREDICTO': 'HUMO: no hay veredicto (una semilla de practica)'}
    log("VEREDICTO por la letra (PREREGISTRO_n10.md sec. 6):")
    for k, v in V.items(): log(f"  {k}: {v}")
    meta = dict(etiqueta=et, sello=sello, semillas=semillas, T=T, brazos=brazos, shas={os.path.basename(p): s for p, s in SHAS.items()},
                corre_n10=h16(os.path.abspath(__file__)), seg_pared=round(time.time() - t0, 1), seg_cpu=round(sum(r['seg'] for r in R), 1))
    res = dict(meta=meta, agregado=A, pareados=P, pareados_mix=PM, veredicto=V,
               por_semilla=[{k: r[k] for k in ('seed', 'brazo', 'T', 'seg', 'estr')} for r in R])
    json.dump(res, open(base + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with gzip.open(base + '_crudo.json.gz', 'wt', encoding='utf-8') as f: json.dump(R, f)
    log(f"\nescrito: {base}.json ({h16(base + '.json')}) · crudo {base}_crudo.json.gz")
    flog.close()


if __name__ == '__main__':
    main()
