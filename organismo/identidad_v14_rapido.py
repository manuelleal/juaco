"""Arnes de identidad del gemelo compilado del TRONCO v14 (regla 9 de EQUIPO.md):
organismo_v14_rapido.run(...) debe ser BIT A BIT igual (TODAS las claves, tras ida y vuelta por JSON) a
organismo_v14c_on.run(...), el organismo que el director decidio congelar como v14 (= v13 + hija dispersa +
puerta por codigo). Misma normalizacion que organismo/identidad_rapido.py:
N = json.loads(json.dumps(x, default=str)).

Que cubre (>= 40 corridas):
  (0) LA FIRMA: los defaults de organismo_v14_rapido.run son EXACTAMENTE los de organismo_v14c_on.run,
      parametro a parametro y en el mismo orden (inspect.signature). Es lo unico que distingue a este modulo
      del gemelo de la composicion, asi que se comprueba como un caso mas y no como un comentario.
  (a) LOS 7 ESCENARIOS DEL EXAMEN (E1, E2 = mundo con INVERSION, E2I, E2J, E2K, E2L, CTRL2) x 3 semillas a
      T=30000, con los defaults del tronco v14 (las dos perillas ON), todas las claves. 21 corridas.
  (b) INVERSION y ESTIMULO NUEVO C en semillas aparte y con los eventos en otro punto. 4 corridas.
  (c) T LARGO = 200000: base, inversion, nuevo C y A∩B=3. 4 corridas.
  (d) PERILLAS EXPLICITAMENTE APAGADAS == organismo_v13 (el tronco congelado): pasar mask_rel=0, puerta_pat=0,
      pat_shuf=0, pat_min=0 por encima de los defaults ON debe devolver el tronco v13 EXACTO, por los dos
      lados (organismo_v13 interpretado y organismo_v13_rapido). 3 escenarios x 2 referencias = 6 comparaciones.
      Comprueba de paso que la delegacion pasa las perillas y no las ignora.
  (e) PROCESO NUEVO QUE LEE LA CACHE: un subproceso limpio importa organismo_v14_rapido y reproduce 6 casos;
      se comparan clave a clave contra este proceso y se mide el primer run (con la cache borrada tarda ~18s;
      leyendola, < 1s). Se comprueba ademas que NO se genera una segunda cache numba: organismo_v14_rapido
      delega, asi que los .nbi/.nbc siguen siendo los de organismo_v14c_rapido y no aparece ninguno suyo.
  Y se mide la ACELERACION contra organismo_v14c_on a 100000 y 200000 pasos.

FUERA DE ALCANCE (declarado): el mundo de REGLA. organismo_v14gc.py es OTRO archivo, con otra firma
(mundo='regla', regla, fase2_en, sonda_final) y otras claves de salida; su gemelo no existe y este no lo
reemplaza. bateria_generaliza_v14c.py sigue usando el organismo interpretado.

OJO (ERR-28): organismo/ va PRIMERO en sys.path, siempre.
Uso:  cd organismo && python identidad_v14_rapido.py [--T 30000] [--rapido]
"""
import hashlib, inspect, json, os, subprocess, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)   # tronco: organismo/ -> bundle/
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]   # ERR-28: organismo/ PRIMERO

import organismo_v13 as V13                 # tronco v13 CONGELADO (interpretado)
import organismo_v13_rapido as V13R         # gemelo del tronco v13 (72/72 + 180/180)
import organismo_v14 as LENTO               # el TRONCO v14 CONGELADO, interpretado (las dos perillas ON por defecto)
import organismo_v14_rapido as RAPIDO       # el gemelo que se examina aqui

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 30000
T_LARGO = 200000
N = lambda x: json.loads(json.dumps(x, default=str))
APAG = dict(mask_rel=0, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=0, pat_shuf=0, pat_min=0, eta_s=0.015, clip_s=3.0)   # v14.1: el punto de v13 exige tambien sus constantes viejas


def escenarios(t):
    """Los del examen (bateria_v14c.py / corre_composicion_v14.py), con los eventos escalados a T."""
    return {
        'E1':    dict(),
        'E2':    dict(invertir_en=t // 2),                                                   # mundo con INVERSION
        'E2I':   dict(nuevo='C', nuevo_en=t // 3),
        'E2J':   dict(nuevo='D', nuevo_val='comida', solap_B=1, nuevo_en=t // 3),
        'E2K':   dict(nuevo='D', nuevo_val='comida', solap_B=2, nuevo_en=t // 3),
        'E2L':   dict(solap_AB=3),
        'CTRL2': dict(solap_AB=3, plast=False),
    }


SEEDS = (1, 2, 3)
EXTRA = [('inversion_temprana', 4, dict(invertir_en=T // 4)),
         ('inversion_tardia', 5, dict(invertir_en=3 * (T // 4))),
         ('nuevo_C_veneno', 4, dict(nuevo='C', nuevo_en=T // 2)),
         ('nuevo_C_comida', 5, dict(nuevo='C', nuevo_en=T // 2, nuevo_val='comida'))]
LARGO = [('base', 7, dict()), ('inversion', 7, dict(invertir_en=T_LARGO // 2)),
         ('nuevo_C', 8, dict(nuevo='C', nuevo_en=T_LARGO // 2)), ('solapAB3', 8, dict(solap_AB=3))]
APAGADAS = [('E1', 1, dict()), ('E2', 2, dict(invertir_en=T // 2)), ('E2L', 3, dict(solap_AB=3))]

HIJO = [('e_E1', 1, T, dict()), ('e_inversion', 2, T, dict(invertir_en=T // 2)),
        ('e_nuevo_C', 3, T, dict(nuevo='C', nuevo_en=T // 3)), ('e_solapAB3', 1, T, dict(solap_AB=3)),
        ('e_sin_plast', 2, T, dict(solap_AB=3, plast=False)), ('e_apagadas', 3, T, dict(**APAG))]


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def cmp(a, b, etiq, fallos):
    """a es la referencia: se comparan SUS claves (b puede tener mas, p.ej. las 4 nuevas frente al tronco v13)."""
    dif = [k for k in a if N(a[k]) != N(b.get(k))]
    if dif:
        fallos.append((etiq, dif))
        print(f"  DIFIERE {etiq}: {dif[:8]}", flush=True)
    return not dif


if __name__ == '__main__':
    if '--hijo' in sys.argv:   # (e) proceso nuevo: importa el gemelo, lee la cache de numba y reproduce HIJO
        t0 = time.time(); _ = RAPIDO.run(HIJO[0][1], T=HIJO[0][2], **HIJO[0][3]); t_primero = time.time() - t0
        out = {'t_primero': t_primero, 'res': {}}
        for etiq, s, t, kw in HIJO:
            out['res'][etiq] = N(RAPIDO.run(s, T=t, **kw))
        print('###JSON###' + json.dumps(out))
        sys.exit(0)

    t0 = time.time()
    print("arnes de identidad del gemelo compilado del TRONCO v14 (organismo_v14c_on)")
    for nom, p in [('organismo_v13 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
                   ('organismo_v13_rapido', os.path.join(RAIZ, 'organismo', 'organismo_v13_rapido.py')),
                   ('organismo_v14c_on', os.path.join(AQUI, 'organismo_v14.py')),
                   ('organismo_v14c_rapido', os.path.join(AQUI, 'organismo_v14c_rapido.py')),
                   ('organismo_v14_rapido', os.path.join(AQUI, 'organismo_v14_rapido.py')),
                   ('identidad_v14_rapido', os.path.abspath(__file__))]:
        print(f"  sha {nom:26s} {h16(p)}")
    print(f"  organismo_v13 importado desde: {V13.__file__}")
    print(f"  T = {T}   T_largo = {T_LARGO}")

    tc = time.time(); RAPIDO.run(1, T=2000); V13R.run(1, T=2000)
    log(f"compilacion/carga de cache numba: {time.time()-tc:.1f}s")

    fallos = []; n = 0
    ESC = escenarios(T)

    print("\n(0) la firma de organismo_v14_rapido.run == la de organismo_v14c_on.run (nombres, orden y defaults)")
    fa = inspect.signature(LENTO.run).parameters; fb = inspect.signature(RAPIDO.run).parameters
    dif_firma = ([f"orden/nombres: {list(fa)} vs {list(fb)}"] if list(fa) != list(fb) else
                 [f"{k}: {fa[k].default!r} vs {fb[k].default!r}" for k in fa if fa[k].default != fb[k].default])
    n += 1
    if dif_firma:
        fallos.append(('0/firma', dif_firma)); print(f"  DIFIERE 0/firma: {dif_firma[:6]}")
    else:
        print(f"  IDENTICA ({len(fa)} parametros; perillas ON: mask_rel={fb['mask_rel'].default}, "
              f"del_s={fb['del_s'].default}, del_c={fb['del_c'].default}, ema_c={fb['ema_c'].default}, "
              f"puerta_pat={fb['puerta_pat'].default}, pat_shuf={fb['pat_shuf'].default}, pat_min={fb['pat_min'].default})")

    print(f"\n(a) los 7 escenarios del examen x {len(SEEDS)} semillas a T={T}, todas las claves")
    tp = time.time()
    for en, ek in ESC.items():
        for s in SEEDS:
            a = LENTO.run(s, T=T, **ek); b = RAPIDO.run(s, T=T, **ek)
            n += 1; cmp(a, b, f"a/{en}/s{s}", fallos)
    log(f"  {len(ESC)*len(SEEDS)} corridas en {time.time()-tp:.1f}s")

    print("\n(b) inversion y estimulo nuevo en otras semillas y otros puntos del tiempo")
    tp = time.time()
    for en, s, ek in EXTRA:
        a = LENTO.run(s, T=T, **ek); b = RAPIDO.run(s, T=T, **ek)
        n += 1; cmp(a, b, f"b/{en}/s{s}", fallos)
    log(f"  {len(EXTRA)} corridas en {time.time()-tp:.1f}s")

    print(f"\n(c) T largo = {T_LARGO}")
    tp = time.time()
    for en, s, ek in LARGO:
        a = LENTO.run(s, T=T_LARGO, **ek); b = RAPIDO.run(s, T=T_LARGO, **ek)
        n += 1; cmp(a, b, f"c/{en}/s{s}", fallos)
    log(f"  {len(LARGO)} corridas a {T_LARGO} pasos en {time.time()-tp:.1f}s")

    print("\n(d) perillas EXPLICITAMENTE apagadas == organismo_v13 (tronco congelado), por los dos lados")
    tp = time.time()
    for en, s, ek in APAGADAS:
        b = RAPIDO.run(s, T=T, **ek, **APAG)
        n += 1; cmp(V13.run(s, T=T, **ek), b, f"d/v13_lento/{en}/s{s}", fallos)
        n += 1; cmp(V13R.run(s, T=T, **ek), b, f"d/v13_rapido/{en}/s{s}", fallos)
    log(f"  {2*len(APAGADAS)} comparaciones en {time.time()-tp:.1f}s")

    print("\n(e) proceso NUEVO que lee la cache de numba (subprocess)")
    aqui_res = {etiq: N(RAPIDO.run(s, T=t, **kw)) for etiq, s, t, kw in HIJO}
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    tp = time.time()
    pr = subprocess.run([sys.executable, os.path.abspath(__file__), '--hijo', '--T', str(T)],
                        capture_output=True, text=True, env=env, cwd=RAIZ, timeout=3600)
    t_sub = time.time() - tp
    linea = [l for l in pr.stdout.splitlines() if l.startswith('###JSON###')]
    if pr.returncode != 0 or not linea:
        n += 1; fallos.append(('e/subproceso', ['sin salida']))
        print(f"  DIFIERE e/subproceso: codigo {pr.returncode}\n{pr.stderr[-1200:]}")
    else:
        hijo = json.loads(linea[0][len('###JSON###'):])
        print(f"  proceso nuevo: {t_sub:.1f}s en total, primer run del gemelo {hijo['t_primero']:.2f}s "
              f"(con la cache borrada el mismo primer run tarda ~18s: la cache se leyo "
              f"{'SI' if hijo['t_primero'] < 3.0 else 'NO'})")
        for etiq, s, t, kw in HIJO:
            n += 1; cmp(aqui_res[etiq], hijo['res'][etiq], f"e/{etiq}", fallos)
    pc = os.path.join(AQUI, '__pycache__')
    nb = [f for f in os.listdir(pc) if f.endswith(('.nbi', '.nbc'))] if os.path.isdir(pc) else []
    print(f"  cache numba en {os.path.basename(pc)}/: {sum('v14c_rapido' in f for f in nb)} de organismo_v14c_rapido, "
          f"{sum(f.startswith('organismo_v14_rapido') for f in nb)} de organismo_v14_rapido "
          f"(delega: no debe generar ninguna propia)")

    print(f"\nIDENTIDAD {n - len(fallos)}/{n} corridas identicas   ({time.time()-t0:.1f}s)")

    if '--rapido' not in sys.argv:
        for t in (100000, T_LARGO):
            t1 = time.time(); LENTO.run(9, T=t); tl = time.time() - t1
            t1 = time.time(); RAPIDO.run(9, T=t); tr = time.time() - t1
            print(f"aceleracion a {t} pasos: organismo_v14c_on {tl:.2f}s -> gemelo {tr:.3f}s  x{tl/tr:.0f}")

    print("fuera de alcance: el mundo de REGLA (organismo_v14gc.py) es otro archivo con otra firma y otras "
          "claves; su gemelo no existe y este no lo reemplaza.")
    sys.exit(1 if fallos else 0)
