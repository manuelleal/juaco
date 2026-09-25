"""identidad_muro2.py — ARNES del SEGUNDO intento del muro (GLOTU + PATAS). N/N; sale con 1 si algo falla. Antes de mirar numeros.

MISION: llegar a la AGI por este camino.
(K) instrumentos de la serie 1 intactos (corre_muro.py, construye_muro.py); construye_muro2 == disco; revisa_carro; shas de origen
(A) candidato y control con PAGA = GLOT = PATAS = TELEM = 0 == V143, salida ENTERA (N 9, fundador limpio, s 37913, T 2000)
(S) la configuracion en memoria: brazos, candidato, control, semillas, humo, carpeta; y corre_muro vuelve a su config al re-importarse
(C) regla 14: tarea == corre_v143.tarea campo a campo; corre_v143.verifica_todo con entrada; P.run restaurado
(D) por pieza: el candidato = GLOTU (boca) + PATAS (patas a lo que sirve a la ACTIVA); el control = GLOTU + patas a lo que sirve a la
    OTRA; las dos piezas actuan en decisiones distintas (la boca no cambia las patas y viceversa)
(E) actuan en la pista; (G) determinismo; (F) nube-9 y --reanuda; (H) ERR-115 con las semillas nuevas; (V) la letra con los brazos nuevos
    python experimentos/organelos/muro/identidad_muro2.py
"""
import importlib, json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_muro2 as CM2
CM = CM2.CM; CV = CM.CV; P = CM.P; RC = CM.RC; CB = CM.CB; CB2 = CM2.CB2

N = lambda x: json.loads(json.dumps(x, default=str))
casos = []


def caso(nombre, ok, extra=''):
    casos.append((nombre, bool(ok))); print(f"  [{'OK' if ok else 'FALLA'}] {nombre}{(' · ' + extra) if extra else ''}", flush=True)


def corre(mod, seed=37913, T=2000):
    return P.run(seed, [('C', mod)] * 9, T=T, fundador_limpio=1)


def main():
    t0 = time.time()
    print("== (K) instrumentos")
    caso("K corre_muro.py intacto (503b531ea1213c59, el de la serie 1)", CM.h16(CM.__file__) == CM2.SHA_CORRE_MURO)
    caso("K construye_muro.py intacto (ad607c6ad4f9ced9)", CB.h16(CB.__file__) == CB2.SHA_CONSTRUYE_MURO)
    for n, b in list(CB.todas().items()) + list(CB2.todas2().items()):
        if n not in ('V143_GLOTUPATAS', 'V143_GLOTUPATASDESF', 'V143_MTEL'): continue
        ruta = os.path.join(CM.CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        caso(f"K {n} construye == disco (sha {CB.h16b(b)})", igual)
        caso(f"K {n} revisa_carro PASA", not RC.revisa_fuente(b.decode('utf-8'), n))
    for ruta, sha in CM.SHAS.items(): caso(f"K sha {os.path.basename(ruta)} == {sha}", CM.h16(ruta) == sha)
    CM.registra()
    base = N(corre(CV.modulo('V143')))
    print("== (A) perillas en 0 == V143")
    for n in ('V143_GLOTUPATAS', 'V143_GLOTUPATASDESF'):
        m = CV._MODS[n]; g = (m.PAGA, m.GLOT, m.PATAS, m.TELEM)
        caso(f"A {n} perillas de fabrica {g}", g == ((0, 3, 1, 1) if n == 'V143_GLOTUPATAS' else (0, 3, 2, 1)))
        try:
            m.PAGA = 0; m.GLOT = 0; m.PATAS = 0; m.TELEM = 0; x = N(corre(m))
        finally:
            m.PAGA, m.GLOT, m.PATAS, m.TELEM = g
        caso(f"A {n} con PAGA = GLOT = PATAS = TELEM = 0 == V143 (salida ENTERA)", x == base)
    print("== (S) configuracion del segundo intento")
    caso("S brazos de la serie", CM.SERIE_BRAZOS == ('v143', 'glotupatas', 'glotupatasdesf', 'o1'))
    caso("S candidato / control", (CM.CAND, CM.CTRL) == ('glotupatas', 'glotupatasdesf'))
    caso("S semillas: serie 37101-37120, replica 37121-37140, sin choque con la serie 1 (37001-37040) ni con la practica",
         list(CM.SERIE) == list(range(37101, 37121)) and list(CM.REPLICA) == list(range(37121, 37141))
         and not (set(CM.SERIE) | set(CM.REPLICA)) & set(range(37001, 37041)) and not (set(CM.SERIE) | set(CM.REPLICA)) & set(CM.PRACTICA))
    caso("S datos en muro/datos/muro2", CM.DATOS == os.path.join(AQUI, 'datos', 'muro2'))
    caso("S humo: 6 corridas de practica", len(CM.HUMO) == 6 and all(s in CM.PRACTICA for s, _ in CM.HUMO))
    caso("S verifica = verifica2 (incluye el carro nuevo)", CM.verifica is CM2.verifica2)
    spec = importlib.util.spec_from_file_location('corre_muro_fresco', CM.__file__); f = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(f)
    caso("S corre_muro recien importado conserva la config de la serie 1 (glotu / glotuinv, 37001-37040)",
         (f.CAND, f.CTRL, f.SERIE_BRAZOS, list(f.SERIE)[0]) == ('glotu', 'glotuinv', ('v143', 'glotu', 'glotuinv', 'o1'), 37001))
    ok_v = CM.verifica(lambda s: None)
    caso("S verifica2 pasa (shas, carros, identidades cortas)", ok_v)
    print("== (C) regla 14")
    y1 = CM.tarea((37913, 'V143', 2000)); y2 = CV.tarea((37913, 'V143', 2000)); tm = y1.pop('tel_muro')
    caso("C tarea == corre_v143.tarea campo a campo (V143, s 37913, T 2000; salvo 'seg')",
         tm == [None] * 9 and N({k: v for k, v in y1.items() if k != 'seg'}) == N({k: v for k, v in y2.items() if k != 'seg'}))
    caso("C P.run restaurado", P.run.__name__ == 'run')
    caso("C corre_v143.verifica_todo con entrada", CV.verifica_todo(lambda s: None, con_entrada=True))
    print("== (D) por pieza")
    ctx = lambda: dict(id='x', indice=0, n_linajes=9, T=1000, L=360, PAT=P.cfg_fabrica()['PAT'], rng=__import__('numpy').random.default_rng(1),
                       dote=0.6, rep_umbral=1.0, costo=0.001, costo_a=0.001, rep_X=500, cupo=16, ancho=8, fabrica=P.cfg_fabrica())
    FILAS = {'A': (1.0, 0.0), 'B': (-3.0, 0.0), 'C': (0.0, 1.0), 'D': (0.0, -3.0)}
    def carro(n, na, meta, E=0.5, Ag=0.5):
        c = CV._MODS[n].crea(ctx()); c._na = na; c._v3m = meta; c._v3v = FILAS; c._v3o = frozenset({'B', 'D'}) if meta else frozenset()
        c._adS = {'A': [1.6, 0.0, 2], 'B': [-0.4, 0.0, 1], 'C': [0.0, 0.8, 1], 'D': [0.0, -0.4, 1]}; c._pg_lev = (E, Ag)
        return c
    objs = {5: 'C', 9: 'A', 300: 'B'}
    caso("D candidato: con meta y hambre las patas van a A (la activa) aunque C este mas cerca", carro('V143_GLOTUPATAS', 0, True)._see(0, objs, 0)[1] == 'A')
    caso("D control: con meta y hambre las patas van a C (la otra)", carro('V143_GLOTUPATASDESF', 0, True)._see(0, {9: 'C', 5: 'A', 300: 'B'}, 0)[1] == 'C')
    caso("D sin meta: candidato y control van a lo mas cercano (v14.3)",
         carro('V143_GLOTUPATAS', 0, False)._see(0, objs, 0)[1] == carro('V143_GLOTUPATASDESF', 0, False)._see(0, objs, 0)[1] == 'C')
    for n in ('V143_GLOTUPATAS', 'V143_GLOTUPATASDESF'):
        c = carro(n, 0, True, E=1.3, Ag=1.1); c._v3o = frozenset({'B', 'D'}); c._pg_prep(FILAS, 0, True)
        caso(f"D {n}: la boca es GLOTU (E 1.3 > Ag 1.1 >= U: veta A, no C)", 'A' in c._pgv and 'C' not in c._pgv)
    c1 = carro('V143_GLOTUPATAS', 0, True, E=1.3, Ag=1.1); d0 = c1._see(0, objs, 0); c1._pg_prep(FILAS, 0, True); d1 = c1._see(0, objs, 0)
    caso("D decisiones distintas: el veto de la boca (GLOTU) no cambia el objetivo de las patas", d0 == d1)
    print("== (E) actuan en la pista")
    mb = [l['mord'] for l in N(corre(CV.modulo('V143'), T=3000))['linajes']]
    x1 = N(corre(CV._MODS['V143_GLOTUPATAS'], T=3000)); x2 = N(corre(CV._MODS['V143_GLOTUPATASDESF'], T=3000))
    caso("E candidato != V143, control != V143, candidato != control en la fisica (s 37913, T 3000)",
         [l['mord'] for l in x1['linajes']] != mb and [l['mord'] for l in x2['linajes']] != mb
         and [l['mord'] for l in x1['linajes']] != [l['mord'] for l in x2['linajes']])
    for nom, x in (('candidato', x1), ('control', x2)):
        t = [l['carro']['muro'] for l in x['linajes']]
        caso(f"E {nom}: las dos piezas actuan (veto_glot > 0 y patas_meta > 0) y no escribe en la pizarra",
             sum(z['veto_glot'] for z in t) > 0 and sum(z['patas_meta'] for z in t) > 0 and x['pista']['pizarra_n'] == 0,
             f"veto_glot {sum(z['veto_glot'] for z in t)} · patas_meta {sum(z['patas_meta'] for z in t)}")
    caso("E V4 de la letra (pieza) verdadera para candidato y control", CM.pieza(CM.tm_suma([dict(tel_muro=[l['carro']['muro'] for l in x1['linajes']])]))
         and CM.pieza(CM.tm_suma([dict(tel_muro=[l['carro']['muro'] for l in x2['linajes']])])))
    print("== (G) determinismo")
    caso("G candidato dos corridas iguales (s 37914, T 2000)", N(corre(CV._MODS['V143_GLOTUPATAS'], 37914)) == N(corre(CV._MODS['V143_GLOTUPATAS'], 37914)))
    print("== (F) nube-9 y --reanuda")
    with tempfile.TemporaryDirectory() as d:
        CM.BRAZOS['_malo'] = 'NO_EXISTE'
        try:
            r = CM.trabajo((37913, '_malo', 100, d, False))
        finally:
            CM.BRAZOS.pop('_malo', None)
        caso("F brazo invalido: aborto atrapado y JSON escrito", bool(r['aborto']) and os.path.exists(os.path.join(d, '_malo_s37913.json')))
        with open(os.path.join(d, 'glotupatas_s37913.json'), 'w', encoding='utf-8') as fh: json.dump(dict(seed=37913, brazo='glotupatas', aborto=None, linajes=[], marca=7), fh)
        caso("F --reanuda lee el JSON existente", CM.trabajo((37913, 'glotupatas', 100, d, True)).get('marca') == 7)
    caso("F 1 aborto -> NO SE LEE", CM.lee_serie({}, {}, {}, True, 1)['veredicto'] == 'NO SE LEE')
    print("== (H) ERR-115 y semillas")
    malos = [['--hum'], ['--serie', '--des', '37101'], ['--humo', '--xx'], ['--humo', '--pool', '6'],
             ['--serie', '--desde', '37001', '--n', '20'], ['--serie', '--desde', '37111', '--n', '20'],
             ['--serie', '--desde', '37101', '--n', '20', '--T', '50000'], ['--serie', '--desde', '37101', '--n', '20', '--brazos', 'v143,glotu,glotuinv,o1'],
             ['--humo', '--desde', '37101'], ['--humo', '--T', '100000']]
    for m_ in malos:
        try:
            CM.main(m_); ok = False
        except SystemExit:
            ok = True
        caso(f"H {' '.join(m_)} -> aborta", ok)
    for m_ in (['1', 'glotupatas'], ['37906', 'glotupatas'], ['37901', 'nada'], ['37901']):
        try:
            CM2.explora(m_); ok = False
        except SystemExit:
            ok = True
        caso(f"H --explora {' '.join(m_)} -> aborta", ok)
    print("== (V) letra (la de corre_muro, con los brazos nuevos)")
    C_, K_ = CM.CAND, CM.CTRL
    def res(o1=True, v=0.6, cand=False, ctrl=False):
        b = lambda g, r: dict(gana_e5=g, R0_real_med=r, coherente='180/180')
        return {'v143': b(False, v), C_: b(cand, 0.9), K_: b(ctrl, 0.5), 'o1': b(o1, 0.94)}
    tmok = {C_: dict(veto_glot=5, patas_meta=9), K_: dict(veto_glot=9, patas_meta=9)}
    pr = lambda gc, dc, gk: {(C_, 'v143'): dict(semillas=20, gana=gc, dif_med=dc), (C_, K_): dict(semillas=20, gana=gk, dif_med=0.1)}
    L = CM.lee_serie
    caso("V FUNCIONA", L(res(cand=True), pr(15, 0.2, 15), tmok, True, 0)['veredicto'] == 'FUNCIONA')
    caso("V control tambien cruza -> MODESTO si gana 16/20 dif 0.15 y al control 12/20", L(res(cand=True, ctrl=True), pr(16, 0.15, 12), tmok, True, 0)['veredicto'] == 'HAY ALGO MODESTO')
    caso("V MODESTO: gana 15/20, dif 0.10, al control 11/20", L(res(), pr(15, 0.10, 11), tmok, True, 0)['veredicto'] == 'HAY ALGO MODESTO')
    caso("V NO: gana 14/20", L(res(), pr(14, 0.3, 20), tmok, True, 0)['veredicto'] == 'NO')
    caso("V NO: dif 0.09", L(res(), pr(15, 0.09, 20), tmok, True, 0)['veredicto'] == 'NO')
    caso("V NO: empata al control 10/20", L(res(), pr(15, 0.2, 10), tmok, True, 0)['veredicto'] == 'NO')
    caso("V NO SE LEE: O1 no gana", L(res(o1=False, cand=True), pr(20, 0.3, 20), tmok, True, 0)['veredicto'] == 'NO SE LEE')
    caso("V NO SE LEE: V143 fuera de [0.40, 0.80]", L(res(v=0.85, cand=True), pr(20, 0.3, 20), tmok, True, 0)['veredicto'] == 'NO SE LEE')
    caso("V NO SE LEE: la pieza no actua", L(res(cand=True), pr(20, 0.3, 20), {C_: {}, K_: {}}, True, 0)['veredicto'] == 'NO SE LEE')
    caso("V bloque: FUNCIONA + NO -> NO", CM.bloque('FUNCIONA', 'NO') == 'NO')
    n_ok = sum(ok for _, ok in casos)
    print(f"\nARNES MURO2: {n_ok}/{len(casos)} · {time.time()-t0:.0f} s")
    return 0 if n_ok == len(casos) else 1


if __name__ == '__main__':
    sys.exit(main())
