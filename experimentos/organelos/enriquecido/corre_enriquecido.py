"""corre_enriquecido.py — runner EXPLORATORIO de MUNDO ENRIQUECIDO (29-sep-2026; plan 3b de registro/ESTADO.md).

Mision: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros, y solo con seleccion natural.

Preregistro: PREREGISTRO_enriquecido.md (la LETRA de la puerta esta AQUI, en veredicto(), y alli).
Base: BLOQUES (FUNCIONA x2): ECO w90 con hijos ingenuos (FABRICA_ECO), vivero finito t_corte 100 000, genoma de reglas heredable
(donante padre), arranque VACIO. Se IMPORTA eco_sel_ing/nucleo_eco_sel_ing.py (sha c2189f9d22b72386, sin tocarlo): trabajo(), K,
persistencia, checkpoint. El gemelo enchufado en CR.ME es motor_enriquecido (construido por anclas desde bloques/opusM/motor_bloques.py).
Brazos (todos: MUT0, FABRICA_ECO, t_corte 100 000, reglas heredables con el kit ENRIQUECIDO: 7 sentidos (+ 'nuez'), 5 acciones
(+ 'copiar')):
  NUEZ_SOC   nueces (f 0.5, llave C, bonus 0.8, fallo 0.005) + canal social SOC (copia al vecino que ABRIO)
  NUEZ_OFF   nueces + canal apagado (mismo disparo y moneda; no copia)
  NUEZ_DESF  nueces + canal desfasado (mismo disparo y moneda; copia a un vecino al azar que NO abrio)
  REF        sin nueces (sin tarea secuencial), canal SOC (inerte: nadie abre nueces), el mismo kit
Uso (ERR-115: banderas desconocidas abortan):
  python corre_enriquecido.py --humo                       # 1 proceso: 50195, T 200 000, NUEZ_SOC; escribe JSON
  python corre_enriquecido.py --explora --pool 2           # SOLO el coordinador (pool <= 2): 50101-50105 x 4 brazos, T 500 000
  python corre_enriquecido.py --explora --pool 2 --reanuda # el mismo, reanuda (JSON hechos se saltan; los cortados siguen del ckpt)
  python corre_enriquecido.py --lee explora                # lee los JSON y escribe VEREDICTO.json (la letra)
"""
import argparse, glob, hashlib, json, os, sys, time, types
import numpy as np

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ORG = os.path.dirname(AQUI)
ING_DIR = os.path.join(ORG, 'eco_sel_ing')
for _d in (ING_DIR, AQUI):
    if _d not in sys.path: sys.path.insert(0, _d)
import nucleo_eco_sel_ing as NS   # noqa: E402

SHAS = {os.path.join(ING_DIR, 'nucleo_eco_sel_ing.py'): 'c2189f9d22b72386',
        os.path.join(ORG, 'bloques', 'opusM', 'motor_bloques.py'): 'ff782697e54585a5',
        os.path.join(AQUI, 'motor_enriquecido.py'): '09f1f2f4d85b2368'}
DATOS = os.path.join(AQUI, 'datos')
FAB = NS.FAB
T_CORTE = 100000
BQ_DEF = dict(on=1, donante='padre', p_campo=0.10, p_dup=0.02, p_ins=0.02, p_hgt=0.01, p_del=0.05, banco=200, inicial=None,
              forzada=None, nsen=7, nacc=5)
NZ_DEF = dict(nuez=1, f=0.5, bonus=0.8, c_fallo=0.005, llave=2, social=0, radio=10)
BRAZOS = {'NUEZ_SOC': dict(nuez=1, social=1), 'NUEZ_OFF': dict(nuez=1, social=3), 'NUEZ_DESF': dict(nuez=1, social=2),
          'REF': dict(nuez=0, social=1)}
for _b in BRAZOS: NS.BRAZOS[_b] = ('MUT0', FAB, T_CORTE)
EXPLORA_BR = ('NUEZ_SOC', 'NUEZ_OFF', 'NUEZ_DESF', 'REF')
SEM_EXPLORA = (50101, 50102, 50103, 50104, 50105)
T_EXPLORA = 500000
HUMO = dict(semilla=50195, T=200000, brazos=('NUEZ_SOC',))   # 1 corrida (tope de corridas del creador); ver PREREGISTRO §9
SENT = ['hambre', 'sed', 'cerca', 'pixF', 'pixM', 'Rult', 'nuez']
ACC = ['boca', 'hacia', 'quieto', 'parir', 'copiar']
MUNDO_ULT = {}
MIN_INT = 20   # intentos minimos en la ventana para que frac_ok y SI se definan (si no: frac_ok = 0, SI = None)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def verifica():
    for p, h in SHAS.items():
        if h16(p) != h: raise SystemExit(f'{os.path.relpath(p, ORG)} cambio: {h16(p)} != {h}')


def cfg_de(brazo):
    bq = dict(BQ_DEF); nz = dict(NZ_DEF); nz.update(BRAZOS[brazo])
    return bq, nz


def usa_motor():
    import motor_enriquecido as MB
    g = types.ModuleType('motor_enriquecido_gemelo')
    g.__dict__.update({k: v for k, v in NS.ME_PY.__dict__.items() if not k.startswith('__')})

    def _rs(*a, **k):   # misma llamada; guarda la composicion del mundo (diagnostico, no cambia nada)
        r = MB.run_solapadas(*a, **k); P = r['pista']
        MUNDO_ULT.clear(); MUNDO_ULT.update(comp_mundo=P['comp_mundo'], nobj_medio=P['nobj_medio'], llegadas=P['llegadas'],
                                            perdidas=P['llegadas_perdidas'])
        return r
    g.run_solapadas = _rs
    g._MF = MB
    NS.CR.ME = g
    return MB


def corre(seed, brazo, T, carpeta, reanuda=False, nz_extra=None):
    """UNA corrida. La cfg (BQ_CFG y NZ_CFG) se FIJA AQUI, en el trabajador, en cada llamada (tambien al reanudar); el motor comprueba
    al reanudar que el checkpoint es de la misma cfg. Escribe su JSON (M_<brazo>_s<seed>.json) antes de volver."""
    fn = os.path.join(carpeta, f'M_{brazo}_s{seed}.json')
    if reanuda and os.path.exists(fn):   # H-3 del auditor: un JSON ABORTADO se reintenta (sigue del checkpoint si lo hay)
        d0 = json.load(open(fn, encoding='utf-8'))
        if d0.get('aborto') is None: return d0
        os.remove(fn)
    os.makedirs(carpeta, exist_ok=True)
    fin_ns = os.path.join(carpeta, f'{brazo}_s{seed}.json')   # el JSON de NS.trabajo: sin el M_ no sirve (le faltan reglas y NZ)
    if os.path.exists(fin_ns): os.remove(fin_ns)
    MB = usa_motor()
    bq, nz = cfg_de(brazo); nz.update(nz_extra or {})   # nz_extra: SOLO --practica (calibracion declarada)
    MB.BQ_CFG.clear(); MB.BQ_CFG.update(bq); MB.NZ_CFG.clear(); MB.NZ_CFG.update(nz)
    res = NS.trabajo((seed, brazo, T, T_CORTE, NS.FRIO['T_lect'], carpeta, bool(reanuda)))
    out = dict(K=kbar(res), persiste=res.get('persiste'), bloqueados=res.get('bloqueados'), aborto=res.get('aborto'), seg=res.get('seg'),
               n_nac=res.get('n_nac'), n_refund=res.get('n_refund'), t_ext=res.get('t_ext'), t_corte=res.get('t_corte'),
               carro=res.get('carro'), genetica=res.get('genetica'), motor=res.get('motor'), tam_total=res.get('tam_total'))
    out['mundo'] = dict(MUNDO_ULT)
    out['cfg_bq'] = dict(MB.BQ_CFG); out['cfg_nz'] = dict(MB.NZ_CFG)
    out['bloques'] = json.loads(json.dumps(MB.BQ_OUT, default=float)) if MB.BQ_CFG.get('on') else None
    out['nz'] = json.loads(json.dumps(MB.NZ_OUT, default=float)) if (MB.NZ_CFG.get('nuez') or MB.NZ_CFG.get('social')) else None
    out = dict(seed=seed, brazo=brazo, T=T, **out)
    out['med'] = medidas(out)
    with open(fn + '.tmp', 'w', encoding='utf-8') as f: json.dump(out, f)
    os.replace(fn + '.tmp', fn)
    if os.path.exists(fin_ns): os.remove(fin_ns)
    return out


def kbar(res):
    """K = media de tam_total en [T/2, T] (copia de corre_bloques.NS_kbar / corre_eco_sel_ing.kbar)."""
    tt = res.get('tam_total')
    if not tt: return None
    m = NS.MUNDO['muestra']; T = res['T']; n = T // m + 1; i0 = (T // 2) // m
    v = (list(tt) + [0] * max(0, n - len(tt)))[i0:n]
    return float(np.mean(v))


def _ventana(serie, fin, t0, t1):
    """Contadores al final (NZC_T) menos en t0 (ultima fila de la serie con t <= t0, o ceros)."""
    a = np.zeros(16, np.int64)
    for row in serie:
        if row[0] <= t0: a = np.array(row[2:18], np.int64)
    return np.array(fin, np.int64) - a   # fin = contadores al final (t1 = T, o la extincion)


def medidas(d):
    """Medidas por corrida (preregistradas en §6). Ventana [T/2, T]."""
    T = d['T']; Z = d.get('nz')
    if not Z or 'NZC_T' not in Z: return None
    sr = Z['serie']; w = _ventana(sr, Z['NZC_T'], T // 2, T)
    inten, abre, falla, a_com, a_com_ll = int(w[0]), int(w[1]), int(w[2]), int(w[3]), int(w[4])
    frac_ok = (abre / inten) if inten >= MIN_INT else 0.0
    p_ll_A = (a_com_ll / a_com) if a_com >= MIN_INT else None
    SI = (frac_ok - p_ll_A) if (inten >= MIN_INT and p_ll_A is not None) else None
    tt = d.get('tam_total') or []
    m = NS.MUNDO['muestra']
    i0 = (T // 2) // m; cs = float(np.sum(tt[i0:T // m + 1])) * m if tt else 0.0
    abre_pc = (abre / cs * 1000.0) if cs > 0 else 0.0   # nueces abiertas por cuerpo y 1000 pasos
    ult = sr[-1] if sr else None
    viv = ult[1] if ult else 0
    frac_copia = (ult[18] / viv) if (ult and viv) else None
    frac_sen_nuez = (ult[19] / viv) if (ult and viv) else None
    t_adq = None   # primera t con frac_ok >= 0.6 en la ventana movil de 20 000 pasos (>= MIN_INT intentos); descriptivo
    for i, row in enumerate(sr):
        t = row[0]
        if t < 20000: continue
        prev = next((r for r in reversed(sr[:i]) if r[0] <= t - 20000), None)
        a0 = np.array(prev[2:18]) if prev else np.zeros(16)
        dd = np.array(row[2:18]) - a0
        if dd[0] >= MIN_INT and dd[1] / dd[0] >= 0.6:
            t_adq = int(t); break
    return dict(intentos=inten, abre=abre, falla=falla, frac_ok=round(frac_ok, 4), p_llave_A=(None if p_ll_A is None else round(p_ll_A, 4)),
                SI=(None if SI is None else round(SI, 4)), abre_pc=round(abre_pc, 5), frac_copia_T=frac_copia, frac_sen_nuez_T=frac_sen_nuez,
                disparos=int(w[8]), monedas=int(w[9]), copias=int(w[10]), fuente_vacia=int(w[11]), desf_global=int(w[12]),
                nueces_creadas=int(w[7]), A_llegadas=int(w[6]), t_adq=t_adq, vivos_T=viv, nueces_T=Z.get('nueces_T'))


def tipo(r):
    s, p, c, th, a, w = r
    s = int(s); a = int(a)
    sen = SENT[s] + (f'{int(p)}' if s in (3, 4) else '')
    return f"{sen}{'>' if c > 0.5 else '<'}θ -> {ACC[a]}{'+' if w > 0 else '-'}"


# ================================================================ LA LETRA (PREREGISTRO_enriquecido.md §7-§8)
def veredicto(D, T=T_EXPLORA, sem=SEM_EXPLORA):
    """D[brazo][seed] = dict de corre(). Devuelve (veredicto, lineas, sub)."""
    L = []
    ss = [s for s in sem if all(s in D.get(b, {}) for b in EXPLORA_BR)]
    todo = [D[b][s] for b in EXPLORA_BR for s in ss]
    n = len(sem)
    v0 = (len(ss) == n and all(x.get('T') == T and x.get('t_corte') == T_CORTE and x.get('aborto') is None and x.get('bloqueados') == 0
                               for x in todo))

    def cfg_ok(x):
        bq, nz = cfg_de(x['brazo'])
        return x.get('carro') == FAB and x.get('cfg_bq') == bq and x.get('cfg_nz') == nz
    v1 = bool(todo) and all(cfg_ok(x) for x in todo)
    pers = {b: sum(1 for s in ss if D[b][s].get('persiste')) for b in EXPLORA_BR}
    M = lambda b, s: (D[b][s].get('med') or {})
    v2 = all(pers.get(b, 0) >= 3 for b in ('NUEZ_SOC', 'NUEZ_OFF', 'NUEZ_DESF'))   # H-1 del auditor: tambien DESF
    v3 = all(M(b, s).get('nueces_creadas', 0) > 0 for b in ('NUEZ_SOC', 'NUEZ_OFF', 'NUEZ_DESF') for s in ss if D[b][s].get('persiste')) \
        and all(M('REF', s).get('nueces_creadas', 1) == 0 and M('REF', s).get('copias', 1) == 0 for s in ss) \
        and all(M('NUEZ_OFF', s).get('copias', 1) == 0 for s in ss)
    L.append(f"V0 completo ({n} semillas x 4 brazos, T {T}, t_corte {T_CORTE}, sin abortos, bloqueados 0): {'SE CUMPLE' if v0 else 'NO SE CUMPLE'}")
    L.append(f"V1 cfg declarada por brazo (BQ y NZ) y carro FABRICA_ECO en cada JSON: {'SE CUMPLE' if v1 else 'NO SE CUMPLE'}")
    L.append(f"V2 el mundo con nueces es vivible (NUEZ_SOC, NUEZ_OFF y NUEZ_DESF persisten >= 3/5 cada uno): {'SE CUMPLE' if v2 else 'NO SE CUMPLE'} {pers}")
    L.append(f"V3 sanidad (hay nueces en NUEZ_*; REF sin nueces ni copias; OFF sin copias): {'SE CUMPLE' if v3 else 'NO SE CUMPLE'}")
    if not (v0 and v1 and v2 and v3):
        L.append('VEREDICTO: NO EVALUABLE'); return 'NO EVALUABLE', L, {}
    fo = lambda b, s: M(b, s).get('frac_ok', 0.0) or 0.0
    # H-1 del auditor: en P1 y P2 cuentan SOLO los pares validos (los dos brazos persisten y tienen >= MIN_INT intentos en la ventana);
    # se exigen >= 4 pares validos; con menos, la puerta NO SE CUMPLE.
    val = lambda b, s: bool(D[b][s].get('persiste')) and (M(b, s).get('intentos') or 0) >= MIN_INT
    s1 = [s for s in ss if val('NUEZ_SOC', s) and val('NUEZ_OFF', s)]
    s2 = [s for s in ss if val('NUEZ_SOC', s) and val('NUEZ_DESF', s)]
    d1 = [fo('NUEZ_SOC', s) - fo('NUEZ_OFF', s) for s in s1]
    d2 = [fo('NUEZ_SOC', s) - fo('NUEZ_DESF', s) for s in s2]
    med = lambda d: (float(np.median(d)) if d else float('nan'))
    si = [M('NUEZ_SOC', s).get('SI') for s in ss]
    si_off = [M('NUEZ_OFF', s).get('SI') for s in ss]
    p1 = len(s1) >= 4 and sum(x > 0 for x in d1) >= 4 and med(d1) >= 0.05
    p2 = len(s2) >= 4 and sum(x > 0 for x in d2) >= 4 and med(d2) >= 0.05
    p3 = sum(1 for x in si if x is not None and x >= 0.10) >= 3
    ps = sum(1 for x in si_off if x is not None and x >= 0.10) >= 3
    fc = lambda b, s: (M(b, s).get('frac_copia_T') or 0.0)
    d4 = [fc('NUEZ_SOC', s) - fc('NUEZ_DESF', s) for s in ss]
    p4 = sum(x > 0 for x in d4) >= 4
    L.append(f"P1 frac_ok(SOC) > frac_ok(OFF) en >= 4 pares validos (>= 4 exigidos) y mediana >= +0.05: {'SE CUMPLE' if p1 else 'NO SE CUMPLE'} "
             f"({sum(x > 0 for x in d1)}/{len(s1)} pares validos {s1}, mediana {med(d1):+.3f}; {[round(x, 3) for x in d1]})")
    L.append(f"P2 (control) frac_ok(SOC) > frac_ok(DESF) en >= 4 pares validos (>= 4 exigidos) y mediana >= +0.05: {'SE CUMPLE' if p2 else 'NO SE CUMPLE'} "
             f"({sum(x > 0 for x in d2)}/{len(s2)} pares validos {s2}, mediana {med(d2):+.3f}; {[round(x, 3) for x in d2]})")
    L.append(f"P3 la secuencia es real en SOC: SI = P(llave|nuez) - P(llave|A comun) >= 0.10 en >= 3/5: {'SE CUMPLE' if p3 else 'NO SE CUMPLE'} ({si})")
    L.append(f"PS (sub-veredicto, sin social) SI(OFF) >= 0.10 en >= 3/5: {'SE CUMPLE' if ps else 'NO SE CUMPLE'} ({si_off})")
    L.append(f"P4 (firma, no entra al veredicto) frac de vivos con 'copiar+' en T: SOC > DESF pareado >= 4/5: {'SE CUMPLE' if p4 else 'NO SE CUMPLE'} "
             f"({[round(x, 3) for x in d4]})")
    if p1 and p2 and p3: v = 'FUNCIONA'
    elif (p1 and p2) or (p3 and (p1 or p2)): v = 'HAY ALGO MODESTO'
    else: v = 'NO'
    L.append(f'VEREDICTO (social + secuencia, EXPLORATORIO): {v}')
    L.append(f"SUB-VEREDICTO (la seleccion arma la secuencia sin social): {'SI' if ps else 'NO'}")
    return v, L, dict(p1=p1, p2=p2, p3=p3, ps=ps, p4=p4, pers=pers, pares_p1=s1, pares_p2=s2)


def lee(carpeta, escribe=True):
    fs = sorted(glob.glob(os.path.join(carpeta, 'M_*.json')))
    D = {}
    for f in fs:
        d = json.load(open(f, encoding='utf-8')); D.setdefault(d['brazo'], {})[d['seed']] = d
    print(f'carpeta {carpeta}: brazos {list(D)}')
    cols = ('frac_ok', 'SI', 'p_llave_A', 'abre_pc', 'intentos', 'copias', 'disparos', 'frac_copia_T', 'frac_sen_nuez_T', 't_adq')
    for b in D:
        for s in sorted(D[b]):
            x = D[b][s]; m = x.get('med') or {}
            print(f"  {b:10s} s{s}: K {x.get('K') if x.get('K') is None else round(x['K'], 2)} · persiste {x.get('persiste')} · aborto {x.get('aborto')} · "
                  + ' · '.join(f"{c} {m.get(c) if not isinstance(m.get(c), float) else round(m.get(c), 3)}" for c in cols))
    for b in D:
        v = [D[b][s] for s in sorted(D[b])]
        if not v[0].get('bloques'): continue
        print(f'--- {b}: formas de regla en >= 30 % de los vivos en T')
        for d in v:
            vv = (d['bloques'] or {}).get('vivos_T') or []
            cnt = {}
            for x in vv:
                for t_ in set(tipo(r) for r in x[3]): cnt[t_] = cnt.get(t_, 0) + 1
            top = sorted(((c / max(1, len(vv)), t_) for t_, c in cnt.items()), reverse=True)
            print(f"  s{d['seed']} (vivos {len(vv)}): " + ' | '.join(f'{t_} {f:.2f}' for f, t_ in top if f >= 0.30))
    if all(b in D for b in EXPLORA_BR) and all(d.get('T') == T_EXPLORA for b in D for d in D[b].values()):
        v, L, sub = veredicto(D)
        for x in L: print(x)
        if escribe:
            with open(os.path.join(carpeta, 'VEREDICTO.json'), 'w', encoding='utf-8') as f:
                json.dump(dict(veredicto=v, lineas=L, sub=sub, T=T_EXPLORA, semillas=SEM_EXPLORA,
                               shas={os.path.basename(p_): h16(p_) for p_ in SHAS}), f, indent=1)
        return v
    print('(no es la explora completa: sin veredicto)')
    return None


def _job(a):
    seed, brazo, T, car, rean = a
    t0 = time.time()
    try:
        o = corre(seed, brazo, T, car, reanuda=rean)
    except KeyboardInterrupt:
        raise
    except BaseException as ex:   # nunca matar al trabajador del Pool: queda NO EVALUABLE por V0
        o = dict(seed=seed, brazo=brazo, T=T, aborto=f'{type(ex).__name__}: {ex}', K=None, persiste=None, bloqueados=None)
        fn = os.path.join(car, f'M_{brazo}_s{seed}.json')
        with open(fn + '.tmp', 'w', encoding='utf-8') as f: json.dump(o, f)
        os.replace(fn + '.tmp', fn)
    return seed, brazo, o, round(time.time() - t0, 1)


def explora(pool, rean):
    from multiprocessing import Pool
    car = os.path.join(DATOS, 'explora')
    os.makedirs(car, exist_ok=True)
    jobs = [(s, b, T_EXPLORA, car, rean) for b in EXPLORA_BR for s in SEM_EXPLORA]
    t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] explora: {len(jobs)} trabajos, pool {pool}, T {T_EXPLORA}, reanuda {rean}", flush=True)
    with Pool(pool) as P:
        for k, (s, b, o, seg) in enumerate(P.imap_unordered(_job, jobs), 1):
            m = o.get('med') or {}
            print(f"[{time.strftime('%H:%M:%S')}] [{k}/{len(jobs)}] {b} s{s}: K {o.get('K')} · persiste {o.get('persiste')} · "
                  f"frac_ok {m.get('frac_ok')} · SI {m.get('SI')} · copias {m.get('copias')} · aborto {o.get('aborto')} "
                  f"({seg} s; {time.time() - t0:.0f} s)", flush=True)
    lee(car)


def main():
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--explora', action='store_true')
    ap.add_argument('--pool', type=int, default=None); ap.add_argument('--reanuda', action='store_true')
    ap.add_argument('--lee', default=None)
    ap.add_argument('--practica', default=None)   # SOLO el creador: 'semilla:brazo:T[:clave=valor,...]' (50191-50199, T <= 200 000)
    a, resto = ap.parse_known_args()
    if resto: raise SystemExit(f'banderas desconocidas: {resto}')
    if a.lee:
        lee(a.lee if os.path.isabs(a.lee) else os.path.join(DATOS, a.lee)); return
    verifica()
    if a.explora:   # SOLO el coordinador
        if not a.pool or not 1 <= a.pool <= 2: raise SystemExit('--explora exige --pool entre 1 y 2 (PC compartido, 3 lineas a la vez)')
        explora(a.pool, a.reanuda); return
    if a.humo:
        car = os.path.join(DATOS, 'humo'); runs = [(HUMO['semilla'], b, HUMO['T']) for b in HUMO['brazos']]
    elif a.practica:
        pz = a.practica.split(':'); s = int(pz[0]); b = pz[1]; T = int(pz[2])
        ext = {kv.split('=')[0]: float(kv.split('=')[1]) for kv in pz[3].split(',')} if len(pz) > 3 else {}
        if not 50191 <= s <= 50199 or T > 200000 or b not in BRAZOS or any(k not in ('f', 'bonus', 'c_fallo') for k in ext):
            raise SystemExit('practica: semilla 50191-50199, T <= 200 000, brazo valido, solo f/bonus/c_fallo')
        car = os.path.join(DATOS, 'practica' + ('_' + '_'.join(f'{k}{v}' for k, v in ext.items()) if ext else '')); runs = [(s, b, T)]
    else:
        raise SystemExit('usa --humo, --practica, --explora --pool N [--reanuda] o --lee <carpeta>')
    t0 = time.time()
    for s, b, T in runs:
        o = corre(s, b, T, car, reanuda=a.reanuda, nz_extra=(ext if a.practica else None))
        m = o.get('med') or {}
        print(f"[{time.strftime('%H:%M:%S')}] {b} s{s} T{T}: K {o['K']} · persiste {o['persiste']} · aborto {o['aborto']} · "
              f"{json.dumps(m)} ({o['seg']} s; {time.time() - t0:.0f} s)", flush=True)
    lee(car, escribe=False)


if __name__ == '__main__':
    main()
