"""Arnes de identidad de subida_n8c_memoria_lenta (se corre ANTES de mirar cualquier numero). Escribe identidad_n8c_salida.txt.
Un proceso, sin Pool. Corridas cortas (<= 40 000 pasos) salvo UNA de 200 000 (A3: la BASE reproduce el JSON de la serie de
subida_n8 en la semilla 12601, medida por medida). Ultima linea: "RESULTADO: N/N"."""
import hashlib, inspect, io, json, os, re, subprocess, sys, tempfile, time, contextlib

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
N8 = os.path.join(RAIZ, 'experimentos', 'subida_n8')
sys.path.insert(0, AQUI)
sys.path.insert(0, N8)
sys.path.insert(0, os.path.join(RAIZ, 'organismo'))
import numpy as np
import construye_n8c as CN
import organismo_repaso as ORP
import organismo_flujo as OF
import organismo_v142 as TR
import mundo_n8 as MN
import corre_n8c as CR

NUEVAS = {'n_rep', 'n_rep_pos', 'n_rep_neg', 'repaso', 'dosis'}
SERIE_N8 = os.path.join(N8, 'datos', 'n8_serie_base-fus-fusazar-recic_s12601-12620_20260923_164801.json')
SHA_SERIE_N8 = '2d6e45e313ed0401'
R = []
LINEAS = []


def chk(nombre, ok, det=''):
    R.append(bool(ok))
    ln = f"  [{'OK ' if ok else 'MAL'}] {nombre} {det}"
    LINEAS.append(ln); print(ln, flush=True)


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def sin(d):
    return {k: v for k, v in d.items() if k not in NUEVAS}


def plan12(semilla, n_est):
    orden, pats, val = MN.mundo(semilla, n_est=n_est)
    return orden, pats, val, MN.plan_de(orden, val)


def corre_cli(args):
    p = subprocess.run([sys.executable, os.path.join(AQUI, 'corre_n8c.py')] + args, capture_output=True, text=True,
                       encoding='utf-8', errors='replace', cwd=RAIZ)
    return p.returncode, p.stdout + p.stderr


def listado():
    out = set()
    for d, _, fs in os.walk(os.path.join(AQUI, 'datos')):
        out |= {os.path.join(d, f) for f in fs}
    return out


def main():
    t0 = time.time()
    print(f"identidad_n8c  {time.strftime('%Y-%m-%d %H:%M:%S')}")
    # (0) procedencia
    chk('(0a) origen organismo_flujo sha', h16(CN.ORIGEN) == CN.SHA_ORIGEN, h16(CN.ORIGEN))
    chk('(0b) tronco organismo_v142 sha', h16(os.path.join(RAIZ, 'organismo', 'organismo_v142.py')) == CR.SHA_TRONCO)
    chk('(0c) organismo_repaso en disco == construye_n8c y == sha del runner',
        open(os.path.join(AQUI, 'organismo_repaso.py'), encoding='utf-8').read() == CN.construir()
        and h16(os.path.join(AQUI, 'organismo_repaso.py')) == CR.SHA_ORG, h16(os.path.join(AQUI, 'organismo_repaso.py')))
    chk('(0d) mundo_n8 sha (importado de solo lectura)', h16(os.path.join(N8, 'mundo_n8.py')) == CR.SHA_MUN)
    V = CR.V142
    # (A) perilla apagada == organismo_flujo EXACTO, todas las claves (retina 6, mundo de dos estimulos)
    for s in (1, 2):
        a = ORP.run(s, T=20000, **V); b = OF.run(s, T=20000, **V)
        chk(f'(A) s{s} repaso=0 == organismo_flujo, retina 6, T 20000, {len(b)} claves', sin(a) == b, f"muertes {a['deaths']}")
    # (A1) en el mundo en flujo de 12 pixeles, con fotos; y con dosis=10 pero repaso=0 (dosis inerte)
    for s, dz in ((1, 1), (2, 10)):
        _, pats, _, plan = plan12(s, 40)
        ch = [MN.t_entrada(i) for i in range(1, 40)]
        a = ORP.run(s, T=40000, plan=plan, pats=pats, chk=ch, ventana=8, repaso=0, dosis=dz, **V)
        b = OF.run(s, T=40000, plan=plan, pats=pats, chk=ch, ventana=8, **V)
        chk(f'(A1) s{s} flujo, retina 12, 40 estimulos, fotos, dosis={dz}: == organismo_flujo todas las claves',
            sin(a) == b and a['n_rep'] == 0, f"splits {a['splits']} celdas {a['celdas']} fotos {len(a['hist'])}")
    # (A2) ancla al TRONCO congelado: perillas v14.2, retina 6 == organismo_v142
    for s in (1, 2, 3):
        a = ORP.run(s, T=20000, **V); b = TR.run(s, T=20000)
        chk(f'(A2) s{s} == organismo_v142 en W, muertes, divisiones, celdas, mordidas, visitas',
            all(a[k] == b[k] for k in ('W', 'deaths', 'splits', 'celdas', 'mord', 'vis')), f"W {b['W']}")
    # (A3) la BASE del runner reproduce la serie ya registrada de subida_n8 (semilla 12601), medida por medida
    ok_sha = h16(SERIE_N8) == SHA_SERIE_N8
    d8 = json.load(open(SERIE_N8, encoding='utf-8'))
    r8 = [x for x in d8['resultados'] if x['brazo'] == 'base' and x['semilla'] == 12601][0]
    rc = CR.corre_uno((12601, 'base'))
    comunes = [k for k in r8 if k in rc and k not in ('dur_s',)]
    dist = [k for k in comunes if r8[k] != rc[k]]
    chk(f'(A3) BASE s12601 T 200000 == JSON de la serie de subida_n8 ({SHA_SERIE_N8}) en {len(comunes)} medidas comunes',
        ok_sha and not dist and len(comunes) >= 20, f"distintas {dist} RET40 {rc['RET40']}")
    # (B) el organo actua, cuenta bien y es determinista
    _, pats, _, plan = plan12(3, 40)
    ch = [MN.t_entrada(i) for i in range(1, 40)]
    run = lambda rp, dz: ORP.run(3, T=40000, plan=plan, pats=pats, chk=ch, ventana=8, repaso=rp, dosis=dz, **V)
    r0 = run(0, 1); rs = {(rp, dz): run(rp, dz) for rp, dz in ((1, 1), (1, 10), (2, 10), (3, 10))}
    for (rp, dz), r in rs.items():
        mord = r['mc_tot'] + r['mv_tot']
        chk(f'(B1) repaso={rp} dosis={dz}: repasa (n_rep {r["n_rep"]}) <= dosis x mordidas ({dz}x{mord}) y >= 90 %, + y - suman',
            0.9 * dz * mord <= r['n_rep'] <= dz * mord and r['n_rep_pos'] + r['n_rep_neg'] == r['n_rep'])
    chk('(B2) el organo cambia la vida (W final distinto de la base) en los 4 brazos',
        all(r['W'] != r0['W'] for r in rs.values()))
    chk('(B3) los 4 brazos con organo difieren entre si', len({json.dumps(r['W'], sort_keys=True) for r in rs.values()}) == 4)
    chk('(B4) determinismo: rep10 dos veces == identico', sin(run(1, 10)) == sin(rs[(1, 10)]) and run(1, 10)['n_rep'] == rs[(1, 10)]['n_rep'])
    fp = lambda r: r['n_rep_pos'] / max(r['n_rep'], 1)
    chk('(B5) BARAJ10 conserva la proporcion de objetivos positivos de REP10 (+-0.15)', abs(fp(rs[(2, 10)]) - fp(rs[(1, 10)])) <= 0.15,
        f"{fp(rs[(2, 10)]):.3f} vs {fp(rs[(1, 10)]):.3f}")
    # (F) estatico: el organo solo escribe Wp/Wn (y su memoria declarada); no toca rng, huellas, evidencia, via lenta ni energia
    src = open(os.path.join(AQUI, 'organismo_repaso.py'), encoding='utf-8').read()
    i = src.index('    def _repasa():'); j = src.index('    def _key(_k):')
    cuerpo = src[i:j]
    prohib = r'(?<![\w.])(mu|mup|mun|zp|zn|ncod|KW|activa|Wps|Wns|E|err|splits|_ord|objs|pos)\s*(\[[^\]]*\])?\s*[-+*/]?=(?!=)'
    chk('(F1) _repasa no asigna mu/mup/mun/zp/zn/ncod/KW/activa/Wps/Wns/E/err/splits', re.search(prohib, cuerpo) is None)
    chk('(F2) _repasa no llama al rng del organismo (solo _rngr)', re.search(r'(?<![\w_])rng\.', cuerpo) is None and '_rngr' in cuerpo)
    chk('(F3) el organo no lee valencias del mundo (val, R_VAL, objs)', re.search(r'(?<![\w_])(val|R_VAL|objs)\b', cuerpo) is None)
    nuevas = [l for l in src.splitlines() if '# n8c' in l]
    chk('(F4) toda linea nueva lleva la marca n8c y hay exactamente 4', len(nuevas) == 4, f'{len(nuevas)}')
    # (G) regla 14
    malos, filas = CR.entrada_campo_a_campo()
    chk(f'(G) regla 14: entrada campo a campo contra organismo_v142', not malos and len(filas) >= 100, f'{len(filas)} campos, {len(malos)} distintos')
    # (H) el runner ABORTA ante banderas desconocidas, abreviadas o combinaciones malas, sin escribir datos
    antes = listado()
    malos_cli = [['--humo', '--bogus'], ['--hum'], ['--humo', '--semila_humo', '15893'], [], ['--humo', '--pool', '6'],
                 ['--humo', '--semilla_humo', '15801'], ['--serie', 'base,rep10', '--desde', '12601', '--n', '20', '--pool', '6'],
                 ['--serie', 'base,xyz', '--desde', '15801', '--n', '20', '--pool', '6'],
                 ['--serie', 'base', '--desde', '15801', '--n', '5', '--pool', '6'], ['--serie', 'base', '--desde', '15801', '--n', '20'],
                 ['--humo', '--brazos_humo', 'base,base']]
    rcs = [corre_cli(a)[0] for a in malos_cli]
    chk(f'(H) {len(malos_cli)} invocaciones malas abortan (rc != 0) y no escriben nada en datos/', all(r != 0 for r in rcs) and listado() == antes,
        f'rc {rcs}')
    # (I) la letra sobre resultados sinteticos, y --veredicto imprime la letra en la ULTIMA linea
    def sint(ret_rep, adq_rep, ret_bj, ret_base=0.625, ret_sh=0.6):
        res = []
        for k, s in enumerate(range(1, 21)):
            e = 0.001 * k
            for b, ret, adq in (('base', ret_base + e, 0.40), ('rep1', ret_base + e, 0.40), ('rep10', ret_rep + e, adq_rep),
                                ('baraj10', ret_bj + e, 0.40), ('sinhue10', ret_sh + e, 0.40)):
                res.append(dict(semilla=s, brazo=b, RET40=ret, ADQ_tarde_com=adq, ADQ_tarde=0.66 + (adq - 0.40), muertes=370,
                                RET40_ven=0.95, RET40_rel=ret))
        return res
    casos = [('FUNCIONA', sint(0.80, 0.40, 0.60)), ('HAY ALGO MODESTO', sint(0.72, 0.30, 0.60)),
             ('NO (el repaso', sint(0.72, 0.40, 0.72)), ('NO SE LEE', sint(0.80, 0.40, 0.60, ret_base=0.45))]
    oks = []
    for letra, res in casos:
        ev = CR.predicciones(res); v = CR.veredicto(ev, ev)
        oks.append(v.startswith(letra))
    chk('(I1) la letra: FUNCIONA / HAY ALGO MODESTO / NO / NO SE LEE sobre sinteticos', all(oks), f'{oks}')
    tmp = tempfile.mkdtemp()
    rutas = []
    for nm in ('s.json', 'r.json'):
        p = os.path.join(tmp, nm)
        json.dump(dict(humo=False, shas={'organismo_repaso': CR.SHA_ORG}, resultados=casos[1][1]), open(p, 'w', encoding='utf-8'))
        rutas.append(p)
    rc, out = corre_cli(['--veredicto'] + rutas)
    ult = out.strip().splitlines()[-1] if out.strip() else ''
    chk('(I2) --veredicto: rc 0 y ultima linea "VEREDICTO: HAY ALGO MODESTO"', rc == 0 and ult == 'VEREDICTO: HAY ALGO MODESTO', ult)
    json.dump(dict(humo=True, shas={'organismo_repaso': CR.SHA_ORG}, resultados=casos[1][1]), open(rutas[0], 'w', encoding='utf-8'))
    rc, _ = corre_cli(['--veredicto'] + rutas)
    chk('(I3) --veredicto rechaza un JSON de humo', rc != 0)
    n = sum(R)
    fin = [f"TOTAL {n}/{len(R)} en {time.time() - t0:.1f}s", f"RESULTADO: {n}/{len(R)}"]
    for l in fin:
        print(l)
    open(os.path.join(AQUI, 'identidad_n8c_salida.txt'), 'w', encoding='utf-8').write(
        f"identidad_n8c  {time.strftime('%Y-%m-%d %H:%M:%S')}\n" + '\n'.join(LINEAS + fin) + '\n')


if __name__ == '__main__':
    main()
