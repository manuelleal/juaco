"""Arnes de identidad del instrumento del CREADOR B de la junta de la fase 5
(organismo_familias_jb.py = organismo_familias_b6 + `mem_marginal`, el RELEVO MARGINAL en la LECTURA).

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy: que el
mensaje refiera a la FAMILIA **Y** a la VARIANTE con la MISMA tabla.

  APAGADO (mem_marginal=0) : == organismo_familias_b6 en TODAS sus claves, con el sufijo ON y OFF, para k = 1 y
                       k = 3, en mundo='AB', en el mundo de familias, con el canal apagado y con el canal en sus
                       tres modos, y a T = 120000 (el rng NO se consume).
  INERTE (memoria_variante=0): mem_marginal 1 y 2 == mem_marginal 0. LA CONFIGURACION QUE NO USA EL MECANISMO
                       ES BIT A BIT LA DEL BLOQUE 6 (y por su cadena, b5, b4b, b4, b3, b2, organismo_familias,
                       organismo_v14 TRONCO y organismo_v15f_on).
  INERCIA            : con memoria_pares=None no hay tabla que leer -> la perilla no existe.
  CADENA             : apagado + mundo=AB == organismo_v14 (TRONCO); relevo ON == organismo_v15f_on;
                       apagado == b5 (mv=0) y == b4b (mv=0, k=1).
  ESTRUCTURA         : la marginal REIMPLEMENTADA FUERA del organismo (de `mem_tabla`, `mem_visitas`,
                       `mem_ganadoras` y `mem_dir`) == la de dentro (`W_tabla`), estimulo a estimulo; y con el
                       relevo la via lenta NO ABSTIENE cuando alguna celda tiene visitas.
  EL MECANISMO HACE LO QUE DICE: con el sufijo ON, el relevo QUITA la abstencion (cobertura efectiva 32/32) sin
                       meter a la HERMANA en la direccion del referente. Si esto no se cumple no hay nada que
                       medir y se para aqui.
  CONTROLES QUE DEBEN FALLAR: sin ellos el arnes pasaria por vacuidad (ERR-64b: >= 2 de 3 semillas).

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/junta_fase5/B/identidad_familias_jb.py
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]

import numpy as np
import organismo_v14 as V14
import organismo_v15f_on as V15FON
import organismo_familias_b4b as B4B
import organismo_familias_b5 as B5
import organismo_familias_b6 as B6
import organismo_familias_jb as JB
import identidad_familias_b6 as ID6          # ERR-31: se IMPORTAN sus objetos y sus helpers, no se recopian

T = 20000
T_LARGO = 120000
T_CANAL = ID6.T_CANAL
SEM = ID6.SEM
SEM_R = ID6.SEM_R
VORAZ = ID6.VORAZ
KS = ID6.KS
NP, NVAR, SLOTS_ON = ID6.NP, ID6.NVAR, ID6.SLOTS_ON
FAM, SAL, MUNDO, KW_E, KW_R = ID6.FAM, ID6.SAL, ID6.MUNDO, ID6.KW_E, ID6.KW_R
XPOS, XNEG, HERM, OTRO_TK = ID6.XPOS, ID6.XNEG, ID6.HERM, ID6.OTRO_TK
PATS, dir_fuera = ID6.PATS, ID6.dir_fuera
caso, uno, lanza, compara, h16 = ID6.caso, ID6.uno, ID6.lanza, ID6.compara, ID6.h16
NUEVAS_JB = ('mem_marginal', 'mem_canales', 'mem_kvar', 'mem_conj', 'mem_can', 'mem_celdas_can',
             'mem_via', 'mem_visitas', 'mem_dir', 'canal_lee_post')
NUEVAS_B6 = ID6.NUEVAS_B6
NUEVAS_B5 = ID6.NUEVAS_B5
NUEVAS_B4B = ID6.NUEVAS_B4B
SHAS = {'organismo_v14.py (TRONCO CONGELADO)': (os.path.join(RAIZ, 'organismo', 'organismo_v14.py'),
                                                'feefc88b1fd8d434'),
        'organismo_familias_b5.py (bloque 5)': (os.path.join(N12, 'organismo_familias_b5.py'),
                                                'e0b6b90f6f92d5c1'),
        'organismo_familias_b6.py (bloque 6, ORIGEN)': (os.path.join(N12, 'organismo_familias_b6.py'),
                                                        'b10cbd4ddd0c32a3'),
        'construye_familias_jb.py': (os.path.join(AQUI, 'construye_familias_jb.py'), None),
        'organismo_familias_jb.py': (os.path.join(AQUI, 'organismo_familias_jb.py'), None)}
MMS = (1, 2, 3)   # los modos del relevo: ponderado por visitas / sin ponderar / la MODA del bin


def mensaje(s, Tc=T_CANAL, ref=XNEG, voraz=VORAZ):
    """El EMISOR de la junta corre con mem_marginal=0, memoria_variante=0 y k=1: es b4b BIT A BIT (caso (R))."""
    e = (JB.run(s, T=Tc, fam_seed=s, canal={'modo': 'emite'}, voraz=voraz, k_ganadoras=1, memoria_variante=0,
                mem_marginal=0, **KW_E)['canal_emitido'] or {}).get(ref)
    return None if e is None else dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))


def receptor(s, msg, modo='sen', k=3, mv=1, mm=1, Tc=T_CANAL, P=None, par_herm=None):
    c = dict(modo=modo, t=msg['t'], ref=msg['ref'], P=(msg['P'] if P is None else P), R=msg['R'])
    return JB.run(s + SEM_R, T=Tc, fam_seed=s, canal=c, par_herm=par_herm, k_ganadoras=k,
                  memoria_variante=mv, mem_marginal=mm, **KW_R)


def lee_fuera(r, nombre, nvar=NVAR, mm=None):
    """La lectura de la via lenta REIMPLEMENTADA FUERA del organismo, de sus propias claves de salida.
    Devuelve (valor, visto) igual que `_tabla_v15f`: exacta si la subcasilla se conoce, si no la MARGINAL del
    bin (ponderada por visitas con mem_marginal=1, sin ponderar con 2), y abstencion si el bin esta vacio.
    Con `mm` se fuerza OTRA regla de lectura sobre LA MISMA tabla (asi se comparan las reglas sin confundirlas
    con las trayectorias, que divergen en cuanto la conducta cambia)."""
    M = np.asarray(r['mem_tabla'], float); Nv = np.asarray(r['mem_visitas'], float)
    mm = (r['mem_marginal'] if mm is None else mm)
    mv, NV = r['memoria_variante'], (nvar if r['memoria_variante'] else 0)
    pares = [(i, j) for i in range(12) for j in range(i + 1, 12)]
    gan = [pares.index(tuple(g)) for g in r['mem_ganadoras']]
    dirs = r['mem_dir'][nombre]
    s, n = 0.0, 0
    for g, c in zip(gan, dirs):
        if Nv[g, c] > 0:
            s += float(M[g, c]); n += 1; continue
        if not mm or not mv:
            continue
        b = c >> NV; lo = b << NV; hi = lo + (1 << NV)
        w = Nv[g, lo:hi]; m = M[g, lo:hi]
        if mm == 2:
            k = w > 0
            if k.any():
                s += float(m[k].mean()); n += 1
        elif mm == 3:
            a = int(w.argmax())
            if w[a] > 0:
                s += float(m[a]); n += 1
        elif float(w.sum()) > 0:
            s += float((m * w).sum() / float(w.sum())); n += 1
    return (s, True) if n else (0.0, False)


if __name__ == '__main__':
    t0 = time.time()
    malo = False
    for nom, (p, esp) in SHAS.items():
        s = h16(p)
        aviso = '' if esp is None else ('  OK' if s == esp else f'  *** ESPERADO {esp}')
        malo = malo or (esp is not None and s != esp)
        print(f"  sha {nom:44s} {s}{aviso}")
    if malo:
        raise SystemExit("Un origen cambio. Reconstruir por anclas antes de seguir.")
    print(f"  T = {T} (ancla del rng: {T_LARGO}; canal: {T_CANAL}), semillas {SEM}, k = {KS}, "
          f"mem_marginal = {MMS}, UN proceso\n")

    tot = [0, 0]
    m0 = {s: mensaje(s) for s in SEM}
    SEM_MSG = tuple(s for s in SEM if m0[s] is not None)
    print(f"  emisores con mensaje (-): {len(SEM_MSG)}/{len(SEM)} -> {SEM_MSG}\n")

    print("APAGADO (mem_marginal=0): organismo_familias_jb == organismo_familias_b6, con el sufijo ON y OFF")
    for etiq, kw in [('(a) mundo=AB base', dict()),
                     ('(b) mundo=AB, relevo de pares ENCENDIDO (v15f)', dict(memoria_pares='relevo')),
                     ('(c) mundo=familias (bloque 1)', dict(FAM)),
                     ('(d) escenario S del bloque 2/3 (vira=8, relevo)', dict(SAL, vira=8, reg_b2=1,
                                                                              memoria_pares='relevo')),
                     ('(e) el mundo del bloque 4, EMISOR', dict(KW_E, fam_seed=1)),
                     ('(f) el mundo del bloque 4, RECEPTOR', dict(KW_R, fam_seed=1)),
                     ('(g) el emisor VORAZ del bloque 4b anotando', dict(KW_E, fam_seed=1, voraz=VORAZ,
                                                                         canal={'modo': 'emite'}))]:
        for k in KS:
            for mv in (0, 1):
                caso(f'{etiq}  [k={k}, sufijo={mv}]',
                     (lambda x, kk, m: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=m, **x))(kw, k, mv),
                     (lambda x, kk, m: lambda s: JB.run(s, T=T, k_ganadoras=kk, memoria_variante=m,
                                                        mem_marginal=0, **x))(kw, k, mv),
                     t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_JB)
    print("  ...y con el CANAL ENCENDIDO en sus tres modos (el canal NO se toca)")
    for etiq, modo in [('(h) canal sen', 'sen'), ('(i) canal inm', 'inm'), ('(j) canal mudo', 'mudo')]:
        for mv in (0, 1):
            caso(f'{etiq}, k = 3, sufijo={mv}',
                 (lambda mo, m: lambda s: B6.run(s + SEM_R, T=T_CANAL, fam_seed=s, k_ganadoras=3,
                     memoria_variante=m, canal=dict(modo=mo, t=m0[s]['t'], ref=m0[s]['ref'], P=m0[s]['P'],
                                                    R=m0[s]['R']), **KW_R))(modo, mv),
                 (lambda mo, m: lambda s: JB.run(s + SEM_R, T=T_CANAL, fam_seed=s, k_ganadoras=3,
                     memoria_variante=m, mem_marginal=0, canal=dict(modo=mo, t=m0[s]['t'], ref=m0[s]['ref'],
                                                                    P=m0[s]['P'], R=m0[s]['R']),
                     **KW_R))(modo, mv), t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_JB)
    print("\nRNG NO CONSUMIDO por la perilla apagada (ancla larga)")
    for k in KS:
        caso(f'(k{k}) mundo=AB a T = {T_LARGO}, relevo ON, sufijo ON, k = {k}',
             (lambda kk: lambda s: B6.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=kk,
                                          memoria_variante=1))(k),
             (lambda kk: lambda s: JB.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=kk,
                                          memoria_variante=1, mem_marginal=0))(k),
             t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_JB)

    print("\nINERTE CON EL SUFIJO APAGADO: memoria_variante=0 -> mem_marginal NO PUEDE HACER NADA")
    print("  (la marginal de un bin de UNA subcasilla es esa misma subcasilla: la configuracion que no usa mi")
    print("   mecanismo es BIT A BIT la del bloque 6, y por su cadena la del bloque 5 y la del TRONCO)")
    for mm in MMS:
        for k in KS:
            caso(f'(l{k}m{mm}) mv=0, k={k}, mem_marginal={mm} == b6 (el mundo del RECEPTOR, con canal sen)',
                 (lambda kk: lambda s: B6.run(s + SEM_R, T=T_CANAL, fam_seed=s, k_ganadoras=kk,
                     memoria_variante=0, canal=dict(modo='sen', t=m0[s]['t'], ref=m0[s]['ref'], P=m0[s]['P'],
                                                    R=m0[s]['R']), **KW_R))(k),
                 (lambda kk, mmm: lambda s: JB.run(s + SEM_R, T=T_CANAL, fam_seed=s, k_ganadoras=kk,
                     memoria_variante=0, mem_marginal=mmm, canal=dict(modo='sen', t=m0[s]['t'], ref=m0[s]['ref'],
                                                                      P=m0[s]['P'], R=m0[s]['R']),
                     **KW_R))(k, mm), t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_JB)
            caso(f'(m{k}m{mm}) mv=0, k={k}, mem_marginal={mm} == b6 (mundo de familias, sin canal)',
                 (lambda kk: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=0, **FAM))(k),
                 (lambda kk, mmm: lambda s: JB.run(s, T=T, k_ganadoras=kk, memoria_variante=0,
                                                   mem_marginal=mmm, **FAM))(k, mm),
                 t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_JB)

    print("\nINERTE CON k = 1: con UNA sola ganadora, la CONJUNCION y la DISYUNCION son la misma regla")
    for mv in (0, 1):
        caso(f'(j{mv}) k=1, mem_conj=1 == mem_conj=0 (sufijo={mv}, el mundo del RECEPTOR)',
             (lambda m: lambda s: JB.run(s, T=T, k_ganadoras=1, memoria_variante=m,
                                         **dict(KW_R, fam_seed=s)))(mv),
             (lambda m: lambda s: JB.run(s, T=T, k_ganadoras=1, memoria_variante=m, mem_conj=1,
                                         **dict(KW_R, fam_seed=s)))(mv),
             t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_JB)

    print("\nINERCIA: con memoria_pares=None no hay tabla que leer")
    for mm in MMS:
        caso(f'(n{mm}) memoria_pares=None: mem_marginal={mm} == 0 (mundo de familias, k = 3, sufijo ON)',
             lambda s: JB.run(s, T=T, k_ganadoras=3, memoria_variante=1, mem_marginal=0, **FAM),
             (lambda mmm: lambda s: JB.run(s, T=T, k_ganadoras=3, memoria_variante=1, mem_marginal=mmm,
                                           **FAM))(mm), t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_JB)

    print("\nCADENA (se comprueba hasta el TRONCO, no se supone)")
    caso('(o) apagado + mundo=AB == organismo_v14 (TRONCO CONGELADO)', lambda s: V14.run(s, T=T),
         lambda s: JB.run(s, T=T), t0, semillas=SEM[:2], tot=tot,
         salta=NUEVAS_JB + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso('(p) relevo ON + mundo=AB == organismo_v15f_on', lambda s: V15FON.run(s, T=T),
         lambda s: JB.run(s, T=T, memoria_pares='relevo'), t0, semillas=SEM[:2], tot=tot,
         salta=NUEVAS_JB + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    for mm in (0,) + MMS:
        caso(f'(q{mm}) sufijo OFF + mem_marginal={mm} == organismo_familias_b5 (el mundo del RECEPTOR, k = 3)',
             lambda s: B5.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
             (lambda mmm: lambda s: JB.run(s, T=T, k_ganadoras=3, memoria_variante=0, mem_marginal=mmm,
                                           **dict(KW_R, fam_seed=s)))(mm),
             t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_JB + NUEVAS_B6)
    caso('(r) sufijo OFF + k=1 == organismo_familias_b4b (el mundo del bloque 4, emisor voraz)',
         lambda s: B4B.run(s, T=T, voraz=VORAZ, **dict(KW_E, fam_seed=s)),
         lambda s: JB.run(s, T=T, voraz=VORAZ, mem_marginal=1, **dict(KW_E, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_JB + NUEVAS_B6 + NUEVAS_B5)

    print("\nPERILLA MAL ESCRITA (no cae en silencio)")
    lanza('(s) mem_marginal=4 lanza', lambda: JB.run(1, T=100, mem_marginal=4), t0, tot)
    lanza('(t) mem_marginal=-1 lanza', lambda: JB.run(1, T=100, mem_marginal=-1), t0, tot)
    lanza('(u) mem_marginal=0.5 lanza', lambda: JB.run(1, T=100, mem_marginal=0.5), t0, tot)
    lanza("(v) mem_marginal='1' lanza", lambda: JB.run(1, T=100, mem_marginal='1'), t0, tot)
    lanza('(w) mem_marginal=True lanza (un bool no es una perilla)',
          lambda: JB.run(1, T=100, mem_marginal=True), t0, tot)
    lanza('(w2) mem_canales=3 lanza', lambda: JB.run(1, T=100, mem_canales=3), t0, tot)
    lanza('(w3) mem_conj=2 lanza', lambda: JB.run(1, T=100, mem_conj=2), t0, tot)
    lanza('(w4) mem_kvar=0 lanza', lambda: JB.run(1, T=100, mem_kvar=0), t0, tot)
    lanza('(w5) mem_canales=1 con fam_nvar=0 lanza (un canal vacio)',
          lambda: JB.run(1, T=200, mem_canales=1, **dict(FAM, fam_nvar=0)), t0, tot)

    print("\nESTRUCTURA: la marginal REIMPLEMENTADA FUERA del organismo == la de dentro")
    okF = okA = okD = True
    abst = []
    for s in SEM:
        for mm in (0,) + MMS:
            r = JB.run(s, T=T, k_ganadoras=3, memoria_variante=1, mem_marginal=mm, **dict(KW_R, fam_seed=s))
            Q = PATS(s)
            for n in r['W_tabla']:
                v, vis = lee_fuera(r, n)
                okF &= ((r['W_tabla'][n] is None) == (not vis)) and (vis is False or
                                                                     abs(r['W_tabla'][n] - round(v, 3)) < 5e-4)
                # la DIRECCION exportada es la de `_dir_var`, reimplementada fuera
                okD &= (r['mem_dir'][n] == [dir_fuera(tuple(g), Q[n], 1) for g in r['mem_ganadoras']])
            if mm == 0:
                # LA MISMA TABLA leida con las tres reglas: el que abstiene con relevo abstiene tambien sin el.
                # (Comparar dos CORRIDAS no valdria: en cuanto la conducta cambia, las trayectorias divergen.)
                a = {x: {n for n in r['W_tabla'] if not lee_fuera(r, n, mm=x)[1]} for x in (0, 1, 2, 3)}
                okA &= all(a[x] <= a[0] for x in (1, 2, 3)) and a[1] == a[2] == a[3]
                abst.append((s, len(a[0]), len(a[1])))
    uno('(x) lectura de dentro (`W_tabla`) == lectura reimplementada FUERA, estimulo a estimulo', okF, t0, tot)
    uno('(y) la DIRECCION exportada == la reimplementada fuera (funcion solo de la retina presente)', okD, t0, tot)
    uno('(z) sobre LA MISMA tabla, quien abstiene con relevo abstiene tambien sin el (el relevo solo QUITA '
        'abstencion)', okA, t0, tot)
    print(f"        abstenciones sobre la misma tabla (semilla, b6 -> relevo, de 32): "
          + '  '.join(f'{s}: {a}->{b}' for s, a, b in abst))

    print("\nEL MECANISMO HACE LO QUE DICE (estructural; no es conducta)")
    okH = okT = okC = True
    det = []
    for s in SEM_MSG:
        for mm in (0,) + MMS:
            r = receptor(s, m0[s], 'sen', k=3, mv=1, mm=mm)
            d = r['canal_mismo_dir_k']
            if d is None:
                okC = False; continue
            okH &= (HERM not in d)     # el relevo NO mete a la hermana en la direccion del mensaje
            okT &= (XNEG in d)
            ex = sum(1 for n in r['mem_via'] if r['mem_via'][n][0] == 3)
            det.append((s, mm, len(d), ex, sum(1 for v in r['W_tabla'].values() if v is None)))
    uno('(A) con el relevo la HERMANA sigue FUERA de la direccion del mensaje (el sufijo no se diluye)',
        okH, t0, tot)
    uno('(B) el referente sigue SIEMPRE en su propia direccion (escritura y lectura coinciden)', okT, t0, tot)
    uno('(C) el diagnostico por direccion existe en las semillas que emiten', okC, t0, tot)
    print('        (s, mem_marginal, grupo por DIRECCION /32, estimulos con las 3 celdas EXACTAS /32, '
          'estimulos que ABSTIENEN /32): ' + '  '.join(str(x) for x in det))

    print("\nCONTROLES QUE DEBEN FALLAR (sin ellos el arnes pasaria por vacuidad; ERR-64b: >= 2 de 3)")
    for mm in MMS:
        caso(f'(D{mm}) con el sufijo ON, mem_marginal={mm} CAMBIA la corrida, k = 3 (DEBE diferir)',
             lambda s: JB.run(s, T=T, k_ganadoras=3, memoria_variante=1, mem_marginal=0,
                              **dict(KW_R, fam_seed=s)),
             (lambda mmm: lambda s: JB.run(s, T=T, k_ganadoras=3, memoria_variante=1, mem_marginal=mmm,
                                           **dict(KW_R, fam_seed=s)))(mm),
             t0, debe_diferir=True, tot=tot, salta=NUEVAS_JB)
    for cn in (1, 2):
        caso(f'(D-c{cn}) mem_canales={cn} CAMBIA la corrida, k = 3 (DEBE diferir)',
             lambda s: JB.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s)),
             (lambda c: lambda s: JB.run(s, T=T, k_ganadoras=3, memoria_variante=1, mem_canales=c,
                                         **dict(KW_R, fam_seed=s)))(cn),
             t0, debe_diferir=True, tot=tot, salta=NUEVAS_JB)
    caso('(D-j) mem_conj=1 CAMBIA la corrida con el sufijo ON, k = 3 (DEBE diferir)',
         lambda s: JB.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s)),
         lambda s: JB.run(s, T=T, k_ganadoras=3, memoria_variante=1, mem_conj=1,
                          **dict(KW_R, fam_seed=s)),
         t0, debe_diferir=True, tot=tot, salta=NUEVAS_JB)
    caso('(E) CANAL != CORTADO con sufijo ON y relevo ON, k = 3 (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'mudo', k=3, mv=1, mm=1),
         lambda s: receptor(s, m0[s], 'sen', k=3, mv=1, mm=1),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',) + NUEVAS_JB)
    caso('(F) el patron de la HERMANA != CANAL, relevo ON, k = 3 (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'sen', k=3, mv=1, mm=1),
         lambda s: receptor(s, m0[s], 'sen', k=3, mv=1, mm=1, P=PATS(s)[HERM]),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',) + NUEVAS_JB)
    caso('(G) el patron de OTRO TOKEN != CANAL, relevo ON, k = 3 (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'sen', k=3, mv=1, mm=1),
         lambda s: receptor(s, m0[s], 'sen', k=3, mv=1, mm=1, P=PATS(s)[OTRO_TK]),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',) + NUEVAS_JB)

    print("\nEL MONTAJE E -> R (ERR-71: la direccion se comprueba SIN pasar por el emisor)")
    pre = lambda r, tc: hashlib.sha256(json.dumps([f for f in r['log'] if f[0] < tc]).encode()).hexdigest()[:16]
    okg = oke = True
    for mm in (0,) + MMS:
        for s in SEM_MSG:
            rc = receptor(s, m0[s], 'sen', k=3, mv=1, mm=mm); cc = receptor(s, m0[s], 'mudo', k=3, mv=1, mm=mm)
            okg &= (pre(rc, rc['canal_t_entrega']) == pre(cc, rc['canal_t_entrega']))
            oke &= (rc['primera_b2'][XNEG][0] == rc['canal_t_entrega'])
    uno('(H) P-I3: CANAL y CORTADO comparten el prefijo EXACTO hasta la entrega, en los 3 modos', okg, t0, tot)
    uno('(I) P-I4: el receptor NUNCA habia visto el referente antes de la entrega, en los 3 modos', oke, t0, tot)
    uno('(J) el mensaje es el MISMO objeto que en b6 (el emisor no cambia)',
        all(m0[s] == ID6.mensaje(s) for s in SEM[:2]), t0, tot)
    uno('(K) el receptor NO ve al emisor: mismo (t, ref, P, R) sin pasar por E -> identico',
        all(compara(receptor(s, m0[s], 'sen', k=3, mv=1, mm=1),
                    receptor(s, dict(t=m0[s]['t'], ref=XNEG, P=PATS(s)[XNEG], R=m0[s]['R']), 'sen', k=3, mv=1,
                             mm=1)) == [] for s in SEM_MSG[:2]), t0, tot)

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el instrumento puede medir." if tot[0] == tot[1] else
                                              "  -> NO se mide nada hasta que sea 100%."))
    sys.exit(0 if tot[0] == tot[1] else 1)
