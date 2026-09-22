"""Arnes de identidad de mundo_fase10 (F0_fable_solo). Regla 2 de EQUIPO.md: se corre y se pega ENTERO antes de mirar un numero.

MISION: llegar a la AGI por este camino. El mundo nuevo no puede haber movido al organismo: con las perillas apagadas tiene
que ser el tronco v14.2 BIT A BIT (y, con desambiguar=0, organismo_f9 bit a bit, la cadena entera hasta v14.1); y cada
perilla nueva tiene que hacer algo (si un control no cambia nada, no controla nada: ERR-38).

IDENTIDADES (DEBEN ser identicas):
  I1  mundo del tronco (vivo=0, n_nec=1): perillas apagadas == organismo/organismo_v142.py (TRONCO v14.2), TODAS las claves,
      los 12 escenarios de identidad_v142.py x 2 semillas, T = 30000.
  I2  el rng NO se consume con las perillas apagadas: T = 120000 == organismo_v142, semilla 1.
  I3  desambiguar=0 == organismo_f9 (3a821884394d66c9) en los 9 brazos de corre_f9 (RENACE, NADA, M1, REC, REL, REL_FIJO, REL_BAR,
      REL_AZAR, REL_TARDE) x 2 semillas, claves de f9 (3 claves nuevas de solo lectura fuera: desambiguar, des_splits, des_t).
  I4  mundo vivo con B-5 (sin reproduccion): desambiguar=1 == experimentos/creacion_B/organismo_vivo_codigo.py (el instrumento
      que midio el alias 18/18), 2 semillas, TODAS las claves.
  I5  mundo vivo con reproduccion (rep2, sin h1) y PLACEBO: placebo=1, desambiguar=1 == experimentos/criterio_v3/organismo_v3cal.py
      (placebo=1) en sus claves comunes, 2 semillas: el placebo copiado consume EXACTAMENTE los mismos sorteos.
  I6  ORACULO: desambiguar=0, nodo_or=1 == organismo_f9c.py (nodo_or=1, nodo_via=0), 2 semillas, claves de f9c.
  I7  INERCIA DEL MAPA sin r_vis: usa_M=1, olvida_M=1, escribe_M=1 con r_vis=None == organismo_v142 en el mundo del tronco (todas las
      claves) y == organismo_f9 REL (desambiguar=0) en el mundo vivo: el mapa NO toca las baterias del tronco (M10-4, coste 1.00x).
  I8  f10=1 solo AGREGA la clave 'f10': todas las demas claves identicas a f10=0 (brazo REL del mundo F10).
  I9  DETERMINISMO: dos llamadas iguales del brazo REL del mundo F10 dan el mismo dict.
  I10 regla 14: CUERPO y NODO del runner == corre_f9.CUERPO / NODO campo a campo.
CONTROLES QUE DEBEN DIFERIR (>= 7):
  D1 r_vis=8 != r_vis=None (cuerpo REL, mundo vivo del tronco)      D2 usa_M=1 != usa_M=0 (con r_vis=8)
  D3 olvida_M=1 != olvida_M=0 (mundo F10)                            D4 parches=6 != parches=0 (mundo vivo, r_vis=8)
  D5 cambia_cada=5000 != 0 (mundo F10)                               D6 placebo=1 != placebo=0 (mundo F10)
  D7 nodo_or=1 != REL (mundo F10)                                    D8 desambiguar=1 != 0 (mundo F10: B-5 actua)
  D9 pats de 16 tipos != pats del tronco                             D10 NODO_BARAJADO != REL y NADA != REL (mundo F10)
  D11 MUNDO_FIJO != REL                                              D12 MAPA_SIN_TABLA != SIN_HERENCIA
GUARDIAS: nodo_or sin nodo; olvida_M sin usa_M; parches sin vivo; f10 sin h1; vals incompletos -> SystemExit.
Un proceso, sin Pool (regla 3). Uso: python identidad_mundo_fase10.py [T]
"""
import os, sys, time, json

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
JUACO = r'C:\Users\User\Documents\PROYECTOS\JUACO\bundle'
EXP = os.path.join(JUACO, 'experimentos')
sys.path[:0] = [AQUI, os.path.join(JUACO, 'organismo'), os.path.join(EXP, 'nivel09_cuerpo_nuevo'), os.path.join(EXP, 'nivel09_cuerpo_nuevo_b2'),
                os.path.join(EXP, 'nivel13_alma'), os.path.join(EXP, 'nivel11_mundo_vivo'), os.path.join(EXP, 'creacion_B'), os.path.join(EXP, 'criterio_v3')]

import organismo_v142 as V142
import organismo_f9 as F9
import organismo_f9c as F9C
import organismo_vivo_codigo as VC
import organismo_v3cal as V3
import corre_f9 as CF
import mundo_fase10 as M10
import corre_mundo_fase10 as CM

T = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
TV = 20000   # mundo vivo (los brazos mortales son lentos de comparar; 20000 basta para ver muertes, partos y lecturas)
N, h16 = CM.N, CM.h16
NUEV = {'desambiguar', 'des_splits', 'des_t'}
ESC = [('AB por defecto', dict()), ('AB invertido', dict(invertir_en=15000)), ('AB + patron nuevo C', dict(nuevo='C', nuevo_en=15000)),
       ('AB solap_AB=3 (E2L)', dict(solap_AB=3)), ('AB sin plasticidad', dict(plast=False)), ('AB via lenta apagada', dict(eta_s=0.0)),
       ('AB sin puerta', dict(puerta=None)), ('AB sin division por signo', dict(div_signo=False)), ('AB sin hija dispersa', dict(mask_rel=0)),
       ('AB sin puerta por codigo', dict(puerta_pat=0)), ('AB las dos perillas v14 off', dict(mask_rel=0, puerta_pat=0)),
       ('AB D comida solap_B=2 (E2K)', dict(nuevo='D', nuevo_val='comida', solap_B=2, nuevo_en=15000))]
OK = [0, 0]
t0 = time.time()


def comp(a, b, quitar=()):
    return ([k for k in a if k in b and N(a[k]) != N(b[k])] + [k for k in a if k not in b and k not in quitar]
            + [k for k in b if k not in a and k not in quitar])


def caso(etq, ok, det=''):
    OK[0] += bool(ok); OK[1] += 1
    print(f"  [{time.time()-t0:5.0f}s] {'OK   ' if ok else 'FALLA'} {etq}  {det}")


def igual(etq, a, b, quitar=()):
    d = comp(a, b, quitar); caso(etq, not d, 'IDENTICO' if not d else f'DIFIERE {d[:5]}')


def difiere(etq, a, b, det=''):
    caso(etq, N(a) != N(b), ('DIFIERE (debe)' if N(a) != N(b) else 'IDENTICO: el control NO controla (ERR-38)') + ' ' + det)


def guardia(etq, f):
    try:
        f(); caso(etq, False, 'NO lanzo SystemExit')
    except SystemExit as e:
        caso(etq, True, str(e)[:70])


if __name__ == '__main__':
    for nom, p in [('organismo_v142 (TRONCO)', os.path.join(JUACO, 'organismo', 'organismo_v142.py')), ('organismo_f9 (origen)', os.path.join(EXP, 'nivel09_cuerpo_nuevo', 'organismo_f9.py')),
                   ('organismo_f9c', os.path.join(EXP, 'nivel09_cuerpo_nuevo_b2', 'organismo_f9c.py')), ('organismo_vivo_codigo', os.path.join(EXP, 'creacion_B', 'organismo_vivo_codigo.py')),
                   ('organismo_v3cal', os.path.join(EXP, 'criterio_v3', 'organismo_v3cal.py')), ('mundo_mapa', os.path.join(EXP, 'nivel6_mapa', 'mundo_mapa.py')),
                   ('mundo_fase10 (DESTINO)', os.path.join(AQUI, 'mundo_fase10.py')), ('corre_mundo_fase10', os.path.join(AQUI, 'corre_mundo_fase10.py')), ('este arnes', os.path.abspath(__file__))]:
        print(f'  sha {nom:26s} {h16(p)}')
    print(f"\n--- I10 regla 14: CUERPO / NODO del runner == corre_f9 ---")
    for k in sorted(set(CF.CUERPO) | set(CM.CUERPO)):
        if N(CF.CUERPO.get(k)) != N(CM.CUERPO.get(k)): caso(f'I10 campo {k}', False, f'{CF.CUERPO.get(k)} vs {CM.CUERPO.get(k)}')
    for k in ('alma_muertes', 'menu', 'f9', 'nodo_k', 'nodo_lee'):
        if N(CF.NODO[k]) != N(CM.NODO[k]): caso(f'I10 NODO {k}', False, f'{CF.NODO[k]} vs {CM.NODO[k]}')
    caso('I10 CUERPO (17 campos) y NODO campo a campo == corre_f9', OK[1] == 0, f'{len(CM.CUERPO)} campos')

    print(f"\n--- I1: mundo del tronco, perillas apagadas == organismo_v142 (12 escenarios x 2 semillas, T={T}) ---")
    for etq, kw in ESC:
        for s in (1, 2):
            igual(f'I1 {etq:>30} s{s}', V142.run(s, T=T, **kw), M10.run(s, T=T, **kw))
    print(f"\n--- I2: el rng NO se consume (T=120000, semilla 1) ---")
    igual('I2 T=120000 s1', V142.run(1, T=120000), M10.run(1, T=120000))

    print(f"\n--- I3: desambiguar=0 == organismo_f9 en los 9 brazos de corre_f9 (T={TV}) ---")
    for b in CF.ORDEN:
        for s in (1, 2):
            igual(f'I3 {b:>10} s{s}', F9.run(s, T=TV, **CF.BRAZOS[b]), M10.run(s, T=TV, desambiguar=0, **CF.BRAZOS[b]), NUEV)

    print(f"\n--- I4: mundo vivo + B-5 == organismo_vivo_codigo (desambiguar=1, sin reproduccion) ---")
    VKW = dict(vivo=1, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001, n_nec=2)
    for s in (1, 2):
        igual(f'I4 vivo desambiguar=1 s{s}', VC.run(s, T=TV, desambiguar=1, **VKW), M10.run(s, T=TV, desambiguar=1, **VKW))
        igual(f'I4 vivo desambiguar=0 s{s}', VC.run(s, T=TV, desambiguar=0, **VKW), M10.run(s, T=TV, desambiguar=0, **VKW))

    print(f"\n--- I5: rep2 + PLACEBO == organismo_v3cal (placebo=1, desambiguar=1) ---")
    RKW = dict(VKW, rep_cuello=2, reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0, rep_coste=0.0, rep2=1, rep2_regalo=600)
    for s in (1, 2):
        for pl in (0, 1):
            igual(f'I5 placebo={pl} s{s}', V3.run(s, T=TV, placebo=pl, desambiguar=1, **RKW), M10.run(s, T=TV, placebo=pl, desambiguar=1, **RKW), {'invertir_vivo_en', 'placebo'})

    print(f"\n--- I6: ORACULO == organismo_f9c (nodo_or=1, nodo_via=0), desambiguar=0 ---")
    for s in (1, 2):
        kw = dict(CF.BRAZOS['REL'], nodo_or=1)
        a = F9C.run(s, T=TV, nodo_via=0, **kw); a['f9'] = {k: v for k, v in a['f9'].items() if k != 'nodo_or'}   # f9c agrega el eco de configuracion nodo_or=1 al dict f9; el contenido leido es el mismo
        igual(f'I6 ORACULO s{s}', a, M10.run(s, T=TV, desambiguar=0, **kw), NUEV)

    print(f"\n--- I7: INERCIA del mapa sin r_vis (usa_M=1, olvida_M=1) ---")
    for s in (1, 2):
        igual(f'I7 tronco s{s}', V142.run(s, T=T), M10.run(s, T=T, usa_M=1, olvida_M=1, escribe_M=1))
        igual(f'I7 vivo REL s{s}', F9.run(s, T=TV, **CF.BRAZOS['REL']), M10.run(s, T=TV, desambiguar=0, usa_M=1, olvida_M=1, **CF.BRAZOS['REL']), NUEV)

    print(f"\n--- I8 / I9: f10 solo agrega 'f10'; determinismo (mundo F10, brazo REL, T={TV}) ---")
    rel = M10.run(1, T=TV, **CM.BRAZOS['REL'])
    igual('I8 f10=1 vs f10=0 (menos la clave f10)', M10.run(1, T=TV, **dict(CM.BRAZOS['REL'], f10=0)), rel, {'f10'})
    igual('I9 determinismo REL', rel, M10.run(1, T=TV, **CM.BRAZOS['REL']))

    print(f"\n--- D1..D12: controles que DEBEN diferir (mundo F10 salvo donde se dice, T={TV}, semilla 1) ---")
    B = CM.BRAZOS
    base_vivo = dict(CF.BRAZOS['REL'])
    difiere('D1 r_vis=8 != r_vis=None (cuerpo REL, mundo vivo del tronco)', M10.run(1, T=TV, r_vis=8, **base_vivo), M10.run(1, T=TV, **base_vivo))
    difiere('D2 usa_M=1 != usa_M=0 (r_vis=8, mundo vivo del tronco)', M10.run(1, T=TV, r_vis=8, usa_M=1, **base_vivo), M10.run(1, T=TV, r_vis=8, **base_vivo))
    difiere('D3 olvida_M=1 != olvida_M=0 (mundo F10)', rel, M10.run(1, T=TV, **dict(B['REL'], olvida_M=0)))
    difiere('D4 parches=6 != parches=0 (mundo vivo, r_vis=8)', M10.run(1, T=TV, r_vis=8, parches=6, cap=5, regen=30, **base_vivo), M10.run(1, T=TV, r_vis=8, **base_vivo))
    difiere('D5 cambia_cada=5000 != 0 (mundo F10)', rel, M10.run(1, T=TV, **dict(B['REL'], cambia_cada=0)), f"cambios {rel['f10']['n_cambios']}")
    difiere('D6 placebo=1 != 0 (mundo F10)', rel, M10.run(1, T=TV, **B['PLACEBO']))
    difiere('D7 ORACULO != REL (mundo F10)', rel, M10.run(1, T=TV, **B['ORACULO']))
    difiere('D8 desambiguar=1 != 0 (mundo F10: B-5 actua)', rel, M10.run(1, T=TV, **B['REL_D0']), f"des_splits REL {rel['des_splits']}")
    difiere('D9 pats 16 tipos != pats del tronco', rel, M10.run(1, T=TV, **dict(B['REL'], pats=None, vals=None, estims=('A', 'B', 'C', 'D'))))
    nada = M10.run(1, T=TV, **B['NADA']); bar = M10.run(1, T=TV, **B['NODO_BARAJADO'])
    difiere('D10a NODO_BARAJADO != REL', rel, bar, f"baraja_identidad {bar['alma2']['baraja_nodo_identidad']}")
    difiere('D10b NADA != REL', rel, nada, f"lect_div REL {rel['f9']['lect_div']}/{rel['f9']['lecturas']}")
    difiere('D11 MUNDO_FIJO != REL', rel, M10.run(1, T=TV, **B['MUNDO_FIJO']))
    difiere('D12 MAPA_SIN_TABLA != SIN_HERENCIA', M10.run(1, T=TV, **B['MAPA_SIN_TABLA']), M10.run(1, T=TV, **B['SIN_HERENCIA']))
    difiere('D13 REL_SIN_MAPA != REL', rel, M10.run(1, T=TV, **B['REL_SIN_MAPA']))

    print(f"\n--- GUARDIAS ---")
    guardia('G1 nodo_or sin nodo', lambda: M10.run(1, T=100, **dict(B['NADA'], nodo_or=1)))
    guardia('G2 olvida_M sin usa_M', lambda: M10.run(1, T=100, **dict(B['REL'], usa_M=0)))
    guardia('G3 parches sin vivo', lambda: M10.run(1, T=100, parches=6))
    guardia('G4 f10 sin h1', lambda: M10.run(1, T=100, f10=1))
    guardia('G5 vals incompletos', lambda: M10.run(1, T=100, **dict(B['REL'], vals={'A': 'comida'})))

    print(f"\nVEREDICTO identidad_mundo_fase10: {'PASA' if OK[0] == OK[1] else 'NO PASA'}  {OK[0]}/{OK[1]}   ({time.time()-t0:.0f}s, un proceso)")
    sys.exit(0 if OK[0] == OK[1] else 1)
