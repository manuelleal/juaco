"""corre_entre_linajes.py — RUNNER y LETRA del EXPLORATORIO "SELECCION SOBRE GENES EN LA CAMARA CON COLONIZACION Y SIEMBRA POR PARTOS"
(entre_linajes, encargo "seleccion real entre linajes", 30-sep-2026, creador; cambios por auditoria antes de datos: ERR-158, H-1..H-5).
Preregistro: PREREGISTRO_entre_linajes.md (la letra esta AQUI, en lee_explora(), y alli en la sec. 6).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Pregunta: si la siembra se reparte por HIJOS y el linaje extinto se refunda con un hijo de OTRO linaje vivo
(colonizacion), ¿la seleccion entre linajes mueve los genes de O1 y hace cruzar mas que la misma camara con genes que nadie lee?

QUE SE CORRE (por indice i = 0..4):
  CADENA sel   : 10 pasajes T 25 000 de O1_PAS (sigma 0.03, PS_LEE 1) en la CAMARA (camara_linajes.py): colonizacion + siembra ∝ partos.
  CADENA neu   : LA MISMA camara y semillas con PS_LEE 0 (genes heredados, colonizados y sembrados igual, pero nadie los lee).
  CADENA igual : el pasaje de o1_evo sin cambios (sin colonizacion, siembra igualada) = brazo o1pas de corre_o1_evo (arnes (c)).
  PRUEBA T 100 000 en la PISTA VIEJA con juez (corre_o1_evo.tarea, fundador limpio, letra ENMIENDA 5; PS_LEE 1): sel, neu, igual
  (fundadores de la siembra FINAL de su cadena, sorteo uniforme como siempre) y o1 (O1 de fabrica).
SEMILLAS NUEVAS (grep 30-sep: 624xxx no aparece en .py/.md de PROYECTOS/JUACO; en .txt solo como digitos de decimales):
  explora: pasaje p de la cadena i -> 624000 + 10 i + p (624000-624049), las TRES cadenas con las mismas (numeros aleatorios comunes);
           prueba de i -> 624201 + i (624201-624205). Arnes 624950-624989; humo 624990 (pasajes) y 624998 (prueba).
  Reservadas para una serie si la puerta la abre (con preregistro nuevo): 624300-624499 y 624501-624520.
Cada trabajo atrapa TODO y escribe su JSON antes de volver (ERR-54); --reanuda salta lo hecho y reintenta abortos. Aborto -> NO APLICA.

Uso (banderas desconocidas o abreviadas ABORTAN, ERR-115; --explora SOLO el coordinador, con preregistro, runner y camara COMMITEADOS):
  python experimentos/organelos/condiciones/entre_linajes/corre_entre_linajes.py --humo            # 1 proceso: 6 corridas (sel y neu 2x5k, prueba sel y o1 20k)
  python experimentos/organelos/condiciones/entre_linajes/corre_entre_linajes.py --humo --reanuda  # 2o proceso: 4 corridas (igual 2x5k, prueba neu e igual)
  python experimentos/organelos/condiciones/entre_linajes/corre_entre_linajes.py --explora --pool 2
  python experimentos/organelos/condiciones/entre_linajes/corre_entre_linajes.py --explora --pool 2 --reanuda
  python experimentos/organelos/condiciones/entre_linajes/corre_entre_linajes.py --lee <carpeta>
"""
import argparse, glob, hashlib, json, math, os, platform, statistics as st, subprocess, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import camara_linajes as CL
E = CL.E; P = CL.P; RAIZ = CL.RAIZ

PRERREGISTRO = 'PREREGISTRO_entre_linajes.md'
DATOS = os.path.join(AQUI, 'datos')
# brazo -> (brazo de corre_o1_evo para el CARRO, PS_LEE en la cadena, modo de la camara, siembra proporcional). o1: solo prueba.
BRAZOS = {'sel': ('o1pas', 1, 'col', 1), 'neu': ('o1neu', 0, 'col', 1), 'igual': ('o1pas', 1, 'nada', 0), 'o1': None}
CADENAS = ('sel', 'neu', 'igual'); ORDEN = ('sel', 'neu', 'igual', 'o1')
GENES = E.GENES; FABRICA = E.FABRICA
BASE = (624000, 624201)
N_IND = 5; NPAS = 10; T_PAS = 25000; T_PRU = 100000; POOL_MAX = 2
HUMO = dict(base=(624990, 624998), n=1, npas=2, T_pas=5000, T_pru=20000)
# ------------------------------------------------------------------ constantes de la LETRA (sec. 6), para n = 5 indices
GANA = 4            # P1: sel > neu en linajes que cruzan en >= 4/5 (empates EN CONTRA)
DIR_SIGNO = 4       # P2: un gen con el mismo signo de desplazamiento (siembra final - fabrica) en >= 4/5 cadenas sel
DIR_VECES = 2.0     # P2: y mediana |desplazamiento| sel > 2 x la de neu
MOD_GANA = 3        # MODESTO: sel > neu en >= 3/5 ...
MOD_SUMA = 4        # ... o suma(sel) >= suma(neu) + 4
GANA_IGUAL = 3      # H-1 (ERR-158): FUNCIONA exige ademas sel > igual en >= 3/5 (empates EN CONTRA)
O1_MAY = 4          # validez: o1 con mayoria que cruza (>= 5/9) en >= 4/5


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
def sem_pas(base, i, p): return base[0] + 10 * i + p
def sem_pru(base, i): return base[1] + i
def med(x):
    x = [v for v in x if v is not None]
    return round(float(st.median(x)), 4) if x else None
def esc(k, n, N=N_IND): return math.ceil(k * n / N - 1e-9)


def cadena(i, brazo, base, npas, T, carpeta, reanuda, log=None):
    """npas pasajes de la cadena del brazo; JSON por pasaje (reanudable)."""
    be, lee, modo, prop = BRAZOS[brazo]
    sie = None; F = []
    for p in range(npas):
        fin = os.path.join(carpeta, f"pasaje_i{i:02d}_{brazo}_p{p:02d}.json")
        if reanuda and os.path.exists(fin):
            with open(fin, encoding='utf-8') as fh: d = json.load(fh)
        else:
            x, cam = CL.tarea_pasaje(sem_pas(base, i, p), be, T, sie, lee, modo)
            if prop: sig, info = CL.siembra_prop(x['tel_ps'], T)
            else: sig = E.siembra(x['tel_ps'], T); info = dict(prop=0)
            f = E.fila(x, T); f['p'] = p; f['sembrado'] = int(sie is not None); f['genes_siembra'] = E.genes_de(sig)
            f['n_siembra'] = len(sig or []); f['camara'] = cam; f['siembra_info'] = info
            f['partos_tel_por_linaje'] = [int(((x['tel_ps'] or {}).get(str(j)) or {}).get('partos', 0)) for j in range(len(f['cruza']))]
            d = dict(fila=f, siembra_sig=sig)
            tmp = fin + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as fh: json.dump(d, fh, ensure_ascii=False)
            os.replace(tmp, fin)
        F.append(d['fila']); sie = d['siembra_sig']
        if log: log(f"    cadena i{i} {brazo} p{p} colonos {d['fila']['camara']['colonos_total']}/{d['fila']['camara']['fundadores_total']} "
                    f"Ne de pesos de siembra {d['fila']['siembra_info'].get('ne')} genes {d['fila']['genes_siembra']}")
        if not sie: raise RuntimeError(f"pasaje {p}: siembra vacia")
    return dict(pasajes=F, siembra_final=sie)


def trabajo(args):
    """UN trabajo: ('cadena', i, brazo) o ('prueba', i, brazo). Atrapa TODO; escribe su JSON antes de volver; con reanuda salta lo hecho
    sin aborto. cfg por worker: E.fija (dentro de E.tarea) carga y verifica el carro en ESTE proceso; los shas se verifican aqui tambien."""
    tipo, i, brazo, base, npas, T_pas, T_pru, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{tipo}_i{i:02d}_{brazo}.json"); previo = None
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: x0 = json.load(fh)
        if not x0.get('aborto'): return x0
        previo = x0['aborto']
    t0 = time.time()
    try:
        malos = [os.path.relpath(r, RAIZ) for r, s, s0, ok in CL.verifica_shas() if not ok]
        if malos: raise RuntimeError(f"shas cambiados en el worker: {malos}")
        if tipo == 'cadena':
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, **cadena(i, brazo, base, npas, T_pas, carpeta, reanuda))
        else:
            if brazo == 'o1':
                y = E.tarea(sem_pru(base, i), 'o1', T_pru); sie = None
            else:
                with open(os.path.join(carpeta, f"cadena_i{i:02d}_{brazo}.json"), encoding='utf-8') as fh: c = json.load(fh)
                if c.get('aborto') or not c.get('siembra_final'): raise RuntimeError("cadena sin siembra final")
                sie = c['siembra_final']
                y = E.tarea(sem_pru(base, i), 'o1pas', T_pru, siembra=sie, lee=1)   # = corre_o1_evo.trabajo('prueba'): la medida oficial
            x = dict(tipo=tipo, i=i, brazo=brazo, aborto=None, genes_siembra_usada=E.genes_de(sie), **E.fila(y, T_pru))
    except BaseException as e:   # noqa: nube-9
        x = dict(tipo=tipo, i=i, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300])
    if previo: x['reintento_de'] = previo
    x['seg'] = round(time.time() - t0, 1)
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO sec. 6)
def par(A, B, I):
    a = [A[i]['cruzan'] for i in I]; b = [B[i]['cruzan'] for i in I]
    return dict(n=len(I), gana=sum(x > y for x, y in zip(a, b)), empata=sum(x == y for x, y in zip(a, b)), pierde=sum(x < y for x, y in zip(a, b)),
                suma_a=sum(a), suma_b=sum(b), dif=sum(a) - sum(b), por_indice_a=a, por_indice_b=b)


def desplaza(Cb, I):
    """gen -> lista (por cadena) de genes de la siembra FINAL - fabrica."""
    out = {}
    for k in GENES:
        out[k] = [(Cb[i]['pasajes'][-1]['genes_siembra'] or {}).get(k, FABRICA[k]) - FABRICA[k] for i in I]
    return out


def lee_explora(C, R, n, abortos):
    """C[brazo][i] = cadena (sel, neu, igual); R[brazo][i] = prueba T 100k. n = indices (5; humo 1)."""
    I = list(range(n))
    completo = all(len(C.get(b, {})) == n for b in CADENAS) and all(len(R.get(b, {})) == n for b in ORDEN)
    v = {}
    v['V1_completa'] = bool(abortos == 0 and completo and all(R[b][i]['coherente'] for b in ORDEN for i in R.get(b, {})))
    v['V2_ancla_o1'] = completo and sum(R['o1'][i]['mayoria'] for i in I) >= esc(O1_MAY, n)
    v['V3_siembra_actua'] = completo and all(R[b][i]['fund_n'] > 0 and R[b][i]['fund_de_siembra'] == R[b][i]['fund_n'] for b in CADENAS for i in I)
    est = lambda d: d.get('estado') or {}
    v['V4_perillas'] = completo and all(est(q).get('lee') == BRAZOS[b][1] and est(q).get('sigma') == 0.03 and est(q).get('carro') == 'O1_PAS'
                                        for b in CADENAS for i in I for q in C[b][i]['pasajes']) \
        and all(est(R[b][i]).get('lee') == 1 and est(R[b][i]).get('sigma') == 0.03 for b in CADENAS for i in I) \
        and all(est(R['o1'][i]).get('carro') == 'O1' for i in I)
    # V5: el mecanismo actua donde debe y SOLO ahi
    col = lambda b, i: sum(q['camara']['colonos_total'] for q in C[b][i]['pasajes'])
    v['V5_mecanismo'] = completo and all(col(b, i) > 0 for b in ('sel', 'neu') for i in I) and all(col('igual', i) == 0 for i in I) \
        and all(any(q['siembra_info'].get('prop') == 1 and len(set((q['siembra_info'].get('n_por_linaje') or {}).values())) > 1
                    for q in C[b][i]['pasajes']) for b in ('sel', 'neu') for i in I) \
        and all(q['siembra_info'].get('prop') == 0 for i in I for q in C['igual'][i]['pasajes'])
    valido = all(v.values())
    p = {}; pn = po = pi = None; dsel = dneu = None; direccional = {}
    if completo:
        pn = par(R['sel'], R['neu'], I); po = par(R['sel'], R['o1'], I); pi = par(R['sel'], R['igual'], I)
        dsel = desplaza(C['sel'], I); dneu = desplaza(C['neu'], I)
        for k in GENES:
            sube = sum(1 for d in dsel[k] if d > 0); baja = sum(1 for d in dsel[k] if d < 0)
            ms = med([abs(d) for d in dsel[k]]); mn = med([abs(d) for d in dneu[k]])
            direccional[k] = dict(sube=sube, baja=baja, med_abs_sel=ms, med_abs_neu=mn, med_sel=med(dsel[k]), med_neu=med(dneu[k]),
                                  pasa=bool(max(sube, baja) >= esc(DIR_SIGNO, n) and ms is not None and mn is not None and ms > DIR_VECES * mn))
        p['P1_sel_gana_neu'] = pn['gana'] >= esc(GANA, n)
        p['P2_direccional'] = any(d['pasa'] for d in direccional.values())
        p['P3_sel_gana_o1'] = po['gana'] >= esc(GANA, n)        # NO decide el veredicto; con FUNCIONA habilita la frase de la sec. 7
        p['P4_sel_gana_igual'] = pi['gana'] >= esc(GANA_IGUAL, n)   # H-1 (ERR-158): DECIDE FUNCIONA (>= 3/5, empates en contra)
    matiz = None
    if not valido: ver = 'NO APLICA'
    elif p['P1_sel_gana_neu'] and p['P2_direccional'] and p['P4_sel_gana_igual']: ver = 'FUNCIONA'
    elif p['P1_sel_gana_neu'] and p['P2_direccional']:
        ver = 'HAY ALGO MODESTO'; matiz = 'seleccion sobre genes, no atribuible a la camara'   # H-1: P1 y P2 sin P4
    elif p['P1_sel_gana_neu'] or pn['gana'] >= esc(MOD_GANA, n) or pn['dif'] >= math.ceil(MOD_SUMA * n / N_IND - 1e-9): ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    umbral = bool(completo and pn['gana'] in (esc(GANA, n) - 1, esc(GANA, n)))
    desc = {}
    if completo:
        desc['pareados'] = {f"{a}_vs_{b}": par(R[a], R[b], I) for a, b in (('sel', 'neu'), ('sel', 'o1'), ('sel', 'igual'), ('neu', 'igual'),
                                                                           ('igual', 'o1'), ('neu', 'o1'))}
        desc['suma_cruzan'] = {b: sum(R[b][i]['cruzan'] for i in I) for b in ORDEN}
        desc['mayorias'] = {b: sum(R[b][i]['mayoria'] for i in I) for b in ORDEN}
        desc['R0_med'] = {b: med([R[b][i]['R0_med'] for i in I]) for b in ORDEN}
        desc['fund_por_linaje_media'] = {b: med([st.mean(R[b][i]['fund']) for i in I]) for b in ORDEN}
        desc['establecidos_0fund_post10k'] = {b: sum(sum(int(z == 0) for z in R[b][i]['fund_post10k']) for i in I) for b in ORDEN}
        desc['mundo_AC'] = {b: med([R[b][i]['mundo_AC'] for i in I]) for b in ORDEN}
        desc['genes_vivos_fin_prueba'] = {b: {k: med([(R[b][i]['genes_vivos_fin'] or {}).get(k) for i in I]) for k in GENES} for b in CADENAS}
        desc['direccional'] = direccional
        desc['desplazamiento_sel_por_cadena'] = dsel; desc['desplazamiento_neu_por_cadena'] = dneu
        for b in CADENAS:
            Cb = C[b]; npas = min(len(Cb[i]['pasajes']) for i in I)
            desc[f'{b}_trayectoria_genes_siembra_mediana'] = {k: [med([Cb[i]['pasajes'][q]['genes_siembra'][k] for i in I]) for q in range(npas)] for k in GENES}
            desc[f'{b}_colonos_sobre_fundadores_por_pasaje'] = [med([Cb[i]['pasajes'][q]['camara']['colonos_total'] /
                                                                    max(1, Cb[i]['pasajes'][q]['camara']['fundadores_total']) for i in I]) for q in range(npas)]
            desc[f'{b}_fundadores_camara_por_pasaje'] = [med([Cb[i]['pasajes'][q]['camara']['fundadores_total'] for i in I]) for q in range(npas)]
            desc[f'{b}_partos_por_pasaje'] = [med([sum(Cb[i]['pasajes'][q]['camara']['partos']) for i in I]) for q in range(npas)]
            desc[f'{b}_ne_pesos_siembra_por_pasaje'] = [med([Cb[i]['pasajes'][q]['siembra_info'].get('ne', 9.0 if not Cb[i]['pasajes'][q]['siembra_info'].get('prop') else None)
                                                      for i in I]) for q in range(npas)]
            desc[f'{b}_cadena_cruzan_por_pasaje'] = [med([Cb[i]['pasajes'][q]['cruzan'] for i in I]) for q in range(npas)]
    return dict(validez=v, puertas=p, veredicto=ver, matiz=matiz, en_umbral=umbral, umbrales=dict(gana=esc(GANA, n), gana_igual=esc(GANA_IGUAL, n), dir_signo=esc(DIR_SIGNO, n),
                mod_gana=esc(MOD_GANA, n), mod_suma=math.ceil(MOD_SUMA * n / N_IND - 1e-9), o1_may=esc(O1_MAY, n)),
                pareado_neu=pn, pareado_o1=po, pareado_igual=pi, descriptivo=desc)


def carga(carpeta):
    C = {b: {} for b in CADENAS}; R = {b: {} for b in ORDEN}; ab = []
    for f in sorted(glob.glob(os.path.join(carpeta, 'cadena_i*_*.json')) + glob.glob(os.path.join(carpeta, 'prueba_i*_*.json'))):
        d = json.load(open(f, encoding='utf-8'))
        if d.get('aborto'): ab.append(f"{d['tipo']} i{d['i']} {d['brazo']}: {d['aborto']}"); continue
        (C if d['tipo'] == 'cadena' else R)[d['brazo']][d['i']] = d
    return C, R, ab


def imprime(L, log):
    log(f"  validez: {L['validez']}")
    log(f"  puertas: {L['puertas']} · umbrales {L['umbrales']} · en el umbral (P1 a -1/0): {L['en_umbral']}")
    for k in ('pareado_neu', 'pareado_o1', 'pareado_igual'):
        q = L[k]
        if q: log(f"  {k}: gana {q['gana']} empata {q['empata']} pierde {q['pierde']} · suma {q['suma_a']} vs {q['suma_b']} (dif {q['dif']})")
    for k, v in L['descriptivo'].items():
        if 'por_cadena' not in k: log(f"  [desc] {k}: {v}")


# ------------------------------------------------------------------ candados y verificaciones
def identidad_corta(log, seed=624950, T=1200):
    """En CADA corrida (no reemplaza al arnes): camara sin gancho == pista.run; pasaje 'nada' == corre_o1_evo.tarea; siembra_prop con
    partos iguales == siembra igualada."""
    strip = lambda x: json.loads(json.dumps({k: v for k, v in x.items() if k != 'seg'}, default=str))
    E.fija('o1pas'); m = CL.E.CV._MODS['O1_PAS']
    kw = dict(T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
    m._TEL.clear(); m._PS_CNT.clear(); a = json.dumps(P.run(seed, [('X', m)] * 9, **kw), default=str)
    m._TEL.clear(); m._PS_CNT.clear(); b = json.dumps(CL.corre_camara(None)(seed, [('X', m)] * 9, **kw), default=str)
    x0 = E.tarea(seed, 'o1pas', T); x1, _ = CL.tarea_pasaje(seed, 'o1pas', T, None, 1, 'nada')
    tel = {str(j): dict(vivos=[[t, list(E.FABRICA.values())] for t in (0, 1, 2)], partos=3) for j in range(9)}
    s0 = E.siembra(tel, 3, 5); s1, _ = CL.siembra_prop(tel, 3, 5)
    ok = (a == b, strip(x0) == strip(x1), s0 == s1)
    log(f"  IDENTIDAD CORTA (s {seed}, T {T}): camara sin gancho == pista.run {ok[0]} · pasaje 'nada' == corre_o1_evo.tarea {ok[1]} · "
        f"siembra_prop (partos iguales) == siembra igualada {ok[2]}")
    return all(ok)


def git_limpio(rutas, log):
    ok = True
    for r in rutas:
        rel = os.path.relpath(r, RAIZ).replace('\\', '/')
        try:
            t = subprocess.run(['git', '-C', RAIZ, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
            c = subprocess.run(['git', '-C', RAIZ, 'diff', '--quiet', 'HEAD', '--', rel], capture_output=True, text=True).returncode == 0
        except Exception:   # noqa
            t = c = False
        ok &= t and c; log(f"  git {rel}: commiteado {t} · sin cambios vs HEAD {c}")
    return ok


def guarda(pre, reanuda):
    previas = sorted(d for d in glob.glob(os.path.join(DATOS, pre + '_*')) if os.path.isdir(d))
    for d in previas:
        rj = os.path.join(d, 'resumen.json')
        if os.path.exists(rj):
            r = json.load(open(rj, encoding='utf-8'))
            if not r.get('humo') and (r.get('letra') or {}).get('veredicto') in ('FUNCIONA', 'HAY ALGO MODESTO', 'NO'):
                return f"{os.path.relpath(rj, RAIZ)} ya tiene veredicto {r['letra']['veredicto']}: no se re-corre"
    if previas and not reanuda: return f"ya existe {os.path.relpath(previas[-1], RAIZ)}: solo --reanuda"
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--explora', action='store_true'); g.add_argument('--lee', default=None)
    ap.add_argument('--pool', type=int, default=0); ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.pool < 0 or a.pool > POOL_MAX: raise SystemExit(f"--pool entre 0 y {POOL_MAX} (contrato del encargo)")
    if a.lee:
        C, R, ab = carga(os.path.abspath(a.lee))
        n = max([len(v) for v in C.values()] + [len(v) for v in R.values()])
        L = lee_explora(C, R, n, len(ab)); imprime(L, print)
        print(f"VEREDICTO ({'HUMO/parcial, no cuenta' if n != N_IND else 'letra'}): {L['veredicto']} (matiz {L.get('matiz')}) · en el umbral {L['en_umbral']} · abortos {ab}")
        return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        modo = 'humo'; base = HUMO['base']; n = HUMO['n']; npas = HUMO['npas']; Tp = HUMO['T_pas']; Tr = HUMO['T_pru']
        f1 = [('cadena', 0, 'sel'), ('cadena', 0, 'neu'), ('prueba', 0, 'sel'), ('prueba', 0, 'o1')]   # 2x2 pasajes + 2 = 6 corridas
        if a.reanuda: f1 += [('cadena', 0, 'igual'), ('prueba', 0, 'neu'), ('prueba', 0, 'igual')]    # + 4 corridas (lo escrito se salta)
        pre = 'humo'; dest = os.path.join(DATOS, 'humo')
    else:
        modo = 'explora'; base = BASE; n = N_IND; npas = NPAS; Tp = T_PAS; Tr = T_PRU
        f1 = [('cadena', i, b) for i in range(n) for b in CADENAS] + [('prueba', i, 'o1') for i in range(n)]
        pre = f"explora_i{sem_pru(base, 0)}-{sem_pru(base, n - 1)}"; dest = DATOS
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
    shp = h16(os.path.join(AQUI, PRERREGISTRO)) if os.path.exists(os.path.join(AQUI, PRERREGISTRO)) else 'NO EXISTE'
    log(f"CORRE_ENTRE_LINAJES · {modo} · {sel} · python {platform.python_version()} · pool {a.pool or 'NO (un proceso)'} · runner "
        f"{h16(os.path.abspath(__file__))} · camara {h16(os.path.join(AQUI, 'camara_linajes.py'))} · preregistro {shp} · carpeta {carpeta}")
    log(f"  pasajes {sem_pas(base, 0, 0)}-{sem_pas(base, n - 1, npas - 1)} (T {Tp} x {npas}) · pruebas {sem_pru(base, 0)}-{sem_pru(base, n - 1)} (T {Tr}) · "
        f"brazos {list(ORDEN)} · reanuda {a.reanuda}")
    if not a.humo:
        e = guarda(pre, a.reanuda)
        if e: log(f"  NO SE CORRE (candado): {e}"); return 1
    ok = True
    for r, s, s0, bien in CL.verifica_shas():
        ok &= bien; log(f"  sha {os.path.relpath(r, RAIZ)} {s} {'OK' if bien else '!= ' + s0 + ' FALLA'}")
    ok = ok and identidad_corta(log)
    if not a.humo:
        ok &= git_limpio([os.path.join(AQUI, PRERREGISTRO), os.path.abspath(__file__), os.path.join(AQUI, 'camara_linajes.py'),
                          os.path.join(AQUI, 'identidad_entre_linajes.py')], log)
    if not ok: log("  ALGO FALLA -> no se corre (no se crea carpeta)."); return 1
    os.makedirs(carpeta, exist_ok=True)
    LOGF[0] = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8'); LOGF[0].write('\n'.join(BUF) + '\n'); LOGF[0].flush()
    mk = lambda t: (t[0], t[1], t[2], base, npas, Tp, Tr, carpeta, a.reanuda)

    def fmt(x):
        if x['tipo'] == 'cadena':
            return (f"  [{time.time()-t0:7.1f}s] cadena i{x['i']} {x['brazo']} ({x['seg']}s) aborto {x['aborto']} colonos por pasaje "
                    f"{[q['camara']['colonos_total'] for q in x.get('pasajes', [])]} genes p-ultimo {(x.get('pasajes') or [{}])[-1].get('genes_siembra')}")
        return (f"  [{time.time()-t0:7.1f}s] prueba i{x['i']} {x['brazo']:5s} ({x['seg']}s) aborto {x['aborto']} cruzan {x.get('cruzan')}/9 "
                f"fund {x.get('fund')} de siembra {x.get('fund_de_siembra')}/{x.get('fund_n')}")
    if a.pool and a.pool > 1:
        from multiprocessing import Pool
        with Pool(a.pool) as PL:
            pend = {PL.apply_async(trabajo, (mk(t),)): t for t in f1}
            while pend:
                listos = [r for r in pend if r.ready()]
                if not listos: time.sleep(2); continue
                for r in listos:
                    t = pend.pop(r); x = r.get(); log(fmt(x))
                    if t[0] == 'cadena':   # su prueba entra a la cola en cuanto la cadena termina
                        pend[PL.apply_async(trabajo, (mk(('prueba', t[1], t[2])),))] = ('prueba', t[1], t[2])
    else:
        todo = list(f1)
        if not a.humo: todo += [('prueba', i, b) for i in range(n) for b in CADENAS]
        for t in todo:
            x = trabajo(mk(t)); log(fmt(x))
    C, R, ab = carga(carpeta)
    L = lee_explora(C, R, n, len(ab))
    log(f"\n================ LA LETRA ({PRERREGISTRO} sec. 6)" + (" -- HUMO: T corto, practica, 1 indice: NO cuenta" if a.humo else ""))
    imprime(L, log)
    if ab: log(f"  ABORTOS: {ab}")
    ver = ('HUMO (no cuenta): ' if a.humo else '') + L['veredicto'] + (f" ({L['matiz']})" if L.get('matiz') else '')
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, humo=a.humo, letra=L, abortos=ab, n=n, npas=npas, T_pas=Tp, T_pru=Tr, veredicto=ver, preregistro=PRERREGISTRO,
                       sha_preregistro=(shp if shp != 'NO EXISTE' else None), sha_runner=h16(os.path.abspath(__file__)),
                       sha_camara=h16(os.path.join(AQUI, 'camara_linajes.py')),
                       shas={os.path.relpath(k, RAIZ): v for k, v in CL.SHAS_FIJOS.items()}, seg=round(time.time() - t0, 1)), fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)}) · abortos {len(ab)} · {time.time()-t0:.1f}s")
    log(f"VEREDICTO DEL {modo.upper()}: {ver}   (en el umbral: {L['en_umbral']}; {PRERREGISTRO} sec. 6-7)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
