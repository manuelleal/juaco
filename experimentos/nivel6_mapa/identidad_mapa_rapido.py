"""Arnes de identidad del gemelo compilado del mundo del mapa: mundo_mapa_rapido.run(...) debe ser BIT A BIT igual
(todas las claves, tras ida y vuelta por JSON) a mundo_mapa.run(...). Dos rejillas:
  PRINCIPAL (T=100000, semillas 1-4): lo que usan los runners -- las PERILLAS APAGADAS (= organismo_v13, con y sin
  invertir/nuevo, las tres identidades de corre_mapa.py) y los SEIS BRAZOS de corre_mapa.py (MAPA, SINMAPA,
  CONGELADA, BARAJADO, SINCOMIDA, INVERTIDO).
  COBERTURA (T mas corto): los caminos que los seis brazos no tocan -- mapa con inversion de valencia, mapa sin
  memoria de rechazo, mapa sin puerta, mapa sin vision limitada, mapa con sitios=None (spawn con azar), regen/H_M/
  disc_M/gamma_M distintos, sin prueba, y las variantes historicas del tronco (v11/v10/v9, sin plasticidad, solap_AB).
Antes de las rejillas comprueba, como pide la regla 9 de registro/EQUIPO.md, que un proceso NUEVO puede LEER el cache
de numba sin segmentar (el gemelo no tiene funciones recursivas con cache=True: _bucle -> _see/_code/_spawn/_borrar/
_idx_en/_sesgo -> _valor -> _code, un arbol sin ciclos). Imprime la aceleracion a 100k pasos.
Un solo proceso a la vez, sin Pool (regla 3 de registro/EQUIPO.md).
Uso: python experimentos/nivel6_mapa/identidad_mapa_rapido.py [--T 100000] [--semillas 4] [--Tc 20000] [--sin-cobertura]
"""
import sys, os, json, time, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]
import mundo_mapa as lento, mundo_mapa_rapido as rapido

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 100000
TC = int(sys.argv[sys.argv.index('--Tc') + 1]) if '--Tc' in sys.argv else 20000
NS = int(sys.argv[sys.argv.index('--semillas') + 1]) if '--semillas' in sys.argv else 4
N = lambda x: json.loads(json.dumps(x, default=str))

MUNDO = dict(r_vis=3, sitios=('A', 'B'))
PRUEBA = dict(n_tel=40, E_test=0.3, max_pasos=30)
CONFIGS = {
    # (a) perillas apagadas == organismo_v13 (las tres identidades de corre_mapa.py)
    'apagadas': dict(),
    'apagadas_invertir': dict(invertir_en=T // 2),
    'apagadas_nuevo_C': dict(nuevo='C', nuevo_en=T // 3),
    # (b/c) los seis brazos de corre_mapa.py
    'MAPA': dict(MUNDO, usa_M=True, prueba=dict(PRUEBA)),
    'SINMAPA': dict(MUNDO, usa_M=False, prueba=dict(PRUEBA)),
    'CONGELADA': dict(MUNDO, usa_M=True, escribe_M=False, prueba=dict(PRUEBA)),
    'BARAJADO': dict(MUNDO, usa_M=True, prueba=dict(PRUEBA, barajar=True)),
    'SINCOMIDA': dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), sitios=('B', 'B')),
    'INVERTIDO': dict(MUNDO, usa_M=True, prueba=dict(PRUEBA, invertir=True)),
}
COBERTURA = {
    'mapa_invertir':    dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), invertir_en=TC // 2),   # la prueba busca el sitio de B
    'mapa_nuevo_C':     dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), nuevo='C', nuevo_en=TC // 3),
    'mapa_sin_rechazo': dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), memoria_rechazo=0),
    'mapa_sin_puerta':  dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), puerta=None),           # valor = rapida + lenta
    'mapa_sin_plast':   dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), plast=False),
    'mapa_v9':          dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), eta_s=0.0, puerta=None, div_signo=False, mu_norm=False),
    'mapa_perillas':    dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), regen=17, H_M=7, disc_M=0.75, gamma_M=1.3),
    'mapa_sin_prueba':  dict(MUNDO, usa_M=True),                                             # sin teletransporte
    'mapa_3sitios':     dict(r_vis=2, sitios=('A', 'B', 'A'), usa_M=True, prueba=dict(PRUEBA), regen=30),
    'mapa_sin_rvis':    dict(sitios=('A', 'B'), usa_M=True),                                 # sitios + M con vista infinita (sin prueba: _dn necesita r_vis)
    'M_sin_sitios':     dict(r_vis=3, usa_M=True, nobj=6, lam=0.0),                          # spawn con azar + tabla M
    'mapa_M_splits':    dict(r_vis=3, usa_M=True, solap_AB=1),                               # DIVISIONES (celdas>30) con la tabla M viva
    'solo_rvis':        dict(r_vis=1),                                                       # vista limitada, mundo v13
    'techo_apagadas':   dict(eta=0.6, aversion=2.0),                                         # fuerza el TECHO (n_techo/t_techo > 0)
    'techo_mapa':       dict(MUNDO, usa_M=True, prueba=dict(PRUEBA), eta=0.6, aversion=2.0),
    'apagadas_v11':     dict(eta_s=0.0, puerta=None),
    'apagadas_v10':     dict(eta_s=0.0, puerta=None, div_signo=False),
    'apagadas_solapAB1': dict(solap_AB=1),                                                   # DIVISIONES en el mundo v13
}
SEEDS = list(range(1, NS + 1))
SEEDS_C = [1, 2, 3]


def rejilla(titulo, configs, tt, seeds):
    fallos = []; n = 0
    print(f"--- {titulo} (T={tt}, {len(configs)} configuraciones x {len(seeds)} semillas) ---", flush=True)
    for nombre, kw in configs.items():
        ta = tb = 0.0
        for s in seeds:
            t0 = time.time(); a = lento.run(s, T=tt, **kw); ta += time.time() - t0
            t0 = time.time(); b = rapido.run(s, T=tt, **kw); tb += time.time() - t0
            dif = [k for k in a if N(a[k]) != N(b[k])]; n += 1
            if dif:
                fallos.append((nombre, s, dif))
                print(f"  DIFIERE {nombre} s{s}: {dif}", flush=True)
        ok = len(seeds) - sum(1 for f in fallos if f[0] == nombre)
        print(f"  {nombre:19s} {ok}/{len(seeds)} ok   original {ta:6.1f}s  gemelo {tb:5.1f}s  x{ta/max(tb,1e-9):.0f}", flush=True)
    print(f"  => {n - len(fallos)}/{n} corridas identicas", flush=True)
    return n, fallos


def cache_en_proceso_nuevo():
    """Regla 9 de EQUIPO.md: un proceso NUEVO debe poder LEER el cache de numba sin segmentar (si no, mata a cada worker)."""
    src = ("import sys;sys.path[:0]=[r'%s'];import mundo_mapa_rapido as r;"
           "d=r.run(2,T=3000,r_vis=3,sitios=('A','B'),usa_M=True,prueba=dict(n_tel=8,E_test=0.3,max_pasos=30));"
           "print('M_llenas',d['M_llenas'],'tel_n',d['tel']['n'])" % AQUI)
    t0 = time.time(); p = subprocess.run([sys.executable, '-c', src], capture_output=True, text=True, timeout=600)
    print(f"proceso NUEVO leyendo el cache (regla 9): rc={p.returncode} en {time.time()-t0:.1f}s  {p.stdout.strip()}"
          f"{('  ' + p.stderr.strip()[-300:]) if p.returncode else ''}", flush=True)
    return p.returncode == 0


if __name__ == '__main__':
    t0 = time.time(); rapido.run(1, T=2000, **dict(MUNDO, usa_M=True, prueba=dict(PRUEBA)))
    print(f"compilacion/carga de cache: {time.time()-t0:.1f}s", flush=True)
    if not cache_en_proceso_nuevo():
        print("*** el cache de numba no sobrevive a un proceso nuevo: el gemelo NO se usa."); sys.exit(2)
    n1, f1 = rejilla('PRINCIPAL: perillas apagadas + los seis brazos de corre_mapa.py', CONFIGS, T, SEEDS)
    n2, f2 = (0, []) if '--sin-cobertura' in sys.argv else rejilla('COBERTURA: caminos que los seis brazos no tocan', COBERTURA, TC, SEEDS_C)
    n = n1 + n2; fallos = f1 + f2
    print(f"identidad TOTAL: {n - len(fallos)}/{n} corridas identicas")
    if not fallos:
        kw = dict(MUNDO, usa_M=True, prueba=dict(PRUEBA))
        t0 = time.time(); a = lento.run(7, T=100000, **kw); tl = time.time() - t0
        t0 = time.time(); b = rapido.run(7, T=100000, **kw); tr = time.time() - t0
        print(f"100k pasos (MAPA, usa_M=True): original {tl:.2f}s, gemelo {tr:.2f}s -> x{tl/tr:.1f}; "
              f"identidad a 100k: {'OK' if all(N(a[k]) == N(b[k]) for k in a) else 'FALLA'}")
    sys.exit(1 if fallos else 0)
