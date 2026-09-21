"""ARNES DE IDENTIDAD del paquete dE5 (candidato a v15 bajo el CRITERIO DE TRONCO v2).
UN proceso, sin Pool (regla 3 de EQUIPO.md). Se corre ANTES de mirar cualquier numero del candidato.

IDENTIDADES (deben salir IDENTICAS, bit a bit, clave por clave):
  I1  organismo_v15_dE5(vivo=0, n_nec=1, eta_pred=0, k_sorp=0) == organismo/organismo_v142.py  (TRONCO v14.2,
      17528d767fcebaf6) en TODAS las claves de v14.2 — los 7 escenarios de bateria_v142.ETAPAS x 3 semillas.
  I2  organismo_v15_dE5(desambiguar=0, eta_pred=0, k_sorp=0) == organismo_vivo_rep2.py (96feb4918dc5d694) en TODAS
      sus claves — brazos VIVO y CUELLO_MIN de corre_vivo_rep2, el BASE del bloque de la sal y el VIVO de mini_vivo.
  I3  organismo_v15_dE5g(eta_pred=0, k_sorp=0) == organismo/organismo_v142g.py (9e5f566cd6a7a4d2) — mundo de regla
      (px0, azar) y mundo AB, con los kwargs EXACTOS de la entrada del tronco en INSTRUMENTOS (regla 14).
  I4  B-5 es INERTE en los mundos del tronco (R nunca es 0): desambiguar=1 == desambiguar=0 en los 7 escenarios.
      (Prediccion de v14.2, no exigencia: si fallara, el candidato no seria v14.2 + dE.)
  I5  EL PREDICTOR SOLO MIDE: eta_pred=0.03 con k_sorp=0 == apagado por completo (no consume rng, no realimenta).
  I6  LAS DOS IMPLEMENTACIONES DEL dE COINCIDEN: organismo_v15_dE5g(mundo='AB', kwargs del tronco, DOSIS ON) ==
      organismo_v15_dE5(vivo=0, n_nec=1, DOSIS ON) en las claves comunes. Es lo que autoriza a usar el modulo de
      mundo de regla para T-B con la misma dosis.
  I7  invertir_vivo_en > T es INERTE (la perilla de T-C no contamina las demas puertas).

CONTROLES QUE DEBEN FALLAR (si alguno sale IDENTICO, el arnes no mide nada y el runner se para):
  M1  la DOSIS ENCENDIDA (k_sorp=5) cambia la conducta frente a apagada, en el mundo de la recuperacion.
  M2  DOSIS 10 != DOSIS 5 (la dosis es la perilla preregistrada; 10 ya fue descartada por G1 0.750).
  M3  desambiguar=1 != desambiguar=0 en una semilla ALIAS del bloque de la sal (B-5 SI actua donde hay R == 0).
  M4  invertir_vivo_en = T/2 SI cambia la conducta (la reversion del mundo vivo no es un adorno).
  M5  paja del comparador: dos semillas distintas del mismo montaje NO son iguales.
  M6  en el mundo de REGLA, la dosis encendida != apagada (el instrumento de T-B distingue los dos brazos).
  M7  el CONTROL DE CANTIDAD (sesgo_fijo) SI empuja la boca: si fuera inerte, el control de T-G no controlaria nada.

    python experimentos/tronco_v15_dE5/identidad_v15_dE5.py [T]      (T por defecto 20000)
"""
import sys, os, json, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
NIV11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
CREB = os.path.join(RAIZ, 'experimentos', 'creacion_B')
sys.path[:0] = [ORG, NIV11, CREB, AQUI]

import organismo_v15_dE5 as D5
import organismo_v15_dE5g as D5G
import organismo_v142 as V142
import organismo_v142g as V142G
import organismo_vivo_rep2 as REP2
import bateria_v142 as BAT
import corre_vivo_rep2 as CR2
import corre_sal as CS
import mini_vivo as MV

T = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20000

OFF = dict(eta_pred=0.0, k_sorp=0.0)
ON = dict(eta_pred=0.03, ema_pred=0.05, k_sorp=5.0)
ON10 = dict(eta_pred=0.03, ema_pred=0.05, k_sorp=10.0)
# claves NUEVAS del candidato (solo lectura); no existen en el origen contra el que se compara
NUEV_V142 = {'t_ext_B', 'mord_post', 'deaths_post', 'sbarE', 'invertir_vivo_en', 'sesgo_fijo', 'sesgo_q', 'enc_q'}
NUEV_REP2 = NUEV_V142 | {'desambiguar', 'des_splits', 'des_t'}
NUEV_G = {'sbarE', 'sesgo_fijo', 'sesgo_q', 'enc_q'}
# kwargs EXACTOS de la entrada del tronco en bateria_generaliza_v142.INSTRUMENTOS['organismo_v142'] (regla 14)
KW142 = dict(eta_s=0.15, clip_s=10.0, puerta=3, mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05,
             puerta_pat=5, pat_shuf=0, pat_min=1)


def N(x):
    return json.dumps(x, sort_keys=True, default=str)


def dif(ref, cand, nuevas, ignora=frozenset()):
    """Devuelve la lista de claves que NO coinciden. Exige: todas las de `ref` identicas, y que las claves de mas
    del candidato sean EXACTAMENTE las declaradas en `nuevas`. `ignora`: ECOS del propio argumento (p. ej. la clave
    `desambiguar`, que solo devuelve el valor que se le paso): no son conducta y no se comparan."""
    d = [k for k in ref if k not in ignora and (k not in cand or N(ref[k]) != N(cand[k]))]
    extra = set(cand) - set(ref)
    if extra != (nuevas & set(cand)) or not extra <= nuevas:
        d.append(f'CLAVES EXTRA {sorted(extra - nuevas)}')
    return d


OK = [0]; NO = [0]; DET = []


def chk(nombre, ref, cand, nuevas=frozenset(), ignora=frozenset()):
    d = dif(ref, cand, nuevas, ignora)
    if d:
        NO[0] += 1; DET.append(f'    *** {nombre}: DIFIERE en {d[:6]}')
    else:
        OK[0] += 1
    return not d


MOK = [0]; MNO = [0]


def must_fail(nombre, a, b, claves=('W', 'mord', 'deaths', 'splits')):
    """Control que DEBE fallar: a y b tienen que diferir en al menos una de `claves`."""
    igual = all(N(a.get(k)) == N(b.get(k)) for k in claves)
    if igual:
        MNO[0] += 1; DET.append(f'    *** CONTROL {nombre} SALIO IDENTICO: el arnes no mide nada aqui.')
    else:
        MOK[0] += 1
    return not igual


if __name__ == '__main__':
    t0 = time.time()
    print(f'ARNES dE5 — T={T}. candidato organismo_v15_dE5 / organismo_v15_dE5g')
    SEM = [1, 2, 3]

    # ---------------- I1: con vivo=0, n_nec=1 y la dosis apagada es el TRONCO v14.2, bit a bit
    print(f"--- I1: organismo_v15_dE5(vivo=0,n_nec=1,dosis OFF) == organismo_v142 (TRONCO v14.2), {len(BAT.ETAPAS)} escenarios x {len(SEM)} semillas")
    for e, kw in BAT.ETAPAS.items():
        for s in SEM:
            chk(f'I1 {e} s{s}', V142.run(s, T=T, **kw), D5.run(s, T=T, **kw, **OFF), NUEV_V142)

    # ---------------- I2: con desambiguar=0 y la dosis apagada es organismo_vivo_rep2, bit a bit
    print("--- I2: organismo_v15_dE5(desambiguar=0,dosis OFF) == organismo_vivo_rep2 (mundo vivo, sal, mini_vivo)")
    MONT = [(f'rep2 {b}', CR2.BRAZOS[b]) for b in ('VIVO', 'CUELLO_MIN')]
    MONT += [('sal BASE', dict(CS.BASE)), ('mini VIVO', dict(MV.BRAZOS['VIVO']))]
    for nom, kw in MONT:
        for s in (CS.ALIAS[0], CS.LIMPIAS[0]):
            chk(f'I2 {nom} s{s}', REP2.run(s, T=T, **kw), D5.run(s, T=T, **kw, desambiguar=0, **OFF), NUEV_REP2)

    # ---------------- I3: el instrumento de mundo de regla, con los kwargs de INSTRUMENTOS (regla 14)
    print("--- I3: organismo_v15_dE5g(dosis OFF) == organismo_v142g (mundo de regla px0/azar y mundo AB)")
    for regla in ('px0', 'azar'):
        for s in SEM[:2]:
            chk(f'I3 regla {regla} s{s}', V142G.run(s, T=T, mundo='regla', regla=regla, **KW142),
                D5G.run(s, T=T, mundo='regla', regla=regla, **KW142, **OFF), NUEV_G)
    for s in SEM[:2]:
        chk(f'I3 AB s{s}', V142G.run(s, T=T, mundo='AB', **KW142), D5G.run(s, T=T, mundo='AB', **KW142, **OFF), NUEV_G)

    # ---------------- I4: B-5 es inerte en los mundos del tronco (R nunca es 0)
    print("--- I4: B-5 INERTE en los mundos del tronco: desambiguar=1 == desambiguar=0 (prediccion de v14.2)")
    for e, kw in BAT.ETAPAS.items():
        s = SEM[0]
        a = D5.run(s, T=T, **kw, desambiguar=0, **OFF)
        chk(f'I4 {e} s{s}', a, D5.run(s, T=T, **kw, desambiguar=1, **OFF), ignora={'desambiguar'})

    # ---------------- I5: el predictor SOLO MIDE (eta_pred on, k_sorp=0) == apagado
    print("--- I5: el predictor SOLO MIDE (eta_pred=0.03, k_sorp=0) == apagado por completo")
    for e in ('E1', 'E2', 'E2I'):
        for s in SEM[:2]:
            a = D5.run(s, T=T, **BAT.ETAPAS[e], **OFF)
            b = D5.run(s, T=T, **BAT.ETAPAS[e], eta_pred=0.03, ema_pred=0.05, k_sorp=0.0)
            d = [k for k in a if k != 'sbarE' and N(a[k]) != N(b[k])]
            if d: NO[0] += 1; DET.append(f'    *** I5 {e} s{s}: DIFIERE en {d[:6]}')
            else: OK[0] += 1

    # ---------------- I6: las DOS implementaciones del dE coinciden (vectorial n_nec=1 vs (1,6)/(1,NKMAX))
    print("--- I6: organismo_v15_dE5g(mundo='AB', DOSIS ON) == organismo_v15_dE5(vivo=0,n_nec=1, DOSIS ON) en claves comunes")
    for s in SEM:
        a = D5.run(s, T=T, **ON)
        b = D5G.run(s, T=T, mundo='AB', **KW142, **ON)
        comunes = [k for k in ('W', 'mord', 'vis', 'deaths', 'splits', 'celdas', 'comp', 'W_lenta', 'Wps', 'Wns', 'n_cod', 'sbarE', 'sesgo_q', 'enc_q', 'err_max', 'split_t')]
        d = [k for k in comunes if N(a.get(k)) != N(b.get(k))]
        if d: NO[0] += 1; DET.append(f'    *** I6 s{s}: DIFIERE en {d}')
        else: OK[0] += 1

    # ---------------- I7: invertir_vivo_en > T es inerte
    print("--- I7: invertir_vivo_en > T es INERTE")
    for s in (CS.ALIAS[0], CS.ALIAS[1]):
        a = D5.run(s, T=T, **dict(CS.BASE), **OFF)
        chk(f'I7 s{s}', a, D5.run(s, T=T, **dict(CS.BASE), invertir_vivo_en=T + 10, **OFF), ignora={'invertir_vivo_en'})

    # ---------------- CONTROLES QUE DEBEN FALLAR
    print("--- CONTROLES QUE DEBEN FALLAR (M1..M7)")
    s = SEM[0]
    inv = dict(invertir_en=T // 2)
    a_off = D5.run(s, T=T, **inv, **OFF)
    a_on = D5.run(s, T=T, **inv, **ON)
    a_10 = D5.run(s, T=T, **inv, **ON10)
    must_fail('M1 dosis ON != OFF (mundo de la recuperacion)', a_off, a_on)
    must_fail('M2 dosis 10 != dosis 5', a_on, a_10)
    sa = CS.ALIAS[0]
    must_fail('M3 desambiguar=1 != desambiguar=0 (semilla ALIAS)',
              D5.run(sa, T=T, **dict(CS.BASE), desambiguar=0, **OFF),
              D5.run(sa, T=T, **dict(CS.BASE), desambiguar=1, **OFF), claves=('W_nec', 'mord', 'deaths', 'splits'))
    must_fail('M4 invertir_vivo_en = T/2 SI cambia',
              D5.run(sa, T=T, **dict(MV.BRAZOS['VIVO']), **OFF),
              D5.run(sa, T=T, **dict(MV.BRAZOS['VIVO']), invertir_vivo_en=T // 2, **OFF), claves=('W_nec', 'mord', 'deaths'))
    must_fail('M5 paja del comparador (semillas distintas)', a_off, D5.run(s + 1, T=T, **inv, **OFF))
    must_fail('M6 mundo de regla: dosis ON != OFF',
              D5G.run(SEM[0], T=T, mundo='regla', regla='px0', **KW142, **OFF),
              D5G.run(SEM[0], T=T, mundo='regla', regla='px0', **KW142, **ON), claves=('W_apriori', 'mord', 'deaths'))
    must_fail('M7 sesgo_fijo (control de CANTIDAD) SI empuja la boca', a_off,
              D5.run(s, T=T, **inv, **OFF, sesgo_fijo=0.30))

    for l in DET:
        print(l)
    tot_ok = OK[0] + MOK[0]; tot = OK[0] + NO[0] + MOK[0] + MNO[0]
    print(f'IDENTIDADES {OK[0]}/{OK[0]+NO[0]}   CONTROLES QUE FALLAN COMO DEBEN {MOK[0]}/{MOK[0]+MNO[0]}   ({time.time()-t0:.1f}s)')
    print(f'ARNES TOTAL: {tot_ok}/{tot}')
    sys.exit(0 if tot_ok == tot else 1)
