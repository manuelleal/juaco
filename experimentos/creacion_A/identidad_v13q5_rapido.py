"""Arnes de identidad del gemelo compilado de organismo_v13q5 (regla 9 de registro/EQUIPO.md):
experimentos/creacion_A/organismo_v13q5_rapido.run(...) debe ser BIT A BIT igual — TODAS las claves, y ademas el
MISMO conjunto de claves, tras ida y vuelta por JSON — a experimentos/creacion_A/organismo_v13q5.run(...)
(original vigente fae9c32b146fdbb4). Misma normalizacion que experimentos/nivel7_xor_lectura/identidad_v13q_rapido.py:
N = json.loads(json.dumps(x, default=str)).

Que cubre (>= 80 comparaciones; por defecto 84 configuraciones x 2 semillas = 168, mas las etapas 0, 1, 3 y 4):
  (0) LA FIRMA: los parametros de run (nombre, orden y valor por defecto) son EXACTAMENTE los de organismo_v13q5.run
      (inspect.signature). Una perilla que se cuele con otro default cambiaria corridas enteras en silencio.
  (1) PERILLAS NUEVAS APAGADAS (regla_lenta='dos_canales', constante=False, seleccion=None, lab=False) == el gemelo
      YA VALIDADO organismo_v13q_rapido (81/81 + 243/243 + 81/81) en todas SUS claves, y == organismo_v13q5
      interpretado en todas las de el. Comparacion a TRES bandas: 11 casillas x 2 semillas.
  (2) LA REJILLA (ETAPA 2, el grueso): cada `lectura` x cada `regla_lenta` x `constante` on/off; los tres mundos
      (px0, xor01, azar); `seleccion='wta'` con sel_estad 'cond' y 'cov' (y cupo/calienta/theta/rho distintos);
      el oraculo con y sin ruido; eta_s in {0.015, 0.15, 1.0} x clip_s in {3, 10}; `lab` encendido en 7 casillas
      repartidas (la secuencia `lenta_eventos` se compara elemento a elemento, como una clave mas); el mundo 'AB'
      con las perillas del tronco y sus variantes; sonda_final, fase2_en explicito, `nuevo` en el mundo de regla,
      puerta=None, lam_lenta distinto, el punto v13g por defecto, y los cuatro PUNTOS DE PRODUCCION que ya consumen
      los instrumentos de creacion_A (cosecha_lab.py, mini_prueba_A_seleccion.py COND/COV, mini_prueba_A_ganadora.py).
  (3) T LARGO: T in {30000, 100000, 200000} en 6 casillas (dos con lab=True, dos con seleccion='wta', dos de produccion),
      con la aceleracion medida en cada una.
  (4) PROCESO NUEVO QUE LEE LA CACHE: un subproceso limpio importa organismo_v13q5_rapido y reproduce 8 casos; se
      comparan clave a clave contra este proceso y se mide su primer run (con la cache borrada la compilacion tarda
      ~25 s; leyendola, < 3 s).

REGLA: si esto no da 100 %, el gemelo no se usa para confirmar nada. Nunca se relaja la comparacion.
OJO (ERR-28): organismo/ va PRIMERO en sys.path, siempre.
Uso:  python experimentos/creacion_A/identidad_v13q5_rapido.py [--T 30000] [--desde 1] [--n 2] [--rapido]
"""
import inspect, json, os, subprocess, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [os.path.join(RAIZ, 'organismo'), AQUI, os.path.join(RAIZ, 'experimentos', 'nivel7_xor_lectura')]   # ERR-28: organismo/ PRIMERO

import organismo_v13q5 as LENTO            # el original de esta linea (fae9c32b146fdbb4), interpretado
import organismo_v13q5_rapido as RAPIDO    # el gemelo que se examina aqui
import organismo_v13q_rapido as Q_RAP      # gemelo YA VALIDADO de organismo_v13q (perillas nuevas apagadas)

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 30000
N = lambda x: json.loads(json.dumps(x, default=str))
TR = dict(eta_s=0.015, puerta=3)           # perillas del tronco (las de corre_xor.py / corre_xor_3d.py / banco_lab.py)


def RG(rg, lec, **kw):
    d = dict(mundo='regla', regla=rg, lectura=lec); d.update(TR); d.update(kw); return d


def cmp(a, b, etiqueta, fallos, solo=None):
    """Compara TODAS las claves (y el conjunto de claves). `solo`: subconjunto de claves (referencia con menos claves)."""
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


# ---------------------------------------------------------------- (1) perillas nuevas apagadas == organismo_v13q_rapido
APAGADAS = {
    'ap_AB_tronco': dict(**TR),
    'ap_AB_defecto': dict(),
    'ap_AB_invertir': dict(**TR, invertir_en=T // 2),
    'ap_px0_lineal': RG('px0', 'lineal'),
    'ap_px0_cuadratica': RG('px0', 'cuadratica'),
    'ap_px0_random15': RG('px0', 'random15'),
    'ap_azar_cuadratica': RG('azar', 'cuadratica'),
    'ap_azar_random15': RG('azar', 'random15'),
    'ap_xor01_lineal': RG('xor01', 'lineal'),
    'ap_xor01_cuadratica': RG('xor01', 'cuadratica'),
    'ap_xor01_cuad_sonda': RG('xor01', 'cuadratica', sonda_final=True),
}

# ---------------------------------------------------------------- (2) la rejilla
CONFIGS = {}
# -- cada lectura x cada regla_lenta x constante on/off (20)
for _lec in ('lineal', 'cuadratica', 'random15', 'oraculo01', 'oraculo01_ruido'):
    for _rl in ('dos_canales', 'delta_signo'):
        for _ct in (False, True):
            CONFIGS[f'g_{_lec}_{_rl}_c{int(_ct)}'] = RG('xor01', _lec, regla_lenta=_rl, constante=_ct)
# -- los tres mundos (8 mas; xor01 ya sale entero arriba)
CONFIGS['m_px0_lin_dos'] = RG('px0', 'lineal')
CONFIGS['m_px0_cuad_delta_c1'] = RG('px0', 'cuadratica', regla_lenta='delta_signo', constante=True)
CONFIGS['m_px0_orac_dos'] = RG('px0', 'oraculo01')
CONFIGS['m_px0_r15_delta'] = RG('px0', 'random15', regla_lenta='delta_signo')
CONFIGS['m_azar_lin_delta'] = RG('azar', 'lineal', regla_lenta='delta_signo')
CONFIGS['m_azar_cuad_dos_c1'] = RG('azar', 'cuadratica', constante=True)
CONFIGS['m_azar_oracruido_delta'] = RG('azar', 'oraculo01_ruido', regla_lenta='delta_signo')
CONFIGS['m_azar_r15_dos'] = RG('azar', 'random15')
# -- seleccion 'wta' con las dos estadisticas (12)
CONFIGS['s_cuad_dos_cond'] = RG('xor01', 'cuadratica', seleccion='wta', sel_estad='cond')
CONFIGS['s_cuad_dos_cov'] = RG('xor01', 'cuadratica', seleccion='wta', sel_estad='cov')
CONFIGS['s_cuad_delta_cond'] = RG('xor01', 'cuadratica', seleccion='wta', sel_estad='cond', regla_lenta='delta_signo')
CONFIGS['s_cuad_delta_cov'] = RG('xor01', 'cuadratica', seleccion='wta', sel_estad='cov', regla_lenta='delta_signo')
CONFIGS['s_cuad_c1_cond'] = RG('xor01', 'cuadratica', seleccion='wta', sel_estad='cond', constante=True)
CONFIGS['s_r15_dos_cov'] = RG('xor01', 'random15', seleccion='wta', sel_estad='cov')
CONFIGS['s_orac_delta_cond'] = RG('xor01', 'oraculo01', seleccion='wta', sel_estad='cond', regla_lenta='delta_signo')
CONFIGS['s_oracruido_dos_cov'] = RG('xor01', 'oraculo01_ruido', seleccion='wta', sel_estad='cov')
CONFIGS['s_lineal_cond'] = RG('xor01', 'lineal', seleccion='wta', sel_estad='cond')            # sin candidatos: la competencia nunca abre
CONFIGS['s_cuad_cupo4'] = RG('xor01', 'cuadratica', seleccion='wta', sel_estad='cond', sel_cupo=4, sel_calienta=50, sel_theta=0.05, sel_rho=0.2)
CONFIGS['s_cuad_todos'] = RG('xor01', 'cuadratica', seleccion='wta', sel_estad='cov', sel_cupo=15, sel_theta=0.002, sel_rho=0.3, eta_s=0.15)
CONFIGS['s_cuad_sin_puerta'] = RG('xor01', 'cuadratica', seleccion='wta', sel_estad='cond', puerta=None)
# -- eta_s x clip_s, con las dos reglas lentas (12)
for _e in (0.015, 0.15, 1.0):
    for _c in (3, 10):
        CONFIGS[f'e{_e}_c{_c}_dos'] = RG('xor01', 'cuadratica', eta_s=_e, clip_s=_c)
        CONFIGS[f'e{_e}_c{_c}_delta'] = RG('xor01', 'cuadratica', eta_s=_e, clip_s=_c, regla_lenta='delta_signo')
# -- lab encendido (7): la secuencia lenta_eventos se compara elemento a elemento como una clave mas
CONFIGS['lab_cuad_dos'] = RG('xor01', 'cuadratica', lab=True)
CONFIGS['lab_cuad_delta_c1'] = RG('xor01', 'cuadratica', lab=True, regla_lenta='delta_signo', constante=True)
CONFIGS['lab_orac_wta_cov'] = RG('xor01', 'oraculo01', lab=True, seleccion='wta', sel_estad='cov', eta_s=0.15)
CONFIGS['lab_r15_sin_puerta'] = RG('xor01', 'random15', lab=True, puerta=None)
CONFIGS['lab_px0_lineal'] = RG('px0', 'lineal', lab=True)
CONFIGS['lab_azar_cuad_eta1'] = RG('azar', 'cuadratica', lab=True, eta_s=1.0)
CONFIGS['lab_AB_tronco'] = dict(**TR, lab=True)
# -- mundo 'AB' (13)
CONFIGS['AB_tronco'] = dict(**TR)
CONFIGS['AB_v13g_defecto'] = dict()
CONFIGS['AB_sin_puerta'] = dict(eta_s=0.015, puerta=None)
CONFIGS['AB_invertir'] = dict(**TR, invertir_en=T // 2)
CONFIGS['AB_nuevo_C'] = dict(**TR, nuevo='C', nuevo_en=T // 3)
CONFIGS['AB_nuevo_D_solapB'] = dict(**TR, nuevo='D', nuevo_en=T // 3, solap_B=1, nuevo_val='comida')
CONFIGS['AB_sin_plast'] = dict(**TR, plast=False)
CONFIGS['AB_sin_rechazo'] = dict(**TR, memoria_rechazo=0)
CONFIGS['AB_nobj6_lam0'] = dict(**TR, nobj=6, lam=0.0)
CONFIGS['AB_solapAB1'] = dict(**TR, solap_AB=1)
CONFIGS['AB_v9'] = dict(eta_s=0.0, puerta=None, div_signo=False, mu_norm=False)
CONFIGS['AB_delta_c1'] = dict(**TR, regla_lenta='delta_signo', constante=True, lectura='cuadratica')
CONFIGS['AB_wta_cuad_cov'] = dict(**TR, lectura='cuadratica', seleccion='wta', sel_estad='cov')
# -- el resto de las perillas que tocan claves de salida (8)
CONFIGS['x_sonda_cuad_delta_c1'] = RG('xor01', 'cuadratica', sonda_final=True, regla_lenta='delta_signo', constante=True)
CONFIGS['x_sonda_orac_wta'] = RG('xor01', 'oraculo01', sonda_final=True, seleccion='wta', sel_estad='cov')
CONFIGS['x_fase2_explicito'] = RG('px0', 'cuadratica', fase2_en=T // 3, regla_lenta='delta_signo')
CONFIGS['x_nuevo_en_regla'] = RG('px0', 'cuadratica', nuevo='111000', nuevo_en=T // 4, nuevo_val='comida', constante=True)
CONFIGS['x_v13g_defecto_regla'] = dict(mundo='regla', regla='azar', lectura='random15', regla_lenta='delta_signo')   # eta_s=0: la via lenta inerte
CONFIGS['x_sin_puerta_delta'] = RG('xor01', 'cuadratica', puerta=None, regla_lenta='delta_signo')
CONFIGS['x_sin_plast_orac'] = RG('xor01', 'oraculo01_ruido', plast=False, constante=True)
CONFIGS['x_lam_lenta_05'] = RG('xor01', 'cuadratica', regla_lenta='delta_signo', lam_lenta=0.05, eta_s=0.15)
# -- los puntos de PRODUCCION de la linea: los que ya consumen los instrumentos de creacion_A (4)
CONFIGS['p_cosecha_lab'] = RG('xor01', 'cuadratica', constante=True, regla_lenta='delta_signo', lam_lenta=0.0, clip_s=3.0, lab=True)   # cosecha_lab.py
CONFIGS['p_seleccion_cuad_cov'] = RG('xor01', 'cuadratica', constante=True, regla_lenta='delta_signo', lam_lenta=0.0, eta_s=0.05, clip_s=10.0,
                                     seleccion='wta', sel_theta=0.6, sel_rho=0.05, sel_cupo=1, sel_calienta=0, sel_estad='cov')          # mini_prueba_A_seleccion.py, brazo COV
CONFIGS['p_seleccion_orac_cond'] = RG('xor01', 'oraculo01', constante=True, regla_lenta='delta_signo', lam_lenta=0.0, eta_s=0.05, clip_s=10.0,
                                      seleccion='wta', sel_theta=0.6, sel_rho=0.05, sel_cupo=1, sel_calienta=0, sel_estad='cond')        # idem, brazo COND
CONFIGS['p_ganadora'] = RG('xor01', 'cuadratica', constante=True, regla_lenta='delta_signo', lab=True, eta_s=0.15, clip_s=10.0, lam_lenta=0.0,
                           seleccion='wta', sel_theta=0.3, sel_rho=0.02, sel_cupo=1, sel_estad='cond')                                   # mini_prueba_A_ganadora.py (regla GANADORA del meta-aprendizaje)

_desde = int(sys.argv[sys.argv.index('--desde') + 1]) if '--desde' in sys.argv else 1
_n = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 2
SEEDS = list(range(_desde, _desde + _n))

# ---------------------------------------------------------------- (3) T largo  y  (4) proceso nuevo
LARGAS = [('g_cuadratica_dos_canales_c0', 4), ('g_cuadratica_delta_signo_c1', 4),
          ('s_cuad_dos_cov', 5), ('lab_cuad_delta_c1', 5),
          ('p_cosecha_lab', 6), ('p_ganadora', 6)]
HIJO = [('h_AB_tronco', 1, dict(**TR)),
        ('h_cuad_dos', 1, RG('xor01', 'cuadratica')),
        ('h_cuad_delta_c1', 2, RG('xor01', 'cuadratica', regla_lenta='delta_signo', constante=True)),
        ('h_r15_wta_cond', 2, RG('px0', 'random15', seleccion='wta', sel_estad='cond')),
        ('h_orac_wta_cov', 3, RG('xor01', 'oraculo01', seleccion='wta', sel_estad='cov', eta_s=0.15)),
        ('h_oracruido_delta', 3, RG('azar', 'oraculo01_ruido', regla_lenta='delta_signo')),
        ('h_lab_cuad', 4, RG('xor01', 'cuadratica', lab=True, eta_s=1.0, clip_s=10)),
        ('h_sonda_lineal', 4, RG('px0', 'lineal', sonda_final=True, constante=True))]


def _hijo():
    """Proceso NUEVO: importa el gemelo (leyendo la cache de numba) y reproduce los casos de HIJO."""
    t0 = time.time(); res = {}
    for i, (etiq, s, kw) in enumerate(HIJO):
        res[etiq] = N(RAPIDO.run(s, T=T, **kw))
        if i == 0: t_primero = time.time() - t0
    print('###JSON###' + json.dumps(dict(t_primero=t_primero, res=res)))


if __name__ == '__main__':
    if '--hijo' in sys.argv:
        _hijo(); sys.exit(0)
    t00 = time.time()
    print(f"organismo_v13q5.py           sha {__import__('hashlib').sha256(open(LENTO.__file__,'rb').read()).hexdigest()[:16]}")
    print(f"organismo_v13q5_rapido.py    sha {__import__('hashlib').sha256(open(RAPIDO.__file__,'rb').read()).hexdigest()[:16]}")
    fallos = []; n = 0

    # ---- (0) la firma
    sa = inspect.signature(LENTO.run); sb = inspect.signature(RAPIDO.run); n += 1
    if [(p.name, p.default) for p in sa.parameters.values()] != [(p.name, p.default) for p in sb.parameters.values()]:
        fallos.append(('0/firma', ['firma distinta'])); print(f"  DIFIERE 0/firma:\n    {sa}\n    {sb}", flush=True)
    else:
        print(f"(0) firma identica parametro a parametro ({len(sa.parameters)} parametros)")

    t0 = time.time(); RAPIDO.run(1, T=2000); RAPIDO.run(1, T=2000, **RG('px0', 'cuadratica'))
    print(f"compilacion/carga de cache: {time.time()-t0:.1f}s", flush=True)

    # ---- (1) perillas nuevas apagadas: a tres bandas
    print(f"\n(1) perillas nuevas apagadas == organismo_v13q_rapido (gemelo validado) y == organismo_v13q5 interpretado")
    for nombre, kw in APAGADAS.items():
        for s in SEEDS:
            a = LENTO.run(s, T=T, **kw); b = RAPIDO.run(s, T=T, **kw); c = Q_RAP.run(s, T=T, **{k: v for k, v in kw.items() if k in inspect.signature(Q_RAP.run).parameters})
            n += 1; cmp(a, b, f"1/{nombre}/s{s}/v13q5", fallos)
            n += 1; cmp(b, c, f"1/{nombre}/s{s}/v13q_rapido", fallos, solo=list(c))
        print(f"  {nombre:22s} {len(SEEDS)} semillas x 2 referencias", flush=True)

    # ---- (2) la rejilla
    print(f"\n(2) rejilla: {len(CONFIGS)} configuraciones x {len(SEEDS)} semillas a T={T}")
    tc = time.time()
    for ic, (nombre, kw) in enumerate(CONFIGS.items(), 1):
        fc = 0
        for s in SEEDS:
            a = LENTO.run(s, T=T, **kw); b = RAPIDO.run(s, T=T, **kw); n += 1
            if not cmp(a, b, f"2/{nombre}/s{s}", fallos): fc += 1
        print(f"  [{time.strftime('%H:%M:%S')} +{time.time()-tc:6.1f}s] {ic:3d}/{len(CONFIGS)} {nombre:28s} {len(SEEDS)-fc}/{len(SEEDS)} semillas identicas", flush=True)   # REGLA 10

    # ---- (3) T largo + aceleracion
    print(f"\n(3) T in (30000, 100000, 200000)")
    tl_tot = tr_tot = 0.0
    for nombre, s in LARGAS:
        for TL in (30000, 100000, 200000):
            kw = CONFIGS[nombre]
            t1 = time.time(); a = LENTO.run(s, T=TL, **kw); dl = time.time() - t1
            t1 = time.time(); b = RAPIDO.run(s, T=TL, **kw); dr = time.time() - t1
            n += 1; ok = cmp(a, b, f"3/{nombre}/s{s}/T{TL}", fallos)
            if TL == 200000: tl_tot += dl; tr_tot += dr
            print(f"  {nombre:28s} s{s} T={TL:6d}: original {dl:6.2f}s, gemelo {dr:5.2f}s -> x{dl/dr:5.1f}  {'OK' if ok else 'FALLA'}", flush=True)

    # ---- (4) proceso nuevo que lee la cache
    print(f"\n(4) proceso NUEVO que lee la cache de numba (subprocess)")
    aqui_res = {etiq: N(RAPIDO.run(s, T=T, **kw)) for etiq, s, kw in HIJO}
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    tp = time.time()
    pr = subprocess.run([sys.executable, os.path.abspath(__file__), '--hijo', '--T', str(T)],
                        capture_output=True, text=True, env=env, cwd=RAIZ, timeout=3600)
    t_sub = time.time() - tp
    linea = [l for l in pr.stdout.splitlines() if l.startswith('###JSON###')]
    if pr.returncode != 0 or not linea:
        n += 1; fallos.append(('4/subproceso', ['sin salida']))
        print(f"  DIFIERE 4/subproceso: codigo {pr.returncode}\n{pr.stderr[-1500:]}")
    else:
        hijo = json.loads(linea[0][len('###JSON###'):])
        print(f"  proceso nuevo: {t_sub:.1f}s en total, primer run del gemelo {hijo['t_primero']:.2f}s "
              f"(la cache se leyo: {'SI' if hijo['t_primero'] < 3.0 else 'NO'})")
        for etiq, s, kw in HIJO:
            n += 1; cmp(aqui_res[etiq], hijo['res'][etiq], f"4/{etiq}", fallos)
    pc = os.path.join(AQUI, '__pycache__')
    nb = [f for f in os.listdir(pc) if f.endswith(('.nbi', '.nbc'))] if os.path.isdir(pc) else []
    print(f"  cache numba en creacion_A/__pycache__/: {sum(f.startswith('organismo_v13q5_rapido') for f in nb)} archivos del gemelo")

    print(f"\nIDENTIDAD {n - len(fallos)}/{n} comparaciones identicas   ({time.time()-t00:.1f}s)")
    if tr_tot:
        print(f"ACELERACION a 200000 pasos ({len(LARGAS)} casillas): original {tl_tot:.2f}s, gemelo {tr_tot:.2f}s -> x{tl_tot/tr_tot:.1f}")
    if fallos:
        print("FALLOS:"); [print('  ', f) for f in fallos]
    print("limitaciones declaradas: log_cada no esta compilado (ValueError); invertir_en solo con mundo='AB'; "
          "`nuevo` antes de `invertir_en` no se admite (el original pierde val[nuevo]).")
    sys.exit(1 if fallos else 0)
