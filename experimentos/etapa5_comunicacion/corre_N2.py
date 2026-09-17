"""Etapa 5, N2: el significado emerge (juego de senalizacion experto-novato en el mundo de regla 'azar', base v13).
Ejecuta PREREGISTRO_N2.md. REGLA 10: log desde el arranque. REGLA 11: procesos vivos. Igualdades NUMERICAS.
Precisiones escritas ANTES de correr:
- Progenitor del experto: mundo_social.run(seed, n=1, mundo='regla', regla='azar', T=200000, devolver_estado=True).
- Novato = organismo 0; experto = organismo 1 (estado heredado; Pq y M NO se heredan).
- veneno_total = suma de mordidas propias sobre los 10 patrones veneno (veneno_propio); veneno_q1 = suma de mord[k][0].
- s_rech / s_mord = argmax de Pq[0] / Pq[1] del EXPERTO al final.
Uso:  python experimentos/etapa5_comunicacion/corre_N2.py [--desde N] [--n N]
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias')]
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 1
_n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 20
SEEDS = list(range(_desde, _desde + _n)); T = 200000; REGLA = 'azar'
CONDS = {'SOLO': dict(n=1), 'N0': dict(n=2), 'INNATO': dict(n=2, senal='conducta'), 'CONV': dict(n=2, senal='simbolo'),
         'SHUF': dict(n=2, senal='simbolo_barajado')}
N_PARALELO = 14
_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def N(x):
    return json.loads(json.dumps(x, default=str))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def tarea(args):
    tipo = args[0]
    import mundo_social as ms
    if tipo == 'K1':
        _, seed = args
        import organismo_v13g as g
        a = g.run(seed, T=100000, mundo='regla', regla=REGLA, fase2_en=0, eta_s=0.015, puerta=3)   # v13g con los defectos del TRONCO
        b = ms.run(seed, n=1, T=100000, mundo='regla', regla=REGLA)[0]
        claves = ['W', 'mord', 'vis', 'deaths', 'splits', 'split_t', 'celdas']
        dif = [k for k in claves if N(a[k]) != N(b[k])]
        return dict(tipo=tipo, seed=seed, identico=not dif, difieren=dif)
    if tipo == 'P':
        _, seed = args
        r = ms.run(seed, n=1, T=T, mundo='regla', regla=REGLA, devolver_estado=True)[0]
        return dict(tipo=tipo, seed=seed, estado=r['estado'], W=r['W'])
    _, cond, seed, estado = args
    kw = CONDS[cond]
    estados = None if kw['n'] == 1 else [None, estado]
    out = ms.run(seed, T=T, mundo='regla', regla=REGLA, estados=estados, **kw)
    import organismo_v13g as g
    vr = g.split_regla(seed, REGLA)[3]
    for o in out:
        o.pop('estado', None)
        ven = [k for k in vr if vr[k] == 'veneno']; com = [k for k in vr if vr[k] == 'comida']
        o['veneno_total'] = int(sum(o['veneno_propio'][k] for k in ven)); o['veneno_q1'] = int(sum(o['mord'][k][0] for k in ven))
        o['venenos_conocidos'] = int(sum(o['W'][k] <= -2.5 for k in ven)); o['comidas_conocidas'] = int(sum(o['W'][k] >= 0.5 for k in com))
    return dict(tipo='R', cond=cond, seed=seed, orgs=out)


def med(xs):
    return float(np.median(xs))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    _log['f'] = open(os.path.join(RAIZ, 'datos', f'N2_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_N2.md')
    log(f"ARRANQUE N2 (significado emergente). semillas {SEEDS[0]}..{SEEDS[-1]}, T={T}, regla {REGLA}. Pool({N_PARALELO}).")
    log(f"sha preregistro {h16(pre)}  script {h16(os.path.abspath(__file__))}  mundo_social {h16(os.path.join(AQUI, 'mundo_social.py'))}"
        f"  v13 {h16(os.path.join(RAIZ, 'organismo', 'organismo_v13.py'))}  v13g {h16(os.path.join(RAIZ, 'experimentos', 'v13_dos_vias', 'organismo_v13g.py'))}")
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 — procesos python vivos ({len(ps)}), este es pid {os.getpid()}")
    V = {}
    with mp.Pool(N_PARALELO) as pool:
        k1 = pool.map(tarea, [('K1', s) for s in (1, 2, 3)], chunksize=1)
        V['K1'] = all(x['identico'] for x in k1)
        log(f"ETAPA 1/4 — K1 mundo_social(n=1, regla) == organismo_v13g(regla, fase2_en=0): {sum(x['identico'] for x in k1)}/3 -> {'OK' if V['K1'] else 'FALLA'}")
        for x in k1:
            if not x['identico']: log(f"      DIFIERE s{x['seed']}: {x['difieren']}")
        if not V['K1']:
            log("*** K1 FALLIDO: se para."); sys.exit(1)
        log(f"ETAPA 2/4 — progenitores del experto ({len(SEEDS)}, T={T})...")
        prog = {r['seed']: r for r in pool.map(tarea, [('P', s) for s in SEEDS], chunksize=1)}
        import organismo_v13g as g
        conoc = []
        for s in SEEDS:
            vr = g.split_regla(s, REGLA)[3]
            conoc.append(sum(prog[s]['W'][k] <= -2.5 for k in vr if vr[k] == 'veneno'))
        log(f"  progenitores: venenos conocidos (de 10) mediana {med(conoc):.0f} [{min(conoc)}, {max(conoc)}]")
        trabajos = [('R', c, s, prog[s]['estado']) for c in CONDS for s in SEEDS]
        log(f"ETAPA 3/4 — {len(trabajos)} corridas...")
        res = []
        for i, r in enumerate(pool.imap_unordered(tarea, trabajos, chunksize=1), 1):
            res.append(r)
            if i % 20 == 0 or i == len(trabajos):
                log(f"          {i}/{len(trabajos)}")
    log("ETAPA 4/4 — analisis.")
    G = lambda c: {r['seed']: r['orgs'] for r in res if r['cond'] == c}
    nov = lambda c: [G(c)[s][0] for s in SEEDS]
    exp = lambda c: [G(c)[s][1] for s in SEEDS]
    log(); log(f"  {'cond':7s} {'veneno total (novato)':24s} {'veneno Q1':10s} {'muertes':8s} {'venenos conocidos/10':21s} {'comidas/10':11s} {'simbolos recibidos':19s} {'decodificados':14s}")
    for c in CONDS:
        n_ = nov(c)
        log(f"  {c:7s} {med([o['veneno_total'] for o in n_]):6.0f} [{min(o['veneno_total'] for o in n_):4d},{max(o['veneno_total'] for o in n_):4d}]       "
            f"{med([o['veneno_q1'] for o in n_]):6.0f}     {med([o['deaths'] for o in n_]):6.0f}   {med([o['venenos_conocidos'] for o in n_]):4.0f}                  "
            f"{med([o['comidas_conocidas'] for o in n_]):4.0f}        {med([o['simbolos_recibidos'] for o in n_]):7.0f}             {med([o['decodificados'] for o in n_]):7.0f}")
    V['K2'] = med([o['simbolos_recibidos'] for o in nov('CONV')]) >= 1000
    # E1: convencion en el experto (CONV)
    ex = exp('CONV'); nv = nov('CONV')
    e1 = [(o['simbolos']['distintos'] and o['simbolos']['consistencia_q4'] is not None and o['simbolos']['consistencia_q4'] >= 0.9) for o in ex]
    V['E1'] = sum(e1) >= 15
    # E2: decodificacion en el novato con los simbolos preferidos del experto
    e2 = []
    for o_e, o_n in zip(ex, nv):
        sr, sm = o_e['simbolos']['simbolo_rechazo'], o_e['simbolos']['simbolo_muerde']
        Cn = [m - float(np.mean(o_n['M'])) for m in o_n['M']]   # ENMIENDA 1: contraste, no magnitud
        e2.append(Cn[sr] <= -1.0 and Cn[sm] >= 0.3)
    V['E2'] = sum(e2) >= 15
    rech0 = sum(o['simbolos']['simbolo_rechazo'] == 0 for o in ex)
    V['E3'] = 5 <= rech0 <= 15
    v0 = [o['veneno_total'] for o in nov('N0')]; vc = [o['veneno_total'] for o in nv]; vi = [o['veneno_total'] for o in nov('INNATO')]; vs = [o['veneno_total'] for o in nov('SHUF')]
    par = sum(b < a for a, b in zip(v0, vc))
    V['E4'] = med(vc) <= 0.7 * med(v0) and par >= 14
    shuf_M = sum(all(abs(m - float(np.mean(o['M']))) < 1.0 for m in o['M']) for o in nov('SHUF'))   # ENMIENDA 1: contraste
    V['E5'] = shuf_M >= 15 and med(vs) >= 0.9 * med(v0)
    log()
    log(f"  K2 simbolos recibidos por el novato (CONV): mediana {med([o['simbolos_recibidos'] for o in nv]):.0f} (>=1000): {'OK' if V['K2'] else 'FALLA'}")
    log(f"  E1 convencion en el emisor (simbolos distintos y consistencia Q4 >= 0.9): {sum(e1)}/20 (>=15): {'SOSTENIDA' if V['E1'] else 'REFUTADA'}"
        f"   consistencia Q4 mediana {med([o['simbolos']['consistencia_q4'] or 0 for o in ex]):.2f}  distintos {sum(o['simbolos']['distintos'] for o in ex)}/20")
    log(f"  E2 decodificacion en el receptor (M[s_rech]<=-1 y M[s_mord]>=+0.3): {sum(e2)}/20 (>=15): {'SOSTENIDA' if V['E2'] else 'REFUTADA'}"
        f"   contraste C[s_rech] mediana {med([o_n['M'][o_e['simbolos']['simbolo_rechazo']] - float(np.mean(o_n['M'])) for o_e, o_n in zip(ex, nv)]):+.2f}"
        f"  C[s_mord] {med([o_n['M'][o_e['simbolos']['simbolo_muerde']] - float(np.mean(o_n['M'])) for o_e, o_n in zip(ex, nv)]):+.2f}"
        f"  (M crudo: {med([o_n['M'][o_e['simbolos']['simbolo_rechazo']] for o_e, o_n in zip(ex, nv)]):+.2f} / {med([o_n['M'][o_e['simbolos']['simbolo_muerde']] for o_e, o_n in zip(ex, nv)]):+.2f})")
    log(f"  E3 arbitrariedad: el simbolo 0 significa rechazo en {rech0}/20 (entre 5 y 15): {'SOSTENIDA' if V['E3'] else 'REFUTADA'}")
    log(f"  E4 beneficio: veneno CONV {med(vc):.0f} <= 0.7 x N0 {med(v0):.0f} = {0.7*med(v0):.0f}, pareado {par}/20 (>=14): {'SOSTENIDA' if V['E4'] else 'REFUTADA'}   (INNATO {med(vi):.0f}, SOLO {med([o['veneno_total'] for o in nov('SOLO')]):.0f})")
    log(f"  E5 barajar destruye: |M|<1 en {shuf_M}/20 (>=15) y veneno SHUF {med(vs):.0f} >= 0.9 x N0 {0.9*med(v0):.0f}: {'SOSTENIDA' if V['E5'] else 'REFUTADA'}")
    log(f"  E6 (sin voto) el individuo solo no tiene simbolos: SOLO recibe {med([o['simbolos_recibidos'] for o in nov('SOLO')]):.0f}")
    log(f"  refuerzos del experto (CONV) +/-: {med([o['simbolos']['refuerzos'][0] for o in ex]):.0f} / {med([o['simbolos']['refuerzos'][1] for o in ex]):.0f};  Pq experto (mediana de |Pq|): {med([abs(x) for o in ex for fila in o['simbolos']['Pq'] for x in fila]):.2f}")
    V['N2_EMERGE'] = bool(V['K1'] and V['K2'] and V['E1'] and V['E2'] and V['E3'] and V['E4'] and V['E5'])
    log(); log("VEREDICTO N2: " + " ".join(f"{k}={v}" for k, v in V.items()))
    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), semillas=SEEDS, T=T, regla=REGLA, veredictos=V, K1=k1, procesos_python=ps,
                sha_preregistro=h16(pre), sha_script=h16(os.path.abspath(__file__)), sha_mundo_social=h16(os.path.join(AQUI, 'mundo_social.py')),
                python=platform.python_version(), numpy=np.__version__)
    dj = os.path.join(RAIZ, 'datos', f'N2_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}.json')
    json.dump(dict(meta=meta, corridas=res), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
