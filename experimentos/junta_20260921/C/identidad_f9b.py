"""Arnes de identidad de organismo_f9b (FASE 9 BLOQUE 2 — leer con las DOS VIAS). Regla 2 de EQUIPO.md.

MISION: llegar a la AGI por este camino. Este arnes se corre y se pega ENTERO en el informe, CON LA PERILLA
APAGADA, ANTES de mirar un solo numero del experimento.

Cadena: organismo_v14 (TRONCO CONGELADO v14.1) -> organismo_vivo -> _rep -> _rep2 -> _h1 -> organismo_alma
-> organismo_alma2 -> organismo_f9 (3a821884394d66c9) -> organismo_f9b.

  (A) APAGADA: nodo_via=0 == organismo_f9 BIT A BIT en los NUEVE brazos x 2 semillas x 2 niveles de
      rep_acum, en TODAS las claves.  DEBE SER IDENTICO.
  (B) CADENA: nodo_via=0 con vivo=0, n_nec=1 == organismo_v14 (TRONCO).  DEBE SER IDENTICO.
  (C) LA MAESTRA: con alma=None la perilla se apaga sola (nodo_via=1 == nodo_via=0) y no aparece
      ninguna clave nueva.
  (D) NINGUNA CLAVE NUEVA con nodo_via=0 (ni siquiera con f9=1): el dict es el de organismo_f9.
  (E) DEBEN DIFERIR (si no, la perilla es INERTE -- ERR-38): nodo_via=1 != 0 en REL, REC, REL_BAR,
      REL_AZAR y REL_TARDE.
  (F) LA PUERTA SE ABRE (la prueba directa de que la via rapida entra en la decision, no solo en los
      pesos): via_msg > 0 y max(fam_nac) > 0 en REL con nodo_via=1. Si fam_nac fuera 0 en todos los
      nacimientos, la perilla mueve Wp y NO cambia la conducta: seria inerte de hecho.
  (G) ANTES DE LA PRIMERA LECTURA (T = el paso de la primera muerte) nodo_via=1 == nodo_via=0:
      ninguna linea nueva toca el estado ni el rng del mundo antes de que alguien lea.
  (H) EL RNG DEL MUNDO NO SE CONSUME: con nodo_via=1 la secuencia de `spawn`/posiciones no se adelanta.
      Se prueba por (G) y por la guardia de regex del constructor; aqui se comprueba ademas que con
      `conectado=0` y `nodo=1` (nadie lee nunca) nodo_via=1 == nodo_via=0 a T completo.
  (I) GUARDIAS: nodo_via fuera de {0,1}; nodo_via=1 con nodo=0 -> SystemExit.
  (J) DETERMINISMO: dos llamadas iguales dan el mismo dict.

Un proceso, sin Pool (regla 3). T = 20000. OJO (ERR-28): organismo/ va primero en sys.path.
Uso:  python experimentos/junta_20260921/C/identidad_f9b.py
"""
import os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
N09 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo')
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
sys.path[:0] = [AQUI, N09, N13, N11, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_f9 as F9
import organismo_f9b as F9B
import corre_f9 as CF

T = 20000
SEM = (1, 2)
N, h16 = CF.N, CF.h16
B = CF.BRAZOS
OK = [0, 0]


def compara(a, b, quitar=()):
    bb = {k: v for k, v in b.items() if k not in quitar}
    return ([k for k in a if k not in bb], [k for k in a if k in bb and N(a[k]) != N(bb[k])],
            [k for k in bb if k not in a])


def di(et, ok, extra=''):
    OK[1] += 1
    OK[0] += int(bool(ok))
    print(f"  {'OK ' if ok else 'FALLA'}  {et}   {extra}")


def main():
    t0 = time.time()
    print(f"ARNES organismo_f9b — {time.strftime('%Y-%m-%d %H:%M:%S')} · T={T} · semillas {SEM} · UN proceso")
    print(f"  organismo_f9b.py  sha {h16(os.path.join(AQUI, 'organismo_f9b.py'))}")
    print(f"  organismo_f9.py   sha {h16(os.path.join(N09, 'organismo_f9.py'))}  (origen, solo lectura)")
    print(f"  organismo_v14.py  sha {h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'))}  (TRONCO v14.1)")

    print('\n(A) APAGADA (nodo_via=0) == organismo_f9 BIT A BIT — 9 brazos x 2 semillas x 2 rep_acum')
    for br in CF.ORDEN:
        for ac in (0, 1):
            for s in SEM:
                kw = dict(B[br], rep_acum=ac)
                a = F9.run(s, T=T, **kw)
                b = F9B.run(s, T=T, **kw, nodo_via=0)
                f, d, e = compara(a, b)
                di(f'(A) {br} acum={ac} s={s}', not (f or d or e), f'falta {f} dif {d} extra {e}')

    print('\n(B) CADENA: nodo_via=0, vivo=0, n_nec=1 == organismo_v14 (TRONCO CONGELADO)')
    for s in SEM:
        for esc in (dict(), dict(nuevo='C', solap_B=2), dict(invertir_en=T // 2)):
            a = V14.run(s, T=T, **esc)
            b = F9B.run(s, T=T, **esc, nodo_via=0)
            f, d, e = compara(a, b)
            di(f'(B) v14 s={s} {sorted(esc)}', not (f or d or e), f'falta {f} dif {d} extra {e}')

    print('\n(C) LA MAESTRA: con alma=None la perilla se apaga sola')
    for s in SEM:
        base = dict(CF.CUERPO)
        a = F9B.run(s, T=T, **base, nodo_via=0)
        b = F9B.run(s, T=T, **base, nodo_via=1)
        f, d, e = compara(a, b)
        di(f'(C) alma=None s={s}', not (f or d or e), f'falta {f} dif {d} extra {e}')

    print('\n(D) NINGUNA CLAVE NUEVA con nodo_via=0 (el dict es el de organismo_f9)')
    for s in SEM:
        b = F9B.run(s, T=T, **B['REL'], nodo_via=0)
        nue = [k for k in b.get('f9', {}) if k in ('nodo_via', 'via_msg', 'fam_nac')]
        di(f'(D) claves nuevas s={s}', not nue, f'claves nuevas presentes: {nue}')

    print('\n(E) DEBEN DIFERIR (si no, la perilla es INERTE, ERR-38)')
    for br in ('REL', 'REC', 'REL_BAR', 'REL_AZAR', 'REL_TARDE'):
        for s in SEM:
            a = F9B.run(s, T=T, **B[br], nodo_via=0)
            b = F9B.run(s, T=T, **B[br], nodo_via=1)
            f, d, e = compara(a, b, quitar=('f9',))
            di(f'(E) {br} 1 != 0 s={s}', bool(d), f'claves que cambian: {len(d)}')

    print('\n(F) LA PUERTA SE ABRE: via_msg > 0 y max(fam_nac) > 0 en REL con nodo_via=1')
    for s in SEM:
        b = F9B.run(s, T=T, **B['REL'], nodo_via=1)
        f9 = b.get('f9', {})
        vm, fn = f9.get('via_msg', 0), (f9.get('fam_nac') or [0])
        di(f'(F) REL s={s}', vm > 0 and max(fn) > 0,
           f'via_msg {vm} · fam_nac max {max(fn)} media {round(sum(fn)/max(len(fn),1),2)} · n_cod {b.get("n_cod")}')

    print('\n(G) ANTES DE LA PRIMERA LECTURA (T = paso de la primera muerte): 1 == 0')
    for s in SEM:
        r = F9B.run(s, T=T, **B['REL'], nodo_via=0)
        tm = (r.get('vidas_h1') or r.get('vidas') or [T])[0]
        a = F9B.run(s, T=int(tm), **B['REL'], nodo_via=0)
        b = F9B.run(s, T=int(tm), **B['REL'], nodo_via=1)
        f, d, e = compara(a, b, quitar=('f9',))
        d = [k for k in d if k != 'f9']
        di(f'(G) T={int(tm)} s={s}', not d, f'dif {d}')

    print('\n(H) SI NADIE LEE (nodo=1, conectado=0, sin con_desde): 1 == 0 a T completo')
    for s in SEM:
        kw = dict(CF.CUERPO, **CF.NODO, nodo=1, conectado=0, nodo_rel=1)
        a = F9B.run(s, T=T, **kw, nodo_via=0)
        b = F9B.run(s, T=T, **kw, nodo_via=1)
        f, d, e = compara(a, b, quitar=('f9',))
        d = [k for k in d if k != 'f9']
        di(f'(H) nadie lee s={s}', not d, f'dif {d}')

    print('\n(I) GUARDIAS (deben abortar)')
    for et, kw in (('nodo_via=2', dict(B['REL'], nodo_via=2)),
                   ('nodo_via=1 con nodo=0', dict(B['NADA'], nodo_via=1))):
        try:
            F9B.run(1, T=200, **kw)
            di(f'(I) {et}', False, 'NO abortó')
        except SystemExit as ex:
            di(f'(I) {et}', True, str(ex)[:70])

    print('\n(J) DETERMINISMO')
    for s in SEM:
        a = F9B.run(s, T=T, **B['REL'], nodo_via=1)
        b = F9B.run(s, T=T, **B['REL'], nodo_via=1)
        f, d, e = compara(a, b)
        di(f'(J) REL s={s}', not (f or d or e), f'dif {d}')

    print(f'\nTOTAL {OK[0]}/{OK[1]} en {time.time()-t0:.1f}s')
    if OK[0] != OK[1]:
        raise SystemExit('ARNES INCOMPLETO: no se mira ningun numero del experimento.')


if __name__ == '__main__':
    main()
