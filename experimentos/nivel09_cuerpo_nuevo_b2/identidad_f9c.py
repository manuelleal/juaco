"""Arnes de identidad de organismo_f9c (FASE 9 BLOQUE 2). Regla 2 de EQUIPO.md.

MISION: llegar a la AGI por este camino. Este arnes se corre y se pega ENTERO en el informe, CON LAS
PERILLAS APAGADAS, ANTES de mirar un solo numero del experimento.

Cadena: organismo_v14 (TRONCO CONGELADO v14.1 feefc88b1fd8d434) -> organismo_vivo -> _rep -> _rep2
-> _h1 -> organismo_alma -> organismo_alma2 -> organismo_f9 (3a821884394d66c9) -> organismo_f9c,
incorporando las inserciones de organismo_f9b (6a57e9fa9514099b).

  (A) APAGADAS: nodo_via=0, nodo_or=0, sesgo_fijo=0, f9c=0 == organismo_f9 BIT A BIT en los NUEVE
      brazos del bloque 1 x 2 semillas x 2 niveles de rep_acum, en TODAS las claves.
  (B) CADENA: apagadas con vivo=0, n_nec=1 == organismo_v14 (TRONCO).
  (C) ANCLA DEL BLOQUE 2: nodo_via=1 == organismo_f9b BIT A BIT (salvo pa/pn con f9c=1, declaradas
      SOLO LECTURA) en cinco brazos x 2 semillas. Sin esto, los numeros del humo de C no transfieren.
  (D) LA MAESTRA: con alma=None las cuatro perillas se apagan solas y no aparece ninguna clave nueva.
  (E) NINGUNA CLAVE NUEVA con todo apagado (ni siquiera con f9=1).
  (F) DEBEN DIFERIR (>= 7 controles; si no difieren, la perilla es INERTE -- ERR-38):
      1 REL2b != REL · 2 REL2b != REL2 · 3 REL2b_BAR != REL2b · 4 CAUTELA != NADA · 5 DOSIS != REL
      6 ORACULO != REL2b · 7 ORACULO != REL · 8 REL2 != REL · 9 rep_acum 1 != 0 en REL2b.
  (G) EL MECANISMO, MEDIDO (no supuesto): con nodo_via=2 `fam_nac` = 0 en TODOS los nacimientos
      (leer NO abre la puerta) mientras con nodo_via=1 es > 0 (con evidencia SI la abre), `via_msg`
      es el MISMO en la PRIMERA lectura (se absorbe lo mismo; a T completo las trayectorias divergen y
      por eso NO tiene que coincidir) y `pa` > 0 (morder SI abre la puerta).
  (H) ANTES DE LA PRIMERA LECTURA (T = el paso de la primera muerte) nodo_via=2 == nodo_via=0.
  (I) EL RNG DEL MUNDO NO SE CONSUME: con conectado=0 y nodo=1 (nadie lee nunca) nodo_via=2 ==
      nodo_via=0 a T completo; idem nodo_or=1.
  (J) EL ORACULO LEE LA TABLA VERDADERA: con nodo_lee=400 (ocho copias de la tabla) la via lenta del
      recien nacido converge a la fila EXACTA de su necesidad, y difiere de la de REL con el nodo real.
  (K) f9c ES SOLO LECTURA: f9c=1 == f9c=0 en TODAS las claves salvo {pa, pn}.
  (L) CAUTELA ES UN EMPUJON, NO OTRO MUNDO: sesgo_fijo=0 == NADA bit a bit, y sesgo_fijo<0 muerde
      ESTRICTAMENTE menos que NADA (si no, el empujon no empuja).
  (M) GUARDIAS: nodo_via fuera de {0,1,2}; nodo_via con nodo=0; nodo_or con nodo=0 -> SystemExit.
  (N) DETERMINISMO: dos llamadas iguales dan el mismo dict.

Un proceso, sin Pool (regla 3). T = 20000. OJO (ERR-28): organismo/ va primero en sys.path.
Uso:  python experimentos/nivel09_cuerpo_nuevo_b2/identidad_f9c.py
"""
import os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N09 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo')
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
JC = os.path.join(RAIZ, 'experimentos', 'junta_20260921', 'C')
sys.path[:0] = [AQUI, JC, N09, N13, N11, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_f9 as F9
import organismo_f9b as F9B
import organismo_f9c as F9C
import corre_f9 as CF
import corre_bloque2 as CB

T = 20000
SEM = (1, 2)
N, h16 = CF.N, CF.h16
B1, B2 = CF.BRAZOS, CB.BRAZOS
APAGADO = dict(nodo_via=0, nodo_or=0, sesgo_fijo=0.0, f9c=0)
NUEV = {'pa', 'pn'}
OK = [0, 0]


def compara(a, b, quitar=(), extra_ok=()):
    """`quitar` se aplica a LOS DOS lados: una clave excluida no puede contar como 'falta'."""
    aa = {k: v for k, v in a.items() if k not in quitar}
    bb = {k: v for k, v in b.items() if k not in quitar}
    return ([k for k in aa if k not in bb],
            [k for k in aa if k in bb and N(aa[k]) != N(bb[k])],
            [k for k in bb if k not in aa and k not in extra_ok])


def di(et, ok, extra=''):
    OK[1] += 1
    OK[0] += int(bool(ok))
    print(f"  {'OK ' if ok else 'FALLA'}  {et}   {extra}")


def main():
    t0 = time.time()
    print(f"ARNES organismo_f9c — {time.strftime('%Y-%m-%d %H:%M:%S')} · T={T} · semillas {SEM} · UN proceso, sin Pool")
    print(f"  organismo_f9c.py  sha {h16(os.path.join(AQUI, 'organismo_f9c.py'))}")
    print(f"  organismo_f9.py   sha {h16(os.path.join(N09, 'organismo_f9.py'))}  (origen, solo lectura)")
    print(f"  organismo_f9b.py  sha {h16(os.path.join(JC, 'organismo_f9b.py'))}  (ancla del bloque 2, solo lectura)")
    print(f"  organismo_v14.py  sha {h16(os.path.join(RAIZ, 'organismo', 'organismo_v14.py'))}  (TRONCO v14.1)")

    print('\n(A) APAGADAS == organismo_f9 BIT A BIT — 9 brazos x 2 rep_acum x 2 semillas')
    for br in CF.ORDEN:
        for ac in (0, 1):
            for s in SEM:
                kw = dict(B1[br], rep_acum=ac)
                f, d, e = compara(F9.run(s, T=T, **kw), F9C.run(s, T=T, **kw, **APAGADO))
                di(f'(A) {br} acum={ac} s={s}', not (f or d or e), f'falta {f} dif {d} extra {e}')

    print('\n(B) CADENA: apagadas con vivo=0, n_nec=1 == organismo_v14 (TRONCO CONGELADO)')
    for s in SEM:
        for esc in (dict(), dict(nuevo='C', solap_B=2), dict(invertir_en=T // 2)):
            f, d, e = compara(V14.run(s, T=T, **esc), F9C.run(s, T=T, **esc, **APAGADO))
            di(f'(B) v14 s={s} {sorted(esc)}', not (f or d or e), f'falta {f} dif {d} extra {e}')

    print('\n(C) ANCLA DEL BLOQUE 2: nodo_via=1 == organismo_f9b BIT A BIT (salvo pa/pn, SOLO LECTURA)')
    for br in ('REL', 'REC', 'REL_BAR', 'REL_AZAR', 'REL_TARDE'):
        for s in SEM:
            a = F9B.run(s, T=T, **B1[br], nodo_via=1)
            b = F9C.run(s, T=T, **B1[br], nodo_via=1, nodo_or=0, sesgo_fijo=0.0, f9c=1)
            f, d, e = compara(a, b, quitar=('f9',))
            fa, fb = a.get('f9') or {}, b.get('f9') or {}
            df = [k for k in fa if k not in fb or N(fa[k]) != N(fb[k])]
            ex = set(fb) - set(fa)
            di(f'(C) {br} s={s}', not (f or d or e) and not df and ex <= NUEV,
               f'dif {d} f9dif {df} extra_f9 {sorted(ex - NUEV)} (pa/pn declaradas)')

    print('\n(D) LA MAESTRA: con alma=None las cuatro perillas se apagan solas')
    for s in SEM:
        base = dict(CF.CUERPO)
        a = F9C.run(s, T=T, **base, **APAGADO)
        b = F9C.run(s, T=T, **base, nodo_via=2, nodo_or=1, sesgo_fijo=0.0, f9c=1)
        f, d, e = compara(a, b)
        di(f'(D) alma=None s={s}', not (f or d or e), f'falta {f} dif {d} extra {e}')

    print('\n(E) NINGUNA CLAVE NUEVA con todo apagado (el dict es el de organismo_f9)')
    for s in SEM:
        b = F9C.run(s, T=T, **B1['REL'], **APAGADO)
        nue = [k for k in b.get('f9', {}) if k in ('nodo_via', 'via_msg', 'fam_nac', 'pa', 'pn', 'nodo_or')]
        nue += [k for k in b if k == 'sesgo_fijo']
        di(f'(E) claves nuevas s={s}', not nue, f'claves nuevas presentes: {nue}')

    print('\n(F) DEBEN DIFERIR (>= 7 controles; si no, la perilla es INERTE, ERR-38)')
    PARES = (('REL2b', 'REL'), ('REL2b', 'REL2'), ('REL2b_BAR', 'REL2b'), ('CAUTELA', 'NADA'),
             ('DOSIS', 'REL'), ('ORACULO', 'REL2b'), ('ORACULO', 'REL'), ('REL2', 'REL'))
    for x, y in PARES:
        for s in SEM:
            a, b = F9C.run(s, T=T, **B2[x]), F9C.run(s, T=T, **B2[y])
            f, d, e = compara(a, b, quitar=('f9',))
            di(f'(F) {x} != {y} s={s}', bool(d) or N(a.get('f9')) != N(b.get('f9')),
               f'claves que cambian: {len(d)} {d[:3]}')
    for s in SEM:
        a = F9C.run(s, T=T, **B2['REL2b'])
        b = F9C.run(s, T=T, **dict(B2['REL2b'], rep_acum=1))
        di(f'(F) rep_acum 1 != 0 en REL2b s={s}', N(a) != N(b),
           f"desc {a['descendientes']} -> {b['descendientes']}")

    print('\n(G) EL MECANISMO, MEDIDO: leer NO abre la puerta con nodo_via=2; morder SI')
    for s in SEM:
        v2 = F9C.run(s, T=T, **B2['REL2b'])['f9']
        v1 = F9C.run(s, T=T, **B2['REL2'])['f9']
        fn2, fn1 = v2.get('fam_nac') or [], v1.get('fam_nac') or []
        di(f'(G1) fam_nac == 0 en TODOS los nacimientos con nodo_via=2 s={s}',
           bool(fn2) and max(fn2) == 0, f'nacimientos {len(fn2)} max {max(fn2) if fn2 else None}')
        di(f'(G2) fam_nac > 0 con nodo_via=1 (la evidencia SI abre la puerta) s={s}',
           bool(fn1) and max(fn1) > 0, f'max {max(fn1) if fn1 else None} media {round(sum(fn1)/max(len(fn1),1),2)}')
        # G3 (CORREGIDA antes de mirar un numero del experimento; la primera version estaba MAL ESCRITA y
        # se declara en el informe): a T completo `via_msg` NO PUEDE coincidir, porque las dos trayectorias
        # divergen desde la primera lectura. La identidad exacta es LA PRIMERA LECTURA: mismo estado antes
        # -> mismos mensajes absorbidos; lo unico que cambia es QUE cuenta como evidencia.
        r0 = F9C.run(s, T=T, **B1['REL'], **APAGADO)
        tm0 = int((r0.get('vidas_h1') or r0.get('vidas') or [T])[0]) + 1
        w2 = F9C.run(s, T=tm0, **B2['REL2b'])['f9']
        w1 = F9C.run(s, T=tm0, **B2['REL2'])['f9']
        # (fam_nac en el PRIMER nacimiento puede ser 0 tambien con nodo_via=1: el nodo todavia es corto y
        #  ningun codigo junta puerta_pat=5 mensajes. Se REPORTA; la prueba de la puerta es G1/G2 a T completo.)
        di(f'(G3) en la PRIMERA lectura via_msg es IGUAL en nodo_via 1 y 2 s={s}',
           w2.get('via_msg') == w1.get('via_msg') and (w2.get('via_msg') or 0) > 0,
           f"T={tm0} · via_msg 2 -> {w2.get('via_msg')} · 1 -> {w1.get('via_msg')} · fam_nac "
           f"{max(w2.get('fam_nac') or [None])} vs {max(w1.get('fam_nac') or [None])} · a T completo "
           f"divergen (2 -> {v2.get('via_msg')}, 1 -> {v1.get('via_msg')}): trayectorias distintas, no un fallo")
        di(f'(G4) pa > 0 con nodo_via=2 (MORDER abre la puerta) s={s}',
           (v2.get('pa') or 0) > 0, f"pa {v2.get('pa')} / pn {v2.get('pn')}")

    print('\n(H) ANTES DE LA PRIMERA LECTURA (T = paso de la primera muerte): nodo_via=2 == 0')
    for s in SEM:
        r = F9C.run(s, T=T, **B1['REL'], **APAGADO)
        tm = int((r.get('vidas_h1') or r.get('vidas') or [T])[0])
        a = F9C.run(s, T=tm, **B1['REL'], **APAGADO)
        b = F9C.run(s, T=tm, **B2['REL2b'])
        f, d, e = compara(a, b, quitar=('f9',))
        di(f'(H) T={tm} s={s}', not d, f'dif {d}')

    print('\n(I) SI NADIE LEE (nodo=1, conectado=0): nodo_via=2 y nodo_or=1 == apagado, a T completo')
    for s in SEM:
        kw = dict(CF.CUERPO, **CF.NODO, nodo=1, conectado=0, nodo_rel=1)
        a = F9C.run(s, T=T, **kw, **APAGADO)
        for et, per in (('nodo_via=2', dict(nodo_via=2, nodo_or=0, sesgo_fijo=0.0, f9c=0)),
                        ('nodo_or=1', dict(nodo_via=0, nodo_or=1, sesgo_fijo=0.0, f9c=0))):
            f, d, e = compara(a, F9C.run(s, T=T, **kw, **per), quitar=('f9',))
            di(f'(I) nadie lee {et} s={s}', not d, f'dif {d}')

    print('\n(J) EL ORACULO LEE LA TABLA VERDADERA: con nodo_lee=400 (8x50) la via lenta del recien nacido')
    print('    converge a la fila EXACTA de su necesidad -- hambre A=+1 B=-3 C=D=0, o sed C=+1 D=-3 A=B=0')
    for s in SEM:
        r = F9C.run(s, T=T, **B1['REL'], **APAGADO)
        tm = int((r.get('vidas_h1') or r.get('vidas') or [T])[0]) + 1
        o = F9C.run(s, T=tm, **dict(B2['ORACULO'], nodo_lee=400))
        n = F9C.run(s, T=tm, **B2['REL'])
        W, WN = o['W_lenta'], n['W_lenta']
        hambre = (abs(W['A'] - 1.0) <= 0.35 and abs(W['B'] + 3.0) <= 0.5 and abs(W['C']) <= 0.35 and abs(W['D']) <= 0.40)
        sed = (abs(W['C'] - 1.0) <= 0.35 and abs(W['D'] + 3.0) <= 0.5 and abs(W['A']) <= 0.35 and abs(W['B']) <= 0.40)
        di(f'(J) oraculo s={s}', (hambre or sed) and W != WN,
           f"ORACULO W_lenta {W} ({'fila HAMBRE exacta' if hambre else 'fila SED exacta' if sed else 'NINGUNA fila'}) · "
           f"REL (mismo T, nodo real) {WN} · via_msg {o['f9'].get('via_msg')} lecturas {o['f9'].get('lecturas')}")

    print('\n(K) f9c ES SOLO LECTURA: f9c=1 == f9c=0 salvo {pa, pn}')
    for br in ('REL', 'REL2b', 'ORACULO'):
        for s in SEM:
            a = F9C.run(s, T=T, **dict(B2[br], f9c=0))
            b = F9C.run(s, T=T, **dict(B2[br], f9c=1))
            f, d, e = compara(a, b, quitar=('f9',))
            fa, fb = a.get('f9') or {}, b.get('f9') or {}
            df = [k for k in fa if k not in fb or N(fa[k]) != N(fb[k])]
            ex = set(fb) - set(fa)
            di(f'(K) {br} s={s}', not (f or d or e) and not df and ex == NUEV,
               f'dif {d} f9dif {df} extra {sorted(ex)}')

    print('\n(L) CAUTELA ES UN EMPUJON: sesgo_fijo=0 == NADA; sesgo_fijo<0 muerde ESTRICTAMENTE menos')
    for s in SEM:
        a = F9C.run(s, T=T, **B2['NADA'])
        b = F9C.run(s, T=T, **dict(B2['CAUTELA'], sesgo_fijo=0.0))
        f, d, e = compara(a, b)
        di(f'(L1) sesgo_fijo=0 == NADA s={s}', not (f or d or e), f'dif {d} extra {e}')
        c = F9C.run(s, T=T, **dict(B2['CAUTELA'], sesgo_fijo=-2.0))
        ma = sum(sum(v) for v in a['mord'].values()); mc = sum(sum(v) for v in c['mord'].values())
        di(f'(L2) sesgo_fijo=-2.0 muerde menos que NADA s={s}', mc < ma, f'mordidas {mc} < {ma}')

    print('\n(M) GUARDIAS (deben abortar)')
    for et, kw in (('nodo_via=3', dict(B1['REL'], nodo_via=3)),
                   ('nodo_via=2 con nodo=0', dict(B1['NADA'], nodo_via=2)),
                   ('nodo_or=1 con nodo=0', dict(B1['NADA'], nodo_or=1))):
        try:
            F9C.run(1, T=200, **kw)
            di(f'(M) {et}', False, 'NO abortó')
        except SystemExit as ex:
            di(f'(M) {et}', True, str(ex)[:80])

    print('\n(N) DETERMINISMO')
    for br in ('REL2b', 'ORACULO', 'CAUTELA'):
        for s in SEM:
            f, d, e = compara(F9C.run(s, T=T, **B2[br]), F9C.run(s, T=T, **B2[br]))
            di(f'(N) {br} s={s}', not (f or d or e), f'dif {d}')

    print(f'\nTOTAL {OK[0]}/{OK[1]} en {time.time()-t0:.1f}s')
    if OK[0] != OK[1]:
        raise SystemExit('ARNES INCOMPLETO: no se mira ningun numero del experimento.')


if __name__ == '__main__':
    main()
