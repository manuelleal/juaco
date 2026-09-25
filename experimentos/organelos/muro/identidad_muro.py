"""identidad_muro.py — ARNES del bloque MURO (antes de mirar numeros). Imprime N/N casos y sale con 1 si alguno falla.

MISION: llegar a la AGI por este camino.
(K) construye == disco; shas de los origenes; revisa_carro de los 8 carros
(A) cada carro del muro con PAGA = GLOT = TELEM = 0 == V143, salida ENTERA (N 9, fundador limpio, s 37908, T 2000)
(B) V143_MTEL (TELEM 1, PAGA = GLOT = 0) es solo lectura: todo igual a V143 salvo d['carro']['muro']
(C) regla 14: tarea de corre_muro == corre_v143.tarea campo a campo; corre_v143.tarea == juez.tarea (verifica_todo); P.run restaurado
(D) POR PIEZA (unidad sobre un carro vivo): GLOT veta lo SENTIDO bueno solo para la necesidad que no es la activa (con y sin meta),
    no mira cuanto, no veta lo que sirve a las dos, _adS vacio -> nada; GLOTFILA lee las filas (y con filas contaminadas veta lo que
    el cuerpo necesita); CTA / LIMPIA / SINEST / DESF / GLOTCTA (exploratorio v2) y MTEL solo lectura
(E) la pieza ACTUA en la pista (GLOT y GLOTFILA != V143 en T 3000) y no escribe en la pizarra
(G) determinismo (dos corridas iguales)
(F) nube-9: brazo invalido -> aborto atrapado + JSON; --reanuda lee el JSON existente; 1 aborto -> NO SE LEE
(H) ERR-115: banderas desconocidas/abreviadas abortan; la serie rechaza semillas/T/brazos fuera del preregistro
(V) la letra en casos sinteticos
    python experimentos/organelos/muro/identidad_muro.py
"""
import json, os, sys, tempfile, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_muro as CM
CV = CM.CV; P = CM.P; CB = CM.CB; RC = CM.RC

N = lambda x: json.loads(json.dumps(x, default=str))
casos = []


def caso(nombre, ok, extra=''):
    casos.append((nombre, bool(ok))); print(f"  [{'OK' if ok else 'FALLA'}] {nombre}{(' · ' + extra) if extra else ''}", flush=True)


def corre(mod, seed=37908, T=2000):
    return P.run(seed, [('C', mod)] * 9, T=T, fundador_limpio=1)


def main():
    t0 = time.time()
    print("== (K) construye y origenes")
    for n, b in CB.todas().items():
        ruta = os.path.join(CM.CARROS, n + '.py'); igual = os.path.exists(ruta) and open(ruta, 'rb').read() == b
        caso(f"K {n} construye == disco (sha {CB.h16b(b)})", igual)
        caso(f"K {n} revisa_carro PASA", not RC.revisa_fuente(b.decode('utf-8'), n))
    for ruta, sha in CM.SHAS.items(): caso(f"K sha {os.path.basename(ruta)} == {sha}", CM.h16(ruta) == sha)
    CM.registra()
    base = N(corre(CV.modulo('V143')))
    print("== (A) perillas en 0 == V143, salida ENTERA")
    for n in CM.PROPIOS:
        m = CV._MODS[n]; g = (m.PAGA, m.GLOT, m.PATAS, m.TELEM)
        try:
            m.PAGA = 0; m.GLOT = 0; m.PATAS = 0; m.TELEM = 0; x = N(corre(m))
        finally:
            m.PAGA, m.GLOT, m.PATAS, m.TELEM = g
        caso(f"A {n} con PAGA = GLOT = PATAS = TELEM = 0 == V143 (N 9, s 37908, T 2000, fundador limpio)", x == base)
    print("== (B) telemetria es solo lectura")
    x = N(corre(CV._MODS['V143_MTEL']))
    tiene = all('muro' in l['carro'] for l in x['linajes'])
    for l in x['linajes']: l['carro'].pop('muro', None)
    caso("B V143_MTEL: todo igual a V143 salvo d['carro']['muro']", tiene and x == base)
    print("== (C) regla 14")
    y1 = CM.tarea((37908, 'V143', 2000)); y2 = CV.tarea((37908, 'V143', 2000))
    tm = y1.pop('tel_muro')
    caso("C tarea(corre_muro) == corre_v143.tarea campo a campo (V143; salvo 'seg'; tel_muro = 9 None)",
         tm == [None] * 9 and N({k: v for k, v in y1.items() if k != 'seg'}) == N({k: v for k, v in y2.items() if k != 'seg'}))
    caso("C P.run restaurado tras tarea()", P.run.__name__ == 'run')
    caso("C corre_v143.verifica_todo con entrada (juez.tarea, identidad del juez y de v14.3)", CV.verifica_todo(lambda s: None, con_entrada=True))
    print("== (D) por pieza")
    ctx = lambda: dict(id='x', indice=0, n_linajes=9, T=1000, L=360, PAT=P.cfg_fabrica()['PAT'], rng=__import__('numpy').random.default_rng(1),
                       dote=0.6, rep_umbral=1.0, costo=0.001, costo_a=0.001, rep_X=500, cupo=16, ancho=8, fabrica=P.cfg_fabrica())
    V143SET = frozenset({'B', 'D'})   # lo que v14.3 veta con meta (en estas pruebas)
    FILAS = {'A': (1.0, 0.0), 'B': (-3.0, 0.0), 'C': (0.0, 1.0), 'D': (0.0, -3.0)}   # filas de valor (na 0 = energia, 1 = agua)
    def prep(nombre, E, Ag, na, meta, ads=True, filas=FILAS):
        m = CV._MODS[nombre]; c = m.crea(ctx())
        if ads: c._adS = {'A': [1.6, 0.0, 2], 'B': [-0.4, 0.0, 1], 'C': [0.0, 0.8, 1], 'D': [0.0, -0.4, 1]}   # lo SENTIDO por el linaje
        c._pg_lev = (E, Ag); c._v3m = meta
        c._v3o = V143SET if meta else frozenset()
        c._pg_prep(filas, na, meta)
        return c
    # --- PATAS (v4): el objetivo de las patas con meta
    import numpy as _np
    def see(nombre, na, meta, objs, pos=0, rech=None):
        m = CV._MODS[nombre]; c = m.crea(ctx()); c._na = na; c._v3m = meta; c._v3v = FILAS
        c._v3o = V143SET if meta else frozenset()
        if rech: c._rech.update(rech)
        return c._see(pos, objs, 0)
    objs = {5: 'C', 9: 'A', 300: 'B'}   # C a 5, A a 9, B a 60 (anillo 360)
    caso("D PATAS hambre con meta: va a A (sirve a la activa) aunque C este mas cerca; v14.3 va a C",
         see('V143_PATAS', 0, True, objs)[1] == 'A' and see('V143_MTEL', 0, True, objs)[1] == 'C')
    caso("D PATAS sed con meta: va a C", see('V143_PATAS', 1, True, objs)[1] == 'C')
    caso("D PATAS sin meta: v14.3 tal cual (el mas cercano)", see('V143_PATAS', 0, False, objs)[:2] == see('V143_MTEL', 0, False, objs)[:2])
    caso("D PATASDESF hambre con meta: va a C (sirve a la OTRA)", see('V143_PATASDESF', 0, True, {9: 'C', 5: 'A', 300: 'B'})[1] == 'C')
    caso("D PATASDESF sin nada que sirva a la otra: v14.3 tal cual", see('V143_PATASDESF', 0, True, {5: 'A', 300: 'B'})[:2] == see('V143_MTEL', 0, True, {5: 'A', 300: 'B'})[:2])
    caso("D PATAS con lo util en memoria de rechazo: cae al respaldo de v14.3 (no se queda sin objetivo)",
         see('V143_PATAS', 0, True, objs, rech={9: 10})[1] == see('V143_MTEL', 0, True, objs, rech={9: 10})[1])
    # --- GLOTU (v5): por NIVELES; U = rep_umbral del mundo (1.0)
    c = prep('V143_GLOTU', 1.3, 1.1, 0, True)
    caso("D GLOTU E 1.3 > Ag 1.1, E >= U: veta A (solo sube E, la mas llena y ya sobre el umbral); C no", 'A' in c._pgv and 'C' not in c._pgv)
    c = prep('V143_GLOTU', 0.9, 0.5, 1, True)
    caso("D GLOTU E 0.9 > Ag 0.5 pero E < U: NO veta A (aun le hace falta para la ventana)", 'A' not in c._pgv)
    c = prep('V143_GLOTU', 1.1, 1.3, 0, False)
    caso("D GLOTU Ag 1.3 > E 1.1 >= U: veta C y no A (mide niveles, no el deficit recortado que da na 0)", 'C' in c._pgv and 'A' not in c._pgv)
    c = prep('V143_GLOTU', 1.3, 1.1, 0, True, ads=False)
    caso("D GLOTU con _adS vacio: no veta lo bueno (solo lo de v14.3)", c._pgv == V143SET)
    c = prep('V143_GLOTUINV', 1.3, 1.1, 0, True)
    caso("D GLOTUINV (control al reves) E 1.3 > Ag 1.1 >= U: veta C (la menos llena) y no A", 'C' in c._pgv and 'A' not in c._pgv)
    # --- GLOT (exploratorio v3)
    c = prep('V143_GLOT', 0.3, 0.9, 0, True)
    caso("D GLOT hambre (na 0), con meta: veta C (sentida buena SOLO para el agua, que no es la activa) ademas de lo de v14.3",
         c._pg_glot == {'C'} and c._pgv == V143SET | {'C'})
    c = prep('V143_GLOT', 0.3, 0.9, 0, False)
    caso("D GLOT hambre, sin meta: veta C y nada mas (no toca lo malo)", c._pgv == {'C'})
    c = prep('V143_GLOT', 0.9, 0.3, 1, False)
    caso("D GLOT sed (na 1): veta A (solo sirve a la energia)", c._pgv == {'A'})
    c = prep('V143_GLOT', 0.3, 0.9, 0, False, ads=False)
    caso("D GLOT con _adS vacio (nada sentido): no veta nada (== v14.3)", c._pgv == frozenset())
    c = prep('V143_GLOT', 0.3, 0.9, 0, False)
    c2 = prep('V143_GLOT', 0.5, 0.52, 0, False)
    caso("D GLOT no mira CUANTO falta, solo CUAL (mismo veto con Ag 0.9 que con Ag 0.52)", c._pgv == c2._pgv == {'C'})
    c = prep('V143_GLOT', 0.3, 0.9, 0, False)
    c._adS['E'] = [0.4, 0.4, 1]
    c._pg_prep(FILAS, 0, False)
    caso("D GLOT: una letra que sirve a las DOS necesidades no se veta", 'E' not in c._pgv)
    # --- GLOTFILA (control por filas)
    c = prep('V143_GLOTFILA', 0.3, 0.9, 0, False, ads=False)
    caso("D GLOTFILA hambre: veta C leyendo las FILAS aunque el linaje no haya sentido nada", c._pgv == {'C'})
    filas2 = dict(FILAS); filas2['A'] = (-0.2, 0.3)   # filas contaminadas por generalizacion: A parece mala-para-E y buena-para-agua
    c = prep('V143_GLOTFILA', 0.3, 0.9, 0, False, filas=filas2)
    c2 = prep('V143_GLOT', 0.3, 0.9, 0, False, filas=filas2)
    caso("D GLOTFILA con filas contaminadas veta A (lo que el cuerpo necesita); GLOT (lo sentido) no", 'A' in c._pgv and 'A' not in c2._pgv)
    # --- CTA y familia (exploratorio v2, refutado; se conserva el arnes de la pieza)
    c = prep('V143_CTA', 0.3, 0.9, 0, False)
    caso("D CTA sin meta, hambre, Ag sobra: act {B}, otra {D} pagable -> boca veta {B}",
         c._pg_act == {'B'} and c._pg_otra == {'D'} and c._pgv == {'B'})
    c = prep('V143_CTA', 0.3, 0.6, 0, False)
    caso("D CTA sin meta, Ag no sobra: veta {B, D}", c._pgv == {'B', 'D'})
    c = prep('V143_CTA', 0.3, 0.6, 0, True)
    caso("D CTA con meta: v14.3 tal cual", c._pgv == V143SET)
    c = prep('V143_LIMPIA', 0.3, 0.9, 0, True)
    caso("D LIMPIA con meta: libera la otra pagable (D) -> veta {B}", c._pgv == {'B'})
    c = prep('V143_SINEST', 0.3, 0.9, 0, False)
    caso("D SINEST sin meta: veta {B, D}", c._pgv == {'B', 'D'})
    c = prep('V143_DESF', 0.3, 0.9, 0, False)
    caso("D DESF sin meta, hambre: veta {D}, deja B", c._pgv == {'D'})
    c = prep('V143_GLOTCTA', 0.3, 0.9, 0, False)
    caso("D GLOTCTA sin meta, hambre: veta {B} (CTA) y {C} (GLOT)", c._pgv == {'B', 'C'})
    c = prep('V143_MTEL', 0.3, 0.6, 0, False)
    caso("D MTEL (PAGA = GLOT = 0): calcula los conjuntos y el veto es _v3o (no toca nada)", c._pg_act == {'B'} and c._pg_glot == {'C'} and c._pgv == frozenset())
    print("== (E) la pieza actua en la pista")
    b3 = N(corre(CV.modulo('V143'), T=3000)); mb = [l['mord'] for l in b3['linajes']]
    x4 = N(corre(CV._MODS['V143_PATAS'], T=3000)); x5 = N(corre(CV._MODS['V143_PATASDESF'], T=3000))
    # (corregido ANTES del humo) el caso exigia PATAS != V143 en T 3000; en s37908 PATAS es fisicamente == V143 hasta T 3000 (las filas
    # generalizan: la buena de la otra necesidad suele tener valor > 0 tambien en la fila activa, y el objetivo no cambia). Se informa.
    caso("E PATASDESF != V143 y != PATAS en la fisica (s 37908, T 3000); PATAS == V143 en T 3000 se INFORMA",
         [l['mord'] for l in x5['linajes']] != mb and [l['mord'] for l in x5['linajes']] != [l['mord'] for l in x4['linajes']],
         f"PATAS == V143 en la fisica a T 3000: {[l['mord'] for l in x4['linajes']] == mb}")
    x6 = N(corre(CV._MODS['V143_GLOTU'], T=3000)); x7 = N(corre(CV._MODS['V143_GLOTUINV'], T=3000))
    caso("E GLOTU (candidato) != V143 y GLOTUINV (control) != V143 y != GLOTU en la fisica (s 37908, T 3000)",
         [l['mord'] for l in x6['linajes']] != mb and [l['mord'] for l in x7['linajes']] != mb and [l['mord'] for l in x7['linajes']] != [l['mord'] for l in x6['linajes']])
    tg = [l['carro']['muro'] for l in x6['linajes']]; tk = [l['carro']['muro'] for l in x7['linajes']]
    caso("E GLOTU y GLOTUINV vetan (telemetria de la ultima instancia) y no escriben en la pizarra",
         sum(t['veto_glot'] for t in tg) > 0 and sum(t['veto_glot'] for t in tk) > 0 and x6['pista']['pizarra_n'] == 0 and x7['pista']['pizarra_n'] == 0,
         f"veto_glot GLOTU {sum(t['veto_glot'] for t in tg)} · GLOTUINV {sum(t['veto_glot'] for t in tk)}")
    tp = [l['carro']['muro'] for l in x4['linajes']]
    caso("E PATAS telemetria: la pieza decide el objetivo en pasos con meta", all(t['patas'] == 1 for t in tp) and sum(t['patas_meta'] for t in tp) > 0,
         str(sum(t['patas_meta'] for t in tp)))
    caso("E PATAS no escribe en la pizarra", x4['pista']['pizarra_n'] == 0 and x4['pista']['escrituras_descartadas'] == 0)
    x2 = N(corre(CV._MODS['V143_GLOT'], T=3000)); x3 = N(corre(CV._MODS['V143_GLOTFILA'], T=3000))
    caso("E GLOT != V143 en la fisica (s 37908, T 3000)", [l['mord'] for l in x2['linajes']] != mb)
    caso("E GLOTFILA != V143 y != GLOT en la fisica", [l['mord'] for l in x3['linajes']] != mb and [l['mord'] for l in x3['linajes']] != [l['mord'] for l in x2['linajes']])
    caso("E GLOT y GLOTFILA no escriben en la pizarra", all(x['pista']['pizarra_n'] == 0 and x['pista']['escrituras_descartadas'] == 0 for x in (x2, x3)))
    tv = [l['carro']['muro'] for l in x2['linajes']]
    caso("E GLOT telemetria presente en los 9 linajes (ultima instancia) y veta", all(t and t['glot'] == 1 for t in tv) and sum(t['veto_glot'] for t in tv) > 0,
         str({k: sum(t[k] for t in tv) for k in ('veto_glot', 'mord_solo_otra')}))
    print("== (G) determinismo")
    caso("G candidato dos corridas iguales (s 37909, T 2000)", N(corre(CV._MODS[CM.BRAZOS[CM.CAND]], 37909)) == N(corre(CV._MODS[CM.BRAZOS[CM.CAND]], 37909)))
    print("== (F) nube-9 y --reanuda")
    with tempfile.TemporaryDirectory() as d:
        CM.BRAZOS['_malo'] = 'NO_EXISTE'
        try:
            r = CM.trabajo((37908, '_malo', 100, d, False))
        finally:
            CM.BRAZOS.pop('_malo', None)
        caso("F brazo invalido: aborto atrapado y JSON escrito", bool(r['aborto']) and os.path.exists(os.path.join(d, '_malo_s37908.json')))
        with open(os.path.join(d, 'glot_s37908.json'), 'w', encoding='utf-8') as fh: json.dump(dict(seed=37908, brazo='glot', aborto=None, linajes=[], marca=7), fh)
        r2 = CM.trabajo((37908, 'glot', 100, d, True))
        caso("F --reanuda lee el JSON existente (no corre)", r2.get('marca') == 7)
    L = CM.lee_serie({}, {}, {}, True, 1)
    caso("F 1 aborto -> NO SE LEE", L['veredicto'] == 'NO SE LEE')
    print("== (H) ERR-115")
    malos = [['--hum'], ['--serie', '--des', '37001'], ['--humo', '--xx'], ['--serie', '--desde', '37001', '--n', '20', '--poo', '6'],
             ['--humo', '--pool', '6'], ['--serie', '--desde', '36001', '--n', '20'], ['--serie', '--desde', '37001', '--n', '20', '--T', '50000'],
             ['--serie', '--desde', '37001', '--n', '20', '--brazos', 'v143,glot'], ['--humo', '--desde', '37001'], ['--humo', '--T', '100000']]
    for m_ in malos:
        try:
            CM.main(m_); ok = False
        except SystemExit:
            ok = True
        caso(f"H {' '.join(m_)} -> aborta", ok)
    print("== (V) letra")
    C_, K_ = CM.CAND, CM.CTRL
    def res(o1=True, v=0.6, cand=False, ctrl=False):
        b = lambda g, r: dict(gana_e5=g, R0_real_med=r, coherente='180/180')
        return {'v143': b(False, v), C_: b(cand, 0.9), K_: b(ctrl, 0.5), 'o1': b(o1, 0.94)}
    tmok = {C_: dict(veto_glot=5), K_: dict(veto_glot=9)}
    pr = lambda gc, dc, gk: {(C_, 'v143'): dict(semillas=20, gana=gc, dif_med=dc), (C_, K_): dict(semillas=20, gana=gk, dif_med=0.1)}
    caso("V FUNCIONA: cruza, gana 15/20, control no cruza", CM.lee_serie(res(cand=True), pr(15, 0.2, 15), tmok, True, 0)['veredicto'] == 'FUNCIONA')
    caso("V NO: control tambien cruza (P3 cae) y candidato gana -> MODESTO si dif >= 0.10 y gana al control > 10/20",
         CM.lee_serie(res(cand=True, ctrl=True), pr(16, 0.15, 12), tmok, True, 0)['veredicto'] == 'HAY ALGO MODESTO')
    caso("V MODESTO: no cruza, gana 15/20 con dif 0.10, gana al control 11/20", CM.lee_serie(res(), pr(15, 0.10, 11), tmok, True, 0)['veredicto'] == 'HAY ALGO MODESTO')
    caso("V NO: gana 14/20", CM.lee_serie(res(), pr(14, 0.3, 20), tmok, True, 0)['veredicto'] == 'NO')
    caso("V NO: gana 15/20 con dif 0.09", CM.lee_serie(res(), pr(15, 0.09, 20), tmok, True, 0)['veredicto'] == 'NO')
    caso("V NO: gana 15/20, dif 0.2, pero empata al control 10/20", CM.lee_serie(res(), pr(15, 0.2, 10), tmok, True, 0)['veredicto'] == 'NO')
    caso("V NO SE LEE: O1 no gana", CM.lee_serie(res(o1=False, cand=True), pr(20, 0.3, 20), tmok, True, 0)['veredicto'] == 'NO SE LEE')
    caso("V NO SE LEE: V143 fuera de [0.40, 0.80]", CM.lee_serie(res(v=0.3, cand=True), pr(20, 0.3, 20), tmok, True, 0)['veredicto'] == 'NO SE LEE')
    caso("V NO SE LEE: la pieza no actua (V4)", CM.lee_serie(res(cand=True), pr(20, 0.3, 20), {C_: dict(veto_glot=0), K_: dict(veto_glot=0)}, True, 0)['veredicto'] == 'NO SE LEE')
    caso("V bloque: FUNCIONA + MODESTO -> MODESTO; NO SE LEE manda", CM.bloque('FUNCIONA', 'HAY ALGO MODESTO') == 'HAY ALGO MODESTO' and CM.bloque('FUNCIONA', 'NO SE LEE') == 'NO SE LEE')
    n_ok = sum(ok for _, ok in casos)
    print(f"\nARNES MURO: {n_ok}/{len(casos)} · {time.time()-t0:.0f} s")
    return 0 if n_ok == len(casos) else 1


if __name__ == '__main__':
    sys.exit(main())
