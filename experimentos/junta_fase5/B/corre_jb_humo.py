"""HUMO del creador B de la junta de la fase 5 -- las TRES REGLAS DE LECTURA (`mem_conj`, `mem_marginal`,
`mem_canales`) sobre el instrumento del bloque 6. NO ES EVIDENCIA: <= 3 semillas de 901-910 y T corto. La serie
confirmatoria (821-860) la corre el coordinador.

MISION (primero, siempre): llegar a la AGI por este camino. Hoy: que el mensaje refiera a la FAMILIA **Y** a la
VARIANTE con la MISMA tabla -- BAR-T <= 5/20 y PAR >= 15/20 a la vez, sin subir la base sin mensaje.

QUE MIDE: los brazos del bloque 6 (dir. (-) sola, ERR-53) en las CELDAS que se le pidan. Nombre de celda:
`k<K>v<MV>m<MM>c<CN>j<CJ>` = k_ganadoras, memoria_variante (sufijo), mem_marginal, mem_canales, mem_conj.
  k3v0m0c0j0 = organismo_familias_b5 con k = 3  BIT A BIT  (linea base de FAMILIA: BAR-T 5/20 y 4/18, PAR 12/20)
  k3v1m0c0j0 = organismo_familias_b6 con k = 3  BIT A BIT  (linea base de VARIANTE: PAR 15/20 y 15/18, BAR-T 11/20)
  k3v1m0c0j1 = EL CANDIDATO: sufijo + LECTURA CONJUNTIVA (las k celdas deben conocer su direccion)
  k3v0m0c0j1 = control: conjuncion SIN sufijo (demuestra que el sufijo sigue haciendo falta)
  k3v1m1c0j0 = control: relevo marginal (refutado en el humo; queda como consecuencia registrada)

REGLAS QUE CUMPLE (exoesqueleto y nave de MISION.md):
  - un proceso, sin Pool; semillas SOLO de 901-910 (nunca 821-860, que son de la confirmacion);
  - ERR-54: los CRUDOS se guardan ANTES del analisis (si el analisis se cae, los datos no se pierden);
  - ERR-70: P-I4 es criterio de EXCLUSION por semilla (no puerta todo-o-nada), y se reporta cuantas se excluyen;
  - P-I2: las semillas cuyo emisor no emite se excluyen y se reportan;
  - P-I3: CANAL y su gemelo (CORTADO / PAR0) comparten el prefijo EXACTO hasta la entrega -- se comprueba;
  - ERR-44: TODO se mide sobre la conducta de la boca (`primera_b2` / `primera_b4`), nunca sobre pesos;
  - ERR-31: se importan los OBJETOS del bloque 5/6 (mundo, canal, brazos, lectura), no se recopian;
  - ERR-28: organismo/ va PRIMERO en sys.path;
  - el EMISOR corre siempre con k=1 y las tres perillas en 0: es b4b BIT A BIT en todas las celdas (un solo
    emisor por semilla, compartido por todos los brazos: el mensaje es EL MISMO).

Ademas del `com` de cada brazo imprime `canal_lee_post`: QUE LEE la via lenta para el referente en el paso de la
ENTREGA y por que via (cuantas de las k contestan EXACTO). Eso es el MECANISMO, y es lo unico que un humo de 3
semillas puede decidir: los `com` a T = 30 000 NO reproducen las lineas base de las series.

Uso:  python experimentos/junta_fase5/B/corre_jb_humo.py [--T 30000] [--semillas 901,902,903]
                                                         [--celdas k3v1m0c0j1,k3v1m0c0j0]
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
import organismo_familias_jb as JB
import corre_familias_b5 as B5R                  # ERR-31: los OBJETOS del bloque 5 (mundo, canal, brazos, letra)
B4BR, B2R = B5R.B4BR, B5R.B2R
KW_E, KW_R = B5R.KW_E, B5R.KW_R
XNEG, BAR, PATS, prefijo, PAR_HERM = B5R.XNEG, B5R.BAR, B5R.PATS, B5R.prefijo, B5R.PAR_HERM
SEM_R, SEM_OTRO, VORAZ = B5R.SEM_R, B5R.SEM_OTRO, B5R.VORAZ
h16 = B5R.CF.h16

T_HUMO = 30000
SEMILLAS = [901, 902, 903]                       # SOLO 901-910 (nave, MISION.md)
CELDAS = ['k3v0m0c0j0', 'k3v1m0c0j0', 'k3v1m0c0j1', 'k3v0m0c0j1', 'k3v1m1c0j0']
PLANTILLA = [p for p in B5R.PLANTILLA if p[0] in ('CANAL', 'CORTADO', 'BAR-H', 'BAR-T', 'VALOR', 'PAR', 'PAR0')]
SHA_B6_ESPERADO = 'b10cbd4ddd0c32a3'
SHA_B5_ESPERADO = 'e0b6b90f6f92d5c1'
SHA_V14_ESPERADO = 'feefc88b1fd8d434'


def celda(nom):
    """'k3v1m1c0j1' -> (3, 1, 1, 0, 1) = (k_ganadoras, memoria_variante, mem_marginal, mem_canales, mem_conj)"""
    k, resto = nom[1:].split('v'); mv, resto = resto.split('m')
    mm, resto = (resto.split('c') if 'c' in resto else (resto, '0'))
    cn, cj = (resto.split('j') if 'j' in resto else (resto, '0'))
    return int(k), int(mv), int(mm), int(cn), int(cj)


def canal_de(base, pat, modo, msg, fam_seed_R, D=12):
    if pat == 'CEROS':
        P = [0.0] * D
    elif pat == 'REF':
        P = msg['P']
    else:
        P = PATS(msg['fam_seed'])[BAR['neg'][pat]]
    return dict(modo=modo, t=msg['t'], ref=msg['ref'], P=P, R=msg['R'])


def emisor(seed, Ti):
    """k=1, memoria_variante=0, mem_marginal=0 -> organismo_familias_b4b BIT A BIT. UN mensaje: la dir. (-)."""
    kw = B2R.resuelve(KW_E, Ti)
    r = JB.run(seed, T=Ti, fam_seed=seed, canal={'modo': 'emite'}, voraz=VORAZ, k_ganadoras=1,
               memoria_variante=0, mem_marginal=0, **kw)
    e = (r['canal_emitido'] or {}).get(XNEG)
    return (None if e is None else dict(t=int(e[0]), ref=e[1], P=[float(x) for x in e[2]], R=float(e[3]),
                                        enc=int(e[4]), fam_seed=seed, muertes=r['deaths']))


def corre(base, modo, pat, otro, par, cel, seed, msg, Ti):
    k, mv, mm, cn, cj = celda(cel)
    kw = B2R.resuelve(KW_R, Ti)
    fsr = seed + SEM_OTRO if otro else seed
    r = JB.run(seed + SEM_R, T=Ti, fam_seed=fsr, canal=canal_de(base, pat, modo, msg, fsr),
               par_herm=par, k_ganadoras=k, memoria_variante=mv, mem_marginal=mm, mem_canales=cn, mem_conj=cj, **kw)
    b4 = B4BR.lee_b4(r, msg['ref'])
    via = r.get('mem_via') or {}
    # QUE LEE LA VIA LENTA EN EL PASO DE LA ENTREGA (diagnostico del instrumento jb): [valor, conocido, k exactas, k]
    lp = r.get('canal_lee_post') or {}
    lref = lp.get(msg['ref']); lher = lp.get(BAR['neg']['H'])
    return dict(brazo=f'{base}-{cel}', base=base, cel=cel, k=k, mv=mv, mm=mm, cn=cn, cj=cj, seed=seed,
                can=(r.get('mem_can') or {}).get(msg['ref']), celdas_can=r.get('mem_celdas_can'),
                deaths=r['deaths'], celdas=r['celdas'], fam_seed=r['fam_seed'],
                entregado=r['canal_entregado'], t_entrega=r['canal_t_entrega'], t_msg=r['canal_t_msg'],
                prefijo=prefijo(r, r['canal_t_entrega'] if r['canal_t_entrega'] is not None else r['canal_t_msg']),
                # conducta de la boca (ERR-44): `com` = mordio en su PRIMERA exposicion de la VIDA al referente
                com=(None if b4['evX'] is None else 1 - b4['evX']), evX=b4['evX'], okX=b4['okX'],
                okU=b4['okU'], evU=b4['evU'], dist=b4['dist'], okP=b4['okP'], lag_par=b4['lag_par'],
                fam1=b4['fam1'], t_X=b4['t_X'], lag_t=b4['lag_t'], lag_m=b4['lag_m'],
                ret2=b4['ret2'], ret3=b4['ret3'], comH=b4['comH'], n_H=b4['n_H'],
                # mecanismo (diagnostico, no decide ninguna prediccion)
                lee_ref=lref, lee_herm=lher,
                cobertura=r.get('mem_cobertura'), vistas=r.get('mem_vistas'), slots=r.get('memoria_slots'),
                n_dir_k=(None if r.get('canal_mismo_dir_k') is None else len(r['canal_mismo_dir_k'])),
                n_bin_k=(None if r.get('canal_mismo_bin_k') is None else len(r['canal_mismo_bin_k'])),
                dir_k=r.get('canal_mismo_dir_k'), gan_k=r.get('canal_gan_k_post'),
                abst=(None if not r.get('W_tabla') else sum(1 for v in r['W_tabla'].values() if v is None)),
                exactas=(None if not via else sum(1 for n in via if via[n][0] == via[n][1])),
                wv=r.get('w_var_med'))


def n_de(xs):
    xs = [x for x in xs if x is not None]
    return (len(xs), sum(xs))


if __name__ == '__main__':
    arg = lambda n, d: (type(d)(sys.argv[sys.argv.index(n) + 1]) if n in sys.argv else d)
    Ti = arg('--T', T_HUMO)
    if '--semillas' in sys.argv:
        SEMILLAS = [int(x) for x in sys.argv[sys.argv.index('--semillas') + 1].split(',')]
    if '--celdas' in sys.argv:
        CELDAS = [c.strip() for c in sys.argv[sys.argv.index('--celdas') + 1].split(',') if c.strip()]
    if len(SEMILLAS) > 3 or not all(901 <= s <= 910 for s in SEMILLAS):
        raise SystemExit(f"NAVE: el humo usa <= 3 semillas de 901-910 (pedidas {SEMILLAS}). Abortado.")
    t0 = time.time()
    stamp = time.strftime('%Y%m%d_%H%M%S')
    CRUDO = os.path.join(AQUI, f'jb_humo_s{SEMILLAS[0]}-{SEMILLAS[-1]}_{stamp}_crudo.json')
    log = lambda m: print(f"  [{time.time()-t0:6.1f}s] {m}", flush=True)

    shas = dict(instrumento=h16(os.path.join(AQUI, 'organismo_familias_jb.py')),
                constructor=h16(os.path.join(AQUI, 'construye_familias_jb.py')),
                arnes=h16(os.path.join(AQUI, 'identidad_familias_jb.py')),
                runner=h16(os.path.abspath(__file__)),
                origen_b6=h16(os.path.join(N12, 'organismo_familias_b6.py')),
                origen_b5=h16(os.path.join(N12, 'organismo_familias_b5.py')),
                tronco_v14=h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py')))
    for nom, esp in (('origen_b6', SHA_B6_ESPERADO), ('origen_b5', SHA_B5_ESPERADO),
                     ('tronco_v14', SHA_V14_ESPERADO)):
        if shas[nom] != esp:
            raise SystemExit(f"ORIGEN {nom}: sha {shas[nom]}, se esperaba {esp}. Abortado.")
    print(f"HUMO creador B (REGLAS DE LECTURA: conjuncion / marginal / canales) -- NO ES EVIDENCIA. "
          f"T = {Ti}, semillas {SEMILLAS}, "
          f"celdas {CELDAS}, {len(PLANTILLA)} brazos, un proceso")
    for k, v in shas.items():
        print(f"  sha {k:14s} {v}")
    print()

    # -------------------------------------------------- 1. EMISORES (uno por semilla, compartido por las celdas)
    msgs = {}
    for s in SEMILLAS:
        msgs[s] = emisor(s, Ti)
        log(f"emisor semilla {s}: " + ('SIN MENSAJE (se excluye, P-I2)' if msgs[s] is None else
            f"ref {msgs[s]['ref']} R {msgs[s]['R']:+.1f} t {msgs[s]['t']} tras {msgs[s]['enc']} exposiciones"))
    SEM_MSG = [s for s in SEMILLAS if msgs[s] is not None]
    print(f"  P-I2: emisores con mensaje {len(SEM_MSG)}/{len(SEMILLAS)} -> {SEM_MSG}\n")
    if not SEM_MSG:
        raise SystemExit("Ningun emisor emitio: no hay nada que medir.")

    # -------------------------------------------------- 2. RECEPTORES (crudos ANTES del analisis, ERR-54)
    res = []
    for cel in CELDAS:
        for base, modo, pat, otro, par in PLANTILLA:
            for s in SEM_MSG:
                res.append(corre(base, modo, pat, otro, par, cel, s, msgs[s], Ti))
                with open(CRUDO, 'w', encoding='utf-8', newline='\n') as f:
                    json.dump(dict(shas=shas, T=Ti, semillas=SEMILLAS, celdas=CELDAS, msgs=msgs, res=res), f)
            r3 = [x for x in res if x['brazo'] == f'{base}-{cel}']
            log(f"{base:8s} {cel}: com {[x['com'] for x in r3]}  dist {[x['dist'] for x in r3]}  "
                f"muertes {[x['deaths'] for x in r3]}  abstienen {[x['abst'] for x in r3]}/32")
    print(f"\n  crudos en {os.path.relpath(CRUDO, RAIZ)}\n")

    # -------------------------------------------------- 3. ANALISIS (desde los crudos, ERR-54)
    G = {(x['brazo']): {x['seed']: x for x in res if x['brazo'] == x['brazo']} for x in res}
    por = lambda base, cel: [x for x in res if x['base'] == base and x['cel'] == cel]
    # P-I4 (ERR-70): semilla utilizable = la 1.a exposicion de la VIDA al referente es la entrega
    util = {}
    for cel in CELDAS:
        u = [s for s in SEM_MSG
             if all((x['t_X'] is not None and x['t_entrega'] is not None and x['t_X'] >= x['t_entrega'])
                    for x in res if x['cel'] == cel and x['seed'] == s and x['base'] in ('CANAL', 'CORTADO'))]
        util[cel] = u
    # P-I3: el prefijo de cada brazo `sen` contra su gemelo de la MISMA celda
    for cel in CELDAS:
        malos = []
        for base, modo, pat, otro, par in PLANTILLA:
            if modo != 'sen':
                continue
            g = 'PAR0' if base.startswith('PAR') else 'CORTADO'
            for s in SEM_MSG:
                a = [x for x in res if x['base'] == base and x['cel'] == cel and x['seed'] == s]
                b = [x for x in res if x['base'] == g and x['cel'] == cel and x['seed'] == s]
                if a and b and a[0]['prefijo'] != b[0]['prefijo']:
                    malos.append((base, s))
        print(f"  P-I3 {cel}: prefijo identico al gemelo hasta la entrega -> "
              f"{'OK' if not malos else 'CAE en ' + str(malos)}   |   P-I4 utilizables {len(util[cel])}"
              f"/{len(SEM_MSG)} -> {util[cel]}")

    print(f"\n{'='*112}\nBRAZOS (com = la boca mordio en su PRIMERA exposicion de la VIDA al referente, tras la "
          f"entrega; n = {len(SEM_MSG)})\n{'='*112}")
    cab = f"  {'brazo':10s}" + ''.join(f"{c:>18s}" for c in CELDAS)
    print(cab + '\n  ' + '-' * (len(cab) - 2))
    for base, modo, pat, otro, par in PLANTILLA:
        fila = f"  {base:10s}"
        for cel in CELDAS:
            xs = [x for x in por(base, cel) if x['seed'] in util[cel]]
            n, c = n_de([x['com'] for x in xs])
            if base.startswith('PAR'):
                nd, cd = n_de([x['dist'] for x in xs])
                fila += f"{f'{c}/{n} (dist {cd}/{nd})':>18s}"
            else:
                fila += f"{f'{c}/{n}':>18s}"
        print(fila)
    print()
    for etq, campo, f in (('muertes (mediana)', 'deaths', np.median), ('okU (control de valor)', 'okU', np.mean),
                          ('cobertura de la ganadora', 'cobertura', np.median),
                          ('estimulos que ABSTIENEN /32', 'abst', np.median),
                          ('estimulos con las k EXACTAS /32', 'exactas', np.median),
                          ('grupo por DIRECCION /32', 'n_dir_k', np.median),
                          ('grupo por BIN /32', 'n_bin_k', np.median)):
        fila = f"  {etq:32s}"
        for cel in CELDAS:
            xs = [x[campo] for x in por('CANAL', cel) if x['seed'] in util[cel] and x[campo] is not None]
            fila += f"{(f'{f(xs):.3g}' if xs else '-'):>18s}"
        print(fila)
    print(f"\n  (las filas de arriba son del brazo CANAL; `abstienen` y `exactas` son del FINAL de la corrida)")
    print(f"\n  QUE LEE LA VIA LENTA PARA EL REFERENTE EN EL PASO DE LA ENTREGA  [mediana del valor, celdas "
          f"EXACTAS de k]  -- el MECANISMO, no la conducta")
    for base, modo, pat, otro, par in PLANTILLA:
        fila = f"  {base:10s}"
        for cel in CELDAS:
            xs = [x['lee_ref'] for x in por(base, cel) if x['seed'] in util[cel] and x.get('lee_ref')]
            v = (f"{np.median([x[0] for x in xs]):+.2f} ex{int(np.median([x[2] for x in xs]))}/"
                 f"{int(np.median([x[3] for x in xs]))}" if xs else '-')
            fila += f"{v:>18s}"
        print(fila)
    print(f"  crudos: {os.path.relpath(CRUDO, RAIZ)}")
    print(f"  pared: {time.time()-t0:.1f} s")
