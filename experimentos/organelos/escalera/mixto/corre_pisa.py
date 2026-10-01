"""corre_pisa.py — RAFAGA 2 de mixto (no cuenta, no se declara, no escribe en BITACORA): la variante O1_SEN_PISA (lo oido pisa lo vivido que
ya no vale; construye_pisa.py) como LECTOR en la pista mixta. 1-oct-2026. Reutiliza corre_mixto (tarea / fila / verifica) por import.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con controles y replicas).

  BRAZOS (mundo de la serie de juntos: oasis + mueve 20000 + c_e 0.01, T 100000):
    pmix     linaje 0 = O1_TODO (explorador, carro ORIGINAL) · 1-8 = O1_SEN_PISA                       CANDIDATO
    pmixbar  linaje 0 = O1_TODO · 1-8 = O1_SEN_PISA_BAR (leen al antipoda, tambien pisan)              CONTROL de contenido (puede ganar)
    sen9     los 9 = O1_TODO_SEN original                                                              BASE, mismo runner
    pmudo    linaje 0 = O1_TODO_PREG (explora, NO emite ni lee) · 1-8 = O1_SEN_PISA                     CONTROL: hay explorador pero mudo
  P7 (--p7): mundo SIN mudanza (mueve 0, c_e 0.01 = el mundo de P7): pisa9 (9 x O1_SEN_PISA) vs sen9 (9 x O1_TODO_SEN == O1_LUGAR_SENAL).
SEMILLAS NUEVAS: humo 738621-738622 · p7 738623 · arnes 738631.
  python experimentos/organelos/escalera/mixto/corre_pisa.py --identidad
  python experimentos/organelos/escalera/mixto/corre_pisa.py --humo [--brazos pmix,pmixbar,sen9] [--n 2]
  python experimentos/organelos/escalera/mixto/corre_pisa.py --p7 [--T 100000]
"""
import argparse, importlib.util, json, os, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_mixto as CM
import construye_pisa as CP
RJ = CM.RJ; CV = CM.CV; h16 = CM.h16; med = CM.med
SHA_MIXTO = 'f27edde098cf7a1a'
PROPIOS = {n: os.path.join(AQUI, 'carros', n + '.py') for n, _, _ in CP.VARIANTES}
BRAZOS = {'pmix': ['O1_TODO'] + ['O1_SEN_PISA'] * 8, 'pmixbar': ['O1_TODO'] + ['O1_SEN_PISA_BAR'] * 8, 'sen9': ['O1_TODO_SEN'] * 9,
          'pmudo': ['O1_TODO_PREG'] + ['O1_SEN_PISA'] * 8, 'pisa9': ['O1_SEN_PISA'] * 9, 'pisa0': ['O1_SEN_PISA0'] * 9}
SEM_HUMO = 738621; SEM_P7 = 738623; SEM_ARNES = 738631
_carga0 = CM.carga


def carga(nombre):
    if nombre not in PROPIOS: return _carga0(nombre)
    ruta = PROPIOS[nombre]
    if open(ruta, 'rb').read() != CP.todas()[nombre]: raise SystemExit(f"{ruta} != construye_pisa (correr construye_pisa.py)")
    m = CV._MODS.get(nombre)
    if m is None or os.path.abspath(m.__file__) != os.path.abspath(ruta):
        spec = importlib.util.spec_from_file_location(f"carro_{nombre}", ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[nombre] = m
    return m


def tarea(seed, nombres, T, mundo):
    """corre_mixto.tarea con el cargador de esta carpeta. Si el linaje 0 es un carro propio, corre_juntos.tarea recibe 'O1_TODO_SEN' solo como
    identificador de estado (la lista de carros que corre es SIEMPRE la de `nombres`; x['estado']['carros'] la deja escrita)."""
    CM.carga = carga
    try:
        if nombres[0] in PROPIOS:
            orig = RJ.tarea
            RJ.tarea = lambda s, n, T_, m_: orig(s, 'O1_TODO_SEN', T_, m_)
            try: x = CM.tarea(seed, nombres, T, mundo)
            finally: RJ.tarea = orig
        else:
            x = CM.tarea(seed, nombres, T, mundo)
    finally:
        CM.carga = _carga0
    x['estado']['carro'] = nombres[0]; x['estado']['carros_sha'] = {n: h16(PROPIOS[n]) for n in set(nombres) if n in PROPIOS}
    return x


def fila(x, T, nombres):
    f = CM.fila(x, T, nombres)
    f['mixto']['sn_pisa'] = [((t.get('sn') or {}).get('sn_pisa')) for t in (x.get('tel') or [])]
    return f


def verifica(log):
    ok = CM.verifica(log)
    s = h16(CM.__file__); ok &= s == SHA_MIXTO; log(f"  sha corre_mixto.py {s} {'OK' if s == SHA_MIXTO else 'FALLA'}")
    for n, b in CP.todas().items():
        i = os.path.exists(PROPIOS[n]) and open(PROPIOS[n], 'rb').read() == b; ok &= i; log(f"  carro {n} == construye_pisa: {i} (sha {CP.h16b(b)})")
    return ok


def identidad(log, seed=SEM_ARNES, T=3000):
    """variante APAGADA (O1_SEN_PISA0 x 9) == corre_juntos.tarea('O1_TODO_SEN'), salida ENTERA menos reloj y estado (nombre/sha del carro);
    con mudanza y sin mudanza. Y que puede fallar: pisa9 != sen9."""
    def N(x):
        x = {k: v for k, v in x.items() if k not in ('seg', 'estado')}
        return json.loads(json.dumps(x, default=str, sort_keys=True).replace('O1_SEN_PISA0', 'O1_TODO_SEN'))
    ok = True
    for mv in (T // 3, 0):
        mundo = dict(RJ.MUNDO_J, mueve=mv)
        a = N(tarea(seed, BRAZOS['pisa0'], T, mundo)); c = N(RJ.tarea(seed, 'O1_TODO_SEN', T, mundo)); i = a == c; ok &= i
        log(f"  IDENTIDAD [O1_SEN_PISA0] * 9 == corre_juntos.tarea(O1_TODO_SEN) · salida ENTERA sin 'seg'/'estado' · s {seed} T {T} mueve {mv}: {i} ({len(json.dumps(c))} bytes)")
        if mv:
            p = N(tarea(seed, BRAZOS['pisa9'], T, mundo)); d = p['linajes'] != c['linajes']; ok &= d
            log(f"  EL ARNES PUEDE FALLAR: pisa9 != sen9 {d}")
    log(f"  ARNES {'OK' if ok else 'FALLA'}")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--identidad', action='store_true'); g.add_argument('--p7', action='store_true')
    ap.add_argument('--T', type=int, default=100000); ap.add_argument('--n', type=int, default=None); ap.add_argument('--brazos', default=None)
    ap.add_argument('--desde', type=int, default=None); ap.add_argument('--nota', default='')
    a = ap.parse_args(argv)
    BUF = []

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); BUF.append(s)
    modo = 'identidad' if a.identidad else ('p7' if a.p7 else 'humo')
    log(f"CORRE_PISA · {modo} · un proceso (sin Pool) · corre_pisa.py {h16(os.path.abspath(__file__))}")
    if not verifica(log): log("  SHA FALLA -> no se corre"); return 1
    if a.identidad: return 0 if identidad(log) else 1
    if a.p7: brazos = ('pisa9', 'sen9'); n = a.n or 1; base = a.desde or SEM_P7; mv = 0
    else: brazos = tuple((a.brazos or 'pmix,pmixbar,sen9').split(',')); n = a.n or 2; base = a.desde or SEM_HUMO; mv = RJ.MUEVE
    if len(brazos) * n > CM.MAX_CORRIDAS_1P or a.T > CM.MAX_PASOS_1P: raise SystemExit("un proceso: <= 6 corridas y <= 200000 pasos")
    if not identidad(log, T=1500): log("  ARNES FALLA -> no se corre"); return 1
    mundo = dict(RJ.MUNDO_J, mueve=mv)
    carpeta = os.path.join(CM.DATOS, f"pisa_{modo}_s{base}-{base + n - 1}_T{a.T}_m{mv}_{time.strftime('%Y%m%d_%H%M%S')}"); os.makedirs(carpeta)
    log(f"  semillas {base}-{base + n - 1} · T {a.T} · brazos {list(brazos)} · mundo {mundo} · carpeta {carpeta} · nota {a.nota!r}")
    t0 = time.time(); R = {b: {} for b in brazos}; ab = []
    for i in range(n):
        for b in brazos:
            t1 = time.time()
            try:
                x = dict(tipo='prueba', i=i, brazo=b, aborto=None, **fila(tarea(base + i, BRAZOS[b], a.T, mundo), a.T, BRAZOS[b]))
            except BaseException as e:   # noqa: nube-9
                x = dict(tipo='prueba', i=i, brazo=b, aborto=f"{type(e).__name__}: {e}"[:300]); ab.append(f"i{i} {b}: {x['aborto']}")
            x['seg'] = round(time.time() - t1, 1)
            fin = os.path.join(carpeta, f"prueba_i{i:02d}_{b}.json")
            with open(fin + '.tmp', 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
            os.replace(fin + '.tmp', fin)
            if x['aborto']: log(f"  i{i} {b} ABORTO {x['aborto']}"); continue
            R[b][i] = x; m = x['mixto']; sn = x.get('senal') or {}; lv = x.get('latencia_vida') or {}
            log(f"  [{time.time()-t0:6.1f}s] i{i} s{base + i} {b:7s} ({x['seg']}s) LECTORES lat med {m['lat_lectores_med']} (n {m['lat_lectores_n']}, nunca {m['nunca_lectores']}) "
                f"por mudanza {m['lat_lectores_por_mudanza']} · explorador {m['lat_explorador']} · antes que el explorador {m['lectores_antes_que_explorador']} · "
                f"cruzan {x['cruzan']}/9 (lectores {m['cruza_lectores']}) R0 {x['R0_med']} fund {x['fund']} · lat por vida {lv.get('med')} (frac {lv.get('frac_vidas')}) · "
                f"lee {sn.get('sn_lee')} siembra {sn.get('sn_siembra')} pisa {m['sn_pisa']} escribe {sum(z or 0 for z in m['escrituras'])} · ratio oasis {(x.get('oasis') or {}).get('ratio_pasos')} · mundo AC {x.get('mundo_AC')}")
    res = {b: dict(lat_lectores_por_semilla=[R[b][i]['mixto']['lat_lectores_med'] for i in sorted(R[b])],
                   lat_lectores_todas=med([v for i in R[b] for j, l in enumerate(R[b][i]['mixto']['lat_por_linaje']) if not (R[b][i]['mixto']['explorador'] == j) for v in l]),
                   nunca=sum(R[b][i]['mixto']['nunca_lectores'] for i in R[b]), cruza_lectores=[R[b][i]['mixto']['cruza_lectores'] for i in sorted(R[b])],
                   cruzan=[R[b][i]['cruzan'] for i in sorted(R[b])], R0_med=[R[b][i]['R0_med'] for i in sorted(R[b])],
                   lat_vida=[(R[b][i].get('latencia_vida') or {}).get('med') for i in sorted(R[b])],
                   lat_explorador_med=[R[b][i]['mixto']['lat_explorador_med'] for i in sorted(R[b])], mundo_AC=[R[b][i]['mundo_AC'] for i in sorted(R[b])]) for b in brazos}
    log("\n  ================ RESUMEN (RAFAGA: no cuenta, no se declara)")
    for b in brazos: log(f"  {b:7s} {res[b]}")
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo=modo, n=n, T=a.T, mundo=mundo, semillas=[base, base + n - 1], brazos={b: BRAZOS[b] for b in brazos}, resumen=res, abortos=ab, nota=a.nota,
                       sha_runner=h16(os.path.abspath(__file__)), sha_mixto=h16(CM.__file__), carros={k: h16(v) for k, v in PROPIOS.items()}, seg=round(time.time() - t0, 1)),
                  fh, ensure_ascii=False, indent=1)
    with open(os.path.join(carpeta, 'log.txt'), 'w', encoding='utf-8') as fh: fh.write('\n'.join(BUF) + '\n')
    log(f"  RESUMEN {rj} · abortos {len(ab)} · {time.time()-t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
