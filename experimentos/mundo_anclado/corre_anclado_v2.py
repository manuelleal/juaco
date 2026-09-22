"""corre_anclado_v2.py -- MUNDO ANCLADO v2 (enmienda de diseno tras el NO de la v1; ERR-? pendiente).
Ejecuta PREREGISTRO_mundo_anclado_v2.md. Mision: llegar a la AGI por este camino.

DOS perillas del MUNDO, las dos POR OBJETO:
  tox = k    -> cada bocado de un objeto MALO hace k veces su dano nominal (tabla del mundo: veneno (-0.4k, 0),
                sal (0, -0.4k)); lo bueno intacto. Via el kwarg `tabla` que YA existe en organismo_f9c: la
                recompensa que aprende el cuerpo depende solo del SIGNO (_Rv), asi que el aprendizaje no cambia,
                cambia la consecuencia. tox=1 -> tabla == EFECTO (identidad comprobada en --humo).
  olv_mal = h -> dilucion por objeto de lo malo (organismo_anclado.py, v1, sha e689c2952b1991a4).
Instrumento, brazos y resumen: los de corre_anclado.py (v1, commit afcc7e9), importados, no copiados.

    python experimentos/mundo_anclado/corre_anclado_v2.py --humo                 (semilla 1, 6 corridas + identidad tox=1)
    python experimentos/mundo_anclado/corre_anclado_v2.py --calibra --fila K     (7021-7040, UNA fila de la rejilla)
    python experimentos/mundo_anclado/corre_anclado_v2.py --elige SELLO1,SELLO2,...  (aplica la regla 5 a las filas)
    python experimentos/mundo_anclado/corre_anclado_v2.py --confirma --tox K --h H --desde 7041 [--pool N]
"""
import argparse, json, os, statistics as st, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_anclado as CA

B2, ANC, log, md, h16 = CA.B2, CA.ANC, CA.log, CA.md, CA.h16
T = CA.T
PREREG2 = os.path.join(AQUI, 'PREREGISTRO_mundo_anclado_v2.md')
PERILLAS = CA.PERILLAS + ('tabla',)

# ------------------------------------------------------------------ LA LETRA DEL PREREGISTRO v2
CAL_DESDE, CONF_DESDE, REP_DESDE, NSEM = 7021, 7041, 7061, 20
TOX = [1.25, 1.5, 2.0]                   # filas
HS = [0.003, 0.006, 0.012]               # columnas, ASCENDENTES dentro de cada fila
ANCLA_NADA, ANCLA_OR = CA.ANCLA_NADA, CA.ANCLA_OR


def tabla(k):
    E = ANC.EFECTO
    return {v: tuple((x * k if x < 0 else x) for x in E[v]) for v in E}


def kwargs(brazo, tox, h):
    kw = CA.kwargs(brazo, 0, h)
    if tox != 1:
        kw['tabla'] = tabla(tox)
    return kw


def regla14():
    for b in CA.BRAZOS:
        base = CA.BRAZOS[b][0]; kw = kwargs(b, 2.0, 0.006); ref = B2.BRAZOS[base]
        falta = [k for k in ref if k not in kw]
        dif = [k for k in ref if k in kw and kw[k] is not ref[k] and kw[k] != ref[k]]
        extra = [k for k in kw if k not in ref and k not in PERILLAS]
        ok = not (falta or dif or extra)
        log(f"  {'OK  ' if ok else 'FALLA'} regla14 {b:14s} = corre_bloque2.BRAZOS[{base!r}] + {sorted(k for k in kw if k not in ref)}")
        if not ok:
            raise SystemExit('REGLA 14 FALLA')


def cabecera(modo):
    log(f"MUNDO ANCLADO v2 · {modo} · {time.strftime('%Y-%m-%d %H:%M:%S')} · T={T}")
    sa = h16(os.path.join(AQUI, 'organismo_anclado.py'))
    log(f"  organismo_anclado {sa} (esperado {CA.SHA_ANC})")
    if sa != CA.SHA_ANC:
        raise SystemExit('SHA del instrumento cambio')
    if os.path.exists(PREREG2):
        log(f"  PREREGISTRO v2 sha {h16(PREREG2)}")
    elif not modo.startswith('HUMO'):
        raise SystemExit('sin PREREGISTRO_mundo_anclado_v2.md no se calibra ni se confirma')
    regla14()


def tarea(args):
    brazo, seed, tox, h = args
    t0 = time.time()
    r = ANC.run(seed, T=T, **kwargs(brazo, tox, h))
    o = CA.resumen(brazo, seed, 0, h, r, time.time() - t0); o['tox'] = tox
    return o


def corre(tareas, pool):
    if pool and pool > 1:
        from multiprocessing import Pool
        with Pool(pool) as P:
            return list(P.imap(tarea, tareas))
    out = []
    for t in tareas:
        o = tarea(t); out.append(o)
        log(f"    {o['brazo']:14s} s{o['seed']} tox={o['tox']} h={o['h']}  R0={o['R0']:.3f}  vida={o['vida_med']}  "
            f"f_mala={o['f_mala']}  J={o['J']}  ({o['seg']:.1f}s)")
    return out


def abre_log(nombre, carpeta):
    os.makedirs(carpeta, exist_ok=True)
    CA.LOG[0] = open(os.path.join(carpeta, nombre + '.log'), 'w', encoding='utf-8')


# ------------------------------------------------------------------ modos
def humo():
    s = time.strftime('%Y%m%d_%H%M%S'); abre_log(f'anclado2_humo_{s}', CA.HUMO)
    cabecera('HUMO v2 (semilla 1, ya vista; identidad tox=1 + 6 corridas)')
    kw0 = CA.kwargs('ORACULO', 0, 0.003)
    a = ANC.run(1, T=20000, **kw0); b = ANC.run(1, T=20000, **dict(kw0, tabla=tabla(1.0)))
    ok = json.dumps(a, sort_keys=True, default=str) == json.dumps(b, sort_keys=True, default=str)
    log(f"  {'OK  ' if ok else 'FALLA'} identidad: tabla(1.0) == EFECTO (ORACULO s1 h=0.003 T=20000, dict completo)")
    if not ok:
        raise SystemExit('tabla(1.0) no es identica')
    R = corre([('NADA', 1, 1.25, 0.006), ('ORACULO', 1, 1.25, 0.006), ('NADA', 1, 1.5, 0.006),
               ('ORACULO', 1, 1.5, 0.006), ('NADA', 1, 2.0, 0.012), ('ORACULO', 1, 2.0, 0.012)], 1)
    CA.escribe(os.path.join(CA.HUMO, f'anclado2_humo_{s}.json'), dict(modo='humo_v2', sello=s, T=T, corridas=R))


def calibra_fila(k, pool):
    tox = TOX[k]; s = time.strftime('%Y%m%d_%H%M%S')
    tag = f'anclado2_cal_s{CAL_DESDE}-{CAL_DESDE + NSEM - 1}_fila{k}_{s}'
    abre_log(tag, CA.DATOS)
    cabecera(f'CALIBRACION v2 fila {k} (tox={tox}) semillas {CAL_DESDE}-{CAL_DESDE + NSEM - 1}')
    semillas = list(range(CAL_DESDE, CAL_DESDE + NSEM)); todo, filas = [], []
    ruta = os.path.join(CA.DATOS, tag + '.json')
    for h in HS:
        log(f"  punto tox={tox} h={h}")
        R = corre([(b, sd, tox, h) for b in ('NADA', 'ORACULO') for sd in semillas], pool)
        todo += R
        nada, orac = md(R, 'NADA'), md(R, 'ORACULO')
        filas.append(dict(tox=tox, h=h, R0_NADA=nada, R0_OR=orac, razon=(round(orac / nada, 2) if nada else None),
                          ancla=CA.ancla_ok(nada, orac, ANCLA_NADA, ANCLA_OR),
                          vida_NADA=md(R, 'NADA', 'vida_med'), vida_OR=md(R, 'ORACULO', 'vida_med'),
                          fmala_NADA=md(R, 'NADA', 'f_mala'), fmala_OR=md(R, 'ORACULO', 'f_mala'),
                          J_NADA=md(R, 'NADA', 'J'), J_OR=md(R, 'ORACULO', 'J')))
        CA.escribe(ruta, dict(modo='calibra_v2', fila=k, tox=tox, sello=s, T=T, corridas=todo, filas=filas))
        log(f"  -> R0 NADA {nada}  R0 ORACULO {orac}  razon {filas[-1]['razon']}  ancla={'SI' if filas[-1]['ancla'] else 'no'}")
        if orac is not None and orac >= ANCLA_OR:
            log("  ORACULO ya >= 1.0: en esta fila los h mayores solo inflan el mundo (regla 5b); fila cerrada"); break
        if nada is not None and nada > ANCLA_NADA[1]:
            log("  NADA > 0.30: los h mayores no pueden devolverla al ancla (regla 5b); fila cerrada"); break
    log(f"  FILA {k} CERRADA: {filas}")


def elige(sellos):
    filas = []
    for s in sellos:
        import glob
        g = glob.glob(os.path.join(CA.DATOS, f'anclado2_cal_s{CAL_DESDE}-*_fila*_{s}.json'))
        if len(g) != 1:
            raise SystemExit(f'sello {s}: se esperaba UN json de fila, hay {len(g)} (ERR-87)')
        filas += json.load(open(g[0], encoding='utf-8'))['filas']
    if sorted({f['tox'] for f in filas}) != sorted(TOX):
        raise SystemExit(f'faltan filas: {sorted({f["tox"] for f in filas})} != {TOX}')
    for f in filas:
        print(f"  tox={f['tox']:<5} h={f['h']:<6} NADA {f['R0_NADA']}  ORACULO {f['R0_OR']}  razon {f['razon']}  ancla={'SI' if f['ancla'] else 'no'}")
    c = [f for f in filas if f['ancla']]
    if not c:
        print('  PUNTO ELEGIDO: NINGUNO -> NO (regla 5d, sin ampliar)'); return
    p = min(c, key=lambda f: (f['R0_OR'], f['tox'], f['h']))
    print(f"  PUNTO ELEGIDO (regla 5c: el ORACULO mas bajo >= 1.0): tox={p['tox']} h={p['h']}  NADA {p['R0_NADA']}  ORACULO {p['R0_OR']}")
    print(f"  confirmacion: python experimentos/mundo_anclado/corre_anclado_v2.py --confirma --tox {p['tox']} --h {p['h']} --desde {CONF_DESDE} --pool N")


def confirma(tox, h, desde, pool, brazos):
    s = time.strftime('%Y%m%d_%H%M%S'); tag = f'anclado2_conf_s{desde}-{desde + NSEM - 1}_{s}'
    abre_log(tag, CA.DATOS)
    cabecera(f'CONFIRMACION v2 {desde}-{desde + NSEM - 1} tox={tox} h={h} brazos {brazos}')
    R = corre([(b, sd, tox, h) for b in brazos for sd in range(desde, desde + NSEM)], pool)
    CA.escribe(os.path.join(CA.DATOS, tag + '.json'), dict(modo='confirma_v2', sello=s, T=T, tox=tox, h=h, corridas=R))
    CA.juzga(R, h, 0)   # MISMAS puertas que la v1 (ANC-1, ANC-2, REL posicion, CTL-1 BARAJA, CTL-2 PLACEBO, reportes)
    log(f"  P-REL (v2): REL R0 {md(R, 'REL')} (prediccion firmada en el preregistro v2, sec. 7)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--humo', action='store_true')
    ap.add_argument('--calibra', action='store_true')
    ap.add_argument('--fila', type=int)
    ap.add_argument('--elige')
    ap.add_argument('--confirma', action='store_true')
    ap.add_argument('--tox', type=float)
    ap.add_argument('--h', type=float)
    ap.add_argument('--desde', type=int, default=CONF_DESDE)
    ap.add_argument('--brazos', default=','.join(CA.CONF_ORDEN))
    ap.add_argument('--pool', type=int, default=1)
    a = ap.parse_args()
    if a.humo:
        humo()
    elif a.calibra:
        if a.fila not in range(len(TOX)):
            raise SystemExit(f'--fila en 0..{len(TOX) - 1}')
        calibra_fila(a.fila, a.pool)
    elif a.elige:
        elige(a.elige.split(','))
    elif a.confirma:
        if a.tox is None or a.h is None:
            raise SystemExit('--confirma exige --tox y --h')
        confirma(a.tox, a.h, a.desde, a.pool, a.brazos.split(','))
    else:
        ap.print_help()


if __name__ == '__main__':
    main()
