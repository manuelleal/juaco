"""corre_bp.py — BLOQUES_PISTA (28-sep-2026, creador; EXPLORATORIO, no es serie). Preregistro: PREREGISTRO_bloques_pista.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros, y solo con seleccion natural.

ENTRADA (regla 14): la corrida ES experimentos/organelos/termo/corre_termo.tarea (se IMPORTA, no se toca; sha fijado) =
corre_v143.tarea = juez.tarea(seed, 9 carros iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador limpio 1). Lo unico
agregado: x['bq'] = telemetria de SOLO LECTURA del modulo del carro (_BQ_TEL, _BQ_BANCO) leida DESPUES del run (no puntua).
BRAZOS: termo (V143_TERMO) · bloq (V143_BQ: reglas heredables + banco del linaje) · bloqaza (V143_BQAZA: sin herencia) · o1 (O1).
SEMILLAS (grep 28-sep 21:00: 592xx libre en py/md/txt): exploracion 59201-59205 · humo 59291 · arnes 59292.
Sin Pool. Un proceso por invocacion; cada corrida escribe su JSON antes de seguir (ERR-54); --explora salta las que ya estan.

  python experimentos/organelos/bloques_pista/corre_bp.py --arnes                     # identidad (escribe identidad_bp_salida.txt)
  python experimentos/organelos/bloques_pista/corre_bp.py --humo                      # 5 corridas T 20 000, s 59291, escribe JSON
  python experimentos/organelos/bloques_pista/corre_bp.py --explora --semillas 59201,59202 --brazos termo,bloq,bloqaza,o1
  python experimentos/organelos/bloques_pista/corre_bp.py --lee datos/explora_T100000
"""
import argparse, copy, hashlib, importlib.util, json, os, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
TERMOD = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')
for _d in (AQUI, TERMOD):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_termo as CT          # tarea, cuerpos, establece, verifica (se IMPORTA, no se toca)
import construye_bp as CB
import construye_bp2 as CB2
CV = CT.CV; P = CT.P; RC = CT.RC
CARROS = os.path.join(AQUI, 'carros'); DATOS = os.path.join(AQUI, 'datos')
SHAS = {os.path.join(TERMOD, 'corre_termo.py'): None, os.path.join(TERMOD, 'carros', 'V143_TERMO.py'): '3db639cab75641fb'}
BRAZOS = {'termo': 'V143_TERMO', 'bloq': 'V143_BQ', 'bloqaza': 'V143_BQAZA', 'o1': 'O1', 'bloq2': 'V143_BQ2', 'bloq2aza': 'V143_BQ2AZA'}
LEE_BRAZOS = ('termo', 'bloq', 'bloqaza', 'o1', 'bloq_pas', 'bloqaza_pas', 'prueba_forzada', 'bloq2', 'bloq2aza', 'bloq2_pas', 'bloq2aza_pas')
PROPIOS = ('V143_BQ', 'V143_BQAZA', 'V143_BQ0', 'V143_BQ2', 'V143_BQ2AZA')
SEM_EXPLORA = range(59201, 59211); SEM_HUMO = 59291; SEM_ARNES = 59292
RECHAZO = [[3.0, 4.0, 1.0, 0.5, 0.0, -3.0]]
# SOLO diagnostico v2 (humo2): la regla PRUEBA de O1 escrita en reglas: 'desconocida -> boca -3' + 'reserva > 0.5 -> boca +3'
PRUEBA_O1 = [[7.0, 0.0, 0.0, 0.5, 0.0, -3.0], [8.0, 0.0, 1.0, 0.5, 0.0, 3.0]]   # SOLO humo/arnes: "no muerdas lo que tiene el pixel 4" (separa B, D de A, C)


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def registra():
    CT.registra()
    for n in PROPIOS:
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", os.path.join(CARROS, n + '.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    for k, v in BRAZOS.items(): CV.BRAZOS.setdefault(k, v)


def prepara(ident, seed, cfg=None, forzada=None, siembra=None):
    m = CV._MODS.get(ident)
    if m is None or not hasattr(m, '_BQ_BANCO'): return None
    m._BQ_BANCO.clear(); m._BQ_CNT.clear(); m._BQ_TEL.clear(); m.BQ_SEMILLA = int(seed); m.BQ_FORZADA = forzada
    m.BQ_C = dict(CFG0 if cfg is None else cfg)
    if siembra:   # PASAJES: el banco de cada linaje arranca con una muestra de la siembra (rng del RUNNER, no del carro)
        rr = np.random.default_rng([int(seed), 7901]); nb = int(m.BQ_C['banco'])
        for i in range(9):
            ix = rr.choice(len(siembra), size=min(nb, len(siembra)), replace=False)
            m._BQ_BANCO[i] = [[list(map(float, r)) for r in siembra[int(j)]] for j in ix]
    return m


def siembra_de(x):
    """La siembra del pasaje siguiente = union de los bancos finales de los 9 linajes (solo entra quien pario, en 'padre')."""
    return [R for B in x['bq']['banco'].values() for R in B if R]


def tarea(seed, brazo, T, cfg=None, forzada=None, siembra=None):
    registra()
    ident = BRAZOS.get(brazo, brazo); m = prepara(ident, seed, cfg, forzada, siembra)
    x = CT.tarea((seed, ident, T)); x.pop('pizarra_log', None)
    x['brazo'] = brazo; x['aborto'] = None
    if m is not None:
        x['bq'] = dict(cfg=dict(m.BQ_C), forzada=forzada, tel={str(i): copy.deepcopy(v) for i, v in m._BQ_TEL.items()},
                       banco={str(i): copy.deepcopy(v) for i, v in m._BQ_BANCO.items()})
    return x


CFG0 = None


def _cfg_carro():
    global CFG0
    registra(); CFG0 = dict(CV._MODS['V143_BQ'].BQ_C)


# ------------------------------------------------------------------ lectura
def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def regla_txt(r):
    s, j, c, th, a, w = int(r[0]), int(r[1]), int(r[2] > 0.5), r[3], int(r[4]), r[5]
    sen = ['hambre', 'sed', 'cercania de lo que mira', f'pixel {j} de la letra en foco', f'pixel {j} de la ultima mordida',
           'R de la ultima mordida', f'cercania del objeto mas cercano con pixel {j}', 'la letra en foco ya fue mordida por el linaje',
           'reserva min(E, Ag)'][s]
    acc = ['boca', 'patas hacia lo que mira', 'quedarse'][a]
    return f"{sen} {'>' if c else '<'} {th:.2f} -> {acc} {w:+.2f}"


def es_rechazo(r):
    """Organo de rechazo por la retina: baja la boca sobre B y D y no sobre A y C (pixel 4 = 1 solo en B, D; pixel 1 = 0 solo en B, D)."""
    s, j, c, th, a, w = int(r[0]), int(r[1]), int(r[2] > 0.5), r[3], int(r[4]), r[5]
    return a == 0 and w < 0 and s == 3 and ((j == 4 and c == 1 and th < 1.0) or (j == 1 and c == 0 and th > 0.0))


def es_prueba(r):
    """v2: 'lo desconocido no se muerde' (sentido 7 < th -> boca negativa) o 'con reserva baja no se muerde' (sentido 8 < th -> boca negativa)."""
    s, c, a, w = int(r[0]), int(r[2] > 0.5), int(r[4]), r[5]
    return a == 0 and w < 0 and s in (7, 8) and c == 0


def resumen(R, brazo):
    L = [l for c in R for l in c['linajes']]
    por_sem = [st.median([l['R0_real'] for l in c['linajes']]) for c in R]
    may = sum(1 for c in R if sum(l['cruza_real'] for l in c['linajes']) * 2 > len(c['linajes']))
    est = [l for l in L if l['fund_post10k'] == 0]
    cz = CT.cuerpos(R)
    fc = cz['fundadores']['causas']; nf = max(1, sum(fc.values()))
    out = dict(brazo=brazo, n=len(R), R0_real_med_sem=med(por_sem), R0_real_por_sem=[round(x, 3) for x in por_sem],
               mayoria_cruza=f"{may}/{len(R)}", linajes_cruzan=f"{sum(l['cruza_real'] for l in L)}/{len(L)}",
               fund_media=round(sum(l['fundadores'] for l in L) / max(1, len(L)), 1), fund_mediana=med([l['fundadores'] for l in L]),
               establecidos=f"{len(est)}/{len(L)}", fund_mediana_establecidos=med([l['fundadores'] for l in est]),
               fund_causas=fc, fund_frac_veneno_sal=round((fc.get('veneno', 0) + fc.get('sal', 0)) / nf, 3),
               fund_vida_med=cz['fundadores']['vida_med'], fund_hijos_por_cuerpo=cz['fundadores']['hijos_por_cuerpo'],
               hijos_cola=cz['hijos_de_cola'], frac_sin_bueno_mundo=med([c['pista'].get('frac_sin_bueno_mundo') for c in R]),
               mord_BD_med=med([l['mord']['B'] + l['mord']['D'] for l in L]), mord_AC_med=med([l['mord']['A'] + l['mord']['C'] for l in L]))
    if all('bq' in c for c in R):
        suelo = [s[1] for c in R for s in (c['bq']['tel'].get('0') or {}).get('suelo', [])]
        out['AC_en_anillo_med'] = med(suelo)
        reglas = {}; n_rech = 0; n_prue = 0; n_lin = 0; largo = []; n_s6 = 0; banco_n = []
        for c in R:
            for i, B in c['bq']['banco'].items():
                if not B: continue
                n_lin += 1; banco_n.append(len(B)); ult = B[-10:]
                largo.append(st.mean(len(x) for x in ult))
                if any(es_rechazo(r) for x in ult for r in x): n_rech += 1
                if any(es_prueba(r) for x in ult for r in x): n_prue += 1
                if any(int(r[0]) == 6 for x in ult for r in x): n_s6 += 1
                for x in ult:
                    for r in x:
                        k = (int(r[0]), int(r[1]), int(r[2] > 0.5), int(r[4]), int(np.sign(r[5])) if False else (1 if r[5] > 0 else -1))
                        reglas[k] = reglas.get(k, 0) + 1
        top = sorted(reglas.items(), key=lambda z: -z[1])[:6]
        out['banco'] = dict(linajes_con_banco=n_lin, con_rechazo=n_rech, con_prueba_v2=n_prue, con_sentido6=n_s6, largo_med=med(largo),
                            top=[[f"sentido {k[0]} j {k[1]} {'>' if k[2] else '<'} accion {k[3]} signo {k[4]:+d}", v] for k, v in top])
        # reglas del cuerpo vivo al final (muestra mas tardia de cada linaje)
        fin = []
        for c in R:
            for i, t in c['bq']['tel'].items():
                if t['muestras']: fin.append((c['seed'], i, t['muestras'][-1][1]))
        out['vivos_final_con_rechazo'] = f"{sum(1 for _, _, x in fin if any(es_rechazo(r) for r in x))}/{len(fin)}"
        out['fund_de_banco'] = f"{sum(f[1] == 1 for c in R for t in c['bq']['tel'].values() for f in t['fund'])}/" \
                               f"{sum(len(t['fund']) for c in R for t in c['bq']['tel'].values())}"
    return out


def lee(carpeta, log=print):
    R = [json.load(open(os.path.join(carpeta, f), encoding='utf-8')) for f in sorted(os.listdir(carpeta)) if f.endswith('.json') and '_s' in f]
    por = {}
    for x in R:
        if x.get('aborto'): log(f"  ABORTO {x['brazo']} s{x['seed']}: {x['aborto']}"); continue
        por.setdefault(x['brazo'], []).append(x)
    res = {}
    for b in LEE_BRAZOS:
        if b in por:
            por[b].sort(key=lambda z: z['seed']); res[b] = resumen(por[b], b)
            log(f"\n== {b} · semillas {[c['seed'] for c in por[b]]}")
            for k, v in res[b].items():
                if k not in ('brazo',): log(f"  {k}: {v}")
    log("\nPAREADOS (mediana del R0 real de los 9 linajes por semilla)")
    par = {}
    for a, b in (('bloq', 'termo'), ('bloq', 'bloqaza'), ('bloqaza', 'termo'), ('o1', 'termo'), ('bloq', 'o1'),
                 ('bloq_pas', 'termo'), ('bloq_pas', 'bloq'), ('bloq_pas', 'bloqaza_pas'), ('bloqaza_pas', 'termo'), ('bloq_pas', 'o1'),
                 ('prueba_forzada', 'termo'), ('prueba_forzada', 'o1'), ('bloq2', 'termo'), ('bloq2', 'bloq2aza'), ('bloq2', 'bloq'),
                 ('bloq2aza', 'termo'), ('bloq2_pas', 'termo'), ('bloq2_pas', 'bloq2aza_pas')):
        if por.get(a) and por.get(b):
            par[f"{a}_vs_{b}"] = CV.pareado(por[a], por[b]); log(f"  {a} vs {b}: {par[f'{a}_vs_{b}']}")
    # reglas fijadas por linaje (bloq): las mas frecuentes del banco al final, en palabras
    for bb in ('bloq', 'bloq_pas', 'bloq2', 'bloq2_pas'):
        if not por.get(bb): continue
        log(f"\nREGLAS DEL BANCO AL FINAL ({bb}; por linaje: la lista mas reciente del banco)")
        for c in por[bb]:
            for i, B in sorted(c['bq']['banco'].items(), key=lambda z: int(z[0])):
                if B: log(f"  s{c['seed']} L{i} (fund {c['linajes'][int(i)]['fundadores']}, R0 {c['linajes'][int(i)]['R0_real']}): "
                          + ' | '.join(regla_txt(r) for r in B[-1]))
    out = os.path.join(carpeta, 'resumen_bp.json')
    with open(out, 'w', encoding='utf-8') as fh: json.dump(dict(brazos=res, pareados=par), fh, ensure_ascii=False, indent=1)
    log(f"\nRESUMEN {out}")
    return res, par


import numpy as np   # noqa: E402 (solo para la lectura)


# ------------------------------------------------------------------ arnes
def arnes(log):
    ok = True; N = lambda x: json.loads(json.dumps(x, default=str))
    registra()
    log(f"(K) construye_bp --verifica, shas y revisa_carro")
    for n, b in list(CB.todas().items()) + list(CB2.todas().items()):
        ruta = os.path.join(CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = RC.revisa_fuente(b.decode('utf-8'), n); ok &= igual and not vr
        log(f"  carro {n} sha {CB.h16b(b)} == construye: {igual} · revisa_carro: {'PASA' if not vr else vr[:2]}")
    s = h16(CB.ORIGEN); ok &= s == CB.SHA_TERMO; log(f"  origen V143_TERMO {s} fijado {CB.SHA_TERMO}: {'OK' if s == CB.SHA_TERMO else 'FALLA'}")
    log(f"  corre_termo.py sha {h16(os.path.join(TERMOD, 'corre_termo.py'))} (importado sin tocar) · corre_bp.py {h16(os.path.abspath(__file__))}")
    ok &= CT.verifica(log)   # shas fijados de corre_termo (pista, juez, O1, V143, TERMO) + identidad corta TERMO=0 == V143
    T = 2000; sd = SEM_ARNES
    base = N(P.run(sd, [('C', CV._MODS['V143_TERMO'])] * 9, T=T, fundador_limpio=1))
    cero = dict(inicial=0, p_campo=0.0, p_dup=0.0, p_del=0.0, p_ins=0.0, banco=50)
    log(f"(A) BLOQ = 0 == V143_TERMO (salida ENTERA de pista.run, N 9, s {sd}, T {T}, fundador limpio)")
    prepara('V143_BQ0', sd); i = N(P.run(sd, [('C', CV._MODS['V143_BQ0'])] * 9, T=T, fundador_limpio=1)) == base; ok &= i
    log(f"  V143_BQ0: {'OK' if i else 'FALLA'}")
    log("(B) BLOQ = 1, genoma vacio (INICIAL 0) y tasas 0 == V143_TERMO (salida ENTERA)")
    for n in ('V143_BQ', 'V143_BQAZA', 'V143_BQ2', 'V143_BQ2AZA'):
        prepara(n, sd, cero); i = N(P.run(sd, [('C', CV._MODS[n])] * 9, T=T, fundador_limpio=1)) == base; ok &= i
        log(f"  {n}: {'OK' if i else 'FALLA'}")
    log("(C) controles que DEBEN diferir: tasas de exploracion; organo de rechazo forzado (y ACTUA: menos mordidas B+D)")
    for n in ('V143_BQ', 'V143_BQAZA', 'V143_BQ2', 'V143_BQ2AZA'):
        prepara(n, sd); d = N(P.run(sd, [('C', CV._MODS[n])] * 9, T=T, fundador_limpio=1)) != base; ok &= d
        log(f"  {n} con tasas de exploracion != TERMO: {'OK (difiere)' if d else 'FALLA (igual)'}")
    prepara('V143_BQ', sd, cero, RECHAZO); xf = P.run(sd, [('C', CV._MODS['V143_BQ'])] * 9, T=T, fundador_limpio=1)
    Lb = [CV.J.resumen_linaje(dd, sd) for dd in base['linajes']]; Lf = [CV.J.resumen_linaje(dd, sd) for dd in N(xf)['linajes']]
    bd0 = sum(l['mord']['B'] + l['mord']['D'] for l in Lb); bd1 = sum(l['mord']['B'] + l['mord']['D'] for l in Lf)
    ac0 = sum(l['mord']['A'] + l['mord']['C'] for l in Lb); ac1 = sum(l['mord']['A'] + l['mord']['C'] for l in Lf)
    a = bd1 < bd0; ok &= a
    log(f"  rechazo forzado: mordidas B+D {bd0} -> {bd1}, A+C {ac0} -> {ac1}: {'OK (actua)' if a else 'FALLA'}")
    prepara('V143_BQ2', sd, cero, PRUEBA_O1); xp = N(P.run(sd, [('C', CV._MODS['V143_BQ2'])] * 9, T=T, fundador_limpio=1))
    Lp = [CV.J.resumen_linaje(dd, sd) for dd in xp['linajes']]; d = xp != base; ok &= d
    log(f"  v2 PRUEBA_O1 forzada != TERMO: {'OK' if d else 'FALLA'} · mordidas B+D {bd0} -> {sum(l['mord']['B'] + l['mord']['D'] for l in Lp)}, "
        f"A+C {ac0} -> {sum(l['mord']['A'] + l['mord']['C'] for l in Lp)} · fundadores {sum(l['fundadores'] for l in Lb)} -> {sum(l['fundadores'] for l in Lp)}")
    log("(E) regla 14: ENTRADA campo a campo. tarea de este runner (termo) == corre_termo.tarea; bloq con genoma vacio y tasas 0 == termo")
    x = N(tarea(sd, 'termo', T)); y = N(CT.tarea((sd, 'V143_TERMO', T))); y.pop('pizarra_log', None)
    ks = sorted(set(x) | set(y) - {'seg', 'brazo', 'aborto'})
    e = all(x.get(k) == y.get(k) for k in ks if k not in ('seg', 'brazo', 'aborto')); ok &= e
    log(f"  termo: {len(ks)} campos, {'OK' if e else 'FALLA ' + str([k for k in ks if x.get(k) != y.get(k)][:5])}")
    z = json.loads(json.dumps(N(tarea(sd, 'bloq', T, cfg=cero))).replace('V143_BQ#', 'V143_TERMO#'))   # el id lleva el nombre del carro
    kz = [k for k in ks if k not in ('seg', 'brazo', 'aborto', 'bq')]
    e2 = all(z.get(k) == y.get(k) for k in kz); ok &= e2
    log(f"  bloq vacio tasas 0 == termo campo a campo ({len(kz)} campos; ids con el nombre del carro normalizado): "
        f"{'OK' if e2 else 'FALLA ' + str([k for k in kz if z.get(k) != y.get(k)][:5])}")
    log("(H) herencia exacta con tasas 0 e INICIAL 1: toda muestra de cuerpo vivo de un linaje es la lista de algun fundador del linaje")
    cfg1 = dict(cero, inicial=1)
    for b in ('bloq',):
        prepara(BRAZOS[b], sd, cfg1); P.run(sd, [('C', CV._MODS[BRAZOS[b]])] * 9, T=T, fundador_limpio=1)
        m = CV._MODS[BRAZOS[b]]; tot = 0; bien = 0
        for i, t in m._BQ_TEL.items():
            funds = [r for r in m._BQ_BANCO.get(i, [])]
            for tt, R in t['muestras']:
                tot += 1; bien += int(len(R) == 1)
        h = tot > 0 and bien == tot; ok &= h
        log(f"  {b}: muestras con exactamente 1 regla (sin mutacion no cambia el largo) {bien}/{tot}: {'OK' if h else 'FALLA'}")
    log("(D) determinismo: bloq con tasas de exploracion, dos veces")
    a1 = N(tarea(sd, 'bloq', T)); a2 = N(tarea(sd, 'bloq', T)); a1.pop('seg'); a2.pop('seg'); d = a1 == a2; ok &= d
    log(f"  {'OK' if d else 'FALLA'}")
    log(f"ARNES: {'PASA' if ok else 'FALLA'}")
    return ok


def trabajo(seed, brazo, T, carpeta, log, cfg=None, forzada=None, etiqueta=None, siembra=None):
    fin = os.path.join(carpeta, f"{etiqueta or brazo}_s{seed}.json")
    if os.path.exists(fin):
        log(f"  ya esta {fin}"); return json.load(open(fin, encoding='utf-8'))
    t0 = time.time()
    try:
        x = tarea(seed, brazo, T, cfg, forzada, siembra)
        if siembra is not None: x['siembra_n'] = len(siembra)
        if etiqueta: x['brazo'] = etiqueta
    except BaseException as e:   # noqa: nube-9
        x = dict(seed=seed, brazo=etiqueta or brazo, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    L = x.get('linajes', [])
    log(f"  [{time.time()-t0:6.1f}s] {x['brazo']} s{seed} T {T} aborto {x.get('aborto')} · R0 real {[l['R0_real'] for l in L]} · "
        f"fundadores {[l['fundadores'] for l in L]}")
    return x


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--arnes', action='store_true'); g.add_argument('--humo', action='store_true')
    g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    g.add_argument('--pasajes', action='store_true'); g.add_argument('--humo2', action='store_true')
    ap.add_argument('--cadenas', default=None); ap.add_argument('--np', type=int, default=4); ap.add_argument('--Tp', type=int, default=25000)
    ap.add_argument('--semillas', default=None); ap.add_argument('--brazos', default='termo,bloq,bloqaza,o1')
    ap.add_argument('--T', type=int, default=100000)
    a = ap.parse_args(argv)   # ERR-115
    _cfg_carro()
    if a.lee:
        c = a.lee if os.path.isabs(a.lee) else os.path.join(AQUI, a.lee)
        LOGF = open(os.path.join(c, 'lectura.txt'), 'w', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        lee(c, log); return 0
    if a.arnes:
        LOGF = open(os.path.join(AQUI, 'identidad_bp_salida.txt'), 'w', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        log(f"ARNES bloques_pista · {time.strftime('%Y-%m-%d %H:%M:%S')} · CFG del carro {CFG0}")
        return 0 if arnes(log) else 1
    if a.humo:
        carpeta = os.path.join(DATOS, 'humo', time.strftime('humo_%Y%m%d_%H%M%S')); os.makedirs(carpeta, exist_ok=True)
        LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        T = 20000; sd = SEM_HUMO
        log(f"HUMO bloques_pista · s {sd} · T {T} · 5 corridas · carpeta {carpeta}")
        for b in ('termo', 'bloq', 'bloqaza', 'o1'): trabajo(sd, b, T, carpeta, log)
        trabajo(sd, 'bloq', T, carpeta, log, cfg=dict(CFG0, p_campo=0.0, p_dup=0.0, p_del=0.0, p_ins=0.0, inicial=0), forzada=RECHAZO,
                etiqueta='rechazo_forzado')
        lee(carpeta, log); return 0
    if a.humo2:
        # diagnostico (no es candidato): la regla PRUEBA de O1 escrita con los sentidos v2, forzada, tasas 0, T 100k, semillas de --explora
        sem = [int(x) for x in (a.semillas or '59201,59202,59203').split(',')]
        if len(sem) > 6 or not all(x in SEM_EXPLORA for x in sem): raise SystemExit("--humo2")
        carpeta = os.path.join(DATOS, f"explora_T{a.T}"); os.makedirs(carpeta, exist_ok=True)
        LOGF = open(os.path.join(carpeta, f"log_humo2_{'_'.join(map(str, sem))}.txt"), 'a', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        log(f"HUMO2 (diagnostico PRUEBA_O1 forzada) · {time.strftime('%H:%M:%S')} · {sem} · T {a.T}")
        for x in sem:
            trabajo(x, 'bloq2', a.T, carpeta, log, cfg=dict(CFG0, p_campo=0.0, p_dup=0.0, p_del=0.0, p_ins=0.0, inicial=0), forzada=PRUEBA_O1,
                    etiqueta='prueba_forzada')
        return 0
    if a.pasajes:
        # cadena c (1..5): pasajes p = 0..np-1 a T Tp en la semilla 59220 + 4 (c - 1) + p; luego PRUEBA a T (100k) en la semilla 59200 + c
        # (= la de --explora: se parea con termo/o1). Brazo bloq_pas / bloqaza_pas. El pasaje 0 arranca como bloq (banco vacio).
        cad = [int(c) for c in a.cadenas.split(',')]; brazos = [b for b in a.brazos.split(',') if b]
        if not all(1 <= c <= 5 for c in cad) or a.np > 4 or any(b not in ('bloq', 'bloqaza', 'bloq2', 'bloq2aza') for b in brazos): raise SystemExit("--pasajes")
        carpeta = os.path.join(DATOS, f"pasajes_Tp{a.Tp}_np{a.np}"); os.makedirs(carpeta, exist_ok=True)
        cprueba = os.path.join(DATOS, f"explora_T{a.T}"); os.makedirs(cprueba, exist_ok=True)
        LOGF = open(os.path.join(carpeta, f"log_{'_'.join(map(str, cad))}_{'_'.join(brazos)}.txt"), 'a', encoding='utf-8')
        def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
        log(f"PASAJES bloques_pista · {time.strftime('%H:%M:%S')} · cadenas {cad} · brazos {brazos} · np {a.np} · Tp {a.Tp} · prueba T {a.T}")
        for c in cad:
            for b in brazos:
                sb = None
                for p in range(a.np):
                    x = trabajo(59220 + 4 * (c - 1) + p, b, a.Tp, carpeta, log, etiqueta=f"{b}_c{c}_p{p}", siembra=sb)
                    sb = siembra_de(x) if not x.get('aborto') else None
                    log(f"    siembra tras p{p}: {len(sb) if sb else 0} listas; con rechazo {sum(any(es_rechazo(r) for r in R) for R in (sb or []))}")
                trabajo(59200 + c, b, a.T, cprueba, log, etiqueta=f"{b}_pas", siembra=sb)
        return 0
    sem = [int(s) for s in a.semillas.split(',')]
    if not all(s in SEM_EXPLORA for s in sem): raise SystemExit("--explora: solo semillas 59201-59210")
    brazos = [b for b in a.brazos.split(',') if b]
    for b in brazos:
        if b not in BRAZOS: raise SystemExit(f"brazo {b!r}")
    carpeta = os.path.join(DATOS, f"explora_T{a.T}"); os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, f"log_{'_'.join(map(str, sem))}_{'_'.join(brazos)}.txt"), 'a', encoding='utf-8')
    def log(s=''): print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()
    log(f"EXPLORA bloques_pista · {time.strftime('%H:%M:%S')} · semillas {sem} · brazos {brazos} · T {a.T} · CFG {CFG0} · corre_bp {h16(os.path.abspath(__file__))}")
    for s in sem:
        for b in brazos: trabajo(s, b, a.T, carpeta, log)
    return 0


if __name__ == '__main__':
    sys.exit(main())
