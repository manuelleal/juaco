"""Arnes de identidad del GEMELO COMPILADO del bloque 2: organismo_f9c_rapido.run(...) debe ser BIT A BIT
igual (TODAS las claves, tras ida y vuelta por JSON) a organismo_f9c.run(...).

MISION: llegar a la AGI por este camino. Un gemelo que no sea bit a bit identico SOLO EXPLORA, nunca confirma
(regla 9 de registro/EQUIPO.md). Este arnes se corre y se entrega con el gemelo.

El gemelo del bloque 2 NO tiene bucle propio: delega en organismo_f9_rapido (gemelo del bloque 1, 138/138),
que lleva nodo_via / nodo_or / sesgo_fijo / f9c en el MISMO bucle, apagadas por defecto. Por eso aqui se
comprueban tres cosas:
  (1) LOS CATORCE BRAZOS de corre_bloque2.py x los DOS niveles de rep_acum, contra organismo_f9c.
  (2) EL ANCLA DEL BLOQUE 1: con nodo_via=0, nodo_or=0, sesgo_fijo=0 y f9c=0 el gemelo del bloque 2 es
      organismo_f9 (el instrumento del bloque 1, sha 3a821884394d66c9) bit a bit en sus nueve brazos.
  (3) CONTROLES QUE DEBEN DIFERIR: las perillas nuevas tienen que cambiar algo (ERR-38), y las guardias
      nuevas tienen que abortar donde abortan en el original.

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va primero en sys.path.
Uso:  python experimentos/nivel09_cuerpo_nuevo_b2/identidad_f9c_rapido.py [--T 20000] [--semillas a,b,c]
"""
import json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
B1 = os.path.join(RAIZ, 'experimentos', 'nivel09_cuerpo_nuevo')
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
sys.path[:0] = [AQUI, B1, N13, N11, os.path.join(RAIZ, 'organismo')]

import organismo_f9c as lento
import organismo_f9c_rapido as rapido
import organismo_f9 as B1LENTO
import corre_bloque2 as C2
import corre_f9 as CF

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 20000
SEEDS = ([int(x) for x in sys.argv[sys.argv.index('--semillas') + 1].split(',')]
         if '--semillas' in sys.argv else [1501, 1502, 1503])
N = lambda x: json.loads(json.dumps(x, default=str))

CONFIGS = {}
for _b in C2.ORDEN:
    for _a in C2.ACUM:
        CONFIGS[f'{_b}_acum{_a}'] = dict(C2.BRAZOS[_b], rep_acum=_a)
REL2 = dict(C2.BRAZOS['REL2b'])
CONTROLES = [
    ('REL2b != REL',      C2.BRAZOS['REL2b'], C2.BRAZOS['REL']),
    ('REL2 != REL2b',     C2.BRAZOS['REL2'], C2.BRAZOS['REL2b']),
    ('REL2b_BAR != REL2b', C2.BRAZOS['REL2b_BAR'], C2.BRAZOS['REL2b']),
    ('ORACULO != REL2b',  C2.BRAZOS['ORACULO'], C2.BRAZOS['REL2b']),
    ('CAUTELA != NADA',   C2.BRAZOS['CAUTELA'], C2.BRAZOS['NADA']),
    ('DOSIS != REL',      C2.BRAZOS['DOSIS'], C2.BRAZOS['REL']),
]
GUARDIAS = [
    ('nodo_via=3',        dict(REL2, nodo_via=3)),
    ('nodo_via sin nodo', dict(REL2, nodo=0, conectado=0)),
    ('nodo_or sin nodo',  dict(C2.BRAZOS['NADA'], nodo_or=1)),
    ('nodo_or sin vivo',  dict(REL2, nodo_or=1, vivo=0, n_nec=1, estims=('A', 'B'))),
]


def compara(a, b):
    return ([k for k in a if k not in b], [k for k in a if k in b and N(a[k]) != N(b[k])],
            [k for k in b if k not in a])


if __name__ == '__main__':
    print(f"ARNES DE IDENTIDAD — organismo_f9c_rapido vs organismo_f9c   (T={T}, semillas {SEEDS})")
    t0 = time.time(); rapido.run(1501, T=600, **C2.BRAZOS['REL2b']); print(
        f"compilacion / carga del cache de numba: {time.time() - t0:.1f}s")
    fallos = []; n = 0; tl = 0.0; tr = 0.0
    for nombre, kw in CONFIGS.items():
        for s in SEEDS:
            t0 = time.time(); a = lento.run(s, T=T, **kw); tl += time.time() - t0
            t0 = time.time(); b = rapido.run(s, T=T, **kw); tr += time.time() - t0
            falta, dif, extra = compara(a, b); n += 1
            if falta or dif or extra:
                fallos.append((nombre, s)); print(f"  DIFIERE {nombre} s{s}: falta={falta[:4]} dif={dif[:6]} extra={extra[:4]}")
                for k in dif[:3]:
                    print(f"      {k}: tronco {str(N(a[k]))[:160]}"); print(f"      {k}: gemelo {str(N(b[k]))[:160]}")
    print(f"\nIDENTIDAD (bloque 2): {n - len(fallos)}/{n} corridas identicas "
          f"({len(CONFIGS)} configuraciones x {len(SEEDS)} semillas, T={T}, todas las claves)")
    print(f"   tiempo total: tronco {tl:.1f}s, gemelo {tr:.1f}s -> x{tl / max(tr, 1e-9):.1f}")

    print("\nANCLA DEL BLOQUE 1 (perillas nuevas apagadas == organismo_f9, sha 3a821884394d66c9):")
    m = 0; na = 0
    for _b in CF.ORDEN:
        for s in SEEDS:
            a = B1LENTO.run(s, T=T, **CF.BRAZOS[_b]); b = rapido.run(s, T=T, **CF.BRAZOS[_b])
            na += 1; m += int(any(compara(a, b)))
    print(f"   {na - m}/{na} corridas identicas ({len(CF.ORDEN)} brazos del bloque 1 x {len(SEEDS)} semillas)")

    print("\nCONTROLES QUE DEBEN DIFERIR (las perillas nuevas tienen que cambiar algo — ERR-38):")
    mal = 0
    for etiq, ka, kb in CONTROLES:
        malos = [s for s in SEEDS if not any(compara(rapido.run(s, T=T, **ka), rapido.run(s, T=T, **kb)))]
        mal += len(malos)
        print(f"   {etiq:22s} -> {'DIFIERE (bien)' if not malos else f'IGUAL en {malos} (MAL)'}")
    print("GUARDIAS NUEVAS (el gemelo aborta donde aborta el original):")
    for etiq, kw in GUARDIAS:
        ra = rb = 'sin excepcion'
        try: lento.run(SEEDS[0], T=400, **kw)
        except BaseException as e: ra = type(e).__name__
        try: rapido.run(SEEDS[0], T=400, **kw)
        except BaseException as e: rb = type(e).__name__
        ok = ra == rb == 'SystemExit'; mal += int(not ok)
        print(f"   {etiq:20s} tronco {ra:14s} gemelo {rb:14s} {'OK' if ok else 'MAL'}")

    print("\nACELERACION a T=100000 (un proceso, sin Pool):")
    tot_l = tot_r = 0.0
    for b in ('REL2b', 'ORACULO', 'CAUTELA'):
        t0 = time.time(); a = lento.run(1501, T=100000, **C2.BRAZOS[b]); t_l = time.time() - t0
        t0 = time.time(); c = rapido.run(1501, T=100000, **C2.BRAZOS[b]); t_r = time.time() - t0
        ok = not any(compara(a, c)); tot_l += t_l; tot_r += t_r
        print(f"   {b:9s} tronco {t_l:6.2f}s  gemelo {t_r:6.3f}s  -> x{t_l / t_r:5.1f}   identidad a 100k: {'OK' if ok else 'FALLA'}")
        if not ok: fallos.append((b, 1501))
    print(f"   TOTAL     tronco {tot_l:6.2f}s  gemelo {tot_r:6.3f}s  -> x{tot_l / tot_r:5.1f}")

    print(f"\nVEREDICTO: identidad {n - len(fallos)}/{n} · ancla del bloque 1 {na - m}/{na} · "
          f"controles y guardias {len(CONTROLES) + len(GUARDIAS) - mal}/{len(CONTROLES) + len(GUARDIAS)}")
    sys.exit(1 if (fallos or m or mal) else 0)
