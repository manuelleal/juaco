"""corre_mixto.py — RAFAGA "uno va a lo menos visitado, ocho leen" (ficha 4 de investigacion_20261001/ENTREGA_2). 1-oct-2026.
HUMO DE EXPLORACION: no cuenta como resultado, no se declara nada, NO escribe en BITACORA.md.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

HIPOTESIS: la senal no sumo en JUNTOS porque los 9 exploraban; paga cuando explorar es de pocos.
QUE SE CORRE: corre_juntos.tarea tal cual (IMPORTADO por sha) con UNA sola diferencia: la lista de carros que recibe mundo_tramo_c.run
es mixta (CV.tarea arma [(ident, mod)] * 9; aqui se sustituye por la lista del brazo). Codigo de conducta nuevo: CERO. Memoria nueva: CERO.
  BRAZOS (9 linajes, mundo de la serie de juntos: oasis + mueve 20000 + c_e 0.01, T 100000):
    mix      linaje 0 = O1_TODO (memoria + senal + pregunta) · linajes 1-8 = O1_TODO_SEN (memoria + senal)           CANDIDATO
    mixbar   linaje 0 = O1_TODO · linajes 1-8 = O1_LUGAR_SENAL_BAR (leen la senal al ANTIPODA, b + 15 mod 30)         CONTROL (a)
    sen9     los 9 = O1_TODO_SEN                                                                                     CONTROL (b), mismo runner
    (arnes)  todo9 / preg9: 9 iguales, solo para la identidad contra corre_juntos.tarea
MEDIDA: latencia de los LECTORES (linajes 1-8) = pasos desde cada mudanza hasta su primer bocado A+C dentro del oasis nuevo
(d['_carrera']['oasis']['latencias'][1:], fisica de solo lectura de mundo_tramo_c; None = nunca -> cuenta T, como corre_c.fila_c).
PREDICCION (ficha): mix <= 700; mixbar >= 1200; sen9 1250-1400.
SEMILLAS NUEVAS: humo 738611-738612, arnes 738630 (grep 1-oct: 73861x / 73863x no aparecen en .py/.md).
  python experimentos/organelos/escalera/mixto/corre_mixto.py --identidad
  python experimentos/organelos/escalera/mixto/corre_mixto.py --humo [--n 2] [--T 100000] [--mueve 20000] [--brazos mix,mixbar,sen9]
"""
import argparse, json, os, statistics as st, sys, time

try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
ESC = os.path.dirname(AQUI)
sys.path.insert(0, ESC); sys.path.insert(0, os.path.join(ESC, 'juntos'))
import corre_juntos as RJ
CV = RJ.CV; P = RJ.P; MC = RJ.MC; R7 = RJ.R7; h16 = RJ.h16

SHAS = {os.path.join(ESC, 'juntos', 'corre_juntos.py'): 'db75135c8c2f3e0d', os.path.join(ESC, 'mundo_tramo_c.py'): '4a1044a4e0e1d5c9',
        os.path.join(ESC, 'juntos', 'carros', 'O1_TODO.py'): 'b7519a4a481a0cf5', os.path.join(ESC, 'juntos', 'carros', 'O1_TODO_SEN.py'): 'dff5e762bd23612e',
        os.path.join(ESC, 'juntos', 'carros', 'O1_TODO_PREG.py'): '382dafcf822b36a1', os.path.join(ESC, 'carros', 'O1_LUGAR_SENAL_BAR.py'): 'cab7460e91e215e3'}
EXPLORADOR = 0   # indice del linaje que pregunta en los brazos mixtos
BRAZOS = {'mix': ['O1_TODO'] + ['O1_TODO_SEN'] * 8, 'mixbar': ['O1_TODO'] + ['O1_LUGAR_SENAL_BAR'] * 8, 'sen9': ['O1_TODO_SEN'] * 9,
          'todo9': ['O1_TODO'] * 9, 'preg9': ['O1_TODO_PREG'] * 9}
HUMO = ('mix', 'mixbar', 'sen9')
SEM_HUMO = 738611; SEM_ARNES = 738630
MAX_CORRIDAS_1P = 6; MAX_PASOS_1P = 200000
DATOS = os.path.join(AQUI, 'datos')


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 1) if xs else None


def carga(nombre):
    """-> modulo del carro, cargado y verificado por el cargador de su duenno (corre_juntos.modulo o corre_p7.fija)."""
    if nombre == 'O1_LUGAR_SENAL_BAR':
        R7.fija('senbar'); return CV._MODS[nombre]
    return RJ.modulo(nombre)[0]


def tarea(seed, nombres, T, mundo):
    """corre_juntos.tarea(seed, nombres[0], T, mundo) con la lista de carros sustituida por la mixta. Con 9 nombres iguales ES corre_juntos.tarea."""
    carros = [(n, carga(n)) for n in nombres]
    orig = MC.run

    def run_mixto(s, _carros, **k):
        return orig(s, carros, **k)
    MC.run = run_mixto          # corre_juntos.tarea llama MC.run(*a, **k) dentro de su P.run parcheado
    try:
        x = RJ.tarea(seed, nombres[0], T, mundo)
    finally:
        MC.run = orig
    x['estado']['carros'] = list(nombres)
    return x


def fila(x, T, nombres):
    f = RJ.fila(x, T)
    L = x['linajes']; tel = x.get('tel') or []
    lat = [[(T if v is None else v) for v in ((l.get('_oasis') or {}).get('latencias') or [])[1:]] for l in L]
    nun = [sum(v is None for v in ((l.get('_oasis') or {}).get('latencias') or [])[1:]) for l in L]
    mixto = len(set(nombres)) > 1
    lec = [i for i in range(len(L)) if not (mixto and i == EXPLORADOR)]
    f['mixto'] = dict(carros=list(nombres), explorador=(EXPLORADOR if mixto else None), lat_por_linaje=lat, nunca_por_linaje=nun,
                      lat_lectores_med=med([v for i in lec for v in lat[i]]), lat_lectores_n=sum(len(lat[i]) for i in lec), nunca_lectores=sum(nun[i] for i in lec),
                      lat_lectores_por_mudanza=[med([lat[i][j] for i in lec]) for j in range(len(lat[0]))],
                      lat_explorador=(lat[EXPLORADOR] if mixto else None), lat_explorador_med=(med(lat[EXPLORADOR]) if mixto else None),
                      # llegadas de lectores ANTES que el explorador en la misma mudanza (si son muchas, la senal no es la via)
                      lectores_antes_que_explorador=(sum(lat[i][j] < lat[EXPLORADOR][j] for i in lec for j in range(len(lat[0]))) if mixto else None),
                      cruza_lectores=sum(f['cruza'][i] for i in lec), fund_lectores=med([f['fund'][i] for i in lec]),
                      sn=[(t.get('sn') or None) for t in tel], pg_exc=[((t.get('carro') or {}).get('pg_exc')) for t in tel],
                      escrituras=f['pizarra']['escrituras'], cobros=f['pizarra']['cobros'])
    return f


def verifica(log):
    ok = True
    for r, s in SHAS.items():
        h = h16(r); ok &= h == s; log(f"  sha {os.path.relpath(r, ESC)} {h} {'OK' if h == s else '!= ' + s + ' FALLA'}")
    return ok


def identidad(log, seed=SEM_ARNES, T=3000):
    """ARNES: la pista mixta con 9 carros IGUALES == corre_juntos.tarea homogenea, salida ENTERA (menos 'seg', reloj), misma semilla.
    Y la prueba de que el arnes puede fallar: mix != sen9 y mixbar != mix."""
    N = lambda x: json.loads(json.dumps({k: v for k, v in x.items() if k != 'seg'}, default=str, sort_keys=True))
    mundo = dict(RJ.MUNDO_J, mueve=T // 3); ok = True
    for b in ('sen9', 'todo9', 'preg9'):
        n = BRAZOS[b][0]
        a = N(tarea(seed, BRAZOS[b], T, mundo)); a['estado'].pop('carros')
        c = N(RJ.tarea(seed, n, T, mundo))
        i = a == c; ok &= i
        log(f"  IDENTIDAD mixto([{n}] * 9) == corre_juntos.tarea({n}) · salida ENTERA sin 'seg' · s {seed} T {T} mueve {T // 3}: {i} ({len(json.dumps(c))} bytes)")
    s9 = N(tarea(seed, BRAZOS['sen9'], T, mundo)); mx = N(tarea(seed, BRAZOS['mix'], T, mundo)); mb = N(tarea(seed, BRAZOS['mixbar'], T, mundo))
    for d in (s9, mx, mb): d['estado'].pop('carros')
    d1 = mx['linajes'] != s9['linajes']; d2 = mb['linajes'] != mx['linajes']; ok &= d1 and d2
    log(f"  EL ARNES PUEDE FALLAR: mix != sen9 {d1} · mixbar != mix {d2}")
    log(f"  ARNES {'OK' if ok else 'FALLA'}")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--humo', action='store_true'); g.add_argument('--identidad', action='store_true')
    ap.add_argument('--T', type=int, default=100000); ap.add_argument('--n', type=int, default=2); ap.add_argument('--mueve', type=int, default=RJ.MUEVE)
    ap.add_argument('--brazos', default=','.join(HUMO)); ap.add_argument('--desde', type=int, default=SEM_HUMO); ap.add_argument('--nota', default='')
    a = ap.parse_args(argv)
    BUF = []

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); BUF.append(s)
    log(f"CORRE_MIXTO · {'identidad' if a.identidad else 'humo'} · un proceso (sin Pool) · corre_mixto.py {h16(os.path.abspath(__file__))}")
    if not verifica(log): log("  SHA FALLA -> no se corre"); return 1
    if a.identidad: return 0 if identidad(log) else 1
    brazos = tuple(a.brazos.split(','))
    if len(brazos) * a.n > MAX_CORRIDAS_1P or a.T > MAX_PASOS_1P: raise SystemExit(f"un proceso: <= {MAX_CORRIDAS_1P} corridas y <= {MAX_PASOS_1P} pasos")
    if not identidad(log, T=1500): log("  ARNES FALLA -> no se corre"); return 1
    mundo = dict(RJ.MUNDO_J, mueve=a.mueve)
    carpeta = os.path.join(DATOS, f"humo_s{a.desde}-{a.desde + a.n - 1}_T{a.T}_m{a.mueve}_{time.strftime('%Y%m%d_%H%M%S')}"); os.makedirs(carpeta)
    log(f"  semillas {a.desde}-{a.desde + a.n - 1} · T {a.T} · brazos {list(brazos)} · mundo {mundo} · carpeta {carpeta} · nota {a.nota!r}")
    t0 = time.time(); R = {b: {} for b in brazos}; ab = []
    for i in range(a.n):
        for b in brazos:
            t1 = time.time()
            try:
                x = dict(tipo='prueba', i=i, brazo=b, aborto=None, **fila(tarea(a.desde + i, BRAZOS[b], a.T, mundo), a.T, BRAZOS[b]))
            except BaseException as e:   # noqa: nube-9
                x = dict(tipo='prueba', i=i, brazo=b, aborto=f"{type(e).__name__}: {e}"[:300]); ab.append(f"i{i} {b}: {x['aborto']}")
            x['seg'] = round(time.time() - t1, 1)
            fin = os.path.join(carpeta, f"prueba_i{i:02d}_{b}.json")
            with open(fin + '.tmp', 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False)
            os.replace(fin + '.tmp', fin)
            if x['aborto']: log(f"  i{i} {b} ABORTO {x['aborto']}"); continue
            R[b][i] = x; m = x['mixto']; sn = x.get('senal') or {}
            log(f"  [{time.time()-t0:6.1f}s] i{i} s{a.desde + i} {b:6s} ({x['seg']}s) LECTORES lat med {m['lat_lectores_med']} (n {m['lat_lectores_n']}, nunca {m['nunca_lectores']}) "
                f"por mudanza {m['lat_lectores_por_mudanza']} · explorador {m['lat_explorador']} · lectores antes que el explorador {m['lectores_antes_que_explorador']} · "
                f"cruzan {x['cruzan']}/9 (lectores {m['cruza_lectores']}) fund lectores {m['fund_lectores']} · lee {sn.get('sn_lee')} siembra {sn.get('sn_siembra')} "
                f"escribe {m['escrituras']} · pg_exc {m['pg_exc']} · mundo AC {x.get('mundo_AC')}")
    res = {b: dict(lat_lectores_por_semilla=[R[b][i]['mixto']['lat_lectores_med'] for i in sorted(R[b])],
                   lat_lectores_todas=med([v for i in R[b] for j, l in enumerate(R[b][i]['mixto']['lat_por_linaje'])
                                           if not (R[b][i]['mixto']['explorador'] == j) for v in l]),
                   nunca=sum(R[b][i]['mixto']['nunca_lectores'] for i in R[b]), cruza_lectores=sum(R[b][i]['mixto']['cruza_lectores'] for i in R[b]),
                   lat_explorador_med=[R[b][i]['mixto']['lat_explorador_med'] for i in sorted(R[b])]) for b in brazos}
    log("\n  ================ RESUMEN (HUMO DE EXPLORACION: no cuenta, no se declara)")
    for b in brazos: log(f"  {b:6s} {res[b]}")
    rj = os.path.join(carpeta, 'resumen.json')
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(modo='humo', n=a.n, T=a.T, mundo=mundo, semillas=[a.desde, a.desde + a.n - 1], brazos={b: BRAZOS[b] for b in brazos}, resumen=res, abortos=ab,
                       nota=a.nota, sha_runner=h16(os.path.abspath(__file__)), shas={os.path.relpath(k, ESC): v for k, v in SHAS.items()}, seg=round(time.time() - t0, 1)),
                  fh, ensure_ascii=False, indent=1)
    with open(os.path.join(carpeta, 'log.txt'), 'w', encoding='utf-8') as fh: fh.write('\n'.join(BUF) + '\n')
    log(f"  RESUMEN {rj} · abortos {len(ab)} · {time.time()-t0:.1f}s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
