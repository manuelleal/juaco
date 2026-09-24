"""corre_n10c.py — SUBIDA_N10C: "la familia pasa SOLO LO QUE IMPORTA" (PREREGISTRO_n10c.md manda).

MISION: llegar a la AGI por este camino.

Instrumento = el de subida_n10b SIN TOCAR: se importa corre_n10b (sha fijado) y se usan SUS funciones tarea, agrega y pareado
(mismo mundo: pista2 solapadas=1, quimiostato 'fija', r_rep 0.03, tope 300, T = 100000; mismo juez; mismas medidas). Lo unico
que cambia es QUE carros carga: se reasignan corre_n10b.carga / MONO / MIX / PARES / PARES_MIX en este proceso y en cada worker
del Pool (inicializador). Carros: carros_n10c.py (subclases de los FAMB_* de n10b con el FILTRO de lo neutro en el parto).
Brazos: NADA · RES · RES_SIN0 (candidato) · BAR_SIN0 (control de contenido que puede ganar) · ORA_SIN0 (referencia) · MIX
(3 NADA + 3 RES_SIN0 + 3 BAR_SIN0 en el MISMO mundo).

ERR-115: el parser es una LISTA BLANCA; aborta ante cualquier bandera desconocida, abreviada, con '=', repetida o '--help'.
Uso:
  humo (un proceso, sin Pool):  python experimentos/subida_n10c/corre_n10c.py --humo                 (semilla 12891, T = 20000, 6 brazos)
  identidad:                    python experimentos/subida_n10c/identidad_n10c.py
  serie (SOLO el coordinador):  python experimentos/subida_n10c/corre_n10c.py --serie --desde 12801 --n 20 --pool 3
  replica (SOLO coordinador):   python experimentos/subida_n10c/corre_n10c.py --serie --desde 12821 --n 20 --pool 3
"""
import gzip, hashlib, json, os, platform, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SIN_VALOR = {'--humo', '--serie'}
CON_VALOR = {'--desde': int, '--n': int, '--pool': int}
MONO = ('NADA', 'RES', 'RES_SIN0', 'BAR_SIN0', 'ORA_SIN0')
BRAZOS = MONO + ('MIX',)
MIX = ['NADA'] * 3 + ['RES_SIN0'] * 3 + ['BAR_SIN0'] * 3
PARES = (('RES_SIN0', 'RES'), ('RES_SIN0', 'BAR_SIN0'), ('RES_SIN0', 'NADA'), ('BAR_SIN0', 'NADA'), ('RES', 'NADA'),
         ('ORA_SIN0', 'RES_SIN0'))
PARES_MIX = (('RES_SIN0', 'NADA'), ('RES_SIN0', 'BAR_SIN0'), ('BAR_SIN0', 'NADA'))
SEMILLAS = dict(practica=(12891, 12899), serie=(12801, 12820), replica=(12821, 12840))
T_DEF = 100000
T_HUMO = 20000
GANA = 15
SHA_CORRE_N10B = 'b7808bbb83fb038e'
SHA_CARROS_N10C = '67f149c81f880cb1'   # fijado tras el arnes 16/16 y antes del humo (PREREGISTRO_n10c.md sec. 3)
ANCLA_NADA = (0.085, 0.135)  # n10b (ERR-116), la MISMA ancla calibrada
BANDA_RES = (0.60, 0.82)     # n10b dio 0.688 (serie) y 0.737 (replica) con el mismo instrumento


class BanderaMala(SystemExit):
    pass


def parsea(argv):
    a = dict(humo=False, serie=False, desde=None, n=None, pool=None)
    vistos = set(); i = 0
    while i < len(argv):
        f = argv[i]
        if f in vistos: raise BanderaMala(f"corre_n10c: bandera repetida {f!r} -> ABORTA (ERR-115)")
        vistos.add(f)
        if f in SIN_VALOR:
            a[f[2:]] = True; i += 1
        elif f in CON_VALOR:
            if i + 1 >= len(argv): raise BanderaMala(f"corre_n10c: falta el valor de {f} -> ABORTA")
            try: a[f[2:]] = CON_VALOR[f](argv[i + 1])
            except ValueError: raise BanderaMala(f"corre_n10c: valor malo para {f}: {argv[i + 1]!r} -> ABORTA")
            i += 2
        else:
            raise BanderaMala(f"corre_n10c: bandera desconocida {f!r}; validas {sorted(SIN_VALOR | set(CON_VALOR))} -> ABORTA (ERR-115)")
    if a['humo'] == a['serie']: raise BanderaMala("corre_n10c: exactamente una de --humo / --serie -> ABORTA")
    if a['humo'] and any(a[k] is not None for k in ('desde', 'n', 'pool')): raise BanderaMala("corre_n10c: --humo no admite otras banderas -> ABORTA")
    if a['serie']:
        if (a['desde'], a['n']) not in ((SEMILLAS['serie'][0], 20), (SEMILLAS['replica'][0], 20)):
            raise BanderaMala(f"corre_n10c: la serie solo corre --desde {SEMILLAS['serie'][0]} o {SEMILLAS['replica'][0]} con --n 20 -> ABORTA")
        if a['pool'] is None or not 1 <= a['pool'] <= 6: raise BanderaMala("corre_n10c: --pool entre 1 y 6 -> ABORTA")
    return a


def h16(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def _instala():
    """Reasigna en corre_n10b QUE carros carga (y los pares); todo lo demas del instrumento queda igual."""
    sys.path.insert(0, os.path.join(RAIZ, 'experimentos', 'subida_n10b')); sys.path.insert(0, AQUI)
    import corre_n10b as CN
    import carros_n10c as C3
    CN.carga = C3.modulo
    CN.MONO = MONO; CN.MIX = list(MIX); CN.PARES = PARES; CN.PARES_MIX = PARES_MIX
    return CN, C3


def tarea(args):
    CN, C3 = _instala()
    r = CN.tarea(args)
    for et in ('RES_SIN0', 'BAR_SIN0'):   # telemetria del carro (informa; ERR-96): la de n10b solo cubre RES, RES1 y BAR
        if et in r['estr'] and et in C3.ULTIMO:
            r['estr'][et]['tele'] = CN.tele(C3.ULTIMO[et])
    return r


def verifica_shas(CN, log):
    p = os.path.join(RAIZ, 'experimentos', 'subida_n10b', 'corre_n10b.py')
    if h16(p) != SHA_CORRE_N10B: raise SystemExit(f"corre_n10c: corre_n10b.py con sha {h16(p)} != {SHA_CORRE_N10B} -> ABORTA")
    CN.verifica_shas()   # pista2, motor_convive, corre_convive, FABRICA y los FAMB_* de n10b
    pc = os.path.join(AQUI, 'carros_n10c.py')
    if SHA_CARROS_N10C is not None and h16(pc) != SHA_CARROS_N10C:
        raise SystemExit(f"corre_n10c: carros_n10c.py con sha {h16(pc)} != {SHA_CARROS_N10C} -> ABORTA")
    log(f"shas: corre_n10b.py={h16(p)} carros_n10c.py={h16(pc)} " + ' '.join(f"{os.path.basename(k)}={v}" for k, v in CN.SHAS.items()))


def veredicto(A, P, PM, n_sem):
    """La letra de PREREGISTRO_n10c.md sec. 6."""
    g = GANA * n_sem / 20
    par = {(x['par'], x['clave']): x for x in P}; pm = {(x['par'], x['clave']): x for x in PM}
    ok = lambda d, k: bool(d.get(k) and d[k]['gana'] >= g)
    v = {}
    nd = A.get('NADA', {}); rs = A.get('RES', {}); r0 = A.get('RES_SIN0', {})
    v['V-ANCLA-c (mediana R0_nacidos NADA en [0.085, 0.135] y NADA persiste_carro <= 5/20)'] = bool(
        nd.get('R0_nacidos') is not None and ANCLA_NADA[0] <= nd['R0_nacidos'] <= ANCLA_NADA[1] and nd.get('persiste_carro', 99) <= 5 * n_sem / 20)
    v['V-RES-c (mediana R0_nacidos RES en [0.60, 0.82])'] = bool(rs.get('R0_nacidos') is not None and BANDA_RES[0] <= rs['R0_nacidos'] <= BANDA_RES[1])
    s1 = ok(par, ('RES_SIN0-RES', 'R0_nacidos')); s2 = ok(par, ('RES_SIN0-BAR_SIN0', 'R0_nacidos'))
    s3 = ok(pm, ('RES_SIN0-NADA', 'R0_nacidos')); s4 = ok(pm, ('RES_SIN0-BAR_SIN0', 'R0_nacidos'))
    h1 = bool(r0.get('sem_R0nac_ge_090') is not None and r0['sem_R0nac_ge_090'] >= g)
    pe = bool(r0.get('persiste_carro') is not None and r0['persiste_carro'] >= g)
    v['S-1 (RES_SIN0 > RES en R0_nacidos >= 15/20)'] = s1
    v['S-2 (RES_SIN0 > BAR_SIN0 en R0_nacidos >= 15/20)'] = s2
    v['S-3 (MIX: RES_SIN0 > NADA, mismo mundo, >= 15/20)'] = s3
    v['S-4 (MIX: RES_SIN0 > BAR_SIN0, mismo mundo, >= 15/20)'] = s4
    v['R0N-90 (calificador: RES_SIN0 R0_nacidos >= 0.90 en >= 15/20 semillas; NO es H-1: H-1 exige ademas 0 fundadores)'] = h1
    v['PER-c (calificador: persiste el carro RES_SIN0 en >= 15/20 semillas)'] = pe
    v['informativo ORA_SIN0 > RES_SIN0 (semillas)'] = (par.get(('ORA_SIN0-RES_SIN0', 'R0_nacidos')) or {}).get('gana')
    v['informativo persiste_carro por brazo'] = {b: A[b].get('persiste_carro') for b in MONO if b in A}
    validez = v['V-ANCLA-c (mediana R0_nacidos NADA en [0.085, 0.135] y NADA persiste_carro <= 5/20)'] and v['V-RES-c (mediana R0_nacidos RES en [0.60, 0.82])']
    if not validez:
        V = 'NO SE LEE (validez: el ancla NADA o la banda de RES cayo; el instrumento o el mundo no es el de n10b)'
    elif s1 and s2 and s3 and s4:
        V = 'FUNCIONA' + (' + R0 DE NACIDOS >= 0.90' if h1 else '') + (' + PERSISTE' if pe else '')
    elif s1 and s2:
        V = 'HAY ALGO MODESTO' + (' + R0 DE NACIDOS >= 0.90' if h1 else '') + (' + PERSISTE' if pe else '')
    else:
        V = 'NO'
    v['VEREDICTO'] = V
    return v


def main(argv):
    a = parsea(argv)   # ANTES de importar nada pesado o tocar disco (ERR-115)
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    CN, C3 = _instala()
    if a['humo']:
        semillas = [SEMILLAS['practica'][0]]; T = T_HUMO; sal = os.path.join(AQUI, 'datos', 'humo'); et = f"n10c_humo_s{semillas[0]}_T{T}"
    else:
        semillas = list(range(a['desde'], a['desde'] + a['n'])); T = T_DEF; sal = os.path.join(AQUI, 'datos'); et = f"n10c_serie_s{semillas[0]}-{semillas[-1]}_T{T}"
    os.makedirs(sal, exist_ok=True)
    sello = time.strftime('%Y%m%d_%H%M%S'); base = os.path.join(sal, f"{et}_{sello}")
    flog = open(base + '.log', 'w', encoding='utf-8')

    def log(s=''):
        print(s, flush=True); flog.write(s + '\n'); flog.flush()
    pre = os.path.join(AQUI, 'PREREGISTRO_n10c.md')
    log(f"corre_n10c · {et} · {sello} · python {platform.python_version()} · corre_n10c.py {h16(os.path.abspath(__file__))} · "
        f"PREREGISTRO_n10c.md {h16(pre) if os.path.exists(pre) else 'NO EXISTE'}")
    if not os.path.exists(pre): raise SystemExit('corre_n10c: no existe PREREGISTRO_n10c.md -> ABORTA (se escribe ANTES de correr)')
    verifica_shas(CN, log)
    tareas = [(s, b, T) for b in BRAZOS for s in semillas]
    t0 = time.time(); R = []

    def linea(r):
        return f"  {r['brazo']:8s} s{r['seed']} {r['seg']:7.1f} s · " + ' · '.join(
            f"{e}: R0nac {v['R0_nacidos']} vida nac {v['vida_nacidos']} nac {v['nac']} tam {v['tam_carro']} gen {v['gen_max']} "
            f"sin_ext {v['linajes_sin_ext']} carro {int(v['persiste_carro'])}" + (f" tele {v['tele']}" if v.get('tele') else '')
            for e, v in r['estr'].items())
    if a['pool'] and a['pool'] > 1:
        from multiprocessing import Pool
        with Pool(a['pool']) as pool:
            for r in pool.imap_unordered(tarea, tareas): R.append(r); log(linea(r))
    else:
        for tk in tareas: r = tarea(tk); R.append(r); log(linea(r))
    with gzip.open(base + '_crudo.json.gz', 'wt', encoding='utf-8') as f: json.dump(R, f)   # ERR-54: el crudo ANTES de resumir
    A, P, PM = CN.agrega(R)
    log(f"\nAGREGADO (medianas por semilla) · {len(semillas)} semillas · {time.time() - t0:.0f} s de pared")
    for b, v in A.items(): log(f"  {b:9s} {v}")
    log("PAREADOS (monocultivo, por semilla):")
    for x in P: log(f"  {x}")
    log("PAREADOS (MIX, dentro del mismo mundo):")
    for x in PM: log(f"  {x}")
    V = veredicto(A, P, PM, len(semillas)) if a['serie'] else {'VEREDICTO': 'HUMO: no hay veredicto (una semilla de practica)'}
    log("VEREDICTO por la letra (PREREGISTRO_n10c.md sec. 6):")
    for k, v in V.items(): log(f"  {k}: {v}")
    meta = dict(etiqueta=et, sello=sello, semillas=semillas, T=T, brazos=list(BRAZOS), corre_n10c=h16(os.path.abspath(__file__)),
                carros_n10c=h16(os.path.join(AQUI, 'carros_n10c.py')), corre_n10b=h16(os.path.join(RAIZ, 'experimentos', 'subida_n10b', 'corre_n10b.py')),
                preregistro=h16(pre), seg_pared=round(time.time() - t0, 1), seg_cpu=round(sum(r['seg'] for r in R), 1))
    res = dict(meta=meta, agregado=A, pareados=P, pareados_mix=PM, veredicto=V,
               por_semilla=[{k: r[k] for k in ('seed', 'brazo', 'T', 'seg', 'estr')} for r in R])
    json.dump(res, open(base + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
    log(f"\nescrito: {os.path.relpath(base + '.json', RAIZ)} ({h16(base + '.json')}) · crudo {os.path.relpath(base + '_crudo.json.gz', RAIZ)}")
    flog.close()


if __name__ == '__main__':
    main(sys.argv[1:])
