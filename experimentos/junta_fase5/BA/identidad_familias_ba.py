"""Arnes de identidad del instrumento del candidato BA de la junta de la fase 5
(organismo_familias_ba.py = organismo_familias_a1 + CONJUNCION POR TIPO). Reglas 2 y 14 de EQUIPO.md.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy, fase 5:
que el mensaje refiera a la FAMILIA Y a la VARIANTE con la MISMA tabla (BAR-T <= 5/20 Y PAR >= 15/20).

  APAGADO (conj_tipo=0): == organismo_familias_a1 en TODAS sus claves, para CUALQUIER combinacion de las
                       perillas de A (dos_tipos, combina, dentro, exige_dir, msg_elige, pesos_tipo), cualquier
                       `k_ganadoras`, cualquier `memoria_variante`, en mundo='AB', en el mundo de familias, con
                       el canal apagado y con el canal encendido en sus TRES modos.
  RNG NO CONSUMIDO   : lo mismo a T = 120000 (ancla larga).
  CADENA COMPLETA    : apagado + dos_tipos=0 == b6, == b5, == b4b, == organismo_familias, == organismo_v14
                       (TRONCO CONGELADO) y, con el relevo ON en 6 px, == organismo_v15f_on.
  INERCIA            : con memoria_pares=None la perilla NO existe (no hay tabla que leer).
  ESTRUCTURA (la leccion de B: las reglas de lectura se comparan SOBRE LA MISMA TABLA, nunca con dos
                       trayectorias distintas): la regla de BA se REIMPLEMENTA FUERA del organismo a partir de
                       `mem_tabla`, `mem_visto` y las ganadoras exportadas, y se compara estimulo a estimulo
                       con `W_tabla`; y sobre ESA MISMA tabla se comparan las TRES reglas (A1 `exige_dir`, BA
                       `conj_tipo`, A1-d sin ninguna), que deben quedar ENCAJADAS:
                           habla(A1) SUBCONJUNTO habla(BA) SUBCONJUNTO habla(A1-d).
                       Si no encajan, la regla no es la que dice la cabecera y no se mide nada.
  EL MECANISMO HACE LO QUE DICE: con dos_tipos=1 el referente esta en su direccion conjunta y la HERMANA no
                       (estructural, T = 0 sobre el catalogo; ERR-71: NO pasa por el emisor).
  PERILLA MAL ESCRITA: lanza -- incluidas las DOS combinaciones prohibidas y declaradas (conj_tipo=1 sin
                       dos_tipos; conj_tipo=1 con exige_dir=1).
  CONTROLES QUE DEBEN DIFERIR: sin ellos el arnes pasaria por vacuidad (ERR-64b: >= 2 de 3 semillas).

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/junta_fase5/BA/identidad_familias_ba.py
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
JA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A')
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, JA, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_v15f_on as V15FON
import organismo_familias as MF
import organismo_familias_b4b as B4B
import organismo_familias_b5 as B5
import organismo_familias_b6 as B6
import organismo_familias_a1 as A1
import organismo_familias_ba as BA

T = 20000
T_LARGO = 120000
T_CANAL = 60000
SEM = (1, 2, 3)
SEM_R = 100000
VORAZ = 1.0          # FIJADO en el preregistro del bloque 4b 3.2; los bloques 5, 6 y la junta NO lo tocan
KS = (1, 3)
NP = 66              # C(12,2)
NVAR = 3             # fam_nvar: los pixeles 9, 10 y 11
N_FORMA = 36
N_MIXTAS = 27
SHAS = {'organismo_v14.py (TRONCO CONGELADO)': (os.path.join(RAIZ, 'organismo', 'organismo_v14.py'), 'feefc88b1fd8d434'),
        'organismo_v15f_on.py': (os.path.join(CREA, 'organismo_v15f_on.py'), '54d6efe0b564113c'),
        'organismo_familias.py (bloque 1)': (os.path.join(N12, 'organismo_familias.py'), 'b9dd561a0cf056b8'),
        'organismo_familias_b4b.py (bloque 4b)': (os.path.join(N12, 'organismo_familias_b4b.py'), 'b3dd1d7e66a2d147'),
        'organismo_familias_b5.py (bloque 5)': (os.path.join(N12, 'organismo_familias_b5.py'), 'e0b6b90f6f92d5c1'),
        'organismo_familias_b6.py (bloque 6)': (os.path.join(N12, 'organismo_familias_b6.py'), 'b10cbd4ddd0c32a3'),
        'organismo_familias_a1.py (creador A, ORIGEN)': (os.path.join(JA, 'organismo_familias_a1.py'), '8833e1dcfb62f26d'),
        'construye_familias_ba.py': (os.path.join(AQUI, 'construye_familias_ba.py'), None),
        'organismo_familias_ba.py': (os.path.join(AQUI, 'organismo_familias_ba.py'), None)}

FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)
MUNDO = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=2, n_neu=0, costo=0.008, log_cada=250,
             crit_exp=0.5, cambio=10**9, vira=0, fam_val='familia', exc_fija=2, memoria_pares='relevo', reg_b2=1)
KW_E = dict(MUNDO, deriva=5000)
KW_R = dict(MUNDO, deriva=T_CANAL // 3 + 1, reg_b4=1)
XNEG = 'T1v2'
HERM, OTRO_TK = 'T1v0', 'T3v2'

# claves que SOLO existen en cada eslabon (se saltan al comparar hacia atras)
NUEVAS_BA = ('conj_tipo', 'canal_lee_ref', 'mem_visto')
NUEVAS_A1 = ('dos_tipos', 'k_forma', 'k_var', 'var_cubre', 'pesos_tipo', 'eta_w', 'combina', 'msg_elige',
             'exige_dir', 'dentro', 'n_forma', 'n_mixtas', 'tipo_gan_forma', 'tipo_gan_var', 'w_forma',
             'w_variante', 'canal_mismo_dos', 'canal_gan_tipo')
NUEVAS_B6 = ('memoria_variante', 'memoria_slots', 'memoria_nvar', 'canal_mismo_dir_k')
NUEVAS_B5 = ('k_ganadoras', 'mem_ganadoras', 'canal_gan_k_pre', 'canal_gan_k_post', 'canal_mismo_bin_k')
NUEVAS_B4B = ('voraz', 'par_herm', 'par_fijo')

# las tres lecturas que se comparan (las de A, y la de BA en medio)
A1P = dict(dos_tipos=1, combina='min', exige_dir=1, msg_elige=0)                 # A1, el candidato del creador A
BAP = dict(dos_tipos=1, combina='min', exige_dir=0, msg_elige=0, conj_tipo=1)    # BA, EL CANDIDATO DE ESTA CARPETA
BVP = dict(dos_tipos=1, combina='min', exige_dir=0, msg_elige=0, conj_tipo=2)    # BA-v, ablacion declarada
ADP = dict(dos_tipos=1, combina='min', exige_dir=0, msg_elige=0)                 # A1-d, sin ninguna regla de abstencion


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
    print(f"  [{time.time()-t0:6.1f}s] {etiq:78s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None:
        tot[0] += int(ok >= need); tot[1] += 1
    return ok >= need


def uno(etiq, ok, t0, tot):
    print(f"  [{time.time()-t0:6.1f}s] {etiq:78s} {'1/1 OK' if ok else '0/1 FALLA'}", flush=True)
    tot[0] += int(bool(ok)); tot[1] += 1
    return bool(ok)


def lanza(etiq, f, t0, tot):
    try:
        f(); ok = False
    except (ValueError, TypeError, IndexError):
        ok = True
    except Exception:
        ok = False
    print(f"  [{time.time()-t0:6.1f}s] {etiq:78s} {'1/1 LANZA (como debe)' if ok else '0/1 NO LANZA'}", flush=True)
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


def suma_fuera(gs, P, tabla, visto, mv):
    """La suma de las casillas CONOCIDAS de un tipo, REIMPLEMENTADA FUERA del organismo."""
    s, n = 0.0, 0
    for par in gs:
        c = dir_fuera(tuple(par), P, mv)
        g = PARES12.index(tuple(par))
        if visto[g][c]:
            s += float(tabla[g][c]); n += 1
    return s, n


def lee_fuera(regla, gf, gv, P, tabla, visto, mv):
    """Las TRES reglas de lectura, FUERA del organismo y SOBRE LA MISMA TABLA. Devuelve (valor, habla)."""
    sf, nf = suma_fuera(gf, P, tabla, visto, mv)
    sv, nv = suma_fuera(gv, P, tabla, visto, mv)
    if regla in ('BA', 'BAv'):                           # conjuncion POR TIPO, la FORMA manda
        if nf < len(gf):
            return (0.0, False)
        if nv < len(gv) and (regla == 'BA' or not nv):
            return (sf, True)
        return (min(sf, sv), True)
    if regla == 'A1':                                    # `exige_dir`: los SEIS o la tabla calla
        if nf < len(gf) or nv < len(gv):
            return (0.0, False)
        return (min(sf, sv), True)
    if not nf and not nv:                                # A1-d: sin ninguna regla de abstencion
        return (0.0, False)
    if not nf:
        return (sv, True)
    if not nv:
        return (sf, True)
    return (min(sf, sv), True)


def mensaje(s, Tc=T_CANAL, ref=XNEG, voraz=VORAZ):
    """El EMISOR de la fase 5 corre con dos_tipos=0, memoria_variante=0 y k_ganadoras=1: es b4b BIT A BIT."""
    e = (BA.run(s, T=Tc, fam_seed=s, canal={'modo': 'emite'}, voraz=voraz, k_ganadoras=1, memoria_variante=0,
                **KW_E)['canal_emitido'] or {}).get(ref)
    return None if e is None else dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))


def receptor(s, msg, modo='sen', Tc=T_CANAL, P=None, par_herm=None, mod=BA, **kw):
    c = dict(modo=modo, t=msg['t'], ref=msg['ref'], P=(msg['P'] if P is None else P), R=msg['R'])
    return mod.run(s + SEM_R, T=Tc, fam_seed=s, canal=c, par_herm=par_herm, **dict(KW_R, **kw))


if __name__ == '__main__':
    t0 = time.time()
    malo = False
    for nom, (p, esp) in SHAS.items():
        s = h16(p)
        aviso = '' if esp is None else ('  OK' if s == esp else f'  *** ESPERADO {esp}')
        malo = malo or (esp is not None and s != esp)
        print(f"  sha {nom:46s} {s}{aviso}")
    if malo:
        raise SystemExit("Un origen cambio. Reconstruir por anclas antes de seguir.")
    print(f"  T = {T} (ancla del rng: {T_LARGO}; canal: {T_CANAL}), semillas {SEM}, k = {KS}, UN proceso\n")

    tot = [0, 0]
    m0 = {s: mensaje(s) for s in SEM}
    SEM_MSG = tuple(s for s in SEM if m0[s] is not None)
    print(f"  emisores con mensaje (-): {len(SEM_MSG)}/{len(SEM)} -> {SEM_MSG}\n")

    print("APAGADO (conj_tipo=0): organismo_familias_ba == organismo_familias_a1, con TODAS las perillas de A")
    CFGS = [('(a) mundo=AB base', dict()),
            ('(b) mundo=AB, relevo ENCENDIDO (v15f)', dict(memoria_pares='relevo')),
            ('(c) mundo=AB, linaje v13', dict(mask_rel=0, puerta_pat=0)),
            ('(d) mundo=familias (bloque 1)', dict(FAM)),
            ('(e) el mundo del bloque 4, EMISOR', dict(KW_E, fam_seed=1)),
            ('(f) el mundo del bloque 4, RECEPTOR', dict(KW_R, fam_seed=1)),
            ('(g) el emisor VORAZ anotando (voraz=1.0)', dict(KW_E, fam_seed=1, voraz=VORAZ,
                                                              canal={'modo': 'emite'})),
            ('(h) el brazo PAR del bloque 4b (par_herm=(1,0))', dict(KW_R, fam_seed=1, par_herm=(1, 0)))]
    for etiq, kw in CFGS:
        for k, mv in ((1, 0), (3, 1)):
            caso(f'{etiq[:3]} k={k} sufijo={mv} {etiq[4:]}',
                 (lambda x, kk, m: lambda s: A1.run(s, T=T, k_ganadoras=kk, memoria_variante=m, **x))(kw, k, mv),
                 (lambda x, kk, m: lambda s: BA.run(s, T=T, k_ganadoras=kk, memoria_variante=m, conj_tipo=0,
                                                    **x))(kw, k, mv),
                 t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BA)
    print("  ...y con las perillas de LECTURA de A encendidas (conj_tipo=0 tiene que ser inerte con TODAS)")
    for etiq, p in [('(a2) A1 (dos tipos + min + exige_dir + msg_elige=0)', A1P),
                    ('(a3) A1-d (dos tipos + min, sin exige_dir)', ADP),
                    ('(a4) A1-c (dos tipos + media + exige_dir)', dict(A1P, combina='media')),
                    ('(a5) A1-e (dos tipos + min + exige_dir, el mensaje SI re-elige)', dict(A1P, msg_elige=1)),
                    ("(a6) dos tipos + dentro='min' + pesos_tipo=1", dict(dos_tipos=1, dentro='min',
                                                                          pesos_tipo=1))]:
        caso(etiq, (lambda x: lambda s: A1.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **x)))(p),
             (lambda x: lambda s: BA.run(s, T=T, k_ganadoras=3, conj_tipo=0, **dict(KW_R, fam_seed=s, **x)))(p),
             t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BA)
    print("  ...y con el CANAL ENCENDIDO en sus tres modos (el canal NO se toca)")
    for etiq, modo in [('(i) canal sen, A1 encendido', 'sen'), ('(j) canal inm, A1 encendido', 'inm'),
                       ('(k) canal mudo, A1 encendido', 'mudo')]:
        caso(etiq, (lambda mo: lambda s: receptor(s, m0[s], mo, mod=A1, k_ganadoras=3, **A1P))(modo),
             (lambda mo: lambda s: receptor(s, m0[s], mo, mod=BA, k_ganadoras=3, conj_tipo=0, **A1P))(modo),
             t0, semillas=SEM_MSG[:2], tot=tot, salta=NUEVAS_BA)

    print("\nRNG NO CONSUMIDO por la perilla apagada (ancla larga)")
    caso(f'(l) mundo=AB a T = {T_LARGO}, relevo ENCENDIDO, k = 3',
         lambda s: A1.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=3),
         lambda s: BA.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=3, conj_tipo=0),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BA)
    caso(f'(l2) mundo=AB a T = {T_LARGO}, dos tipos ENCENDIDOS (A1), k = 3',
         lambda s: A1.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=3, **A1P),
         lambda s: BA.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=3, conj_tipo=0, **A1P),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BA)

    print("\nCADENA COMPLETA (se comprueba hasta el TRONCO, no se supone)")
    caso('(m) apagado == organismo_familias_b6 (mundo del receptor, k = 3, sufijo ON)',
         lambda s: B6.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s)),
         lambda s: BA.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BA + NUEVAS_A1)
    caso('(n) apagado == organismo_familias_b5 (mundo del bloque 4, k = 3)',
         lambda s: B5.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
         lambda s: BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BA + NUEVAS_A1 + NUEVAS_B6)
    caso('(o) apagado == organismo_familias_b4b (mundo del bloque 4, emisor voraz)',
         lambda s: B4B.run(s, T=T, voraz=VORAZ, **dict(KW_E, fam_seed=s)),
         lambda s: BA.run(s, T=T, voraz=VORAZ, **dict(KW_E, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BA + NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5)
    caso('(p) apagado + mundo=AB == organismo_v14 (TRONCO CONGELADO)', lambda s: V14.run(s, T=T),
         lambda s: BA.run(s, T=T), t0, tot=tot,
         salta=NUEVAS_BA + NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso('(q) relevo ON + mundo=AB == organismo_v15f_on', lambda s: V15FON.run(s, T=T),
         lambda s: BA.run(s, T=T, memoria_pares='relevo'), t0, tot=tot,
         salta=NUEVAS_BA + NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso('(r) apagado + mundo=familias == organismo_familias (bloque 1)', lambda s: MF.run(s, T=T, **FAM),
         lambda s: BA.run(s, T=T, **FAM), t0, semillas=SEM[:2], tot=tot,
         salta=NUEVAS_BA + NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)

    print("\nINERCIA: sin tabla no hay lectura que cambiar")
    caso('(s) memoria_pares=None: conj_tipo=1 == conj_tipo=0 (mundo=AB)',
         lambda s: BA.run(s, T=T, dos_tipos=1), lambda s: BA.run(s, T=T, dos_tipos=1, conj_tipo=1),
         t0, tot=tot, salta=NUEVAS_BA)
    caso('(s2) memoria_pares=None: conj_tipo=1 == conj_tipo=0 (mundo de familias)',
         lambda s: BA.run(s, T=T, dos_tipos=1, **FAM),
         lambda s: BA.run(s, T=T, dos_tipos=1, conj_tipo=1, **FAM), t0, tot=tot, salta=NUEVAS_BA)
    # HALLAZGO del arnes de BA (candidato a ERR, reportado al coordinador): `dentro` es una perilla MUERTA en
    # el instrumento del creador A -- `_DMv` se CALCULA y NUNCA SE USA (1 sola aparicion en el fuente, la de su
    # definicion). A la reporto como "prediccion propia medida INERTE"; lo que esta medido es que la perilla no
    # esta conectada, no que las ganadoras de un mismo tipo no discrepen. Aqui se comprueba las dos cosas y se
    # dice con su nombre; BA NO la usa (hereda el mismo codigo muerto de A, sin tocarlo).
    caso("(s3) `dentro` es una perilla MUERTA (heredada de A): la corrida es IDENTICA salvo la clave que la "
         "repite -- no es una medida del mecanismo",
         lambda s: BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BAP)),
         lambda s: BA.run(s, T=T, k_ganadoras=3, dentro='min', **dict(KW_R, fam_seed=s, **BAP)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BA + ('dentro',))
    uno("(s4) ...y se ve en el fuente: `_DMv` aparece UNA sola vez (su definicion) en organismo_familias_ba.py "
        "y en organismo_familias_a1.py -> codigo muerto, no mecanismo medido",
        open(os.path.join(AQUI, 'organismo_familias_ba.py'), encoding='utf-8').read().count('_DMv') == 1
        and open(os.path.join(JA, 'organismo_familias_a1.py'), encoding='utf-8').read().count('_DMv') == 1,
        t0, tot)

    print("\nESTRUCTURA: la regla REIMPLEMENTADA FUERA, y las TRES reglas SOBRE LA MISMA TABLA (leccion de B)")
    okR = okE = okP2 = True
    det = []
    for s in SEM:
        r = BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BAP))
        Q = PATS(s); tab, vis = r['mem_tabla'], r['mem_visto']
        gf, gv = r['tipo_gan_forma'], r['tipo_gan_var']
        okP2 &= (r['n_forma'] == N_FORMA and r['n_mixtas'] == N_MIXTAS
                 and r['n_forma'] + r['n_mixtas'] + len(PURA_F) == NP
                 and len(gf) == 3 and all(PARES12.index(tuple(g)) in FORMA_F for g in gf)
                 and len(gv) == NVAR and all(PARES12.index(tuple(g)) in MIXTA_F for g in gv)
                 and sorted(max(g) for g in gv) == list(range(12 - NVAR, 12)))
        hab = {'A1': set(), 'BA': set(), 'BAv': set(), 'AD': set()}
        nvi = 0
        for n in Q:
            v, h = lee_fuera('BA', gf, gv, Q[n], tab, vis, 0)
            dentro = r['W_tabla'].get(n)
            okR &= ((dentro is None and not h) or (h and dentro is not None and abs(dentro - round(v, 3)) < 1e-9))
            for rg in ('A1', 'BA', 'BAv', 'AD'):
                if lee_fuera(rg, gf, gv, Q[n], tab, vis, 0)[1]:
                    hab[rg].add(n)
            nvi += int(suma_fuera(gv, Q[n], tab, vis, 0)[1] < len(gv))
        okE &= (hab['A1'] <= hab['BA'] <= hab['AD'] and hab['BA'] == hab['BAv'])
        det.append((s, len(hab['A1']), len(hab['BA']), len(hab['AD']), nvi))
    uno('(A) la particion y las ganadoras de A siguen intactas (36 forma + 27 mixtas; 1 mixta por px variante)',
        okP2, t0, tot)
    uno('(B) la regla de BA reimplementada FUERA coincide con `W_tabla` en los 32 estimulos', okR, t0, tot)
    uno('(C) sobre LA MISMA tabla: habla(A1) <= habla(BA) = habla(BA-v) <= habla(A1-d) -- BA abstiene MENOS '
        'que A1 y las dos variantes de BA callan en los mismos estimulos', okE, t0, tot)
    print('        ' + '  '.join(f's{s}: habla A1 {a}/32, BA {b}/32, A1-d {c}/32; el tipo VARIANTE esta '
                                 f'incompleto en {d}/32' for s, a, b, c, d in det))

    print("\nEL MECANISMO HACE LO QUE DICE (estructural sobre el catalogo; ERR-71: NO pasa por el emisor)")
    okH = okT = True
    for s in SEM:
        r = BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BAP))
        Q = PATS(s); X = Q[XNEG]
        gk = [tuple(g) for g in (r['tipo_gan_forma'] + r['tipo_gan_var'])]
        grupo = sorted(n for n in Q if all(dir_fuera(g, Q[n], 0) == dir_fuera(g, X, 0) for g in gk))
        okT &= (XNEG in grupo)
        okH &= (HERM not in grupo)
    uno('(D) el referente esta SIEMPRE en su propia direccion conjunta (escritura y lectura coinciden)', okT, t0, tot)
    uno('(E) la HERMANA NUNCA comparte la direccion conjunta del referente (la puerta del mecanismo)', okH, t0, tot)

    print("\nPERILLA MAL ESCRITA (no cae en silencio)")
    lanza('(F) conj_tipo=3 lanza (solo 0, 1 y 2 existen)', lambda: BA.run(1, T=100, dos_tipos=1, conj_tipo=3),
          t0, tot)
    lanza('(G) conj_tipo=True lanza (un bool no es una perilla)',
          lambda: BA.run(1, T=100, dos_tipos=1, conj_tipo=True), t0, tot)
    lanza("(H) conj_tipo='1' lanza", lambda: BA.run(1, T=100, dos_tipos=1, conj_tipo='1'), t0, tot)
    lanza('(I) conj_tipo=1 SIN dos_tipos lanza (no hay tipos que conjugar)',
          lambda: BA.run(1, T=100, conj_tipo=1), t0, tot)
    lanza('(J) conj_tipo=1 CON exige_dir=1 lanza (dos reglas de abstencion no se componen)',
          lambda: BA.run(1, T=100, dos_tipos=1, conj_tipo=1, exige_dir=1), t0, tot)
    lanza('(K) conj_tipo=1 con fam_nvar=0 lanza (no hay tipo VARIANTE)',
          lambda: BA.run(1, T=200, dos_tipos=1, conj_tipo=1, **dict(FAM, fam_nvar=0)), t0, tot)
    lanza('(L) las perillas de A siguen lanzando: dos_tipos=2', lambda: BA.run(1, T=100, dos_tipos=2), t0, tot)
    lanza("(M) las perillas de A siguen lanzando: combina='suma'",
          lambda: BA.run(1, T=100, combina='suma'), t0, tot)

    print("\nCONTROLES QUE DEBEN DIFERIR (sin ellos el arnes pasaria por vacuidad; ERR-64b: >= 2 de 3)")
    caso('(N) BA != A1 (`exige_dir`) en el mundo del receptor (DEBE diferir: es el cambio que se propone)',
         lambda s: BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **A1P)),
         lambda s: BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BAP)),
         t0, debe_diferir=True, tot=tot, salta=NUEVAS_BA)
    caso('(O) BA != A1-d (sin regla de abstencion) (DEBE diferir: la conjuncion de la FORMA hace algo)',
         lambda s: BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **ADP)),
         lambda s: BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BAP)),
         t0, debe_diferir=True, tot=tot, salta=NUEVAS_BA)
    caso('(O2) BA (conj_tipo=1) != BA-v (conj_tipo=2) (DEBE diferir: la variante incompleta vota o no vota)',
         lambda s: BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BVP)),
         lambda s: BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BAP)),
         t0, debe_diferir=True, tot=tot, salta=NUEVAS_BA)
    caso('(P) BA != b5 k=3 (la linea base de familia) (DEBE diferir)',
         lambda s: BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
         lambda s: BA.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BAP)),
         t0, debe_diferir=True, tot=tot, salta=NUEVAS_BA),
    caso('(Q) CANAL != CORTADO con conj_tipo=1 (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'mudo', k_ganadoras=3, **BAP),
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, **BAP),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',) + NUEVAS_BA)
    caso('(R) el patron de la HERMANA != CANAL con conj_tipo=1 (DEBE diferir: es el brazo que decide)',
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, **BAP),
         lambda s: receptor(s, m0[s], 'sen', P=PATS(s)[HERM], k_ganadoras=3, **BAP),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',) + NUEVAS_BA)
    caso('(S) el patron de OTRO TOKEN != CANAL con conj_tipo=1 (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, **BAP),
         lambda s: receptor(s, m0[s], 'sen', P=PATS(s)[OTRO_TK], k_ganadoras=3, **BAP),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',) + NUEVAS_BA)

    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el paquete puede correr." if tot[0] == tot[1] else
                                              "  -> NO se corre nada hasta que sea 100%."))
    sys.exit(0 if tot[0] == tot[1] else 1)
