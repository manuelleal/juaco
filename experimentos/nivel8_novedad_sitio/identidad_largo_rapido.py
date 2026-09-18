"""Arnes de identidad del gemelo compilado del mundo largo: mundo_largo_n_rapido.run(...) debe ser BIT A BIT igual
(todas las claves, tras ida y vuelta por JSON) a
  - mundo_largo.run(...)    en las configuraciones de corre_mundo_largo.py (V13, MAPA, REC_V13, REC_MAPA y el control
    de identidad pool=None == mundo_mapa). La UNICA clave que el gemelo puede anadir es 'nov_diag' (como mundo_largo_n).
  - mundo_largo_n.run(...)  en los SEIS brazos de corre_novedad.py (V13, MAPA, MAPA_NOV, MAPA_NOV_BAR, MAPA_NOV_CTE,
    MAPA_NOV_ALTA) y en los dos controles de su serie --alta (gamma_N=1.8 con nov_barajada y con nov_cte), todas las claves.
Dos rejillas: ANCHA (todas las configuraciones, --T corto) y LARGA (dos brazos con mapa a T=200000, el T real del
runner). Comprueba antes, como pide la regla 9 de registro/EQUIPO.md, que un proceso NUEVO lee el cache de numba sin
segmentar (el gemelo no tiene funciones recursivas con cache=True). Un solo proceso, sin Pool (regla 3).
Uso: python experimentos/nivel8_novedad_sitio/identidad_largo_rapido.py [--T 30000] [--Tlargo 200000] [--semillas 3] [--solo-ancha]
"""
import sys, os, json, time, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo'),
                os.path.join(RAIZ, 'experimentos', 'nivel6_mapa'), os.path.join(RAIZ, 'organismo')]
import mundo_largo as largo, mundo_largo_n as largo_n, mundo_largo_n_rapido as rapido
from corre_mundo_largo import pool_de, sitios_de, T_NUEVO, T_INV

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 30000
TL = int(sys.argv[sys.argv.index('--Tlargo') + 1]) if '--Tlargo' in sys.argv else 200000
NS = int(sys.argv[sys.argv.index('--semillas') + 1]) if '--semillas' in sys.argv else 3
N = lambda x: json.loads(json.dumps(x, default=str))
SEEDS = list(range(1, NS + 1))

# corre_mundo_largo.py: se comparan contra mundo_largo (clave extra permitida: nov_diag)
BRAZOS_LARGO = {
    'V13':      dict(usa_M=False),
    'MAPA':     dict(usa_M=True),
    'REC_V13':  dict(usa_M=False, reciclado=True),
    'REC_MAPA': dict(usa_M=True, reciclado=True),
}
# corre_novedad.py: se comparan contra mundo_largo_n (todas las claves)
BRAZOS_NOV = {
    'V13':           dict(usa_M=False),
    'MAPA':          dict(usa_M=True),
    'MAPA_NOV':      dict(usa_M=True, gamma_N=0.6, tau_N=4000.0),
    'MAPA_NOV_BAR':  dict(usa_M=True, gamma_N=0.6, tau_N=4000.0, nov_barajada=True),
    'MAPA_NOV_CTE':  dict(usa_M=True, gamma_N=0.6, tau_N=4000.0, nov_cte=True),
    'MAPA_NOV_ALTA': dict(usa_M=True, gamma_N=1.8, tau_N=4000.0),
    # serie --alta de corre_novedad.py (enmienda 1): la misma dosis 1.8 en los dos controles
    'ALTA:NOV_BAR':  dict(usa_M=True, gamma_N=1.8, tau_N=4000.0, nov_barajada=True),
    'ALTA:NOV_CTE':  dict(usa_M=True, gamma_N=1.8, tau_N=4000.0, nov_cte=True),
}
# control de identidad de corre_mundo_largo.py: sin pool, mundo_largo == mundo_mapa
IDENT_MAPA = dict(r_vis=3, sitios=('A', 'B'), usa_M=True, prueba=dict(n_tel=40))
# cobertura: caminos que las configuraciones de los runners no tocan con el T corto de la rejilla ancha
COBERTURA = {
    'apagadas(v13)':   (False, dict()),                                               # todas las perillas apagadas
    'pool_agotado':    (True, dict(usa_M=True, gamma_N=0.6, T_nuevo=500)),            # se ven los 50 -> _cand vacio -> reciclaje forzado
    'REC+NOV':         (True, dict(usa_M=True, gamma_N=0.6, reciclado=True, nov_barajada=True)),
}


def kw_de(seed, extra, tt):
    pool = pool_de(seed)
    kw = dict(T=tt, r_vis=3, sitios=sitios_de(pool, seed), pool=pool, T_nuevo=T_NUEVO, invertir_largo=T_INV)
    kw.update(extra)
    return kw


def una(mod, seed, kw, extras_ok):
    ta = time.time(); a = mod.run(seed, **kw); ta = time.time() - ta
    tb = time.time(); b = rapido.run(seed, **kw); tb = time.time() - tb
    dif = [k for k in a if N(a[k]) != N(b[k])]
    extra = sorted(set(b) - set(a))
    if extra != extras_ok: dif = dif + [f"CLAVES_EXTRA:{extra}"]
    return dif, ta, tb


def rejilla(titulo, casos, tt, seeds):
    fallos = []; n = 0
    print(f"--- {titulo} (T={tt}, {len(casos)} configuraciones x {len(seeds)} semillas) ---", flush=True)
    for nombre, (mod, extra, extras_ok, usa_pool) in casos.items():
        ta = tb = 0.0; mal = 0
        for s in seeds:
            kw = kw_de(s, extra, tt) if usa_pool else dict(extra, T=tt)
            dif, xa, xb = una(mod, s, kw, extras_ok); ta += xa; tb += xb; n += 1
            if dif:
                mal += 1; fallos.append((nombre, s, dif))
                print(f"  DIFIERE {nombre} s{s}: {dif[:6]}", flush=True)
        print(f"  {nombre:16s} [{mod.__name__:14s}] {len(seeds)-mal}/{len(seeds)} ok   original {ta:6.1f}s  gemelo {tb:5.1f}s  x{ta/max(tb,1e-9):.0f}", flush=True)
    print(f"  => {n - len(fallos)}/{n} corridas identicas", flush=True)
    return n, fallos


def cache_en_proceso_nuevo():
    """Regla 9 de EQUIPO.md: un proceso NUEVO debe poder LEER el cache de numba sin segmentar."""
    src = ("import sys;sys.path[:0]=[r'%s',r'%s',r'%s'];"
           "from corre_mundo_largo import pool_de,sitios_de;import mundo_largo_n_rapido as r;"
           "p=pool_de(2);d=r.run(2,T=4000,r_vis=3,sitios=sitios_de(p,2),pool=p,T_nuevo=2000,invertir_largo=3000,"
           "usa_M=True,gamma_N=0.6);print('vistos',len(d['vistos']),'inyecciones',len(d['inyecciones']))"
           % (AQUI, os.path.join(RAIZ, 'experimentos', 'nivel8_mundo_largo'), os.path.join(RAIZ, 'organismo')))
    t0 = time.time(); p = subprocess.run([sys.executable, '-c', src], capture_output=True, text=True, timeout=900)
    print(f"proceso NUEVO leyendo el cache (regla 9): rc={p.returncode} en {time.time()-t0:.1f}s  {p.stdout.strip()}"
          f"{('  ' + p.stderr.strip()[-300:]) if p.returncode else ''}", flush=True)
    return p.returncode == 0


if __name__ == '__main__':
    ANCHA = {'ident_mapa(pool=None)': (largo, IDENT_MAPA, ['nov_diag'], False)}
    for b, kw in BRAZOS_LARGO.items(): ANCHA[f'largo:{b}'] = (largo, kw, ['nov_diag'], True)
    for b, kw in BRAZOS_NOV.items(): ANCHA[f'nov:{b}'] = (largo_n, kw, [], True)
    for b, (up, kw) in COBERTURA.items(): ANCHA[f'cob:{b}'] = (largo_n, kw, [], up)
    LARGA = {'largo:MAPA': (largo, BRAZOS_LARGO['MAPA'], ['nov_diag'], True),
             'nov:MAPA_NOV': (largo_n, BRAZOS_NOV['MAPA_NOV'], [], True)}

    t0 = time.time(); rapido.run(1, **kw_de(1, BRAZOS_NOV['MAPA_NOV_BAR'], 3000))
    print(f"compilacion/carga de cache: {time.time()-t0:.1f}s", flush=True)
    if not cache_en_proceso_nuevo():
        print("*** el cache de numba no sobrevive a un proceso nuevo: el gemelo NO se usa."); sys.exit(2)
    n1, f1 = rejilla('ANCHA: las 4 configuraciones de corre_mundo_largo.py + los 6 brazos de corre_novedad.py', ANCHA, T, SEEDS)
    n2, f2 = (0, []) if '--solo-ancha' in sys.argv else rejilla('LARGA: dos brazos con mapa al T real del runner', LARGA, TL, SEEDS)
    n = n1 + n2; fallos = f1 + f2
    print(f"identidad TOTAL: {n - len(fallos)}/{n} corridas identicas")
    if not fallos:
        kw = kw_de(7, BRAZOS_NOV['MAPA_NOV'], 200000)
        t0 = time.time(); a = largo_n.run(7, **kw); tl = time.time() - t0
        t0 = time.time(); b = rapido.run(7, **kw); tr = time.time() - t0
        ok = all(N(a[k]) == N(b[k]) for k in a) and sorted(set(b) - set(a)) == []
        print(f"200k pasos (MAPA_NOV): original {tl:.2f}s, gemelo {tr:.2f}s -> x{tl/tr:.1f}; identidad a 200k: {'OK' if ok else 'FALLA'}")
    sys.exit(1 if fallos else 0)
