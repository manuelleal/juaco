"""Arnes de identidad del GEMELO COMPILADO de la fase 9: organismo_f9_rapido.run(...) debe ser BIT A BIT igual
(TODAS las claves, tras ida y vuelta por JSON) a organismo_f9.run(...).

MISION: llegar a la AGI por este camino (organismo minimo, reglas locales, sin retropropagacion, peldanos
preregistrados con controles y replicas). Un gemelo que no sea bit a bit identico SOLO EXPLORA, nunca confirma.
Regla 9 de registro/EQUIPO.md: la salida de este arnes se entrega con el gemelo.

QUE SE COMPARA
  (1) LOS NUEVE BRAZOS de corre_f9.py (RENACE, NADA, M1, REC, REL, REL_FIJO, REL_BAR, REL_AZAR, REL_TARDE)
      x los DOS niveles de rep_acum = 18 celdas, con sus perillas exactas (nodo, conectado, nodo_rel,
      con_desde, nodo_baraja, nodo_k, nodo_lee, menu='f', alma nula, f9=1).
  (2) LA CADENA APAGADA: v14 (todo apagado), el linaje v13 (mask_rel=0, puerta_pat=0), el mundo vivo solo,
      la reproduccion sin cuello / con CUELLO / con CUELLO_MIN, ESCALAR (val_esc), sin herencia entre
      necesidades, sin puerta, y la muerte real con vivo=0 (el _nace del tronco).
  (3) EL ALMA DE VERDAD: un alma que recorre TODO el menu ('abcdef': conectar, miedo escrito en el nodo, dote
      mayor, umbral menor, heredar M1, nada), un menu recortado ('af'), el tope de muertes (alma_muertes
      chico: corte anticipado y T_efectivo), un nodo_lee enorme, una cola chica (desborde) y los puntos de
      rampa de H-1 (costo 0.0005 con regalo 1200; nobj 8 con rep_X 250 y dote 0.3).
  (4) CONTROLES QUE DEBEN DIFERIR (si no cambia nada, no controla nada — ERR-38): REL != REC, REL_BAR,
      REL_AZAR, REL_FIJO y REL_TARDE; NADA != M1 y != RENACE; rep_acum=1 != rep_acum=0; semilla vecina; y el
      cruce gemelo(REL) != tronco(REC), para que "identico" no sea "identico a cualquier cosa".
  (5) GUARDIAS: las mismas SystemExit del original (nodo_rel invalido, nodo_rel sin nodo, con_desde sin nodo,
      con_desde con conectado, f9 sin h1, dote >= rep_umbral) y los ValueError propios del gemelo por lo que
      NO compila (log_cada, nec_shuf, predictor, tercera necesidad, hereda M1+pares/baraja).
  (6) DETERMINISMO: dos llamadas iguales dan el mismo dict.
  (7) ACELERACION a T=100000 y comprobacion de que el cache de numba lo lee un proceso NUEVO (regla 9: se
      imprime el tiempo de la primera llamada; al correr el arnes por segunda vez debe caer a ~1 s).

Un proceso, sin Pool (regla 3). OJO (ERR-28): organismo/ va primero en sys.path.
Uso:  python experimentos/nivel09_cuerpo_nuevo/identidad_f9_rapido.py [--T 20000] [--rapido]
"""
import json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N11 = os.path.join(RAIZ, 'experimentos', 'nivel11_mundo_vivo')
N13 = os.path.join(RAIZ, 'experimentos', 'nivel13_alma')
sys.path[:0] = [AQUI, N13, N11, os.path.join(RAIZ, 'organismo')]

import organismo_f9 as lento
import organismo_f9_rapido as rapido
import corre_f9 as CF

T = int(sys.argv[sys.argv.index('--T') + 1]) if '--T' in sys.argv else 20000
SEEDS = ([int(x) for x in sys.argv[sys.argv.index('--semillas') + 1].split(',')]
         if '--semillas' in sys.argv else [1501, 1502, 1503])
N = lambda x: json.loads(json.dumps(x, default=str))
CUERPO = dict(CF.CUERPO)
NODO = dict(CF.NODO)
GRANDE = CF.GRANDE


def fija(c):
    return lambda res: {'curita': c, 'motivo': f'arnes: siempre ({c})'}


def alma_ciclo(res):
    """Recorre el MENU CERRADO entero en orden, cuerpo a cuerpo: a,b,c,d,e,f,a,b,..."""
    c = 'abcdef'[int(res['cuerpo']) % 6]
    return {'curita': c, 'motivo': f"arnes ciclo cuerpo {res['cuerpo']} causa {res['causa']} R0 {res['R0']}"}


CONFIGS = {}
for _b in CF.ORDEN:
    for _a in CF.ACUM:
        CONFIGS[f'{_b}_acum{_a}'] = dict(CF.BRAZOS[_b], rep_acum=_a)
REL = dict(CF.BRAZOS['REL'])
CONFIGS.update({
    'V14_APAGADO':      dict(),
    'V13_LINAJE':       dict(mask_rel=0, puerta_pat=0),
    'VIVO_SOLO':        dict(vivo=1, n_nec=2, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001),
    'VIVO_2EST':        dict(vivo=1, n_nec=1, estims=('A', 'B'), costo_a=0.0),
    'REP_SIN_CUELLO':   dict(CUERPO, rep_cuello=0),
    'REP_CUELLO1':      dict(CUERPO, rep_cuello=1),
    'ESCALAR':          dict(CUERPO, val_esc=1),
    'SIN_HEREDA_NEC':   dict(CUERPO, hereda_nec=0),
    'SIN_PUERTA':       dict(CUERPO, rep_cuello=0, puerta=None),
    'MORTAL_V14':       dict(vivo=0, n_nec=1, reproduccion=1, rep_mide=1, rep2=1, h1=1, muerte_real=1,
                             hereda='nada', dote=0.6, rep_X=500, rep_umbral=1.0),
    'MORTAL_V14_M1':    dict(vivo=0, n_nec=1, reproduccion=1, rep_mide=1, rep2=1, h1=1, muerte_real=1,
                             hereda='M1', dote=0.6, rep_X=500, rep_umbral=1.0, rep_acum=1),
    'ALMA_CICLO_REL':   dict(CUERPO, **dict(NODO, alma=alma_ciclo, menu='abcdef'), nodo=1, conectado=1, nodo_rel=1),
    'ALMA_CICLO_REC':   dict(CUERPO, **dict(NODO, alma=alma_ciclo, menu='abcdef'), nodo=1, conectado=1, nodo_rel=0,
                             nodo_baraja=1, rep_acum=1),
    'ALMA_CICLO_TARDE': dict(CUERPO, **dict(NODO, alma=alma_ciclo, menu='abcdef'), nodo=1, conectado=0,
                             nodo_rel=3, con_desde=3, miedo_n=3, miedo_R=-2.0),
    'MENU_AF':          dict(REL, **dict(NODO, alma=fija('a'), menu='af'), nodo=1, conectado=0, nodo_rel=1, con_desde=0),
    'ALMA_TOPE7':       dict(REL, alma_muertes=7),
    'NODO_GRANDE':      dict(REL, nodo_lee=1000, nodo_k=5),
    'REL_FIJO_GRANDE':  dict(CF.BRAZOS['REL_FIJO'], nodo_lee=1000),
    'REL_AZAR_LEE10':   dict(CF.BRAZOS['REL_AZAR'], nodo_lee=10),
    'RAMPA_C05':        dict(REL, costo=0.0005, costo_a=0.0005, rep2_regalo=1200),
    'RAMPA_N8_X250':    dict(REL, nobj=8, rep_X=250, dote=0.3, cola_max=3, rep_acum=1),
    'COLA_CHICA':       dict(CF.BRAZOS['M1'], cola_max=2, rep_X=200),
    # --- casos que fuerzan los caminos raros del gemelo (buffers que crecen, tablas, inercias)
    'MUCHAS_MUERTES':   dict(REL, costo=0.01, costo_a=0.01),
    'VIDA_LARGA':       dict(REL, costo=0.0002, costo_a=0.0002, rep2_regalo=3000),
    'REP_COSTE':        dict(vivo=1, n_nec=2, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001,
                             reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0, rep_coste=0.4, rep_cuello=2),
    'NO_INFORMA':       dict(vivo=1, n_nec=2, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001,
                             tabla={'comida': (+0.8, 0.0), 'veneno': (-0.4, 0.0), 'agua': (0.0, +0.8), 'sal': (0.0, 0.0)}),
    'A_INI_BAJO':       dict(CUERPO, A_ini=0.5),
    'MIEDO_INERTE':     dict(CUERPO, alma=fija('b'), alma_muertes=GRANDE, menu='bf', f9=1, nodo=0, conectado=0,
                             nodo_k=20, nodo_lee=50),
})

# controles que DEBEN diferir: (etiqueta, kwargs A, semilla A, kwargs B, semilla B) sobre el GEMELO,
# salvo el ultimo, que cruza gemelo y tronco.
CONTROLES = [
    ('REL != REC',                 CF.BRAZOS['REL'], 0, CF.BRAZOS['REC'], 0),
    ('REL != REL_BAR',             CF.BRAZOS['REL'], 0, CF.BRAZOS['REL_BAR'], 0),
    ('REL != REL_AZAR',            CF.BRAZOS['REL'], 0, CF.BRAZOS['REL_AZAR'], 0),
    ('REL != REL_FIJO',            CF.BRAZOS['REL'], 0, CF.BRAZOS['REL_FIJO'], 0),
    ('REL != REL_TARDE',           CF.BRAZOS['REL'], 0, CF.BRAZOS['REL_TARDE'], 0),
    ('NADA != M1',                 CF.BRAZOS['NADA'], 0, CF.BRAZOS['M1'], 0),
    ('NADA != RENACE',             CF.BRAZOS['NADA'], 0, CF.BRAZOS['RENACE'], 0),
    ('NADA rep_acum 1 != 0',       dict(CF.BRAZOS['NADA'], rep_acum=1), 0, CF.BRAZOS['NADA'], 0),
    ('REL rep_acum 1 != 0',        dict(CF.BRAZOS['REL'], rep_acum=1), 0, CF.BRAZOS['REL'], 0),
    ('REL semilla vecina',         CF.BRAZOS['REL'], 0, CF.BRAZOS['REL'], 1),
    ('ALMA_CICLO != alma nula',    CONFIGS['ALMA_CICLO_REL'], 0, CF.BRAZOS['REL'], 0),
]

# guardias: (etiqueta, kwargs, excepcion esperada en el tronco o None si el tronco lo admite)
GUARDIAS = [
    ('nodo_rel=4',            dict(REL, nodo_rel=4), SystemExit),
    ('nodo_rel sin nodo',     dict(REL, nodo=0, conectado=0, nodo_rel=1), SystemExit),
    ('con_desde sin nodo',    dict(REL, nodo=0, conectado=0, con_desde=3), SystemExit),
    ('con_desde y conectado', dict(REL, con_desde=3), SystemExit),
    ('f9 sin h1',             dict(vivo=1, n_nec=2, estims=('A', 'B', 'C', 'D'), costo=0.001, costo_a=0.001,
                                   reproduccion=1, rep2=1, muerte_real=1, h1=0, alma=fija('f'),
                                   alma_muertes=GRANDE, menu='f', f9=1), SystemExit),
    ('dote >= rep_umbral',    dict(REL, dote=1.5), SystemExit),
    ('menu vacio',            dict(REL, menu=''), SystemExit),
]
NO_COMPILA = [
    ('log_cada',    dict(REL, log_cada=1000)),
    ('nec_shuf',    dict(CUERPO, nec_shuf=1)),
    ('eta_pred',    dict(CUERPO, eta_pred=0.05)),
    ('k_sorp',      dict(CUERPO, k_sorp=0.2)),
    ('hereda pares', dict(CUERPO, hereda='M1+pares')),
    ('hereda baraja', dict(CUERPO, hereda='baraja')),
]


def compara(a, b):
    falta = [k for k in a if k not in b]
    extra = [k for k in b if k not in a]
    dif = [k for k in a if k in b and N(a[k]) != N(b[k])]
    return falta, dif, extra


if __name__ == '__main__':
    print(f"ARNES DE IDENTIDAD — organismo_f9_rapido vs organismo_f9   (T={T}, semillas {SEEDS})")
    t0 = time.time(); rapido.run(1501, T=600, **CF.BRAZOS['REL']); tc = time.time() - t0
    print(f"compilacion / carga del cache de numba: {tc:.1f}s   (proceso NUEVO: al repetir el arnes debe caer a ~1s)")
    fallos = []; n = 0; tl_tot = 0.0; tr_tot = 0.0; testigos = []
    cobertura = dict(muertes_max=0, splits_max=0, nodo_max=0, cola_desborde=0, miedo_inerte=0,
                     fundadores=0, desc=0, lect_div=0, curitas=0)
    for nombre, kw in CONFIGS.items():
        for s in SEEDS:
            t0 = time.time(); a = lento.run(s, T=T, **kw); tl_tot += time.time() - t0
            t0 = time.time(); b = rapido.run(s, T=T, **kw); tr_tot += time.time() - t0
            falta, dif, extra = compara(a, b); n += 1
            if nombre.endswith('_acum0') and s == SEEDS[0]:
                testigos.append((nombre[:-6], a, b))
            cobertura['muertes_max'] = max(cobertura['muertes_max'], b['deaths'])
            cobertura['splits_max'] = max(cobertura['splits_max'], b['splits'])
            cobertura['nodo_max'] = max(cobertura['nodo_max'], b.get('nodo_n') or 0)
            cobertura['cola_desborde'] += b.get('cola_desborde') or 0
            cobertura['miedo_inerte'] += b.get('miedo_inerte') or 0
            cobertura['fundadores'] += b.get('fundadores') or 0
            cobertura['desc'] += b.get('descendientes') or 0
            cobertura['lect_div'] += (b.get('f9') or {}).get('lect_div') or 0
            cobertura['curitas'] += len(b.get('curitas') or [])
            if falta or dif or extra:
                fallos.append((nombre, s, falta, dif, extra))
                print(f"  DIFIERE {nombre} s{s}: falta={falta[:4]} dif={dif[:6]} extra={extra[:4]}")
                for k in dif[:3]:
                    print(f"      {k}: tronco {str(N(a[k]))[:160]}")
                    print(f"      {k}: gemelo {str(N(b[k]))[:160]}")
    print(f"\nIDENTIDAD: {n - len(fallos)}/{n} corridas identicas "
          f"({len(CONFIGS)} configuraciones x {len(SEEDS)} semillas, T={T}, todas las claves)")
    print(f"   tiempo total: tronco {tl_tot:.1f}s, gemelo {tr_tot:.1f}s -> x{tl_tot / max(tr_tot, 1e-9):.1f} sobre el arnes entero")

    def T9(r, c):   # los testigos del preregistro, leidos del dict como los lee corre_f9.py
        f9d = r.get('f9') or {}
        v = dict(muertes=r['deaths'], nacim=r.get('nacimientos'), fund=r.get('fundadores'),
                 desc=r.get('descendientes'), R0=round(r.get('descendientes', 0) / max(r['deaths'], 1), 4),
                 vida_med=round(sum(r.get('vidas_h1', [0])) / max(len(r.get('vidas_h1', [0])), 1), 1),
                 nodo_esc=r.get('nodo_n'), lect=f9d.get('lecturas'), div=f9d.get('lect_div'),
                 p1=[x for x in f9d.get('p1', []) if x >= 0], c1=[x for x in f9d.get('c1', []) if x >= 0])
        v['p1'] = round(sum(v['p1']) / len(v['p1']), 3) if v['p1'] else None
        v['c1'] = round(sum(v['c1']) / len(v['c1']), 3) if v['c1'] else None
        return v[c]

    COLS = ['muertes', 'nacim', 'fund', 'desc', 'R0', 'vida_med', 'nodo_esc', 'lect', 'div', 'p1', 'c1']
    mal_t = 0
    print()
    print(f"TESTIGOS (semilla {SEEDS[0]}, rep_acum=0): valor del TRONCO, con = si el gemelo da el mismo")
    print("   brazo      " + " ".join(f"{c:>10s}" for c in COLS))
    for nombre, a, b in testigos:
        fila = []
        for c in COLS:
            va, vb = T9(a, c), T9(b, c)
            mal_t += int(va != vb)
            fila.append((("= " if va == vb else "!=") + str(va))[:10].rjust(10))
        print(f"   {nombre:10s} " + " ".join(fila))
    print(f"   (= : tronco y gemelo dan el MISMO valor; discrepancias: {mal_t})")
    _cob = {k: v for k, v in cobertura.items()}
    print("   caminos forzados (tienen que ser > 0 para que el caso pruebe algo): " +
          ", ".join(f"{k}={v}" for k, v in _cob.items()))
    print()
    print("\nCONTROLES QUE DEBEN DIFERIR (si alguno sale IGUAL, el gemelo no distingue nada):")
    mal_ctl = 0
    for etiq, ka, da, kb, db in CONTROLES:
        malos = []
        for s in SEEDS:
            a = rapido.run(s + da, T=T, **ka)
            b = (rapido if 'tronco' not in etiq else lento).run(s + db, T=T, **kb)
            falta, dif, extra = compara(a, b)
            if not (falta or dif or extra): malos.append(s)
        estado = 'DIFIERE (bien)' if not malos else f'IGUAL en {malos} (MAL)'
        mal_ctl += len(malos)
        print(f"   {etiq:28s} -> {estado}")
    # cruce gemelo/tronco: el gemelo de REL no puede ser igual al tronco de REC
    cruce = compara(rapido.run(SEEDS[0], T=T, **CF.BRAZOS['REL']), lento.run(SEEDS[0], T=T, **CF.BRAZOS['REC']))
    ok_cruce = bool(cruce[0] or cruce[1] or cruce[2])
    mal_ctl += int(not ok_cruce)
    print(f"   {'gemelo REL != tronco REC':28s} -> {'DIFIERE (bien)' if ok_cruce else 'IGUAL (MAL)'}")

    print("\nGUARDIAS (el gemelo aborta donde aborta el original):")
    mal_g = 0
    for etiq, kw, exc in GUARDIAS:
        ra = rb = 'sin excepcion'
        try: lento.run(SEEDS[0], T=400, **kw)
        except BaseException as e: ra = type(e).__name__
        try: rapido.run(SEEDS[0], T=400, **kw)
        except BaseException as e: rb = type(e).__name__
        ok = (ra == rb == exc.__name__)
        mal_g += int(not ok)
        print(f"   {etiq:22s} tronco {ra:14s} gemelo {rb:14s} {'OK' if ok else 'MAL'}")
    print("FUERA DE ALCANCE (el gemelo avisa en vez de callar):")
    for etiq, kw in NO_COMPILA:
        rb = 'sin excepcion'
        try: rapido.run(SEEDS[0], T=400, **kw)
        except BaseException as e: rb = type(e).__name__
        ok = rb == 'ValueError'
        mal_g += int(not ok)
        print(f"   {etiq:22s} gemelo {rb:14s} {'OK' if ok else 'MAL'}")

    d1 = rapido.run(SEEDS[0], T=T, **CF.BRAZOS['REL'])
    d2 = rapido.run(SEEDS[0], T=T, **CF.BRAZOS['REL'])
    det = not any(compara(d1, d2))
    print(f"\nDETERMINISMO: dos llamadas iguales del gemelo -> {'MISMO dict (OK)' if det else 'DISTINTO (MAL)'}")

    if '--rapido' not in sys.argv:
        print("\nACELERACION a T=100000 (un proceso, sin Pool):")
        tot_l = tot_r = 0.0
        for b in ('NADA', 'REL', 'REL_AZAR'):
            t0 = time.time(); a = lento.run(1501, T=100000, **CF.BRAZOS[b]); tl = time.time() - t0
            t0 = time.time(); c = rapido.run(1501, T=100000, **CF.BRAZOS[b]); tr = time.time() - t0
            ok = not any(compara(a, c))
            tot_l += tl; tot_r += tr
            print(f"   {b:9s} tronco {tl:6.2f}s  gemelo {tr:6.3f}s  -> x{tl / tr:5.1f}   identidad a 100k: {'OK' if ok else 'FALLA'}")
            if not ok: fallos.append((b, 1501, *compara(a, c)))
        print(f"   TOTAL     tronco {tot_l:6.2f}s  gemelo {tot_r:6.3f}s  -> x{tot_l / tot_r:5.1f}")
        print(f"   una serie de 360 corridas de T=100000: tronco ~{tot_l / 3 * 360 / 60:.0f} min de CPU, "
              f"gemelo ~{tot_r / 3 * 360 / 60:.1f} min de CPU")

    print(f"\nVEREDICTO: identidad {n - len(fallos)}/{n} · controles que deben diferir "
          f"{len(CONTROLES) + 1 - mal_ctl}/{len(CONTROLES) + 1} · guardias "
          f"{len(GUARDIAS) + len(NO_COMPILA) - mal_g}/{len(GUARDIAS) + len(NO_COMPILA)} · testigos "
          f"{'todos iguales' if not mal_t else str(mal_t) + ' DISCREPAN'} · determinismo {'OK' if det else 'MAL'}")
    sys.exit(1 if (fallos or mal_ctl or mal_g or mal_t or not det) else 0)
