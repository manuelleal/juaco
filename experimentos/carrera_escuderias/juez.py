"""juez.py — EL JUEZ DE LA CARRERA DE ESCUDERIAS (REGLAMENTO sec. 7). Fijo: se commitea antes de la ronda 0.

MISION: llegar a la AGI por este camino. Corre una RONDA (lista de carros, semillas, T) en pista.py y
calcula por linaje, con la definicion de H-1 (corre_f9.py:193-207):
  R0 = descendientes / (muertes + 1) · vida mediana (vidas_h1, la ultima truncada en T, como corre_f9)
  muertes · descendientes · fundadores · causas de muerte (hambre / sed / veneno / sal; veneno = murio por
  energia habiendo mordido B en sus ultimos W_CAUSA=400 pasos; sal = idem por agua con D) · p1/c1 (F9)
  · exposiciones a A y C · escrituras por linaje (hasta 3000 en la telemetria). La pizarra COMPLETA se guarda
  aparte en <prefijo>_pizarra.jsonl.gz (una linea [semilla, t, id, contenido] por escritura publicada).
Y de la pista: R0_pista = sum(descendientes) / (sum(muertes) + n_linajes) · composicion del mundo por cuarto de T.
ERR-96: TODO sale de las claves FISICAS de primer nivel que escribe pista.py (resumen_linaje); lo que devuelve
el carro (d['carro']) no se lee; la contabilidad fisica tiene que cerrar (coherente). Test: test_tramposo.py.
ENMIENDA 1: --escala 1 por defecto (L = 40N, nobj = 4N; con N = 1 es la pista original).

Antes de correr, el juez comprueba (0) el CHEQUEO ESTATICO de cada carro (revisa_carro.py; si uno falla, NO
corre), (1) el sha de organismo_f9c.py y (2) la IDENTIDAD CORTA: FABRICA solo, compat=1, pizarra 0 ==
organismo_f9c REL bit a bit (s=1, T=5000). Si falla, NO corre (el arnes completo es identidad_pista.py).
Registra el sha de cada carro: la ronda queda atada a esas versiones.

    python experimentos/carrera_escuderias/juez.py --humo                          (UN proceso: ronda 0, 9 FABRICA, 4001-4002)
    python experimentos/carrera_escuderias/juez.py --ronda 1 --carros O1,O2,...,H3 --desde 4001 --n 20 --pool 6   (SOLO el coordinador)

POOL (ERR-86): --pool o JUACO_POOL; 0 = un proceso. Los agentes no corren Pool (regla 3).
ERR-54: el crudo se escribe ANTES de resumir. VOCABULARIO: "linaje", "cuerpo", "R0 del linaje"; no
"poblacion", "generacion", "evoluciona", "coopera" (REGLAMENTO sec. 6).
"""
import argparse, gzip, json, os, platform, statistics as st, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
import pista as P
import revisa_carro as RC

DATOS = os.path.join(AQUI, 'datos')
REF_REL = dict(R0=0.395, R0_acum1=0.483, fuente='bloque 2, replica 1601-1620, un cuerpo a la vez (REGLAMENTO sec. 1)')
PRED_RONDA0 = {0: (0.15, 0.35),   # prediccion firmada del organizador, pista SIN escalar (REGLAMENTO sec. 1)
               1: (0.35, 0.55)}   # ENMIENDA 1: pista escalada L=40N, nobj=4N (firmada por el coordinador)
T_DEF = 100000


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 3) if xs else None


def frac(xs):
    ys = [x for x in xs if x >= 0]
    return round(sum(ys) / len(ys), 4) if ys else None


def identidad_corta():
    sys.path[:0] = [os.path.join(RAIZ, 'experimentos', d) for d in
                    ('nivel09_cuerpo_nuevo_b2', 'nivel09_cuerpo_nuevo', 'nivel13_alma', 'nivel11_mundo_vivo')] + [os.path.join(RAIZ, 'organismo')]
    _a = sys.argv; sys.argv = [sys.argv[0]]
    import corre_bloque2 as CB, organismo_f9c as F9C
    sys.argv = _a
    N = lambda x: json.loads(json.dumps(x, default=str))
    sha = P.h16(P.ORIGEN)
    a = F9C.run(1, T=5000, **CB.BRAZOS['REL'])
    b = P.plano(P.run(1, ['FABRICA'], T=5000, pizarra=0, compat=1)['linajes'][0])
    dif = [k for k in a if k not in b or N(a[k]) != N(b[k])] + [k for k in b if k not in a]
    return dict(sha_f9c=sha, sha_ok=(sha == P.SHA_F9C), dif=dif, ok=(sha == P.SHA_F9C and not dif))


FISICAS = ('descendientes', 'deaths', 'vidas_h1', 'fundadores', 'muertes_nec', 'exposiciones', 'mord', 'pasos_viables',
           'T_efectivo', 'cola_final', 'desc_por_vida', 'nacimientos', 'origen_cuerpo', '_carrera')


def resumen_linaje(d, seed):
    """ERR-96: SOLO la verdad FISICA de la pista (claves de primer nivel escritas por pista.py). d['carro'] (lo
    que devuelve el carro) NO se lee. Ademas la contabilidad fisica tiene que cerrar (coherente)."""
    f = {k: d[k] for k in FISICAS}
    c = f['_carrera']; p1 = c['p1']; c1 = c['c1']; mu = f['deaths']; v = f['vidas_h1']
    coh = (f['nacimientos'] == mu and len(v) == mu + 1 and len(f['desc_por_vida']) == mu + 1
           and sum(v) == f['T_efectivo'] and sum(f['desc_por_vida']) == f['descendientes']
           and len(f['origen_cuerpo']) == mu + 1 and f['fundadores'] + 1 == sum(1 for g in f['origen_cuerpo'] if not g)
           and sum(c['causas'].values()) == mu)
    return dict(id=c['id'], indice=c['indice'], seed=seed, descendientes=f['descendientes'], muertes=mu,
                R0=round(f['descendientes'] / (mu + 1), 4), r=f['descendientes'] - mu,
                vida_med=med(v), cuerpos=len(v), fundadores=f['fundadores'], coherente=bool(coh),
                causas=c['causas'], muertes_nec=f['muertes_nec'], p1=frac(p1), c1=frac(c1),
                exp_A=f['exposiciones']['A'], exp_C=f['exposiciones']['C'],
                mord={k: sum(x) for k, x in f['mord'].items()}, pasos_viables=f['pasos_viables'],
                sac_frac=round(f['pasos_viables'] / f['T_efectivo'], 4), cola_final=f['cola_final'],
                escrituras=c['escrituras'], vetos=c['vetos'],
                telem=dict(vidas=v, desc_por_vida=f['desc_por_vida'], causa_cuerpo=c['causa_cuerpo'], escr=c['escr']))


def tarea(args):
    seed, carros, T, pizarra, rep_acum, escala = args
    t0 = time.time()
    r = P.run(seed, carros, T=T, pizarra=pizarra, rep_acum=rep_acum, escala=escala)
    L = [resumen_linaje(d, seed) for d in r['linajes']]
    sd = sum(x['descendientes'] for x in L); sm = sum(x['muertes'] for x in L)
    return dict(seed=seed, seg=round(time.time() - t0, 1), linajes=L, pista=r['pista'],
                R0_pista=round(sd / (sm + len(L)), 4), pizarra_log=r['pizarra_log'])


def agrega(R):
    ids = R[0]['pista']['ids']
    tab = []
    for i, ident in enumerate(ids):
        xs = [c['linajes'][i] for c in R]
        cz = {k: sum(x['causas'][k] for x in xs) for k in ('hambre', 'sed', 'veneno', 'sal')}
        tab.append(dict(id=ident, R0_med=med([x['R0'] for x in xs]), R0=[x['R0'] for x in xs],
                        vida_med=med([x['vida_med'] for x in xs]), muertes=med([x['muertes'] for x in xs]),
                        descendientes=med([x['descendientes'] for x in xs]), fundadores=med([x['fundadores'] for x in xs]),
                        p1=med([x['p1'] for x in xs]), c1=med([x['c1'] for x in xs]), exp_A=med([x['exp_A'] for x in xs]),
                        sac_frac=med([x['sac_frac'] for x in xs]), causas=cz,
                        cruza_09=sum(1 for x in xs if x['R0'] >= 0.9), n=len(xs)))
    return tab, med([c['R0_pista'] for c in R])


def informe(R, meta, log):
    tab, r0p = agrega(R)
    log(f"\nRESUMEN · {meta['etiqueta']} · semillas {meta['semillas']} · T={meta['T']} · pizarra {meta['pizarra']} · rep_acum {meta['rep_acum']}")
    log(f"  {'linaje':12s} {'R0 med':>7} {'R0 por semilla':>22} {'vida':>7} {'muert':>6} {'desc':>5} {'fund':>5} "
        f"{'p1':>5} {'c1':>5} {'expA':>6} {'sac':>6}  causas (hambre/sed/veneno/sal)  >=0.9")
    for x in tab:
        cz = x['causas']; tot = max(1, sum(cz.values()))
        log(f"  {x['id']:12s} {str(x['R0_med']):>7} {str(x['R0']):>22} {str(x['vida_med']):>7} {str(x['muertes']):>6} "
            f"{str(x['descendientes']):>5} {str(x['fundadores']):>5} {str(x['p1']):>5} {str(x['c1']):>5} {str(x['exp_A']):>6} "
            f"{str(x['sac_frac']):>6}  {cz['hambre']}/{cz['sed']}/{cz['veneno']}/{cz['sal']} "
            f"({cz['hambre']/tot:.0%}/{cz['sed']/tot:.0%}/{cz['veneno']/tot:.0%}/{cz['sal']/tot:.0%})  {x['cruza_09']}/{x['n']}")
    log(f"  R0 de la pista (mediana por semilla de sum desc / (sum muertes + n)): {r0p} · por semilla {[c['R0_pista'] for c in R]}")
    for c in R:
        fq = [round((q['B'] + q['D']) / max(1e-9, sum(q.values())), 3) for q in c['pista']['comp_mundo_q']]
        log(f"  semilla {c['seed']}: fraccion B+D del mundo por cuarto de T {fq} · L {c['pista']['L']} nobj {c['pista']['nobj']}")
    log(f"  contabilidad fisica coherente: {sum(l['coherente'] for c in R for l in c['linajes'])}/{sum(len(c['linajes']) for c in R)}")
    log(f"  mundo: objetos medios por tipo (A comida, B veneno, C agua, D sal; nobj={R[0]['pista']['nobj']}) por semilla "
        f"{[c['pista']['comp_mundo'] for c in R]} · olvidos {[c['pista']['olvidos'] for c in R]}")
    ms = [{k: sum(l['mord'][k] for l in c['linajes']) for k in 'ABCD'} for c in R]
    log(f"  mordidas totales por tipo por semilla {ms}")
    log(f"  referencia UN cuerpo a la vez: REL {REF_REL['R0']} (acum 1: {REF_REL['R0_acum1']}) -- {REF_REL['fuente']}")
    return tab, r0p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--ronda', default='0')
    ap.add_argument('--carros', default=','.join(['FABRICA'] * 9))
    ap.add_argument('--desde', type=int, default=4001)
    ap.add_argument('--n', type=int, default=20)
    ap.add_argument('--T', type=int, default=T_DEF)
    ap.add_argument('--pizarra', type=int, default=1)
    ap.add_argument('--rep_acum', type=int, default=0)
    ap.add_argument('--escala', type=int, default=1)   # ENMIENDA 1
    ap.add_argument('--pool', type=int, default=int(os.environ.get('JUACO_POOL', 0)))
    a = ap.parse_args()
    carros = [c for c in a.carros.split(',') if c]
    if a.humo:
        semillas = [4001, 4002]; pool = 0; etiqueta = f"humo_ronda{a.ronda}"
    else:
        semillas = list(range(a.desde, a.desde + a.n)); pool = a.pool; etiqueta = f"ronda{a.ronda}_s{semillas[0]}-{semillas[-1]}"
    os.makedirs(DATOS, exist_ok=True)
    sel = time.strftime('%Y%m%d_%H%M%S'); pre = f"carrera_{etiqueta}_{sel}"
    LOGF = open(os.path.join(DATOS, pre + '.log'), 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); LOGF.write(s + '\n'); LOGF.flush()

    t0 = time.time()
    shas = {c: P.h16(os.path.join(P.CARROS, c + '.py')) for c in sorted(set(carros))}
    log(f"JUEZ · {etiqueta} · {time.strftime('%Y-%m-%d %H:%M:%S')} · python {platform.python_version()} · pool {pool or 'NO (un proceso)'}")
    log(f"  pista.py {P.h16(os.path.join(AQUI,'pista.py'))} · juez.py {P.h16(os.path.abspath(__file__))} · carros {shas}")
    log(f"  carros (orden = indice de linaje): {carros} · semillas {semillas[0]}-{semillas[-1]} · T={a.T} · pizarra {a.pizarra} · rep_acum {a.rep_acum} · escala {a.escala}")
    rv = {c: RC.revisa(c) for c in sorted(set(carros))}
    for c, v in rv.items():
        log(f"  CHEQUEO ESTATICO {c}: {'PASA' if not v else 'RECHAZADO'}" + ''.join(chr(10) + '     ' + x for x in v))
    if any(rv.values()):
        log("  UN CARRO NO PASA EL CHEQUEO ESTATICO (ERR-96) -> la ronda NO se corre."); return 1
    ide = identidad_corta()
    log(f"  IDENTIDAD CORTA: sha f9c {ide['sha_f9c']} ({'OK' if ide['sha_ok'] else 'DISTINTO'}) · FABRICA solo == organismo_f9c REL "
        f"(s=1, T=5000): {'OK' if not ide['dif'] else 'FALLA ' + str(ide['dif'][:5])}")
    if not ide['ok']:
        log("  IDENTIDAD FALLA -> la ronda NO se corre."); return 1
    tareas = [(s, carros, a.T, a.pizarra, a.rep_acum, a.escala) for s in semillas]
    R = []
    if pool and pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as PL:
            for x in PL.imap_unordered(tarea, tareas):
                R.append(x); log(f"  [{time.time()-t0:7.1f}s] semilla {x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']}")
    else:
        for tk in tareas:
            x = tarea(tk); R.append(x)
            log(f"  [{time.time()-t0:7.1f}s] semilla {x['seed']} ({x['seg']}s) R0 pista {x['R0_pista']} · R0 por linaje "
                f"{[l['R0'] for l in x['linajes']]}")
    R.sort(key=lambda x: x['seed'])
    piz = os.path.join(DATOS, pre + '_pizarra.jsonl.gz')   # ENMIENDA 1: la pizarra COMPLETA, aparte de la telemetria
    with gzip.open(piz, 'wt', encoding='utf-8') as fz:
        for x in R:
            for e in x.pop('pizarra_log'): fz.write(json.dumps([x['seed']] + e) + chr(10))
    meta = dict(etiqueta=etiqueta, ronda=a.ronda, sello=sel, semillas=semillas, T=a.T, pizarra=a.pizarra, rep_acum=a.rep_acum,
                carros=carros, sha_carros=shas, escala=a.escala, chequeo_estatico=rv, sha_pista=P.h16(os.path.join(AQUI, 'pista.py')),
                sha_juez=P.h16(os.path.abspath(__file__)), sha_f9c=ide['sha_f9c'], identidad_corta=ide,
                W_CAUSA=P.W_CAUSA, CUPO=P.CUPO, ANCHO=P.ANCHO, ref=REF_REL)
    crudo = os.path.join(DATOS, pre + '.json')     # ERR-54: el crudo ANTES de resumir
    json.dump(dict(meta=meta, corridas=R), open(crudo, 'w', encoding='utf-8'), ensure_ascii=False)
    log(f"  CRUDO {crudo} (sha {P.h16(crudo)})")
    tab, r0p = informe(R, meta, log)
    log(f"  PIZARRA completa {piz}")
    if carros == ['FABRICA'] * 9:
        todos = [l['R0'] for c in R for l in c['linajes']]
        mr = med(todos); lo, hi = PRED_RONDA0[1 if a.escala else 0]
        log(f"\n  PREDICCION FIRMADA ({'ENMIENDA 1, pista escalada' if a.escala else 'organizador, pista sin escalar'}): con 9 FABRICA "
            f"la mediana del R0 por linaje cae en {lo}-{hi}. Medido: mediana de los {len(todos)} linajes-semilla {mr} "
            f"(min {min(todos)}, max {max(todos)}) -> {'DENTRO del rango' if lo <= mr <= hi else ('DEBAJO del rango' if mr < lo else 'ENCIMA del rango')}")
    res = os.path.join(DATOS, pre + '_resumen.json')
    json.dump(dict(meta=meta, tabla=tab, R0_pista=r0p), open(res, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    log(f"  RESUMEN {res}")
    log(f"\nTerminado en {time.time()-t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
