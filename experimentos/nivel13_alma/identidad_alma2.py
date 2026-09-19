"""Arnes de identidad de organismo_alma2 (los TRES CONTROLES del BLOQUE ALMA). Regla 2 de registro/EQUIPO.md.

MISION: llegar a la AGI por este camino, hasta la fase 10 y superarla.

Cadena: organismo_v14 (TRONCO v14.1) -> organismo_vivo -> _rep -> _rep2 -> _h1 -> organismo_alma -> organismo_alma2.

  (A) APAGADA SIN ALMA (alma=None): alma2 == organismo_alma == organismo_vivo_h1, TODAS las claves, 5 brazos H-1.
  (B) APAGADA CON ALMA (menu='abcdef', nodo_baraja=0): claves viejas bit a bit + EXACTAMENTE la clave `alma2`.
  (C) CADENA: vivo=0, n_nec=1 == organismo_v14 (TRONCO).
  (D) DEBEN DIFERIR (si no difieren, el control es inerte y no controla nada):
      BARAJA != CIEGO (misma secuencia de curitas, solo cambia el nodo) · menu recortado != menu completo.
  (E) EL BARAJADO BARAJA: permutaciones identidad escasas y marginales conservadas (mismo multiconjunto de
      recompensas leidas), comprobado con el nodo final del crudo.
  (F) SIN_NODO NO SE CONECTA NUNCA: con menu sin (a), conectado_final == 0 aunque el nodo se llene.
  (G) GUARDIAS del instrumento: menu vacio / con repeticiones / fuera de abcdef, curita fuera del menu
      ofrecido, y nodo_baraja=1 con nodo=0 -> SystemExit.
  (H) EL BUZON ES PACIENTE (corre_alma.seguro): respuesta que no es dict, sin `curita`, con curita fuera del
      menu, o un alma que lanza excepcion -> se registra (f) y la corrida NO aborta.
  (I) DETERMINISMO: dos llamadas iguales dan el mismo dict.

Un proceso, sin Pool (regla 3). T = 20000. OJO (ERR-28): organismo/ va primero en sys.path.
Uso:  python experimentos/nivel13_alma/identidad_alma2.py
"""
import json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
sys.path[:0] = [AQUI, N11, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_vivo_h1 as H1
import organismo_alma as A1
import organismo_alma2 as A2
import corre_vivo_rep as C1
import corre_vivo_rep2 as C2
import corre_alma as CA

T = 20000
SEM = (1, 2)
MED_H1 = dict(C2.MED2, h1=1)
MODOS = {'RENACE': dict(muerte_real=0), 'NADA': dict(muerte_real=1, hereda='nada', dote=0.6),
         'M1': dict(muerte_real=1, hereda='M1', dote=0.6),
         'PARES': dict(muerte_real=1, hereda='M1+pares', dote=0.6),
         'BARAJA_H': dict(muerte_real=1, hereda='baraja', dote=0.6)}
BRAZOS = {m: dict(C1.BRAZOS['CUELLO_MIN']) | MED_H1 | MODOS[m] for m in MODOS}
BASE = BRAZOS['NADA']
GRANDE = 10 ** 9
N, h16 = C1.N, C1.h16


def fija(c):
    return lambda res: {'curita': c, 'motivo': f'arnes: siempre ({c})'}


def compara(a, b, quitar=()):
    bb = {k: v for k, v in b.items() if k not in quitar}
    return ([k for k in a if k not in bb], [k for k in a if k in bb and N(a[k]) != N(bb[k])], [k for k in bb if k not in a])


def caso(etiq, fa, fb, t0, difiere=False, extra=None, sem=SEM):
    ok, det = 0, ''
    for s in sem:
        a, b = fa(s), fb(s)
        falta, dif, ext = compara(a, b)
        igual = (not falta and not dif and ((set(ext) == extra) if extra is not None else (not ext)))
        ok += int(igual != difiere)
        if (falta or dif or (ext and extra is None)) and not det:
            det = f"  falta {falta[:3]} dif {dif[:4]} extra {sorted(ext)[:3]}"
    marca = 'DIFIERE (como debe)' if difiere else 'IDENTICO'
    print(f"  [{time.time()-t0:6.1f}s] {etiq:74s} {ok}/{len(sem)} {marca if ok == len(sem) else 'FALLA' + det}", flush=True)
    return ok, len(sem)


def prueba(etiq, f, t0, sem=SEM):
    ok = sum(int(bool(f(s))) for s in sem)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:74s} {ok}/{len(sem)} {'OK' if ok == len(sem) else 'FALLA'}", flush=True)
    return ok, len(sem)


def lanza(f):
    try:
        f(); return False
    except SystemExit:
        return True


def main():
    t0 = time.time(); P = []
    print(f"IDENTIDAD organismo_alma2  (sha {h16(os.path.join(AQUI,'organismo_alma2.py'))})")
    print(f"  origen organismo_alma.py    sha {h16(os.path.join(AQUI,'organismo_alma.py'))} (se espera 7c09cec391daa879)")
    print(f"  origen organismo_vivo_h1.py sha {h16(os.path.join(N11,'organismo_vivo_h1.py'))} (se espera 9e99ff87b5e2db1e)")

    print("\n(A) APAGADA SIN ALMA: alma2 == organismo_alma == organismo_vivo_h1, todas las claves")
    for b, kw in BRAZOS.items():
        P.append(caso(f"(A) {b}: alma2 == organismo_alma", lambda s, k=kw: A1.run(s, T=T, **k),
                      lambda s, k=kw: A2.run(s, T=T, **k), t0))
    P.append(caso("(A6) NADA: alma2 == organismo_vivo_h1 (el origen del origen)",
                  lambda s: H1.run(s, T=T, **BASE), lambda s: A2.run(s, T=T, **BASE), t0))

    print("\n(B) APAGADA CON ALMA: menu='abcdef', nodo_baraja=0 -> claves viejas bit a bit + solo `alma2`")
    for c in ('f', 'a', 'b'):
        P.append(caso(f"(B) alma=({c}) menu completo, sin baraja == organismo_alma",
                      lambda s, cc=c: A1.run(s, T=T, **BASE, alma=fija(cc), alma_muertes=GRANDE, nodo=1),
                      lambda s, cc=c: A2.run(s, T=T, **BASE, alma=fija(cc), alma_muertes=GRANDE, nodo=1),
                      t0, extra={'alma2'}))

    print("\n(C) CADENA")
    P.append(caso("(C) vivo=0, n_nec=1 == organismo_v14 (TRONCO)",
                  lambda s: V14.run(s, T=T), lambda s: A2.run(s, T=T, vivo=0, n_nec=1), t0))

    print("\n(D) DEBEN DIFERIR: si el control no cambia nada, no controla nada")
    P.append(caso("(D1) BARAJA-NODO != NODO-CIEGO (misma curita, mismo nodo, solo se permutan las R)",
                  lambda s: A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=1, conectado=1, menu='bcdef'),
                  lambda s: A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=1, conectado=1, menu='bcdef', nodo_baraja=1),
                  t0, difiere=True))
    P.append(caso("(D2) NODO-CIEGO (conectado=1) != sin conectar (mismo menu, mismas curitas)",
                  lambda s: A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=1, conectado=0, menu='bcdef'),
                  lambda s: A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=1, conectado=1, menu='bcdef'),
                  t0, difiere=True))
    P.append(caso("(D3) menu recortado 'cdef' con alma (c) != menu completo con alma (a)",
                  lambda s: A2.run(s, T=T, **BASE, alma=fija('a'), alma_muertes=10, nodo=1, menu='abcdef'),
                  lambda s: A2.run(s, T=T, **BASE, alma=fija('c'), alma_muertes=10, nodo=1, menu='cdef'),
                  t0, difiere=True))

    print("\n(E) EL BARAJADO BARAJA  ·  (F) SIN_NODO no se conecta  ·  (G) guardias  ·  (H) buzon  ·  (I) determinismo")
    P.append(prueba("(E1) permutaciones IDENTIDAD escasas (<= 1 de 10 nacimientos conectados)",
                    lambda s: A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=1, conectado=1,
                                     menu='bcdef', nodo_baraja=1)['alma2']['baraja_nodo_identidad'] <= 1, t0))
    P.append(prueba("(E2) sin baraja, baraja_nodo_identidad == 0 y la clave dice nodo_baraja=0",
                    lambda s: (lambda r: r['alma2']['baraja_nodo_identidad'] == 0 and r['alma2']['nodo_baraja'] == 0)
                    (A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=1, conectado=1, menu='bcdef')), t0))
    P.append(prueba("(E3) MARGINALES: con 1 muerte el NODO ALMACENADO es identico con y sin baraja "
                    "(solo se permuta la COPIA que el hijo lee)",
                    lambda s: (lambda a, b: N(a['nodo_cola']) == N(b['nodo_cola']) and a['nodo_n'] == b['nodo_n'])
                    (A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=1, nodo=1, conectado=1, menu='bcdef'),
                     A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=1, nodo=1, conectado=1, menu='bcdef', nodo_baraja=1)), t0))
    P.append(prueba("(F) SIN_NODO (menu 'cdef'): conectado_final == 0 y nodo_n > 0 (se llena, nadie lee)",
                    lambda s: (lambda r: r['conectado_final'] == 0 and r['nodo_n'] > 0)
                    (A2.run(s, T=T, **BASE, alma=fija('c'), alma_muertes=10, nodo=1, menu='cdef')), t0))
    for et, f in (("menu vacio", lambda s: A2.run(s, T=T, **BASE, alma=fija('f'), alma_muertes=5, menu='')),
                  ("menu con repeticiones", lambda s: A2.run(s, T=T, **BASE, alma=fija('f'), alma_muertes=5, menu='ffa')),
                  ("menu fuera de abcdef", lambda s: A2.run(s, T=T, **BASE, alma=fija('f'), alma_muertes=5, menu='fz')),
                  ("curita fuera del menu ofrecido", lambda s: A2.run(s, T=T, **BASE, alma=fija('a'), alma_muertes=5, menu='cdef')),
                  ("nodo_baraja=1 con nodo=0", lambda s: A2.run(s, T=T, **BASE, alma=fija('f'), alma_muertes=5, nodo=0, nodo_baraja=1))):
        P.append(prueba(f"(G) {et} -> SystemExit", lambda s, ff=f: lanza(lambda: ff(s)), t0))

    def buzon(mal, menu='abcdef'):
        CA.INVALIDAS.clear()
        r = A2.run(1, T=T, **BASE, alma=CA.seguro(mal, menu), alma_muertes=5, nodo=1, menu=menu)
        return [c[1] for c in r['curitas']] == ['f'] * 5 and len(CA.INVALIDAS) == 5
    P.append(prueba("(H1) respuesta que NO es objeto -> 5 curitas (f), 5 invalidas, sin abortar",
                    lambda s: buzon(lambda res: 'a'), t0, sem=(1,)))
    P.append(prueba("(H2) respuesta sin clave `curita` -> 5 curitas (f), 5 invalidas",
                    lambda s: buzon(lambda res: {'motivo': 'me olvide'}), t0, sem=(1,)))
    P.append(prueba("(H3) curita fuera del menu ofrecido -> 5 curitas (f), 5 invalidas",
                    lambda s: buzon(lambda res: {'curita': 'a'}, 'cdef'), t0, sem=(1,)))
    P.append(prueba("(H4) el alma lanza excepcion -> 5 curitas (f), 5 invalidas",
                    lambda s: buzon(lambda res: (_ for _ in ()).throw(ValueError('buzon roto'))), t0, sem=(1,)))
    CA.INVALIDAS.clear()
    P.append(prueba("(I) determinismo con baraja del nodo",
                    lambda s: N(A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=1, conectado=1, menu='bcdef', nodo_baraja=1)) ==
                              N(A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=1, conectado=1, menu='bcdef', nodo_baraja=1)), t0))

    ok = sum(a for a, _ in P); tot = sum(b for _, b in P)
    print(f"\nIDENTIDAD organismo_alma2: {ok}/{tot}  [{time.time()-t0:.1f}s]")
    return 0 if ok == tot else 1


if __name__ == '__main__':
    sys.exit(main())
