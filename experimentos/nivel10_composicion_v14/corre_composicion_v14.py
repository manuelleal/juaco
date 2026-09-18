"""corre_composicion_v14.py -- orquesta C1-C4 de PREREGISTRO_composicion_v14.md.

Los UMBRALES que decide este runner son los del PREREGISTRO (C1 8/8; C2 G1>=0.80,G2>=0.85,K 20/20; C3 lift_q4
mediana>=0.25 y >v13 en >=15/20, celdas<=0.75xv13 en >=14/20; C4 N*>=48 a paso 60000), NO los que traen de fabrica
bateria_generaliza.py (G1>=0.65,G2>=0.55) ni ningun otro umbral de una bateria que se reutiliza -- regla derivada de
ERR-31 (corre_baterias_v13E.py decidio con los umbrales equivocados; el veredicto impreso no coincidia con el
preregistro). Por eso C2 NO lee el campo `veredictos` del JSON de bateria_generaliza_v14c.py: recalcula G1/G2/K
desde `corridas` (los numeros crudos por semilla) con los umbrales de aqui.

REGLA 10 (EQUIPO.md): log desde el arranque, con fsync. REGLA 11: un solo Pool a la vez -- C1/C2 se lanzan como
SUBPROCESOS secuenciales (bateria_v14c.py / bateria_generaliza_v14c.py abren cada uno su propio Pool(14), heredado
sin cambios de los originales congelados); C3/C4 abren su Pool(14) DIRECTO en este proceso (mismo patron que la
etapa 1 de corre_baterias_v13D.py), pero siempre DESPUES de que el Pool del subproceso anterior ya haya terminado
-- nunca dos Pool vivos a la vez.

REGLA 3 (EQUIPO.md) -- por que --humo no llama a bateria_v14c.py ni a bateria_generaliza_v14c.py: esos dos
scripts SIEMPRE abren Pool(14) (lo heredan sin cambios de bateria_v13.py/bateria_generaliza.py; no aceptan un modo
de "una sola corrida"), y un implementador no corre Pool. --humo hace, en UN SOLO PROCESO, sin Pool y sin lanzar
ningun subproceso: (a) una identidad en miniatura (perillas apagadas == organismo_v13, 2 semillas -- ya se corrio
la version completa en identidad_v14c.py, 30/30); (b) C3 con 2 semillas y T corto; (c) C4 con 2 semillas y un
mundo chico. NO mide C1/C2 (eso exige Pool: lo corre el coordinador, sin --humo).

Uso (desde la raiz del repo):
  python experimentos/nivel10_composicion_v14/corre_composicion_v14.py --humo
  python experimentos/nivel10_composicion_v14/corre_composicion_v14.py [--desde-bat 101] [--n-bat 20]
      [--desde-3t 61] [--desde-cap 41] [--solo C1,C2]
"""
import sys, os, json, time, hashlib, platform, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
# ERR-28: organismo/ PRIMERO en sys.path, siempre.
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo'), os.path.join(RAIZ, 'experimentos', 'v13_dos_vias'),
                os.path.join(RAIZ, 'experimentos', 'nivel7_3T_k'), os.path.join(RAIZ, 'experimentos', 'capacidad_grande'),
                os.path.join(RAIZ, 'experimentos', 'v13_reverificacion'), os.path.join(RAIZ, 'experimentos', 'v11_evo_division')]

HUMO = '--humo' in sys.argv


def _arg(flag, default):
    return int(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default


DESDE_BAT = _arg('--desde-bat', 101)
NSEM_BAT = 2 if HUMO else _arg('--n-bat', 20)
DESDE_3T = _arg('--desde-3t', 61)
DESDE_CAP = _arg('--desde-cap', 41)
SOLO = set(sys.argv[sys.argv.index('--solo') + 1].split(',')) if '--solo' in sys.argv else {'C1', 'C2', 'C3', 'C4'}
N_PARALELO = 14

# ---- C2: umbrales del PREREGISTRO (no los de bateria_generaliza.py; ERR-31) ----
G1_MIN, G2_MIN = 0.80, 0.85

# ---- C3: composicion temporal (3T-k) ----
V13KW_3T = dict(mu_norm=True, div_signo=True, eta_s=0.015, puerta=3)   # el punto confirmado del tronco en este mundo
BRAZOS_3T = {
    'V13':  dict(mask_rel=0, del_s=0.25, del_c=0.25, n_cf=1, puerta_pat=0, pat_shuf=0, pat_min=0),
    'COMP': dict(mask_rel=2, del_s=0.25, del_c=0.25, n_cf=1, puerta_pat=5, pat_shuf=0, pat_min=1),   # las DOS ON
}
K3T = 5
T_3T = 3000 if HUMO else 100000
SEEDS_3T = list(range(DESDE_3T, DESDE_3T + (2 if HUMO else 20)))
# Referencia YA REGISTRADA de la hija dispersa SOLA en este mismo k y esta misma serie de semillas (61-80, k=5;
# registro/REGISTRO_etapas_1_2.md, bloque "composicion a k=4/5 (3T-k), serie 61-80"): sep 3.09, lift_q4 0.251,
# celdas 48 (medianas). C3 exige que la composicion llegue AL MENOS a eso (no solo a los umbrales absolutos).
REL_SOLA_61_80_K5 = dict(sep=3.09, lift_q4=0.251, celdas=48)


def tarea_c3(args):
    brazo, seed = args
    import mundo_composicion_v14 as m
    r = m.run(seed, arm='C3', kprof=K3T, T=T_3T, **V13KW_3T, **BRAZOS_3T[brazo])
    lf = r['lift'][3] if r['lift'][3] is not None else 0.0
    return dict(brazo=brazo, seed=seed, sep=r['sep'], lift_q4=lf, celdas=r['celdas'], splits=r['splits'], deaths=r['deaths'])


# ---- C4: capacidad en el mundo grande ----
D_PIX = 10
N_EST = 8 if HUMO else 60
PASOS = (500,) if HUMO else (20000, 60000)
SEEDS_CAP = list(range(DESDE_CAP, DESDE_CAP + (2 if HUMO else 20)))
BASE_CAP = dict(plast=True, lam=0.05, memoria_rechazo=20, mu_norm=True, div_signo=True)
BRAZOS_CAP = {
    'v13':  dict(eta_s=0.015, puerta=3),                                                                      # tronco: referencia baja (registro: N* 35 a 60k, 28 a 20k)
    'COMP': dict(eta_s=0.015, puerta=3, puerta_pat=5, pat_min=1, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05),   # las DOS ON
}


def tarea_c4(args):
    brazo, pt, seed = args
    import organismo_capBD as o
    import mundo_grande as G
    nom, pats, val, R = G.mundo(D_PIX, N_EST)
    kw = dict(T=G.T_de(pt, N_EST), plan=G.plan_de(pt, nom, val), pats=pats, chk=G.chks(pt, N_EST))
    r = o.run(seed, **kw, **BASE_CAP, **BRAZOS_CAP[brazo])
    for h in r['hist']:
        h['dev'] = {k: round(abs(v - R[k]), 3) for k, v in h['W'].items()}
    hist = [dict(t=h['t'], n=h['n'], celdas=h['celdas'], splits=h['splits'], dev=h['dev']) for h in r['hist']]
    return dict(brazo=brazo, pt=pt, seed=seed, hist=hist, celdas=r['celdas'], splits=r['splits'], deaths=r['deaths'])


def med(xs):
    xs = list(xs)
    return (float(np.median(xs)), float(min(xs)), float(max(xs))) if xs else (None, None, None)


_log = {'f': None, 't0': time.time()}


def log(msg=""):
    linea = f"[{time.strftime('%H:%M:%S')} +{time.time()-_log['t0']:7.1f}s] {msg}"
    print(linea, flush=True)
    if _log['f']:
        _log['f'].write(linea + "\n"); _log['f'].flush(); os.fsync(_log['f'].fileno())


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def lee_json(pref):
    """Ultimo datos/<pref>*.json escrito (las baterias lo dejan con --log). None si no hay ninguno (p.ej. si el
    criterio 5 de bateria_v14c.py aborto antes de escribir: sys.exit(1) antes del json.dump)."""
    d = os.path.join(RAIZ, 'datos')
    c = sorted([f for f in os.listdir(d) if f.startswith(pref) and f.endswith('.json')])
    return json.load(open(os.path.join(d, c[-1]), encoding='utf-8')) if c else None


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    nom = f'composicion_v14{"_humo" if HUMO else ""}_{stamp}'
    _log['f'] = open(os.path.join(RAIZ, 'datos', nom + '.log'), 'w', encoding='utf-8', newline='\n')
    pre = os.path.join(AQUI, 'PREREGISTRO_composicion_v14.md')
    shas = {n_: h16(p) for n_, p in [
        ('preregistro', pre), ('script', os.path.abspath(__file__)),
        ('constructor', os.path.join(AQUI, 'construye_v14c.py')), ('identidad', os.path.join(AQUI, 'identidad_v14c.py')),
        ('organismo_v14c', os.path.join(AQUI, 'organismo_v14c.py')), ('organismo_v14c_on', os.path.join(AQUI, 'organismo_v14c_on.py')),
        ('organismo_v14gc', os.path.join(AQUI, 'organismo_v14gc.py')), ('bateria_v14c', os.path.join(AQUI, 'bateria_v14c.py')),
        ('bateria_generaliza_v14c', os.path.join(AQUI, 'bateria_generaliza_v14c.py')),
        ('organismo_capBD', os.path.join(AQUI, 'organismo_capBD.py')), ('mundo_composicion_v14', os.path.join(AQUI, 'mundo_composicion_v14.py')),
        ('origen organismo_v13 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
        ('origen bateria_v13 (congelada)', os.path.join(RAIZ, 'organismo', 'bateria_v13.py')),
        ('origen bateria_generaliza', os.path.join(RAIZ, 'organismo', 'bateria_generaliza.py')),
        ('origen mundo_hija_dispersa', os.path.join(RAIZ, 'experimentos', 'nivel7_hija_dispersa', 'mundo_hija_dispersa.py')),
        ('origen organismo_capB', os.path.join(RAIZ, 'experimentos', 'nivel4_puerta_codigo', 'organismo_capB.py'))]}
    log(f"ARRANQUE composicion v14 (hija dispersa + puerta por codigo). {'HUMO (un proceso, sin Pool, sin subprocesos)' if HUMO else f'SOLO={sorted(SOLO)}  Pool({N_PARALELO}) por etapa, secuencial'}")
    log("sha " + "  ".join(f"{k}={v}" for k, v in shas.items()))
    try:
        ps = subprocess.run(['powershell', '-NoProfile', '-Command',
                             "Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | ForEach-Object { \"$($_.ProcessId) $($_.CommandLine)\" }"],
                            capture_output=True, text=True, timeout=60).stdout.strip().splitlines()
    except Exception as e:
        ps = [f"(no se pudo listar: {e})"]
    log(f"REGLA 11 -- procesos python vivos ({len(ps)}), este es pid {os.getpid()}")

    V = {}; crudos = {}
    env = dict(os.environ, PYTHONIOENCODING='utf-8')

    if HUMO:
        log(); log("ETAPA humo 1/3 -- identidad en miniatura (perillas apagadas == organismo_v13, 2 semillas)...")
        import organismo_v13 as _V13, organismo_v14c as _V14C
        ide = []
        for s in (1, 2):
            a, b = _V13.run(s, T=T_3T), _V14C.run(s, T=T_3T, mask_rel=0, puerta_pat=0, pat_shuf=0, pat_min=0)
            dif = [k for k in a if a[k] != b.get(k)]
            ide.append(dict(seed=s, identico=not dif, difieren=dif))
            log(f"   s{s}: {'IDENTICO' if not dif else 'DIFIERE ' + str(dif[:6])}")
        V['identidad_humo'] = dict(ok=all(x['identico'] for x in ide), n=len(ide))
        log(f"   -> {V['identidad_humo']['ok']}  (identidad completa: python identidad_v14c.py, 30/30 ya corrido)")

    # ---------------- C1 ----------------
    if 'C1' in SOLO and not HUMO:
        log(); log(f"ETAPA C1 -- examen v3' completo (bateria_v14c, las DOS perillas ON), semillas {DESDE_BAT}-{DESDE_BAT+NSEM_BAT-1}...")
        cmd = [sys.executable, os.path.join(AQUI, 'bateria_v14c.py'), str(NSEM_BAT), '--desde', str(DESDE_BAT), '--log']
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=os.path.join(RAIZ, 'organismo'))
        for l in [x.split('] ', 1)[-1].strip() for x in p.stdout.splitlines() if ('PASA' in x or 'FALLA' in x or 'VEREDICTO' in x or '***' in x)]:
            log(f"   {l}")
        if p.returncode != 0:
            log(f"   *** codigo {p.returncode} (si es el criterio 5, aborta antes de escribir el json): {p.stderr[-500:]}")
        j = lee_json('examen_v14c_')
        veredictos = (j or {}).get('meta', {}).get('veredictos')
        decisivos = ['5_identidad', '1_cientificos', '2_celdas', '3_control', '4a_identidad',
                     '4b_sin_conflicto_no_divide', '4c_misma_valencia', '4d_causa']
        ok8 = bool(veredictos) and all(bool(veredictos.get(k)) for k in decisivos)
        V['C1'] = dict(returncode=p.returncode, veredictos=veredictos, decisivos_ok=sum(bool((veredictos or {}).get(k)) for k in decisivos) if veredictos else 0, ok=ok8)
        log(f"   C1 = {V['C1']['decisivos_ok']}/8  ok={ok8}")
    elif 'C1' in SOLO:
        log(); log("ETAPA C1 -- SALTADA en modo humo (exige Pool via bateria_v14c.py; la corre el coordinador sin --humo).")

    # ---------------- C2 ----------------
    if 'C2' in SOLO and not HUMO:
        log(); log(f"ETAPA C2 -- generalizacion (bateria_generaliza_v14c, organismo_v14c_on), semillas {DESDE_BAT}-{DESDE_BAT+NSEM_BAT-1}...")
        cmd = [sys.executable, os.path.join(AQUI, 'bateria_generaliza_v14c.py'), 'organismo_v14c_on', str(NSEM_BAT), '--desde', str(DESDE_BAT), '--log']
        p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=os.path.join(RAIZ, 'organismo'))
        for l in [x.split('] ', 1)[-1].strip() for x in p.stdout.splitlines() if ('PASA' in x or 'FALLA' in x or 'OK ' in x or 'VEREDICTO' in x)]:
            log(f"   {l}")
        if p.returncode != 0:
            log(f"   *** codigo {p.returncode}: {p.stderr[-500:]}")
        j = lee_json('regresion_generaliza_organismo_v14c_on_')
        # ERR-31: NO se lee j['meta']['veredictos'] (esos son los umbrales 0.65/0.55 de bateria_generaliza.py).
        # Se recalcula G1/G2/K desde 'corridas' (numeros crudos por semilla) con los umbrales DEL PREREGISTRO.
        if j:
            res = j['corridas']; seeds = j['meta']['semillas']
            G_ = lambda rg: {r['seed']: r for r in res if r['regla'] == rg}
            px, az = G_('px0'), G_('azar')
            mpx = float(np.median([px[s]['acc'] for s in seeds])); maz = float(np.median([az[s]['acc'] for s in seeds]))
            par1 = sum(px[s]['acc'] > az[s]['acc'] for s in seeds)
            bpx = [px[s]['ba'] for s in seeds if px[s]['ba'] is not None]; baz = [az[s]['ba'] for s in seeds if az[s]['ba'] is not None]
            par2 = sum(1 for s in seeds if px[s]['ba'] is not None and az[s]['ba'] is not None and px[s]['ba'] > az[s]['ba'])
            cob20 = sum(px[s]['cobertura'] >= 6 for s in seeds)
            G1 = mpx >= G1_MIN; G2 = bool(bpx) and bool(baz) and float(np.median(bpx)) >= G2_MIN; K = cob20 == len(seeds)
            V['C2'] = dict(returncode=p.returncode, mpx=mpx, maz=maz, par1=par1, S=len(seeds),
                           ba_px=float(np.median(bpx)) if bpx else None, ba_az=float(np.median(baz)) if baz else None, par2=par2,
                           cobertura20=cob20, G1=G1, G2=G2, K=K, ok=bool(G1 and G2 and K))
            log(f"   G1 px0={mpx:.3f} (>={G1_MIN}) azar={maz:.3f} px0>azar {par1}/{len(seeds)}  -> {G1}")
            log(f"   G2 px0={V['C2']['ba_px']}  (>={G2_MIN}) azar={V['C2']['ba_az']} px0>azar {par2}/{len(seeds)}  -> {G2}")
            log(f"   K  cobertura>=6: {cob20}/{len(seeds)}  -> {K}   ==> C2 ok={V['C2']['ok']}")
        else:
            V['C2'] = dict(returncode=p.returncode, ok=False)
            log("   *** sin JSON: C2 no medible en esta corrida.")
    elif 'C2' in SOLO:
        log(); log("ETAPA C2 -- SALTADA en modo humo (exige Pool via bateria_generaliza_v14c.py).")

    # ---------------- C3 ----------------
    if 'C3' in SOLO:
        log(); log(f"ETAPA C3 -- composicion temporal (3T-k, k={K3T}), semillas {SEEDS_3T[0]}-{SEEDS_3T[-1]}, T={T_3T}...")
        lote = [(b, s) for b in BRAZOS_3T for s in SEEDS_3T]
        if HUMO:
            res = [tarea_c3(x) for x in lote]
        else:
            with mp.Pool(N_PARALELO) as pool:
                res = list(pool.imap_unordered(tarea_c3, lote, chunksize=1))
        Gb = lambda b: {r['seed']: r for r in res if r['brazo'] == b}
        v13, comp = Gb('V13'), Gb('COMP')
        m_lift = med([comp[s]['lift_q4'] for s in SEEDS_3T])[0]
        n_lift = sum(comp[s]['lift_q4'] > v13[s]['lift_q4'] for s in SEEDS_3T)
        n_cel = sum(comp[s]['celdas'] <= 0.75 * v13[s]['celdas'] for s in SEEDS_3T)
        m_sep_comp = med([comp[s]['sep'] for s in SEEDS_3T])[0]; m_cel_comp = med([comp[s]['celdas'] for s in SEEDS_3T])[0]
        m_sep_v13 = med([v13[s]['sep'] for s in SEEDS_3T])[0]; m_cel_v13 = med([v13[s]['celdas'] for s in SEEDS_3T])[0]
        ok_lift = None if HUMO else bool(m_lift is not None and m_lift >= 0.25 and n_lift >= 15)
        ok_cel = None if HUMO else bool(n_cel >= 14)
        ge_hija_sola = bool(m_lift is not None and m_lift >= REL_SOLA_61_80_K5['lift_q4']
                            and m_cel_comp is not None and m_cel_comp <= REL_SOLA_61_80_K5['celdas'])
        V['C3'] = dict(S=len(SEEDS_3T), lift_q4_comp=m_lift, lift_q4_v13=med([v13[s]['lift_q4'] for s in SEEDS_3T])[0],
                       n_lift_mayor=n_lift, sep_comp=m_sep_comp, sep_v13=m_sep_v13, celdas_comp=m_cel_comp, celdas_v13=m_cel_v13,
                       n_celdas_ok=n_cel, ok_lift=ok_lift, ok_celdas=ok_cel, ge_hija_sola=ge_hija_sola, ok=(bool(ok_lift and ok_cel) if not HUMO else None))
        log(f"   lift_q4 COMP mediana {m_lift:.3f} (>= 0.25), > V13 en {n_lift}/{len(SEEDS_3T)} (>= 15)  -> ok_lift={ok_lift}" + ('  [HUMO: umbral no aplica]' if HUMO else ''))
        log(f"   celdas COMP<=0.75xV13 en {n_cel}/{len(SEEDS_3T)} (>= 14)  celdas COMP={m_cel_comp:.0f} V13={m_cel_v13:.0f}  -> ok_celdas={ok_cel}" + ('  [HUMO: umbral no aplica]' if HUMO else ''))
        log(f"   referencia hija-dispersa-sola (registro, mismos seeds/k): lift_q4 {REL_SOLA_61_80_K5['lift_q4']}, celdas {REL_SOLA_61_80_K5['celdas']}  -> COMP >= esa referencia: {ge_hija_sola}")
        if HUMO:
            log("   (HUMO: 2 semillas, T corto -- ningun criterio numerico vale; solo prueba que el montaje corre.)")
        crudos['C3'] = res

    # ---------------- C4 ----------------
    if 'C4' in SOLO:
        log(); log(f"ETAPA C4 -- capacidad en el mundo grande (organismo_capBD), semillas {SEEDS_CAP[0]}-{SEEDS_CAP[-1]}, D={D_PIX}, n_est={N_EST}, pasos={PASOS}...")
        import mundo_grande as G_mod
        lote = [(b, pt, s) for pt in PASOS for b in BRAZOS_CAP for s in SEEDS_CAP]
        if HUMO:
            res = [tarea_c4(x) for x in lote]
        else:
            with mp.Pool(N_PARALELO) as pool:
                res = list(pool.imap_unordered(tarea_c4, lote, chunksize=1))
        tabla = {}
        for pt in PASOS:
            for b in BRAZOS_CAP:
                g = {r['seed']: r for r in res if r['brazo'] == b and r['pt'] == pt}
                Ns = [G_mod.techo(g[s]['hist']) for s in SEEDS_CAP]
                tabla[(b, pt)] = dict(N_mediana=med(Ns)[0], N_min=med(Ns)[1], N_max=med(Ns)[2], Ns=Ns,
                                      celdas=med([g[s]['celdas'] for s in SEEDS_CAP])[0])
                log(f"   {b:5s} pt={pt:6d}  N* {tabla[(b, pt)]['N_mediana']:.1f} [{tabla[(b, pt)]['N_min']:.0f},{tabla[(b, pt)]['N_max']:.0f}]  celdas {tabla[(b, pt)]['celdas']:.0f}")
        pt_ref = 60000 if 60000 in PASOS else PASOS[-1]
        n_comp_ref = tabla.get(('COMP', pt_ref), {}).get('N_mediana')
        ok_c4 = None if HUMO else bool(n_comp_ref is not None and n_comp_ref >= 48)
        V['C4'] = dict(pt_ref=pt_ref, N_comp=n_comp_ref, N_v13=tabla.get(('v13', pt_ref), {}).get('N_mediana'),
                       tabla={f"{b}_{pt}": v for (b, pt), v in tabla.items()}, ok=ok_c4)
        log(f"   C4: N*(COMP) a pt={pt_ref} = {n_comp_ref}  (umbral 48)  -> ok={ok_c4}" + ('  [HUMO: umbral no aplica, pt de humo no es 60000]' if HUMO else ''))
        if HUMO:
            log("   (HUMO: 2 semillas, mundo chico -- ningun criterio numerico vale; solo prueba que el montaje corre.)")
        crudos['C4'] = res

    log()
    if HUMO:
        log("VEREDICTO: HUMO completo -- el montaje corre en un proceso, sin Pool (C1/C2 exigen Pool: quedan para el coordinador).")
        ver = "HUMO OK"
    else:
        c1 = V.get('C1', {}).get('ok'); c2 = V.get('C2', {}).get('ok'); c3 = V.get('C3', {}).get('ok'); c4 = V.get('C4', {}).get('ok')
        medidas = {k: v for k, v in [('C1', c1), ('C2', c2), ('C3', c3), ('C4', c4)] if k in SOLO}
        if any(v is False for k, v in [('C1', c1), ('C2', c2)] if k in SOLO):
            ver = "LOS ORGANOS INTERFIEREN: C1 o C2 cayeron -> no se proponen juntos (clausula del preregistro)."
        elif c3 is False:
            ver = "LA PUERTA ANULA LA GANANCIA DE COMPOSICION: C3 cayo (clausula del preregistro)."
        elif all(v in (True, None) for v in medidas.values()) and any(v is True for v in medidas.values()):
            faltan = [k for k, v in medidas.items() if v is None]
            ver = "COMPOSICION SOSTENIDA en lo medido" + (f" (faltan: {faltan})" if faltan else " (C1-C4 completos)")
        else:
            ver = f"INCOMPLETO: {medidas}"
        log(f"VEREDICTO composicion_v14: {ver}")
        log(f"  C1={c1}  C2={c2}  C3={c3}  C4={c4}")

    meta = dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), humo=HUMO, solo=sorted(SOLO), veredictos=V, veredicto=ver,
               semillas=dict(bat=[DESDE_BAT, DESDE_BAT + NSEM_BAT - 1] if not HUMO else None, t3=[SEEDS_3T[0], SEEDS_3T[-1]], cap=[SEEDS_CAP[0], SEEDS_CAP[-1]]),
               shas=shas, procesos_python=ps, python=platform.python_version(), numpy=np.__version__, plataforma=platform.platform())
    dj = os.path.join(RAIZ, 'datos', nom + '.json')
    json.dump(dict(meta=meta, crudos=crudos), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f"datos -> {os.path.basename(dj)}  sha256_16 = {h16(dj)}")
    _log['f'].close()
