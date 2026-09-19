"""SERIE CONFIRMATORIA del creador B (junta de la fase 5) -- LECTURA CONJUNTIVA (`mem_conj`).
La corre EL COORDINADOR. Semillas 821-840 y replica 841-860, T = 100 000.

MISION: llegar a la AGI por este camino. Hoy: que el mensaje refiera a la FAMILIA **Y** a la VARIANTE con la
misma tabla -- BAR-T <= 5/20 y PAR >= 15/20 a la vez, sin subir la base sin mensaje.

FACTORIAL (2 x 2, todo dentro de la misma serie; el control del sufijo va DENTRO, no en otra serie):
  k3v0m0c0j0 = organismo_familias_b5 con k = 3   BIT A BIT   (linea base de FAMILIA)
  k3v1m0c0j0 = organismo_familias_b6 con k = 3   BIT A BIT   (linea base de VARIANTE)
  k3v1m0c0j1 = EL CANDIDATO (sufijo + lectura conjuntiva)
  k3v0m0c0j1 = control: conjuncion SIN sufijo (predigo BAR-H alto: el sufijo sigue haciendo falta)

POOL CONFIGURABLE (pedido del coordinador; hubo BrokenPipe con Pool(14) y otras corridas a la vez):
  variable de entorno  JUACO_POOL  (default 6).  Tambien  --pool N  en la linea de comandos (gana la bandera).

COSTE: 20 emisores + 4 celdas x 7 brazos x 20 semillas = 580 corridas de 100 000 pasos por serie.
  Medido en el humo: ~4.3 s por corrida a T = 30 000 con la maquina cargada  ->  ~14 s a T = 100 000.
  Estimacion por serie:  Pool(5) ~ 27 min   Pool(6) ~ 23 min   Pool(12) ~ 11 min   (pared, no CPU).

REGLAS: ERR-54 (los crudos se guardan ANTES del analisis, y cada vez que llega un resultado); ERR-70 (P-I4 es
exclusion por semilla y se reporta); P-I2 (semillas sin mensaje excluidas y reportadas); P-I3 (prefijo exacto
contra el gemelo); ERR-44 (todo por conducta de la boca); ERR-31 (se importan los objetos del bloque 5/6);
ERR-28 (organismo/ primero en sys.path). El EMISOR corre con k=1 y las tres perillas en 0: b4b BIT A BIT.

Uso (el comando que pide el coordinador):
  set JUACO_POOL=6
  python experimentos/junta_fase5/B/corre_jb_serie.py --desde 821
  python experimentos/junta_fase5/B/corre_jb_serie.py --desde 841
"""
import json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]

import numpy as np
import corre_jb_humo as H          # ERR-31: se importan sus objetos (celdas, brazos, emisor, corre, lectura)

T = 100000
N_SEM = 20
DESDE = 821
CELDAS = ['k3v0m0c0j0', 'k3v1m0c0j0', 'k3v1m0c0j1', 'k3v0m0c0j1']
PLANTILLA = H.PLANTILLA


def tarea(a):
    """Una corrida. Con `spawn` cada proceso reimporta el modulo: por eso todo es de nivel de modulo."""
    tipo = a[0]
    if tipo == 'E':
        _, s, Ti = a
        return dict(tipo='E', seed=s, msg=H.emisor(s, Ti))
    _, base, modo, pat, otro, par, cel, s, msg, Ti = a
    return dict(tipo='R', **H.corre(base, modo, pat, otro, par, cel, s, msg, Ti))


if __name__ == '__main__':
    import multiprocessing as mp
    mp.set_start_method('spawn', force=True)
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    Ti = arg('--T', T)
    desde = arg('--desde', DESDE)
    npool = arg('--pool', int(os.environ.get('JUACO_POOL', 6)))
    if '--celdas' in sys.argv:
        CELDAS = [c.strip() for c in sys.argv[sys.argv.index('--celdas') + 1].split(',') if c.strip()]
    SEEDS = list(range(desde, desde + arg('--n', N_SEM)))
    if not all(821 <= s <= 860 for s in SEEDS):
        print(f"  AVISO: semillas {SEEDS[0]}-{SEEDS[-1]} fuera del rango confirmatorio 821-860.", flush=True)
    t0 = time.time()
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CRUDO = os.path.join(RAIZ, 'datos', f'jb_serie_s{SEEDS[0]}-{SEEDS[-1]}_{stamp}_crudo.json')
    log = lambda m: print(f"  [{time.time()-t0:7.1f}s] {m}", flush=True)
    shas = dict(instrumento=H.h16(os.path.join(AQUI, 'organismo_familias_jb.py')),
                constructor=H.h16(os.path.join(AQUI, 'construye_familias_jb.py')),
                arnes=H.h16(os.path.join(AQUI, 'identidad_familias_jb.py')),
                runner_humo=H.h16(os.path.join(AQUI, 'corre_jb_humo.py')),
                runner=H.h16(os.path.abspath(__file__)),
                propuesta=H.h16(os.path.join(AQUI, 'PROPUESTA.md')),
                origen_b6=H.h16(os.path.join(N12, 'organismo_familias_b6.py')),
                origen_b5=H.h16(os.path.join(N12, 'organismo_familias_b5.py')),
                tronco_v14=H.h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))
    for nom, esp in (('origen_b6', H.SHA_B6_ESPERADO), ('origen_b5', H.SHA_B5_ESPERADO),
                     ('tronco_v14', H.SHA_V14_ESPERADO)):
        if shas[nom] != esp:
            raise SystemExit(f"ORIGEN {nom}: sha {shas[nom]}, se esperaba {esp}. Abortado.")
    print(f"SERIE JB (LECTURA CONJUNTIVA) semillas {SEEDS[0]}-{SEEDS[-1]}, T = {Ti}, celdas {CELDAS}, "
          f"{len(PLANTILLA)} brazos, Pool({npool})")
    for k, v in shas.items():
        print(f"  sha {k:14s} {v}")
    guarda = lambda res, msgs: json.dump(dict(shas=shas, T=Ti, seeds=SEEDS, celdas=CELDAS, pool=npool,
                                              msgs=msgs, res=res),
                                         open(CRUDO, 'w', encoding='utf-8', newline='\n'))

    with mp.Pool(npool) as pool:
        # ---------------- 1. EMISORES (uno por semilla; el mismo mensaje para todas las celdas)
        msgs = {}
        for r in pool.imap_unordered(tarea, [('E', s, Ti) for s in SEEDS]):
            msgs[r['seed']] = r['msg']
            guarda([], msgs)
        SEM_MSG = [s for s in SEEDS if msgs.get(s) is not None]
        log(f"P-I2: emisores con mensaje {len(SEM_MSG)}/{len(SEEDS)} (>= 18/20 exige la letra); "
            f"sin mensaje: {[s for s in SEEDS if s not in SEM_MSG]}")

        # ---------------- 2. RECEPTORES (crudo tras CADA corrida: ERR-54)
        tr = [('R', b, m, p, o, ph, cel, s, msgs[s], Ti)
              for cel in CELDAS for (b, m, p, o, ph) in PLANTILLA for s in SEM_MSG]
        log(f"{len(tr)} corridas de {Ti} pasos...")
        res = []
        for r in pool.imap_unordered(tarea, tr):
            res.append(r)
            guarda(res, msgs)
            if len(res) % 40 == 0:
                log(f"  {len(res)}/{len(tr)}")
    log(f"crudos en {os.path.relpath(CRUDO, RAIZ)}")

    # ---------------- 3. ANALISIS (desde los crudos; si esto se cae, los datos ya estan salvados)
    por = lambda base, cel: [x for x in res if x['base'] == base and x['cel'] == cel]
    util = {}
    for cel in CELDAS:
        util[cel] = [s for s in SEM_MSG
                     if all((x['t_X'] is not None and x['t_entrega'] is not None and x['t_X'] >= x['t_entrega'])
                            for x in res if x['cel'] == cel and x['seed'] == s
                            and x['base'] in ('CANAL', 'CORTADO'))]
        malos = [(b, s) for (b, m, p, o, ph) in PLANTILLA if m == 'sen' for s in SEM_MSG
                 for a in [[x for x in res if x['base'] == b and x['cel'] == cel and x['seed'] == s]]
                 for g in [[x for x in res if x['base'] == ('PAR0' if b.startswith('PAR') else 'CORTADO')
                            and x['cel'] == cel and x['seed'] == s]]
                 if a and g and a[0]['prefijo'] != g[0]['prefijo']]
        print(f"  P-I3 {cel}: {'OK' if not malos else 'CAE en ' + str(malos[:5])}   |   P-I4 utilizables "
              f"{len(util[cel])}/{len(SEM_MSG)}  (excluidas: {[s for s in SEM_MSG if s not in util[cel]]})")
        # P-I5, POR BRAZO (pregunta 3 de PROPUESTA.md): la boca leyo la via LENTA (fam1 = 0) ante el referente
        f1 = {b: sum(1 for x in por(b, cel) if x['seed'] in util[cel] and x['fam1'] == 1) for b, *_ in PLANTILLA}
        print(f"       P-I5 por brazo (semillas con fam1 = 1, o sea el mensaje escrito y NO consultado): {f1}")

    n_de = H.n_de
    cab = f"  {'brazo':10s}" + ''.join(f"{c:>14s}" for c in CELDAS)
    print(f"\n{'='*100}\nBRAZOS (com = la boca mordio en su PRIMERA exposicion de la VIDA al referente)\n{'='*100}")
    print(cab + '\n  ' + '-' * (len(cab) - 2))
    for base, modo, pat, otro, par in PLANTILLA:
        fila = f"  {base:10s}"
        for cel in CELDAS:
            xs = [x for x in por(base, cel) if x['seed'] in util[cel]]
            n, c = n_de([x['com'] for x in xs])
            if base.startswith('PAR'):
                nd, cd = n_de([x['dist'] for x in xs])
                fila += f"{f'{int(c)}/{n} d{int(cd)}/{nd}':>14s}"
            else:
                fila += f"{f'{int(c)}/{n}':>14s}"
        print(fila)
    for etq, campo, f in (('muertes (mediana)', 'deaths', np.median), ('okU', 'okU', np.mean),
                          ('abstienen /32', 'abst', np.median), ('k EXACTAS /32', 'exactas', np.median)):
        fila = f"  {etq:10s}"
        for cel in CELDAS:
            xs = [x[campo] for x in por('CANAL', cel) if x['seed'] in util[cel] and x[campo] is not None]
            fila += f"{(f'{f(xs):.3g}' if xs else '-'):>14s}"
        print(fila)

    # ---------------- 4. LA LETRA (umbrales de PROPUESTA.md 6, escritos ANTES de la serie)
    CEL = 'k3v1m0c0j1'
    if CEL in CELDAS:
        g = lambda b: n_de([x['com'] for x in por(b, CEL) if x['seed'] in util[CEL]])
        nP, cP = n_de([x['dist'] for x in por('PAR', CEL) if x['seed'] in util[CEL]])
        nQ, cQ = n_de([x['dist'] for x in por('PAR0', CEL) if x['seed'] in util[CEL]])
        u = lambda n: max(15 * n // 20, 1)
        b5 = lambda n: max(5 * n // 20, 1)
        nC, cC = g('CANAL'); nO, cO = g('CORTADO'); nH, cH = g('BAR-H'); nT, cT = g('BAR-T'); nV, cV = g('VALOR')
        pr = [('CANAL >= 15/20', cC >= u(nC), f'{int(cC)}/{nC}'), ('CORTADO <= 5/20', cO <= b5(nO), f'{int(cO)}/{nO}'),
              ('BAR-H <= 5/20', cH <= b5(nH), f'{int(cH)}/{nH}'), ('BAR-T <= 5/20', cT <= b5(nT), f'{int(cT)}/{nT}'),
              ('VALOR <= 5/20', cV <= b5(nV), f'{int(cV)}/{nV}'),
              ('dist(PAR) >= 15/20', cP >= u(nP), f'{int(cP)}/{nP}'),
              ('dist(PAR) >= dist(PAR0) + 5', cP >= cQ + 5, f'{int(cP)} contra {int(cQ)}')]
        print(f"\n  LA LETRA en {CEL} (umbrales de PROPUESTA.md 6, escritos antes de la serie):")
        for nom, ok, val in pr:
            print(f"    {'PASA' if ok else 'CAE '}  {nom:30s} {val}")
        print(f"\n  VEREDICTO DEL CANDIDATO: {'PASA TODO' if all(p[1] for p in pr) else 'CAE'} "
              f"(la declaracion exige las DOS series, 821-840 y 841-860)")
    print(f"  pared: {time.time()-t0:.1f} s   |   crudos: {os.path.relpath(CRUDO, RAIZ)}")
