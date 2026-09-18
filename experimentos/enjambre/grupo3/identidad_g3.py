"""Arnes de identidad de organismo_g3 (MINI-EQUIPO 3, sala de enjambre; regla EQUIPO.md #2: instrumento nuevo
por anclas => identidad bit a bit obligatoria con la perilla nueva APAGADA, ANTES de mirar ningun numero).

organismo_g3.run(..., memoria=None) debe dar los MISMOS valores, en TODAS las claves de
experimentos/creacion_A/organismo_v13q5.run(...) (original, SOLO LEIDO, fae9c32b146fdbb4), tras ida y vuelta por
JSON (N = json.loads(json.dumps(x, default=str))). g3 anade 3 claves nuevas (mem_ganadora, mem_tabla, mem_vistas):
se compara con `solo=list(original)`, el mismo patron que usa identidad_v13q5_rapido.py (ancla (1), linea ~210)
para comparar un objeto con MAS claves contra su referencia de menos claves.

Que cubre:
  (0) LA FIRMA: los parametros de organismo_v13q5.run son, en el mismo orden y con el mismo default, un PREFIJO
      EXACTO de los de organismo_g3.run (que solo anade memoria, mem_alfa, mem_rho al final).
  (1) 9 CASOS OBLIGATORIOS (mundo de regla): xor01/px0/azar x semillas 1-3, T=30000, con los knobs del tronco
      v14.1 (eta_s=0.15, clip_s=10, regla_lenta='delta_signo', constante=True, lectura='cuadratica', puerta=3) --
      la MISMA configuracion que usara mini_g3.py. TODAS las claves de organismo_v13q5.
  (2) 5 CASOS BONUS: mundo 'AB' (tronco clasico), config por defecto, lab=True, lectura='lineal'+regla_lenta=
      'dos_canales' (el brazo mas antiguo de la linea), y seleccion='wta' -- para no fiarse de una sola config.
  (3) VALIDACION: memoria='cualquier_cosa' debe lanzar ValueError (el knob mal escrito no cae en silencio).
  (4) HUMO de que memoria SI hace algo cuando esta encendida: memoria='combi' y memoria='combi1' no truenan,
      escriben mem_vistas > 0, y dan un W_lenta_apriori DISTINTO del de memoria=None (si no, la rama no se probo).

REGLA: si (0)+(1)+(2) no dan 100%, el instrumento no se usa para nada. OJO (ERR-28): organismo/ va PRIMERO en
sys.path, siempre. Un solo proceso, sin multiprocessing.Pool (regla EQUIPO.md #3).
Uso: python experimentos/enjambre/grupo3/identidad_g3.py
"""
import inspect, json, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))                              # experimentos/enjambre/grupo3/
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))                 # bundle/
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI, os.path.join(RAIZ, 'experimentos', 'creacion_A')]   # ERR-28

import organismo_v13q5 as ORIGINAL   # experimentos/creacion_A/, solo se lee (fae9c32b146fdbb4)
import organismo_g3 as G3            # el instrumento de este mini-equipo

N = lambda x: json.loads(json.dumps(x, default=str))


def cmp(a, b, etiqueta, fallos):
    """Compara TODAS las claves de `a` (la referencia, con MENOS claves) contra `b` (g3). No exige mismo conjunto
    de claves: g3 anade mem_ganadora/mem_tabla/mem_vistas a proposito (ancla 5)."""
    dif = [k for k in a if N(a[k]) != N(b[k])]
    nuevas = sorted(k for k in b if k not in a)
    if dif:
        fallos.append((etiqueta, dif)); print(f"  DIFIERE {etiqueta}: {dif}", flush=True); return False, nuevas
    return True, nuevas


if __name__ == '__main__':
    import hashlib
    sha_o = hashlib.sha256(open(ORIGINAL.__file__, 'rb').read()).hexdigest()[:16]
    sha_g = hashlib.sha256(open(G3.__file__, 'rb').read()).hexdigest()[:16]
    print(f"organismo_v13q5.py sha {sha_o}  (esperado fae9c32b146fdbb4: {'OK' if sha_o == 'fae9c32b146fdbb4' else 'FALLA'})")
    print(f"organismo_g3.py    sha {sha_g}")
    fallos = []; n = 0; claves_nuevas_vistas = set()

    # ---------------------------------------------------------------- (0) la firma: prefijo exacto
    n += 1
    pa = [(p.name, p.default) for p in inspect.signature(ORIGINAL.run).parameters.values()]
    pb = [(p.name, p.default) for p in inspect.signature(G3.run).parameters.values()]
    firma_ok = (pb[:len(pa)] == pa) and [nm for nm, _ in pb[len(pa):]] == ['memoria', 'mem_alfa', 'mem_rho']
    if not firma_ok:
        fallos.append(('0/firma', ['firma distinta'])); print(f"  DIFIERE 0/firma:\n    {pa}\n    {pb}")
    else:
        print(f"(0) firma: los {len(pa)} parametros de organismo_v13q5 son prefijo exacto de organismo_g3; "
              f"anade {[nm for nm, _ in pb[len(pa):]]}")

    # ---------------------------------------------------------------- (1) 9 casos obligatorios: xor01/px0/azar x 3 semillas
    TR = dict(T=30000, mundo='regla', lectura='cuadratica', regla_lenta='delta_signo', constante=True,
              eta_s=0.15, clip_s=10.0, puerta=3)   # config de mini_g3.py (tronco v14.1)
    print(f"\n(1) 9 casos obligatorios (xor01/px0/azar x semillas 1-3, T=30000, config tronco v14.1)")
    ok1 = 0
    for regla in ('xor01', 'px0', 'azar'):
        for s in (1, 2, 3):
            kw = dict(TR, regla=regla)
            a = ORIGINAL.run(s, **kw); b = G3.run(s, memoria=None, **kw); n += 1
            ok, nuevas = cmp(a, b, f"1/{regla}/s{s}", fallos)
            ok1 += int(ok); claves_nuevas_vistas |= set(nuevas)
            print(f"  1/{regla:5s}/s{s}: {'OK' if ok else 'FALLA'}  ({len(a)} claves originales, +{len(nuevas)} nuevas)")
    print(f"  subtotal (1): {ok1}/9")

    # ---------------------------------------------------------------- (2) 5 casos bonus: otras configuraciones
    print(f"\n(2) 5 casos bonus (otras configuraciones, para no fiarse de una sola)")
    BONUS = {
        'AB_tronco':      dict(mundo='AB', T=30000, eta_s=0.015, puerta=3),
        'AB_defecto':     dict(mundo='AB', T=30000),
        'lab_encendido':  dict(TR, regla='xor01', lab=True),
        'lineal_dos_canales': dict(T=30000, mundo='regla', regla='px0', lectura='lineal', regla_lenta='dos_canales',
                                    constante=False, eta_s=0.15, clip_s=3.0, puerta=3),
        'seleccion_wta':  dict(TR, regla='xor01', seleccion='wta', sel_estad='cond'),
    }
    ok2 = 0
    for nombre, kw in BONUS.items():
        a = ORIGINAL.run(2, **kw); b = G3.run(2, memoria=None, **kw); n += 1
        ok, nuevas = cmp(a, b, f"2/{nombre}", fallos)
        ok2 += int(ok); claves_nuevas_vistas |= set(nuevas)
        print(f"  2/{nombre:20s} s2: {'OK' if ok else 'FALLA'}")
    print(f"  subtotal (2): {ok2}/5")
    print(f"\nclaves nuevas de g3 vistas en todos los casos: {sorted(claves_nuevas_vistas)}"
          f"  ({'OK, son exactamente las 3 esperadas' if claves_nuevas_vistas == {'mem_ganadora','mem_tabla','mem_vistas'} else 'INESPERADO'})")

    # ---------------------------------------------------------------- (3) validacion del knob
    print(f"\n(3) memoria='no_existe' debe lanzar ValueError")
    n += 1
    try:
        G3.run(1, T=1000, mundo='regla', regla='px0', memoria='no_existe')
        fallos.append(('3/validacion', ['no lanzo ValueError'])); print("  DIFIERE 3/validacion: no lanzo ValueError")
    except ValueError as e:
        print(f"  OK: ValueError({e})")

    # ---------------------------------------------------------------- (4) humo: memoria SI cambia el resultado
    print(f"\n(4) humo: memoria='combi'/'combi1' no truena, escribe mem_vistas>0 y CAMBIA W_lenta_apriori")
    base = dict(TR, T=30000, regla='xor01')
    r0 = G3.run(5, memoria=None, **base)
    for tipo in ('combi', 'combi1'):
        n += 1
        r = G3.run(5, memoria=tipo, **base)
        distinto = N(r['W_lenta_apriori']) != N(r0['W_lenta_apriori'])
        vistas_ok = r['mem_vistas'] > 0
        ok4 = distinto and vistas_ok
        if not ok4:
            fallos.append((f'4/{tipo}', [f'distinto={distinto} vistas_ok={vistas_ok} mem_vistas={r["mem_vistas"]}']))
        print(f"  memoria={tipo:7s}: mem_vistas={r['mem_vistas']:3d}  mem_ganadora={r['mem_ganadora']}  "
              f"W_lenta_apriori distinto de memoria=None: {'SI' if distinto else 'NO'}  {'OK' if ok4 else 'FALLA'}")

    print(f"\nIDENTIDAD {n - len(fallos)}/{n} comprobaciones OK")
    if fallos:
        print("FALLOS:")
        for f in fallos:
            print("  ", f)
    sys.exit(1 if fallos else 0)
