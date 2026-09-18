"""Arnes de identidad del instrumento del BLOQUE 4b (organismo_familias_b4b.py = organismo_familias_b4 + `voraz`
+ `par_herm`). Regla 2 y regla 14 de registro/EQUIPO.md.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive, se reproduce y se COMUNICA. Hoy: que dos celulas se
comuniquen SOBRE ALGO QUE AMBAS REPRESENTAN -- y que la que habla pueda llegar a saberlo (ERR-51).

  APAGADO (voraz=0.0, par_herm=None): == organismo_familias_b4 en TODAS sus claves, en mundo='AB', en el mundo de
                       familias, con el canal apagado y con el canal encendido en sus tres modos.
  RNG NO CONSUMIDO   : lo mismo a T = 120000.
  CADENA COMPLETA    : apagado == organismo_familias_b3, == organismo_familias_b2, == organismo_familias,
                       == organismo_v14 (TRONCO) y, con el relevo ON en 6 px, == organismo_v15f_on.
  `voraz`            : solo puede mover la MORDIDA -- con learn=False, TODO lo que depende de los pesos (W, comp,
                       W_lenta, Wps, Wns, celdas, splits) es identico para cualquier voraz (`n_cod` no: cuenta
                       mordidas, no pesos).
  `par_herm`         : sustituye la presentacion SIN tocar el rng del mundo (val_mundo, exc_win, herm y cod0
                       identicos), la hermana sustituida NO deriva, y el token sustituido no vuelve a verse.
  EL CANAL NO SE TOCA: los cuatro casos del bloque 4 se revalidan a traves de b4b.
  CONTROLES QUE DEBEN FALLAR: sin ellos el arnes pasaria por vacuidad.

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/nivel12_mundo_familias/identidad_familias_b4b.py
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

T = 20000
T_LARGO = 120000
T_CANAL = 60000
SEM = (1, 2, 3)
SEM_R = 100000
VORAZ = 1.0          # el valor FIJADO en el preregistro 3.2, antes de la serie
SHAS = {'organismo_v14.py (TRONCO CONGELADO)': (os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), 'feefc88b1fd8d434'),
        'organismo_v15f_on.py': (os.path.join(CREA, 'organismo_v15f_on.py'), '54d6efe0b564113c'),
        'organismo_familias.py (bloque 1)': (os.path.join(AQUI, 'organismo_familias.py'), 'b9dd561a0cf056b8'),
        'organismo_familias_b2.py (bloque 2)': (os.path.join(AQUI, 'organismo_familias_b2.py'), '30200bea6a41c3c8'),
        'organismo_familias_b3.py (bloque 3)': (os.path.join(AQUI, 'organismo_familias_b3.py'), '62a1e53b452b078e'),
        'organismo_familias_b4.py (bloque 4)': (os.path.join(AQUI, 'organismo_familias_b4.py'), 'ff9946ee2ffe27e6'),
        'construye_familias_b4b.py': (os.path.join(AQUI, 'construye_familias_b4b.py'), None),
        'organismo_familias_b4b.py': (os.path.join(AQUI, 'organismo_familias_b4b.py'), None)}

FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)
SAL = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=0, n_neu=0, costo=0.008,
           deriva=5000, cambio=T_CANAL // 2, log_cada=250)
MUNDO = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=2, n_neu=0, costo=0.008, log_cada=250,
             crit_exp=0.5, cambio=10**9, vira=0, fam_val='familia', exc_fija=2, memoria_pares='relevo', reg_b2=1)
KW_E = dict(MUNDO, deriva=5000)
KW_R = dict(MUNDO, deriva=T_CANAL // 3 + 1, reg_b4=1)
XPOS, XNEG = 'T0v2', 'T1v2'
NUEVAS_B4B = {'voraz', 'par_herm', 'par_fijo'}
# Lo que SOLO depende de los pesos. `n_cod` NO entra: cuenta MORDIDAS del codigo exacto (se incrementa fuera de
# `if learn:`), asi que `voraz` lo mueve legitimamente -- lo comprobo el arnes al fallar esta misma linea.
PESOS = ('W', 'comp', 'W_lenta', 'Wps', 'Wns', 'celdas', 'splits', 'split_t')


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
    print(f"  [{time.time()-t0:6.1f}s] {etiq:66s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None and puerta:
        tot[0] += ok; tot[1] += len(semillas)
    return ok


def uno(etiq, ok, t0, tot):
    print(f"  [{time.time()-t0:6.1f}s] {etiq:66s} {'1/1 IDENTICO' if ok else '0/1 FALLA'}", flush=True)
    tot[0] += int(ok); tot[1] += 1
    return ok


def lanza(etiq, f, t0, tot):
    try:
        f(); ok = False
    except (ValueError, TypeError, IndexError):
        ok = True
    except Exception:
        ok = False
    print(f"  [{time.time()-t0:6.1f}s] {etiq:66s} {'1/1 LANZA (como debe)' if ok else '0/1 NO LANZA'}", flush=True)
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


def emisor(s, Tc=T_CANAL, voraz=VORAZ):
    return B4B.run(s, T=Tc, fam_seed=s, canal={'modo': 'emite'}, voraz=voraz, **KW_E)


def mensaje(s, Tc=T_CANAL, ref=XNEG, voraz=VORAZ):
    e = (emisor(s, Tc, voraz)['canal_emitido'] or {}).get(ref)
    return None if e is None else dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))


def receptor(s, msg, modo='sen', Tc=T_CANAL, P=None, par_herm=None, fam_seed=None):
    c = dict(modo=modo, t=msg['t'], ref=msg['ref'], P=(msg['P'] if P is None else P), R=msg['R'])
    return B4B.run(s + SEM_R, T=Tc, fam_seed=(s if fam_seed is None else fam_seed), canal=c,
                   par_herm=par_herm, **KW_R)


if __name__ == '__main__':
    t0 = time.time()
    malo = False
    for nom, (p, esp) in SHAS.items():
        s = h16(p)
        aviso = '' if esp is None else ('  OK' if s == esp else f'  *** ESPERADO {esp}')
        malo = malo or (esp is not None and s != esp)
        print(f"  sha {nom:40s} {s}{aviso}")
    if malo:
        raise SystemExit("Un origen cambio. Reconstruir por anclas antes de seguir.")
    print(f"  T = {T} (ancla del rng: {T_LARGO}; canal: T = {T_CANAL}), semillas {SEM}, voraz del bloque = {VORAZ}, "
          f"UN proceso\n")

    tot = [0, 0]
    m0 = {s: mensaje(s) for s in SEM[:2]}

    print("APAGADO (voraz=0.0, par_herm=None): organismo_familias_b4b == organismo_familias_b4")
    for etiq, kw in [('(a) mundo=AB base', dict()),
                     ('(b) mundo=AB, inversion en T/2', dict(invertir_en=T // 2)),
                     ('(c) mundo=AB, sin puerta', dict(puerta=None)),
                     ('(d) mundo=AB, linaje v13', dict(mask_rel=0, puerta_pat=0)),
                     ('(e) mundo=AB, B-5 encendido', dict(desambiguar=1)),
                     ('(f) mundo=AB, relevo ENCENDIDO (v15f)', dict(memoria_pares='relevo')),
                     ('(g) mundo=familias (bloque 1)', dict(FAM)),
                     ('(h) escenario S del bloque 2/3 (vira=8, relevo)', dict(SAL, vira=8, reg_b2=1,
                                                                              memoria_pares='relevo')),
                     ('(i) el mundo del bloque 4, EMISOR', dict(KW_E, fam_seed=1)),
                     ('(j) el mundo del bloque 4, RECEPTOR', dict(KW_R, fam_seed=1)),
                     ('(k) el mundo del bloque 4 con el emisor ANOTANDO', dict(KW_E, fam_seed=1,
                                                                               canal={'modo': 'emite'}))]:
        caso(etiq, (lambda x: lambda s: B4.run(s, T=T, **x))(kw),
             (lambda x: lambda s: B4B.run(s, T=T, voraz=0.0, par_herm=None, **x))(kw), t0, tot=tot,
             salta=tuple(NUEVAS_B4B))
    print("  ...y con el CANAL ENCENDIDO en sus tres modos (el canal NO se toca en 4b)")
    for etiq, modo in [('(l) canal sen', 'sen'), ('(m) canal inm', 'inm'), ('(n) canal mudo', 'mudo')]:
        caso(etiq, (lambda mo: lambda s: B4.run(s + SEM_R, T=T_CANAL, fam_seed=s, canal=dict(
                 modo=mo, t=m0[s]['t'], ref=m0[s]['ref'], P=m0[s]['P'], R=m0[s]['R']), **KW_R))(modo),
             (lambda mo: lambda s: B4B.run(s + SEM_R, T=T_CANAL, fam_seed=s, canal=dict(
                 modo=mo, t=m0[s]['t'], ref=m0[s]['ref'], P=m0[s]['P'], R=m0[s]['R']), voraz=0.0,
                 par_herm=None, **KW_R))(modo),
             t0, semillas=SEM[:2], tot=tot, salta=tuple(NUEVAS_B4B))

    print("\nRNG NO CONSUMIDO por las perillas apagadas (ancla larga)")
    caso(f'(o) mundo=AB a T = {T_LARGO}, relevo ENCENDIDO', lambda s: B4.run(s, T=T_LARGO, memoria_pares='relevo'),
         lambda s: B4B.run(s, T=T_LARGO, memoria_pares='relevo'), t0, semillas=SEM[:2], tot=tot,
         salta=tuple(NUEVAS_B4B))

    print("\nCADENA COMPLETA (se comprueba hasta el TRONCO, no se supone)")
    KW_B3 = {k: v for k, v in KW_R.items() if k not in ('exc_fija', 'reg_b4')}
    CLAVES_B4 = ('canal', 'canal_modo', 'canal_t_msg', 'canal_entregado', 'canal_t_entrega', 'canal_emitido',
                 'canal_gan_pre', 'canal_gan_post', 'canal_bin', 'canal_mismo_bin', 'primera_b4', 'fam_seed')
    caso('(p) apagado == organismo_familias_b3 (mundo del bloque 4)',
         lambda s: B3.run(s, T=T, **KW_B3), lambda s: B4B.run(s, T=T, **KW_B3),
         t0, tot=tot, salta=tuple(NUEVAS_B4B) + CLAVES_B4)
    caso('(q) apagado + mundo=AB == organismo_v14 (TRONCO)', lambda s: V14.run(s, T=T),
         lambda s: B4B.run(s, T=T), t0, tot=tot, salta=tuple(NUEVAS_B4B))
    caso('(r) relevo ON + mundo=AB == organismo_v15f_on', lambda s: V15FON.run(s, T=T),
         lambda s: B4B.run(s, T=T, memoria_pares='relevo'), t0, tot=tot, salta=tuple(NUEVAS_B4B))
    caso('(s) apagado + mundo=familias == organismo_familias (bloque 1)', lambda s: MF.run(s, T=T, **FAM),
         lambda s: B4B.run(s, T=T, **FAM), t0, tot=tot, salta=tuple(NUEVAS_B4B))
    caso('(t) apagado + escenario S == organismo_familias_b2 (bloque 2)',
         lambda s: B2.run(s, T=T, reg_b2=1, vira=8, **SAL), lambda s: B4B.run(s, T=T, reg_b2=1, vira=8, **SAL),
         t0, tot=tot, salta=tuple(NUEVAS_B4B) + CLAVES_B4 + ('memoria_pares', 'mem_alfa', 'mem_ganadora',
                                                 'mem_tabla', 'mem_vistas', 'mem_cobertura', 'mem_err_tabla',
                                                 'W_tabla', 'mem_fam', 'mem_ev'))

    print("\n`voraz`: SOLO puede mover la MORDIDA (es una constante del organo de la boca)")
    caso('(u) voraz=0.0 explicito == el defecto', lambda s: B4B.run(s, T=T, **KW_E),
         lambda s: B4B.run(s, T=T, voraz=0.0, **KW_E), t0, tot=tot)
    caso('(v) con learn=False, TODO lo que depende de los pesos es igual para cualquier voraz',
         lambda s: {k: B4B.run(s, T=4000, learn=False, voraz=0.0, **KW_E)[k] for k in PESOS},
         lambda s: {k: B4B.run(s, T=4000, learn=False, voraz=3.0, **KW_E)[k] for k in PESOS}, t0, tot=tot)
    ok_v = all(B4B.run(s, T=2000, voraz=2.5, **KW_E)['voraz'] == 2.5 for s in SEM)
    uno('(w) `voraz` sale en la salida con su valor', ok_v, t0, tot)

    print("\n`par_herm`: sustituye la PRESENTACION sin tocar el rng del mundo")
    caso('(x) par_herm=None explicito == el defecto', lambda s: B4B.run(s, T=T, **KW_R),
         lambda s: B4B.run(s, T=T, par_herm=None, **KW_R), t0, tot=tot)
    ok_m, ok_f, ok_d, ok_t = True, True, True, True
    for s in SEM:
        a = B4B.run(s, T=T, fam_seed=s, **KW_R)
        b = B4B.run(s, T=T, fam_seed=s, par_herm=(1, 0), **KW_R)
        ok_m &= all(N(a[k]) == N(b[k]) for k in ('val_mundo', 'exc_win', 'herm', 'exc', 'cod0'))
        ok_f &= (b['par_fijo'] == 'T1v0' and a['par_fijo'] is None and b['par_herm'] == [1, 0])
        ok_t &= (sum(b['vis']['T1']) == 0 and sum(a['vis']['T1']) > 0)
        ok_d &= (sum(b['vis']['T1v0']) > 0)
    uno('(y) el rng del MUNDO intacto (val_mundo/exc_win/herm/exc/cod0 identicos)', ok_m, t0, tot)
    uno("(z) `par_fijo` es 'T1v0' y sale en la salida", ok_f, t0, tot)
    uno('(A) el TOKEN sustituido NO vuelve a verse, y la hermana SI', ok_t and ok_d, t0, tot)
    ok_p = True
    for s in SEM[:2]:
        b = B4B.run(s, T=T_CANAL, fam_seed=s, par_herm=(1, 0), **KW_R)
        q = int(len(b['vis']['T1v0']) - 1)                       # ultimo cuarto: la fase de la variante 2
        ok_p &= (b['vis']['T1v0'][q] > 0 and b['vis'][XNEG][q] > 0)
    uno('(B) en la fase de la prueba conviven la hermana Y la excepcion (la hermana NO deriva)', ok_p, t0, tot)
    lanza("(C) par_herm mal escrito lanza", lambda: B4B.run(1, T=100, par_herm=5, **KW_R), t0, tot)

    print(f"\nEL MONTAJE E -> R CON EL EMISOR VORAZ (voraz = {VORAZ}, T = {T_CANAL})")
    mv = {s: mensaje(s, voraz=VORAZ) for s in SEM[:2]}
    uno(f'(D) el emisor VORAZ anota la excepcion CIEGA (T1v2, R > 0) en las 2 semillas',
        all(v is not None and v['R'] > 0 and v['ref'] == XNEG for v in mv.values()), t0, tot)
    uno('(E) ...y el patron del mensaje es el del catalogo del bloque 0',
        all(mv[s]['P'] == PATS(s)[XNEG] for s in SEM[:2]), t0, tot)
    uno('(F) el emisor con voraz=0 NO siempre llega (ERR-51: el motivo del bloque 4b)',
        any(mensaje(s, voraz=0.0) is None for s in SEM[:2]), t0, tot)
    rec = {s: receptor(s, mv[s], 'sen') for s in SEM[:2]}
    cor = {s: receptor(s, mv[s], 'mudo') for s in SEM[:2]}
    uno('(G) el receptor recibe por SENALAMIENTO en las 2 semillas',
        all(rec[s]['canal_entregado'] and rec[s]['canal_t_entrega'] is not None for s in SEM[:2]), t0, tot)
    uno('(H) el receptor NUNCA habia visto el referente (1.a exposicion = la entrega)',
        all(rec[s]['primera_b2'][XNEG][0] == rec[s]['canal_t_entrega'] for s in SEM[:2]), t0, tot)
    pre = lambda r, tc: hashlib.sha256(json.dumps([f for f in r['log'] if f[0] < tc]).encode()).hexdigest()[:16]
    uno('(I) PUERTA P-I3: CANAL- y CORTADO- comparten el prefijo EXACTO de `log` hasta la entrega',
        all(pre(rec[s], rec[s]['canal_t_entrega']) == pre(cor[s], rec[s]['canal_t_entrega']) for s in SEM[:2]),
        t0, tot)
    uno('(J) el receptor NO ve al emisor: mismo (t, ref, P, R) sin pasar por E -> identico',
        all(compara(rec[s], receptor(s, dict(t=mv[s]['t'], ref=XNEG, P=PATS(s)[XNEG], R=mv[s]['R']), 'sen')) == []
            for s in SEM[:2]), t0, tot)
    uno('(K) el brazo PAR y su gemelo comparten prefijo (el canal es lo unico que los separa)',
        all(pre(receptor(s, mv[s], 'sen', par_herm=(1, 0)), receptor(s, mv[s], 'sen', par_herm=(1, 0))
                ['canal_t_entrega']) ==
            pre(receptor(s, mv[s], 'mudo', par_herm=(1, 0)), receptor(s, mv[s], 'sen', par_herm=(1, 0))
                ['canal_t_entrega']) for s in SEM[:1]), t0, tot)

    print("\nCONTROLES QUE DEBEN FALLAR (sin ellos el arnes pasaria por vacuidad)")
    caso('(L) voraz != 0 cambia la corrida (DEBE diferir)', lambda s: B4B.run(s, T=T, voraz=0.0, **KW_E),
         lambda s: B4B.run(s, T=T, voraz=VORAZ, **KW_E), t0, debe_diferir=True, tot=tot, salta=('voraz',))
    caso('(M) par_herm != None cambia la corrida (DEBE diferir)', lambda s: B4B.run(s, T=T, **KW_R),
         lambda s: B4B.run(s, T=T, par_herm=(1, 0), **KW_R), t0, debe_diferir=True, tot=tot,
         salta=('par_herm', 'par_fijo'))
    caso('(N) CANAL- != CORTADO- con el emisor voraz (DEBE diferir)', lambda s: receptor(s, mv[s], 'mudo'),
         lambda s: receptor(s, mv[s], 'sen'), t0, debe_diferir=True, semillas=SEM[:2], tot=tot, salta=('canal',))
    caso("(O) entrega 'inm' != 'sen' (DEBE diferir)", lambda s: receptor(s, mv[s], 'inm'),
         lambda s: receptor(s, mv[s], 'sen'), t0, debe_diferir=True, semillas=SEM[:2], tot=tot, salta=('canal',))
    caso('(P) BARAJADO por hermana != CANAL (DEBE diferir)', lambda s: receptor(s, mv[s], 'sen'),
         lambda s: receptor(s, mv[s], 'sen', P=PATS(s)['T1v0']), t0, debe_diferir=True, semillas=SEM[:2],
         tot=tot, salta=('canal',))
    caso('(Q) VALOR-SOLO != CANAL (DEBE diferir)', lambda s: receptor(s, mv[s], 'sen'),
         lambda s: receptor(s, mv[s], 'sen', P=[0.0] * 12), t0, debe_diferir=True, semillas=SEM[:2], tot=tot,
         salta=('canal',))
    caso('(R) R-SIN-SAL != CANAL (DEBE diferir)', lambda s: receptor(s, mv[s], 'sen'),
         lambda s: receptor(s, mv[s], 'sen', fam_seed=s + 200000), t0, debe_diferir=True, semillas=SEM[:2],
         tot=tot, salta=('canal', 'fam_seed'))

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el paquete puede correr." if tot[0] == tot[1] else
                                              "  -> NO se corre nada hasta que sea 100%."))

    print("\nDIAGNOSTICO (NO es puerta): el emisor voraz y el brazo PAR")
    for s in SEM[:2]:
        e0, ev = emisor(s, T_CANAL, 0.0), emisor(s, T_CANAL, VORAZ)
        f = lambda r: sum(sum(c) for k, c in r['mord'].items() if r['val_mundo'][k] == 'veneno')
        print(f"  semilla {s}: voraz 0.0 -> emite {sorted(e0['canal_emitido'] or {})}, muertes {e0['deaths']}, "
              f"veneno mordido {f(e0)}")
        print(f"             voraz {VORAZ} -> emite {sorted(ev['canal_emitido'] or {})}, muertes {ev['deaths']}, "
              f"veneno mordido {f(ev)}")
        p = receptor(s, mv[s], 'sen', par_herm=(1, 0))['primera_b4'] or {}
        print(f"             PAR: 1.a exposicion tras la entrega a {XNEG} {p.get(XNEG, [None])[0]} y a T1v0 "
              f"{p.get('T1v0', [None])[0]}")

    sys.exit(0 if tot[0] == tot[1] else 1)
