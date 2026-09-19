"""Arnes de identidad de organismo_vivo_h1 (H-1: la muerte que mata). Regla 2 de registro/EQUIPO.md.

MISION: llegar a la AGI por este camino. Hoy: que la muerte mate de verdad, para que el linaje signifique algo.

Cadena de origen: organismo_v14 (TRONCO, v14.1) -> organismo_vivo -> organismo_vivo_rep -> organismo_vivo_rep2 -> organismo_vivo_h1.

  (A) APAGADA (muerte_real=0, h1=0): h1 == organismo_vivo_rep2 en los 7 brazos del bloque 2, todas las claves.
  (B) CADENA: reproduccion=0 == organismo_vivo; vivo=0, n_nec=1 == organismo_v14 (base e inversion).
  (C) ENCENDIDA de solo lectura (h1=1, muerte_real=0): claves viejas bit a bit + exactamente 15 nuevas, y coherencia
      contable (len(desc_por_vida) = muertes+1, suma = descendientes, suma(vidas_h1) = T).
  (D) ANTES DE LA PRIMERA MUERTE: con muerte_real=1 y T = paso de la primera muerte, TODO es identico a rep2
      (ninguna linea nueva consume el rng DEL MUNDO ni toca el estado antes de que alguien muera).
  (E) MUERE DE VERDAD: coherencia contable en los cuatro modos de herencia.
  (F) DETERMINISMO: dos llamadas iguales dan el mismo dict (los rng derivados son funcion de (seed, k)).
  (G) EL BARAJADO BARAJA: permutaciones no identidad en 'baraja' y ninguna en los demas.
  (H) DEBEN FALLAR: NADA != RENACE, M1 != NADA, M1+PARES != M1, BARAJA != M1, dote 0.3 != dote 0.6.
  (I) GUARDIAS: seis combinaciones prohibidas deben lanzar SystemExit.

Un proceso, sin Pool (regla 3). T = 20000. OJO (ERR-28): organismo/ va primero en sys.path.
Uso:  python experimentos/nivel11_mundo_vivo/identidad_vivo_h1.py
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_vivo as VV
import organismo_vivo_rep2 as V2
import organismo_vivo_h1 as H1
import mini_vivo as MV
import corre_vivo_rep2 as C2

T = 20000
SEM = (1, 2)
NUEVAS_H1 = {'muerte_real', 'hereda', 'dote', 'nacimientos', 'fundadores', 'desc_fund', 'desc_por_vida', 'vidas_h1',
             'origen_cuerpo', 'suma_vidas', 'cola_final', 'cola_desborde', 't_fund', 'baraja_identidad', 'h1'}
MODOS = ('nada', 'M1', 'M1+pares', 'baraja')
DOTE = 0.6


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def compara(a, b, quitar=()):
    bb = {k: v for k, v in b.items() if k not in quitar}
    return ([k for k in a if k not in bb], [k for k in a if k in bb and N(a[k]) != N(bb[k])], [k for k in bb if k not in a])


def caso(etiq, f_a, f_b, t0, debe_diferir=False, quitar=(), extra_esperado=None, sem=SEM):
    ok, det = 0, ''
    for s in sem:
        a, b = f_a(s), f_b(s)
        falta, dif, extra = compara(a, b, quitar)
        igual = (not falta and not dif and
                 ((set(extra) == extra_esperado) if extra_esperado is not None else (not extra)))
        ok += int(igual != debe_diferir)
        if (falta or dif or (extra and extra_esperado is None)) and not det:
            det = f"  falta {falta[:3]} dif {dif[:4]} extra {extra[:3]}"
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    print(f"  [{time.time()-t0:6.1f}s] {etiq:64s} {ok}/{len(sem)} {marca if ok == len(sem) else 'FALLA' + det}", flush=True)
    return ok, len(sem)


def kw_h1(brazo, **extra):
    return dict(C2.BRAZOS[brazo], h1=1, **extra)


def kw_muere(brazo, hereda, **extra):
    return dict(C2.BRAZOS[brazo], h1=1, muerte_real=1, hereda=hereda, dote=DOTE) | dict(extra)


def coherente(r, Ti):
    v, o, d = r['vidas_h1'], r['origen_cuerpo'], r['desc_por_vida']
    return dict(nac=(r['nacimientos'] == (r['deaths'] if r['muerte_real'] else 0)),
                largos=(len(v) == len(o) == len(d) == r['deaths'] + 1),
                vidas=(sum(v) == Ti and r['suma_vidas'] + r['vida_final'] == Ti),
                desc=(sum(d) == r['descendientes']),
                fund=(r['fundadores'] + 1 == o.count(0) if r['muerte_real'] else r['fundadores'] == 0),
                topes=(r['desc_fund'] <= r['descendientes'] and r['fundadores'] <= max(r['nacimientos'], 1) and r['cola_final'] >= 0))


if __name__ == '__main__':
    t0 = time.time()
    for nom, p in [('organismo_v14 (TRONCO congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
                   ('organismo_vivo.py', os.path.join(AQUI, 'organismo_vivo.py')),
                   ('organismo_vivo_rep.py', os.path.join(AQUI, 'organismo_vivo_rep.py')),
                   ('organismo_vivo_rep2.py (origen)', os.path.join(AQUI, 'organismo_vivo_rep2.py')),
                   ('construye_vivo_h1.py', os.path.join(AQUI, 'construye_vivo_h1.py')),
                   ('organismo_vivo_h1.py', os.path.join(AQUI, 'organismo_vivo_h1.py'))]:
        print(f"  sha {nom:36s} {h16(p)}")
    print(f"  T = {T}, semillas {SEM}, dote {DOTE}, UN proceso\n")
    ok = tot = 0

    print("(A) APAGADA (muerte_real=0, h1=0): organismo_vivo_h1 == organismo_vivo_rep2, todas las claves, 7 brazos del bloque 2")
    for b in C2.ORDEN:
        a, n = caso(f'(A) {b}', lambda s, b=b: V2.run(s, T=T, **C2.BRAZOS[b]), lambda s, b=b: H1.run(s, T=T, **C2.BRAZOS[b]), t0)
        ok += a; tot += n

    print("\n(B) CADENA hacia atras")
    a, n = caso('(B1) reproduccion=0 (VIVO) == organismo_vivo', lambda s: VV.run(s, T=T, **MV.BRAZOS['VIVO']),
                lambda s: H1.run(s, T=T, **MV.BRAZOS['VIVO']), t0); ok += a; tot += n
    a, n = caso('(B2) TODAS las perillas H-1 encendidas con la maestra apagada (inertes)', lambda s: VV.run(s, T=T, **MV.BRAZOS['VIVO']),
                lambda s: H1.run(s, T=T, **MV.BRAZOS['VIVO'], reproduccion=0, rep_mide=1, rep2=1, h1=1,
                                 muerte_real=1, hereda='M1+pares', dote=0.9, cola_max=3), t0); ok += a; tot += n
    a, n = caso('(B3) vivo=0, n_nec=1 == organismo_v14 (TRONCO)', lambda s: V14.run(s, T=T),
                lambda s: H1.run(s, T=T, vivo=0, n_nec=1), t0); ok += a; tot += n

    print("\n(C) ENCENDIDA de solo lectura (h1=1, muerte_real=0): claves viejas bit a bit + exactamente 15 nuevas")
    for b in ('VIVO', 'CUELLO_MIN'):
        a, n = caso(f'(C) {b} + h1', lambda s, b=b: V2.run(s, T=T, **C2.BRAZOS[b]), lambda s, b=b: H1.run(s, T=T, **kw_h1(b)),
                    t0, extra_esperado=NUEVAS_H1); ok += a; tot += n
        c = 0
        for s in SEM:
            r = H1.run(s, T=T, **kw_h1(b))
            d = coherente(r, T); c += int(all(d.values()))
            print(f"        {b:12s} s{s}: muertes {r['deaths']}, desc {r['descendientes']}, "
                  f"suma(vidas_h1) {sum(r['vidas_h1'])} = T -> {'coherente' if all(d.values()) else '*** ' + str(d)}")
        ok += c; tot += len(SEM)

    print("\n(D) ANTES DE LA PRIMERA MUERTE: con muerte_real=1, T = paso de la primera muerte -> IDENTICO a rep2")
    for b in ('VIVO', 'CUELLO_MIN'):
        tm = {s: V2.run(s, T=T, **C2.BRAZOS[b])['vidas'][0] for s in SEM}
        print(f"        {b:12s} primera muerte en t = {tm}")
        a, n = caso(f'(D) {b} muerte_real=1 hasta la primera muerte', lambda s, b=b, tm=tm: V2.run(s, T=tm[s], **C2.BRAZOS[b]),
                    lambda s, b=b, tm=tm: H1.run(s, T=tm[s], **kw_muere(b, 'M1+pares')), t0, quitar=NUEVAS_H1); ok += a; tot += n

    print("\n(E) MUERE DE VERDAD: coherencia contable en los cuatro modos de herencia (CUELLO_MIN)")
    for her in MODOS:
        c = 0
        for s in SEM:
            r = H1.run(s, T=T, **kw_muere('CUELLO_MIN', her))
            d = coherente(r, T); c += int(all(d.values()))
            print(f"        {her:9s} s{s}: nac {r['nacimientos']} = muertes {r['deaths']}; desc {r['descendientes']} "
                  f"(fundaciones {r['fundadores']}, heredados {r['nacimientos']-r['fundadores']}, regalo {r['desc_fund']}); "
                  f"R0 {r['descendientes']/(r['deaths']+1):.3f}  -> {'coherente' if all(d.values()) else '*** ' + str(d)}")
        ok += c; tot += len(SEM)

    print("\n(F) DETERMINISMO (los rng derivados son funcion de (seed, k), no del reloj)")
    for her in ('nada', 'baraja'):
        r1 = N(H1.run(1, T=T, **kw_muere('VIVO', her))); r2 = N(H1.run(1, T=T, **kw_muere('VIVO', her)))
        ok += int(r1 == r2); tot += 1
        print(f"        {her:9s} dos llamadas identicas -> {'IGUAL' if r1 == r2 else '*** DISTINTO'}")

    print("\n(G) EL BARAJADO BARAJA (permutacion nueva por parto, rng propio)")
    for her in ('nada', 'M1', 'M1+pares', 'baraja'):
        r = H1.run(1, T=T, **kw_muere('CUELLO_MIN', her))
        her_n = r['nacimientos'] - r['fundadores']
        esp = (r['baraja_identidad'] < max(her_n, 1)) if her == 'baraja' else (r['baraja_identidad'] == 0)
        ok += int(esp); tot += 1
        print(f"        {her:9s} nacimientos heredados {her_n:3d}, permutaciones identidad {r['baraja_identidad']:3d} -> {'OK' if esp else '*** FALLA'}")

    print("\n(H) CONTROLES QUE DEBEN FALLAR (si alguno sale IDENTICO, la perilla es inerte y el instrumento esta roto)")
    PARES = [('NADA != RENACE', lambda s: H1.run(s, T=T, **kw_h1('CUELLO_MIN')), lambda s: H1.run(s, T=T, **kw_muere('CUELLO_MIN', 'nada'))),
             ('M1 != NADA', lambda s: H1.run(s, T=T, **kw_muere('CUELLO_MIN', 'nada')), lambda s: H1.run(s, T=T, **kw_muere('CUELLO_MIN', 'M1'))),
             ('M1+PARES != M1', lambda s: H1.run(s, T=T, **kw_muere('CUELLO_MIN', 'M1')), lambda s: H1.run(s, T=T, **kw_muere('CUELLO_MIN', 'M1+pares'))),
             ('BARAJA != M1', lambda s: H1.run(s, T=T, **kw_muere('CUELLO_MIN', 'M1')), lambda s: H1.run(s, T=T, **kw_muere('CUELLO_MIN', 'baraja'))),
             ('dote 0.3 != dote 0.6 (NADA)', lambda s: H1.run(s, T=T, **kw_muere('CUELLO_MIN', 'nada')),
              lambda s: H1.run(s, T=T, **kw_muere('CUELLO_MIN', 'nada', dote=0.3)))]
    for etiq, fa, fb in PARES:
        a, n = caso(f'(H) {etiq}', fa, fb, t0, debe_diferir=True); ok += a; tot += n

    print("\n(I) GUARDIAS: seis combinaciones prohibidas deben lanzar SystemExit")
    MALAS = [("hereda desconocido", dict(h1=1, muerte_real=1, hereda='M2')),
             ("hereda sin muerte_real", dict(h1=1, hereda='M1')),
             ("muerte_real sin h1", dict(muerte_real=1)),
             ("h1 sin rep2", dict(h1=1, rep2=0)),
             ("dote >= rep_umbral", dict(h1=1, muerte_real=1, dote=1.0)),
             ("dote con rep_coste", dict(h1=1, muerte_real=1, dote=0.6, rep_coste=0.4))]
    for etiq, extra in MALAS:
        base = dict(C2.BRAZOS['CUELLO_MIN']); base.update(extra)
        try:
            H1.run(1, T=200, **base); salto = False
        except SystemExit:
            salto = True
        ok += int(salto); tot += 1
        print(f"        {etiq:26s} -> {'SystemExit (como debe)' if salto else '*** NO LANZO'}")

    print(f"\nIDENTIDAD {ok}/{tot}" + ("  -> el paquete puede correr." if ok == tot else "  -> NO se corre nada hasta que sea 100%."))
    sys.exit(0 if ok == tot else 1)
