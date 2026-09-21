"""Arnes de identidad del instrumento del candidato **BA-vm** del nivel 5
(organismo_familias_bavm.py = organismo_familias_bav + la perilla `dentro` CONECTADA). Reglas 2 y 14 de EQUIPO.md.

MISION (primero, siempre): llegar a la AGI por este camino -- un organismo minimo con reglas locales, sin
retropropagacion, que aprende, desaprende, generaliza, sobrevive y se COMUNICA CON REFERENCIA. Hoy, fase 5:
que el mensaje refiera a la FAMILIA Y a la VARIANTE con la MISMA tabla (BAR-T <= 5/20 Y PAR >= 15/20).

  APAGADO (dentro='suma'): == organismo_familias_bav en TODAS sus claves, para CUALQUIER `conj_tipo` (0, 1 y
                       2), cualquier combinacion de las perillas de A, cualquier `k_ganadoras`, cualquier
                       `memoria_variante`, en mundo='AB', en el mundo de familias, con el canal apagado y con
                       el canal encendido en sus TRES modos, y con `baraja_msg`=1.
  RNG NO CONSUMIDO   : lo mismo a T = 120000 (ancla larga).
  CADENA COMPLETA    : apagado == ba, == a1, == b6, == b5, == b4b, == organismo_familias,
                       == organismo_v14 (TRONCO CONGELADO) y, con el relevo ON, == organismo_v15f_on.
  ESTRUCTURA         : las reglas de BA-vm y BA-vM REIMPLEMENTADAS FUERA del organismo coinciden con
                       `W_tabla` estimulo a estimulo (los 32), y con `dentro='suma'` la reimplementacion
                       reproduce la de BA-v.
  PERILLA MAL ESCRITA: lanza (>= 8 casos, incluidas las de BA-v y las nuevas de `dentro`).
  CONTROLES QUE DEBEN DIFERIR (ERR-88, >= 2 de 3 semillas): **BA-vm != BA-v**, **BA-vM != BA-v**,
                       **BA-vm != BA-vM**, **BA-vm-sh != BA-vm**. Si alguno de los tres primeros NO difiere,
                       la perilla esta DESCONECTADA y la serie NO se corre.

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va PRIMERO en sys.path.
Uso:  python experimentos/junta_20260921/B/identidad_familias_bavm.py
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
BAVD = os.path.join(RAIZ, 'experimentos', 'nivel05_familia_variante_BAv')
JBA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'BA')
JA = os.path.join(RAIZ, 'experimentos', 'junta_fase5', 'A')
N12 = os.path.join(RAIZ, 'experimentos', 'nivel12_mundo_familias')
CREA = os.path.join(RAIZ, 'experimentos', 'creacion_A')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [AQUI, BAVD, JBA, JA, N12, CREA, CREB, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_v15f_on as V15FON
import organismo_familias as MF
import organismo_familias_b4b as B4B
import organismo_familias_b5 as B5
import organismo_familias_b6 as B6
import organismo_familias_a1 as A1
import organismo_familias_ba as BA
import organismo_familias_bav as BAV
import organismo_familias_bavm as BVM

T = 20000
T_LARGO = 120000
T_CANAL = 60000
SEM = (1, 2, 3)
SEM_R = 100000
VORAZ = 1.0          # FIJADO en el preregistro del bloque 4b 3.2; los bloques 5, 6 y la junta NO lo tocan
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
        'organismo_familias_a1.py (creador A)': (os.path.join(JA, 'organismo_familias_a1.py'), '8833e1dcfb62f26d'),
        'organismo_familias_ba.py (candidato BA)': (os.path.join(JBA, 'organismo_familias_ba.py'), '1f196ee786b2040d'),
        'organismo_familias_bav.py (BA-v, ORIGEN)': (os.path.join(BAVD, 'organismo_familias_bav.py'), '2dca0a3e239481f0'),
        'construye_familias_bavm.py': (os.path.join(AQUI, 'construye_familias_bavm.py'), None),
        'organismo_familias_bavm.py': (os.path.join(AQUI, 'organismo_familias_bavm.py'), None)}

FAM = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=4, n_neu=0)
MUNDO = dict(mundo='familias', renov=1.0, largo=160, nobj=16, n_exc=2, n_neu=0, costo=0.008, log_cada=250,
             crit_exp=0.5, cambio=10**9, vira=0, fam_val='familia', exc_fija=2, memoria_pares='relevo', reg_b2=1)
KW_E = dict(MUNDO, deriva=5000)
KW_R = dict(MUNDO, deriva=T_CANAL // 3 + 1, reg_b4=1)
XNEG = 'T1v2'
HERM, OTRO_TK = 'T1v0', 'T3v2'

# claves que SOLO existen en cada eslabon (se saltan al comparar hacia atras)
NUEVAS_BAVM = ('canal_lee_herm',)
NUEVAS_BAV = ('baraja_msg', 'baraja_perm')
NUEVAS_BA = ('conj_tipo', 'canal_lee_ref', 'mem_visto')
NUEVAS_A1 = ('dos_tipos', 'k_forma', 'k_var', 'var_cubre', 'pesos_tipo', 'eta_w', 'combina', 'msg_elige',
             'exige_dir', 'dentro', 'n_forma', 'n_mixtas', 'tipo_gan_forma', 'tipo_gan_var', 'w_forma',
             'w_variante', 'canal_mismo_dos', 'canal_gan_tipo')
NUEVAS_B6 = ('memoria_variante', 'memoria_slots', 'memoria_nvar', 'canal_mismo_dir_k')
NUEVAS_B5 = ('k_ganadoras', 'mem_ganadoras', 'canal_gan_k_pre', 'canal_gan_k_post', 'canal_mismo_bin_k')
NUEVAS_B4B = ('voraz', 'par_herm', 'par_fijo')

# las lecturas que se comparan
A1P = dict(dos_tipos=1, combina='min', exige_dir=1, msg_elige=0)                 # A1, el candidato del creador A
BAP = dict(dos_tipos=1, combina='min', exige_dir=0, msg_elige=0, conj_tipo=1)    # BA
BVP = dict(dos_tipos=1, combina='min', exige_dir=0, msg_elige=0, conj_tipo=2)    # BA-v: el pareado de hoy
BVMP = dict(BVP, dentro='minv')                                                   # **BA-vm: EL CANDIDATO**
BVMM = dict(BVP, dentro='min')                                                   # **BA-vM: LA ABLACION**
ADP = dict(dos_tipos=1, combina='min', exige_dir=0, msg_elige=0)                 # A1-d, sin regla de abstencion
PREFIJO_CANAL = ('canal_t_msg', 'canal_t_entrega', 'canal_gan_pre', 'canal_bin', 'canal_gan_k_pre',
                 'canal_mismo_bin', 'canal_mismo_dir_k', 'canal_mismo_dos', 'canal_gan_tipo')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def compara(a, b, salta=()):
    return [k for k in a if k not in salta and N(a[k]) != N(b.get(k))] + \
           [k for k in a if k not in b and k not in salta]


def caso(etiq, fa, fb, t0, debe_diferir=False, semillas=SEM, tot=None, salta=(), solo=None):
    ok, detalle = 0, ''
    for s in semillas:
        A, B = fa(s), fb(s)
        if solo is not None:
            A, B = {k: A[k] for k in solo}, {k: B[k] for k in solo}
        dif = compara(A, B, salta)
        ok += int((not dif) != debe_diferir)
        if dif and not detalle:
            detalle = ' ' + str(dif[:5])
    need = (len(semillas) - 1 if (debe_diferir and len(semillas) >= 3) else len(semillas))
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    est = marca if ok >= need else ('FALLA' + detalle)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:84s} {ok}/{len(semillas)} {est}", flush=True)
    if tot is not None:
        tot[0] += int(ok >= need); tot[1] += 1
    return ok >= need


def uno(etiq, ok, t0, tot):
    print(f"  [{time.time()-t0:6.1f}s] {etiq:84s} {'1/1 OK' if ok else '0/1 FALLA'}", flush=True)
    tot[0] += int(bool(ok)); tot[1] += 1
    return bool(ok)


def lanza(etiq, f, t0, tot):
    try:
        f(); ok = False
    except (ValueError, TypeError, IndexError):
        ok = True
    except Exception:
        ok = False
    print(f"  [{time.time()-t0:6.1f}s] {etiq:84s} {'1/1 LANZA (como debe)' if ok else '0/1 NO LANZA'}", flush=True)
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


def suma_fuera(gs, P, tabla, visto, mv, modo='suma', tv=0):
    """La lectura DENTRO de un tipo, REIMPLEMENTADA FUERA del organismo: suma, o `k*min` (BA-vm/BA-vM)."""
    s, n, m = 0.0, 0, 0.0
    for par in gs:
        c = dir_fuera(tuple(par), P, mv)
        g = PARES12.index(tuple(par))
        if visto[g][c]:
            x = float(tabla[g][c]); s += x; n += 1; m = (x if n == 1 else min(m, x))
    if n and (modo == 'min' or (modo == 'minv' and tv)):
        return float(n) * m, n
    return s, n


def lee_fuera(regla, gf, gv, P, tabla, visto, mv, modo='suma'):
    """Las reglas de lectura, FUERA del organismo y SOBRE LA MISMA TABLA. Devuelve (valor, habla)."""
    sf, nf = suma_fuera(gf, P, tabla, visto, mv, modo, 0)
    sv, nv = suma_fuera(gv, P, tabla, visto, mv, modo, 1)
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
    e = (BVM.run(s, T=Tc, fam_seed=s, canal={'modo': 'emite'}, voraz=voraz, k_ganadoras=1, memoria_variante=0,
                 **KW_E)['canal_emitido'] or {}).get(ref)
    return None if e is None else dict(t=int(e[0]), ref=e[1], P=list(e[2]), R=float(e[3]))


def receptor(s, msg, modo='sen', Tc=T_CANAL, P=None, par_herm=None, mod=BVM, **kw):
    c = dict(modo=modo, t=msg['t'], ref=msg['ref'], P=(msg['P'] if P is None else P), R=msg['R'])
    return mod.run(s + SEM_R, T=Tc, fam_seed=s, canal=c, par_herm=par_herm, **dict(KW_R, **kw))


if __name__ == '__main__':
    t0 = time.time()
    malo = False
    for nom, (p, esp) in SHAS.items():
        s = h16(p)
        aviso = '' if esp is None else ('  OK' if s == esp else f'  *** ESPERADO {esp}')
        malo = malo or (esp is not None and s != esp)
        print(f"  sha {nom:50s} {s}{aviso}")
    if malo:
        raise SystemExit("Un origen cambio. Reconstruir por anclas antes de seguir.")
    print(f"  T = {T} (ancla del rng: {T_LARGO}; canal: {T_CANAL}), semillas {SEM}, UN proceso\n")

    tot = [0, 0]
    m0 = {s: mensaje(s) for s in SEM}
    SEM_MSG = tuple(s for s in SEM if m0[s] is not None)
    print(f"  emisores con mensaje (-): {len(SEM_MSG)}/{len(SEM)} -> {SEM_MSG}\n")

    print("APAGADO (dentro='suma'): organismo_familias_bavm == organismo_familias_bav (EL ORIGEN), todo encendido")
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
                 (lambda x, kk, m: lambda s: BAV.run(s, T=T, k_ganadoras=kk, memoria_variante=m, **x))(kw, k, mv),
                 (lambda x, kk, m: lambda s: BVM.run(s, T=T, k_ganadoras=kk, memoria_variante=m,
                                                     dentro='suma', **x))(kw, k, mv),
                 t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BAVM)
    print("  ...y con las SEIS configuraciones de LECTURA, INCLUIDO conj_tipo=2 (el pareado de hoy)")
    for etiq, p in [('(a2) A1 (dos tipos + min + exige_dir + msg_elige=0)', A1P),
                    ('(a3) A1-d (dos tipos + min, sin exige_dir)', ADP),
                    ('(a4) BA (conj_tipo=1)', BAP),
                    ('(a5) **BA-v (conj_tipo=2)**', BVP),
                    ('(a6) BA-v con combina=media', dict(BVP, combina='media')),
                    ('(a7) BA-v con el mensaje que SI re-elige (msg_elige=1)', dict(BVP, msg_elige=1))]:
        caso(etiq, (lambda x: lambda s: BAV.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **x)))(p),
             (lambda x: lambda s: BVM.run(s, T=T, k_ganadoras=3, dentro='suma',
                                          **dict(KW_R, fam_seed=s, **x)))(p),
             t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BAVM)
    print("  ...y con el CANAL ENCENDIDO en sus tres modos, y con el CONTROL `baraja_msg`=1 (el canal NO se toca)")
    for etiq, modo in [('(i) canal sen', 'sen'), ('(j) canal inm', 'inm'), ('(k) canal mudo', 'mudo')]:
        caso(etiq + ', BA-v encendido',
             (lambda mo: lambda s: receptor(s, m0[s], mo, mod=BAV, k_ganadoras=3, **BVP))(modo),
             (lambda mo: lambda s: receptor(s, m0[s], mo, mod=BVM, k_ganadoras=3, dentro='suma', **BVP))(modo),
             t0, semillas=SEM_MSG[:2], tot=tot, salta=NUEVAS_BAVM)
    caso('(k2) canal sen + baraja_msg=1 (la memoria BARAJADA de BA-v sigue bit a bit)',
         lambda s: receptor(s, m0[s], 'sen', mod=BAV, k_ganadoras=3, baraja_msg=1, **BVP),
         lambda s: receptor(s, m0[s], 'sen', mod=BVM, k_ganadoras=3, baraja_msg=1, dentro='suma', **BVP),
         t0, semillas=SEM_MSG[:2], tot=tot, salta=NUEVAS_BAVM)

    print("\nRNG NO CONSUMIDO por la perilla apagada (ancla larga)")
    caso(f'(l) mundo=AB a T = {T_LARGO}, relevo ENCENDIDO, k = 3',
         lambda s: BAV.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=3),
         lambda s: BVM.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=3, dentro='suma'),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BAVM)
    caso(f'(l2) mundo=AB a T = {T_LARGO}, BA-v ENCENDIDO (conj_tipo=2), k = 3',
         lambda s: BAV.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=3, **BVP),
         lambda s: BVM.run(s, T=T_LARGO, memoria_pares='relevo', k_ganadoras=3, dentro='suma', **BVP),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BAVM)

    print("\nCADENA COMPLETA (se comprueba hasta el TRONCO, no se supone)")
    caso('(m0) apagado == organismo_familias_ba (el origen de BA-v)',
         lambda s: BA.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s)),
         lambda s: BVM.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BAVM + NUEVAS_BAV)
    caso('(m) apagado == organismo_familias_a1 (el origen de BA)',
         lambda s: A1.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s)),
         lambda s: BVM.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BAVM + NUEVAS_BAV + NUEVAS_BA)
    caso('(n) apagado == organismo_familias_b6 (mundo del receptor, k = 3, sufijo ON)',
         lambda s: B6.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s)),
         lambda s: BVM.run(s, T=T, k_ganadoras=3, memoria_variante=1, **dict(KW_R, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BAVM + NUEVAS_BAV + NUEVAS_BA + NUEVAS_A1)
    caso('(o) apagado == organismo_familias_b5 (mundo del bloque 4, k = 3)',
         lambda s: B5.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
         lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot, salta=NUEVAS_BAVM + NUEVAS_BAV + NUEVAS_BA + NUEVAS_A1 + NUEVAS_B6)
    caso('(p) apagado == organismo_familias_b4b (mundo del bloque 4, emisor voraz)',
         lambda s: B4B.run(s, T=T, voraz=VORAZ, **dict(KW_E, fam_seed=s)),
         lambda s: BVM.run(s, T=T, voraz=VORAZ, **dict(KW_E, fam_seed=s)),
         t0, semillas=SEM[:2], tot=tot,
         salta=NUEVAS_BAVM + NUEVAS_BAV + NUEVAS_BA + NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5)
    caso('(q) apagado + mundo=AB == organismo_v14 (TRONCO CONGELADO)', lambda s: V14.run(s, T=T),
         lambda s: BVM.run(s, T=T), t0, tot=tot,
         salta=NUEVAS_BAVM + NUEVAS_BAV + NUEVAS_BA + NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso('(r) relevo ON + mundo=AB == organismo_v15f_on', lambda s: V15FON.run(s, T=T),
         lambda s: BVM.run(s, T=T, memoria_pares='relevo'), t0, tot=tot,
         salta=NUEVAS_BAVM + NUEVAS_BAV + NUEVAS_BA + NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)
    caso('(s) apagado + mundo=familias == organismo_familias (bloque 1)', lambda s: MF.run(s, T=T, **FAM),
         lambda s: BVM.run(s, T=T, **FAM), t0, semillas=SEM[:2], tot=tot,
         salta=NUEVAS_BAVM + NUEVAS_BAV + NUEVAS_BA + NUEVAS_A1 + NUEVAS_B6 + NUEVAS_B5 + NUEVAS_B4B)

    print("\nESTRUCTURA: las reglas REIMPLEMENTADAS FUERA, sobre LA MISMA tabla (los 32 estimulos)")
    okS = okM = okV = okP2 = True
    det = []
    for s in SEM:
        Q = PATS(s)
        fila = [s]
        for modo, p, flag in (('suma', BVP, 'S'), ('minv', BVMP, 'M'), ('min', BVMM, 'V')):
            r = BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **p))
            tab, vis = r['mem_tabla'], r['mem_visto']
            gf, gv = r['tipo_gan_forma'], r['tipo_gan_var']
            if modo == 'suma':
                okP2 &= (r['n_forma'] == N_FORMA and r['n_mixtas'] == N_MIXTAS
                         and r['n_forma'] + r['n_mixtas'] + len(PURA_F) == NP
                         and len(gf) == 3 and all(PARES12.index(tuple(g)) in FORMA_F for g in gf)
                         and len(gv) == NVAR and all(PARES12.index(tuple(g)) in MIXTA_F for g in gv))
            bien = True
            nhab = 0
            for n in Q:
                v, h = lee_fuera('BAv', gf, gv, Q[n], tab, vis, 0, modo)
                dentro = r['W_tabla'].get(n)
                bien &= ((dentro is None and not h) or (h and dentro is not None and abs(dentro - round(v, 3)) < 1e-9))
                nhab += int(h)
            if modo == 'suma':
                okS &= bien
            elif modo == 'minv':
                okM &= bien
            else:
                okV &= bien
            fila.append(nhab)
        det.append(tuple(fila))
    uno('(A) la particion y las ganadoras siguen intactas (36 forma + 27 mixtas; 1 mixta por px de variante)',
        okP2, t0, tot)
    uno("(B) dentro='suma': la reimplementacion FUERA coincide con `W_tabla` en los 32 estimulos", okS, t0, tot)
    uno("(C) **dentro='minv' (BA-vm): la reimplementacion FUERA coincide con `W_tabla` en los 32**", okM, t0, tot)
    uno("(D) **dentro='min' (BA-vM): la reimplementacion FUERA coincide con `W_tabla` en los 32**", okV, t0, tot)
    print('        ' + '  '.join(f's{s}: habla suma {a}/32, minv {b}/32, min {c}/32' for s, a, b, c in det))

    print("\nEL MECANISMO HACE LO QUE DICE (estructural sobre el catalogo; ERR-71: NO pasa por el emisor)")
    okH = okT = True
    for s in SEM:
        r = BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BVMP))
        Q = PATS(s); X = Q[XNEG]
        gk = [tuple(g) for g in (r['tipo_gan_forma'] + r['tipo_gan_var'])]
        grupo = sorted(n for n in Q if all(dir_fuera(g, Q[n], 0) == dir_fuera(g, X, 0) for g in gk))
        okT &= (XNEG in grupo)
        okH &= (HERM not in grupo)
    uno('(E) el referente esta SIEMPRE en su propia direccion conjunta (escritura y lectura coinciden)', okT, t0, tot)
    uno('(F) la HERMANA NUNCA comparte la direccion conjunta del referente (la puerta del mecanismo)', okH, t0, tot)

    print("\nPERILLA MAL ESCRITA (no cae en silencio)")
    lanza("(G) dentro='mini' lanza (solo 'suma', 'minv' y 'min' existen)",
          lambda: BVM.run(1, T=100, dos_tipos=1, conj_tipo=2, dentro='mini'), t0, tot)
    lanza("(H) dentro='MIN' lanza (la perilla NO es tolerante a mayusculas)",
          lambda: BVM.run(1, T=100, dos_tipos=1, conj_tipo=2, dentro='MIN'), t0, tot)
    lanza('(I) dentro=0 lanza (un entero no es una perilla de texto)',
          lambda: BVM.run(1, T=100, dos_tipos=1, conj_tipo=2, dentro=0), t0, tot)
    lanza('(J) dentro=None lanza', lambda: BVM.run(1, T=100, dos_tipos=1, conj_tipo=2, dentro=None), t0, tot)
    lanza("(K) dentro='minv' SIN dos_tipos lanza (no hay tipo VARIANTE en el que ser pesimista)",
          lambda: BVM.run(1, T=100, dentro='minv'), t0, tot)
    lanza("(L) dentro='min' SIN dos_tipos lanza", lambda: BVM.run(1, T=100, dentro='min'), t0, tot)
    lanza('(M) baraja_msg=2 sigue lanzando',
          lambda: BVM.run(1, T=100, dos_tipos=1, conj_tipo=2, baraja_msg=2), t0, tot)
    lanza('(N) conj_tipo=3 sigue lanzando', lambda: BVM.run(1, T=100, dos_tipos=1, conj_tipo=3), t0, tot)
    lanza('(O) conj_tipo=2 CON exige_dir=1 sigue lanzando',
          lambda: BVM.run(1, T=100, dos_tipos=1, conj_tipo=2, exige_dir=1), t0, tot)
    lanza("(P) combina='suma' sigue lanzando", lambda: BVM.run(1, T=100, combina='suma'), t0, tot)

    print("\nCONTROLES QUE DEBEN DIFERIR (ERR-88: sin ellos el arnes pasaria por vacuidad; >= 2 de 3)")
    okc = []
    okc.append(caso('(Q) **BA-vm != BA-v (LA PERILLA ESTA CONECTADA; si no difiere, NO se corre la serie)**',
                    lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BVP)),
                    lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BVMP)),
                    t0, debe_diferir=True, tot=tot, salta=NUEVAS_BAVM))
    okc.append(caso('(R) **BA-vM != BA-v (la ABLACION tambien esta conectada)**',
                    lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BVP)),
                    lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BVMM)),
                    t0, debe_diferir=True, tot=tot, salta=NUEVAS_BAVM))
    okc.append(caso('(S) **BA-vm != BA-vM (candidato y ablacion NO son la misma regla)**',
                    lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BVMP)),
                    lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BVMM)),
                    t0, debe_diferir=True, tot=tot, salta=NUEVAS_BAVM))
    caso('(T) **BA-vm-sh != BA-vm (la MEMORIA BARAJADA: el control del criterio nuevo)**',
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, **BVMP),
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, baraja_msg=1, **BVMP),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=NUEVAS_BAVM + NUEVAS_BAV)
    caso('(U) BA-vm != A1 (`exige_dir`) en el mundo del receptor (DEBE diferir)',
         lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **A1P)),
         lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BVMP)),
         t0, debe_diferir=True, tot=tot, salta=NUEVAS_BAVM)
    caso('(V) BA-vm != b5 k=3 (la linea base de familia) (DEBE diferir)',
         lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s)),
         lambda s: BVM.run(s, T=T, k_ganadoras=3, **dict(KW_R, fam_seed=s, **BVMP)),
         t0, debe_diferir=True, tot=tot, salta=NUEVAS_BAVM)
    caso('(W) CANAL != CORTADO con BA-vm (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'mudo', k_ganadoras=3, **BVMP),
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, **BVMP),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',) + NUEVAS_BAVM)
    caso('(X) el patron de la HERMANA != CANAL con BA-vm (el brazo que decide la variante)',
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, **BVMP),
         lambda s: receptor(s, m0[s], 'sen', P=PATS(s)[HERM], k_ganadoras=3, **BVMP),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',) + NUEVAS_BAVM)
    caso('(Y) el patron de OTRO TOKEN != CANAL con BA-vm (DEBE diferir)',
         lambda s: receptor(s, m0[s], 'sen', k_ganadoras=3, **BVMP),
         lambda s: receptor(s, m0[s], 'sen', P=PATS(s)[OTRO_TK], k_ganadoras=3, **BVMP),
         t0, debe_diferir=True, semillas=SEM_MSG, tot=tot, salta=('canal',) + NUEVAS_BAVM)

    print("\nDIAGNOSTICO NUEVO `canal_lee_herm` (no decide nada; solo tiene que EXISTIR y ser coherente)")
    r = receptor(SEM_MSG[0], m0[SEM_MSG[0]], 'sen', k_ganadoras=3, **BVMP)
    lh = r['canal_lee_herm']
    uno('(Z) `canal_lee_herm` existe, incluye a la hermana y tiene 4 campos por entrada',
        bool(lh) and HERM in lh and all(len(v) == 4 for v in lh.values()), t0, tot)
    print('        canal_lee_ref %s   canal_lee_herm %s' % (r['canal_lee_ref'], lh))

    if not all(okc):
        print("\n*** UN CONTROL QUE DEBE DIFERIR NO DIFIERE: la perilla esta DESCONECTADA (ERR-88). "
              "LA SERIE NO SE CORRE.")
    print(f"\nIDENTIDAD {tot[0]}/{tot[1]}" + ("  -> el paquete puede correr." if tot[0] == tot[1] else
                                              "  -> NO se corre nada hasta que sea 100%."))
    sys.exit(0 if tot[0] == tot[1] else 1)
