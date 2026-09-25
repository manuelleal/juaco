# EXPLORATORIO, no es dato (runner de la SERIE preregistrada: lo que decide es veredicto(), la letra de PREREGISTRO_serie.md)
"""corre_serie.py — PROMETEO SERIE: ¿los organos que la cinta se ARMA sola se fijan POR ENCIMA DE LO NEUTRO? ¿el mundo estacional hace
mas frecuente el despegue? (Opus, equipo organelos, 25-sep-2026). MISION: llegar a la AGI por este camino.

Preregistro: PREREGISTRO_serie.md. Instrumento: motor_serie.py (construye_serie.py desde ../motor_prometeo.py) + ../codigo_prometeo.py
+ corre_codigo.trabajo() (codigo/, SIN tocar: monkeypatch SOLO en este proceso y en los hijos del Pool, que importan este modulo).
Arnes: identidad_serie.py (N/N).

Mundos: quieto y onda8k (fable_mundos). Brazos (los dos con el alfabeto CON kit: CABLE + HGT; cinta inicial v0 = filtra0 + G0; SOS no se lee):
  PROMETEO   los organos que la cinta arme ACTUAN (cables sobre boca/patas/parto; slots de transmision expresados).
  MUDO       CONTROL NEUTRO: la misma cinta, los mismos errores de copia, la misma HGT; los organos armados NO actuan (cables no leidos por
             el cuerpo; organo expresado = FILTRA0 siempre). Lo que se fija en MUDO se fija por deriva/arrastre.
TL: T 60000, cambio 8000 (onda desde ahi), corte 44000, margen 4000 (= la exploracion).  Semillas: serie 30101-30120, replica 30121-30140; humo 30190.

Uso:
  python corre_serie.py --humo --mundo quieto|onda8k          # 1 semilla, 2 brazos, TL de la serie (mide el COSTO); un proceso
  python corre_serie.py --lee <carpeta de ventana>           # la letra sobre lo que haya
  python corre_serie.py --serie --ventana serie|replica --pool 6 [--reanuda]   # SOLO el coordinador
"""
import argparse, glob, hashlib, json, os, sys, time
import numpy as np
AQUI = os.path.dirname(os.path.abspath(__file__)); PROM = os.path.dirname(AQUI); ORG = os.path.dirname(PROM)
CODIGO = os.path.join(ORG, 'codigo'); FABLE = os.path.join(CODIGO, 'exploracion_fable')
RAIZ = os.path.dirname(os.path.dirname(ORG))
for _d in (FABLE, CODIGO, PROM, AQUI):
    if _d in sys.path: sys.path.remove(_d)
    sys.path.insert(0, _d)
import motor_serie as MS
import codigo_prometeo as CP
import corre_codigo as CC
import fable_mundos as FB
import gramatica_def as GD
import organos_serie as OS
from organos_serie import claves, SEN, DEC

MUNDOS = ('quieto', 'onda8k')
BRAZOS = ('PROMETEO', 'MUDO')
TL = dict(T=60000, t_cambio=8000, t_corte=44000, r0_margen=4000)
VENTANAS = {'serie': 30101, 'replica': 30121}
N = 20
SEM_HUMO = 30190
DESPEGUE = 1000        # nacimientos solos (tras el corte) para llamar DESPEGUE a una corrida (s30003 de la exploracion: 2 677; la siguiente: 611)
FIJO = 0.5             # un organo esta FIJADO si esta en >= 50 % del banco en el corte Y al final
DATOS = os.path.join(AQUI, 'datos')


class BanderaMala(SystemExit):
    pass


# ------------------------------------------------------------------------------------------ el monkeypatch (este proceso y los hijos)
_eco_de0 = CC.eco_de
_SPEC = [None]; _BR = [None]; _ULTR = [None]


def eco_de_serie(brazo, t_corte, t_cambio, **extra):
    CP.pon_alfabeto(CP.OPS + CP.KIT)
    e = _eco_de0('CODIGO_SIN_SOS', t_corte, t_cambio, **extra)
    e['mudo'] = 1 if brazo == 'MUDO' else 0
    if brazo not in BRAZOS: raise SystemExit(f'SERIE: brazo {brazo}')
    if _SPEC[0] is not None: e['cambio'] = dict(_SPEC[0])
    return e


class _Shim:
    NOMBRES = MS.NOMBRES
    @staticmethod
    def run_solapadas(*a, **k):
        r = MS.run_solapadas(*a, **k); _ULTR[0] = r; return r


CC.MC = _Shim; CC.eco_de = eco_de_serie


# ------------------------------------------------------------------------------------------ los organos de una cinta
def fracciones(L):
    fu = {}; ie = {}; nh = 0
    for c in L:
        f, i, h = claves(c); nh += int(h)
        for k in f: fu[k] = fu.get(k, 0) + 1
        for k in i: ie[k] = ie.get(k, 0) + 1
    n = max(1, len(L))
    return {k: v / n for k, v in fu.items()}, {k: v / n for k, v in ie.items()}, nh / n


def medidas_organos(pr):
    """F = max sobre organos FUNCIONALES o de min(frac en el banco del corte, frac en el banco final); Fi = lo mismo con los INERTES."""
    bc = (pr.get('cod_corte') or {}).get('banco') or []; bf = pr.get('banco_final') or []
    fc, ic, hc = fracciones(bc); ff, iff, hf = fracciones(bf)
    def mejor(a, b):
        ks = set(a) & set(b)
        if not ks: return 0.0, None
        k = max(ks, key=lambda z: (min(a[z], b[z]), z)); return round(min(a[k], b[k]), 4), k
    F, kF = mejor(fc, ff); Fi, kI = mejor(ic, iff)
    fijos = sorted(k for k in set(fc) & set(ff) if min(fc[k], ff[k]) >= FIJO)
    return dict(F=F, organo_F=kF, F_inerte=Fi, organo_F_inerte=kI, fijos=fijos, n_banco_corte=len(bc), n_banco_final=len(bf),
                hgt_corte=round(hc, 4), hgt_final=round(hf, 4),
                top_corte=dict(sorted(fc.items(), key=lambda z: -z[1])[:6]), top_final=dict(sorted(ff.items(), key=lambda z: -z[1])[:6]))


def clase(k):
    """Descriptivo: parecido con lo que disenamos."""
    if k is None: return None
    if k == 'ORG nacer/todo/hijo/copiar': return 'ensena'
    if k.startswith('ORG nacer/') and k.endswith('/hijo/copiar'): return 'variante de filtra0'
    if not k.startswith('ORG') and k.split('->')[0] in ('reserva', 'la_otra', 'ventana', 'edad', 'hijos'): return 'lee su estado (tipo O3)'
    return 'nuevo'


# ------------------------------------------------------------------------------------------ UNA corrida (nunca lanza: nube-9)
def trabajo(job):
    mundo, seed, brazo, carpeta, reanuda = job
    sub = os.path.join(carpeta, mundo); os.makedirs(sub, exist_ok=True)
    fin = os.path.join(sub, f"{brazo}_s{seed}.json")
    try:
        if os.path.exists(fin):
            x = json.load(open(fin, encoding='utf-8'))
            if reanuda and x.get('serie_ok'): return x
            os.remove(fin)   # JSON a medias (sin organos) o sin --reanuda: se corre de nuevo (el checkpoint, si lo hay, se usa)
        _SPEC[0] = FB.catalogo(TL['t_cambio'])[mundo]; _ULTR[0] = None
        x = CC.trabajo((seed, brazo, dict(TL), sub, True))
        r = _ULTR[0]; pr = ((r or {}).get('codigo') or {}).get('prometeo')
        if pr is not None:
            kn = pr.pop('kit_nac', []) or []
            # ERR-144: suministro DE NOVO leido en la CINTA. La GUARDIA usa la ventana temprana [0, t_cambio) (cintas casi iguales en los dos
            # brazos: mide el operador de copia, no lo que la seleccion ya hizo); la del vivero entero es descriptiva (ahi MUDO acumula copias
            # neutras de ORG y su tasa de novo sube: eso ya es resultado, no instrumento).
            def _sum(a, b):
                v = [z for z in kn if a <= z[0] < b and len(z) >= 7]
                return dict(n=len(v), de_novo=(round(float(np.mean([z[5] for z in v])), 5) if v else None),
                            con_organo=(round(float(np.mean([z[6] for z in v])), 4) if v else None))
            pr['suministro'] = _sum(0, TL['t_cambio']); pr['suministro_vivero'] = _sum(0, TL['t_corte'])
            pr['largo_nac'] = [[s, round(float(np.mean([z[1] for z in kn if s <= z[0] < s + 4000])), 2)] for s in range(0, TL['T'], 4000)
                               if any(s <= z[0] < s + 4000 for z in kn)]
            pr['n_hgt_ev'] = len(pr.get('hgt_ev') or []); pr['hgt_ev'] = (pr.get('hgt_ev') or [])[:500]
            pr['organos'] = medidas_organos(pr)
        V = x.get('ventanas_r0') or []; nv = {v[0]: v[2] for v in V}
        x.update(prometeo=pr, mundo_serie=mundo, alfabeto=list(CP.ALF[0]), serie_ok=int(x.get('abortado') is None and pr is not None),
                 nac_solo=int(sum(nv.get(a, 0) for a in range(TL['t_corte'], TL['T'] - TL['r0_margen'], CC.W_NAC))))
        tmp = fin + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f: json.dump(x, f)
        os.replace(tmp, fin)
        return x
    except BaseException as e:   # nube-9: el hijo del Pool NUNCA lanza
        return dict(seed=seed, brazo=brazo, mundo_serie=mundo, abortado=f"{type(e).__name__}: {e}", serie_ok=0)


# ------------------------------------------------------------------------------------------ LA LETRA (PREREGISTRO_serie.md §4)
def veredicto(R, n_esperado=N):
    L = []
    ok = lambda x: x is not None and x.get('serie_ok') and not x.get('abortado')
    by = {(m, b): {x['seed']: x for x in R if x.get('mundo_serie') == m and x.get('brazo') == b} for m in MUNDOS for b in BRAZOS}
    completo = all(len([x for x in by[k].values() if ok(x)]) == n_esperado for k in by)
    abortados = [(x.get('mundo_serie'), x.get('brazo'), x.get('seed'), x.get('abortado')) for x in R if x.get('abortado')]
    bloq = sum(int(x.get('bloqueados') or 0) for x in R if ok(x))
    # instrumento: en MUDO el kit NO actua (contadores de boca/patas/veto en 0)
    mudo_actua = sum(1 for m in MUNDOS for x in by[(m, 'MUDO')].values() if ok(x) and any(
        ((x['prometeo'].get('kit') or {}).get(k) or 0) for k in ('boca_si', 'boca_no', 'pata_mueve', 'pata_para', 'veto')))
    P1 = {}; G = {}
    for m in MUNDOS:
        P, M = by[(m, 'PROMETEO')], by[(m, 'MUDO')]
        com = sorted(s for s in P if s in M and ok(P[s]) and ok(M[s]))
        F = lambda x: x['prometeo']['organos']['F']
        gana = sum(int(F(P[s]) > F(M[s])) for s in com)
        nfP = sum(int(F(P[s]) >= FIJO) for s in com); nfM = sum(int(F(M[s]) >= FIJO) for s in com)
        P1[m] = gana >= 14 and nfP - nfM >= 4
        sP = [P[s]['prometeo']['suministro']['de_novo'] or 0.0 for s in com]; sM = [M[s]['prometeo']['suministro']['de_novo'] or 0.0 for s in com]
        raz = (float(np.mean(sP)) / float(np.mean(sM))) if com and np.mean(sM) > 0 else None
        G[m] = raz is not None and 0.5 <= raz <= 2.0
        Fi = lambda x: x['prometeo']['organos']['F_inerte']
        L.append(f"[{m}] P1 organo armado fijado por encima de lo neutro: F(PROMETEO) > F(MUDO) en {gana}/{len(com)} (>= 14) · fijados (F >= {FIJO}) "
                 f"PROMETEO {nfP} vs MUDO {nfM} (dif >= 4) -> {P1[m]}")
        L.append(f"[{m}]   F mediana PROMETEO {np.median([F(P[s]) for s in com]) if com else None} · MUDO {np.median([F(M[s]) for s in com]) if com else None} · "
                 f"inerte (descriptivo) PROMETEO {np.median([Fi(P[s]) for s in com]) if com else None} · MUDO {np.median([Fi(M[s]) for s in com]) if com else None}")
        L.append(f"[{m}]   GUARDIA suministro DE NOVO (ERR-144: nacidos antes de t {TL['t_cambio']} con un organo armado que su donante no tenia): PROMETEO/MUDO = {None if raz is None else round(raz, 3)} "
                 f"(en [0.5, 2]) -> {G[m]}")
    dq = sum(int((x.get('nac_solo') or 0) >= DESPEGUE) for x in by[('quieto', 'PROMETEO')].values() if ok(x))
    do = sum(int((x.get('nac_solo') or 0) >= DESPEGUE) for x in by[('onda8k', 'PROMETEO')].values() if ok(x))
    P2 = do >= dq + 3
    L.append(f"P2 despegue (nac solo >= {DESPEGUE}) en PROMETEO: onda8k {do} vs quieto {dq} (onda >= quieto + 3) -> {P2}")
    L.append(f"instrumento: corridas MUDO donde el kit actuo = {mudo_actua} (debe ser 0) · bloqueados {bloq} · abortadas {len(abortados)}")
    if not completo: v = 'NO EVALUABLE (ventana incompleta)'
    elif abortados: v = f'NO EVALUABLE (abortadas: {abortados[:3]})'
    elif bloq > 0: v = f'NO EVALUABLE (tope de cuerpos: bloqueados = {bloq})'
    elif mudo_actua: v = 'NO EVALUABLE (el control MUDO actuo: instrumento roto)'
    elif not all(G.values()): v = f'NO EVALUABLE (guardia de suministro cae: {G})'
    elif all(P1.values()): v = 'FUNCIONA — los organos que la cinta se arma sola se FIJAN POR ENCIMA DE LO NEUTRO en los dos mundos'
    elif any(P1.values()): v = f'HAY ALGO MODESTO — se fijan por encima de lo neutro en un solo mundo ({[m for m in MUNDOS if P1[m]][0]})'
    else: v = 'NO — los organos armados no se fijan mas que en el control neutro'
    L.append(f"VEREDICTO P1 POR LA LETRA (una ventana; el bloque exige serie + replica con el mismo veredicto): {v}")
    L.append(f"P2 (aparte, por la letra): {'SI — el mundo estacional hace mas frecuente el despegue' if P2 else 'NO'}")
    return v, P2, L


def descriptivo(R):
    """Lo que decide APARTE (no entra a la letra): que organos, su clase, nacimientos solos."""
    L = []
    ok = lambda x: x.get('serie_ok') and not x.get('abortado')
    for m in MUNDOS:
        for b in BRAZOS:
            X = [x for x in R if ok(x) and x.get('mundo_serie') == m and x.get('brazo') == b]
            if not X: continue
            cnt = {}
            for x in X:
                for k in x['prometeo']['organos']['fijos']: cnt[k] = cnt.get(k, 0) + 1
            ns = [x['nac_solo'] for x in X]
            L.append(f"[{m}/{b}] n {len(X)} · persiste {sum(int(x.get('persiste') or 0) for x in X)} · nac solo mediana {np.median(ns):.0f} (suma {sum(ns)}) · "
                     f"despegues {sum(int(v >= DESPEGUE) for v in ns)} · HGT en el banco final (mediana) {np.median([x['prometeo']['organos']['hgt_final'] for x in X]):.2f}")
            sv = [(x['prometeo'].get('suministro_vivero') or {}) for x in X]
            L.append(f"     suministro de novo en el vivero entero (media) {np.mean([z.get('de_novo') or 0 for z in sv]):.4f} · nacidos con organo armado en la cinta {np.mean([z.get('con_organo') or 0 for z in sv]):.3f} · "
                     f"F mediana {np.median([x['prometeo']['organos']['F'] for x in X]):.3f} · F_inerte mediana {np.median([x['prometeo']['organos']['F_inerte'] for x in X]):.3f}")
            for k, v in sorted(cnt.items(), key=lambda z: -z[1])[:8]: L.append(f"     fijado en {v} semillas: {k}  [{clase(k)}]")
    return L


def SHAS():
    f = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    ps = [os.path.join(AQUI, n) for n in ('corre_serie.py', 'motor_serie.py', 'construye_serie.py', 'organos_serie.py', 'identidad_serie.py', 'PREREGISTRO_serie.md')] + \
         [os.path.join(PROM, n) for n in ('codigo_prometeo.py', 'motor_prometeo.py', 'construye_prometeo.py')] + \
         [os.path.join(CODIGO, n) for n in ('corre_codigo.py', 'codigo_def.py', 'carros/FAMB_GRAM_ECO.py')] + [os.path.join(FABLE, 'fable_mundos.py')]
    return {os.path.relpath(p, ORG): f(p) for p in ps if os.path.exists(p)}


def lee_carpeta(c):
    return [json.load(open(p, encoding='utf-8')) for p in sorted(glob.glob(os.path.join(c, '*', '*_s*.json')))]


def resumen_linea(x):
    o = (x.get('prometeo') or {}).get('organos') or {}
    return (f"{x.get('mundo_serie')}/{x.get('brazo')} s{x.get('seed')}: {x.get('seg')} s · abort {x.get('abortado')} · persiste {x.get('persiste')} · "
            f"nac solo {x.get('nac_solo')} · F {o.get('F')} ({o.get('organo_F')}) · F_inerte {o.get('F_inerte')} · fijos {o.get('fijos')} · kit {(x.get('prometeo') or {}).get('kit')}")


# ------------------------------------------------------------------------------------------ banderas (ERR-115: lo malo aborta y no escribe nada)
def parsea(argv):
    ap = argparse.ArgumentParser(allow_abbrev=False, add_help=False)
    ap.add_argument('--humo', action='store_true'); ap.add_argument('--serie', action='store_true'); ap.add_argument('--lee', default=None)
    ap.add_argument('--mundo', default=None); ap.add_argument('--ventana', default=None); ap.add_argument('--pool', type=int); ap.add_argument('--reanuda', action='store_true')
    try:
        a, resto = ap.parse_known_args(argv)
    except SystemExit:
        raise BanderaMala('SERIE: banderas mal formadas')
    if resto: raise BanderaMala(f"SERIE: banderas desconocidas {resto}")
    if any(x.startswith('--') and '=' in x for x in argv): raise BanderaMala('SERIE: sin la forma --bandera=valor')
    flags = [x for x in argv if x.startswith('--')]
    if len(flags) != len(set(flags)): raise BanderaMala('SERIE: bandera repetida')
    if int(a.humo) + int(a.serie) + int(a.lee is not None) != 1: raise BanderaMala('SERIE: exactamente uno de --humo, --serie, --lee')
    if a.humo and (a.mundo not in MUNDOS or a.ventana or a.pool is not None or a.reanuda): raise BanderaMala('SERIE: --humo --mundo quieto|onda8k (y nada mas)')
    if a.serie and (a.ventana not in VENTANAS or a.pool is None or not 1 <= a.pool <= 6 or a.mundo): raise BanderaMala('SERIE: --serie --ventana serie|replica --pool 1..6 [--reanuda]')
    if a.lee is not None and (a.mundo or a.ventana or a.pool is not None or a.reanuda): raise BanderaMala('SERIE: --lee <carpeta> va solo')
    return a


def main(argv=None):
    a = parsea(sys.argv[1:] if argv is None else argv)
    if a.lee is not None:
        R = lee_carpeta(a.lee); n_ = len(set(x.get('seed') for x in R))
        v, p2, L = veredicto(R, n_esperado=n_)
        for l in L + descriptivo(R): print(l)
        return
    if a.humo:
        ts = time.strftime('%Y%m%d_%H%M%S'); carpeta = os.path.join(DATOS, 'humo', f"humo_{a.mundo}_{ts}"); os.makedirs(carpeta, exist_ok=True)
        t0 = time.time(); print(f"[{time.strftime('%H:%M:%S')}] HUMO SERIE {a.mundo} s{SEM_HUMO} {TL} · shas {SHAS()}", flush=True)
        R = []
        for b in BRAZOS:
            x = trabajo((a.mundo, SEM_HUMO, b, carpeta, False)); R.append(x); print(f"[{time.strftime('%H:%M:%S')}] " + resumen_linea(x)[:600], flush=True)
        json.dump(dict(humo=True, mundo=a.mundo, tl=TL, seg=round(time.time() - t0, 1), seg_por_corrida=[x.get('seg') for x in R], shas=SHAS(),
                       lineas=[resumen_linea(x) for x in R], serie_ok=[x.get('serie_ok') for x in R]),
                  open(os.path.join(carpeta, 'HUMO.json'), 'w', encoding='utf-8'), indent=1)
        print(f"HUMO: {round(time.time() - t0, 1)} s (numeros sin valor) · {os.path.relpath(carpeta, RAIZ)}")
        return
    # --serie (SOLO el coordinador; Pool)
    d0 = VENTANAS[a.ventana]; semillas = range(d0, d0 + N); etq = f"prometeo_{a.ventana}_s{d0}-{d0 + N - 1}"
    carpeta = os.path.join(DATOS, etq)
    if os.path.exists(carpeta) and not a.reanuda and glob.glob(os.path.join(carpeta, '*', '*_s*.json')):
        raise SystemExit(f"SERIE: {carpeta} ya tiene resultados; --reanuda")
    os.makedirs(carpeta, exist_ok=True)
    flog = open(os.path.join(carpeta, 'progreso.log'), 'a', encoding='utf-8')
    def log(s):
        s = f"[{time.strftime('%H:%M:%S')}] {s}"; print(s, flush=True); flog.write(s + '\n'); flog.flush()
    log(f"PROMETEO SERIE {etq} · {TL} · brazos {BRAZOS} · mundos {MUNDOS} · pool {a.pool} · reanuda {a.reanuda} · shas {SHAS()}")
    jobs = [(m, s, b, carpeta, a.reanuda) for s in semillas for m in MUNDOS for b in BRAZOS]
    t0 = time.time()
    from multiprocessing import Pool
    with Pool(a.pool) as pool:
        for k, x in enumerate(pool.imap_unordered(trabajo, jobs), 1):
            log(f"[{k}/{len(jobs)}] " + resumen_linea(x)[:500])
    R = lee_carpeta(carpeta)
    v, p2, L = veredicto(R)
    for l in L + descriptivo(R): log(l)
    json.dump(dict(etiqueta=etq, veredicto=v, P2=p2, lineas=L, descriptivo=descriptivo(R), seg=round(time.time() - t0), TL=TL, shas=SHAS()),
              open(os.path.join(carpeta, 'RESUMEN.json'), 'w', encoding='utf-8'), indent=1, default=str)
    flog.close()


if __name__ == '__main__':
    try:
        main()
    except BanderaMala as e:
        print(str(e), file=sys.stderr); sys.exit(2)
