"""explora_termop.py -- EXPLORATORIO (no es serie, no decide nada) de TERMO' (memoria de lo sentido con olvido; construye_termop.py).
MISION: llegar a la AGI por este camino. Encargo del coordinador (28-sep): (a) en el examen, ¿TERMO' ya no muerde A en Q4 tras la
inversion?; (b) en la carrera, ¿conserva el efecto de TERMO? (5 semillas nuevas, contra V143_TERMO en las mismas semillas).

  --examen            UN proceso. E2 (examen v3', invierte en 50 000; T 100 000) y T-C (ii) (mundo vivo, invierte en T/2) con v14.3,
                      TERMO (organismo_v144*) y TERMO' (organismo_v144b*), 2 semillas; + dos chequeos de mundo QUIETO (E1 y T-A
                      CUELLO_MIN, 1 semilla): TERMO' == TERMO bit a bit?
  --carrera --pool N  (N <= 2) la pista de TERMO tal cual (corre_termo.tarea = corre_v143.tarea: 9 carros iguales, L 360, T 100 000,
                      fundador limpio) con V143_TERMO y V143_TERMOP en 5 semillas: R0 real (mediana de los 9 linajes), semillas con
                      mayoria que cruza, y si las dos corridas son IDENTICAS.
JSON en esta carpeta, datos/. Todo EXPLORATORIO.
"""
import argparse, hashlib, importlib.util, json, os, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
V144 = os.path.join(RAIZ, 'experimentos', 'tronco_v14_4_examen')
TERMO_D = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')
for _d in (AQUI, V144, TERMO_D):
    if _d not in sys.path: sys.path.insert(0, _d)
SEM_EX = [49001, 49002]            # busca_semillas_v144b.py: libres
SEM_CARRERA = [49011, 49012, 49013, 49014, 49015]


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def log(f, m):
    l = f"[{time.strftime('%H:%M:%S')}] {m}"; print(l, flush=True); f.write(l + '\n'); f.flush()


# ------------------------------------------------------------------ (a) examen
def examen(f):
    import corre_examen_v144 as R
    import organismo_v143 as V143, organismo_v144 as V144o, organismo_v144b as V144B
    import organismo_v3cal as CAL, organismo_v144cal as V144C, organismo_v144bcal as V144BC
    out = dict(E2=[], TCii=[], quieto={})
    ET = R.B143.ETAPAS
    for s in SEM_EX:
        row = dict(seed=s)
        for nom, m in (('v143', V143), ('termo', V144o), ('termop', V144B)):
            r = m.run(s, **ET['E2'])
            row[nom] = dict(mordA=r['mord']['A'], mordB=r['mord']['B'], deaths=r['deaths'], W=r['W'],
                            memA=(r.get('termo') or {}).get('adS', {}).get('A'))
        out['E2'].append(row)
        log(f, f"E2 s{s}: muerde A por cuarto  v14.3 {row['v143']['mordA']}  TERMO {row['termo']['mordA']}  TERMO' {row['termop']['mordA']} | "
               f"come B Q4 {row['v143']['mordB'][3]}/{row['termo']['mordB'][3]}/{row['termop']['mordB'][3]} | muertes "
               f"{row['v143']['deaths']}/{row['termo']['deaths']}/{row['termop']['deaths']} | memoria de A al final TERMO {row['termo']['memA']} TERMO' {row['termop']['memA']}")
        kw = R.C4.kw_rev('OFF', R.U.T_VIVO)
        row = dict(seed=s)
        for nom, m, extra in (('v143', CAL, {}), ('termo', V144C, R.PIEZA), ('termop', V144BC, R.PIEZA)):
            r = m.run(s, T=R.U.T_VIVO, **dict(kw, **extra))
            row[nom] = dict(mordA=r['mord']['A'], mordB=r['mord']['B'], rev=r['mord']['B'][3] - r['mord']['A'][3], deaths=r['deaths'],
                            memA=(r.get('termo') or {}).get('adS', {}).get('A'))
        out['TCii'].append(row)
        log(f, f"T-C ii s{s}: rev v14.3 {row['v143']['rev']}  TERMO {row['termo']['rev']}  TERMO' {row['termop']['rev']} | muerde A por cuarto "
               f"{row['v143']['mordA']} / {row['termo']['mordA']} / {row['termop']['mordA']} | muertes {row['v143']['deaths']}/{row['termo']['deaths']}/"
               f"{row['termop']['deaths']} | memoria de A TERMO {row['termo']['memA']} TERMO' {row['termop']['memA']}")
    s = SEM_EX[0]
    a, b = V144o.run(s, **ET['E1']), V144B.run(s, **ET['E1'])
    ks = [k for k in a if k != 'termo']
    out['quieto']['E1'] = dict(identicos=all(json.dumps(a[k], sort_keys=True, default=str) == json.dumps(b[k], sort_keys=True, default=str) for k in ks),
                               termo=a['termo']['mord'], termop=b['termo']['mord'])
    kw = R.kw_vivo_cand('CUELLO_MIN')
    a, b = V144C.run(s, T=R.U.T_VIVO, **kw), V144BC.run(s, T=R.U.T_VIVO, **kw)
    ks = [k for k in a if k != 'termo']
    out['quieto']['CUELLO_MIN'] = dict(identicos=all(json.dumps(a[k], sort_keys=True, default=str) == json.dumps(b[k], sort_keys=True, default=str) for k in ks),
                                       r=(a['descendientes'] - a['deaths'], b['descendientes'] - b['deaths']))
    log(f, f"mundo QUIETO s{s}: E1 TERMO' == TERMO (todas las claves del organismo): {out['quieto']['E1']['identicos']} | "
           f"T-A CUELLO_MIN TERMO' == TERMO: {out['quieto']['CUELLO_MIN']['identicos']} (r {out['quieto']['CUELLO_MIN']['r']})")
    return out


# ------------------------------------------------------------------ (b) carrera
def tarea_carrera(args):
    seed, ident, T = args
    import corre_termo as CT
    CT.registra()
    if ident == 'V143_TERMOP' and ident not in CT.CV._MODS:
        spec = importlib.util.spec_from_file_location('carro_V143_TERMOP', os.path.join(AQUI, 'carros', 'V143_TERMOP.py'))
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CT.CV._MODS[ident] = m
    x = CT.tarea((seed, ident, T)); x.pop('pizarra_log', None); x['ident'] = ident
    return x


def carrera(f, pool, T):
    import statistics as st
    tareas = [(s, c, T) for s in SEM_CARRERA for c in ('V143_TERMO', 'V143_TERMOP')]
    log(f, f"(b) carrera: {len(tareas)} corridas, T {T}, Pool {pool}")
    if pool <= 1:
        res = [tarea_carrera(t) for t in tareas]
    else:
        import multiprocessing as mp
        mp.set_start_method('spawn', force=True)
        res = []
        with mp.Pool(pool) as p:
            for r in p.imap_unordered(tarea_carrera, tareas, chunksize=1):
                res.append(r); log(f, f"   {r['ident']} s{r['seed']} listo ({r['seg']} s)")
    por = {(r['seed'], r['ident']): r for r in res}
    filas = []
    for s in SEM_CARRERA:
        a, b = por[(s, 'V143_TERMO')], por[(s, 'V143_TERMOP')]
        R0 = lambda r: round(st.median([l['R0_real'] for l in r['linajes']]), 4)
        may = lambda r: sum(l['cruza_real'] for l in r['linajes']) * 2 > len(r['linajes'])
        sin_id = lambda r: [{k: v for k, v in l.items() if k != 'id'} for l in r['linajes']]   # 'id' lleva el nombre del carro
        ident = json.dumps(sin_id(a), sort_keys=True, default=str) == json.dumps(sin_id(b), sort_keys=True, default=str)
        fila = dict(seed=s, R0_termo=R0(a), R0_termop=R0(b), mayoria_termo=may(a), mayoria_termop=may(b), identicas=ident,
                    fund=(st.median([l['fundadores'] for l in a['linajes']]), st.median([l['fundadores'] for l in b['linajes']])))
        filas.append(fila)
        log(f, f"   s{s}: R0 real TERMO {fila['R0_termo']} TERMO' {fila['R0_termop']} | mayoria que cruza {fila['mayoria_termo']}/{fila['mayoria_termop']} | "
               f"fundadores {fila['fund']} | corridas IDENTICAS: {ident}")
    return dict(filas=filas, crudos=res)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--examen', action='store_true'); g.add_argument('--carrera', action='store_true')
    ap.add_argument('--pool', type=int, default=1); ap.add_argument('--T', type=int, default=100000)
    a = ap.parse_args()
    if not 1 <= a.pool <= 2: ap.error('--pool 1 o 2 (encargo: dos procesos como maximo)')
    os.makedirs(os.path.join(AQUI, 'datos'), exist_ok=True)
    nom = f"explora_termop_{'examen' if a.examen else 'carrera'}_{time.strftime('%Y%m%d_%H%M%S')}"
    f = open(os.path.join(AQUI, 'datos', nom + '.log'), 'w', encoding='utf-8')
    shas = {n: h16(os.path.join(AQUI, n)) for n in ('construye_termop.py', os.path.join('carros', 'V143_TERMOP.py'), 'organismo_v144b.py',
                                                  'organismo_v144bcal.py', 'explora_termop.py')}
    log(f, f"EXPLORATORIO TERMO' — {'examen' if a.examen else 'carrera'}; shas {shas}")
    out = examen(f) if a.examen else carrera(f, a.pool, a.T)
    dj = os.path.join(AQUI, 'datos', nom + '.json')
    json.dump(dict(exploratorio=True, shas=shas, **out), open(dj, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    log(f, f"datos -> {os.path.relpath(dj, RAIZ)}  sha256_16 = {h16(dj)}")
