"""Arnes de identidad BIT A BIT de mundo_subida_b.py (regla 2 de EQUIPO.md). Un proceso, sin Pool.

I-13  (perillas apagadas) mundo_subida_b.run == experimentos/subida_n6/mundo_subida.run (484e34db8f2150da), TODAS las
      claves: anillo v13, anillo con mapa, 2d, rodeo, muralla (6 brazos del 21-sep) y el mundo PARTIDO de subida_n6
      (cierre=5: CIEGO, GF, BRUJULA, BARAJADO, INVERTIDO, PLACEBO).
I-142 (kwargs del tronco leidos de organismo_v142.run con inspect, mundo apagado) mundo_subida_b.run ==
      organismo/organismo_v142.run (17528d767fcebaf6), todas las claves de v14.2: por defecto, con invertir_en y con
      nuevo='C' (examen de desdecirse y de estimulo nuevo del tronco).
CONTROLES que DEBEN DIFERIR: explora=1; vista=1 (con explora: sola puede ser inerte, §9); metas2; kwargs del tronco en el mundo partido; brujula en metas2.
CLASES (instrumento): con un BFS INDEPENDIENTE (coordenadas x,y, escrito aqui, no el del mundo) se comprueba cada
      salida de la prueba metas2: camino a la comida correcta = p0, la otra a >= p0+2, cruza = la correcta al otro lado
      y Manhattan < camino, desvia = la correcta del mismo lado y la otra mas cerca en linea recta; y que el mundo esta
      PARTIDO (ningun camino entre bandas sin pasar por el hueco: ERR-117).
Ultima linea: "RESULTADO: N/N". Escribe datos/humo/identidad_subida_b_<fecha>.json.
Uso: python experimentos/subida_n6b/identidad_subida_b.py
"""
import collections, datetime, hashlib, inspect, json, os, sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))          # ERR-28: organismo/ SIEMPRE primero
sys.path.insert(1, os.path.join(RAIZ, 'experimentos', 'subida_n6'))
sys.path.insert(2, AQUI)

import organismo_v142 as TR                                   # noqa: E402
import mundo_subida as VIEJO                                  # noqa: E402
import mundo_subida_b as NUEVO                                # noqa: E402

SHA = {'experimentos/subida_n6/mundo_subida.py': '484e34db8f2150da', 'organismo/organismo_v142.py': '17528d767fcebaf6',
       'experimentos/subida_n6b/mundo_subida_b.py': '214d5763758473fa'}
SEEDS = (14642, 14643, 14644)   # semillas del arnes (serie 14601-14620, replica 14621-14640, humo 14641)
T = 6000
T_P = 20000   # controles en el mundo partido: el campo necesita valor(A) > 0
CLAVES_V142 = sorted(['desambiguar', 'des_splits', 'des_t', 'puerta_pat', 'pat_shuf', 'pat_min', 'n_cod'])   # las que v14.2 agrega a la salida de v13
TRONCO_KW = {k: v.default for k, v in inspect.signature(TR.run).parameters.items()
             if v.default is not inspect.Parameter.empty and k not in ('T',)}
M2D = dict(sitios=('A', 'B', 'B', 'B', 'B'), xy=((0, 0), (2, -2), (2, -1), (2, 0), (2, 1)),
           casos=({'et': 'rodeo', 'S': (6, 0), 'ok': (0, 3)},))


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def _norm(o):
    if isinstance(o, dict):
        return {str(k): _norm(v) for k, v in sorted(o.items(), key=lambda kv: str(kv[0]))}
    if isinstance(o, (list, tuple)):
        return [_norm(v) for v in o]
    if isinstance(o, float):
        return repr(float(o))
    if hasattr(o, 'tolist'):
        return _norm(o.tolist())
    return o


def sello(r, claves=None):
    if claves is not None:
        r = {k: r[k] for k in claves}
    return hashlib.sha256(json.dumps(_norm(r), sort_keys=True).encode()).hexdigest()[:16]


def mur(**pex):
    pr = dict(modo='muralla', n_tel=8, max_pasos=60, E_test=0.3, d_ini=5); pr.update(pex)
    return dict(T=T, ancho=11, alto=9, r_vis=1, sitios=('B',), regen=50, usa_M=True, prueba=pr)


def part(T_=T, **pex):
    pr = dict(modo='muralla', n_tel=8, max_pasos=60, E_test=0.3, d_ini=4, cierre=5); pr.update(pex)
    return dict(T=T_, ancho=11, alto=11, r_vis=1, sitios=('B',), regen=50, usa_M=True, prueba=pr)


GF = dict(camino=1, grad=1, filtro=1)
CASOS13 = []
for s in SEEDS:
    CASOS13 += [
        ('anillo v13 (sin mapa)', s, dict(T=T)),
        ('anillo con mapa', s, dict(T=T, r_vis=3, sitios=('A', 'B'), usa_M=True)),
        ('rejilla modo=2d', s, dict(T=T, ancho=17, alto=13, r_vis=3, sitios=M2D['sitios'], regen=50, usa_M=True,
                                    prueba=dict(modo='2d', xy=M2D['xy'], casos=M2D['casos'], n_tel=8, max_pasos=60, E_test=0.3))),
        ('anillo modo=rodeo', s, dict(T=T, r_vis=3, sitios=('A', 'B', 'A'), usa_M=True,
                                      prueba=dict(modo='rodeo', g1=5, g2=20, n_tel=8, max_pasos=60, E_test=0.3))),
        ('muralla 21-sep CIEGO', s, dict(mur(), usa_M=False)),
        ('muralla 21-sep CAMINO', s, dict(mur(), camino=1)),
        ('muralla 21-sep CAMINO placebo', s, dict(mur(), camino=1, placebo=3)),
        ('muralla 21-sep barajar', s, dict(mur(barajar=True), camino=1)),
        ('muralla 21-sep invertir', s, dict(mur(invertir=True), camino=1)),
        ('partido n6 CIEGO', s, dict(part(), usa_M=False)),
        ('partido n6 GF', s, dict(part(), **GF)),
        ('partido n6 BRUJULA', s, dict(part(), brujula=1, **GF)),
        ('partido n6 BARAJADO', s, dict(part(barajar=True), **GF)),
        ('partido n6 INVERTIDO', s, dict(part(invertir=True), **GF)),
        ('partido n6 PLACEBO', s, dict(part(), placebo=3, **GF)),
    ]
CASOS142 = []
for s in SEEDS:
    CASOS142 += [('tronco por defecto', s, dict(T=T)),
                 ('tronco invertir_en', s, dict(T=T, invertir_en=T // 2)),
                 ('tronco nuevo=C', s, dict(T=T, nuevo='C', nuevo_en=T // 2))]


def bfs_xy(W, H, bloq, src, tapa=None):
    D = {src: 0}; q = collections.deque([src])
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = ((x + dx) % W, (y + dy) % H)
            if n in D or n in bloq or n == tapa:
                continue
            D[n] = D[(x, y)] + 1; q.append(n)
    return D


def man(W, H, a, b):
    dx = abs(a[0] - b[0]); dy = abs(a[1] - b[1])
    return min(dx, W - dx) + min(dy, H - dy)


def revisa_clases(tel, W, H):
    """Comprueba con un BFS independiente cada salida de metas2. Devuelve (ok, detalle)."""
    xy = lambda c: (c % W, c // W)
    sit = {int(c): k for c, k in tel['sitios'].items()}
    bloq = {xy(c) for c, k in sit.items() if k == 'B'}
    com = [xy(c) for c, k in sit.items() if k == 'A']
    if len(com) != 2:
        return False, f"{len(com)} comidas"
    # el mundo esta PARTIDO: las dos filas de veneno, una con UN hueco y otra ENTERA
    filas = collections.Counter(y for _, y in bloq)
    llenas = sorted(y for y, n in filas.items() if n == W); con_hueco = sorted(y for y, n in filas.items() if n == W - 1)
    if len(llenas) != 1 or len(con_hueco) != 1 or sum(filas.values()) != 2 * W - 1:
        return False, f"filas de veneno {dict(filas)}"
    hueco = [(x, con_hueco[0]) for x in range(W) if (x, con_hueco[0]) not in bloq][0]
    lado = set(bfs_xy(W, H, bloq, com[0], tapa=hueco))
    if com[1] in lado:
        return False, 'las dos comidas del mismo lado'
    if len(lado) + len(set(bfs_xy(W, H, bloq, com[1], tapa=hueco))) != W * H - len(bloq) - 1:
        return False, 'el mundo no queda partido en dos bandas + hueco'
    Dc = {c: bfs_xy(W, H, bloq, c) for c in com}
    for cs in tel['casos']:
        S, F, O = xy(cs['S']), xy(cs['F']), xy(cs['otra'])
        pF, pO = Dc[F][S], Dc[O][S]
        if pF != cs['p0'] or pF + 2 > pO:
            return False, f"camino {cs}"
        mismo = (S in lado) == (F in lado)
        if cs['caso'] == 'cruza' and (mismo or man(W, H, S, F) >= pF):
            return False, f"cruza mal clasificada {cs}"
        if cs['caso'] == 'desvia' and (not mismo or man(W, H, S, O) >= man(W, H, S, F)):
            return False, f"desvia mal clasificada {cs}"
    return True, f"{len(tel['casos'])} salidas; n_salidas {tel['n_salidas']}"


if __name__ == '__main__':
    for p, e in SHA.items():
        h = h16(os.path.join(RAIZ, p))
        print(f"  {p:44s} {h}  (esperado {e})")
        if h != e:
            raise SystemExit(f'sha cambiado en {p}: abortado')
    print(f"  kwargs del tronco (inspect organismo_v142.run): { {k: v for k, v in TRONCO_KW.items() if k in ('eta_s', 'clip_s', 'mask_rel', 'puerta_pat', 'pat_min', 'desambiguar')} }")
    filas = []; ok = tot = 0

    def fila(tipo, et, s, a, b, bien, extra=''):
        global ok, tot
        tot += 1; ok += int(bien)
        filas.append(dict(tipo=tipo, caso=et, seed=s, a=a, b=b, ok=bool(bien), extra=extra))
        print(f"  [{'OK ' if bien else 'MAL'}] {tipo:8s} {et:34s} seed {s}  {a}  {b} {extra}")

    for et, s, kw in CASOS13:   # todas las claves de mundo_subida; las claves NUEVAS deben ser SOLO las del tronco v14.2
        rv = VIEJO.run(s, **kw); rn = NUEVO.run(s, **kw)
        extra = sorted(set(rn) - set(rv))
        a = sello(rv); b = sello(rn, claves=list(rv))
        fila('I-13', et, s, a, b, a == b and extra == CLAVES_V142 and set(rv) <= set(rn), '' if extra == CLAVES_V142 else f'claves extra {extra}')
    for et, s, kw in CASOS142:
        rt = TR.run(s, **kw); rn = NUEVO.run(s, **{**TRONCO_KW, **kw})
        a = sello(rt); b = sello(rn, claves=list(rt)); fila('I-142', et, s, a, b, a == b)
    for s in SEEDS:
        base = NUEVO.run(s, **{**TRONCO_KW, **part(T_P)}, **GF)
        con_x = NUEVO.run(s, **{**TRONCO_KW, **part(T_P)}, explora=1, **GF)
        fila('CONTROL', 'explora=1 difiere (M_llenas)', s, sello(base), sello(con_x), sello(base) != sello(con_x),
             f"M_llenas {base['M_llenas']} -> {con_x['M_llenas']}")
        # vista se prueba CON explora: sola puede ser inerte bit a bit (primera corrida del arnes, semilla 14644: 523
        # avistamientos a un paso, todos de celdas ya conocidas; PREREGISTRO §9). Con explora el organismo costea las
        # murallas y la vista escribe veneno antes de pisarlo.
        con_vx = NUEVO.run(s, **{**TRONCO_KW, **part(T_P)}, vista=1, explora=1, **GF)
        fila('CONTROL', 'vista=1 difiere (con explora)', s, sello(con_x), sello(con_vx), sello(con_x) != sello(con_vx))
        m2 = NUEVO.run(s, **{**TRONCO_KW, **part(T_P, metas2=True)}, explora=1, **GF)
        fila('CONTROL', 'metas2 difiere', s, sello(con_x), sello(m2), sello(con_x) != sello(m2))
        v13 = NUEVO.run(s, **part(T_P, metas2=True), explora=1, **GF)
        fila('CONTROL', 'tronco v14.2 != v13 en el mundo', s, sello(v13), sello(m2), sello(v13) != sello(m2),
             f"W v13 {v13['W']['A']}/{v13['W']['B']}  v14.2 {m2['W']['A']}/{m2['W']['B']}")
        bj = NUEVO.run(s, **{**TRONCO_KW, **part(T_P, metas2=True)}, explora=1, brujula=1, **GF)
        fila('CONTROL', 'brujula difiere en metas2', s, sello(m2), sello(bj), sello(m2) != sello(bj))
        for et, r in (('clases metas2 (GFX v14.2)', m2), ('clases metas2 (v13)', v13)):
            bien, det = revisa_clases(r['tel'], 11, 11)
            fila('CLASES', et, s, r['tel']['geo'], '', bien, det)
    print(f"IDENTIDAD {ok}/{tot}")
    dest = os.path.join(AQUI, 'datos', 'humo', 'identidad_subida_b_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.json')
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    json.dump(dict(sha=SHA, tronco_kw=TRONCO_KW, ok=ok, tot=tot, filas=filas), open(dest, 'w', encoding='utf-8'),
              ensure_ascii=False, default=str)
    print(f"JSON {os.path.relpath(dest, RAIZ)}  sha {h16(dest)}")
    print(f"RESULTADO: {ok}/{tot}")
    sys.exit(0 if ok == tot else 1)
