"""Arnes de identidad del instrumento del BLOQUE 5 (organismo_familias_b5.py = organismo_familias_b4b +
`k_ganadoras`). Regla 2 y regla 14 de registro/EQUIPO.md.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy: que el mensaje
baje de la familia a la variante (H-4 de la sala 4; E-7, el techo de 2 bits).

  APAGADO (k_ganadoras=1): == organismo_familias_b4b en TODAS sus claves, en mundo='AB', en el mundo de familias,
                       con el canal apagado y con el canal encendido en sus tres modos, con `voraz` y con
                       `par_herm` encendidos.
  RNG NO CONSUMIDO   : lo mismo a T = 120000.
  CADENA COMPLETA    : apagado == organismo_familias_b4, == b3, == b2, == organismo_familias, == organismo_v14
                       (TRONCO) y, con el relevo ON en 6 px, == organismo_v15f_on.
  INERCIA            : con memoria_pares=None la perilla NO existe (no hay tabla que leer) para NINGUN k.
  ESTRUCTURA         : la 1.a de las k ganadoras ES la ganadora de b4b; con k = _NP se leen todas las celdas;
                       la lista no repite celdas y esta ordenada por error propio.
  LA ESCRITURA NO SE TOCA: con el MISMO prefijo de conducta, la tabla escrita es la misma para cualquier k.
  CONTROLES QUE DEBEN FALLAR: sin ellos el arnes pasaria por vacuidad.

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/nivel12_mundo_familias/identidad_familias_b5.py
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

T = 20000
T_LARGO = 120000
T_CANAL = 60000
SEM = (1, 2, 3)
SEM_R = 100000
VORAZ = 1.0          # el valor FIJADO en el preregistro del bloque 4b 3.2; el bloque 5 NO lo toca
KS = (3, 5)          # los brazos del bloque 5 por encima del control de Occam (k = 1)
NP = 66              # C(12,2): el numero de celdas de la tabla con la retina del mundo de familias
SHAS = {'organismo_v14.py (TRONCO CONGELADO)': (os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), 'feefc88b1fd8d434'),
        'organismo_v15f_on.py': (os.path.join(CREA, 'organismo_v15f_on.py'), '54d6efe0b564113c'),
        'organismo_familias.py (bloque 1)': (os.path.join(AQUI, 'organismo_familias.py'), 'b9dd561a0cf056b8'),
        'organismo_familias_b2.py (bloque 2)': (os.path.join(AQUI, 'organismo_familias_b2.py'), '30200bea6a41c3c8'),
        'organismo_familias_b3.py (bloque 3)': (os.path.join(AQUI, 'organismo_familias_b3.py'), '62a1e53b452b078e'),
        'organismo_familias_b4.py (bloque 4)': (os.path.join(AQUI, 'organismo_familias_b4.py'), 'ff9946ee2ffe27e6'),
        'organismo_familias_b4b.py (bloque 4b)': (os.path.join(AQUI, 'organismo_familias_b4b.py'), 'b3dd1d7e66a2d147'),
        'construye_familias_b5.py': (os.path.join(AQUI, 'construye_familias_b5.py'), None),
        'organismo_familias_b5.py': (os.path.join(AQUI, 'organismo_familias_b5.py'), None)}

FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)
SAL = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=0, n_neu=0, costo=0.008,
           deriva=5000, cambio=T_CANAL // 2, log_cada=250)
MUNDO = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=2, n_neu=0, costo=0.008, log_cada=250,
             crit_exp=0.5, cambio=10**9, vira=0, fam_val='familia', exc_fija=2, memoria_pares='relevo', reg_b2=1)
KW_E = dict(MUNDO, deriva=5000)
KW_R = dict(MUNDO, deriva=T_CANAL // 3 + 1, reg_b4=1)
XPOS, XNEG = 'T0v2', 'T1v2'
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
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    est = marca if ok == len(semillas) else ('FALLA' + detalle if puerta else 'NO DIFIERE' + detalle)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:70s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None and puerta:
        tot[0] += ok; tot[1] += len(semillas)
    return ok


def uno(etiq, ok, t0, tot):
    print(f"  [{time.time()-t0:6.1f}s] {etiq:70s} {'1/1 IDENTICO' if ok else '0/1 FALLA'}", flush=True)
    tot[0] += int(ok); tot[1] += 1
    return ok


def lanza(etiq, f, t0, tot):
    try:
        f(); ok = False
    except (ValueError, TypeError, IndexError):
        ok = True
    except Exception:
        ok = False
    print(f"  [{time.time()-t0:6.1f}s] {etiq:70s} {'1/1 LANZA (como debe)' if ok else '0/1 NO LANZA'}", flush=True)
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


def mensaje(s, Tc=T_CANAL, ref=XNEG, voraz=VORAZ):
    """El EMISOR del bloque 5 es b5 con k_ganadoras=1, o sea b4b bit a bit (lo comprueba el caso (i)/(l))."""
    e = (B5.run(s, T=Tc, fam_seed=s, canal={'modo': 'emite'}, voraz=voraz, k_ganadoras=1,
                **KW_E)['canal_emitido'] or {}).get(ref)
    return None if e is None else dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))


def receptor(s, msg, modo='sen', k=1, Tc=T_CANAL, P=None, par_herm=None, fam_seed=None):
    c = dict(modo=modo, t=msg['t'], ref=msg['ref'], P=(msg['P'] if P is None else P), R=msg['R'])
    return B5.run(s + SEM_R, T=Tc, fam_seed=(s if fam_seed is None else fam_seed), canal=c,
                  par_herm=par_herm, k_ganadoras=k, **KW_R)


if __name__ == '__main__':
    t0 = time.time()
    malo = False
    for nom, (p, esp) in SHAS.items():
        s = h16(p)
        aviso = '' if esp is None else ('  OK' if s == esp else f'  *** ESPERADO {esp}')
        malo = malo or (esp is not None and s != esp)
        print(f"  sha {nom:42s} {s}{aviso}")
    if malo:
        raise SystemExit("Un origen cambio. Reconstruir por anclas antes de seguir.")
    print(f"  T = {T} (ancla del rng: {T_LARGO}; canal: T = {T_CANAL}), semillas {SEM}, k del bloque = (1,)+{KS}, "
          f"UN proceso\n")

    tot = [0, 0]
    m0 = {s: mensaje(s) for s in SEM[:2]}

    print("APAGADO (k_ganadoras=1): organismo_familias_b5 == organismo_familias_b4b")
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
        caso(etiq, (lambda x: lambda s: B4B.run(s, T=T, **x))(kw),
             (lambda x: lambda s: B5.run(s, T=T, k_ganadoras=1, **x))(kw), t0, tot=tot, salta=NUEVAS_B5)
    print("  ...y con el CANAL ENCENDIDO en sus tres modos (el canal NO se toca en el bloque 5)")
    for etiq, modo in [('(n) canal sen', 'sen'), ('(o) canal inm', 'inm'), ('(p) canal mudo', 'mudo')]:
        caso(etiq, (lambda mo: lambda s: B4B.run(s + SEM_R, T=T_CANAL, fam_seed=s, canal=dict(
                 modo=mo, t=m0[s]['t'], ref=m0[s]['ref'], P=m0[s]['P'], R=m0[s]['R']), **KW_R))(modo),
             (lambda mo: lambda s: B5.run(s + SEM_R, T=T_CANAL, fam_seed=s, canal=dict(
                 modo=mo, t=m0[s]['t'], ref=m0[s]['ref'], P=m0[s]['P'], R=m0[s]['R']), k_ganadoras=1,
                 **KW_R))(modo),
             t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_B5)

    print("\nRNG NO CONSUMIDO por la perilla apagada (ancla larga)")
    caso(f'(q) mundo=AB a T = {T_LARGO}, relevo ENCENDIDO', lambda s: B4B.run(s, T=T_LARGO, memoria_pares='relevo'),
         lambda s: B5.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=1), t0, semillas=SEM[:2], tot=tot,
         salta=NUEVAS_B5)

    print("\nCADENA COMPLETA (se comprueba hasta el TRONCO, no se supone)")
    KW_B3 = {k: v for k, v in KW_R.items() if k not in ('exc_fija', 'reg_b4')}
    caso('(r) apagado == organismo_familias_b4 (mundo del bloque 4)',
         lambda s: B4.run(s, T=T, **KW_B3), lambda s: B5.run(s, T=T, **KW_B3),
         t0, tot=tot, salta=NUEVAS_B5 + NUEVAS_B4B + ('exc_fija',))
    caso('(s) apagado == organismo_familias_b3 (mundo del bloque 4)',
         lambda s: B3.run(s, T=T, **KW_B3), lambda s: B5.run(s, T=T, **KW_B3),
         t0, tot=tot, salta=NUEVAS_B5 + NUEVAS_B4B + CLAVES_B4)
    caso('(t) apagado + mundo=AB == organismo_v14 (TRONCO)', lambda s: V14.run(s, T=T),
         lambda s: B5.run(s, T=T), t0, tot=tot, salta=NUEVAS_B5 + NUEVAS_B4B)
    caso('(u) relevo ON + mundo=AB == organismo_v15f_on', lambda s: V15FON.run(s, T=T),
         lambda s: B5.run(s, T=T, memoria_pares='relevo'), t0, tot=tot, salta=NUEVAS_B5 + NUEVAS_B4B)
    caso('(v) apagado + mundo=familias == organismo_familias (bloque 1)', lambda s: MF.run(s, T=T, **FAM),
         lambda s: B5.run(s, T=T, **FAM), t0, tot=tot, salta=NUEVAS_B5 + NUEVAS_B4B)
    caso('(w) apagado + escenario S == organismo_familias_b2 (bloque 2)',
         lambda s: B2.run(s, T=T, reg_b2=1, vira=8, **SAL), lambda s: B5.run(s, T=T, reg_b2=1, vira=8, **SAL),
         t0, tot=tot, salta=NUEVAS_B5 + NUEVAS_B4B + CLAVES_B4 + CLAVES_B3)

    print("\nINERCIA: con memoria_pares=None NO hay tabla que leer -> `k_ganadoras` no existe")
    for k in KS:
        caso(f'(x{k}) memoria_pares=None: k={k} == k=1 (mundo=AB)', lambda s: B5.run(s, T=T, k_ganadoras=1),
             (lambda kk: lambda s: B5.run(s, T=T, k_ganadoras=kk))(k), t0, tot=tot, salta=('k_ganadoras',))
        caso(f'(y{k}) memoria_pares=None: k={k} == k=1 (mundo de familias)',
             lambda s: B5.run(s, T=T, k_ganadoras=1, **FAM),
             (lambda kk: lambda s: B5.run(s, T=T, k_ganadoras=kk, **FAM))(k), t0, tot=tot, salta=('k_ganadoras',))

    print("\nESTRUCTURA de la lista de ganadoras (la 1.a es la de b4b; sin repetir; ordenada por error propio)")
    ok1 = ok0 = okn = okd = oko = True
    for s in SEM:
        r1 = B5.run(s, T=T, k_ganadoras=1, **dict(KW_R, fam_seed=s))
        ok1 &= (r1['mem_ganadoras'] == [r1['mem_ganadora']] and r1['k_ganadoras'] == 1)
        for k in KS:
            rk = B5.run(s, T=T, k_ganadoras=k, **dict(KW_R, fam_seed=s))
            okn &= (len(rk['mem_ganadoras']) == k and rk['k_ganadoras'] == k)
            okd &= (len({tuple(g) for g in rk['mem_ganadoras']}) == k)
            ok0 &= (rk['mem_ganadoras'][0] == rk['mem_ganadora'])
        rT = B5.run(s, T=T, k_ganadoras=NP + 40, **dict(KW_R, fam_seed=s))
        oko &= (len(rT['mem_ganadoras']) == NP and len({tuple(g) for g in rT['mem_ganadoras']}) == NP)
    uno('(z) con k=1 `mem_ganadoras` es exactamente [mem_ganadora]', ok1, t0, tot)
    uno('(A) la PRIMERA de las k es SIEMPRE la ganadora de b4b (`mem_ganadora`)', ok0, t0, tot)
    uno(f'(B) `mem_ganadoras` tiene longitud k y no repite celdas (k in {KS})', okn and okd, t0, tot)
    uno(f'(C) con k > _NP se leen LAS {NP} celdas y ninguna mas', oko, t0, tot)
    okl = True
    for s in SEM[:2]:
        r = B5.run(s, T=T, k_ganadoras=5, **dict(KW_R, fam_seed=s))
        okl &= (r['mem_ganadoras'][0] == r['mem_ganadora'])
    uno('(D) ...tambien con el mundo del receptor a k = 5', okl, t0, tot)

    print("\nLA ESCRITURA NO SE TOCA: misma conducta -> misma tabla (learn=False, T corto)")
    okw = True
    for s in SEM:
        a = B5.run(s, T=2000, learn=False, k_ganadoras=1, **dict(KW_R, fam_seed=s))
        b = B5.run(s, T=2000, learn=False, k_ganadoras=5, **dict(KW_R, fam_seed=s))
        okw &= (N(a['mord']) != N(b['mord'])) or (N(a['mem_tabla']) == N(b['mem_tabla']))
    uno('(E) si la conducta no cambia, la tabla escrita es la misma para cualquier k', okw, t0, tot)
    lanza('(F) k_ganadoras=0 lanza', lambda: B5.run(1, T=100, k_ganadoras=0), t0, tot)
    lanza('(G) k_ganadoras=-1 lanza', lambda: B5.run(1, T=100, k_ganadoras=-1), t0, tot)
    lanza('(H) k_ganadoras=2.5 lanza', lambda: B5.run(1, T=100, k_ganadoras=2.5), t0, tot)
    lanza("(I) k_ganadoras='3' lanza", lambda: B5.run(1, T=100, k_ganadoras='3'), t0, tot)
    lanza('(J) k_ganadoras=True lanza (un bool no es una k)', lambda: B5.run(1, T=100, k_ganadoras=True), t0, tot)

    print(f"\nEL MONTAJE E -> R DEL BLOQUE 5 (emisor b4b/voraz={VORAZ}, receptor con k; T = {T_CANAL})")
    mv = {s: mensaje(s) for s in SEM[:2]}
    uno('(K) el emisor (k=1) anota la excepcion CIEGA T1v2 con R > 0 en las 2 semillas',
        all(v is not None and v['R'] > 0 and v['ref'] == XNEG for v in mv.values()), t0, tot)
    uno('(L) el mensaje es el MISMO objeto que en b4b (el emisor no cambia en el bloque 5)',
        all(mv[s] == dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))
            for s in SEM[:2]
            for e in [(B4B.run(s, T=T_CANAL, fam_seed=s, canal={'modo': 'emite'}, voraz=VORAZ,
                               **KW_E)['canal_emitido'] or {})[XNEG]]), t0, tot)
    uno('(M) ...y su patron es el del catalogo del bloque 0',
        all(mv[s]['P'] == PATS(s)[XNEG] for s in SEM[:2]), t0, tot)
    pre = lambda r, tc: hashlib.sha256(json.dumps([f for f in r['log'] if f[0] < tc]).encode()).hexdigest()[:16]
    okg = oke = okv = True
    for k in (1,) + KS:
        for s in SEM[:2]:
            rc = receptor(s, mv[s], 'sen', k=k); cc = receptor(s, mv[s], 'mudo', k=k)
            okg &= (pre(rc, rc['canal_t_entrega']) == pre(cc, rc['canal_t_entrega']))
            oke &= (rc['primera_b2'][XNEG][0] == rc['canal_t_entrega'])
            okv &= (len(rc['canal_gan_k_post']) == k and len(rc['canal_gan_k_pre']) == k
                    and rc['canal_gan_k_pre'][0] == rc['canal_gan_pre'])
    uno('(N) PUERTA P-I3 por k: CANAL- y CORTADO- comparten el prefijo EXACTO hasta la entrega', okg, t0, tot)
    uno('(O) PUERTA P-I4 por k: el receptor NUNCA habia visto el referente (1.a exposicion = la entrega)',
        oke, t0, tot)
    uno('(P) el diagnostico por k sale con longitud k y empieza por la ganadora de b4b', okv, t0, tot)
    uno('(Q) el receptor NO ve al emisor: mismo (t, ref, P, R) sin pasar por E -> identico',
        all(compara(receptor(s, mv[s], 'sen', k=5),
                    receptor(s, dict(t=mv[s]['t'], ref=XNEG, P=PATS(s)[XNEG], R=mv[s]['R']), 'sen', k=5)) == []
            for s in SEM[:2]), t0, tot)
    uno('(R) con k=1 el montaje entero es el de b4b (CANAL- clave a clave)',
        all(compara(B4B.run(s + SEM_R, T=T_CANAL, fam_seed=s,
                            canal=dict(modo='sen', t=mv[s]['t'], ref=XNEG, P=mv[s]['P'], R=mv[s]['R']), **KW_R),
                    receptor(s, mv[s], 'sen', k=1), salta=NUEVAS_B5) == [] for s in SEM[:2]), t0, tot)

    print("\nCONTROLES QUE DEBEN FALLAR (sin ellos el arnes pasaria por vacuidad)")
    for k in KS:
        caso(f'(S{k}) k={k} con el relevo ON cambia la corrida (DEBE diferir)',
             lambda s: B5.run(s, T=T, k_ganadoras=1, **dict(KW_R, fam_seed=s)),
             (lambda kk: lambda s: B5.run(s, T=T, k_ganadoras=kk, **dict(KW_R, fam_seed=s)))(k),
             t0, debe_diferir=True, tot=tot, salta=('k_ganadoras',))
    caso('(T) CANAL- != CORTADO- con k = 5 (DEBE diferir)', lambda s: receptor(s, mv[s], 'mudo', k=5),
         lambda s: receptor(s, mv[s], 'sen', k=5), t0, debe_diferir=True, semillas=SEM[:2], tot=tot,
         salta=('canal',))
    caso('(U) BARAJADO por otro token != CANAL con k = 5 (DEBE diferir)',
         lambda s: receptor(s, mv[s], 'sen', k=5),
         lambda s: receptor(s, mv[s], 'sen', k=5, P=PATS(s)['T3v2']), t0, debe_diferir=True, semillas=SEM[:2],
         tot=tot, salta=('canal',))

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el paquete puede correr." if tot[0] == tot[1] else
                                              "  -> NO se corre nada hasta que sea 100%."))

    print("\nDIAGNOSTICO (NO es puerta): a que reduce k la casilla del mensaje")
    for s in SEM[:2]:
        for k in (1,) + KS:
            r = receptor(s, mv[s], 'sen', k=k)
            print(f"  semilla {s} k={k}: ganadoras {r['canal_gan_k_post']}  comparten LAS k casillas "
                  f"{len(r['canal_mismo_bin_k'])}/32  (con 1 casilla: {len(r['canal_mismo_bin'])}/32)  "
                  f"1.a exposicion mordio {((r['primera_b4'] or {}).get(XNEG) or [[None]*5])[0][4]}")

    sys.exit(0 if tot[0] == tot[1] else 1)
