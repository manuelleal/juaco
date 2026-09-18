"""Arnes de identidad del gemelo compilado de organismo_v13q6 (regla 9 de registro/EQUIPO.md):
experimentos/creacion_A/organismo_v13q6_rapido.run(...) debe ser BIT A BIT igual — TODAS las claves, y ademas el
MISMO conjunto de claves, tras ida y vuelta por JSON — a experimentos/creacion_A/organismo_v13q6.run(...)
(original vigente b37aa8124c89cc5f, construido por anclas desde organismo_v13q5.py fae9c32b146fdbb4).
Normalizacion: N = json.loads(json.dumps(x, default=str)), la misma de identidad_v13q5_rapido.py.

Que cubre:
  (0) LA FIRMA: los 44 parametros de run (nombre, orden y default) son EXACTAMENTE los de organismo_v13q6.run, y
      la de split_regla acepta el tercer argumento `ntr_ovr`. Ademas se comprueba que el NUCLEO COMPILADO es el
      MISMO OBJETO que el de organismo_v13q5_rapido (el gemelo delega: `_bucle is _bucle`), y que split_regla
      coincide funcionalmente con la del original en 3 reglas x 8 valores de ntr x 10 semillas.
  (1) PERILLA APAGADA (`ntr=None`, el defecto): 12 casillas x 2 semillas x 2 referencias = 48 comparaciones.
      == organismo_v13q5_rapido (el gemelo ya validado 239/239) en todas SUS claves — la unica clave nueva de
      v13q6 es `ntr` — y == organismo_v13q6 interpretado en todas.
  (2) LA PERILLA ENCENDIDA: ntr in {(4,4), (8,6), (11,9), (14,6)} x regla in {xor01, px0, azar} x brazo in
      {llano, seleccion='wta', lab=True} x semillas 1-3 a T=30000 (108), y ntr in {(11,9), (14,6)} x las tres
      reglas x {llano, seleccion} x semillas 1-3 a T=100000 (36). Los brazos `seleccion` y `lab` son los puntos
      de produccion de la linea (mini_prueba_A_ganadora.py y cosecha_lab.py). (8,6) es el punto que el
      preregistro de A-6 describe (14 patrones de tren); (4,4) es la referencia interna del constructor.
  (3) PROCESO NUEVO QUE LEE LA CACHE: un subproceso limpio importa el gemelo y reproduce 8 casos con ntr; se
      comparan clave a clave contra este proceso, se mide su primer run y se comprueba que el gemelo NO genera
      cache numba propia (delega en organismo_v13q5_rapido).
  Y se mide la ACELERACION a 100000 y 200000 pasos.

AVISO heredado del constructor (trampa 3 de EQUIPO.md, y trampa 2 al leer resultados): mover `ntr` cambia el
MUNDO. Con los valores grandes el test queda casi vacio y de UNA sola clase — medido aqui, semilla 1:
xor01 (12 comida / 8 veneno entre los 20 patrones) ntr=(11,9) -> tren 19, test 1; ntr=(14,6) -> tren 18, test 2,
los dos de veneno; px0 ntr=(11,9) -> test 1 de veneno. El gemelo lo reproduce EXACTAMENTE, que es su trabajo;
interpretar esas casillas es del preregistro.

REGLA: si esto no da 100 %, el gemelo no se usa para confirmar nada. Nunca se relaja la comparacion.
OJO (ERR-28): organismo/ va PRIMERO en sys.path, siempre.
Uso:  python experimentos/creacion_A/identidad_v13q6_rapido.py [--T 30000] [--rapido]
"""
import inspect, json, os, subprocess, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura')]   # ERR-28: organismo/ PRIMERO

import organismo_v13q6 as LENTO             # el original de esta linea (b37aa8124c89cc5f), interpretado
import organismo_v13q6_rapido as RAPIDO     # el gemelo que se examina aqui
import organismo_v13q5_rapido as Q5         # gemelo YA VALIDADO de organismo_v13q5 (239/239): perilla `ntr` apagada

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 30000
T2 = int(sys.argv[sys.argv.index('--T2') + 1]) if '--T2' in sys.argv else 100000
N = lambda x: json.loads(json.dumps(x, default=str))
TR = dict(eta_s=0.015, puerta=3)


def RG(rg, lec, **kw):
    d = dict(mundo='regla', regla=rg, lectura=lec); d.update(TR); d.update(kw); return d


def cmp(a, b, etiqueta, fallos, solo=None):
    """Compara TODAS las claves (y el conjunto de claves). `solo`: subconjunto (referencia con menos claves)."""
    if solo is None:
        fa, fb = set(a), set(b)
        if fa != fb:
            fallos.append((etiqueta, ['CLAVES: ' + str(sorted(fa ^ fb))]))
            print(f"  DIFIERE {etiqueta}: claves {sorted(fa ^ fb)}", flush=True); return False
        claves = list(a)
    else:
        falta = [k for k in solo if k not in b]
        if falta:
            fallos.append((etiqueta, ['FALTAN: ' + str(falta)]))
            print(f"  DIFIERE {etiqueta}: faltan claves {falta}", flush=True); return False
        claves = list(solo)
    dif = [k for k in claves if N(a[k]) != N(b[k])]
    if dif:
        fallos.append((etiqueta, dif)); print(f"  DIFIERE {etiqueta}: {dif}", flush=True); return False
    return True


# ---------------------------------------------------------------- (1) perilla apagada (ntr=None)
APAGADAS = {
    'ap_AB_tronco': dict(**TR),
    'ap_AB_defecto': dict(),
    'ap_xor01_lineal': RG('xor01', 'lineal'),
    'ap_xor01_cuad_delta_c1': RG('xor01', 'cuadratica', regla_lenta='delta_signo', constante=True),
    'ap_xor01_r15_sonda': RG('xor01', 'random15', sonda_final=True),
    'ap_xor01_orac_wta_cov': RG('xor01', 'oraculo01', seleccion='wta', sel_estad='cov', eta_s=0.15),
    'ap_px0_cuad_wta_cond': RG('px0', 'cuadratica', seleccion='wta', sel_estad='cond'),
    'ap_px0_oracruido_delta': RG('px0', 'oraculo01_ruido', regla_lenta='delta_signo', constante=True),
    'ap_azar_cuad_lab': RG('azar', 'cuadratica', lab=True),
    'ap_azar_lineal_sin_puerta': RG('azar', 'lineal', puerta=None),
    'ap_cosecha_lab': RG('xor01', 'cuadratica', constante=True, regla_lenta='delta_signo', lam_lenta=0.0, clip_s=3.0, lab=True),
    'ap_ganadora': RG('xor01', 'cuadratica', constante=True, regla_lenta='delta_signo', lab=True, eta_s=0.15, clip_s=10.0,
                      lam_lenta=0.0, seleccion='wta', sel_theta=0.3, sel_rho=0.02, sel_cupo=1, sel_estad='cond'),
}

# ---------------------------------------------------------------- (2) la perilla encendida
NTRS = [(4, 4), (8, 6), (11, 9), (14, 6)]          # (4,4) referencia interna; (8,6) = los 14 de tren del preregistro A-6
REGLAS = ['xor01', 'px0', 'azar']
BRAZOS = {                                          # los puntos de produccion de la linea
    'llano': dict(lectura='cuadratica'),
    'sel':   dict(lectura='cuadratica', constante=True, regla_lenta='delta_signo', lam_lenta=0.0, eta_s=0.15,
                  clip_s=10.0, seleccion='wta', sel_theta=0.3, sel_rho=0.02, sel_cupo=1, sel_estad='cond'),   # mini_prueba_A_ganadora.py
    'lab':   dict(lectura='cuadratica', constante=True, regla_lenta='delta_signo', lam_lenta=0.0, clip_s=3.0, lab=True),   # cosecha_lab.py
}
SEEDS = [1, 2, 3]
BRAZOS_T2 = ['llano', 'sel']                        # a T=100000, con ntr in {(11,9), (14,6)}
NTRS_T2 = [(11, 9), (14, 6)]

HIJO = [('h_xor01_86_sel', 1, RG('xor01', 'cuadratica', ntr=(8, 6), **BRAZOS['sel'])),
        ('h_xor01_119_lab', 1, RG('xor01', 'cuadratica', ntr=(11, 9), **BRAZOS['lab'])),
        ('h_px0_146_llano', 2, RG('px0', 'cuadratica', ntr=(14, 6))),
        ('h_px0_86_sel', 2, RG('px0', 'cuadratica', ntr=(8, 6), **BRAZOS['sel'])),
        ('h_azar_119_llano', 3, RG('azar', 'cuadratica', ntr=(11, 9))),
        ('h_azar_146_lab', 3, RG('azar', 'cuadratica', ntr=(14, 6), **BRAZOS['lab'])),
        ('h_xor01_44_llano', 4, RG('xor01', 'cuadratica', ntr=(4, 4))),
        ('h_xor01_ntr_none', 4, RG('xor01', 'cuadratica'))]


def _hijo():
    """Proceso NUEVO: importa el gemelo (leyendo la cache de numba de organismo_v13q5_rapido) y reproduce HIJO."""
    t0 = time.time(); res = {}
    for i, (etiq, s, kw) in enumerate(HIJO):
        res[etiq] = N(RAPIDO.run(s, T=T, **kw))
        if i == 0: t_primero = time.time() - t0
    print('###JSON###' + json.dumps(dict(t_primero=t_primero, res=res)))


if __name__ == '__main__':
    if '--hijo' in sys.argv:
        _hijo(); sys.exit(0)
    import hashlib
    t00 = time.time()
    for m, et in ((LENTO, 'organismo_v13q6.py       '), (RAPIDO, 'organismo_v13q6_rapido.py'), (Q5, 'organismo_v13q5_rapido.py')):
        print(f"{et} sha {hashlib.sha256(open(m.__file__,'rb').read()).hexdigest()[:16]}")
    fallos = []; n = 0

    # ---- (0) firma, delegacion del kernel y split_regla
    sa = inspect.signature(LENTO.run); sb = inspect.signature(RAPIDO.run); n += 1
    if [(p.name, p.default) for p in sa.parameters.values()] != [(p.name, p.default) for p in sb.parameters.values()]:
        fallos.append(('0/firma_run', ['firma distinta'])); print(f"  DIFIERE 0/firma_run:\n    {sa}\n    {sb}", flush=True)
    else:
        print(f"(0) firma de run identica parametro a parametro ({len(sa.parameters)} parametros)")
    n += 1
    if [p.name for p in inspect.signature(RAPIDO.split_regla).parameters.values()] != ['seed', 'regla', 'ntr_ovr']:
        fallos.append(('0/firma_split', ['firma distinta'])); print("  DIFIERE 0/firma_split", flush=True)
    n += 1
    if RAPIDO._bucle is not Q5._bucle:
        fallos.append(('0/delega_kernel', ['el gemelo NO delega el nucleo compilado'])); print("  DIFIERE 0/delega_kernel", flush=True)
    else:
        print("(0) nucleo compilado DELEGADO: organismo_v13q6_rapido._bucle is organismo_v13q5_rapido._bucle")
    n += 1; malo = 0
    for rg in REGLAS:
        for ntr in (None, (4, 4), (5, 5), (8, 6), (11, 9), (14, 6), (0, 0), (20, 20)):
            for s in range(1, 11):
                if LENTO.split_regla(s, rg, ntr)[1:] != RAPIDO.split_regla(s, rg, ntr)[1:]: malo += 1
    if malo:
        fallos.append(('0/split_regla', [f'{malo} particiones distintas'])); print(f"  DIFIERE 0/split_regla: {malo}", flush=True)
    else:
        print("(0) split_regla identica en 3 reglas x 8 valores de ntr x 10 semillas (240 particiones)")
    for rg in ('xor01', 'px0'):
        for ntr in NTRS:
            _, tr_, te_, vr_ = LENTO.split_regla(1, rg, ntr)
            cf = sum(1 for k in te_ if vr_[k] == 'comida')
            print(f"      s1 {rg:6s} ntr={str(ntr):8s} -> tren {len(tr_):2d}, test {len(te_):2d} (comida {cf}, veneno {len(te_)-cf})")

    t0 = time.time(); RAPIDO.run(1, T=2000); RAPIDO.run(1, T=2000, **RG('px0', 'cuadratica'))
    print(f"compilacion/carga de cache: {time.time()-t0:.1f}s (delega: no deberia compilar nada nuevo)", flush=True)

    # ---- (1) perilla apagada: a tres bandas
    print(f"\n(1) ntr=None == organismo_v13q5_rapido (gemelo validado) y == organismo_v13q6 interpretado")
    for nombre, kw in APAGADAS.items():
        for s in (1, 2):
            a = LENTO.run(s, T=T, **kw); b = RAPIDO.run(s, T=T, **kw); c = Q5.run(s, T=T, **kw)
            n += 1; cmp(a, b, f"1/{nombre}/s{s}/v13q6", fallos)
            n += 1; cmp(b, c, f"1/{nombre}/s{s}/v13q5_rapido", fallos, solo=list(c))
        print(f"  {nombre:26s} 2 semillas x 2 referencias", flush=True)

    # ---- (2) la perilla encendida
    print(f"\n(2) ntr in {NTRS} x {REGLAS} x {list(BRAZOS)} x semillas {SEEDS} a T={T}")
    tc = time.time(); ic = 0; total = len(NTRS) * len(REGLAS) * len(BRAZOS)
    for ntr in NTRS:
        for rg in REGLAS:
            for bz, bkw in BRAZOS.items():
                ic += 1; fc = 0
                kw = RG(rg, 'cuadratica', ntr=ntr, **{k: v for k, v in bkw.items() if k != 'lectura'})
                for s in SEEDS:
                    a = LENTO.run(s, T=T, **kw); b = RAPIDO.run(s, T=T, **kw); n += 1
                    if not cmp(a, b, f"2/ntr{ntr}/{rg}/{bz}/s{s}", fallos): fc += 1
                print(f"  [{time.strftime('%H:%M:%S')} +{time.time()-tc:6.1f}s] {ic:2d}/{total} ntr={str(ntr):8s} {rg:6s} {bz:6s} "
                      f"{len(SEEDS)-fc}/{len(SEEDS)} semillas identicas", flush=True)   # REGLA 10

    print(f"\n(2b) ntr in {NTRS_T2} x {REGLAS} x {BRAZOS_T2} x semillas {SEEDS} a T={T2}")
    tc = time.time(); ic = 0; total = len(NTRS_T2) * len(REGLAS) * len(BRAZOS_T2)
    for ntr in NTRS_T2:
        for rg in REGLAS:
            for bz in BRAZOS_T2:
                ic += 1; fc = 0
                kw = RG(rg, 'cuadratica', ntr=ntr, **{k: v for k, v in BRAZOS[bz].items() if k != 'lectura'})
                for s in SEEDS:
                    a = LENTO.run(s, T=T2, **kw); b = RAPIDO.run(s, T=T2, **kw); n += 1
                    if not cmp(a, b, f"2b/ntr{ntr}/{rg}/{bz}/s{s}/T{T2}", fallos): fc += 1
                print(f"  [{time.strftime('%H:%M:%S')} +{time.time()-tc:6.1f}s] {ic:2d}/{total} ntr={str(ntr):8s} {rg:6s} {bz:6s} "
                      f"{len(SEEDS)-fc}/{len(SEEDS)} semillas identicas", flush=True)

    # ---- (3) proceso nuevo que lee la cache
    print(f"\n(3) proceso NUEVO que lee la cache de numba (subprocess)")
    aqui_res = {etiq: N(RAPIDO.run(s, T=T, **kw)) for etiq, s, kw in HIJO}
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    tp = time.time()
    pr = subprocess.run([sys.executable, os.path.abspath(__file__), '--hijo', '--T', str(T)],
                        capture_output=True, text=True, env=env, cwd=RAIZ, timeout=3600)
    t_sub = time.time() - tp
    linea = [l for l in pr.stdout.splitlines() if l.startswith('###JSON###')]
    if pr.returncode != 0 or not linea:
        n += 1; fallos.append(('3/subproceso', ['sin salida']))
        print(f"  DIFIERE 3/subproceso: codigo {pr.returncode}\n{pr.stderr[-1500:]}")
    else:
        hijo = json.loads(linea[0][len('###JSON###'):])
        print(f"  proceso nuevo: {t_sub:.1f}s en total, primer run del gemelo {hijo['t_primero']:.2f}s "
              f"(la cache se leyo: {'SI' if hijo['t_primero'] < 3.0 else 'NO'})")
        for etiq, s, kw in HIJO:
            n += 1; cmp(aqui_res[etiq], hijo['res'][etiq], f"3/{etiq}", fallos)
    pc = os.path.join(AQUI, '__pycache__')
    nb = [f for f in os.listdir(pc) if f.endswith(('.nbi', '.nbc'))] if os.path.isdir(pc) else []
    propios = sum(f.startswith('organismo_v13q6_rapido') for f in nb); n += 1
    if propios:
        fallos.append(('3/cache_propia', [f'{propios} archivos .nbi/.nbc de organismo_v13q6_rapido']))
        print(f"  DIFIERE 3/cache_propia: el gemelo genero {propios} archivos de cache propios (deberia delegar)")
    else:
        print(f"  cache numba: {sum(f.startswith('organismo_v13q5_rapido') for f in nb)} archivos de organismo_v13q5_rapido, "
              f"0 de organismo_v13q6_rapido (delega: no debe generar ninguna propia)")

    print(f"\nIDENTIDAD {n - len(fallos)}/{n} comparaciones identicas   ({time.time()-t00:.1f}s)")

    if '--rapido' not in sys.argv:
        kw = RG('xor01', 'cuadratica', ntr=(8, 6), **{k: v for k, v in BRAZOS['sel'].items() if k != 'lectura'})
        tl = tr = 0.0
        for TL in (100000, 200000):
            t1 = time.time(); a = LENTO.run(9, T=TL, **kw); dl = time.time() - t1
            t1 = time.time(); b = RAPIDO.run(9, T=TL, **kw); dr = time.time() - t1
            n += 1; cmp(a, b, f"acel/T{TL}", fallos); tl += dl; tr += dr
            print(f"aceleracion a {TL} pasos (ntr=(8,6), brazo seleccion): original {dl:.2f}s -> gemelo {dr:.3f}s  x{dl/dr:.0f}")
        print(f"aceleracion agregada (100k+200k): original {tl:.2f}s, gemelo {tr:.2f}s -> x{tl/tr:.1f}")

    if fallos:
        print("FALLOS:"); [print('  ', f) for f in fallos]
    print("limitaciones heredadas: log_cada no esta compilado (ValueError); invertir_en solo con mundo='AB'; "
          "`nuevo` antes de `invertir_en` no se admite.")
    sys.exit(1 if fallos else 0)
