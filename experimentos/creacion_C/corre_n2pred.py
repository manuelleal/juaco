"""C-P6 — ejecuta PREREGISTRO_n2pred.md: N2 POR PREDICCION en el mundo minimo decidible (ERR-32/33/34 corregidos).
La pregunta principal es N6: con el emisor MUDO desde T/2, el receptor ¿se queda con lo aprendido, o solo obedecia?
REGLA 10: log desde el arranque, con fsync.

    python experimentos/creacion_C/corre_n2pred.py [--desde N] [--sin-mudo]
    python experimentos/creacion_C/corre_n2pred.py --humo      (UN proceso, sin Pool: lo corre el disenador)

Etapas con Pool (las corre el COORDINADOR, reglas 3 y 11):
  1/2 identidades L1 (perillas apagadas == mundo_social_n3), L2 (la sonda solo lee), L3 (u[c] solo mide). Si no son
      100 %, ABORTA.
  2/2 6 brazos x 2 (hablando / mudo desde T/2) x 20 semillas, T=200000.
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
COM = os.path.join(RAIZ, 'experimentos', 'etapa5_comunicacion')
sys.path[:0] = [AQUI, COM, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias')]

T = 200000
MUDO = T // 2
N_SEM = 20
N_PARALELO = 14
G = 1 / 3
KP = dict(gamma_soc=1.5, eta_sym=0.05, gamma_pred=G, tau_pred=400)
MR = [0, 0, 0, 1, 1, 1.]; ME = [1, 1, 1, 0, 0, 0.]
# El mundo minimo decidible: 8 vistas distintas + flujo DENTRO del conjunto fijo + el mismo nº de objetos en todo brazo.
BASE = dict(mundo='regla', regla='px0', d_senal=5, f_vicaria=1 / 3, regen=50, regen_rota=True,
            regen_en_fijos=True, vida=100, nobj_total=8, win_crit=400, crit_rec=0.75)
BRAZOS = {
    'N0':       dict(n=2, mascaras=[MR, ME]),
    'SOLO_R':   dict(n=1, mascaras=[MR]),
    'INNATO':   dict(n=2, mascaras=[MR, ME], senal='conducta', kw_por_org=[dict(gamma_soc=1.5), dict(escucha=False)]),
    'PRED':     dict(n=2, mascaras=[MR, ME], senal='conducta', kw_por_org=[KP, dict(escucha=False)]),
    'SHUF':     dict(n=2, mascaras=[MR, ME], senal='barajada_conducta', kw_por_org=[KP, dict(escucha=False)]),
    'SACIEDAD': dict(n=2, mascaras=[MR, ME], senal='conducta', kw_por_org=[KP, dict(escucha=False, alpha=0.0)]),
}
BANDA = (0.60, 0.85)

_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


SHAS = lambda: dict(
    preregistro=h16(os.path.join(AQUI, 'PREREGISTRO_n2pred.md')), script=h16(os.path.abspath(__file__)),
    constructor=h16(os.path.join(AQUI, 'construye_n2pred.py')), mundo_pred=h16(os.path.join(AQUI, 'mundo_social_pred.py')),
    mundo_vd=h16(os.path.join(AQUI, 'mundo_vd.py')), identidad=h16(os.path.join(AQUI, 'identidad_n2pred.py')),
    mundo_social_n3=h16(os.path.join(COM, 'mundo_social_n3.py')), corre_N3d=h16(os.path.join(COM, 'corre_N3d.py')))

INF = float('inf')


def cens(x):
    """Cláusula de censura del preregistro (N2'): 'no alcanza el criterio' cuenta como PEOR que cualquier finito."""
    return INF if x is None else float(x)


def mediana(xs):
    xs = [x for x in xs if x is not None]
    return float(np.median(xs)) if xs else None


def pareado(a, b, seeds, clave, menor_es_mejor=True):
    n = 0
    for s in seeds:
        x, y = a.get(s, {}).get(clave), b.get(s, {}).get(clave)
        if x is None and y is None:
            continue
        x, y = cens(x), cens(y)
        n += (x < y) if menor_es_mejor else (x > y)
    return n


def tarea(args):
    tipo = args[0]
    if tipo == 'L':
        _, cual, cond, seed = args
        import identidad_n2pred as I
        import mundo_social_n3 as REF, mundo_social_pred as PR
        from organismo_v13g import split_regla
        _, _, _, val = split_regla(seed, 'px0')
        kw = dict(I.BASE, T=20000, tipos_fijos=I.parejas(seed, dict(val)), **I.COND[cond])
        a = REF.run(seed, **kw); b = PR.run(seed, **kw, **I.CASOS[cual])
        N = lambda x: json.loads(json.dumps(x, default=str))
        dif = [(j, k) for j in range(len(a)) for k in a[j] if N(a[j][k]) != N(b[j][k])]
        return dict(tipo='L', cual=cual, cond=cond, seed=seed, identico=not dif, difieren=dif[:6])

    _, brazo, seed, mudo = args
    import mundo_social_pred as PR
    from organismo_v13g import split_regla
    from mundo_vd import parejas_vd
    from mini_n2pred import acierto_q4
    pats, _, _, val = split_regla(seed, 'px0'); val = dict(val)
    tf = parejas_vd(seed, pats, val)
    extra = dict(mudo_desde=MUDO) if mudo else {}
    out = PR.run(seed, T=T, tipos_fijos=tf, **BASE, **BRAZOS[brazo], **extra)
    r = out[0]
    return dict(tipo='T', brazo=brazo, seed=seed, mudo=bool(mudo), acierto=acierto_q4(r, val),
                presentes=sum(1 for k in r['vis'] if r['vis'][k][3] > 0),
                expo_crit=r['expo_crit'], mord_crit=r['mord_crit'], expo=r['expo_rec'], mord=r['mord_rec'],
                u=r['u'], n_u=r['n_u'], n_pred_vic=r['n_pred_vic'], deaths=r['deaths'],
                recibidas=r.get('senales_recibidas', 0))


def humo():
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'n2pred_humo_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log("HUMO del disenador, UN proceso, sin Pool (regla 3). Preregistro PREREGISTRO_n2pred.md.")
    log("Semillas 1-3, YA expuestas en los humos de diseno. Las 121-140 del experimento quedan limpias.")
    for k, v in SHAS().items():
        log(f"    sha {k:18s} {v}")
    global T, MUDO
    T, MUDO = 100000, 50000
    res = []
    log(f"6 brazos x 2 (hablando / mudo) x 3 semillas, T={T}, mudo desde {MUDO}.")
    log(f"{'brazo':>9} {'sem':>4} {'mudo':>5} | {'pres':>4} {'acierto':>7} | {'mord_crit':>9} | {'u[0]':>7} {'u[1]':>7}")
    for b in BRAZOS:
        for s in (1, 2, 3):
            for mu in (0, 1):
                t1 = time.time(); r = tarea(('T', b, s, mu)); res.append(r)
                log(f"{b:>9} {s:>4} {str(bool(mu)):>5} | {r['presentes']:>4} {r['acierto']:>7.3f} | "
                    f"{str(r['mord_crit']):>9} | {r['u'][0]:>7.3f} {r['u'][1]:>7.3f}   ({time.time()-t1:.1f}s)")
    log("")
    for b in BRAZOS:
        ha = mediana([x['acierto'] for x in res if x['brazo'] == b and not x['mudo']])
        mu = mediana([x['acierto'] for x in res if x['brazo'] == b and x['mudo']])
        log(f"   {b:>9}: hablando {ha:.3f}   MUDO {mu:.3f}")
    n0 = mediana([x['acierto'] for x in res if x['brazo'] == 'N0' and not x['mudo']])
    log(f"   G-c banda de la linea base: N0 {n0:.3f} -> {'DENTRO' if BANDA[0] <= n0 <= BANDA[1] else 'FUERA'} de {BANDA}")
    log(f"   G-b K3: presentes min {min(x['presentes'] for x in res)}/8")
    log("HUMO: n=3 y semillas vistas. NO es evidencia; sirve para ver que el montaje mide.")
    dj = os.path.join(RAIZ, 'datos', f'n2pred_humo_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), tipo='humo', T=T, mudo_desde=MUDO,
                             shas=SHAS(), python=platform.python_version(), numpy=np.__version__), corridas=res),
              open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()


if __name__ == '__main__':
    if '--humo' in sys.argv:
        humo(); sys.exit(0)

    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    import identidad_n2pred as I
    desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 121
    SEEDS = list(range(desde, desde + N_SEM))
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'n2pred_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    log(f"ARRANQUE C-P6 (N2 por prediccion, mundo minimo decidible): brazos {list(BRAZOS)}, semillas {SEEDS[0]}-{SEEDS[-1]}, "
        f"T={T}, mudo desde {MUDO}. Pool({N_PARALELO}).")
    log("Pregunta principal N6: con el emisor MUDO, ¿el receptor retiene lo aprendido o solo obedecia?")
    for k, v in SHAS().items():
        log(f"    sha {k:18s} {v}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V = {}; res = []
    with mp.Pool(N_PARALELO) as pool:
        ctrl = [('L', c, cond, s) for c in I.CASOS for cond in I.COND for s in (1, 2, 3)]
        log(f"ETAPA 1/2 — identidades L1/L2/L3 sobre las {len(I.COND)} condiciones de N3d: {len(ctrl)} comprobaciones...")
        rc = pool.map(tarea, ctrl, chunksize=1)
        for cual in I.CASOS:
            g = [x for x in rc if x['cual'] == cual]
            log(f"    {cual}: {sum(x['identico'] for x in g)}/{len(g)}")
            for x in g:
                if not x['identico']:
                    log(f"        DIFIERE {x['cond']} s{x['seed']}: {x['difieren']}")
            V[cual] = all(x['identico'] for x in g)
        V['G_a_IDENTIDAD'] = all(V[c] for c in I.CASOS)
        if not V['G_a_IDENTIDAD']:
            log("*** GUARDA G-a FALLIDA: las perillas apagadas no son mundo_social_n3. Se para.")
            sys.exit(1)

        tr = [('T', b, s, mu) for b in BRAZOS for s in SEEDS for mu in ((0, 1) if '--sin-mudo' not in sys.argv else (0,))]
        log(f"ETAPA 2/2 — {len(tr)} corridas de {T} pasos...")
        for i, r in enumerate(pool.imap_unordered(tarea, tr, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(tr):
                log(f"          {i}/{len(tr)}")

    Gh = {b: {r['seed']: r for r in res if r['brazo'] == b and not r['mudo']} for b in BRAZOS}
    Gm = {b: {r['seed']: r for r in res if r['brazo'] == b and r['mudo']} for b in BRAZOS}

    log("ANALISIS — guardas primero.")
    pres_ok = sum(1 for s in SEEDS if all(Gh[b].get(s, {}).get('presentes', 0) == 8 for b in BRAZOS))
    V['G_b_K3'] = pres_ok >= 18
    log(f"   G-b K3 (los 8 presentes en Q4 en todos los brazos): {pres_ok}/{N_SEM} -> {'OK' if V['G_b_K3'] else 'NO'}")
    n0 = mediana([r['acierto'] for r in Gh['N0'].values()])
    V['G_c_BANDA'] = bool(n0 is not None and BANDA[0] <= n0 <= BANDA[1])
    log(f"   G-c banda de N0: {None if n0 is None else round(n0,3)} en {BANDA} -> {'OK' if V['G_c_BANDA'] else 'NO (mundo no decidible; ERR)'}")
    rec = mediana([r['recibidas'] for r in Gh['PRED'].values()])
    V['G_d_CANAL'] = bool(rec is not None and rec > 1000)
    log(f"   G-d el canal se usa: senales recibidas por PRED {rec} (>1000) -> {'OK' if V['G_d_CANAL'] else 'NO'}")
    for b in BRAZOS:
        log(f"   {b:>9} hablando {mediana([r['acierto'] for r in Gh[b].values()])}  MUDO {mediana([r['acierto'] for r in Gm[b].values()]) if Gm[b] else None}"
            f"  mord_crit {mediana([r['mord_crit'] for r in Gh[b].values()])}  cens {sum(1 for r in Gh[b].values() if r['mord_crit'] is None)}/{len(Gh[b])}")

    log("ANALISIS — predicciones.")
    pm, n0m = mediana([r['acierto'] for r in Gm['PRED'].values()]), mediana([r['acierto'] for r in Gm['N0'].values()])
    p6n = pareado(Gm['PRED'], Gm['N0'], SEEDS, 'acierto', menor_es_mejor=False)
    N6 = bool(pm is not None and n0m is not None and pm >= 0.65 and pm >= n0m + 0.10 and p6n >= 14)
    log(f"   N6 (PRINCIPAL) PRED mudo {None if pm is None else round(pm,3)} (>=0.65 y >= N0 mudo {round(n0m,3)} +0.10), pareado {p6n}/{N_SEM} (>=14) -> {'OK' if N6 else 'NO'}")
    im = mediana([r['acierto'] for r in Gm['INNATO'].values()])
    N6b = bool(im is not None and im >= 0.65)
    log(f"   N6b INNATO mudo {None if im is None else round(im,3)} (>=0.65) -> {'OK' if N6b else 'NO — y entonces solo el significado APRENDIDO retiene'}")
    n1 = sum(1 for r in Gh['PRED'].values() if r['u'][1] >= 0.5 and r['u'][0] <= -0.15)
    log(f"   N1 significado: {n1}/{N_SEM} (>=15) -> {'OK' if n1 >= 15 else 'NO'}")
    rp, rn = mediana([r['mord_crit'] for r in Gh['PRED'].values()]), mediana([r['mord_crit'] for r in Gh['N0'].values()])
    n2n = pareado(Gh['PRED'], Gh['N0'], SEEDS, 'mord_crit')
    N2 = bool(rp is not None and rn is not None and rp <= 0.70 * rn and n2n >= 14)
    log(f"   N2' mordidas hasta criterio PRED {rp} contra N0 {rn} (<=0.70x), pareado {n2n}/{N_SEM} -> {'OK' if N2 else 'NO'}  [censura: None cuenta como peor]")
    ap, ai = mediana([r['acierto'] for r in Gh['PRED'].values()]), mediana([r['acierto'] for r in Gh['INNATO'].values()])
    N3 = bool(ap is not None and ai is not None and ap >= 0.85 and ap >= ai - 0.10)
    log(f"   N3 con canal: PRED {round(ap,3)} (>=0.85 y >= INNATO {round(ai,3)} -0.10) -> {'OK' if N3 else 'NO'}")
    N4 = True
    for ctl in ('SHUF', 'SACIEDAD'):
        n4 = sum(1 for s in SEEDS if s in Gh[ctl] and Gh[ctl][s]['acierto'] <= (Gh['N0'][s]['acierto'] + 0.02)
                 and (Gh[ctl][s]['u'][1] - Gh[ctl][s]['u'][0]) <= 0.3)
        N4 = N4 and n4 >= 18
        log(f"   N4 control {ctl}: {n4}/{N_SEM} (>=18); acierto {mediana([r['acierto'] for r in Gh[ctl].values()])}")
    ri = mediana([r['mord_crit'] for r in Gh['INNATO'].values()])
    N5 = bool(rp is not None and ri is not None and rp >= ri)
    log(f"   N5 coste del significado: PRED {rp} >= INNATO {ri} -> {'OK' if N5 else 'NO'}")

    V.update(N6=N6, N6b=N6b, N1=n1 >= 15, N2=N2, N3=N3, N4=N4, N5=N5)
    if not (V['G_b_K3'] and V['G_c_BANDA']):
        ver = "NULO: el mundo no es decidible (K3 o la banda de la linea base). ERR y mundo nuevo."
    elif not V['N1']:
        ver = "REFUTADO en la raiz: el receptor no aprende el significado."
    elif not N6:
        ver = "REFUTADO: aprender el significado NO compra retencion; el receptor sigue obedeciendo."
    elif not N6b:
        ver = ("SOLO EL SIGNIFICADO APRENDIDO RETIENE: PRED se queda con lo aprendido y el INNATO no. "
               "Pide replica inmediata en semillas nuevas antes de cualquier afirmacion.")
    elif not N4:
        ver = "NULO: un control informa cuando no deberia. Montaje invalido, ERR."
    else:
        ver = ("RETIENE, y el innato tambien: el mundo permite retener y lo que separa a PRED del innato es el COSTE "
               "en mordidas de aprender el significado (N5). Pide replica en semillas nuevas.")
    log(f"VEREDICTO (20 semillas; no cierra ningun nivel del brief): {ver}")

    dj = os.path.join(RAIZ, 'datos', f'n2pred_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, brazos=BRAZOS, base=BASE,
                             T=T, mudo_desde=MUDO, banda=BANDA, veredicto=ver, veredictos=V, identidades=rc,
                             procesos_python=ps, shas=SHAS(), python=platform.python_version(), numpy=np.__version__),
                   corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
