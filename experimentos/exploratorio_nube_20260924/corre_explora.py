"""corre_explora.py — EXPLORATORIO, no es dato (nube, 24-sep-2026). Corredor de UN proceso para los prototipos de la noche.

Pista: la de la carrera del 22-sep sin tocar (experimentos/carrera_escuderias/pista.py), monocultivo de 9 carros iguales,
escala=1 (L 360, 36 objetos), pizarra=1, rep_acum=0, fundador_limpio=1: la MISMA entrada que juez.tarea y corre_v143.tarea.
Medidas sólo desde la física (juez.resumen_linaje, ERR-96). Semillas EXPLORATORIAS 24001-24099 (no usadas por ningún paquete;
grep del 24-sep): no deben reutilizarse en series confirmatorias.

Uso:
  python experimentos/exploratorio_nube_20260924/corre_explora.py --identidad
  python experimentos/exploratorio_nube_20260924/corre_explora.py --brazos FAB,NEO5,LIM,NEO5_LIM,O1 --desde 24001 --n 8 --T 30000
Escribe datos/<etiqueta>.log desde el arranque (regla 10) y datos/<etiqueta>.json tras CADA corrida.
"""
import argparse, hashlib, json, os, statistics as st, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'carrera_escuderias'))
import pista as P
import juez as J
import carros_reserva as CR

DATOS = os.path.join(AQUI, 'datos')
SEMILLAS_OK = range(24001, 24100)


def _brazos():
    b = {
        'FAB': (lambda: P.carga_carro('FABRICA'), 'FABRICA de la carrera (bicho real, piso)'),
        'O1': (lambda: P.carga_carro('O1'), 'O1 (política escrita a mano por un LLM; techo de la pista)'),
        'APR': (lambda: P.carga_carro('APR'), 'APR de la carrera (FABRICA + boca aprendida por TD y heredada; aprende_barrer)'),
        'W0': (lambda: CR.modulo('W0'), 'subclase sin reglas (debe ser FABRICA bit a bit)'),
        'NEO5': (lambda: CR.modulo('NEO5', neo=0.5), 'neofobia: no prueba lo desconocido si min(E,Ag) < 0.5'),
        'NEO3': (lambda: CR.modulo('NEO3', neo=0.3), 'neofobia con umbral 0.3'),
        'NEO8': (lambda: CR.modulo('NEO8', neo=0.8), 'neofobia con umbral 0.8'),
        'NEOINF': (lambda: CR.modulo('NEOINF', neo=9.9), 'neofobia SIEMPRE (control: no depende de la reserva)'),
        'LIM': (lambda: CR.modulo('LIM', lim=1.4), 'limpia lo malo si min(E,Ag) >= 1.4'),
        'NEO5_LIM': (lambda: CR.modulo('NEO5_LIM', neo=0.5, lim=1.4), 'neofobia 0.5 + limpieza 1.4'),
    }
    for extra in ('carros_extra', 'carros_predice', 'carros_ver', 'carros_apr_reserva', 'carros_limpia', 'carros_v143_reserva', 'carros_v143_familia', 'carros_v143_evo'):
        if os.path.exists(os.path.join(AQUI, extra + '.py')):
            mod = __import__(extra)
            b.update(mod.BRAZOS)
    return b


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def med(xs):
    xs = [x for x in xs if x is not None]
    return round(float(st.median(xs)), 4) if xs else None


def corre(seed, nombre, fabrica, T):
    CR.TOT.clear()
    t0 = time.time()
    mod = fabrica()
    r = P.run(seed, [(nombre, mod)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1)
    L = [J.resumen_linaje(d, seed) for d in r['linajes']]
    cz = {k: sum(l['causas'][k] for l in L) for k in ('hambre', 'sed', 'veneno', 'sal')}
    dg = [l['diag'] for l in L if l.get('diag')]
    return dict(seed=seed, brazo=nombre, T=T, seg=round(time.time() - t0, 1),
                R0_real_med=med([l['R0_real'] for l in L]), R0_real=[l['R0_real'] for l in L],
                persisten=sum(l['persiste'] for l in L), cruzan_real=sum(l['cruza_real'] for l in L),
                vida_med=med([l['vida_med'] for l in L]), muertes_med=med([l['muertes'] for l in L]),
                fundadores_med=med([l['fundadores'] for l in L]), nac_reales_med=med([l['nac_reales'] for l in L]),
                causas=cz, mord_BD=med([l['mord']['B'] + l['mord']['D'] for l in L]),
                mord_AC=med([l['mord']['A'] + l['mord']['C'] for l in L]),
                frac_sin_bueno_mundo=r['pista'].get('frac_sin_bueno_mundo'),
                limpiezas_por_cuerpo=med([x.get('limpiezas_por_cuerpo') for x in dg]),
                muere_sin_parir=med([l['frac_muere_sin_parir'] for l in L]),
                coherente=sum(l['coherente'] for l in L), tot=dict(CR.TOT))


def identidad(log):
    """Subclases sin reglas (W0, W2, WP) == FABRICA y RESP == RES en toda la fisica de los 9 linajes y la pista (T 3000)."""
    B = _brazos(); ok = True

    def fis(r):
        return json.dumps([{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']], sort_keys=True, default=str), r['pista']
    pares = [('W0', 'FAB'), ('W2', 'FAB'), ('WP', 'FAB'), ('WV', 'FAB'), ('WA', 'APR'), ('WL', 'FAB'), ('RESP', 'RES'), ('WV143', 'V143'), ('WF143', 'V143'), ('WE143', 'V143'), ('WEFAB', 'FAB')]
    for s in (24098, 24099):
        for x, y in pares:
            if x not in B or y not in B: continue
            a = P.run(s, [(y, B[y][0]())] * 9, T=3000, fundador_limpio=1)
            b = P.run(s, [(y, B[x][0]())] * 9, T=3000, fundador_limpio=1)
            igual = fis(a) == fis(b)
            ok &= igual
            log(f"  identidad s{s}: {x} == {y} en la fisica de los 9 linajes y la pista: {igual}")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--brazos', default='')
    ap.add_argument('--desde', type=int, default=24001)
    ap.add_argument('--n', type=int, default=4)
    ap.add_argument('--T', type=int, default=30000)
    ap.add_argument('--identidad', action='store_true')
    ap.add_argument('--tag', default='')
    a = ap.parse_args(argv)
    os.makedirs(DATOS, exist_ok=True)
    sello = time.strftime('%Y%m%d_%H%M%S')
    et = 'identidad' if a.identidad else f"explora_{a.tag + '_' if a.tag else ''}{a.brazos.replace(',', '-')}_s{a.desde}-{a.desde + a.n - 1}_T{a.T}"
    base = os.path.join(DATOS, f"{et}_{sello}")
    flog = open(base + '.log', 'w', encoding='utf-8')

    def log(s=''):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    shas = ' · '.join(f"{f} {h16(os.path.join(AQUI, f))}" for f in sorted(os.listdir(AQUI)) if f.startswith('carros_') and f.endswith('.py'))
    log(f"EXPLORATORIO — no es dato · {et} · python {sys.version.split()[0]} · corre_explora.py {h16(os.path.abspath(__file__))} · "
        f"{shas} · pista.py {h16(P.__file__)} · juez.py {h16(J.__file__)}")
    if a.identidad:
        ok = identidad(log); log(f"IDENTIDAD: {'OK' if ok else 'FALLA'}"); flog.close(); sys.exit(0 if ok else 1)
    B = _brazos()
    brazos = [x for x in a.brazos.split(',') if x]
    for x in brazos:
        if x not in B: raise SystemExit(f"brazo desconocido {x}; hay {sorted(B)}")
    semillas = list(range(a.desde, a.desde + a.n))
    if any(s not in SEMILLAS_OK for s in semillas): raise SystemExit('semillas fuera de 24001-24099 (exploratorias)')
    R = []
    for s in semillas:
        for b in brazos:
            x = corre(s, b, B[b][0], a.T); R.append(x)
            log(f"  s{s} {b:10s} R0real {x['R0_real_med']} persisten {x['persisten']}/9 vida {x['vida_med']} muertes {x['muertes_med']} "
                f"fund {x['fundadores_med']} causas {x['causas']} BD {x['mord_BD']} AC {x['mord_AC']} sinbueno {x['frac_sin_bueno_mundo']} "
                f"tot {x['tot']} ({x['seg']} s)")
            json.dump(dict(meta=dict(etiqueta=et, sello=sello, brazos=brazos, semillas=semillas, T=a.T, exploratorio=True,
                                     desc={b: B[b][1] for b in brazos}), R=R), open(base + '.json', 'w', encoding='utf-8'), indent=1)
    log('RESUMEN por brazo (medianas sobre semillas de la mediana de los 9 linajes)')
    por = {b: [x for x in R if x['brazo'] == b] for b in brazos}
    for b, xs in por.items():
        log(f"  {b:10s} R0real {med([x['R0_real_med'] for x in xs])} persisten {sum(x['persisten'] for x in xs)}/{9 * len(xs)} "
            f"vida {med([x['vida_med'] for x in xs])} muertes {med([x['muertes_med'] for x in xs])} fund {med([x['fundadores_med'] for x in xs])} "
            f"BD {med([x['mord_BD'] for x in xs])} AC {med([x['mord_AC'] for x in xs])} sinbueno {med([x['frac_sin_bueno_mundo'] for x in xs])} "
            f"muere_sin_parir {med([x['muere_sin_parir'] for x in xs])} · {B[b][1]}")
    if 'FAB' in por:
        f = {x['seed']: x['R0_real_med'] for x in por['FAB']}
        for b, xs in por.items():
            if b == 'FAB': continue
            d = [x['R0_real_med'] - f[x['seed']] for x in xs if x['seed'] in f]
            log(f"  pareado {b} vs FAB: gana {sum(1 for z in d if z > 0)}/{len(d)} · dif mediana {med(d)}")
    log(f"JSON: {os.path.relpath(base + '.json', RAIZ)}")
    flog.close()


if __name__ == '__main__':
    main()
