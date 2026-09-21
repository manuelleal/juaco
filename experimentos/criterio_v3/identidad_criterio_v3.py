"""ARNES DE IDENTIDAD del paquete A-CAL (calibracion del CRITERIO DE TRONCO v3, ERR-91).
UN proceso, sin Pool (regla 3 de EQUIPO.md). Se corre ANTES de mirar cualquier numero.

IDENTIDADES (deben salir IDENTICAS, bit a bit, clave por clave):
  I1  organismo_v3cal(vivo=0, n_nec=1, placebo=0) == organismo/organismo_v142.py (TRONCO v14.2, 17528d767fcebaf6)
      en TODAS las claves de v14.2 — los 7 escenarios de bateria_v142.ETAPAS x 3 semillas.
  I2  organismo_v3cal(desambiguar=0, placebo=0) == organismo_vivo_rep2.py (96feb4918dc5d694) en TODAS sus claves —
      brazos VIVO y CUELLO_MIN de corre_vivo_rep2 y el VIVO de mini_vivo, x 2 semillas.
  I3  B-5 es INERTE en los mundos del tronco (R nunca es 0): desambiguar=1 == desambiguar=0 en los 7 escenarios.
      (Prediccion de v14.2, no exigencia.)
  I4  placebo=0 == NO pasar la perilla (el defecto es el tronco), en 3 montajes del mundo vivo.
  I5  invertir_vivo_en > T es INERTE (la perilla de T-C ii no contamina T-A).
  I6  EL PLACEBO NO CAMBIA LA LEY, solo la fase del generador: organismo_v3cal(semilla s, placebo=1) NO es igual a
      (s, placebo=0) — eso es M1 — pero el CONJUNTO de 6 semillas con placebo=1 cae DENTRO del rango de las mismas
      6 semillas con placebo=0 en muertes (control de vacuidad debil, se REPORTA, no es puerta).

CONTROLES QUE DEBEN FALLAR (si alguno sale IDENTICO, el arnes no mide nada y el runner se para):
  M1  placebo=1 != placebo=0 en la trayectoria (mundo vivo, brazo VIVO): LA PERILLA HACE ALGO.
  M2  placebo=1 != placebo=2 (el numero de sorteos importa: son dos desplazamientos distintos del flujo).
  M3  placebo=1 != placebo=0 tambien en el mundo del examen (vivo=0, n_nec=1).
  M4  el brazo PEOR (coste de vida mayor) SI cambia la conducta: costo=costo_a=0.00125 != 0.001.
  M5  invertir_vivo_en = T/2 SI cambia la conducta (la reversion del mundo vivo no es un adorno).
  M6  paja del comparador: dos semillas distintas del mismo montaje NO son iguales.
  M7  desambiguar=1 != desambiguar=0 en una semilla ALIAS del bloque de la sal (B-5 SI actua donde hay R == 0).

    python experimentos/criterio_v3/identidad_criterio_v3.py [T]      (T por defecto 20000)
"""
import sys, os, json, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
ORG = os.path.join(RAIZ, 'organismo')
NIV11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
sys.path[:0] = [ORG, NIV11, AQUI]

import organismo_v3cal as CAL
import organismo_v142 as V142
import organismo_vivo_rep2 as REP2
import bateria_v142 as BAT
import corre_vivo_rep2 as CR2
import corre_sal as CS
import mini_vivo as MV

T = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 20000

# claves NUEVAS del paquete (ecos del argumento; no existen en el origen contra el que se compara)
NUEV_V142 = {'invertir_vivo_en', 'placebo'}
NUEV_REP2 = NUEV_V142 | {'desambiguar', 'des_splits', 'des_t'}


def N(x):
    return json.dumps(x, sort_keys=True, default=str)


def dif(ref, cand, nuevas, ignora=frozenset()):
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
    igual = all(N(a.get(k)) == N(b.get(k)) for k in claves)
    if igual:
        MNO[0] += 1; DET.append(f'    *** CONTROL {nombre} SALIO IDENTICO: el arnes no mide nada aqui.')
    else:
        MOK[0] += 1
    return not igual


if __name__ == '__main__':
    t0 = time.time()
    print(f'ARNES A-CAL (criterio v3) — T={T}. instrumento organismo_v3cal')
    SEM = [1, 2, 3]
    VIVO_KW = dict(CR2.BRAZOS['VIVO'])
    CUELLO_KW = dict(CR2.BRAZOS['CUELLO_MIN'])
    MINI_KW = dict(MV.BRAZOS['VIVO'])

    # ---------------- I1: con vivo=0, n_nec=1 y placebo=0 es el TRONCO v14.2, bit a bit
    print(f"--- I1: organismo_v3cal(vivo=0,n_nec=1,placebo=0) == organismo_v142 (TRONCO v14.2), {len(BAT.ETAPAS)} escenarios x {len(SEM)} semillas")
    for e, kw in BAT.ETAPAS.items():
        for s in SEM:
            chk(f'I1 {e} s{s}', V142.run(s, T=T, **kw), CAL.run(s, T=T, **kw, placebo=0), NUEV_V142)

    # ---------------- I2: con desambiguar=0 y placebo=0 es organismo_vivo_rep2, bit a bit
    print("--- I2: organismo_v3cal(desambiguar=0,placebo=0) == organismo_vivo_rep2 (rep2 VIVO/CUELLO_MIN, mini VIVO)")
    for nom, kw in (('rep2 VIVO', VIVO_KW), ('rep2 CUELLO_MIN', CUELLO_KW), ('mini VIVO', MINI_KW)):
        for s in (CS.ALIAS[0], CS.LIMPIAS[0]):
            chk(f'I2 {nom} s{s}', REP2.run(s, T=T, **kw), CAL.run(s, T=T, **kw, desambiguar=0, placebo=0), NUEV_REP2)

    # ---------------- I3: B-5 es inerte en los mundos del tronco (R nunca es 0)
    print("--- I3: B-5 INERTE en los mundos del tronco: desambiguar=1 == desambiguar=0 (prediccion de v14.2)")
    for e, kw in BAT.ETAPAS.items():
        s = SEM[0]
        chk(f'I3 {e} s{s}', CAL.run(s, T=T, **kw, desambiguar=0, placebo=0),
            CAL.run(s, T=T, **kw, desambiguar=1, placebo=0), ignora={'desambiguar'})

    # ---------------- I4: placebo=0 == no pasar la perilla (el defecto es el tronco)
    print("--- I4: placebo=0 == el defecto (no pasar la perilla)")
    for nom, kw in (('rep2 VIVO', VIVO_KW), ('rep2 CUELLO_MIN', CUELLO_KW), ('mini VIVO', MINI_KW)):
        s = CS.LIMPIAS[0]
        chk(f'I4 {nom} s{s}', CAL.run(s, T=T, **kw), CAL.run(s, T=T, **kw, placebo=0))

    # ---------------- I5: invertir_vivo_en > T es inerte
    print("--- I5: invertir_vivo_en > T es INERTE")
    for s in (CS.ALIAS[0], CS.LIMPIAS[0]):
        chk(f'I5 s{s}', CAL.run(s, T=T, **MINI_KW, placebo=0),
            CAL.run(s, T=T, **MINI_KW, placebo=0, invertir_vivo_en=T + 10), ignora={'invertir_vivo_en'})

    # ---------------- I6: vacuidad DEBIL del placebo (se REPORTA, no es puerta)
    print("--- I6: rango de muertes con placebo=1 dentro del rango con placebo=0 (6 semillas; SE REPORTA, no es puerta)")
    sem6 = list(range(11, 17))
    m0 = [CAL.run(s, T=T, **MINI_KW, placebo=0)['deaths'] for s in sem6]
    m1 = [CAL.run(s, T=T, **MINI_KW, placebo=1)['deaths'] for s in sem6]
    print(f"    muertes placebo=0 {sorted(m0)}  mediana {sorted(m0)[len(m0)//2]}")
    print(f"    muertes placebo=1 {sorted(m1)}  mediana {sorted(m1)[len(m1)//2]}")
    print(f"    (T={T}: es una LECTURA, no una puerta; la puerta es la serie de 40 semillas)")

    # ---------------- CONTROLES QUE DEBEN FALLAR
    print("--- CONTROLES QUE DEBEN FALLAR (M1..M7)")
    s = CS.LIMPIAS[0]
    a0 = CAL.run(s, T=T, **MINI_KW, placebo=0)
    a1 = CAL.run(s, T=T, **MINI_KW, placebo=1)
    a2 = CAL.run(s, T=T, **MINI_KW, placebo=2)
    must_fail('M1 placebo=1 != placebo=0 (mundo vivo)', a0, a1, claves=('W_nec', 'mord', 'deaths', 'splits'))
    must_fail('M2 placebo=2 != placebo=1', a1, a2, claves=('W_nec', 'mord', 'deaths', 'splits'))
    must_fail('M3 placebo=1 != placebo=0 (mundo del examen, vivo=0 n_nec=1)',
              CAL.run(SEM[0], T=T, placebo=0), CAL.run(SEM[0], T=T, placebo=1))
    must_fail('M4 el brazo PEOR (coste de vida mayor) SI cambia', a0,
              CAL.run(s, T=T, **dict(MINI_KW, costo=0.00125, costo_a=0.00125), placebo=0),
              claves=('W_nec', 'mord', 'deaths'))
    must_fail('M5 invertir_vivo_en = T/2 SI cambia', a0,
              CAL.run(s, T=T, **MINI_KW, placebo=0, invertir_vivo_en=T // 2), claves=('W_nec', 'mord', 'deaths'))
    must_fail('M6 paja del comparador (semillas distintas)', a0,
              CAL.run(s + 1, T=T, **MINI_KW, placebo=0), claves=('W_nec', 'mord', 'deaths', 'splits'))
    sa = CS.ALIAS[0]
    must_fail('M7 desambiguar=1 != desambiguar=0 (semilla ALIAS del bloque de la sal)',
              CAL.run(sa, T=T, **dict(CS.BASE), desambiguar=0, placebo=0),
              CAL.run(sa, T=T, **dict(CS.BASE), desambiguar=1, placebo=0), claves=('W_nec', 'mord', 'deaths', 'splits'))

    for l in DET:
        print(l)
    tot_ok = OK[0] + MOK[0]; tot = OK[0] + NO[0] + MOK[0] + MNO[0]
    print(f'IDENTIDADES {OK[0]}/{OK[0]+NO[0]}   CONTROLES QUE FALLAN COMO DEBEN {MOK[0]}/{MOK[0]+MNO[0]}   ({time.time()-t0:.1f}s)')
    print(f'ARNES TOTAL: {tot_ok}/{tot}')
    # ERR-42: el arnes ESCRIBE su JSON y anuncia su sello exacto (el runner lo lee por prefijo + sello, ERR-87)
    import hashlib
    DH = os.path.join(RAIZ, 'datos', 'humo'); os.makedirs(DH, exist_ok=True)
    stamp = time.strftime('%Y%m%d_%H%M%S')
    f = os.path.join(DH, f'identidad_v3cal_{stamp}.json')
    json.dump(dict(meta=dict(fecha=time.strftime('%Y-%m-%dT%H:%M:%S'), T=T,
                             sha_organismo_v3cal=hashlib.sha256(open(os.path.join(AQUI, 'organismo_v3cal.py'), 'rb').read()).hexdigest()[:16],
                             sha_organismo_v142=hashlib.sha256(open(os.path.join(ORG, 'organismo_v142.py'), 'rb').read()).hexdigest()[:16],
                             sha_organismo_vivo_rep2=hashlib.sha256(open(os.path.join(NIV11, 'organismo_vivo_rep2.py'), 'rb').read()).hexdigest()[:16]),
                   identidades=[OK[0], OK[0] + NO[0]], controles=[MOK[0], MOK[0] + MNO[0]],
                   total=f'{tot_ok}/{tot}', detalle=DET,
                   muertes_placebo0=m0, muertes_placebo1=m1, semillas_I6=sem6),
              open(f, 'w', encoding='utf-8'), ensure_ascii=False, default=str)
    print(f'datos -> identidad_v3cal_{stamp}.json')
    sys.exit(0 if tot_ok == tot else 1)
