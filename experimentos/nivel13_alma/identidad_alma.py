"""Arnes de identidad de organismo_alma (BLOQUE ALMA, nivel 13). Regla 2 de registro/EQUIPO.md.

MISION: llegar a la AGI por este camino. Hoy: un alma externa que parcha al cuerpo cada vez que muere.

Cadena: organismo_v14 (TRONCO v14.1) -> organismo_vivo -> _rep -> _rep2 -> organismo_vivo_h1 -> organismo_alma.

  (A) APAGADA (alma=None): alma == organismo_vivo_h1 en los CINCO modos de H-1 x 2 cuerpos, TODAS las claves.
  (B) CADENA: reproduccion=0 == organismo_vivo; vivo=0, n_nec=1 == organismo_v14 (TRONCO).
  (C) ENCENDIDA E INERTE (alma que siempre contesta (f) NADA, nodo=0, alma_muertes enorme): las claves VIEJAS
      salen bit a bit y solo aparecen las claves nuevas del bloque. Si esto falla, la maquinaria del alma no es
      neutra y NADA de lo que mida el bloque vale.
  (D) ANTES DE LA PRIMERA MUERTE: con un alma que conecta al nodo y T anterior al primer paso de muerte, TODO es
      identico a h1 (ninguna linea nueva toca el estado ni el rng antes de que alguien muera).
  (E) DEBEN FALLAR (si no fallan, la curita es inerte y el instrumento esta roto): (a) conectar, (b) miedo,
      (c) dote, (d) umbral, (e) heredar -- cada una contra (f) NADA.
  (F) PARADA: con alma_muertes = N la corrida para en la muerte N (deaths == N, len(curitas) == N).
  (G) EL NODO SE LLENA Y SE LEE: con (a) en la primera muerte, nodo_n > 0 y conectado_final == 1; con nodo=0,
      nodo_n == 0 en 2/2.
  (H) MENU CERRADO: una curita fuera de {a..f} lanza SystemExit; los tres guardias del instrumento lanzan
      SystemExit; la invariante 0 < dote < rep_umbral se cumple en TODAS las curitas aplicadas.
  (I) DETERMINISMO: dos llamadas iguales dan el mismo dict.

Un proceso, sin Pool (regla 3). T = 20000. OJO (ERR-28): organismo/ va primero en sys.path.
Uso:  python experimentos/nivel13_alma/identidad_alma.py
"""
import json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
sys.path[:0] = [AQUI, N11, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_vivo as VV
import organismo_vivo_h1 as H1
import organismo_alma as AL
import mini_vivo as MV
import corre_vivo_rep as C1
import corre_vivo_rep2 as C2
import corre_alma as CA

T = 20000
SEM = (1, 2)
NUEVAS_ALMA = {'alma_muertes', 'curitas', 'nodo_n', 'conectado_final', 'dote_final', 'umbral_final',
               'hereda_final', 'T_efectivo', 'miedo_inerte', 'vidas_cuerpo', 'desc_cuerpo', 'nodo_cola', 'alma_cfg'}
MED_H1 = dict(C2.MED2, h1=1)
MODOS = {'RENACE': dict(muerte_real=0),
         'NADA':   dict(muerte_real=1, hereda='nada',     dote=0.6),
         'M1':     dict(muerte_real=1, hereda='M1',       dote=0.6),
         'PARES':  dict(muerte_real=1, hereda='M1+pares', dote=0.6),
         'BARAJA': dict(muerte_real=1, hereda='baraja',   dote=0.6)}
CUERPO = {'CM': 'CUELLO_MIN', 'VIVO': 'VIVO'}
BRAZOS = {f'{m}_{c}': dict(C1.BRAZOS[CUERPO[c]]) | MED_H1 | MODOS[m] for m in MODOS for c in CUERPO}
BASE = BRAZOS['NADA_CM']
GRANDE = 10 ** 9
N, h16 = C1.N, C1.h16


def fija(c):
    return lambda res: {'curita': c, 'motivo': f'arnes: siempre ({c})'}


def compara(a, b, quitar=()):
    bb = {k: v for k, v in b.items() if k not in quitar}
    return ([k for k in a if k not in bb], [k for k in a if k in bb and N(a[k]) != N(bb[k])], [k for k in bb if k not in a])


def caso(etiq, fa, fb, t0, difiere=False, quitar=(), extra=None, sem=SEM):
    ok, det = 0, ''
    for s in sem:
        a, b = fa(s), fb(s)
        falta, dif, ext = compara(a, b, quitar)
        igual = (not falta and not dif and ((set(ext) == extra) if extra is not None else (not ext)))
        ok += int(igual != difiere)
        if (falta or dif or (ext and extra is None)) and not det:
            det = f"  falta {falta[:3]} dif {dif[:4]} extra {sorted(ext)[:3]}"
    marca = 'DIFIERE (como debe)' if difiere else 'IDENTICO'
    print(f"  [{time.time()-t0:6.1f}s] {etiq:72s} {ok}/{len(sem)} {marca if ok == len(sem) else 'FALLA' + det}", flush=True)
    return ok, len(sem)


def prueba(etiq, f, t0, sem=SEM):
    ok = sum(int(bool(f(s))) for s in sem)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:72s} {ok}/{len(sem)} {'OK' if ok == len(sem) else 'FALLA'}", flush=True)
    return ok, len(sem)


def primera_muerte(s):
    r = H1.run(s, T=T, **BASE)
    return int(r['vidas_h1'][0])


def main():
    t0 = time.time(); P = []
    print(f"IDENTIDAD organismo_alma  (sha {h16(os.path.join(AQUI,'organismo_alma.py'))})")
    print(f"  origen organismo_vivo_h1.py sha {h16(os.path.join(N11,'organismo_vivo_h1.py'))} (se espera 9e99ff87b5e2db1e)")

    print("\n(A) APAGADA: alma=None == organismo_vivo_h1, todas las claves")
    for b, kw in BRAZOS.items():
        P.append(caso(f"(A) {b}", lambda s, k=kw: H1.run(s, T=T, **k), lambda s, k=kw: AL.run(s, T=T, **k), t0))

    print("\n(B) CADENA")
    P.append(caso("(B1) reproduccion=0 == organismo_vivo VIVO",
                  lambda s: VV.run(s, T=T, **MV.BRAZOS['VIVO']),
                  lambda s: AL.run(s, T=T, **dict(MV.BRAZOS['VIVO'], reproduccion=0)), t0))
    P.append(caso("(B2) vivo=0, n_nec=1 == organismo_v14 (TRONCO)",
                  lambda s: V14.run(s, T=T), lambda s: AL.run(s, T=T, vivo=0, n_nec=1), t0))

    print("\n(C) ENCENDIDA E INERTE: alma que siempre contesta (f), nodo=0 -> claves viejas bit a bit + las nuevas")
    P.append(caso("(C) alma=(f), nodo=0, alma_muertes=1e9 == h1 NADA_CM",
                  lambda s: H1.run(s, T=T, **BASE),
                  lambda s: AL.run(s, T=T, **BASE, alma=fija('f'), alma_muertes=GRANDE, nodo=0),
                  t0, extra=NUEVAS_ALMA))
    P.append(caso("(C2) alma=(f) CON nodo=1 (el nodo se llena y NADIE lo lee) == h1 NADA_CM",
                  lambda s: H1.run(s, T=T, **BASE),
                  lambda s: AL.run(s, T=T, **BASE, alma=fija('f'), alma_muertes=GRANDE, nodo=1),
                  t0, extra=NUEVAS_ALMA))

    print("\n(D) ANTES DE LA PRIMERA MUERTE: nada nuevo toca el estado ni el rng")
    P.append(caso("(D) T = paso de la 1a muerte, alma=(a) conectar == h1 NADA_CM",
                  lambda s: H1.run(s, T=primera_muerte(s), **BASE),
                  lambda s: AL.run(s, T=primera_muerte(s), **BASE, alma=fija('a'), alma_muertes=GRANDE),
                  t0, extra=NUEVAS_ALMA))

    print("\n(E) DEBEN FALLAR: cada curita contra (f) NADA (si no difiere, la curita es inerte)")
    ref = lambda s: AL.run(s, T=T, **BASE, alma=fija('f'), alma_muertes=GRANDE, nodo=1)
    for c, nom in (('a', 'conectar al nodo'), ('b', 'subir el miedo'), ('c', 'dote mayor'),
                   ('d', 'bajar el umbral'), ('e', 'heredar valores')):
        P.append(caso(f"(E) curita ({c}) {nom} != (f) NADA", ref,
                      lambda s, cc=c: AL.run(s, T=T, **BASE, alma=fija(cc), alma_muertes=GRANDE, nodo=1),
                      t0, difiere=True))

    print("\n(F) PARADA en la muerte N  ·  (G) el nodo  ·  (H) menu y guardias  ·  (I) determinismo")
    for Nm in (3, 10):
        P.append(prueba(f"(F) alma_muertes={Nm}: deaths == {Nm} y len(curitas) == {Nm}",
                        lambda s, n=Nm: (lambda r: r['deaths'] == n and len(r['curitas']) == n and r['T_efectivo'] <= T)
                        (AL.run(s, T=T, **BASE, alma=fija('f'), alma_muertes=n, nodo=1)), t0))
    P.append(prueba("(G1) con (a): nodo_n > 0 y conectado_final == 1",
                    lambda s: (lambda r: r['nodo_n'] > 0 and r['conectado_final'] == 1)
                    (AL.run(s, T=T, **BASE, alma=fija('a'), alma_muertes=10, nodo=1)), t0))
    P.append(prueba("(G2) con nodo=0: nodo_n == 0 aunque la curita sea (a)... (guardia) o (b)",
                    lambda s: (lambda r: r['nodo_n'] == 0 and r['conectado_final'] == 0)
                    (AL.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=0)), t0))
    P.append(prueba("(G3) el linaje conectado NO es el mismo que el no conectado (R0 o vidas cambian)",
                    lambda s: (AL.run(s, T=T, **BASE, alma=fija('a'), alma_muertes=10, nodo=1)['vidas_cuerpo']
                               != AL.run(s, T=T, **BASE, alma=fija('f'), alma_muertes=10, nodo=1)['vidas_cuerpo']), t0))

    def lanza(f):
        try:
            f(); return False
        except SystemExit:
            return True

    P.append(prueba("(H1) curita fuera del menu -> SystemExit",
                    lambda s: lanza(lambda: AL.run(s, T=T, **BASE, alma=fija('z'), alma_muertes=5)), t0))
    P.append(prueba("(H2) alma sin alma_muertes -> SystemExit",
                    lambda s: lanza(lambda: AL.run(s, T=T, **BASE, alma=fija('f'))), t0))
    P.append(prueba("(H3) alma no invocable -> SystemExit",
                    lambda s: lanza(lambda: AL.run(s, T=T, **BASE, alma=7, alma_muertes=5)), t0))
    P.append(prueba("(H4) conectado=1 con nodo=0 -> SystemExit",
                    lambda s: lanza(lambda: AL.run(s, T=T, **BASE, alma=fija('f'), alma_muertes=5, nodo=0, conectado=1)), t0))
    P.append(prueba("(H5) alma con muerte_real=0 es INERTE (no lanza, no aparecen claves nuevas)",
                    lambda s: 'curitas' not in AL.run(s, T=T, **BRAZOS['RENACE_CM'], alma=fija('a'), alma_muertes=5), t0))
    P.append(prueba("(H6) invariante 0 < dote < rep_umbral en TODAS las curitas (c) y (d), 40 muertes",
                    lambda s: all(0 < c[3] < c[4] for cc in
                                  (AL.run(s, T=T, **BASE, alma=fija('c'), alma_muertes=40, nodo=1)['curitas'],
                                   AL.run(s, T=T, **BASE, alma=fija('d'), alma_muertes=40, nodo=1)['curitas'])
                                  for c in cc), t0))
    P.append(prueba("(I) determinismo: dos llamadas iguales dan el mismo dict",
                    lambda s: N(AL.run(s, T=T, **BASE, alma=fija('a'), alma_muertes=10, nodo=1)) ==
                              N(AL.run(s, T=T, **BASE, alma=fija('a'), alma_muertes=10, nodo=1)), t0))

    ok = sum(a for a, _ in P); tot = sum(b for _, b in P)
    print(f"\nIDENTIDAD organismo_alma: {ok}/{tot}  [{time.time()-t0:.1f}s]")
    return 0 if ok == tot else 1


if __name__ == '__main__':
    sys.exit(main())
