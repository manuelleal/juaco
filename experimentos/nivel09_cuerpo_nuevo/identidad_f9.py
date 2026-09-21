"""Arnes de identidad de organismo_f9 (FASE 9 — el cuerpo nuevo). Regla 2 de registro/EQUIPO.md.

MISION: llegar a la AGI por este camino. El arnes se corre y se pega ENTERO en el informe, con las perillas
APAGADAS, ANTES de mirar un solo numero del experimento.

Cadena: organismo_v14 (TRONCO CONGELADO v14.1) -> organismo_vivo -> _rep -> _rep2 -> _h1 -> organismo_alma
-> organismo_alma2 -> organismo_f9.

  (A) APAGADA: nodo_rel=0, con_desde=0, rep_acum=0, f9=0 == organismo_alma2 en los 5 modos de herencia de H-1
      y en los 3 brazos con alma del BLOQUE ALMA.  DEBE SER IDENTICO.
  (B) CADENA: vivo=0, n_nec=1 == organismo_v14 (TRONCO).  DEBE SER IDENTICO.
  (C) LA LINEA BASE DE LA FASE 9 ES LA DE H-1: el brazo NADA (alma nula, menu='f', nodo=0) == organismo_alma2
      con alma=None == organismo_vivo_h1, en todas las claves viejas.  DEBE SER IDENTICO.
  (D) ANTES DE LA PRIMERA LECTURA DEL NODO (T = el paso de la primera muerte, en el que todavia nadie
      nacio ni leyo): REL == REC en todo salvo el eco de configuracion, y lect_div = 0 en los dos.
      Ninguna linea nueva toca el estado ni el rng del mundo antes de que alguien lea.
  (E) DEBEN DIFERIR (si un control no cambia nada, no controla nada -- ERR-38):
      REL != REC · REL_BAR != REL · REL_AZAR != REL · REL_TARDE != REL · REL_TARDE != NADA ·
      rep_acum=1 != rep_acum=0 (en NADA y en REL) · M1 != NADA.
  (F) LA RELEVANCIA RELEVA: lect_div > 0 en REL, REL_FIJO y REL_AZAR, y lect_div == 0 en REC. Con nodo_lee
      enorme (nada que seleccionar) REL_FIJO == REC, y REL (viva) sigue difiriendo porque cambia el ORDEN.
  (G) rep_acum ES ACUMULAR, NO REGALAR: con rep_acum=1 los descendientes NO BAJAN nunca, y el contador se
      reinicia al morir (un cuerpo que nace no hereda el avance de su padre: el 1er descendiente nunca llega
      antes de rep_X pasos del nacimiento).
  (H) CONTABILIDAD (H1-8 entera) en los ocho brazos mortales x los dos niveles de rep_acum.
  (I) GUARDIAS: nodo_rel fuera de {0,1,2,3}; nodo_rel con nodo=0; con_desde con nodo=0; con_desde con
      conectado=1; f9=1 sin h1 -> SystemExit.
  (J) DETERMINISMO: dos llamadas iguales dan el mismo dict (los rng derivados son funcion de (seed,k)).

Un proceso, sin Pool (regla 3). T = 20000. OJO (ERR-28): organismo/ va primero en sys.path.
Uso:  python experimentos/nivel09_cuerpo_nuevo/identidad_f9.py
"""
import os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
sys.path[:0] = [AQUI, N13, N11, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_vivo_h1 as H1
import organismo_alma2 as A2
import organismo_f9 as F9
import corre_f9 as CF

T = 20000
SEM = (1, 2)
N, h16 = CF.N, CF.h16
B = CF.BRAZOS
GRANDE = CF.GRANDE
MODOS = {'RENACE': dict(muerte_real=0), 'NADA': dict(muerte_real=1, hereda='nada', dote=0.6),
         'M1': dict(muerte_real=1, hereda='M1', dote=0.6),
         'PARES': dict(muerte_real=1, hereda='M1+pares', dote=0.6),
         'BARAJA_H': dict(muerte_real=1, hereda='baraja', dote=0.6)}
BASE = dict(CF.CUERPO)
NUEVAS = {'alma_muertes', 'curitas', 'nodo_n', 'conectado_final', 'dote_final', 'umbral_final', 'hereda_final',
          'T_efectivo', 'miedo_inerte', 'vidas_cuerpo', 'desc_cuerpo', 'nodo_cola', 'alma_cfg', 'alma2', 'f9'}


def fija(c):
    return lambda res: {'curita': c, 'motivo': f'arnes: siempre ({c})'}


def compara(a, b, quitar=()):
    bb = {k: v for k, v in b.items() if k not in quitar}
    return ([k for k in a if k not in bb], [k for k in a if k in bb and N(a[k]) != N(bb[k])],
            [k for k in bb if k not in a])


def caso(etiq, fa, fb, t0, difiere=False, extra=None, sem=SEM):
    ok, det = 0, ''
    for s in sem:
        a, b = fa(s), fb(s)
        falta, dif, ext = compara(a, b)
        igual = (not falta and not dif and ((set(ext) <= extra) if extra is not None else (not ext)))
        ok += int(igual != difiere)
        if (falta or dif or (ext and extra is None)) and not det:
            det = f"  falta {falta[:3]} dif {dif[:4]} extra {sorted(ext)[:3]}"
    marca = 'DIFIERE (como debe)' if difiere else 'IDENTICO'
    print(f"  [{time.time()-t0:6.1f}s] {etiq:78s} {ok}/{len(sem)} {marca if ok == len(sem) else 'FALLA' + det}", flush=True)
    return ok, len(sem)


def prueba(etiq, f, t0, sem=SEM):
    ok = sum(int(bool(f(s))) for s in sem)
    print(f"  [{time.time()-t0:6.1f}s] {etiq:78s} {ok}/{len(sem)} {'OK' if ok == len(sem) else 'FALLA'}", flush=True)
    return ok, len(sem)


def lanza(f):
    try:
        f(); return False
    except SystemExit:
        return True


def coherente(r):
    mu = r['deaths']; v = r['vidas_h1']; o = r['origen_cuerpo']
    return (r['nacimientos'] == mu and len(v) == mu + 1 and len(r['desc_por_vida']) == mu + 1
            and len(o) == mu + 1 and sum(v) == r.get('T_efectivo', T) and sum(r['desc_por_vida']) == r['descendientes']
            and r['fundadores'] + 1 == sum(1 for g in o if not g))


def main():
    t0 = time.time(); P = []
    print(f"IDENTIDAD organismo_f9  (sha {h16(os.path.join(AQUI,'organismo_f9.py'))})")
    print(f"  origen organismo_alma2.py   sha {h16(os.path.join(N13,'organismo_alma2.py'))} (se espera 4fd616aeaf535e61)")
    print(f"  cadena organismo_vivo_h1.py sha {h16(os.path.join(N11,'organismo_vivo_h1.py'))} (se espera 9e99ff87b5e2db1e)")
    print(f"  TRONCO organismo_v14.py     sha {h16(os.path.join(RAIZ,'organismo','organismo_v14.py'))} (se espera feefc88b1fd8d434)")
    print(f"  T = {T} · semillas {SEM} · un proceso, sin Pool")

    print("\n(A) APAGADA: nodo_rel=0, con_desde=0, rep_acum=0, f9=0 == organismo_alma2")
    for mm, kw in MODOS.items():
        k = dict(BASE) | kw
        P.append(caso(f"(A) {mm}: f9 apagado == organismo_alma2", lambda s, x=k: A2.run(s, T=T, **x),
                      lambda s, x=k: F9.run(s, T=T, **x), t0))
    for c in ('f', 'a', 'b'):
        P.append(caso(f"(A) con alma ({c}), menu completo, nodo: f9 apagado == organismo_alma2",
                      lambda s, cc=c: A2.run(s, T=T, **BASE, alma=fija(cc), alma_muertes=GRANDE, nodo=1),
                      lambda s, cc=c: F9.run(s, T=T, **BASE, alma=fija(cc), alma_muertes=GRANDE, nodo=1), t0))
    P.append(caso("(A) con nodo barajado (el control de ALMA2): f9 apagado == organismo_alma2",
                  lambda s: A2.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=1, conectado=1,
                                   menu='bcdef', nodo_baraja=1),
                  lambda s: F9.run(s, T=T, **BASE, alma=fija('b'), alma_muertes=10, nodo=1, conectado=1,
                                   menu='bcdef', nodo_baraja=1), t0))

    print("\n(B) CADENA hasta el TRONCO")
    P.append(caso("(B) vivo=0, n_nec=1 == organismo_v14 (TRONCO CONGELADO v14.1)",
                  lambda s: V14.run(s, T=T), lambda s: F9.run(s, T=T, vivo=0, n_nec=1), t0))

    print("\n(C) LA LINEA BASE DE LA FASE 9 ES LA DE H-1 (si esto falla, las predicciones no tienen ancla)")
    P.append(caso("(C1) brazo NADA (alma nula, menu='f', nodo=0) == organismo_alma2 con alma=None",
                  lambda s: A2.run(s, T=T, **BASE), lambda s: F9.run(s, T=T, **B['NADA']), t0, extra=NUEVAS))
    P.append(caso("(C2) brazo NADA == organismo_vivo_h1 NADA_CM (el origen del origen)",
                  lambda s: H1.run(s, T=T, **BASE), lambda s: F9.run(s, T=T, **B['NADA']), t0, extra=NUEVAS))
    P.append(caso("(C3) brazo M1 == organismo_vivo_h1 M1_CM",
                  lambda s: H1.run(s, T=T, **dict(BASE, hereda='M1')), lambda s: F9.run(s, T=T, **B['M1']), t0, extra=NUEVAS))
    P.append(caso("(C4) brazo RENACE == organismo_vivo_h1 RENACE_CM (el ancla del instrumento)",
                  lambda s: H1.run(s, T=T, **dict(BASE, muerte_real=0)), lambda s: F9.run(s, T=T, **B['RENACE']), t0))

    print("\n(D) ANTES DE LA PRIMERA LECTURA DEL NODO nada nuevo toca el estado ni el rng del mundo")
    print("    (la clave `f9` se excluye: es el ECO DE LA CONFIGURACION -- nodo_rel 0 contra 1 -- no estado)")
    for s in SEM:
        r = F9.run(s, T=T, **B['REC'])
        t1 = r['vidas_h1'][0] if r['vidas_h1'] else 10   # el paso de la PRIMERA MUERTE: range(T) llega a T-1, asi que aqui todavia no murio nadie
        P.append(caso(f"(D1) T = primera muerte ({t1}) con semilla {s}: REL == REC salvo el eco de config",
                      lambda z, tt=t1: {k: v for k, v in F9.run(z, T=tt, **B['REC']).items() if k != 'f9'},
                      lambda z, tt=t1: {k: v for k, v in F9.run(z, T=tt, **B['REL']).items() if k != 'f9'},
                      t0, sem=(s,)))
        P.append(prueba(f"(D2) a T = primera muerte ({t1}), semilla {s}: REL no ha leido nada distinto "
                        f"(lect_div = 0 en los dos)",
                        lambda z, tt=t1: F9.run(z, T=tt, **B['REL'])['f9']['lect_div'] == 0 ==
                                         F9.run(z, T=tt, **B['REC'])['f9']['lect_div'], t0, sem=(s,)))

    print("\n(E) DEBEN DIFERIR: si un control no cambia nada, no controla nada (ERR-38)")
    for et, x, y in (("REL != REC", 'REL', 'REC'), ("REL_BAR != REL", 'REL_BAR', 'REL'),
                     ("REL_AZAR != REL", 'REL_AZAR', 'REL'), ("REL_FIJO != REL", 'REL_FIJO', 'REL'),
                     ("REL_FIJO != REC", 'REL_FIJO', 'REC'), ("REL_TARDE != REL", 'REL_TARDE', 'REL'),
                     ("REL_TARDE != NADA", 'REL_TARDE', 'NADA'), ("M1 != NADA", 'M1', 'NADA'),
                     ("REC != NADA", 'REC', 'NADA')):
        P.append(caso(f"(E) {et}", lambda s, a=x: F9.run(s, T=T, **B[a]),
                      lambda s, b=y: F9.run(s, T=T, **B[b]), t0, difiere=True))
    for br in ('NADA', 'REL'):
        P.append(caso(f"(E) rep_acum=1 != rep_acum=0 en {br}", lambda s, b=br: F9.run(s, T=T, **B[b]),
                      lambda s, b=br: F9.run(s, T=T, **dict(B[b], rep_acum=1)), t0, difiere=True))

    print("\n(F) LA RELEVANCIA RELEVA")
    P.append(prueba("(F1) REL: lect_div > 0 (si fuera 0 la perilla seria INERTE, ERR-38)",
                    lambda s: F9.run(s, T=T, **B['REL'])['f9']['lect_div'] > 0, t0))
    P.append(prueba("(F2) REC: lect_div == 0 y lecturas > 0 (la recencia nunca se aparta de la recencia)",
                    lambda s: (lambda f: f['lect_div'] == 0 and f['lecturas'] > 0)(F9.run(s, T=T, **B['REC'])['f9']), t0))
    P.append(prueba("(F3) REL_AZAR: lect_div > 0", lambda s: F9.run(s, T=T, **B['REL_AZAR'])['f9']['lect_div'] > 0, t0))
    P.append(prueba("(F3b) REL_FIJO: lect_div > 0", lambda s: F9.run(s, T=T, **B['REL_FIJO'])['f9']['lect_div'] > 0, t0))
    # Con nodo_lee enorme no hay NADA QUE SELECCIONAR, pero si hay algo que ORDENAR. La relevancia FIJA
    # (nodo_rel=3) devuelve el conjunto entero en orden cronologico -> es la recencia exacta. La relevancia
    # VIVA (nodo_rel=1) lee los mismos mensajes en OTRO ORDEN, y para una regla delta el orden importa: por eso
    # sigue difiriendo. Las dos cosas se prueban por separado.
    P.append(caso("(F4) con nodo_lee enorme: REL_FIJO == REC (mismo conjunto, mismo orden) salvo el eco de config",
                  lambda s: {k: v for k, v in F9.run(s, T=T, **dict(B['REC'], nodo_lee=10 ** 6)).items() if k != 'f9'},
                  lambda s: {k: v for k, v in F9.run(s, T=T, **dict(B['REL_FIJO'], nodo_lee=10 ** 6)).items() if k != 'f9'}, t0))
    P.append(prueba("(F5) con nodo_lee enorme, lect_div = 0 en REL_FIJO (no hay nada que seleccionar)",
                    lambda s: F9.run(s, T=T, **dict(B['REL_FIJO'], nodo_lee=10 ** 6))['f9']['lect_div'] == 0, t0))
    P.append(caso("(F6) con nodo_lee enorme, REL (viva) SIGUE difiriendo de REC: cambia el ORDEN, no solo el conjunto",
                  lambda s: {k: v for k, v in F9.run(s, T=T, **dict(B['REC'], nodo_lee=10 ** 6)).items() if k != 'f9'},
                  lambda s: {k: v for k, v in F9.run(s, T=T, **dict(B['REL'], nodo_lee=10 ** 6)).items() if k != 'f9'},
                  t0, difiere=True))

    print("\n(G) rep_acum ES ACUMULAR, NO REGALAR")
    P.append(prueba("(G1) rep_acum=1 nunca BAJA los descendientes (acumular no puede restar)",
                    lambda s: F9.run(s, T=T, **dict(B['REL'], rep_acum=1))['descendientes'] >=
                              F9.run(s, T=T, **B['REL'])['descendientes'], t0))

    def sin_regalo(r, repX=500):
        """El contador se reinicia AL MORIR: todo descendiente llega al menos rep_X pasos DESPUES del
        nacimiento del cuerpo que cierra su ventana. Si `_gv` cruzara la muerte, esto fallaria."""
        nac, acc = [], 0
        for v in r['vidas_h1']:
            nac.append(acc); acc += v
        for td in r['t_desc']:
            i = max(j for j, b in enumerate(nac) if b <= td)
            if td - nac[i] < repX:
                return False
        return True
    for br in ('NADA', 'REL'):
        P.append(prueba(f"(G2) {br} rep_acum=1: ningun descendiente llega antes de 500 pasos del nacimiento "
                        f"de su cuerpo (el contador se reinicia al morir)",
                        lambda s, bb=br: sin_regalo(F9.run(s, T=T, **dict(B[bb], rep_acum=1))), t0))

    print("\n(H) CONTABILIDAD (H1-8) en los ocho brazos x los dos niveles de rep_acum")
    for b in CF.ORDEN:
        if b == 'RENACE':
            continue
        for a in (0, 1):
            P.append(prueba(f"(H) {b} rep_acum={a}: contabilidad cierra",
                            lambda s, bb=b, aa=a: coherente(F9.run(s, T=T, **dict(B[bb], rep_acum=aa))), t0, sem=(1,)))

    print("\n(I) GUARDIAS")
    for et, f in (("nodo_rel=4", lambda s: F9.run(s, T=T, **dict(B['REL'], nodo_rel=4))),
                  ("nodo_rel=1 con nodo=0", lambda s: F9.run(s, T=T, **dict(B['NADA'], nodo_rel=1))),
                  ("con_desde con nodo=0", lambda s: F9.run(s, T=T, **dict(B['NADA'], con_desde=3))),
                  ("con_desde con conectado=1", lambda s: F9.run(s, T=T, **dict(B['REL'], con_desde=3)))):
        P.append(prueba(f"(I) {et} -> SystemExit", lambda s, ff=f: lanza(lambda: ff(s)), t0, sem=(1,)))
    # La guardia "f9=1 exige h1=1 y rep2=1" es INALCANZABLE por la cadena de guardias que ya existe
    # (f9 exige alma != None -> muerte_real=1 -> h1=1 -> rep2=1). Se declara y se prueba lo que SI se puede
    # probar: con alma=None, f9 se APAGA en silencio -- que es justo lo que hace identico el caso (A).
    P.append(prueba("(I) f9=1 con alma=None -> f9 se apaga y la clave `f9` NO aparece (por eso (A) es identico)",
                    lambda s: 'f9' not in F9.run(s, T=T, **dict(BASE, f9=1, nodo_rel=1, con_desde=3)), t0, sem=(1,)))

    print("\n(J) DETERMINISMO")
    for b in ('REL', 'REL_FIJO', 'REL_AZAR', 'REL_TARDE'):
        P.append(prueba(f"(J) {b}: dos llamadas iguales dan el mismo dict",
                        lambda s, bb=b: N(F9.run(s, T=T, **B[bb])) == N(F9.run(s, T=T, **B[bb])), t0, sem=(1,)))

    ok = sum(a for a, _ in P); tot = sum(b for _, b in P)
    print(f"\nIDENTIDAD organismo_f9: {ok}/{tot}  [{time.time()-t0:.1f}s]")
    return 0 if ok == tot else 1


if __name__ == '__main__':
    sys.exit(main())
