"""Arnes de identidad AMPLIADO del gemelo compilado (auditoria independiente, 17-sep-2026). NO reemplaza ni toca
organismo/identidad_rapido.py (original, 72/72 en 12 configuraciones x 6 semillas, 3/3 a 200000 pasos): este archivo
es un COMPLEMENTO con configuraciones de riesgo NO cubiertas por el original, elegidas tras una lectura linea a
linea de _bucle (organismo_v13_rapido.py) contra run() (organismo_v13.py, tronco congelado). Mismo metodo que el
arnes original: organismo_v13_rapido.run(...) debe ser BIT A BIT igual (todas las claves, tras ida y vuelta por
JSON) a organismo_v13.run(...).

Que cubre cada configuracion nueva y por que se eligio (riesgo identificado en la auditoria):
  - invertir_luego_nuevo: invertir_en Y nuevo JUNTOS por primera vez (el original solo los prueba por separado),
    en el orden que organismo_v13_rapido.run() SI admite (invertir_en < nuevo_en). Ver hallazgo H3 del informe:
    el orden inverso (nuevo_en < invertir_en) esta fuera de alcance por construccion (el tronco tiene un KeyError
    latente; el gemelo lo bloquea con ValueError) y NO se incluye aqui porque el tronco no completa esa corrida.
  - nobj_grande / nobj_uno: nobj=12 (turnover alto de objetos) y nobj=1 (el caso limite "olvido cuando objs tiene
    1 objeto": rng.integers(len(objs)) con len==1, y la rama de fallback de _see cuando el unico objeto esta
    rechazado).
  - rechazo_grande: memoria_rechazo=2000 (>> T/10), memoria de rechazo que cubre buena parte de la corrida.
  - theta_bajo_div0: div_signo=False (rama "elif", v9/v10) con theta=0.05 (divide casi con cualquier error).
  - plast_false_puerta_none y plast_false_nuevo: plast=False combinado con puerta=None y con nuevo/solap_B (el
    original solo prueba plast=False solo, con puerta=3 por defecto).
  - learn_false_T30k: learn=False a T=30000 con semillas 1-10 (la parte 3 del encargo ya cubre learn=False a
    T=50000 en semillas 11-15; esto añade una rejilla a T mas chico con mas semillas).
  - lam_cero_solo y lam_cero_div0: lam=0.0 aislado (el original solo lo cruza con nobj=6) y cruzado con div_signo=False.
  - eta_s_alto_puerta_none y eta_s_bajo_puerta_none: puerta=None (consulta siempre las DOS vias) con eta_s
    distinto del default 0.015 en ambas direcciones (el original solo prueba puerta=None con el eta_s por defecto).
  - clip_s_chico y clip_s_grande: clip_s nunca variado en el original (siempre 3.0 por defecto).
  - solapAB2 y solapAB3_max: solap_AB=2 y =3 (K=3: con 3 fuerza KW[0]==KW[1]==KW[2] EXACTAMENTE, filas identicas,
    lo que garantiza empates de argsort en la frontera del top-K en CASI todos los pasos — maximo estres al
    fallback objmode de _code). El original solo prueba solap_AB=1.
  - muerte_frecuente: costo=0.01 (5x default) para forzar muchas muertes/teletransportes (rng.integers(L) repetido
    en un camino de codigo que en el original rara vez se ejercita porque las muertes son escasas).
  - kitchen_sink: combinacion de 9 parametros no default a la vez, para ver si el gemelo compuesto (no solo cada
    perilla aislada) sigue siendo identico.

Ademas, al final (fuera de la rejilla principal, no cuenta para el veredicto de arriba) hay una demostracion
reproducible del UNICO caso donde se encontro una diferencia real: puerta negativo pero distinto de None
(p.ej. puerta=-1). Ver hallazgo H1 del informe.

Uso: python organismo/identidad_rapido_ampliada.py [--T 30000]
"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import organismo_v13 as lento, organismo_v13_rapido as rapido

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 30000
N = lambda x: json.loads(json.dumps(x, default=str))

CONFIGS = {
    'invertir_luego_nuevo': dict(invertir_en=T // 3, nuevo='C', nuevo_en=2 * (T // 3)),
    'nobj_grande':          dict(nobj=12),
    'nobj_uno':             dict(nobj=1),
    'rechazo_grande':       dict(memoria_rechazo=2000),
    'theta_bajo_div0':      dict(eta_s=0.0, puerta=None, div_signo=False, theta=0.05),
    'plast_false_puerta_none': dict(plast=False, puerta=None, eta_s=0.0),
    'plast_false_nuevo':    dict(plast=False, nuevo='D', nuevo_en=T // 2, solap_B=1, nuevo_val='comida'),
    'learn_false_T30k':     dict(learn=False),
    'lam_cero_solo':        dict(lam=0.0),
    'lam_cero_div0':        dict(lam=0.0, eta_s=0.0, puerta=None, div_signo=False),
    'eta_s_alto_puerta_none': dict(puerta=None, eta_s=0.05),
    'eta_s_bajo_puerta_none': dict(puerta=None, eta_s=0.003),
    'clip_s_chico':         dict(clip_s=1.0),
    'clip_s_grande':        dict(clip_s=10.0),
    'solapAB2':             dict(solap_AB=2),
    'solapAB3_max':         dict(solap_AB=3),
    'muerte_frecuente':     dict(costo=0.01),
    'kitchen_sink':         dict(nobj=8, memoria_rechazo=100, div_signo=False, mu_norm=False, eta_s=0.02,
                                  clip_s=2.0, theta=0.3, lam=0.1, eta=0.05),
}
SEEDS = list(range(1, 11))  # 1-10


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


if __name__ == '__main__':
    t0 = time.time(); rapido.run(1, T=2000); log(f"compilacion/carga de cache numba: {time.time()-t0:.1f}s")
    log(f"arnes ampliado: {len(CONFIGS)} configuraciones x {len(SEEDS)} semillas, T={T}")

    fallos = []; n = 0
    for nombre, kw in CONFIGS.items():
        t0 = time.time()
        for s in SEEDS:
            a = lento.run(s, T=T, **kw); b = rapido.run(s, T=T, **kw)
            dif = [k for k in a if N(a[k]) != N(b[k])]; n += 1
            if dif:
                fallos.append((nombre, s, dif))
                print(f"  DIFIERE {nombre} s{s}: {dif}")
        log(f"{nombre}: {len(SEEDS)} semillas en {time.time()-t0:.1f}s")

    print(f"identidad ampliada: {n - len(fallos)}/{n} corridas identicas (T={T}, {len(CONFIGS)} configuraciones x {len(SEEDS)} semillas)")
    veredicto_grilla = 'PASA' if not fallos else 'FALLA'
    print(f"veredicto de la rejilla de riesgo: {veredicto_grilla}")

    # --- Demostracion aparte (NO cuenta para el veredicto de arriba): hallazgo H1 del informe.
    # puerta=-1 (explicito, no None) colisiona con el centinela interno que organismo_v13_rapido.run() usa para
    # traducir puerta=None a _bucle (-1 if puerta is None else int(puerta)). Dentro de _bucle la condicion es
    # `puerta < 0`, que es cierta tanto para el centinela de None como para un -1 explicito: la DINAMICA de
    # entrenamiento (Wp/Wn/Wps/Wns, mordidas, divisiones) queda IDENTICA a puerta=None, mientras que el tronco,
    # que compara `puerta is None` (identidad de objeto, no un numero), SI distingue -1 de None y usa la via
    # rapida sola durante todo el entrenamiento (mismo resultado que puerta=0). El resultado final W del gemelo
    # se recalcula aparte con `puerta is None` (correcto ahi), asi que queda INTERNAMENTE INCONSISTENTE: W se lee
    # con la regla de puerta=-1 pero se calculo sobre pesos entrenados con la regla de puerta=None.
    print()
    print("=== demostracion aparte: puerta negativo distinto de None (hallazgo H1, no cuenta arriba) ===")
    demo_fallos = 0
    # Resuelto por el coordinador (17-sep 22:20): el gemelo RECHAZA puerta negativa explicita con ValueError (guardia H1).
    for s in [1, 2, 3]:
        try:
            rapido.run(s, T=T, puerta=-1); rechazado = False
        except ValueError:
            rechazado = True
        if not rechazado: demo_fallos += 1
        print(f"  puerta=-1 s{s}: gemelo {'RECHAZA con ValueError (guardia H1: correcto)' if rechazado else 'NO rechaza (H1 sin resolver)'}")
    print(f"guardia H1: {3 - demo_fallos}/3 semillas rechazadas con ValueError (esperado 3/3)")

    sys.exit(1 if fallos else 0)
