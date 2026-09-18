"""Arnes de identidad del gemelo compilado de organismo_v13q: organismo_v13q_rapido.run(...) debe ser BIT A BIT igual
(TODAS las claves, tras ida y vuelta por JSON) a organismo_v13q.run(...) — original vigente 0b59eb03858df3a8 (bloque 3b,
con W_lenta_apriori y familiar_apriori en la sonda de fase2_en).

Rejilla (mismo espiritu que organismo/identidad_rapido.py):
  - mundo 'AB' con las perillas del tronco (eta_s=0.015, puerta=3) y sus variantes (v13g por defecto = eta_s=0/puerta=None,
    invertir, nuevo con y sin solap_B, sin plasticidad, sin memoria de rechazo, nobj/lam distintos, solap_AB, sin puerta).
  - mundo 'regla' con regla x lectura = {px0, azar, xor01} x {lineal, cuadratica, random15}, eta_s=0.015, puerta=3
    (las 9 casillas que consume experimentos/nivel7_xor_lectura/corre_xor.py), mas sonda_final, fase2_en explicito,
    `nuevo` en el mundo de regla y el punto v13g por defecto.
Semillas 1-3 por defecto (--desde/--n para mover la ventana). Al final repite tres casillas a T=200000 y mide la aceleracion.
Uso: python experimentos/nivel7_xor_lectura/identidad_v13q_rapido.py [--T 60000] [--desde 1] [--n 3] [--full]
"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import organismo_v13q as lento, organismo_v13q_rapido as rapido

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 60000
N = lambda x: json.loads(json.dumps(x, default=str))
TR = dict(eta_s=0.015, puerta=3)                      # perillas del tronco (las de corre_xor.py y bateria_generaliza.py)
def RG(rg, lec, **kw):
    d = dict(mundo='regla', regla=rg, lectura=lec); d.update(TR); d.update(kw); return d


CONFIGS = {
    # --- mundo AB (con 'AB' organismo_v13q es organismo_v13 exacto) ---
    'AB_tronco': dict(**TR),
    'AB_v13g_defecto': dict(),                                    # eta_s=0, puerta=None: la via lenta inerte
    'AB_sin_puerta': dict(eta_s=0.015, puerta=None),              # un solo error compartido
    'AB_invertir': dict(**TR, invertir_en=T // 2),
    'AB_nuevo_C': dict(**TR, nuevo='C', nuevo_en=T // 3),
    'AB_nuevo_D_solapB': dict(**TR, nuevo='D', nuevo_en=T // 3, solap_B=1, nuevo_val='comida'),
    'AB_sin_plast': dict(**TR, plast=False),
    'AB_sin_rechazo': dict(**TR, memoria_rechazo=0),
    'AB_nobj6_lam0': dict(**TR, nobj=6, lam=0.0),
    'AB_solapAB1': dict(**TR, solap_AB=1),
    'AB_v9': dict(eta_s=0.0, puerta=None, div_signo=False, mu_norm=False),
    # --- mundo de regla: las 9 casillas de corre_xor.py ---
    'regla_px0_lineal': RG('px0', 'lineal'),
    'regla_px0_cuadratica': RG('px0', 'cuadratica'),
    'regla_px0_random15': RG('px0', 'random15'),
    'regla_azar_lineal': RG('azar', 'lineal'),
    'regla_azar_cuadratica': RG('azar', 'cuadratica'),
    'regla_azar_random15': RG('azar', 'random15'),
    'regla_xor01_lineal': RG('xor01', 'lineal'),
    'regla_xor01_cuadratica': RG('xor01', 'cuadratica'),
    'regla_xor01_random15': RG('xor01', 'random15'),
    # --- mundo de regla: el resto de las perillas que tocan claves de salida ---
    'regla_px0_cuad_sonda': RG('px0', 'cuadratica', sonda_final=True),
    'regla_xor01_r15_sonda': RG('xor01', 'random15', sonda_final=True),
    'regla_px0_lin_fase2': RG('px0', 'lineal', fase2_en=T // 3),
    'regla_px0_cuad_nuevo': RG('px0', 'cuadratica', nuevo='111000', nuevo_en=T // 4, nuevo_val='comida'),
    'regla_azar_r15_v13g_defecto': dict(mundo='regla', regla='azar', lectura='random15'),
    'regla_xor01_cuad_sin_puerta': RG('xor01', 'cuadratica', puerta=None),
    'regla_px0_r15_sin_plast': RG('px0', 'random15', plast=False),
}
_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 1
_n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 3
SEEDS = list(range(_desde, _desde + _n))
LARGAS = [('AB_tronco', 1), ('regla_px0_lineal', 1), ('regla_xor01_cuadratica', 1)]

if __name__ == '__main__':
    t0 = time.time(); rapido.run(1, T=2000); rapido.run(1, T=2000, **RG('px0', 'cuadratica')); print(f"compilacion/carga de cache: {time.time()-t0:.1f}s", flush=True)
    fallos = []; n = 0; tc = time.time()
    for ic, (nombre, kw) in enumerate(CONFIGS.items(), 1):
        fc = 0
        for s in SEEDS:
            a = lento.run(s, T=T, **kw); b = rapido.run(s, T=T, **kw)
            dif = [k for k in a if N(a[k]) != N(b[k])]; n += 1
            if dif:
                fallos.append((nombre, s, dif)); fc += 1
                print(f"  DIFIERE {nombre} s{s}: {dif}", flush=True)
        print(f"  [{time.strftime('%H:%M:%S')} +{time.time()-tc:6.1f}s] {ic:2d}/{len(CONFIGS)} {nombre:28s} {len(SEEDS)-fc}/{len(SEEDS)} semillas identicas", flush=True)   # REGLA 10
    print(f"identidad: {n - len(fallos)}/{n} corridas identicas (T={T}, {len(CONFIGS)} configuraciones x {len(SEEDS)} semillas)")
    if '--full' in sys.argv or not fallos:
        TL = 200000; tl = tr = 0.0; ok = True
        for nombre, s in LARGAS:
            kw = CONFIGS[nombre]
            t0 = time.time(); a = lento.run(s, T=TL, **kw); dl = time.time() - t0
            t0 = time.time(); b = rapido.run(s, T=TL, **kw); dr = time.time() - t0
            dif = [k for k in a if N(a[k]) != N(b[k])]; ok = ok and not dif
            tl += dl; tr += dr
            print(f"200k {nombre:24s} s{s}: original {dl:6.2f}s, gemelo {dr:5.2f}s -> x{dl/dr:5.1f}; identidad {'OK' if not dif else 'FALLA ' + str(dif)}")
        print(f"200k pasos (3 casillas): original {tl:.2f}s, gemelo {tr:.2f}s -> x{tl/tr:.1f}; identidad a 200k: {'OK' if ok else 'FALLA'}")
        if not ok: fallos.append(('200k', 0, ['ver arriba']))
    sys.exit(1 if fallos else 0)
