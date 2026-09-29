"""corre_organo.py — SONDA EXPLORATORIA (28-sep noche): el organo de rechazo de ECO/BLOQUES sobre V143_TERMO en la pista de la carrera.
NO es preregistro. La corrida ES corre_termo.tarea (== corre_v143.tarea + tel_termo; se IMPORTA, no se toca).
MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas).

BRAZOS: termo (V143_TERMO) · org (V143_TERMO_ORG: organo pixel 1) · orgdes (V143_TERMO_ORGDES: control, pixel 0) · o1 (O1, ancla).
SEMILLAS NUEVAS: sonda 49851-49855 · arnes/humo 49856. Sin Pool: cada proceso corre su lista en serie.
  python .../corre_organo.py --arnes                         # identidad: ORGANO 0 == V143_TERMO (T 20 000, 49856) + control que falla
  python .../corre_organo.py --humo                          # 1 proceso, 2 corridas, T 20 000, 49856: escribe JSON
  python .../corre_organo.py --corre org:49851,termo:49851   # corridas de la sonda (T 100 000), una por una, JSON antes de volver
  python .../corre_organo.py --lee                           # tabla de la sonda
"""
import argparse, glob, hashlib, importlib.util, json, os, sys, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception: pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
TERMOD = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')
if TERMOD not in sys.path: sys.path.insert(0, TERMOD)
if AQUI not in sys.path: sys.path.insert(0, AQUI)
import corre_termo as CT          # se IMPORTA, no se toca
import construye_organo as CO
CV = CT.CV; P = CT.P
CARROS = os.path.join(AQUI, 'carros'); DATOS = os.path.join(AQUI, 'datos')
BRAZOS = {'termo': 'V143_TERMO', 'org': 'V143_TERMO_ORG', 'orgdes': 'V143_TERMO_ORGDES', 'o1': 'O1', 'org0': 'V143_TERMO_ORG0'}
PROPIOS = ('V143_TERMO_ORG0', 'V143_TERMO_ORG', 'V143_TERMO_ORGDES')
SONDA = range(49851, 49856); ARNES = 49856
T_SONDA = 100000; T_HUMO = 20000


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def registra():
    CT.registra()
    for n in PROPIOS:
        if n not in CV._MODS:
            spec = importlib.util.spec_from_file_location(f"carro_{n}", os.path.join(CARROS, n + '.py'))
            m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); CV._MODS[n] = m


def verifica():
    ok = True
    for ruta, sha in CT.SHAS.items():
        s = h16(ruta); ok &= s == sha
    for n, o in CO.VARIANTES:
        b = CO.construye(n, o); ruta = os.path.join(CARROS, n + '.py')
        igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        vr = CT.RC.revisa_fuente(b.decode('utf-8'), n) if igual else ['distinto de construye_organo']
        print(f"  carro {n} sha {CO.h16b(b)} == construye: {igual} · revisa_carro: {'PASA' if not vr else vr[:2]}"); ok &= igual and not vr
    print(f"  shas fijados por corre_termo (V143, pista, juez, O1, V143_TERMO...): {'OK' if ok else 'FALLA'} · corre_termo "
          f"{h16(os.path.join(TERMOD, 'corre_termo.py'))} · corre_organo {h16(os.path.abspath(__file__))} · construye_organo {h16(CO.__file__)}")
    return ok


def corre(seed, brazo, T):
    registra()
    x = CT.tarea((seed, BRAZOS[brazo], T)); x.pop('pizarra_log', None); x['brazo'] = brazo
    return x


def limpia(x):
    """para comparar bit a bit: fuera el tiempo de reloj y el NOMBRE del carro."""
    s = json.dumps(x, default=str, sort_keys=True)
    for n in PROPIOS + ('V143_TERMO',): s = s.replace(n, 'CARRO')
    d = json.loads(s)
    d.pop('seg', None); d.pop('brazo', None)
    return d


def disparos(x):
    return {k: sum(((t or {}).get('org') or {}).get('disp', {}).get(k, 0) for t in (x.get('tel_termo') or [])) for k in 'ABCD'}


def arnes():
    t0 = time.time()
    ok = verifica(); print(f"(K) verifica: {ok}")
    a = limpia(corre(ARNES, 'termo', T_HUMO)); b = limpia(corre(ARNES, 'org0', T_HUMO))
    i1 = a == b; print(f"(A) ORGANO 0 == V143_TERMO bit a bit (49856, T {T_HUMO}, 9 carros, salida entera sin 'seg'): {i1}")
    c = corre(ARNES, 'org', T_HUMO); dc = disparos(c); dif = limpia(c) != a
    print(f"(C) control que DEBE fallar: ORGANO 1 != V143_TERMO: {dif} · disparos del organo por letra (9 linajes): {dc}"
          f" · dispara SOLO en B y D: {dc['A'] == 0 and dc['C'] == 0 and dc['B'] + dc['D'] > 0}")
    d = corre(ARNES, 'orgdes', T_HUMO); dd = disparos(d); dif2 = limpia(d) != a
    print(f"(C2) desfasado != V143_TERMO: {dif2} · dispara SOLO en C y D: {dd['A'] == 0 and dd['B'] == 0 and dd['C'] + dd['D'] > 0} · {dd}")
    tot = ok and i1 and dif and dif2 and dc['A'] == 0 and dc['C'] == 0 and dd['A'] == 0 and dd['B'] == 0
    print(f"ARNES {'PASA' if tot else 'FALLA'} en {time.time() - t0:.0f} s")
    return tot


def escribe(x, carpeta):
    os.makedirs(carpeta, exist_ok=True); fin = os.path.join(carpeta, f"{x['brazo']}_s{x['seed']}.json")
    with open(fin + '.tmp', 'w', encoding='utf-8') as fh: json.dump(x, fh, ensure_ascii=False, default=str)
    os.replace(fin + '.tmp', fin); return fin


def resumen_una(x):
    Ls = x['linajes']; n = len(Ls)
    est = [l for l in Ls if l['fund_post10k'] == 0]
    F = CT.cuerpos([x])['fundadores']
    return dict(seed=x['seed'], brazo=x['brazo'], seg=x.get('seg'), R0_real_med=CV.med([l['R0_real'] for l in Ls]),
                cruzan=sum(l['cruza_real'] for l in Ls), n=n, mayoria=bool(sum(l['cruza_real'] for l in Ls) * 2 > n),
                fund_med=CV.med([l['fundadores'] for l in Ls]), fund_med_est=(CV.med([l['fundadores'] for l in est]) if est else None),
                establecidos=len(est), causas_fund=F['causas'], fund_n=F['n'], fund_hijos=F['hijos_por_cuerpo'], fund_sin_hijos=F['frac_sin_hijos'],
                causas_todos={k: sum(l['causas'][k] for l in Ls) for k in ('hambre', 'sed', 'veneno', 'sal')},
                mord_BD=sum(l['mord']['B'] + l['mord']['D'] for l in Ls), mord_AC=sum(l['mord']['A'] + l['mord']['C'] for l in Ls),
                disparos=disparos(x))


def lee(carpeta):
    fs = sorted(glob.glob(os.path.join(carpeta, '*_s*.json')))
    D = {}
    for f in fs:
        x = json.load(open(f, encoding='utf-8')); D.setdefault(x['brazo'], []).append(resumen_una(x))
    for b in ('termo', 'org', 'orgdes', 'o1'):
        v = D.get(b)
        if not v: continue
        cz = {}
        for r in v:
            for k, c in r['causas_fund'].items(): cz[k] = cz.get(k, 0) + c
        tot = sum(cz.values()) or 1
        fe = [r['fund_med_est'] for r in v if r['fund_med_est'] is not None]
        print(f"{b:7s} n {len(v)} · R0 real med {CV.med([r['R0_real_med'] for r in v])} · mayoria cruza {sum(r['mayoria'] for r in v)}/{len(v)} · "
              f"cruzan {sum(r['cruzan'] for r in v)}/{sum(r['n'] for r in v)} · fund/linaje med {CV.med([r['fund_med'] for r in v])} · "
              f"fund/linaje establecidos med {CV.med(fe) if fe else None} (establecidos {sum(r['establecidos'] for r in v)}) · "
              f"causas fundadores " + ' '.join(f"{k} {c / tot:.3f}" for k, c in sorted(cz.items()))
              + f" (n {tot}) · fund sin hijos med {CV.med([r['fund_sin_hijos'] for r in v if r['fund_sin_hijos'] is not None])}"
              + f" · mord B+D {sum(r['mord_BD'] for r in v)} A+C {sum(r['mord_AC'] for r in v)}")
        for r in v:
            print(f"    s{r['seed']} R0 {r['R0_real_med']} cruzan {r['cruzan']}/{r['n']} fund med {r['fund_med']} est {r['establecidos']} "
                  f"disp {r['disparos']} seg {r['seg']}")
    with open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8') as fh:
        json.dump(D, fh, ensure_ascii=False, indent=1, default=str)


def main(argv=None):
    ap = argparse.ArgumentParser(allow_abbrev=False)
    ap.add_argument('--arnes', action='store_true'); ap.add_argument('--humo', action='store_true')
    ap.add_argument('--corre', default=None); ap.add_argument('--lee', action='store_true')
    a = ap.parse_args(argv)
    if a.arnes: return 0 if arnes() else 1
    if a.lee: lee(os.path.join(DATOS, f'sonda_T{T_SONDA}')); return 0
    if not verifica(): raise SystemExit('verifica FALLA: no se corre')
    if a.humo:
        c = os.path.join(DATOS, 'humo')
        for b in ('termo', 'org'):
            x = corre(ARNES, b, T_HUMO); print('  escrito', escribe(x, c), f"{x['seg']} s")
        lee(c); return 0
    if a.corre:
        c = os.path.join(DATOS, f'sonda_T{T_SONDA}')
        for it in a.corre.split(','):
            b, s = it.split(':'); s = int(s)
            if b not in ('termo', 'org', 'orgdes', 'o1') or s not in SONDA: raise SystemExit(f'fuera de la sonda: {it}')
            if os.path.exists(os.path.join(c, f'{b}_s{s}.json')): continue
            x = corre(s, b, T_SONDA); print(time.strftime('%H:%M:%S'), 'escrito', escribe(x, c), f"{x['seg']} s", flush=True)
        return 0


if __name__ == '__main__':
    sys.exit(main())
