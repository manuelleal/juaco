"""corre_termop.py = experimentos/organelos/termo/corre_termo.py (66f1f2539f1030ef) para TERMO' (memoria de lo sentido con olvido): MISMA pista y MISMA letra; carros V143_TERMOP / V143_TERMOPINV; semillas nuevas 49941-49994. Preregistro: PREREGISTRO_termop.md. GENERADO por construye_carrera_termop.py. NO editar a mano."""
"""corre_termo.py — RUNNER y LETRA del bloque TERMO: ULTIMO intento del muro de la carrera. Preregistro: PREREGISTRO_termo.md
(la letra esta AQUI, en lee_serie(), y alli en la sec. 6).

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

Pieza (construye_termo.py, perilla TERMO = 1): termostato de dos necesidades en la boca. Sobre lo SENTIDO bueno por el linaje (_adS sin
componentes negativas y con alguna positiva): muerde <=> existe j con s_j > 0 y nivel_j < rep_umbral + s_j/2. Lo demas: v14.3 tal cual.

ENTRADA (regla 14): la corrida ES experimentos/tronco_v14_3/corre_v143.tarea (se IMPORTA, no se toca; sha fijado) = juez.tarea(seed,
9 carros iguales, T, pizarra 1, rep_acum 0, escala 1, mundo_n None, fundador_limpio 1) + juez.resumen_linaje (solo fisica, ERR-96).
Los carros nuevos se registran en su cache de modulos (corre_v143._MODS) y en su tabla BRAZOS, en memoria. Lo unico agregado:
'tel_termo' = telemetria de SOLO LECTURA (d['carro']['termo'] de la ULTIMA instancia de cada linaje; no puntua). Resumen y pareados:
corre_v143.resume y corre_v143.pareado, tal cual. Mismo formato y misma letra que corre_muro.py / corre_muro2.py (bloque MURO).

BRAZOS (monocultivo de 9 carros iguales, L 360, 36 objetos, T 100 000, fundador limpio = ENMIENDA 5). SERIE = los 4:
  v143      V143            base: el bicho real (tronco_v14_3)
  termo     V143_TERMO      CANDIDATO (TERMO 1)
  termoinv  V143_TERMOINV   CONTROL desfasado (TERMO 2): la misma regla leyendo el nivel de la necesidad que la letra NO sube
  o1        O1              techo escrito por un LLM; ANCLA de la pista
SEMILLAS: serie 49941-49960 · replica 49961-49980 · humo 49991-49992 · arnes 49993-49994 (exploratorio previo 39001-39010, 39901-39902).
SHAS de TODO lo que corre, fijados ANTES del humo (SHAS abajo): si uno cambia, verifica() falla y no se corre nada.
nube-9: trabajo() atrapa TODA excepcion y devuelve un resultado marcado 'aborto'. Cualquier aborto -> NO SE LEE. Cada corrida escribe su
JSON ANTES de volver (ERR-54); --reanuda salta las que ya estan.

Uso (ERR-115: banderas desconocidas o abreviadas ABORTAN; SOLO el coordinador lanza --serie):
  python experimentos/organelos/termo/corre_termo.py --humo                                   # 1 proceso, 6 corridas, T 20 000
  python experimentos/organelos/termo/corre_termo.py --serie --desde 49941 --n 20 --pool 6    # serie   (80 corridas)
  python experimentos/organelos/termo/corre_termo.py --serie --desde 49961 --n 20 --pool 6    # replica (80 corridas; solo si la serie no da NO)
  python experimentos/organelos/termo/corre_termo.py --serie --desde 49941 --n 20 --pool 6 --reanuda
  python experimentos/organelos/termo/corre_termo.py --bloque <resumen serie>.json,<resumen replica>.json
"""
import argparse, hashlib, importlib.util, json, os, platform, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
V143D = os.path.join(RAIZ, 'experimentos', 'tronco_v14_3')
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
for _d in (AQUI, V143D, PISTA):
    if _d not in sys.path: sys.path.insert(0, _d)
import corre_v143 as CV          # tarea, resume, pareado, verifica_todo (se IMPORTA, no se toca)
import construye_termop as CB
import revisa_carro as RC
P = CV.P; J = CV.J

PRERREGISTRO = 'PREREGISTRO_termop.md'
CARROS = os.path.join(AQUI, 'carros')
DATOS = os.path.join(AQUI, 'datos')
SHAS = {os.path.join(V143D, 'corre_v143.py'): '24100621c450da22', os.path.join(V143D, 'carros_v143', 'V143.py'): '2a03048a7f1525e5',
        os.path.join(PISTA, 'pista.py'): '9f47c65e438e0ff4', os.path.join(PISTA, 'juez.py'): '6a68f640a7832f12',
        os.path.join(PISTA, 'carros', 'O1.py'): '99436afa2715f028', os.path.join(PISTA, 'revisa_carro.py'): '1c8a789f7427ab96',
        os.path.join(AQUI, 'construye_termop.py'): '81f63fd59d168759',
        os.path.join(CARROS, 'V143_TERMOP.py'): 'edf5dfc9c5e498da', os.path.join(CARROS, 'V143_TERMOPINV.py'): '63edcafcc569a0d7'}
BRAZOS = {'v143': 'V143', 'termop': 'V143_TERMOP', 'termopinv': 'V143_TERMOPINV', 'o1': 'O1'}
PROPIOS = ('V143_TERMOP', 'V143_TERMOPINV')
CAND = 'termop'; CTRL = 'termopinv'
SERIE_BRAZOS = ('v143', 'termop', 'termopinv', 'o1')
SERIE = range(49941, 49961); REPLICA = range(49961, 49981); PRACTICA = range(49991, 49995)
HUMO = [(49991, 'v143'), (49991, 'termop'), (49991, 'termopinv'), (49991, 'o1'), (49992, 'v143'), (49992, 'termop')]
T_DEF = 100000; T_HUMO = 20000
GANA = 15                       # >= 15/20 semillas (la de la carrera: ENMIENDAS 2, 5, 6 y corre_v143.GANA)
DIF_MOD = 0.10                  # diferencia mediana pareada minima para HAY ALGO MODESTO (la de corre_v143.DIF_MOD)
ANCLA_V143 = (0.40, 0.80)       # V143, mediana del R0 real (la del muro): 0.536, 0.63, 0.602; exploratorio 39001-39010: 0.413


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def registra():
    for n in PROPIOS:
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", os.path.join(CARROS, n + '.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m
    for k in BRAZOS:
        if k not in ('v143', 'o1'): CV.BRAZOS.setdefault(k, BRAZOS[k])


def tarea(args):
    """(seed, carro, T) -> corre_v143.tarea tal cual + 'tel_termo' (telemetria de solo lectura de los carros TERMO)."""
    registra()
    cap = []; orig = P.run

    def run2(*a, **k):
        r = orig(*a, **k); cap.append([(d.get('carro') or {}).get('termo') for d in r['linajes']]); return r
    P.run = run2
    try:
        x = CV.tarea(args)
    finally:
        P.run = orig
    x['tel_termo'] = cap[0] if cap else None
    return x


def trabajo(args):
    """UNA corrida; atrapa TODO (nube-9); escribe su JSON antes de volver (ERR-54); con reanuda salta la que ya existe."""
    seed, brazo, T, carpeta, reanuda = args
    fin = os.path.join(carpeta, f"{brazo}_s{seed}.json")
    if reanuda and os.path.exists(fin):
        with open(fin, encoding='utf-8') as fh: return json.load(fh)
    try:
        x = tarea((seed, BRAZOS[brazo], T)); x.pop('pizarra_log', None); x['brazo'] = brazo; x['aborto'] = None
    except BaseException as e:   # noqa: nube-9
        x = dict(seed=seed, brazo=brazo, aborto=f"{type(e).__name__}: {e}"[:300], linajes=[])
    tmp = fin + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
    os.replace(tmp, fin)
    return x


def tm_suma(R):
    tot = {}
    for c in R:
        for t in (c.get('tel_termo') or []):
            if not t: continue
            for k, v in t.items():
                if isinstance(v, (int, float)) and k != 'termo': tot[k] = tot.get(k, 0) + v
    return tot


def cuerpos(R):
    """DESCRIPTIVO (igual que corre_muro): hijos de la cola contra fundadores, de la fisica (telem del juez)."""
    H = dict(n=0, vidas=[], hijos=0, sin_hijos=0, causas={}); F = dict(n=0, vidas=[], hijos=0, sin_hijos=0, causas={})
    for c in R:
        for l in c['linajes']:
            t = l['telem']; m = min(len(t['vidas']), len(t['desc_por_vida']), len(t['causa_cuerpo']), len(t['origen']))
            for i in range(m):
                D = H if t['origen'][i] == 1 else F
                D['n'] += 1; D['vidas'].append(t['vidas'][i]); D['hijos'] += t['desc_por_vida'][i]; D['sin_hijos'] += int(t['desc_por_vida'][i] == 0)
                D['causas'][t['causa_cuerpo'][i]] = D['causas'].get(t['causa_cuerpo'][i], 0) + 1
    out = {}
    for k, D in (('hijos_de_cola', H), ('fundadores', F)):
        out[k] = dict(n=D['n'], vida_med=(CV.med(D['vidas']) if D['vidas'] else None),
                      hijos_por_cuerpo=(round(D['hijos'] / D['n'], 3) if D['n'] else None),
                      frac_sin_hijos=(round(D['sin_hijos'] / D['n'], 3) if D['n'] else None), causas=D['causas'])
    return out


def establece(R):
    L = [l for c in R for l in c['linajes']]
    e = [l for l in L if l['fund_post10k'] == 0]; ne = [l for l in L if l['fund_post10k'] > 0]
    return dict(linajes=len(L), establecidos=len(e), frac_establecidos=(round(len(e) / len(L), 4) if L else None),
                R0_real_establecidos=CV.med([l['R0_real'] for l in e]), R0_real_no_establecidos=CV.med([l['R0_real'] for l in ne]),
                cruzan_de_establecidos=sum(l['cruza_real'] for l in e))


# ------------------------------------------------------------------ LA LETRA (PREREGISTRO_termo.md sec. 6; la misma del muro)
def pieza(t):
    """V4: la pieza del brazo ACTUO (telemetria de la ultima instancia): cambio al menos una decision de la boca de v14.3."""
    return (t.get('a_no', 0) + t.get('a_si', 0)) > 0


def lee_serie(res, par, tm, completa, abortos):
    v = {}
    v['V1_completa'] = bool(completa and abortos == 0 and all(b in res for b in SERIE_BRAZOS)
                            and all(res[b]['coherente'].split('/')[0] == res[b]['coherente'].split('/')[1] for b in SERIE_BRAZOS if b in res))
    v['V2_ancla_O1_gana'] = bool(res.get('o1', {}).get('gana_e5'))
    m = res.get('v143', {}).get('R0_real_med')
    v['V3_ancla_V143'] = m is not None and ANCLA_V143[0] <= m <= ANCLA_V143[1]
    v['V4_pieza_actua'] = bool(pieza(tm.get(CAND, {})) and pieza(tm.get(CTRL, {})))
    valido = all(v.values())
    p = {}
    p['P1_cand_cruza'] = bool(res.get(CAND, {}).get('gana_e5'))
    x = par.get((CAND, 'v143')) or {}
    p['P2_cand_gana_v143'] = bool(x.get('semillas') and x['gana'] >= GANA * x['semillas'] / 20)
    p['P3_ctrl_no_cruza'] = not bool(res.get(CTRL, {}).get('gana_e5'))
    y = par.get((CAND, CTRL)) or {}
    mod = bool(p['P2_cand_gana_v143'] and x.get('dif_med') is not None and x['dif_med'] >= DIF_MOD - 1e-12
               and y.get('semillas') and y['gana'] * 2 > y['semillas'])
    if not valido: ver = 'NO SE LEE'
    elif all(p.values()): ver = 'FUNCIONA'
    elif mod: ver = 'HAY ALGO MODESTO'
    else: ver = 'NO'
    return dict(validez=v, puertas=p, modesto=mod, veredicto=ver)


ORDEN = {'NO SE LEE': -1, 'NO': 0, 'HAY ALGO MODESTO': 1, 'FUNCIONA': 2}


def bloque(v_serie, v_replica):
    if v_serie == v_replica: return v_serie
    return min((v_serie, v_replica), key=lambda z: ORDEN[z])


def valida(humo, desde, n, T, brazos):
    for b in brazos:
        if b not in BRAZOS: return f"brazo desconocido {b!r} (validos {list(BRAZOS)})"
    if n < 1: return "--n >= 1"
    sem = list(range(desde, desde + n))
    if humo:
        if not all(x in PRACTICA for x in sem): return "--humo: solo semillas de practica 49991-49994"
        if T > 30000: return "--humo: T <= 30000"
    else:
        if not (all(x in SERIE for x in sem) or all(x in REPLICA for x in sem)): return "serie: solo 49941-49960 (serie) o 49961-49980 (replica)"
        if T != T_DEF: return "serie: T = 100000 (preregistrado)"
        if tuple(brazos) != SERIE_BRAZOS: return f"serie: brazos {SERIE_BRAZOS} (preregistrado)"
    return None


def verifica(log):
    """shas FIJADOS de todo lo que corre + carros == construye_termo + revisa_carro + identidad corta (TERMO = 0 == V143)."""
    ok = True
    for ruta, sha in SHAS.items():
        s = h16(ruta); ok &= s == sha; log(f"  sha {os.path.relpath(ruta, RAIZ)} {s} {'OK' if s == sha else '!= ' + sha + ' FALLA'}")
    for n, b in {k[len('carros') + 1:-3]: v.encode('utf-8') for k, v in CB.construye().items() if k.startswith('carros')}.items():
        ruta = os.path.join(CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = RC.revisa_fuente(b.decode('utf-8'), n) if igual else ['distinto de construye_termop']
        ok &= igual and not vr
        log(f"  carro {n} sha {CB.h16b(b)} == construye_termop: {igual} · revisa_carro: {'PASA' if not vr else vr[:2]}")
    registra()
    N = lambda x: json.loads(json.dumps(x, default=str))
    base = N(P.run(49993, [('C', CV.modulo('V143'))] * 9, T=2000, fundador_limpio=1))
    for n in PROPIOS:
        m = CV._MODS[n]; g = m.TERMO
        try:
            m.TERMO = 0; xx = N(P.run(49993, [('C', m)] * 9, T=2000, fundador_limpio=1))
        finally:
            m.TERMO = g
        i = xx == base; ok &= i
        log(f"  IDENTIDAD CORTA: {n} con TERMO = 0 == V143 (salida ENTERA, N 9, s 49993, T 2000, fundador limpio): {'OK' if i else 'FALLA'}")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true')
    g.add_argument('--serie', action='store_true')
    g.add_argument('--bloque', default=None)
    ap.add_argument('--brazos', default=None)
    ap.add_argument('--desde', type=int, default=None)
    ap.add_argument('--n', type=int, default=None)
    ap.add_argument('--T', type=int, default=None)
    ap.add_argument('--pool', type=int, default=0)
    ap.add_argument('--reanuda', action='store_true')
    a = ap.parse_args(argv)   # ERR-115: nunca parse_known_args
    if a.bloque:
        rs = [json.load(open(x.strip(), encoding='utf-8')) for x in a.bloque.split(',')]
        if len(rs) != 2: raise SystemExit("--bloque: <resumen serie>,<resumen replica>")
        s0 = rs[0]['semillas'][0]; s1 = rs[1]['semillas'][0]
        if not (s0 in SERIE and s1 in REPLICA): raise SystemExit("--bloque: primero la serie 49941-49960 y luego la replica 49961-49980")
        vb = bloque(rs[0]['letra']['veredicto'], rs[1]['letra']['veredicto'])
        print(f"serie {rs[0]['letra']['veredicto']} · replica {rs[1]['letra']['veredicto']} -> BLOQUE: {vb}  ({PRERREGISTRO} sec. 6-7)")
        return 0
    if a.humo:
        if a.pool: raise SystemExit("--humo: sin Pool (un proceso)")
        T = a.T or T_HUMO
        if a.brazos or a.desde or a.n:
            brazos = [s for s in (a.brazos or 'v143,termop,termopinv,o1').split(',') if s]; desde = a.desde or 49991; n = a.n or 1
            e = valida(True, desde, n, T, brazos)
            if e: raise SystemExit(e)
            tareas = [(s, b) for s in range(desde, desde + n) for b in brazos]
        else:
            tareas = list(HUMO)
            e = valida(True, 49991, 2, T, list(BRAZOS))
            if e: raise SystemExit(e)
        if len(tareas) > 6: raise SystemExit("--humo: maximo 6 corridas por proceso")
        semillas = sorted({s for s, _ in tareas}); brazos = [b for b in BRAZOS if any(b == x for _, x in tareas)]
        pool = 0; dest = os.path.join(DATOS, 'humo')
    else:
        T = a.T or T_DEF; desde = a.desde or 49941; n = a.n or 20; brazos = [s for s in (a.brazos or ','.join(SERIE_BRAZOS)).split(',') if s]
        e = valida(False, desde, n, T, brazos)
        if e: raise SystemExit(e)
        semillas = list(range(desde, desde + n)); tareas = [(s, b) for b in brazos for s in semillas]; pool = a.pool
        dest = DATOS
    sel = time.strftime('%Y%m%d_%H%M%S')
    pre = f"termop_{'humo_' if a.humo else ''}s{semillas[0]}-{semillas[-1]}_T{T}"
    carpeta = os.path.join(dest, pre if not a.humo else pre + '_' + sel)
    if a.reanuda and not a.humo:
        prev = sorted(d for d in os.listdir(dest) if d.startswith(pre + '_') and os.path.isdir(os.path.join(dest, d))) if os.path.isdir(dest) else []
        carpeta = os.path.join(dest, prev[-1]) if prev else carpeta + '_' + sel
    elif not a.humo:
        carpeta = carpeta + '_' + sel
    os.makedirs(carpeta, exist_ok=True)
    LOGF = open(os.path.join(carpeta, 'log.txt'), 'a', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    log(f"CORRE_TERMOP · {pre} · {sel} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'} · "
        f"corre_termop.py {h16(os.path.abspath(__file__))} · preregistro {PRERREGISTRO} · carpeta {carpeta}")
    log(f"  tareas {len(tareas)} · brazos {brazos} · semillas {semillas[0]}-{semillas[-1]} · T {T} · fundador limpio 1 · reanuda {a.reanuda}")
    ok = verifica(log)
    if a.humo:
        ok &= CV.verifica_todo(log, con_entrada=True)   # regla 14: corre_v143.tarea == juez.tarea (9 FABRICA, s 14281, T 2000)
        N = lambda x: json.loads(json.dumps(x, default=str))
        x = tarea((49993, 'V143', 2000)); y = CV.tarea((49993, 'V143', 2000))
        e14 = x.pop('tel_termo') == [None] * 9 and N({k: v for k, v in x.items() if k != 'seg'}) == N({k: v for k, v in y.items() if k != 'seg'})
        ok &= e14; log(f"  ENTRADA campo a campo (regla 14): tarea de este runner == corre_v143.tarea (V143, s 49993, T 2000): {'OK' if e14 else 'FALLA'}")
    if not ok: log("  ALGO FALLA -> no se corre."); return 1
    args = [(s, b, T, carpeta, a.reanuda) for s, b in tareas]
    R = []
    if pool and pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as PL:
            for x in PL.imap_unordered(trabajo, args):
                R.append(x); log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} s{x['seed']} ({x.get('seg')}s) R0 pista {x.get('R0_pista')} aborto {x['aborto']}")
    else:
        for ar in args:
            x = trabajo(ar); R.append(x)
            log(f"  [{time.time()-t0:7.1f}s] {x['brazo']} s{x['seed']} ({x.get('seg')}s) R0 pista {x.get('R0_pista')} aborto {x['aborto']} · "
                f"R0 real por linaje {[l['R0_real'] for l in x['linajes']]} · fundadores {[l['fundadores'] for l in x['linajes']]}")
    abortos = sum(1 for x in R if x['aborto'])
    por = {b: sorted([x for x in R if x['brazo'] == b and not x['aborto']], key=lambda z: z['seed']) for b in brazos}
    res = {}; tm = {}; cz = {}
    for b in [x for x in por if por[x]]:
        res[b] = CV.resume(por[b], b, log); tm[b] = tm_suma(por[b]); cz[b] = cuerpos(por[b]); cz[b]['establece'] = establece(por[b])
        log(f"  ESTABLECIMIENTO ({b}, descriptivo): {cz[b]['establece']}")
        log(f"  CUERPOS ({b}, descriptivo): {cz[b]['hijos_de_cola']} · fundadores {cz[b]['fundadores']}")
        if tm[b]: log(f"  termo ({b}): telemetria de la ultima instancia {tm[b]}")
    PAR = ((CAND, 'v143'), (CAND, CTRL), (CTRL, 'v143'), ('o1', 'v143'), ('o1', CAND))
    par = {k: CV.pareado(por[k[0]], por[k[1]]) for k in PAR if por.get(k[0]) and por.get(k[1])}
    log("\nPAREADOS (por semilla: mediana del R0 real de los 9 linajes; gana = semillas en que el primero supera al segundo)")
    for k, v in par.items(): log(f"  {k[0]} vs {k[1]}: gana {v['gana']}/{v['semillas']} · diferencia mediana {v['dif_med']}")
    completa = True if a.humo else all(len(por.get(b, [])) == len(semillas) for b in SERIE_BRAZOS)
    letra = lee_serie(res, par, tm, completa, abortos)
    log(f"\n================ LA LETRA ({PRERREGISTRO} sec. 6)" + (" -- HUMO: T corto y semillas de practica, NO cuenta" if a.humo else ""))
    log(f"  validez {letra['validez']}")
    log(f"  puertas {letra['puertas']} · modesto {letra['modesto']}")
    ver = ('HUMO (no cuenta): ' if a.humo else '') + letra['veredicto']
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(brazos=res, pareados={f"{k[0]}_vs_{k[1]}": x for k, x in par.items()}, telemetria=tm, cuerpos=cz, letra=letra,
                       semillas=semillas, T=T, humo=a.humo, abortos=abortos, veredicto=ver, preregistro=PRERREGISTRO,
                       sha_runner=h16(os.path.abspath(__file__)), sha_carros={n: h16(os.path.join(CARROS, n + '.py')) for n in PROPIOS}),
                  fh, ensure_ascii=False, indent=1)
    log(f"\n  RESUMEN {rj} (sha {h16(rj)})\nTerminado en {time.time()-t0:.1f}s")
    log(f"VEREDICTO DE LA SERIE: {ver}   (regla de parada: {PRERREGISTRO} sec. 7)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
