"""Arnes de identidad de organismo_vivo_rep (propósito y reproducción, peldano minimo del mundo vivo). Regla 2 de
registro/EQUIPO.md: un instrumento construido por anclas debe ser su origen BIT A BIT con las perillas apagadas, y el
arnes se corre y se entrega con el trabajo.

Origen: experimentos/nivel11_mundo_vivo/organismo_vivo.py (20c0961c79de8825). Exigencias, en orden:

  APAGADA (reproduccion=0; es el valor por defecto): organismo_vivo_rep == organismo_vivo en TODAS las claves y con el
      MISMO conjunto de claves, en >= 10 escenarios x 2 semillas. Incluye el escenario en que TODAS las perillas rep_*
      estan encendidas pero la maestra apagada (deben ser inertes), y los seis brazos del bloque anterior.
  CADENA: organismo_vivo_rep(vivo=0, n_nec=1) == organismo/organismo_v14.py (el tronco), clave por clave: la cadena de
      origen entera (v14.1 -> organismo_vivo -> organismo_vivo_rep) se comprueba de una vez.
  RNG: ninguna linea nueva llama al rng (lo verifica el constructor); ademas todas las claves que dependen del flujo del
      rng (split_t, deaths, mord, vis, sobre, llegadas) salen identicas, apagada Y con la medida encendida (caso C):
      el rng no se consume con la perilla apagada ni con la medida de solo lectura.
  ENCENDIDA, solo lectura (C): reproduccion=1 con rep_coste=0 y sin tercera necesidad -> las claves viejas salen bit a
      bit; solo aparecen las 7 claves nuevas.
  CONTROLES QUE DEBEN FALLAR (D, E): la tercera necesidad (n_nec=3, rep_nec=1) y el control CUELLO (rep_cuello=1) NO son
      organismo_vivo. Sin estos casos el arnes pasaria por vacuidad.
  (E2) CUELLO_MIN (rep_cuello=2; ERR-38 provisional, anadido tras el humo y antes del bloque) tampoco es organismo_vivo.
  (F) informativo: con rep_coste=0.4 el organismo difiere de organismo_vivo si y solo si produjo >= 1 descendiente en T.
  ENTRE CONSTRUCCIONES (H): la construccion final (con CUELLO_MIN) es BIT A BIT la construccion v1 (ed31d9b989b93307, la
      del humo de registro vivo_rep_humo_20260918_090014) en los brazos que el humo corrio (VIVO, REP_SIN_COSTE, REP,
      CUELLO): asi el humo sigue valiendo para el instrumento final sin repetirlo. La copia v1 se lee de la carpeta
      temporal del disenador; si no esta, el caso se salta y se dice.

Un proceso, sin Pool (regla 3). T = 20000. OJO (ERR-28): organismo/ va primero en sys.path.
Uso:  python experimentos/nivel11_mundo_vivo/identidad_vivo_rep.py [--v1 ruta/a/organismo_vivo_rep_v1.py]
"""
import hashlib, importlib.util, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_vivo as VV
import organismo_vivo_rep as VR
import mini_vivo as MV

T = 20000
SEM = (1, 2)
NUEVAS_REP = {'descendientes', 'pasos_viables', 'desc_q', 't_desc', 'sac_mord', 'sac_dec', 'rep'}
RNG_DEP = ('split_t', 'deaths', 'mord', 'vis', 'sobre', 'llegadas', 'sin_objetivo', 'W', 'comp')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def sin_rep(d):
    return {k: v for k, v in d.items() if k not in NUEVAS_REP}


def compara(a, b, quitar=()):
    """Claves de a que faltan en b o difieren (b sin las claves `quitar`)."""
    bb = {k: v for k, v in b.items() if k not in quitar}
    falta = [k for k in a if k not in bb]
    dif = [k for k in a if k in bb and N(a[k]) != N(bb[k])]
    extra = [k for k in bb if k not in a]
    return falta, dif, extra


def caso(etiq, f_a, f_b, t0, debe_diferir=False, quitar=(), extra_esperado=None):
    ok, det = 0, ''
    for s in SEM:
        a, b = f_a(s), f_b(s)
        falta, dif, extra = compara(a, b, quitar)
        igual = not falta and not dif and (extra_esperado is None or set(extra) == extra_esperado) and (extra_esperado is not None or not extra)
        ok += int(igual != debe_diferir)
        if (falta or dif or (extra and extra_esperado is None)) and not det:
            det = f"  falta {falta[:3]} dif {dif[:4]} extra {extra[:3]}"
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    print(f"  [{time.time()-t0:6.1f}s] {etiq:60s} {ok}/{len(SEM)} {marca if ok == len(SEM) else 'FALLA' + det}", flush=True)
    return ok, len(SEM)


if __name__ == '__main__':
    t0 = time.time()
    for nom, p in [('organismo_v14 (TRONCO congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
                   ('organismo_vivo.py (origen)', os.path.join(AQUI, 'organismo_vivo.py')),
                   ('construye_vivo_rep.py', os.path.join(AQUI, 'construye_vivo_rep.py')),
                   ('organismo_vivo_rep.py', os.path.join(AQUI, 'organismo_vivo_rep.py'))]:
        print(f"  sha {nom:36s} {h16(p)}")
    print(f"  T = {T}, semillas {SEM}, UN proceso\n")
    ok = tot = 0
    B = MV.BRAZOS
    V14A = dict(vivo=1, n_nec=1, estims=('A', 'B'), costo_a=0.0, A_ini=1.0)

    print("APAGADA (reproduccion=0): organismo_vivo_rep == organismo_vivo, mismas claves")
    escenarios = [
        ('(A1) VIVO', B['VIVO'], dict()),
        ('(A2) UNA_NEC', B['UNA_NEC'], dict()),
        ('(A3) ESCALAR', B['ESCALAR'], dict()),
        ('(A4) BARAJA_POL (rng propio del control)', B['BARAJA_POL'], dict()),
        ('(A5) BARAJA_CON', B['BARAJA_CON'], dict()),
        ('(A6) NO_INFORMA (sal muda)', B['NO_INFORMA'], dict()),
        ('(A7) ancla V14 (1 necesidad, 2 estimulos)', V14A, dict()),
        ('(A8) vivo=0 base', dict(vivo=0, n_nec=1), dict()),
        ('(A9) vivo=0 con inversion en 10k', dict(vivo=0, n_nec=1, invertir_en=10000), dict()),
        ('(A10) VIVO + predictor vectorial (eta_pred=0.05)', dict(B['VIVO'], eta_pred=0.05), dict()),
        ('(A11) VIVO con TODAS las rep_* encendidas y la maestra apagada', B['VIVO'],
         dict(reproduccion=0, rep_mide=1, rep_coste=0.4, rep_cuello=1, rep_X=10, rep_umbral=0.9)),
        ('(A12) vivo=0 linaje v13 (mask_rel=0, puerta_pat=0)', dict(vivo=0, n_nec=1, mask_rel=0, puerta_pat=0), dict()),
        ('(A13) VIVO sin puerta (puerta=None)', dict(B['VIVO'], puerta=None), dict()),
    ]
    for etiq, kw, extra in escenarios:
        a, b = caso(etiq, lambda s, kw=kw: VV.run(s, T=T, **kw), lambda s, kw=kw, extra=extra: VR.run(s, T=T, **kw, **extra), t0)
        ok += a; tot += b

    print("\nCADENA AL TRONCO: organismo_vivo_rep(vivo=0, n_nec=1) == organismo_v14 (clave por clave)")
    a, b = caso('(B1) rep(vivo=0) == organismo_v14', lambda s: V14.run(s, T=T), lambda s: VR.run(s, T=T, vivo=0, n_nec=1), t0)
    ok += a; tot += b
    a, b = caso('(B2) lo mismo con inversion en 10k', lambda s: V14.run(s, T=T, invertir_en=10000),
                lambda s: VR.run(s, T=T, vivo=0, n_nec=1, invertir_en=10000), t0)
    ok += a; tot += b

    print("\nENCENDIDA, SOLO LECTURA (reproduccion=1, rep_coste=0, sin tercera necesidad): claves viejas bit a bit + 7 nuevas")
    MED = dict(reproduccion=1, rep_mide=1, rep_X=500, rep_umbral=1.0, rep_coste=0.0)
    for etiq, kw in [('(C1) VIVO + medida', B['VIVO']), ('(C2) UNA_NEC + medida', B['UNA_NEC']),
                     ('(C3) ancla V14 + medida', V14A), ('(C4) BARAJA_POL + medida', B['BARAJA_POL'])]:
        a, b = caso(etiq, lambda s, kw=kw: VV.run(s, T=T, **kw), lambda s, kw=kw: VR.run(s, T=T, **kw, **MED), t0,
                    extra_esperado=NUEVAS_REP)
        ok += a; tot += b
    # rng: las claves que dependen del flujo del rng son identicas con la medida encendida (ya cubierto por C1-C4; se imprime)
    a1 = VV.run(1, T=T, **B['VIVO']); b1 = VR.run(1, T=T, **B['VIVO'], **MED)
    print(f"        claves dependientes del rng identicas con la medida encendida: "
          f"{sum(N(a1[k]) == N(b1[k]) for k in RNG_DEP)}/{len(RNG_DEP)}   descendientes(s1,T={T}) = {b1['descendientes']}, "
          f"pasos_viables = {b1['pasos_viables']}")

    print("\nCONTROLES QUE DEBEN FALLAR (si no, el arnes pasaria por vacuidad)")
    REP0 = dict(MV.CUERPO, n_nec=3, rep_nec=1, **MED)
    CUE = dict(MV.CUERPO, n_nec=2, rep_cuello=1, **MED)
    a, b = caso('(D) tercera necesidad (n_nec=3, rep_nec=1) != organismo_vivo VIVO',
                lambda s: VV.run(s, T=T, **B['VIVO']), lambda s: VR.run(s, T=T, **REP0), t0, debe_diferir=True,
                quitar=NUEVAS_REP)
    ok += a; tot += b
    a, b = caso('(E) control CUELLO (rep_cuello=1) != organismo_vivo VIVO',
                lambda s: VV.run(s, T=T, **B['VIVO']), lambda s: VR.run(s, T=T, **CUE), t0, debe_diferir=True,
                quitar=NUEVAS_REP)
    ok += a; tot += b
    CUE2 = dict(MV.CUERPO, n_nec=2, rep_cuello=2, **MED)
    a, b = caso('(E2) control CUELLO_MIN (rep_cuello=2) != organismo_vivo VIVO',
                lambda s: VV.run(s, T=T, **B['VIVO']), lambda s: VR.run(s, T=T, **CUE2), t0, debe_diferir=True,
                quitar=NUEVAS_REP)
    ok += a; tot += b
    for s in SEM:   # comprobacion del instrumento (no es humo): que CUELLO_MIN hace lo que dice, saciado
        r = VR.run(s, T=T, **CUE2)
        sac = {k: (round(r['sac_mord'][k] / r['sac_dec'][k], 3) if r['sac_dec'][k] >= 20 else None) for k in 'ABCD'}
        print(f"        CUELLO_MIN s{s} T={T}: descendientes {r['descendientes']}, viable {r['pasos_viables']/T:.3f}, muertes {r['deaths']} "
              f"{r['muertes_nec']}, tasa saciado A/B/C/D {sac}")

    print("\nENTRE CONSTRUCCIONES (H): la construccion final == la v1 del humo en los brazos que el humo corrio")
    v1p = (sys.argv[sys.argv.index('--v1') + 1] if '--v1' in sys.argv else
           os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Temp', 'claude',
                        'C--Users-User-Documents-ASIGNACION-SENA-CHRISTIAM-2026-FICHAS-PYTHON-JSON',
                        '0cc0e618-5704-4b6c-aed1-86ef90822ef1', 'scratchpad', 'organismo_vivo_rep_v1.py'))
    if os.path.exists(v1p):
        print(f"        v1: {v1p}  sha {h16(v1p)}")
        spec = importlib.util.spec_from_file_location('organismo_vivo_rep_v1', v1p)
        V1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(V1)
        REPC = dict(dict(MV.CUERPO, n_nec=3, rep_nec=1, **MED), rep_coste=0.4)
        for etiq, kw in [('(H1) VIVO + medida', dict(B['VIVO'], **MED)), ('(H2) REP_SIN_COSTE', REP0), ('(H3) REP (coste 0.4)', REPC),
                         ('(H4) CUELLO (rep_cuello=1)', CUE)]:
            a, b = caso(etiq, lambda s, kw=kw: V1.run(s, T=T, **kw), lambda s, kw=kw: VR.run(s, T=T, **kw), t0)
            ok += a; tot += b
    else:
        print("        (copia v1 no encontrada: caso H saltado; el humo de registro se hizo con ed31d9b989b93307)")

    print("\n(F) informativo: con rep_coste=0.4 difiere de organismo_vivo si y solo si hubo >= 1 descendiente en T")
    for s in SEM:
        a = VV.run(s, T=T, **B['VIVO']); b = VR.run(s, T=T, **dict(dict(B['VIVO'], **MED), rep_coste=0.4))
        falta, dif, extra = compara(a, b, NUEVAS_REP)
        print(f"        semilla {s}: descendientes {b['descendientes']}, difiere {bool(dif)}  -> "
              f"{'coherente' if bool(dif) == (b['descendientes'] > 0) else '*** INCOHERENTE'}")

    print(f"\nIDENTIDAD {ok}/{tot}" + ("  -> el paquete puede correr." if ok == tot else
                                       "  -> NO se corre nada hasta que sea 100%."))
    sys.exit(0 if ok == tot else 1)
