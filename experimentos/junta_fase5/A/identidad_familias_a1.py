"""Arnes de identidad del instrumento del CREADOR A de la junta de la fase 5
(organismo_familias_a1.py = organismo_familias_b6 + LECTURA POR DOS TIPOS DE GANADORA). Reglas 2 y 14 de EQUIPO.md.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales (sin
backprop) que aprende, desaprende, generaliza y se COMUNICA CON REFERENCIA. Hoy: que el mensaje refiera a la
FAMILIA Y a la VARIANTE con la MISMA tabla.

  APAGADO (dos_tipos=0): == organismo_familias_b6 en TODAS sus claves, para CUALQUIER `k_ganadoras` y
                       CUALQUIER `memoria_variante`, en mundo='AB', en el mundo de familias, con el canal
                       apagado y encendido en sus tres modos, con `voraz` y con `par_herm`.
  RNG NO CONSUMIDO   : lo mismo a T = 120000 (ancla larga), con k = 1 y k = 3.
  CADENA COMPLETA    : apagado == b6, == b5, == b4b, == organismo_familias, == organismo_v14 (TRONCO) y, con el
                       relevo ON en 6 px, == organismo_v15f_on.
  INERCIA            : con memoria_pares=None la perilla NO existe (no hay tabla que leer).
  ESTRUCTURA         : los dos tipos son la PARTICION DECLARADA de las 66 celdas (36 forma-forma + 27 mixtas;
                       las 3 puras variante-variante quedan fuera de los dos, a proposito), reimplementada
                       FUERA del organismo y comparada; las ganadoras de variante cubren UN pixel de variante
                       cada una; todas las de forma son ciegas a la variante.
  EL MECANISMO HACE LO QUE DICE: con dos_tipos=1 la HERMANA deja de compartir la direccion CONJUNTA del
                       referente (y con k = 3 sola la comparte), y el referente sigue en la suya. Si esto no se
                       cumple, no hay nada que medir y se para aqui.
  PESOS              : con pesos_tipo=0 los dos pesos valen 1.0 EXACTO al final de la corrida; con 1 se mueven,
                       siguen con media 1 y no bajan del suelo.
  CONTROLES QUE DEBEN FALLAR: sin ellos el arnes pasaria por vacuidad (ERR-64b: >= 2 de 3 semillas).

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/junta_fase5/A/identidad_familias_a1.py
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_v15f_on as V15FON
import organismo_familias as MF
import organismo_familias_b4b as B4B
import organismo_familias_b5 as B5
import organismo_familias_b6 as B6
import organismo_familias_a1 as A1

T = 20000
T_LARGO = 120000
T_CANAL = 60000
SEM = (1, 2, 3)
SEM_R = 100000
VORAZ = 1.0          # FIJADO en el preregistro del bloque 4b 3.2; los bloques 5, 6 y la junta NO lo tocan
KS = (1, 3)
NP = 66              # C(12,2)
NVAR = 3             # fam_nvar: los pixeles 9, 10 y 11
N_FORMA = 36         # C(9,2): pares de dos px de forma
N_MIXTAS = 27        # 9 x 3: un px de forma + uno de variante  (36 + 27 + C(3,2)=3 puras = 66)
SHAS = {'organismo_v14.py (TRONCO CONGELADO)': (os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), 'feefc88b1fd8d434'),
        'organismo_v15f_on.py': (os.path.join(CREA, 'organismo_v15f_on.py'), '54d6efe0b564113c'),
        'organismo_familias.py (bloque 1)': (os.path.join(N12, 'organismo_familias.py'), 'b9dd561a0cf056b8'),
        'organismo_familias_b4b.py (bloque 4b)': (os.path.join(N12, 'organismo_familias_b4b.py'), 'b3dd1d7e66a2d147'),
        'organismo_familias_b5.py (bloque 5)': (os.path.join(N12, 'organismo_familias_b5.py'), 'e0b6b90f6f92d5c1'),
        'organismo_familias_b6.py (bloque 6)': (os.path.join(N12, 'organismo_familias_b6.py'), 'b10cbd4ddd0c32a3'),
        'construye_familias_a1.py': (os.path.join(AQUI, 'construye_familias_a1.py'), None),
        'organismo_familias_a1.py': (os.path.join(AQUI, 'organismo_familias_a1.py'), None)}

FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)
MUNDO = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=2, n_neu=0, costo=0.008, log_cada=250,
             crit_exp=0.5, cambio=10**9, vira=0, fam_val='familia', exc_fija=2, memoria_pares='relevo', reg_b2=1)
KW_E = dict(MUNDO, deriva=5000)
KW_R = dict(MUNDO, deriva=T_CANAL // 3 + 1, reg_b4=1)
XPOS, XNEG = 'T0v2', 'T1v2'
HERM, OTRO_TK = 'T1v0', 'T3v2'
NUEVAS_A1 = ('dos_tipos', 'k_forma', 'k_var', 'var_cubre', 'pesos_tipo', 'eta_w', 'combina', 'msg_elige',
             'exige_dir', 'dentro', 'n_forma', 'n_mixtas', 'tipo_gan_forma', 'tipo_gan_var', 'w_forma',
             'w_variante', 'canal_mismo_dos', 'canal_gan_tipo')
A1P = dict(dos_tipos=1, combina='min', exige_dir=1, msg_elige=0)   # el CANDIDATO A1 (tres reglas; `dentro` NO entra: medido inerte, caso (r3))
NUEVAS_B6 = ('memoria_variante', 'memoria_slots', 'memoria_nvar', 'canal_mismo_dir_k')
NUEVAS_B5 = ('k_ganadoras', 'mem_ganadoras', 'canal_gan_k_pre', 'canal_gan_k_post', 'canal_mismo_bin_k')
NUEVAS_B4B = ('voraz', 'par_herm', 'par_fijo')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def compara(a, b, salta=()):
    return [k for k in a if k not in salta and N(a[k]) != N(b.get(k))] + \
           [k for k in a if k not in b and k not in salta]


def caso(etiq, fa, fb, t0, debe_diferir=False, semillas=SEM, tot=None, salta=()):
    ok, detalle = 0, ''
    for s in semillas:
        dif = compara(fa(s), fb(s), salta)
        ok += int((not dif) != debe_diferir)
        if dif and not detalle:
            detalle = ' ' + str(dif[:5])
    need = (len(semillas) - 1 if (debe_diferir and len(semillas) >= 3) else len(semillas))
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    est = marca if ok >= need else ('FALLA' + detalle)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:74s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None:
        tot[0] += int(ok >= need); tot[1] += 1
    return ok >= need


def uno(etiq, ok, t0, tot):
    print(f"  [{time.time()-t0:6.1f}s] {etiq:74s} {'1/1 OK' if ok else '0/1 FALLA'}", flush=True)
    tot[0] += int(bool(ok)); tot[1] += 1
    return bool(ok)


def lanza(etiq, f, t0, tot):
    try:
        f(); ok = False
    except (ValueError, TypeError, IndexError):
        ok = True
    except Exception:
        ok = False
    print(f"  [{time.time()-t0:6.1f}s] {etiq:74s} {'1/1 LANZA (como debe)' if ok else '0/1 NO LANZA'}", flush=True)
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


# ---- la particion y la direccion REIMPLEMENTADAS FUERA del organismo (para comprobar las de dentro)
PARES12 = [(i, j) for i in range(12) for j in range(i + 1, 12)]
FORMA_F = [c for c in range(NP) if max(PARES12[c]) < 12 - NVAR]
MIXTA_F = [c for c in range(NP) if min(PARES12[c]) < 12 - NVAR <= max(PARES12[c])]
PURA_F = [c for c in range(NP) if min(PARES12[c]) >= 12 - NVAR]


def dir_fuera(par, P, mv, nvar=NVAR, D=12):
    b = int(P[par[0]]) * 2 + int(P[par[1]])
    if not mv:
        return b
    s = 0
    for q in range(D - nvar, D):
        s = s * 2 + int(P[q])
    return b * (1 << nvar) + s


def mensaje(s, Tc=T_CANAL, ref=XNEG, voraz=VORAZ):
    """El EMISOR de la fase 5 corre con dos_tipos=0, memoria_variante=0 y k_ganadoras=1: es b4b BIT A BIT."""
    e = (A1.run(s, T=Tc, fam_seed=s, canal={'modo': 'emite'}, voraz=voraz, k_ganadoras=1, memoria_variante=0,
                **KW_E)['canal_emitido'] or {}).get(ref)
    return None if e is None else dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))


def receptor(s, msg, modo='sen', Tc=T_CANAL, P=None, par_herm=None, **kw):
    c = dict(modo=modo, t=msg['t'], ref=msg['ref'], P=(msg['P'] if P is None else P), R=msg['R'])
    return A1.run(s + SEM_R, T=Tc, fam_seed=s, canal=c, par_herm=par_herm, **dict(KW_R, **kw))


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
          f"tipos: {N_FORMA} forma + {N_MIXTAS} mixtas (+{len(PURA_F)} puras FUERA) = {NP}, UN proceso\n")

    tot = [0, 0]
    m0 = {s: mensaje(s) for s in SEM}
    SEM_MSG = tuple(s for s in SEM if m0[s] is not None)
    print(f"  emisores con mensaje (-): {len(SEM_MSG)}/{len(SEM)} -> {SEM_MSG}\n")

    print("APAGADO (dos_tipos=0): organismo_familias_a1 == organismo_familias_b6, para CUALQUIER k y sufijo")
    for etiq, kw in [('(a) mundo=AB base', dict()),
                     ('(b) mundo=AB, relevo ENCENDIDO (v15f)', dict(memoria_pares='relevo')),
                     ('(c) mundo=AB, linaje v13', dict(mask_rel=0, puerta_pat=0)),
                     ('(d) mundo=familias (bloque 1)', dict(FAM)),
                     ('(e) el mundo del bloque 4, EMISOR', dict(KW_E, fam_seed=1)),
                     ('(f) el mundo del bloque 4, RECEPTOR', dict(KW_R, fam_seed=1)),
                     ('(g) el emisor VORAZ anotando (voraz=1.0)', dict(KW_E, fam_seed=1, voraz=VORAZ,
                                                                       canal={'modo': 'emite'})),
                     ('(h) el brazo PAR del bloque 4b (par_herm=(1,0))', dict(KW_R, fam_seed=1,
                                                                              par_herm=(1, 0)))]:
        for k in KS:
            for mv in (0, 1):
                caso(f'{etiq[:3]}{"" if (k, mv) == (1, 0) else " k=%d sufijo=%d" % (k, mv)} {etiq[4:]}',
                     (lambda x, kk, m: lambda s: B6.run(s, T=T, k_ganadoras=kk, memoria_variante=m, **x))(kw, k, mv),
                     (lambda x, kk, m: lambda s: A1.run(s, T=T, k_ganadoras=kk, memoria_variante=m, dos_tipos=0,
                                                        **x))(kw, k, mv),
                     t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_A1)
    print("  ...y con el CANAL ENCENDIDO en sus tres modos (el canal NO se toca)")
    for etiq, modo in [('(i) canal sen, k = 3', 'sen'), ('(j) canal inm, k = 3', 'inm'),
                       ('(k) canal mudo, k = 3', 'mudo')]:
        caso(etiq, (lambda mo: lambda s: B6.run(s + SEM_R, T=T_CANAL, fam_seed=s, k_ganadoras=3,
                 memoria_variante=0, canal=dict(modo=mo, t=m0[s]['t'], ref=m0[s]['ref'], P=m0[s]['P'],
                                                R=m0[s]['R']), **KW_R))(modo),
             (lambda mo: lambda s: receptor(s, m0[s], mo, k_ganadoras=3, memoria_variante=0, dos_tipos=0))(modo),
             t0, semillas=SEM_MSG[:2], tot=tot, salta=NUEVAS_A1)

    print("\nRNG NO CONSUMIDO por la perilla apagada (ancla larga)")
    for k in KS:
        caso(f'(l{k}) mundo=AB a T = {T_LARGO}, relevo ENCENDIDO, k = {k}',
             (lambda kk: lambda s: B6.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=kk))(k),
             (lambda kk: lambda s: A1.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=kk, dos_tipos=0))(k),
             t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_A1)

    print("\nCADENA COMPLETA (se comprueba hasta el TRONCO, no se supone)")
    caso('(m) apagado == organismo_familias_b5 (mundo del bloque 4, k = 3)',
         lambda s: B5.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
         lambda s: A1.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_A1 + NUEVAS_B6)
    caso('(n) apagado == organismo_familias_b4b (mundo del bloque 4, emisor voraz)',
         lambda s: B4B.run(s, T=T, voraz=VORAZ, **dict(KW_E, fam_seed=s)),
         lambda s: A1.run(s, T=T, voraz=VORAZ, **dict(KW_E, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5)
    caso('(o) apagado + mundo=AB == organismo_v14 (TRONCO CONGELADO)', lambda s: V14.run(s, T=T),
         lambda s: A1.run(s, T=T), t0, tot=tot, salta=NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso('(p) relevo ON + mundo=AB == organismo_v15f_on', lambda s: V15FON.run(s, T=T),
         lambda s: A1.run(s, T=T, memoria_pares='relevo'), t0, tot=tot,
         salta=NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso('(q) apagado + mundo=familias == organismo_familias (bloque 1)', lambda s: MF.run(s, T=T, **FAM),
         lambda s: A1.run(s, T=T, **FAM), t0, semillas=SEM[:2], tot=tot,
         salta=NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)

    print("\nINERCIA: las perillas de LECTURA no existen sin `dos_tipos` (y `msg_elige`=1 es b6 literal)")
    caso('(r0) dos_tipos=0: combina/dentro/exige_dir son INERTES (== b6, mundo del receptor, k = 3)',
         lambda s: B6.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
         lambda s: A1.run(s, T=T, k_ganadoras=3, dos_tipos=0, combina='min', dentro='min', exige_dir=1,
                          **dict(KW_R, fam_seed=s)), t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_A1)
    caso("(r3) MEDIDO INERTE: `dentro`='min' == 'suma' en el brazo BAR-H tras el mensaje -- las ganadoras "
         "de un MISMO tipo, elegidas por error propio, no discrepan entre si (por eso el candidato NO lo lleva)",
         lambda s: receptor(s, m0[s], 'sen', P=PATS(s)[HERM], k_ganadoras=3, dentro='suma', **A1P),
         lambda s: receptor(s, m0[s], 'sen', P=PATS(s)[HERM], k_ganadoras=3, dentro='min', **A1P),
         t0, semillas=SEM_MSG, tot=tot, salta=NUEVAS_A1)
    caso("(r2) con combina='min' los pesos de tipo son INERTES (el minimo no los usa)",
         lambda s: A1.run(s, T=T, pesos_tipo=0, **dict(KW_R, fam_seed=s, **A1P)),
         lambda s: A1.run(s, T=T, pesos_tipo=1, **dict(KW_R, fam_seed=s, **A1P)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_A1)
    caso('(r1) dos_tipos=1 con pesos/eta_w: `eta_w` es INERTE sin `pesos_tipo` (== pesos_tipo=0)',
         lambda s: A1.run(s, T=T, **dict(KW_R, fam_seed=s, **A1P)),
         lambda s: A1.run(s, T=T, eta_w=0.5, **dict(KW_R, fam_seed=s, **A1P)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_A1)
    print("\nINERCIA: con memoria_pares=None NO hay tabla que leer -> `dos_tipos` no existe")
    caso('(r) memoria_pares=None: dos_tipos=1 == dos_tipos=0 (mundo=AB)',
         lambda s: A1.run(s, T=T, dos_tipos=0), lambda s: A1.run(s, T=T, dos_tipos=1),
         t0, tot=tot, salta=NUEVAS_A1)
    caso('(s) memoria_pares=None: dos_tipos=1 == dos_tipos=0 (mundo de familias)',
         lambda s: A1.run(s, T=T, dos_tipos=0, **FAM), lambda s: A1.run(s, T=T, dos_tipos=1, **FAM),
         t0, tot=tot, salta=NUEVAS_A1)

    print("\nESTRUCTURA de los dos tipos (la particion de las 66 celdas, reimplementada FUERA)")
    okP = okF = okV = okD = True
    for s in SEM:
        r = A1.run(s, T=T, **dict(KW_R, fam_seed=s, **A1P))
        okP &= (r['n_forma'] == N_FORMA and r['n_mixtas'] == N_MIXTAS
                and r['n_forma'] + r['n_mixtas'] + len(PURA_F) == NP)
        gf = [tuple(g) for g in r['tipo_gan_forma']]; gv = [tuple(g) for g in r['tipo_gan_var']]
        okF &= (len(gf) == 3 and all(PARES12.index(g) in FORMA_F for g in gf) and len(set(gf)) == 3)
        okV &= (len(gv) == NVAR and all(PARES12.index(g) in MIXTA_F for g in gv)
                and sorted(max(g) for g in gv) == list(range(12 - NVAR, 12)))   # una por PIXEL de variante
        okD &= (A1.run(s, T=T, **dict(KW_R, fam_seed=s, **A1P))['tipo_gan_var'] == r['tipo_gan_var'])
    uno(f'(A) la particion de dentro == la de fuera ({N_FORMA} forma + {N_MIXTAS} mixtas; 3 puras FUERA)',
        okP, t0, tot)
    uno('(B) las ganadoras de FORMA son pares de dos px de forma, sin repetir (ciegas a la variante)', okF, t0, tot)
    uno('(C) las ganadoras de VARIANTE son mixtas y cubren UN pixel de variante cada una', okV, t0, tot)
    uno('(D) la eleccion de ganadoras es DETERMINISTA (misma semilla -> mismas ganadoras)', okD, t0, tot)

    print("\nEL MECANISMO HACE LO QUE DICE (diagnostico estructural de la direccion CONJUNTA, no conducta)")
    okH = okT = okSub = okMen = True
    det = []
    for s in SEM_MSG:
        r = receptor(s, m0[s], 'sen', k_ganadoras=3, **A1P)
        Q = PATS(s); X = Q[XNEG]
        gk = [tuple(g) for g in (r['canal_gan_tipo'][0] + r['canal_gan_tipo'][1])]   # las ganadoras EN LA ENTREGA
        esp = sorted(n for n in Q if all(dir_fuera(g, Q[n], 0) == dir_fuera(g, X, 0) for g in gk))
        okMen &= (r['canal_mismo_dos'] == esp)          # la direccion conjunta de dentro == la de fuera
        okT &= (XNEG in r['canal_mismo_dos'])           # el referente sigue en su propia direccion
        okH &= (HERM not in r['canal_mismo_dos'])       # la HERMANA ya no: es la puerta del mecanismo
        okSub &= set(r['canal_mismo_dos']) <= set(r['canal_mismo_bin_k'])
        det.append((s, len(r['canal_mismo_bin_k']), len(r['canal_mismo_dos']), HERM in r['canal_mismo_bin_k']))
    uno('(E) la direccion CONJUNTA de dentro == la reimplementada FUERA (funcion solo de la retina)', okMen, t0, tot)
    uno('(F) el grupo CONJUNTO es subconjunto del grupo por BIN de k = 3 (los tipos solo pueden afinar)',
        okSub, t0, tot)
    uno('(G) con dos_tipos=1 la HERMANA NUNCA comparte la direccion conjunta del referente', okH, t0, tot)
    uno('(H) el referente esta SIEMPRE en su propia direccion conjunta (escritura y lectura coinciden)',
        okT, t0, tot)
    print('        ' + '  '.join(f's{s}: por BIN k3 {a}/32 -> CONJUNTA {b}/32 (hermana en el BIN: {c})'
                                 for s, a, b, c in det))

    print("\nPESOS POR TIPO (la regla multiplicativa normalizada)")
    okW0 = okW1 = True
    for s in SEM[:2]:
        r0 = A1.run(s, T=T, pesos_tipo=0, **dict(KW_R, fam_seed=s, **A1P))
        r1 = A1.run(s, T=T, pesos_tipo=1, **dict(KW_R, fam_seed=s, **A1P))
        okW0 &= (r0['w_forma'] == 1.0 and r0['w_variante'] == 1.0)
        okW1 &= (abs(r1['w_forma'] + r1['w_variante'] - 2.0) < 1e-6 and min(r1['w_forma'], r1['w_variante']) > 0)
    uno('(I) con pesos_tipo=0 los dos pesos valen 1.0 EXACTO al final (la perilla no se mueve sola)', okW0, t0, tot)
    uno('(J) con pesos_tipo=1 los pesos siguen normalizados (media 1) y positivos', okW1, t0, tot)

    print("\nPERILLA MAL ESCRITA (no cae en silencio)")
    lanza('(K) dos_tipos=2 lanza', lambda: A1.run(1, T=100, dos_tipos=2), t0, tot)
    lanza('(L) dos_tipos=True lanza (un bool no es una perilla)', lambda: A1.run(1, T=100, dos_tipos=True), t0, tot)
    lanza("(M) dos_tipos='1' lanza", lambda: A1.run(1, T=100, dos_tipos='1'), t0, tot)
    lanza('(N) k_forma=0 lanza', lambda: A1.run(1, T=100, dos_tipos=1, k_forma=0), t0, tot)
    lanza('(O) k_var=-1 lanza', lambda: A1.run(1, T=100, dos_tipos=1, k_var=-1), t0, tot)
    lanza('(P) var_cubre=2 lanza', lambda: A1.run(1, T=100, dos_tipos=1, var_cubre=2), t0, tot)
    lanza('(Q) pesos_tipo=0.5 lanza', lambda: A1.run(1, T=100, dos_tipos=1, pesos_tipo=0.5), t0, tot)
    lanza('(R) eta_w=-1 lanza', lambda: A1.run(1, T=100, dos_tipos=1, eta_w=-1), t0, tot)
    lanza('(S) dos_tipos=1 con fam_nvar=0 lanza (no hay tipo VARIANTE)',
          lambda: A1.run(1, T=200, dos_tipos=1, **dict(FAM, fam_nvar=0)), t0, tot)
    lanza("(S2) combina='suma' lanza (no es una de las dos)", lambda: A1.run(1, T=100, combina='suma'), t0, tot)
    lanza("(S3) dentro='media' lanza", lambda: A1.run(1, T=100, dentro='media'), t0, tot)
    lanza('(S4) exige_dir=2 lanza', lambda: A1.run(1, T=100, exige_dir=2), t0, tot)
    lanza('(S5) msg_elige=True lanza (un bool no es una perilla)',
          lambda: A1.run(1, T=100, msg_elige=True), t0, tot)

    print("\nCONTROLES QUE DEBEN FALLAR (sin ellos el arnes pasaria por vacuidad; ERR-64b: >= 2 de 3)")
    caso('(T) dos_tipos=1 cambia la corrida con el relevo ON (DEBE diferir)',
         lambda s: A1.run(s, T=T, dos_tipos=0, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
         lambda s: A1.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **A1P)),
         t0, debe_diferir=True, tot=tot, salta=NUEVAS_A1)
    caso("(U) pesos_tipo=1 cambia la corrida con combina='media' (DEBE diferir)",
         lambda s: A1.run(s, T=T, dos_tipos=1, pesos_tipo=0, **dict(KW_R, fam_seed=s)),
         lambda s: A1.run(s, T=T, dos_tipos=1, pesos_tipo=1, **dict(KW_R, fam_seed=s)),
         t0, debe_diferir=True, tot=tot, salta=NUEVAS_A1)
    caso('(T2) msg_elige=0 cambia la corrida CON canal (DEBE diferir: el mensaje ya no re-elige)',
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, msg_elige=1),
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, msg_elige=0),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=NUEVAS_A1)
    caso('(V) CANAL != CORTADO con dos_tipos=1 (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'mudo', k_ganadoras=3, **A1P),
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, **A1P),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',))
    caso('(W) el patron de la HERMANA != CANAL con dos_tipos=1 (DEBE diferir: es el brazo que decide)',
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, **A1P),
         lambda s: receptor(s, m0[s], 'sen', P=PATS(s)[HERM], k_ganadoras=3, **A1P),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',))
    caso('(X) el patron de OTRO TOKEN != CANAL con dos_tipos=1 (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, **A1P),
         lambda s: receptor(s, m0[s], 'sen', P=PATS(s)[OTRO_TK], k_ganadoras=3, **A1P),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',))

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el paquete puede correr." if tot[0] == tot[1] else
                                              "  -> NO se corre nada hasta que sea 100%."))
    sys.exit(0 if tot[0] == tot[1] else 1)
