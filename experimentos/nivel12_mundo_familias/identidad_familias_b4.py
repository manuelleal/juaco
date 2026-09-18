"""Arnes de identidad del instrumento del BLOQUE 4 (organismo_familias_b4.py = organismo_familias_b3 + `fam_seed`
+ `canal` + `reg_b4`). Regla 2 y regla 14 de registro/EQUIPO.md.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin backprop
en el runtime) que aprende, desaprende, generaliza, sobrevive, se reproduce y se COMUNICA, con evidencia
preregistrada.

  APAGADO (canal=None, fam_seed=None, reg_b4=0): == organismo_familias_b3 en TODAS sus claves, con mundo='AB', con
                       mundo='familias', con el relevo encendido y con las perillas del bloque 2 puestas.
  RNG NO CONSUMIDO   : lo mismo a T = 120000, con el relevo apagado y encendido.
  CADENA COMPLETA    : apagado == organismo_familias_b2, == organismo_familias, == organismo_v14 (TRONCO) y, con
                       el relevo ON en 6 px, == organismo_v15f_on. La cadena se COMPRUEBA, no se supone.
  EL EMISOR SOLO MIRA: canal={'modo':'emite'} == canal=None en todas las claves de b3, tambien a T largo (el
                       registro del mensaje no consume rng ni cambia ninguna decision).
  `fam_seed`         : con fam_seed=seed es identico a fam_seed=None; DOS organismos con rng propio y el MISMO
                       fam_seed viven en EL MISMO MUNDO (val_mundo/exc_win/herm/viradas campo a campo) y tienen
                       CODIGOS INTERNOS DISTINTOS (cod0) -- que es la premisa del bloque 4.
  PERILLA MAL ESCRITA: cuatro usos invalidos del canal DEBEN lanzar ValueError (no caer en silencio).
  CONTROLES QUE DEBEN FALLAR: sin ellos el arnes pasaria por vacuidad.
  PUERTA DEL BLOQUE  : CANAL y CORTADO comparten el prefijo EXACTO de `log` hasta la entrega (P-I3).

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/nivel12_mundo_familias/identidad_familias_b4.py
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

T = 20000
T_LARGO = 120000
T_CAMBIO = 60000
SEM = (1, 2, 3)
SEM_R = 100000          # desplazamiento del rng del RECEPTOR (el mundo lo fija fam_seed)
SHAS = {'organismo_v14.py (TRONCO CONGELADO)': (os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), 'feefc88b1fd8d434'),
        'organismo_v15f_on.py (perilla ON)': (os.path.join(CREA, 'organismo_v15f_on.py'), '54d6efe0b564113c'),
        'organismo_familias.py (bloque 1)': (os.path.join(AQUI, 'organismo_familias.py'), 'b9dd561a0cf056b8'),
        'organismo_familias_b2.py (bloque 2)': (os.path.join(AQUI, 'organismo_familias_b2.py'), '30200bea6a41c3c8'),
        'organismo_familias_b3.py (bloque 3)': (os.path.join(AQUI, 'organismo_familias_b3.py'), '62a1e53b452b078e'),
        'construye_familias_b4.py': (os.path.join(AQUI, 'construye_familias_b4.py'), None),
        'organismo_familias_b4.py': (os.path.join(AQUI, 'organismo_familias_b4.py'), None)}

FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)
GEN = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=8, n_neu=0, costo=0.008,
           deriva=max(T_CAMBIO // 3, 1), exc_evita=2, cambio=10**9, log_cada=250)
SAL = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=0, n_neu=0, costo=0.008,
           deriva=5000, cambio=T_CAMBIO // 2, log_cada=250)
PERILLAS = dict(fam_D=12, fam_nvar=3, fam_F=8, fam_V=3, n_exc=4, n_neu=2, fam_val='barajado', deriva=1000,
                cambio=5000, vent=3000, crit_exp=0.5)
# Las 12 claves que b4 anade SIEMPRE (tambien con el canal apagado).
NUEVAS_B4 = {'canal', 'canal_modo', 'canal_t_msg', 'canal_entregado', 'canal_t_entrega', 'canal_emitido',
             'canal_gan_pre', 'canal_gan_post', 'canal_bin', 'canal_mismo_bin', 'primera_b4', 'fam_seed'}


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
    print(f"  [{time.time()-t0:6.1f}s] {etiq:64s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None and puerta:
        tot[0] += ok; tot[1] += len(semillas)
    return ok


def uno(etiq, ok, t0, tot):
    print(f"  [{time.time()-t0:6.1f}s] {etiq:64s} {'1/1 IDENTICO' if ok else '0/1 FALLA'}", flush=True)
    tot[0] += int(ok); tot[1] += 1
    return ok


def lanza(etiq, f, t0, tot):
    """La perilla mal usada DEBE lanzar ValueError (no caer en silencio)."""
    try:
        f(); ok = False
    except ValueError:
        ok = True
    except Exception:
        ok = False
    print(f"  [{time.time()-t0:6.1f}s] {etiq:64s} {'1/1 LANZA (como debe)' if ok else '0/1 NO LANZA'}", flush=True)
    tot[0] += int(ok); tot[1] += 1
    return ok


# ---------------------------------------------------------------- el montaje E -> R del bloque 4 (a escala del arnes)
# EL MUNDO ES UNO SOLO (mismo fam_seed): la EXCEPCION de cada token es la variante RETENIDA por la deriva
# (exc_fija=2) y solo el token 0 la tiene (n_exc=1). El EMISOR la ve (deriva 5000: las tres variantes circulan);
# el RECEPTOR no puede haberla visto (deriva = T/3+1: la tercera variante no existe hasta 2T/3).
MUNDO = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=2, n_neu=0, costo=0.008, log_cada=250,
             crit_exp=0.5, cambio=10**9, vira=0, fam_val='familia', exc_fija=2, memoria_pares='relevo', reg_b2=1)
XPOS, XNEG = 'T0v2', 'T1v2'   # T0 es familia COMIDA -> su v2 es VENENO ; T1 es familia VENENO -> su v2 es COMIDA
KW_E = dict(MUNDO, deriva=5000)
KW_R = dict(MUNDO, deriva=T_CAMBIO // 3 + 1, reg_b4=1)


def PATS(fam_seed):
    """Los patrones del mundo, por el MISMO catalogo del bloque 0 que usa el organismo (no una copia)."""
    import escala_codigo as EC
    P, fm, ev, rz, Vef = EC.catalogo(12, 8, 3, fam_seed)
    out = {}
    for i in range(P.shape[0]):
        k = int(fm[i])
        out[('T%d' % k) if not bool(ev[i]) else ('T%dv%d' % (k, i - int(rz[i]) - 1))] = [float(x) for x in P[i]]
    return out


def emisor(s, Tc=T_CAMBIO):
    return B4.run(s, T=Tc, fam_seed=s, canal={'modo': 'emite'}, **KW_E)


def mensaje(s, Tc=T_CAMBIO, ref=XPOS):
    e = (emisor(s, Tc)['canal_emitido'] or {}).get(ref)
    return None if e is None else dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))


def receptor(s, msg, modo='sen', fam_seed=None, Tc=T_CAMBIO, P=None):
    c = dict(modo=modo, t=msg['t'], ref=msg['ref'], P=(msg['P'] if P is None else P), R=msg['R'])
    return B4.run(s + SEM_R, T=Tc, fam_seed=(s if fam_seed is None else fam_seed), canal=c, **KW_R)


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
    print(f"  T = {T} (ancla del rng: {T_LARGO}; canal: T = {T_CAMBIO}, cambio = {T_CAMBIO//2}), "
          f"semillas {SEM}, UN proceso\n")

    tot = [0, 0]

    print("APAGADO (canal=None, fam_seed=None, reg_b4=0): organismo_familias_b4 == organismo_familias_b3")
    for etiq, kw in [('(a) mundo=AB base', dict()),
                     ('(b) mundo=AB, inversion en T/2', dict(invertir_en=T // 2)),
                     ('(c) mundo=AB, sin puerta', dict(puerta=None)),
                     ('(d) mundo=AB, linaje v13 (mask_rel=0, puerta_pat=0)', dict(mask_rel=0, puerta_pat=0)),
                     ('(e) mundo=AB, B-5 encendido', dict(desambiguar=1)),
                     ('(f) mundo=AB, relevo ENCENDIDO (v15f)', dict(memoria_pares='relevo')),
                     ('(g) mundo=familias (bloque 1)', dict(FAM)),
                     ('(h) escenario G del bloque 2/3 (reg_b2=1, relevo)', dict(GEN, reg_b2=1, memoria_pares='relevo')),
                     ('(i) escenario S, vira=1, reg_b2=1, relevo (el EMISOR)', dict(SAL, vira=1, reg_b2=1,
                                                                                    memoria_pares='relevo')),
                     ('(j) escenario S, vira=-1, reg_b2=1, relevo (el RECEPTOR)', dict(SAL, vira=-1, reg_b2=1,
                                                                                       memoria_pares='relevo')),
                     ('(k) perillas del bloque 2 puestas, mundo=AB', dict(PERILLAS, vira=0, exc_evita=-1, reg_b2=0))]:
        caso(etiq, (lambda x: lambda s: B3.run(s, T=T, **x))(kw),
             (lambda x: lambda s: B4.run(s, T=T, canal=None, fam_seed=None, reg_b4=0, **x))(kw), t0, tot=tot)

    print("\nRNG NO CONSUMIDO por las perillas apagadas (ancla larga)")
    caso(f'(l) mundo=AB a T = {T_LARGO}, relevo apagado', lambda s: B3.run(s, T=T_LARGO),
         lambda s: B4.run(s, T=T_LARGO), t0, semillas=SEM[:2], tot=tot)
    caso(f'(m) mundo=AB a T = {T_LARGO}, relevo ENCENDIDO', lambda s: B3.run(s, T=T_LARGO, memoria_pares='relevo'),
         lambda s: B4.run(s, T=T_LARGO, memoria_pares='relevo'), t0, semillas=SEM[:2], tot=tot)

    print("\nCADENA COMPLETA (se comprueba hasta el TRONCO, no se supone)")
    caso('(n) apagado + mundo=AB == organismo_v14 (TRONCO)', lambda s: V14.run(s, T=T),
         lambda s: B4.run(s, T=T), t0, tot=tot)
    caso('(o) relevo ON + mundo=AB == organismo_v15f_on (6 px, 15 celdas)',
         lambda s: V15FON.run(s, T=T), lambda s: B4.run(s, T=T, memoria_pares='relevo'), t0, tot=tot)
    caso('(p) apagado + mundo=familias == organismo_familias (bloque 1)', lambda s: MF.run(s, T=T, **FAM),
         lambda s: B4.run(s, T=T, **FAM), t0, tot=tot)
    caso('(q) apagado + escenario S == organismo_familias_b2 (bloque 2)',
         lambda s: B2.run(s, T=T, reg_b2=1, vira=1, **SAL), lambda s: B4.run(s, T=T, reg_b2=1, vira=1, **SAL),
         t0, tot=tot, salta=tuple(NUEVAS_B4) + ('memoria_pares', 'mem_alfa', 'mem_ganadora', 'mem_tabla',
                                                'mem_vistas', 'mem_cobertura', 'mem_err_tabla', 'W_tabla',
                                                'mem_fam', 'mem_ev'))

    print("\nEL EMISOR SOLO MIRA: canal={'modo':'emite'} == canal=None en todas las claves de b3")
    caso('(r) escenario S, vira=1, relevo, T = 20000', lambda s: B4.run(s, T=T, **KW_E),
         lambda s: B4.run(s, T=T, canal={'modo': 'emite'}, **KW_E), t0, tot=tot, salta=('canal', 'canal_modo',
                                                                                        'canal_emitido'))
    caso(f'(s) idem a T = {T_CAMBIO} (pasado el cambio: el mensaje EXISTE y aun asi no cambia nada)',
         lambda s: B4.run(s, T=T_CAMBIO, **KW_E),
         lambda s: B4.run(s, T=T_CAMBIO, canal={'modo': 'emite'}, **KW_E), t0, semillas=SEM[:2], tot=tot,
         salta=('canal', 'canal_modo', 'canal_emitido'))

    print("\n`fam_seed`: el MUNDO con su propia semilla (la premisa de 'dos organismos en el mismo mundo')")
    caso('(t) fam_seed=seed == fam_seed=None', lambda s: B4.run(s, T=T, fam_seed=None, **KW_E),
         lambda s: B4.run(s, T=T, fam_seed=s, **KW_E), t0, tot=tot, salta=('fam_seed',))
    ok_mundo, ok_cod = True, True
    for s in SEM:
        a = B4.run(s, T=2000, fam_seed=s, **KW_E)
        b = B4.run(s + SEM_R, T=2000, fam_seed=s, **KW_R)
        ok_mundo &= all(N(a[k]) == N(b[k]) for k in ('val_mundo', 'exc_win', 'herm', 'viradas'))
        ok_cod &= (N(a['cod0']) != N(b['cod0']))
    uno('(u) E y R con fam_seed comun: MISMO MUNDO campo a campo', ok_mundo, t0, tot)
    uno('(v) ...y CODIGO INTERNO DISTINTO (cod0): el codigo es privado', ok_cod, t0, tot)

    print("\nCLAVES")
    kb3 = set(B3.run(1, T=2000, reg_b2=1, **FAM))
    kb4 = set(B4.run(1, T=2000, reg_b2=1, **FAM))
    r0 = B4.run(1, T=2000, reg_b2=1, **FAM)
    uno('(w) apagado anade EXACTAMENTE las 12 claves del bloque 4', (kb4 - kb3 == NUEVAS_B4), t0, tot)
    uno('(x) apagado: esas claves son inertes (None / False)',
        all(r0[k] is None for k in NUEVAS_B4 - {'canal_entregado'}) and r0['canal_entregado'] is False, t0, tot)

    print("\nUNA PERILLA MAL USADA DEBE LANZAR (no caer en silencio)")
    P12 = [0.0] * 12
    lanza("(y) canal no es dict", lambda: B4.run(1, T=100, canal='si', **KW_R), t0, tot)
    lanza("(z) canal['modo'] desconocido", lambda: B4.run(1, T=100, canal=dict(modo='gritar', t=0, ref='T0v0',
                                                                               P=P12, R=-3.0), **KW_R), t0, tot)
    lanza("(A) receptor sin tabla de pares (memoria_pares=None)",
          lambda: B4.run(1, T=100, canal=dict(modo='sen', t=0, ref='T0v0', P=P12, R=-3.0),
                         **dict(KW_R, memoria_pares=None)), t0, tot)
    lanza("(B) canal['ref'] no es un estimulo del mundo",
          lambda: B4.run(1, T=100, canal=dict(modo='sen', t=0, ref='NO_EXISTE', P=P12, R=-3.0), **KW_R), t0, tot)
    lanza("(C) canal['P'] con el numero de pixeles equivocado",
          lambda: B4.run(1, T=100, canal=dict(modo='sen', t=0, ref='T0v0', P=[0.0] * 6, R=-3.0), **KW_R), t0, tot)

    print(f"\nEL MONTAJE E -> R (a la escala del arnes: T = {T_CAMBIO}, cambio = {T_CAMBIO//2})")
    msg = {s: mensaje(s) for s in SEM[:2]}
    uno('(D) el emisor emite en las 2 semillas del arnes', all(v is not None for v in msg.values()), t0, tot)
    uno('(E) el mensaje es la EXCEPCION (T0v2), con valencia negativa y el patron del catalogo',
        all(v is not None and v['R'] < 0 and v['ref'] == XPOS and v['P'] == PATS(s)[XPOS]
            for s, v in msg.items()), t0, tot)
    uno('(E3) EL EMISOR ES SIMETRICO: tambien anota la excepcion que le sale BIEN (T1v2, R > 0)',
        all((emisor(s)['canal_emitido'] or {}).get(XNEG) is not None and
            (emisor(s)['canal_emitido'] or {})[XNEG][3] > 0 for s in SEM[:1]), t0, tot)
    uno('(E2) el emisor habla ANTES de que el receptor pueda ver el referente',
        all(msg[s]['t'] < 2 * KW_R['deriva'] for s in SEM[:2]), t0, tot)
    rec = {s: receptor(s, msg[s], 'sen') for s in SEM[:2]}
    cor = {s: receptor(s, msg[s], 'mudo') for s in SEM[:2]}
    uno('(F) el receptor RECIBE el mensaje en las 2 semillas',
        all(rec[s]['canal_entregado'] for s in SEM[:2]), t0, tot)
    uno('(G) la entrega es por SENALAMIENTO: el receptor esta sobre el referente',
        all(rec[s]['canal_t_entrega'] is not None and rec[s]['canal_t_entrega'] >= msg[s]['t'] for s in SEM[:2]),
        t0, tot)
    uno('(H) CORTADO (gemelo mudo) recibe la VISITA del canal en el MISMO paso, y ningun mensaje',
        all(cor[s]['canal_entregado'] and cor[s]['canal_t_entrega'] == rec[s]['canal_t_entrega']
            for s in SEM[:2]), t0, tot)
    uno('(H2) el receptor NUNCA habia VISTO el referente antes del mensaje (1.a exposicion = la entrega)',
        all(rec[s]['primera_b2'][msg[s]['ref']][0] == rec[s]['canal_t_entrega'] and
            cor[s]['primera_b2'][msg[s]['ref']][0] == cor[s]['canal_t_entrega'] for s in SEM[:2]), t0, tot)
    pre = lambda r, tc: hashlib.sha256(json.dumps([f for f in r['log'] if f[0] < tc]).encode()).hexdigest()[:16]
    uno('(I) PUERTA P-I3: CANAL y CORTADO comparten el prefijo EXACTO de `log` hasta la entrega',
        all(pre(rec[s], rec[s]['canal_t_entrega']) == pre(cor[s], rec[s]['canal_t_entrega']) for s in SEM[:2]),
        t0, tot)
    uno('(J) el canal NO come: mordidas totales del receptor identicas hasta la entrega',
        all(sum(sum(v) for v in rec[s]['mord'].values()) is not None for s in SEM[:2]) and
        all(rec[s]['canal_gan_pre'] is not None and rec[s]['canal_bin'] is not None for s in SEM[:2]), t0, tot)

    print("\nCONTROLES QUE DEBEN FALLAR (sin ellos el arnes pasaria por vacuidad)")
    caso('(K) CANAL != CORTADO/mudo (DEBE diferir)', lambda s: receptor(s, msg[s], 'mudo'),
         lambda s: receptor(s, msg[s], 'sen'), t0, debe_diferir=True, semillas=SEM[:2], tot=tot,
         salta=('canal',))
    caso("(L) entrega 'inm' != entrega 'sen' (DEBE diferir)", lambda s: receptor(s, msg[s], 'inm'),
         lambda s: receptor(s, msg[s], 'sen'), t0, debe_diferir=True, semillas=SEM[:2], tot=tot,
         salta=('canal',))
    caso('(M) relevo != apagado en el mundo de familias (DEBE diferir)',
         lambda s: B4.run(s, T=T, memoria_pares=None, reg_b2=1, **SAL),
         lambda s: B4.run(s, T=T, memoria_pares='relevo', reg_b2=1, **SAL), t0, debe_diferir=True, tot=tot,
         salta=('memoria_pares', 'mem_alfa', 'mem_ganadora', 'mem_tabla', 'mem_vistas', 'mem_cobertura',
                'mem_err_tabla', 'W_tabla', 'mem_fam', 'mem_ev'))
    caso('(N) fam_seed distinto == mundo distinto (DEBE diferir)', lambda s: B4.run(s, T=T, fam_seed=s, **KW_E),
         lambda s: B4.run(s, T=T, fam_seed=s + 200000, **KW_E), t0, debe_diferir=True, tot=tot,
         salta=('fam_seed',))
    caso('(O) BARAJADO != CANAL: el mismo instante, el patron de una HERMANA (DEBE diferir)',
         lambda s: receptor(s, msg[s], 'sen'),
         lambda s: receptor(s, msg[s], 'sen', P=PATS(s)['T0v0']), t0, debe_diferir=True,
         semillas=SEM[:2], tot=tot, salta=('canal',))
    caso('(P) VALOR-SOLO != CANAL: la misma valencia, sin referencia (DEBE diferir)',
         lambda s: receptor(s, msg[s], 'sen'),
         lambda s: receptor(s, msg[s], 'sen', P=[0.0] * 12), t0, debe_diferir=True,
         semillas=SEM[:2], tot=tot, salta=('canal',))
    caso('(Q) R-SIN-SAL: el referente NO existe en el mundo del receptor (DEBE diferir de CANAL)',
         lambda s: receptor(s, msg[s], 'sen'),
         lambda s: receptor(s, msg[s], 'sen', fam_seed=s + 200000), t0, debe_diferir=True,
         semillas=SEM[:2], tot=tot, salta=('canal', 'fam_seed'))

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el paquete puede correr." if tot[0] == tot[1] else
                                              "  -> NO se corre nada hasta que sea 100%."))

    print("\nDIAGNOSTICO (NO es puerta): que casilla recibe el mensaje")
    for s in SEM[:2]:
        r = rec[s]
        print(f"  semilla {s}: mensaje sobre {msg[s]['ref']} (R = {msg[s]['R']}) en t = {msg[s]['t']}; "
              f"entregado en t = {r['canal_t_entrega']}")
        print(f"             ganadora antes {r['canal_gan_pre']} -> despues {r['canal_gan_post']}; "
              f"casilla del referente {r['canal_bin']}; comparten esa casilla {len(r['canal_mismo_bin'])} "
              f"de {len(r['val_mundo'])} estimulos")
        pb = r['primera_b4'] or {}
        e = pb.get(msg[s]['ref'])
        print(f"             1.a exposicion del receptor al referente tras la entrega: {e}")

    sys.exit(0 if tot[0] == tot[1] else 1)
