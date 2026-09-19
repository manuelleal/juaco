"""Arnes de identidad del instrumento del BLOQUE 6 (organismo_familias_b6.py = organismo_familias_b5 +
`memoria_variante`, el SUFIJO DE VARIANTE en la direccion de la tabla de pares). Reglas 2 y 14 de EQUIPO.md.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin
backprop) que aprende, desaprende, generaliza y se COMUNICA CON REFERENCIA. Hoy: que el mensaje distinga
"sal rosa" de "sal".

  APAGADO (memoria_variante=0): == organismo_familias_b5 en TODAS sus claves, para CUALQUIER `k_ganadoras`, en
                       mundo='AB', en el mundo de familias, con el canal apagado y con el canal encendido en sus
                       tres modos, con `voraz` y con `par_herm` encendidos.
  RNG NO CONSUMIDO   : lo mismo a T = 120000, con k = 1 y con k = 3.
  CADENA COMPLETA    : apagado == b5, == b4b, == b4, == b3, == b2, == organismo_familias, == organismo_v14
                       (TRONCO) y, con el relevo ON en 6 px, == organismo_v15f_on.
  INERCIA            : con memoria_pares=None la perilla NO existe (no hay tabla que direccionar).
  ESTRUCTURA         : 4 subcasillas apagada, 4*2^fam_nvar encendida; la direccion es una funcion SOLO de la
                       retina presente, reimplementada FUERA del organismo y comparada; el conjunto que comparte
                       DIRECCION es un subconjunto del que comparte BIN.
  EL MECANISMO HACE LO QUE DICE: con el sufijo encendido, la HERMANA deja de compartir la direccion del
                       referente (y sin el sufijo la comparte). Si esto no se cumple, el bloque 6 no tiene nada
                       que medir y se para aqui.
  CONTROLES QUE DEBEN FALLAR: sin ellos el arnes pasaria por vacuidad (ERR-64b: >= 2 de 3 semillas; los casos de
                       identidad siguen exigiendo 3/3).

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/nivel12_mundo_familias/identidad_familias_b6.py
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, CREA, CREB, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_v15f_on as V15FON
import organismo_familias as MF
import organismo_familias_b2 as B2
import organismo_familias_b3 as B3
import organismo_familias_b4 as B4
import organismo_familias_b4b as B4B
import organismo_familias_b5 as B5
import organismo_familias_b6 as B6

T = 20000
T_LARGO = 120000
T_CANAL = 60000
SEM = (1, 2, 3)
SEM_R = 100000
VORAZ = 1.0          # FIJADO en el preregistro del bloque 4b 3.2; los bloques 5 y 6 NO lo tocan
KS = (1, 3)          # B6: los dos brazos de lectura del bloque (k = 5 quedo descartado por coste en el bloque 5)
NP = 66              # C(12,2): celdas de la tabla con la retina del mundo de familias
NVAR = 3             # fam_nvar: los pixeles 9, 10 y 11
SLOTS_ON = 4 << NVAR  # 32 subcasillas por celda con el sufijo encendido
SHAS = {'organismo_v14.py (TRONCO CONGELADO)': (os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), 'feefc88b1fd8d434'),
        'organismo_v15f_on.py': (os.path.join(CREA, 'organismo_v15f_on.py'), '54d6efe0b564113c'),
        'organismo_familias.py (bloque 1)': (os.path.join(AQUI, 'organismo_familias.py'), 'b9dd561a0cf056b8'),
        'organismo_familias_b2.py (bloque 2)': (os.path.join(AQUI, 'organismo_familias_b2.py'), '30200bea6a41c3c8'),
        'organismo_familias_b3.py (bloque 3)': (os.path.join(AQUI, 'organismo_familias_b3.py'), '62a1e53b452b078e'),
        'organismo_familias_b4.py (bloque 4)': (os.path.join(AQUI, 'organismo_familias_b4.py'), 'ff9946ee2ffe27e6'),
        'organismo_familias_b4b.py (bloque 4b)': (os.path.join(AQUI, 'organismo_familias_b4b.py'), 'b3dd1d7e66a2d147'),
        'organismo_familias_b5.py (bloque 5)': (os.path.join(AQUI, 'organismo_familias_b5.py'), 'e0b6b90f6f92d5c1'),
        'construye_familias_b6.py': (os.path.join(AQUI, 'construye_familias_b6.py'), None),
        'organismo_familias_b6.py': (os.path.join(AQUI, 'organismo_familias_b6.py'), None)}

FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)
SAL = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=0, n_neu=0, costo=0.008,
           deriva=5000, cambio=T_CANAL // 2, log_cada=250)
MUNDO = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=2, n_neu=0, costo=0.008, log_cada=250,
             crit_exp=0.5, cambio=10**9, vira=0, fam_val='familia', exc_fija=2, memoria_pares='relevo', reg_b2=1)
KW_E = dict(MUNDO, deriva=5000)
KW_R = dict(MUNDO, deriva=T_CANAL // 3 + 1, reg_b4=1)
XPOS, XNEG = 'T0v2', 'T1v2'
HERM, OTRO_TK = 'T1v0', 'T3v2'        # la HERMANA del referente y el patron de OTRO token (los brazos BAR-H y BAR-T)
NUEVAS_B6 = ('memoria_variante', 'memoria_slots', 'memoria_nvar', 'canal_mismo_dir_k')
NUEVAS_B5 = ('k_ganadoras', 'mem_ganadoras', 'canal_gan_k_pre', 'canal_gan_k_post', 'canal_mismo_bin_k')
NUEVAS_B4B = ('voraz', 'par_herm', 'par_fijo')
CLAVES_B4 = ('canal', 'canal_modo', 'canal_t_msg', 'canal_entregado', 'canal_t_entrega', 'canal_emitido',
             'canal_gan_pre', 'canal_gan_post', 'canal_bin', 'canal_mismo_bin', 'primera_b4', 'fam_seed')
CLAVES_B3 = ('memoria_pares', 'mem_alfa', 'mem_ganadora', 'mem_tabla', 'mem_vistas', 'mem_cobertura',
             'mem_err_tabla', 'W_tabla', 'mem_fam', 'mem_ev')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def compara(a, b, salta=()):
    return [k for k in a if k not in salta and N(a[k]) != N(b.get(k))] + \
           [k for k in a if k not in b and k not in salta]


def caso(etiq, fa, fb, t0, debe_diferir=False, semillas=SEM, tot=None, puerta=True, salta=()):
    ok, detalle = 0, ''
    for s in semillas:
        dif = compara(fa(s), fb(s), salta)
        ok += int((not dif) != debe_diferir)
        if dif and not detalle:
            detalle = ' ' + str(dif[:5])
    # ERR-64b: los controles que DEBEN diferir prueban no-vacuidad con >= 2 de 3 (una semilla sin mensaje
    # entregado no es vacuidad); los casos de identidad siguen exigiendo 3/3.
    need = (len(semillas) - 1 if (debe_diferir and len(semillas) >= 3) else len(semillas))
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    est = marca if ok >= need else ('FALLA' + detalle if puerta else 'NO DIFIERE' + detalle)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:72s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None and puerta:
        tot[0] += int(ok >= need); tot[1] += 1
    return ok >= need


def uno(etiq, ok, t0, tot):
    print(f"  [{time.time()-t0:6.1f}s] {etiq:72s} {'1/1 OK' if ok else '0/1 FALLA'}", flush=True)
    tot[0] += int(bool(ok)); tot[1] += 1
    return bool(ok)


def lanza(etiq, f, t0, tot):
    try:
        f(); ok = False
    except (ValueError, TypeError, IndexError):
        ok = True
    except Exception:
        ok = False
    print(f"  [{time.time()-t0:6.1f}s] {etiq:72s} {'1/1 LANZA (como debe)' if ok else '0/1 NO LANZA'}", flush=True)
    tot[0] += int(ok); tot[1] += 1
    return ok


def PATS(fam_seed, D=12, F=8, V=3):
    import escala_codigo as EC
    P, fm, ev, rz, _ = EC.catalogo(D, F, V, fam_seed)
    out = {}
    for i in range(P.shape[0]):
        k = int(fm[i])
        out[('T%d' % k) if not bool(ev[i]) else ('T%dv%d' % (k, i - int(rz[i]) - 1))] = [float(x) for x in P[i]]
    return out


# ---- la direccion local REIMPLEMENTADA FUERA del organismo (para comprobar la de dentro, no para usarla)
def dir_fuera(par, P, mv, nvar=NVAR, D=12):
    b = int(P[par[0]]) * 2 + int(P[par[1]])
    if not mv:
        return b
    s = 0
    for q in range(D - nvar, D):
        s = s * 2 + int(P[q])
    return b * (1 << nvar) + s


def mensaje(s, Tc=T_CANAL, ref=XNEG, voraz=VORAZ):
    """El EMISOR del bloque 6 corre con memoria_variante=0 y k_ganadoras=1: es b4b BIT A BIT (casos (N) y (R))."""
    e = (B6.run(s, T=Tc, fam_seed=s, canal={'modo': 'emite'}, voraz=voraz, k_ganadoras=1, memoria_variante=0,
                **KW_E)['canal_emitido'] or {}).get(ref)
    return None if e is None else dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))


def receptor(s, msg, modo='sen', k=1, mv=0, Tc=T_CANAL, P=None, par_herm=None, fam_seed=None):
    c = dict(modo=modo, t=msg['t'], ref=msg['ref'], P=(msg['P'] if P is None else P), R=msg['R'])
    return B6.run(s + SEM_R, T=Tc, fam_seed=(s if fam_seed is None else fam_seed), canal=c,
                  par_herm=par_herm, k_ganadoras=k, memoria_variante=mv, **KW_R)


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
    print(f"  T = {T} (ancla del rng: {T_LARGO}; canal: T = {T_CANAL}), semillas {SEM}, k = {KS}, "
          f"sufijo de {NVAR} px -> {SLOTS_ON} subcasillas, UN proceso\n")

    tot = [0, 0]
    m0 = {s: mensaje(s) for s in SEM}
    SEM_MSG = tuple(s for s in SEM if m0[s] is not None)   # semillas cuyo emisor SI emitio (P-I2 del montaje)
    print(f"  emisores con mensaje (-): {len(SEM_MSG)}/{len(SEM)} -> {SEM_MSG}\n")

    print("APAGADO (memoria_variante=0): organismo_familias_b6 == organismo_familias_b5, para CUALQUIER k")
    for etiq, kw in [('(a) mundo=AB base', dict()),
                     ('(b) mundo=AB, inversion en T/2', dict(invertir_en=T // 2)),
                     ('(c) mundo=AB, sin puerta (las dos vias SUMAN, un solo error)', dict(puerta=None)),
                     ('(d) mundo=AB, linaje v13', dict(mask_rel=0, puerta_pat=0)),
                     ('(e) mundo=AB, B-5 encendido', dict(desambiguar=1)),
                     ('(f) mundo=AB, relevo ENCENDIDO (v15f)', dict(memoria_pares='relevo')),
                     ('(g) mundo=familias (bloque 1)', dict(FAM)),
                     ('(h) escenario S del bloque 2/3 (vira=8, relevo)', dict(SAL, vira=8, reg_b2=1,
                                                                              memoria_pares='relevo')),
                     ('(i) el mundo del bloque 4, EMISOR', dict(KW_E, fam_seed=1)),
                     ('(j) el mundo del bloque 4, RECEPTOR', dict(KW_R, fam_seed=1)),
                     ('(k) el mundo del bloque 4 con el emisor ANOTANDO', dict(KW_E, fam_seed=1,
                                                                               canal={'modo': 'emite'})),
                     ('(l) el emisor VORAZ del bloque 4b (voraz=1.0)', dict(KW_E, fam_seed=1, voraz=VORAZ)),
                     ('(m) el brazo PAR del bloque 4b (par_herm=(1,0))', dict(KW_R, fam_seed=1,
                                                                              par_herm=(1, 0)))]:
        caso(etiq, (lambda x: lambda s: B5.run(s, T=T, k_ganadoras=1, **x))(kw),
             (lambda x: lambda s: B6.run(s, T=T, k_ganadoras=1, memoria_variante=0, **x))(kw),
             t0, tot=tot, salta=NUEVAS_B6)
    for k in KS:
        caso(f'(n{k}) el mundo del RECEPTOR con k = {k} (la perilla de b5 encendida)',
             (lambda kk: lambda s: B5.run(s, T=T, k_ganadoras=kk, **dict(KW_R, fam_seed=s)))(k),
             (lambda kk: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=0,
                                          **dict(KW_R, fam_seed=s)))(k), t0, tot=tot, salta=NUEVAS_B6)
    caso('(o) el mundo del RECEPTOR con k = 5 (el brazo caro del bloque 5)',
         lambda s: B5.run(s, T=T, k_ganadoras=5, **dict(KW_R, fam_seed=s)),
         lambda s: B6.run(s, T=T, k_ganadoras=5, memoria_variante=0, **dict(KW_R, fam_seed=s)),
         t0, tot=tot, salta=NUEVAS_B6)
    print("  ...y con el CANAL ENCENDIDO en sus tres modos (el canal NO se toca en el bloque 6)")
    for etiq, modo in [('(p) canal sen, k = 3', 'sen'), ('(q) canal inm, k = 3', 'inm'),
                       ('(r) canal mudo, k = 3', 'mudo')]:
        caso(etiq, (lambda mo: lambda s: B5.run(s + SEM_R, T=T_CANAL, fam_seed=s, k_ganadoras=3, canal=dict(
                 modo=mo, t=m0[s]['t'], ref=m0[s]['ref'], P=m0[s]['P'], R=m0[s]['R']), **KW_R))(modo),
             (lambda mo: lambda s: B6.run(s + SEM_R, T=T_CANAL, fam_seed=s, k_ganadoras=3, memoria_variante=0,
                 canal=dict(modo=mo, t=m0[s]['t'], ref=m0[s]['ref'], P=m0[s]['P'], R=m0[s]['R']),
                 **KW_R))(modo), t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_B6)

    print("\nRNG NO CONSUMIDO por la perilla apagada (ancla larga)")
    for k in KS:
        caso(f'(s{k}) mundo=AB a T = {T_LARGO}, relevo ENCENDIDO, k = {k}',
             (lambda kk: lambda s: B5.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=kk))(k),
             (lambda kk: lambda s: B6.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=kk,
                                          memoria_variante=0))(k), t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_B6)

    print("\nCADENA COMPLETA (se comprueba hasta el TRONCO, no se supone)")
    KW_B3 = {k: v for k, v in KW_R.items() if k not in ('exc_fija', 'reg_b4')}
    caso('(t) apagado == organismo_familias_b4b (mundo del bloque 4, emisor voraz)',
         lambda s: B4B.run(s, T=T, voraz=VORAZ, **dict(KW_E, fam_seed=s)),
         lambda s: B6.run(s, T=T, voraz=VORAZ, **dict(KW_E, fam_seed=s)),
         t0, tot=tot, salta=NUEVAS_B6 + NUEVAS_B5)
    caso('(u) apagado == organismo_familias_b4 (mundo del bloque 4)',
         lambda s: B4.run(s, T=T, **KW_B3), lambda s: B6.run(s, T=T, **KW_B3),
         t0, tot=tot, salta=NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B + ('exc_fija',))
    caso('(v) apagado == organismo_familias_b3 (mundo del bloque 4)',
         lambda s: B3.run(s, T=T, **KW_B3), lambda s: B6.run(s, T=T, **KW_B3),
         t0, tot=tot, salta=NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B + CLAVES_B4)
    caso('(w) apagado + mundo=AB == organismo_v14 (TRONCO CONGELADO)', lambda s: V14.run(s, T=T),
         lambda s: B6.run(s, T=T), t0, tot=tot, salta=NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso('(x) relevo ON + mundo=AB == organismo_v15f_on', lambda s: V15FON.run(s, T=T),
         lambda s: B6.run(s, T=T, memoria_pares='relevo'), t0, tot=tot,
         salta=NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso('(y) apagado + mundo=familias == organismo_familias (bloque 1)', lambda s: MF.run(s, T=T, **FAM),
         lambda s: B6.run(s, T=T, **FAM), t0, tot=tot, salta=NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso('(z) apagado + escenario S == organismo_familias_b2 (bloque 2)',
         lambda s: B2.run(s, T=T, reg_b2=1, vira=8, **SAL), lambda s: B6.run(s, T=T, reg_b2=1, vira=8, **SAL),
         t0, tot=tot, salta=NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B + CLAVES_B4 + CLAVES_B3)

    print("\nINERCIA: con memoria_pares=None NO hay tabla que direccionar -> `memoria_variante` no existe")
    for k in KS:
        caso(f'(A{k}) memoria_pares=None: mv=1 == mv=0 (mundo=AB, k = {k})',
             (lambda kk: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=0))(k),
             (lambda kk: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=1))(k),
             t0, tot=tot, salta=NUEVAS_B6)
        caso(f'(B{k}) memoria_pares=None: mv=1 == mv=0 (mundo de familias, k = {k})',
             (lambda kk: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=0, **FAM))(k),
             (lambda kk: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=1, **FAM))(k),
             t0, tot=tot, salta=NUEVAS_B6)

    print("\nESTRUCTURA de la direccion (tamaño, y la funcion reimplementada FUERA del organismo)")
    okS = okD = okF = True
    for s in SEM:
        r0 = B6.run(s, T=T, k_ganadoras=3, memoria_variante=0, **dict(KW_R, fam_seed=s))
        r1 = B6.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s))
        okS &= (r0['memoria_slots'] == 4 and len(r0['mem_tabla'][0]) == 4 and r0['memoria_nvar'] == 0)
        okD &= (r1['memoria_slots'] == SLOTS_ON and len(r1['mem_tabla'][0]) == SLOTS_ON
                and r1['memoria_nvar'] == NVAR and len(r1['mem_tabla']) == NP)
        # la direccion es una funcion SOLO de la retina presente: se reimplementa FUERA y se compara contra el
        # diagnostico `canal_mismo_dir_k` (que el organismo calcula con SU `_dir_var`). Hace falta el canal
        # encendido, porque el diagnostico se toma en el paso de la entrega.
        Q = PATS(s); X = Q[XNEG]; msg = m0[s]
        if msg is None:
            continue
        for mv in (0, 1):
            r = receptor(s, msg, 'sen', k=3, mv=mv)
            gk = r['canal_gan_k_post']
            if gk is None or r['canal_mismo_dir_k'] is None:
                okF = False; continue
            esperado = sorted(n for n in Q if all(dir_fuera(g, Q[n], mv) == dir_fuera(g, X, mv) for g in gk))
            okF &= (r['canal_mismo_dir_k'] == esperado)
            if mv == 0:
                okF &= (r['canal_mismo_dir_k'] == r['canal_mismo_bin_k'])   # apagada: DIRECCION == BIN
    uno('(C) apagada: 4 subcasillas por celda y la tabla tiene 4 columnas', okS, t0, tot)
    uno(f'(D) encendida: {SLOTS_ON} subcasillas por celda, {NP} celdas, firma de {NVAR} px', okD, t0, tot)
    uno('(E) la direccion de dentro == la reimplementada FUERA (funcion solo de la retina presente)', okF, t0, tot)

    print("\nEL MECANISMO HACE LO QUE DICE (diagnostico estructural de la direccion, no conducta)")
    okH = okT = okSub = True
    det, herm_sin = [], [0, 0]
    for s in SEM:
        for k in KS:
            if m0[s] is None:
                continue
            r0 = receptor(s, m0[s], 'sen', k=k, mv=0)
            r1 = receptor(s, m0[s], 'sen', k=k, mv=1)
            d0, d1 = r0['canal_mismo_dir_k'], r1['canal_mismo_dir_k']
            b1 = r1['canal_mismo_bin_k']
            if d0 is None or d1 is None:
                continue
            okSub &= set(d1) <= set(b1)                 # la DIRECCION nunca agrupa mas que el BIN
            okH &= (HERM not in d1)                     # CON sufijo la hermana NO comparte direccion: es la PUERTA
            okT &= (XNEG in d1)                         # el referente sigue en su propia direccion
            herm_sin[0] += int(HERM in d0); herm_sin[1] += 1   # sin sufijo: DIAGNOSTICO, no puerta
            det.append((s, k, len(d0), len(d1)))
    uno('(F) el grupo por DIRECCION es subconjunto del grupo por BIN (el sufijo solo puede afinar)', okSub, t0, tot)
    uno('(G) CON sufijo la HERMANA NUNCA comparte la direccion del referente (la puerta del mecanismo)',
        okH, t0, tot)
    uno('(H) el referente esta SIEMPRE en su propia direccion (la escritura y la lectura coinciden)', okT, t0, tot)
    # DIAGNOSTICO (no es puerta): sin sufijo la hermana comparte la direccion CASI siempre, pero no siempre --
    # cuando el top-k incluye por azar una celda con pixel de variante (`gan_var`, 1/18 en el bloque 5), k sola ya
    # la separa en esa semilla. Se reporta para no leer BAR-H de k3v0 como si fuera puramente ciego a la variante.
    print(f"        SIN sufijo la hermana comparte la direccion en {herm_sin[0]}/{herm_sin[1]} celdas "
          f"(semilla x k)  |  " + '  '.join(f's{s}k{k}: {a}->{b} de 32' for s, k, a, b in det))

    print("\nPERILLA MAL ESCRITA (no cae en silencio)")
    lanza('(I) memoria_variante=2 lanza', lambda: B6.run(1, T=100, memoria_variante=2), t0, tot)
    lanza('(J) memoria_variante=-1 lanza', lambda: B6.run(1, T=100, memoria_variante=-1), t0, tot)
    lanza('(K) memoria_variante=0.5 lanza', lambda: B6.run(1, T=100, memoria_variante=0.5), t0, tot)
    lanza("(L) memoria_variante='1' lanza", lambda: B6.run(1, T=100, memoria_variante='1'), t0, tot)
    lanza('(M) memoria_variante=True lanza (un bool no es una perilla)',
          lambda: B6.run(1, T=100, memoria_variante=True), t0, tot)
    lanza('(N) memoria_variante=1 con fam_nvar=0 lanza (firma vacia)',
          lambda: B6.run(1, T=200, memoria_variante=1, **dict(FAM, fam_nvar=0)), t0, tot)
    lanza('(O) memoria_variante=1 con fam_nvar=12 lanza (la firma se come la retina)',
          lambda: B6.run(1, T=200, memoria_variante=1, **dict(FAM, fam_nvar=12)), t0, tot)

    print(f"\nEL MONTAJE E -> R DEL BLOQUE 6 (emisor mv=0/k=1/voraz={VORAZ}, receptor 2x2; T = {T_CANAL})")
    mv2 = m0   # el MISMO emisor; no se vuelve a correr
    # P-I2 del montaje, a escala del arnes: el emisor voraz avisa en >= 18/20 en la serie; aqui, >= 2 de 3
    # semillas (ERR-64b). Las semillas SIN mensaje se excluyen y se reportan, no tumban el arnes.
    uno(f'(P) el emisor anota la excepcion CIEGA T1v2 con R > 0 en >= 2 de {len(SEM)} semillas '
        f'(emiten {len(SEM_MSG)}: {SEM_MSG})',
        sum(1 for v in mv2.values() if v is not None and v['R'] > 0 and v['ref'] == XNEG) >= 2, t0, tot)
    uno('(Q) el mensaje es el MISMO objeto que en b5 (el emisor no cambia en el bloque 6)',
        all(mv2[s] == dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))
            for s in SEM[:2]
            for e in [(B5.run(s, T=T_CANAL, fam_seed=s, canal={'modo': 'emite'}, voraz=VORAZ, k_ganadoras=1,
                              **KW_E)['canal_emitido'] or {})[XNEG]]), t0, tot)
    uno('(R) ...y el MISMO que en b4b (la cadena del emisor llega al bloque 4b sin tocar)',
        all(mv2[s] == dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))
            for s in SEM[:2]
            for e in [(B4B.run(s, T=T_CANAL, fam_seed=s, canal={'modo': 'emite'}, voraz=VORAZ,
                               **KW_E)['canal_emitido'] or {})[XNEG]]), t0, tot)
    uno('(S) ...y su patron es el del catalogo del bloque 0', all(mv2[s]['P'] == PATS(s)[XNEG] for s in SEM[:2]),
        t0, tot)
    pre = lambda r, tc: hashlib.sha256(json.dumps([f for f in r['log'] if f[0] < tc]).encode()).hexdigest()[:16]
    okg = oke = okv = True
    for k in KS:
        for mv in (0, 1):
            for s in SEM[:2]:
                rc = receptor(s, mv2[s], 'sen', k=k, mv=mv); cc = receptor(s, mv2[s], 'mudo', k=k, mv=mv)
                okg &= (pre(rc, rc['canal_t_entrega']) == pre(cc, rc['canal_t_entrega']))
                oke &= (rc['primera_b2'][XNEG][0] == rc['canal_t_entrega'])
                okv &= (len(rc['canal_gan_k_post']) == k and rc['canal_gan_k_pre'][0] == rc['canal_gan_pre'])
    uno('(T) PUERTA P-I3 en las 4 celdas (k x sufijo): CANAL y CORTADO comparten el prefijo EXACTO', okg, t0, tot)
    uno('(U) PUERTA P-I4 en las 4 celdas: el receptor NUNCA habia visto el referente antes de la entrega',
        oke, t0, tot)
    uno('(V) el diagnostico por k sale con longitud k y empieza por la ganadora de b4b', okv, t0, tot)
    uno('(W) el receptor NO ve al emisor: mismo (t, ref, P, R) sin pasar por E -> identico',
        all(compara(receptor(s, mv2[s], 'sen', k=3, mv=1),
                    receptor(s, dict(t=mv2[s]['t'], ref=XNEG, P=PATS(s)[XNEG], R=mv2[s]['R']), 'sen', k=3,
                             mv=1)) == [] for s in SEM[:2]), t0, tot)
    uno('(X) con mv=0 el montaje entero es el del bloque 5 (CANAL, clave a clave, k = 3)',
        all(compara(B5.run(s + SEM_R, T=T_CANAL, fam_seed=s, k_ganadoras=3,
                           canal=dict(modo='sen', t=mv2[s]['t'], ref=XNEG, P=mv2[s]['P'], R=mv2[s]['R']), **KW_R),
                    receptor(s, mv2[s], 'sen', k=3, mv=0), salta=NUEVAS_B6) == [] for s in SEM[:2]), t0, tot)

    print("\nCONTROLES QUE DEBEN FALLAR (sin ellos el arnes pasaria por vacuidad; ERR-64b: >= 2 de 3)")
    for k in KS:
        caso(f'(Y{k}) mv=1 con el relevo ON cambia la corrida, k = {k} (DEBE diferir)',
             (lambda kk: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=0,
                                          **dict(KW_R, fam_seed=s)))(k),
             (lambda kk: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=1,
                                          **dict(KW_R, fam_seed=s)))(k),
             t0, debe_diferir=True, tot=tot, salta=NUEVAS_B6)
    caso('(Z) CANAL != CORTADO con mv=1, k = 3 (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'mudo', k=3, mv=1),
         lambda s: receptor(s, m0[s], 'sen', k=3, mv=1), t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',))
    caso('(AA) el patron de la HERMANA != CANAL con mv=1, k = 3 (DEBE diferir: es el brazo que decide)',
         lambda s: receptor(s, m0[s], 'sen', k=3, mv=1),
         lambda s: receptor(s, m0[s], 'sen', k=3, mv=1, P=PATS(s)[HERM]),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',))
    caso('(AB) el patron de OTRO TOKEN != CANAL con mv=1, k = 3 (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'sen', k=3, mv=1),
         lambda s: receptor(s, m0[s], 'sen', k=3, mv=1, P=PATS(s)[OTRO_TK]),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',))

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el paquete puede correr." if tot[0] == tot[1] else
                                              "  -> NO se corre nada hasta que sea 100%."))

    print("\nDIAGNOSTICO (NO es puerta): a que reduce el sufijo la direccion del mensaje")
    for s in SEM[:2]:
        for k in KS:
            for mv in (0, 1):
                r = receptor(s, mv2[s], 'sen', k=k, mv=mv)
                print(f"  semilla {s} k={k} sufijo={mv}: ganadoras {r['canal_gan_k_post']}  comparten LAS k "
                      f"DIRECCIONES {len(r['canal_mismo_dir_k'])}/32  (por BIN: {len(r['canal_mismo_bin_k'])}/32)"
                      f"  hermana dentro: {HERM in r['canal_mismo_dir_k']}  1.a exposicion mordio "
                      f"{((r['primera_b4'] or {}).get(XNEG) or [[None]*5])[0][4]}")

    sys.exit(0 if tot[0] == tot[1] else 1)
