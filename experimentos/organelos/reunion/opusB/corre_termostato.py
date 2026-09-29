"""corre_termostato.py — RUNNER y LETRA del confirmatorio "LA SELECCION ENCUENTRA EL TERMOSTATO EN LA PISTA" (Opus B, 28-sep-2026).
Preregistro: PREREGISTRO_termostato_pista.md (la letra esta AQUI, en lee_serie(), y alli en la sec. 6). NO es un intento contra el muro:
su letra es la del termostato (dos puertas), no cruza_real/P1 del muro.

MISION: llegar a la AGI por este camino. Principio del director: que la evolucion construya el organo, no nosotros, solo con seleccion natural.

QUE SE CORRE (todo por corre_pas.tarea, que ES corre_v143.tarea + telemetria de solo lectura; regla 14 en el arnes):
  Por semilla-indice i (0..19) de una serie:
  CADENA pasg: 10 pasajes de T 25 000 de V143_PAS con PS_MUT p 0 (solo el gen g; cerebro fijo en G0); al final de cada pasaje la SIEMBRA
               del siguiente = (g, b) de los VIVOS en los ultimos 5 000 pasos (corre_pas.siembra: no ve R0, hijos ni cruza).
  CADENA ctl:  los MISMOS 10 pasajes (mismas semillas de pista) de V143_PAS con p 0 y SIN transferencia (fundadores siempre de la inicial
               g ~ U[-0.1, 0.1]). Con p 0 y sin siembra, V143_PAS == V143_EVO_BAJO bit a bit (arnes). En el pasaje 0, pasg == ctl bit a bit.
  PRUEBA A T 100 000 (semilla de pista propia de i): pasg con la siembra FIJA del ultimo pasaje de SU cadena · ctl (inicial) · v143 ·
               termo (V143_TERMO, g 0.40 disenado) · o1 (ancla de la pista).
SEMILLAS (grep 28-sep 21:55: 596xxx libre en py/md/txt/log/json de PROYECTOS/JUACO):
  serie:   pasaje p de la cadena i -> 596000 + 10 i + p (596000-596199); prueba T 100k de i -> 596201 + i (596201-596220)
  replica: pasaje p de la cadena i -> 596300 + 10 i + p (596300-596499); prueba T 100k de i -> 596501 + i (596501-596520)
  practica (arnes y humo): 596900-596999.
Pool: fase 1 = 40 cadenas (pasg y ctl) + 80 pruebas sin siembra (ctl, v143, termo, o1); fase 2 = 20 pruebas pasg (dependen de su cadena).
nube-9: trabajo() atrapa TODO y devuelve 'aborto'; JSON por trabajo ANTES de volver (ERR-54); --reanuda salta los hechos. Cualquier aborto
-> NO SE LEE.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN; SOLO el coordinador lanza --serie/--replica):
  python experimentos/organelos/reunion/opusB/corre_termostato.py --humo                 # 1 proceso, 6 corridas, T 5 000, practica
  python experimentos/organelos/reunion/opusB/corre_termostato.py --serie --pool 6       # serie   (20 indices)
  python experimentos/organelos/reunion/opusB/corre_termostato.py --replica --pool 6     # replica (solo si la serie no da NO)
  python experimentos/organelos/reunion/opusB/corre_termostato.py --serie --pool 6 --reanuda
  python experimentos/organelos/reunion/opusB/corre_termostato.py --bloque <resumen serie>.json,<resumen replica>.json
"""
import argparse, hashlib, json, os, platform, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_pas as CPS          # tarea, siembra, registra (se IMPORTA, no se toca; sha fijado)
CV = CPS.CV; P = CPS.P; RAIZ = CPS.RAIZ

PRERREGISTRO = 'PREREGISTRO_termostato_pista.md'
DATOS = os.path.join(AQUI, 'datos_termostato')
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3'); PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
SHAS = {os.path.join(AQUI, 'corre_pas.py'): '49322105ff725569', os.path.join(AQUI, 'construye_pas.py'): 'db39a13617113793',
        os.path.join(AQUI, 'carros', 'V143_PAS.py'): 'd9dd7fb0187a0bc6', os.path.join(AQUI, 'carros', 'V143_PAS0.py'): '598a98a13aa1f754',
        os.path.join(RAIZ, 'experimentos', 'organelos', 'termo', 'carros', 'V143_TERMO.py'): '3db639cab75641fb',
        os.path.join(RAIZ, 'experimentos', 'organelos', 'termo_banco', 'carros', 'V143_EVO_BAJO.py'): '3187b373654e119f',
        os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028'}
# brazo -> (carro, transfiere, p de mutacion del cerebro)
BRAZOS = {'pasg': ('V143_PAS', 1, 0.0), 'ctl': ('V143_PAS', 0, 0.0), 'v143': ('V143', 0, 0.0), 'termo': ('V143_TERMO', 0, 0.0),
          'o1': ('O1', 0, 0.0)}
PRUEBA_BRAZOS = ('pasg', 'ctl', 'v143', 'termo', 'o1'); CADENA_BRAZOS = ('pasg', 'ctl')
BASES = {'serie': (596000, 596201), 'replica': (596300, 596501)}
N_IND = 20; NPAS = 10; T_PAS = 25000; T_PRU = 100000
HUMO = dict(npas=2, T_pas=5000, T_pru=5000, base=(596900, 596990), n=1, prueba=('pasg', 'v143'))   # 2+2+2 = 6 corridas, 30 000 pasos
GANA = 15; DIF_MOD = 0.10; BANDA_G = (0.10, 0.60); LETAL = 0.10; CTL_MAX = 5; ANCLA_V143 = (0.40, 0.80)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sem_pas(base, i, p): return base[0] + 10 * i + p
def sem_pru(base, i): return base[1] + i


def _med(xs):
    xs = [x for x in xs if x is not None]; return round(float(st.median(xs)), 4) if xs else None


def fila(x, T):
    L = x['linajes']
    tel = x.get('tel_ps')
    fp = [f for v in tel.values() for f in v.get('fund_ps', [])] if tel else []
    return dict(seed=x['seed'], T=T, R0_real=[l['R0_real'] for l in L], R0_med=_med([l['R0_real'] for l in L]),
                fund=[l['fundadores'] for l in L], fund_post10k=[l['fund_post10k'] for l in L], cruza=[int(l['cruza_real']) for l in L],
                cruzan=sum(int(l['cruza_real']) for l in L), mayoria=int(sum(int(l['cruza_real']) for l in L) * 2 > len(L)),
                coherente=all(l.get('coherente', True) for l in L),
                fund_de_siembra=sum(f[0] for f in fp), fund_n=len(fp), g_fund_media=(round(sum(f[1] for f in fp) / len(fp), 4) if fp else None))


def g_de(sie):
    if not sie: return None
    return round(sum(s['g'] for s in sie) / len(sie), 4)


def cadena(i, brazo, base, npas, T):
    carro, trans, pm = BRAZOS[brazo]; sie = None; F = []
    for p in range(npas):
        x = CPS.tarea(sem_pas(base, i, p), carro, T, siembra=(sie if trans else None), pmut=pm)
        sig = CPS.siembra({k: v.get('vivos_b', []) for k, v in x['tel_ps'].items()}, T)
        f = fila(x, T); f['p'] = p; f['g_siembra'] = g_de(sig); f['n_siembra'] = len(sig or []); F.append(f)
        if trans: sie = sig
    return dict(pasajes=F, siembra_final=(sie if trans else sig))


def trabajo(args):
    """UN trabajo: ('cadena', i, brazo) o ('prueba', i, brazo). Atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54)."""
    tipo, i, brazo, base, npas, T_pas, T_pru, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{tipo}_i{i:02d}_{brazo}.json")
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: return json.load(fh)
    t0 = time.time()
    try:
        CPS.registra()
        if tipo == 'cadena':
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, **cadena(i, brazo, base, npas, T_pas))
        else:
            carro, trans, pm = BRAZOS[brazo]; sie = None
            if trans:
                with open(os.path.join(carpeta, f"cadena_i{i:02d}_{brazo}.json"), encoding='utf-8') as fh: c = json.load(fh)
                if c.get('aborto') or not c.get('siembra_final'): raise RuntimeError("cadena sin siembra final")
                sie = c['siembra_final']
            y = CPS.tarea(sem_pru(base, i), carro, T_pru, siembra=sie, pmut=pm)
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, g_siembra_usada=g_de(sie), **fila(y, T_pru))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo=tipo, i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_termostato_pista.md sec. 6)
def pareado(A, B):
    """A, B: {i: R0_med}. gana = indices en que A > B (empate no gana); dif = mediana de A - B."""
    I = sorted(set(A) & set(B)); d = [A[i] - B[i] for i in I]
    return dict(n=len(I), gana=sum(1 for z in d if z > 0), dif_med=(round(float(st.median(d)), 4) if d else None))


def lee_serie(C, R, n, abortos):
    """C[brazo][i] = cadena; R[brazo][i] = prueba T 100k. n = indices esperados."""
    v = {}
    v['V1_completa'] = bool(abortos == 0 and all(len(C.get(b, {})) == n for b in CADENA_BRAZOS)
                            and all(len(R.get(b, {})) == n for b in PRUEBA_BRAZOS)
                            and all(R[b][i]['coherente'] for b in PRUEBA_BRAZOS for i in R.get(b, {})))
    v['V2_p0_pasg_eq_ctl'] = bool(n and all(
        C['pasg'][i]['pasajes'][0][k] == C['ctl'][i]['pasajes'][0][k] for i in C.get('pasg', {}) if i in C.get('ctl', {})
        for k in ('R0_real', 'fund', 'fund_post10k', 'cruza')) and len(C.get('pasg', {})) == n)
    m = _med([R['v143'][i]['R0_med'] for i in R.get('v143', {})])
    v['V3_ancla_v143'] = m is not None and ANCLA_V143[0] <= m <= ANCLA_V143[1]
    v['V4_ancla_o1'] = sum(R['o1'][i]['mayoria'] for i in R.get('o1', {})) >= GANA * n / 20
    v['V5_siembra_actua'] = bool(R.get('pasg')) and all(R['pasg'][i]['fund_n'] > 0 and R['pasg'][i]['fund_de_siembra'] == R['pasg'][i]['fund_n']
                                                        for i in R['pasg'])
    valido = all(v.values())
    r0 = {b: {i: R[b][i]['R0_med'] for i in R.get(b, {})} for b in PRUEBA_BRAZOS}
    par = {f"{a}_vs_{b}": pareado(r0[a], r0[b]) for a, b in (('pasg', 'v143'), ('pasg', 'ctl'), ('pasg', 'termo'), ('ctl', 'v143'), ('termo', 'v143'), ('o1', 'v143'))}
    gp = {i: C['pasg'][i]['pasajes'][-1]['g_siembra'] for i in C.get('pasg', {})}
    g0 = {i: C['pasg'][i]['pasajes'][0]['g_siembra'] for i in C.get('pasg', {})}
    gc = {i: C['ctl'][i]['pasajes'][-1]['g_siembra'] for i in C.get('ctl', {})}
    en = lambda g: g is not None and BANDA_G[0] <= g <= BANDA_G[1]
    p = {}
    p['PA_pasg_gana_v143'] = par['pasg_vs_v143']['gana'] >= GANA * n / 20
    p['PA_pasg_gana_ctl'] = par['pasg_vs_ctl']['gana'] >= GANA * n / 20
    sube = [i for i in gp if g0[i] is not None and g0[i] < LETAL and en(gp[i])]
    p['PB_g_sube_a_banda'] = len(sube) >= GANA * n / 20
    p['PC_ctl_no_sube'] = sum(1 for i in gc if en(gc[i])) <= CTL_MAX * n / 20
    mod = bool(p['PA_pasg_gana_ctl'] and par['pasg_vs_ctl']['dif_med'] is not None and par['pasg_vs_ctl']['dif_med'] >= DIF_MOD - 1e-12
               and _med(list(gp.values())) is not None and _med(list(gp.values())) >= BANDA_G[0])
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif mod: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    desc = dict(g_siembra_pasg_ultimo=gp, g_siembra_pasg_p0=g0, g_siembra_ctl_ultimo=gc, indices_que_suben=len(sube),
                R0_med={b: _med(list(r0[b].values())) for b in r0}, mayorias={b: sum(R[b][i]['mayoria'] for i in R.get(b, {})) for b in PRUEBA_BRAZOS},
                fund_por_linaje={b: _med([st.mean(R[b][i]['fund']) for i in R.get(b, {})]) for b in PRUEBA_BRAZOS if R.get(b)},
                pasg_aprox_termo=par['pasg_vs_termo'])
    return dict(validez=v, puertas=p, modesto=mod, veredicto=ver, pareados=par, descriptivo=desc)


ORDEN = {'NO SE LEE': -1, 'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}


def bloque(a, b): return a if a == b else min((a, b), key=lambda z: ORDEN[z])


def verifica(log):
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for nm, b in CPS.CB.todas().items():
        igual = open(os.path.join(CPS.CARROS, nm + '.py'), 'rb').read() == b; ok &= igual
        log(f"  carro {nm} == construye_pas: {igual}")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--serie', action='store_true')
    g.add_argument('--replica', action='store_true'); g.add_argument('--bloque', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115
    if a.bloque:
        rs = [json.load(open(x.strip(), encoding='utf-8')) for x in a.bloque.split(',')]
        if len(rs) != 2 or rs[0]['modo'] != 'serie' or rs[1]['modo'] != 'replica':
            raise SystemExit("--bloque: <resumen serie>,<resumen replica> (en ese orden)")
        vb = bloque(rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto'])
        print(f"serie {rs[0]['letra']['veredicto']} · replica {rs[1]['letra']['veredicto']} -> BLOQUE: {vb}  ({PRERREGISTRO} sec. 6-7)")
        return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        modo = 'humo'; base = HUMO['base']; n = HUMO['n']; npas = HUMO['npas']; Tp = HUMO['T_pas']; Tr = HUMO['T_pru']; pru = HUMO['prueba']
    else:
        modo = 'serie' if a.serie else 'replica'; base = BASES[modo]; n = N_IND; npas = NPAS; Tp = T_PAS; Tr = T_PRU; pru = PRUEBA_BRAZOS
    sel = time.strftime('%Y%m%d_%H%M%S'); pre = f"termostato_{modo}"
    os.makedirs(DATOS, exist_ok=True)
    prev = sorted(d for d in os.listdir(DATOS) if d.startswith(pre + '_'))
    carpeta = os.path.join(DATOS, prev[-1] if (a.reanuda and prev and modo != 'humo') else pre + '_' + sel)
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    t0 = time.time()
    log(f"CORRE_TERMOSTATO · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO'} · corre_termostato.py "
        f"{h16(os.path.abspath(__file__))} · preregistro {PRERREGISTRO} · semillas pasaje {sem_pas(base, 0, 0)}-{sem_pas(base, n-1, npas-1)} · "
        f"prueba {sem_pru(base, 0)}-{sem_pru(base, n-1)} · T pasaje {Tp} · T prueba {Tr} · {carpeta}")
    if not verifica(log): log("  ALGO FALLA -> no se corre."); return 1
    f1 = [('cadena', i, b, base, npas, Tp, Tr, carpeta, a.reanuda) for i in range(n) for b in CADENA_BRAZOS]
    f1 += [('prueba', i, b, base, npas, Tp, Tr, carpeta, a.reanuda) for i in range(n) for b in pru if not BRAZOS[b][1]]
    f2 = [('prueba', i, b, base, npas, Tp, Tr, carpeta, a.reanuda) for i in range(n) for b in pru if BRAZOS[b][1]]
    X = []

    def corre(tareas):
        if a.pool and a.pool > 1:
            from multiprocessing import Pool
            with Pool(a.pool) as PL:
                for x in PL.imap_unordered(trabajo, tareas):
                    X.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['tipo']} i{x['i']} {x['brazo']} ({x['seg']}s) aborto {x['aborto']} "
                                     f"R0 {x.get('R0_med')} g {x.get('g_siembra_usada') or [q['g_siembra'] for q in x.get('pasajes', [])][-1:]}")
        else:
            for ar in tareas:
                x = trabajo(ar); X.append(x)
                log(f"  [{time.time()-t0:7.1f}s] {x['tipo']} i{x['i']} {x['brazo']} ({x['seg']}s) aborto {x['aborto']} R0 {x.get('R0_med')} "
                    f"fund {x.get('fund')} g por pasaje {[q['g_siembra'] for q in x.get('pasajes', [])]} g usada {x.get('g_siembra_usada')}")
    corre(f1); corre(f2)
    abortos = sum(1 for x in X if x['aborto'])
    C = {b: {x['i']: x for x in X if x['tipo'] == 'cadena' and x['brazo'] == b and not x['aborto']} for b in CADENA_BRAZOS}
    R = {b: {x['i']: x for x in X if x['tipo'] == 'prueba' and x['brazo'] == b and not x['aborto']} for b in PRUEBA_BRAZOS}
    letra = lee_serie(C, R, n, abortos)
    log(f"\n================ LA LETRA ({PRERREGISTRO} sec. 6)" + (" -- HUMO: T corto, practica, 2 brazos de prueba: NO cuenta" if a.humo else ""))
    for k in ('validez', 'puertas', 'pareados', 'descriptivo'): log(f"  {k}: {letra[k]}")
    ver = ('HUMO (no cuenta): ' if a.humo else '') + letra['veredicto']
    rj = os.path.join(carpeta, 'resumen.json')
    json.dump(dict(modo=modo, letra=letra, abortos=abortos, n=n, npas=npas, T_pas=Tp, T_pru=Tr, preregistro=PRERREGISTRO,
                   sha_runner=h16(os.path.abspath(__file__))), open(rj, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {abortos} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO DE LA {modo.upper()}: {ver}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
