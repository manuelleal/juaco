"""Arnes de identidad del gemelo compilado de la composicion v14c (regla 9 de EQUIPO.md):
organismo_v14c_rapido.run(...) debe ser BIT A BIT igual (TODAS las claves, tras ida y vuelta por JSON) a
organismo_v14c.run(...). Misma normalizacion que organismo/identidad_rapido.py: N = json.loads(json.dumps(x, default=str)).

Que cubre:
  (a) REJILLA DE PERILLAS x ESCENARIOS DEL EXAMEN: las 4 combinaciones de perillas
        APAG  = las dos apagadas          (mask_rel=0, puerta_pat=0)   -> debe ser v13 EXACTO
        D_ON  = solo HIJA DISPERSA        (mask_rel=2, puerta_pat=0)
        B_ON  = solo PUERTA POR CODIGO    (mask_rel=0, puerta_pat=5, pat_min=1)
        COMP  = las DOS ON                (mask_rel=2, puerta_pat=5, pat_min=1)
      cruzadas con los 7 escenarios que usa bateria_v14c.py (E1, E2 = mundo con INVERSION, E2I, E2J, E2K, E2L,
      CTRL2) x 3 semillas = 84 corridas comparadas en todas las claves.
  (b) PERILLAS APAGADAS == EL TRONCO, por los dos lados (7 escenarios x 3 semillas x 2 = 42 comparaciones):
        organismo_v14c_rapido(APAG) == organismo_v13        (el tronco CONGELADO, interpretado)
        organismo_v14c_rapido(APAG) == organismo_v13_rapido (el gemelo del tronco, 72/72 + 180/180)
      en todas las claves del tronco (las 4 nuevas -- puerta_pat, pat_shuf, pat_min, n_cod -- no existen alli).
  (c) REJILLA DE RIESGO: las perillas en sus casos limite y cruzadas con las perillas de v13 que mas
      estresaron al gemelo del tronco (empates de argsort con solap_AB=3, nobj=1, sin plasticidad, sin memoria
      de rechazo, lam=0, div_signo=False, puerta=None, ema_c y del_s/del_c extremos, pat_shuf de control,
      puerta_pat=1 y 20, pat_min=0 y 3, kitchen sink). 14 configuraciones x 2 semillas = 28 corridas.
  (c2) HIJA DISPERSA CON LA MASCARA VIVA. En el mundo del tronco la mascara es INERTE con del_s=del_c=0.25
      (declarado de antemano en construye_v13D.py: 6 pixeles y un solo objeto), y la rama solo se ENTRA cuando
      la celda vio los dos signos de R. Para que el arnes no sea vacio en ese mecanismo se cruza del_s/del_c en
      los extremos con los escenarios donde la celda SI ve los dos signos (E2 inversion, E2L A∩B=3, E2K nuevo
      solapado): alli la mascara difiere de (P>0) en el 100% de las evaluaciones y cambia splits/split_t.
      3 deltas x 3 escenarios x 3 semillas = 27 corridas.
  (d) T LARGO: T=200000 (el techo del encargo) con las cuatro combinaciones de perillas, con inversion, con
      estimulo nuevo y con la hija dispersa viva.
  (e) PROCESO NUEVO QUE LEE LA CACHE: un subproceso limpio importa el gemelo y reproduce un subconjunto de
      (a)+(c); se compara clave a clave contra lo que dio este proceso y se mide cuanto tarda el primer run
      (si leyera la cache mal, recompilaria y se notaria en el tiempo).
  Y se mide la ACELERACION contra organismo_v14c a 100000 pasos.

FUERA DE ALCANCE (declarado): el MUNDO DE REGLA no se compila aqui. organismo_v14gc.py es OTRO archivo, con
OTRA firma (mundo='regla', regla, fase2_en, sonda_final) y OTRAS claves de salida (sondas a priori, primer
encuentro, sonda final); su gemelo seria organismo_v14gc_rapido.py y necesita su propio arnes. Este arnes NO
lo cubre y este gemelo NO lo reemplaza: bateria_generaliza_v14c.py sigue usando el organismo interpretado.

OJO (ERR-28): organismo/ va PRIMERO en sys.path, siempre.
Uso:  python experimentos/nivel10_composicion_v14/identidad_v14c_rapido.py [--T 30000] [--rapido]
"""
import hashlib, json, os, subprocess, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI]   # ERR-28: organismo/ PRIMERO

import organismo_v13 as V13                 # tronco CONGELADO (interpretado)
import organismo_v13_rapido as V13R         # gemelo del tronco (72/72 + 180/180)
import organismo_v14c as LENTO              # la composicion, interpretada
import organismo_v14c_rapido as RAPIDO      # el gemelo que se examina aqui

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 30000
T_LARGO = 200000
N = lambda x: json.loads(json.dumps(x, default=str))

APAG = dict(mask_rel=0, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=0, pat_shuf=0, pat_min=0)
D_ON = dict(mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=0, pat_shuf=0, pat_min=0)
B_ON = dict(mask_rel=0, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)
COMP = dict(mask_rel=2, del_s=0.25, del_c=0.25, ema_c=0.05, puerta_pat=5, pat_shuf=0, pat_min=1)
PERILLAS = {'apagadas': APAG, 'solo_hija_dispersa': D_ON, 'solo_puerta_codigo': B_ON, 'las_dos_ON': COMP}


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


RIESGO = {   # perillas nuevas en sus limites, y cruzadas con lo que mas estreso al gemelo del tronco
    'shuf_control':        dict(**{**COMP, 'pat_shuf': 1}),
    'shuf_solo_puerta':    dict(**{**B_ON, 'pat_shuf': 1}),
    'pat_min_0':           dict(**{**COMP, 'pat_min': 0}),
    'pat_min_3':           dict(**{**COMP, 'pat_min': 3}),
    'puerta_pat_1':        dict(**{**COMP, 'puerta_pat': 1}),
    'puerta_pat_20':       dict(**{**COMP, 'puerta_pat': 20}),
    'mask_rel_1_inerte':   dict(**{**COMP, 'mask_rel': 1}),
    'ema_c_alto':          dict(**{**COMP, 'ema_c': 0.5}),
    'ema_c_bajo':          dict(**{**COMP, 'ema_c': 0.002}),
    'puerta_none':         dict(**COMP, puerta=None),                       # la puerta no se consulta: las dos vias
    'div_signo_off':       dict(**COMP, div_signo=False, eta_s=0.0, puerta=None),
    'empates_solapAB3':    dict(**COMP, solap_AB=3),                        # maximo estres del fallback objmode de _code
    'nobj1_sin_rechazo':   dict(**COMP, nobj=1, memoria_rechazo=0),
    'kitchen_sink':        dict(mask_rel=2, del_s=0.4, del_c=0.1, ema_c=0.2, puerta_pat=3, pat_shuf=0, pat_min=2,
                                nobj=8, memoria_rechazo=100, mu_norm=False, eta_s=0.02, clip_s=2.0, lam=0.1, eta=0.05,
                                theta=0.3, costo=0.01, invertir_en=T // 2),   # con inversion: la rama D se entra de verdad
}

# (c2) La hija dispersa es INERTE en el mundo del tronco con del_s=del_c=0.25 (declarado en construye_v13D.py:
# 6 pixeles y un solo objeto, no hay nada irrelevante que ignorar), y ademas la rama solo se ENTRA cuando la
# celda vio las dos clases (zp>1e-6 Y zn>1e-6). Para que el arnes NO sea vacio en ese mecanismo, este bloque la
# cruza con los escenarios donde la celda SI ve los dos signos -- inversion (E2), A∩B=3 (E2L) y estimulo nuevo
# solapado (E2K) -- y con del_s/del_c en los extremos, donde la mascara resulta REALMENTE distinta de (P>0) y
# cambia splits/split_t. Medido: con (0,0) y (1,1) la mascara difiere en el 100% de las evaluaciones de la rama.
D_DELTAS = {'delta_0_0': dict(del_s=0.0, del_c=0.0), 'delta_1_1': dict(del_s=1.0, del_c=1.0),
            'delta_04_01': dict(del_s=0.4, del_c=0.1)}
SEEDS = (1, 2, 3)
SEEDS_RIESGO = (4, 5)

# lo que reproduce el proceso nuevo (e); debe poder serializarse tal cual
HIJO = [('e_apagadas_E1', 1, T, dict(**APAG)),
        ('e_las_dos_E2', 2, T, dict(**COMP, invertir_en=T // 2)),
        ('e_hija_E2L', 3, T, dict(**D_ON, solap_AB=3)),
        ('e_puerta_E2I', 1, T, dict(**B_ON, nuevo='C', nuevo_en=T // 3)),
        ('e_shuf', 4, T, dict(**{**COMP, 'pat_shuf': 1})),
        ('e_hija_viva_E2L', 5, T, dict(**{**COMP, 'del_s': 0.0, 'del_c': 0.0}, solap_AB=3)),
        ('e_kitchen', 5, T, RIESGO['kitchen_sink'])]


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def cmp(a, b, etiq, fallos, claves=None):
    """a es la referencia: se comparan SUS claves (b puede tener mas, p.ej. las 4 nuevas frente al tronco)."""
    ks = claves if claves is not None else list(a)
    dif = [k for k in ks if N(a[k]) != N(b.get(k))]
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
    print("arnes de identidad del gemelo compilado de la composicion v14c")
    for nom, p in [('organismo_v13 (congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v13.py')),
                   ('organismo_v13_rapido', os.path.join(RAIZ, 'organismo', 'organismo_v13_rapido.py')),
                   ('organismo_v14c', os.path.join(AQUI, 'organismo_v14c.py')),
                   ('organismo_v14c_rapido', os.path.join(AQUI, 'organismo_v14c_rapido.py')),
                   ('identidad_v14c_rapido', os.path.abspath(__file__))]:
        print(f"  sha {nom:26s} {h16(p)}")
    print(f"  organismo_v13 importado desde: {V13.__file__}")
    print(f"  T = {T}   (rejilla)   T_largo = {T_LARGO}")

    tc = time.time(); RAPIDO.run(1, T=2000); V13R.run(1, T=2000)
    log(f"compilacion/carga de cache numba: {time.time()-tc:.1f}s")

    fallos = []; n = 0
    ESC = escenarios(T)

    print(f"\n(a) organismo_v14c_rapido == organismo_v14c   ({len(PERILLAS)} perillas x {len(ESC)} escenarios x {len(SEEDS)} semillas, todas las claves)")
    for pn, pk in PERILLAS.items():
        tp = time.time()
        for en, ek in ESC.items():
            for s in SEEDS:
                kw = dict(**ek, **pk)
                a = LENTO.run(s, T=T, **kw); b = RAPIDO.run(s, T=T, **kw)
                n += 1; cmp(a, b, f"a/{pn}/{en}/s{s}", fallos)
        log(f"  {pn}: {len(ESC)*len(SEEDS)} corridas en {time.time()-tp:.1f}s")

    print(f"\n(b) perillas apagadas == el tronco   ({len(ESC)} escenarios x {len(SEEDS)} semillas x 2 referencias)")
    tp = time.time()
    for en, ek in ESC.items():
        for s in SEEDS:
            b = RAPIDO.run(s, T=T, **ek, **APAG)
            n += 1; cmp(V13.run(s, T=T, **ek), b, f"b/v13_lento/{en}/s{s}", fallos)
            n += 1; cmp(V13R.run(s, T=T, **ek), b, f"b/v13_rapido/{en}/s{s}", fallos)
    log(f"  {2*len(ESC)*len(SEEDS)} comparaciones en {time.time()-tp:.1f}s")

    print(f"\n(c) rejilla de riesgo   ({len(RIESGO)} configuraciones x {len(SEEDS_RIESGO)} semillas)")
    tp = time.time()
    for rn, rk in RIESGO.items():
        for s in SEEDS_RIESGO:
            a = LENTO.run(s, T=T, **rk); b = RAPIDO.run(s, T=T, **rk)
            n += 1; cmp(a, b, f"c/{rn}/s{s}", fallos)
    log(f"  {len(RIESGO)*len(SEEDS_RIESGO)} corridas en {time.time()-tp:.1f}s")

    D_ESC = {k: ESC[k] for k in ('E2', 'E2L', 'E2K')}   # donde la celda ve los DOS signos: la rama D se entra
    print(f"\n(c2) hija dispersa con la mascara realmente distinta de (P>0)   ({len(D_DELTAS)} deltas x {len(D_ESC)} escenarios x {len(SEEDS)} semillas)")
    tp = time.time()
    for dn, dk in D_DELTAS.items():
        for en, ek in D_ESC.items():
            for s in SEEDS:
                kw = dict(**ek, **{**COMP, **dk})
                a = LENTO.run(s, T=T, **kw); b = RAPIDO.run(s, T=T, **kw)
                n += 1; cmp(a, b, f"c2/{dn}/{en}/s{s}", fallos)
    log(f"  {len(D_DELTAS)*len(D_ESC)*len(SEEDS)} corridas en {time.time()-tp:.1f}s")

    print(f"\n(d) T largo = {T_LARGO}")
    tp = time.time()
    LARGO = [('apagadas', 7, dict(**APAG)), ('solo_hija_dispersa', 7, dict(**D_ON)),
             ('solo_puerta_codigo', 7, dict(**B_ON)), ('las_dos_ON', 7, dict(**COMP)),
             ('las_dos_ON+inversion', 8, dict(**COMP, invertir_en=T_LARGO // 2)),
             ('las_dos_ON+nuevo_C', 8, dict(**COMP, nuevo='C', nuevo_en=T_LARGO // 2)),
             ('hija_viva+inversion', 9, dict(**{**COMP, 'del_s': 0.0, 'del_c': 0.0}, invertir_en=T_LARGO // 2)),
             ('hija_viva+solapAB3', 9, dict(**{**COMP, 'del_s': 1.0, 'del_c': 1.0}, solap_AB=3))]
    for ln, s, lk in LARGO:
        a = LENTO.run(s, T=T_LARGO, **lk); b = RAPIDO.run(s, T=T_LARGO, **lk)
        n += 1; cmp(a, b, f"d/{ln}/s{s}", fallos)
    log(f"  {len(LARGO)} corridas a {T_LARGO} pasos en {time.time()-tp:.1f}s")

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
              f"(si recompilara serian ~10s: la cache se leyo {'SI' if hijo['t_primero'] < 3.0 else 'NO'})")
        for etiq, s, t, kw in HIJO:
            n += 1; cmp(aqui_res[etiq], hijo['res'][etiq], f"e/{etiq}", fallos)

    print(f"\nIDENTIDAD {n - len(fallos)}/{n} corridas identicas   ({time.time()-t0:.1f}s)")

    if '--rapido' not in sys.argv:
        tl0 = time.time(); LENTO.run(9, T=100000, **COMP); tl = time.time() - tl0
        tr0 = time.time(); RAPIDO.run(9, T=100000, **COMP); tr = time.time() - tr0
        tl0 = time.time(); LENTO.run(9, T=100000, **APAG); tl2 = time.time() - tl0
        tr0 = time.time(); RAPIDO.run(9, T=100000, **APAG); tr2 = time.time() - tr0
        print(f"aceleracion a 100000 pasos: las_dos_ON {tl:.2f}s -> {tr:.3f}s  x{tl/tr:.0f} ; "
              f"apagadas {tl2:.2f}s -> {tr2:.3f}s  x{tl2/tr2:.0f}")

    print("fuera de alcance: el mundo de REGLA (organismo_v14gc.py) es otro archivo con otra firma y otras "
          "claves; su gemelo no se compila ni se examina aqui.")
    sys.exit(1 if fallos else 0)
