"""identidad_muro_perillas.py — ARNES DE IDENTIDAD BIT A BIT del carro O1_MURO_GEN (perillas del muro), ANTES de mirar numeros.

MISION: llegar a la AGI por este camino.
Salida ENTERA de pista.run (N 9, fundador limpio 1, pizarra 1, escala 1), normalizada por json:
  (K) shas fijados, carros == construye, chequeo estatico, constantes de fabrica == literales del modulo O1.
  (C) GEN0 == O1 · GEN dosis (1,..,1) sin mutacion == O1 (con y sin camara) · GEN con LIMPIA 0 (resto 1) == CTRL_O1_SINLIMPIA (la
      referencia existente) · NEUTRO (PS_LEE 0, sigma/delta de la serie, camara) == O1 aunque sus genes se muevan · cableado de cada
      gen continuo: dosis 0 == O1 con la constante reescrita a mano al valor APAGADO · HUECO 0 == O1 con `tgt = pos` escrito a mano ·
      controles que DEBEN diferir: todo apagado != O1 y cada gen apagado solo != O1 (si uno no difiere a T 12000, se dice: gen inerte).
  (R) regla 14: corre_muro_perillas.tarea con dosis de fabrica == corre_v143.tarea('O1') campo a campo (linajes y pista).
  (G) generador propio y primer fundador desde la base.
  (F) la letra de la serie (lee_serie) sobre casos sinteticos (solo si GEN_LETRA esta fijado).
    python experimentos/organelos/muro_perillas/identidad_muro_perillas.py
"""
import importlib.util, json, math, os, sys, time, types

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'experimentos', 'tronco_v14_3'), os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')]
import corre_muro_perillas as R
import construye_muro_perillas as CB
CV = R.CV; P = R.P; J = R.J
import revisa_carro as RC

N = lambda x: json.loads(json.dumps(x, default=str))
OK = []


def ok(cond, txt):
    OK.append(bool(cond)); print(f"  {'OK   ' if cond else 'FALLA'} {txt}", flush=True)


def carga_texto(nombre, txt):
    spec = importlib.util.spec_from_loader(nombre, loader=None); m = importlib.util.module_from_spec(spec)
    exec(compile(txt, nombre, 'exec'), m.__dict__)   # arnes: texto de O1 con UNA constante reescrita a mano
    return m


def run(mod, seed, T):
    return N(P.run(seed, [('X', mod)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1))


def con(m, siembra, sigma, delta, lee, camara, seed, T):
    try:
        R._pon(m, siembra, seed, sigma, delta, lee, camara)
        return run(m, seed, T)
    finally:
        R._quita(m)


def main():
    t0 = time.time(); print("ARNES identidad_muro_perillas.py")
    log = lambda s: print('     ' + s)
    ok(R.verifica(log), "(K) verifica(): shas fijados (pista, juez, O1, CTRL_O1_SINLIMPIA, corre_v143), carros == construye")
    for n in ('O1_MURO_GEN', 'O1_MURO_GEN0'):
        v = RC.revisa_fuente(open(R.CARROS[n], encoding='utf-8').read(), n); ok(not v, f"(K) chequeo estatico revisa_carro {n}: {'PASA' if not v else v[:2]}")
    o1 = CV.modulo('O1'); sl = P.carga_carro('CTRL_O1_SINLIMPIA')
    ok((o1.MARGEN, o1.PRUEBA, o1.PEN_OTRO, o1.PISO) == CB.FABRICA[:4] and CB.FABRICA[4:] == (1.0, 1.0) and CB.BASE == (CB.ARRANQUE_MARGEN,) + CB.FABRICA[1:] and CB.DISENO == CB.FABRICA
       and R.genoma('off') == dict(zip(CB.GENES, CB.APAGADO)) and R.genoma('base') == dict(zip(CB.GENES, CB.BASE)) and R.genoma('off+MARGEN=0.25')['PISO'] == CB.APAGADO[3] and R.genoma('off+MARGEN=0.25')['MARGEN'] == 0.25
       and all(lo <= v <= hi for v, (lo, hi) in zip(CB.FABRICA, CB.CLIP)) and all(lo <= v <= hi for v, (lo, hi) in zip(CB.APAGADO, CB.CLIP)),
       f"(K) constantes: FABRICA {CB.FABRICA} == literales de O1 + (1, 1); BASE = (ARRANQUE {CB.ARRANQUE_MARGEN}, resto fabrica) {CB.BASE}; 'off' = APAGADO {CB.APAGADO}, 'off+X' sobre APAGADO, 'base+X' sobre BASE; dentro del clip; sigma {CB.SIGMA} delta {CB.DELTA}")
    R.fija(); m = CV._MODS[R.CARRO]
    spec = importlib.util.spec_from_file_location('carro_O1_MURO_GEN0', R.CARROS['O1_MURO_GEN0']); m0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(m0)
    s = R.BASES['arnes']; T = 3000
    ro = run(o1, s, T); rs = run(sl, s, T)
    ok(run(m0, s, T) == ro, f"(C) GEN0 == O1 (salida ENTERA, s {s}, T {T})")
    D = dict(zip(CB.GENES, CB.DISENO)); B = dict(zip(CB.GENES, CB.BASE))
    ok(con(m, [dict(D)], 0.0, 0.0, 1, 0, s, T) == ro and con(m, [dict(D)], 0.0, 0.0, 1, 1, s, T) == ro,
       "(C) GEN con los genes de FABRICA, sin mutacion == O1 (salida ENTERA), con camara y sin camara")
    try:
        R._pon(m, None, s, 0.0, 0.0, 1, 0, [list(CB.FABRICA)] * 9); rm = run(m, s, T)
        fp = [q for v in m._TEL.values() for q in v.get('fund', [])]
        ok(rm == ro and fp and all(q[0] == 3 for q in fp), f"(C) PISTA MIXTA: PS_POR_LINAJE con 9 x FABRICA == O1 (salida ENTERA); {len(fp)} fundadores, todos de origen 3 (por linaje)")
        R._pon(m, None, s, 0.0, 0.0, 1, 0, [list(CB.FABRICA)] * 8 + [list(dict(zip(CB.GENES, CB.FABRICA), LIMPIA=0.0).values())]); rm2 = run(m, s, T)
        ok(rm2 != ro and rm2['linajes'][:8] != ro['linajes'][:8], "(C) PISTA MIXTA: 8 x FABRICA + 1 con LIMPIA 0 != O1 (el genoma por linaje actua y los vecinos lo sienten)")
    finally:
        R._quita(m)
    gsl = dict(D, LIMPIA=0.0)
    ok(con(m, [gsl], 0.0, 0.0, 1, 0, s, T) == rs, f"(C) GEN con LIMPIA 0 (resto fabrica) == CTRL_O1_SINLIMPIA (la referencia existente, sha {CB.SHA_SINLIMPIA})")
    ok(rs != ro, "(C) control que debe diferir: CTRL_O1_SINLIMPIA != O1 (la limpieza actua a T 3000)")
    rn = con(m, None, CB.SIGMA, CB.DELTA, 0, 1, s, T)
    ok(rn == ro, f"(C) NEUTRO: PS_LEE 0 con mutacion (sigma {CB.SIGMA}, delta {CB.DELTA}), camara, desde la base == O1 (ningun cuerpo lee los genes)")
    try:
        # corregido 1-oct 12:35 (ARNES 31/33): a T 3000 con fundador limpio NO hay refundaciones (0 de camara), asi que el movimiento de los genes
        # se mide en los VIVOS (hijos con '_gen' mutado, profundidad > 1); la camara solo se exige si hubo refundaciones. Defecto del arnes, no del carro.
        R._pon(m, None, s, CB.SIGMA, CB.DELTA, 0, 1); P.run(s, [('X', m)] * 9, T=T, fundador_limpio=1)
        fp = [q for v in m._TEL.values() for q in v.get('fund', [])]; vv = [q for v in m._TEL.values() for q in v.get('vivos', [])]
        partos = sum(v.get('partos', 0) for v in m._TEL.values()); gv = {tuple(q[1]) for q in vv}
        # (12:33, ARNES 32/33: con la base en el borde del clip (ceros) y delta 0.01 muchas mutaciones se recortan al MISMO genoma; a T 3000 hubo 20 partos y
        #  6 genomas distintos entre 27 muestras de vivos, profundidad 2. Se exige >= 2 distintos, partos > 0 y profundidad > 1: eso prueba que el hijo hereda mutado.)
        ok(len(fp) >= 9 and partos > 0 and len(gv) >= 2 and max(q[3] for q in vv) > 1 and sum(q[0] == 2 for q in fp) == len(fp) - 9,
           f"(C)   ...y sus genes SI se mueven: {len(fp)} fundadores (9 de la base, {sum(q[0] == 2 for q in fp)} de camara), {partos} partos, {len(gv)} genomas distintos entre los vivos, profundidad maxima {max(q[3] for q in vv)}")
    finally:
        R._quita(m)
    ok(m.SIEMBRA is None and m.PS_LEE == 1 and m.PS_SIGMA == CB.SIGMA and m.PS_DELTA == CB.DELTA and m.PS_CAMARA == 1 and not m._TEL and not m._PS_CNT and not m._VIVO,
       "(C) el runner deja el modulo como estaba (SIEMBRA None, PS_LEE 1, sigma, delta, camara 1, registros vacios)")
    # cableado: cada gen continuo apagado == O1 con la constante reescrita a mano; HUECO apagado == O1 con tgt = pos
    src = open(CB.ORIGEN, encoding='utf-8').read()
    lit = {'MARGEN': 'MARGEN = 0.25 ', 'PRUEBA': 'PRUEBA = 0.5 ', 'PEN_OTRO': 'PEN_OTRO = 0.35 ', 'PISO': 'PISO = 0.2 '}
    Tc = 12000
    for j, g in enumerate(CB.GENES[:4]):
        assert src.count(lit[g]) == 1
        vals = sorted({CB.APAGADO[j], CB.CLIP[j][0], min(1.0, CB.CLIP[j][1])} - {CB.FABRICA[j]})   # el apagado provisional y los dos extremos del clip (sin la fabrica)
        for val in vals:
            mm = carga_texto(f'o1_{g}_{val}', src.replace(lit[g], f"{g} = {val!r} "))
            a = con(m, [dict(D, **{g: val})], 0.0, 0.0, 1, 0, s, Tc); b = run(mm, s, Tc)
            ok(a == b, f"(C) cableado {g} = {val} (resto fabrica) == O1 con {g} = {val} escrito a mano (T {Tc}); difiere de O1: {a != ro}")
        ok(any(con(m, [dict(D, **{g: val})], 0.0, 0.0, 1, 0, s, Tc) != ro for val in vals), f"(C) control que debe diferir: {g} actua (algun valor != O1 a T {Tc})")
    anc = "            tgt = self._hueco(pos, otros); self.st['sin_blanco'] += 1"
    assert src.count(anc) == 1
    mh = carga_texto('o1_hueco', src.replace(anc, "            tgt = pos; self.st['sin_blanco'] += 1"))
    a = con(m, [dict(D, HUECO=0.0)], 0.0, 0.0, 1, 0, s, Tc)
    ok(a == run(mh, s, Tc), f"(C) cableado HUECO: gen 0 == O1 con `tgt = pos` escrito a mano (T {Tc})")
    ok(a != ro, f"(C) control que debe diferir: HUECO apagado != O1 (T {Tc})")
    ok(con(m, [dict(B)], 0.0, 0.0, 1, 0, s, T) != ro, "(C) control que debe diferir: TODO apagado (base) != O1")
    # brazo pur (5-oct, ERR-192): tope de LECTURA de MARGEN
    try:
        R._pon(m, None, s, CB.SIGMA, CB.DELTA, 1, 1, None, None, None); ra = run(m, s, Tc)
        R._pon(m, None, s, CB.SIGMA, CB.DELTA, 1, 1, None, None, CB.CLIP[0][1]); rb = run(m, s, Tc)
        ok(ra == rb, f"(C) pur: cadena con tope >= clip ({CB.CLIP[0][1]}) == sel (tope None) bit a bit (sigma {CB.SIGMA}, camara, desde BASE, T {Tc})")
        R._pon(m, None, s, CB.SIGMA, CB.DELTA, 1, 1, None, None, R.TOPE_PUR); rp = run(m, s, Tc)
        ok(rp != ra, f"(C) control que debe diferir: pur con tope {R.TOPE_PUR} != sel (el tope actua)")
    finally:
        R._quita(m)
    m0t = carga_texto('o1_MARGEN_0_tope', src.replace(lit['MARGEN'], 'MARGEN = 0.0 '))
    try:
        R._pon(m, [dict(D)], s, 0.0, 0.0, 1, 0, None, None, 0.0); r0 = run(m, s, Tc)
    finally:
        R._quita(m)
    ok(r0 == run(m0t, s, Tc), f"(C) pur: genes de FABRICA con tope 0 == O1 con MARGEN = 0.0 escrito a mano (T {Tc}): el cuerpo lee min(gen, tope); el gen no se toca")
    ok(CB.ARRANQUE_MARGEN < R.TOPE_PUR < R.FUNC_MARGEN and m.PS_TOPE is None, f"(K) TOPE_PUR {R.TOPE_PUR} entre el arranque {CB.ARRANQUE_MARGEN} y la zona funcional {R.FUNC_MARGEN}; PS_TOPE None por defecto")
    ok(P.run is R._ORIG_RUN, "(C) pista.run intacta")
    # (R) regla 14: tarea del runner con dosis de fabrica == corre_v143.tarea('O1') campo a campo
    x = R.tarea(s + 1, 2000, siembra=[dict(D)], sigma=0.0, delta=0.0, lee=1, camara=0); y = CV.tarea((s + 1, 'O1', 2000))
    # corregido 1-oct 12:35 (ARNES 31/33): los ids de linaje llevan el NOMBRE del carro ('O1_MURO_GEN#i' vs 'O1#i'); verificado a T 500 que SOLO difieren
    # 'id' (linajes) e 'ids' (pista). Se compara con el nombre normalizado y se exige que ningun otro campo difiera. Defecto del arnes, no del instrumento.
    dl = sorted({k for a, b in zip(x['linajes'], y['linajes']) for k in a if N(a[k]) != N(b.get(k))}); dp = [k for k in x['pista'] if N(x['pista'][k]) != N(y['pista'][k])]
    ok(set(dl) <= {'id'} and set(dp) <= {'ids'} and R.sin_ids(x['linajes']) == R.sin_ids(y['linajes']) and R.sin_ids(x['pista']) == R.sin_ids(y['pista']) and x['R0_pista'] == y['R0_pista'],
       f"(R) regla 14, ENTRADA campo a campo: corre_muro_perillas.tarea(genes de fabrica) == corre_v143.tarea('O1') salvo el nombre del carro en los ids (s {s + 1}, T 2000); difieren: linajes {dl} pista {dp}")
    # PASO A (5-oct): fundador NO limpio por corrida: tarea(fl=0) == corre_v143.tarea('O1') con FL 0 (salvo ids); y el estado/pista lo registran
    fl0 = CV.FL
    try:
        CV.FL = 0; y0 = CV.tarea((s + 1, 'O1', 2000))
    finally:
        CV.FL = fl0
    x0 = R.tarea(s + 1, 2000, siembra=[dict(D)], sigma=0.0, delta=0.0, lee=1, camara=0, fl=0)
    ok(R.sin_ids(x0['linajes']) == R.sin_ids(y0['linajes']) and R.sin_ids(x0['pista']) == R.sin_ids(y0['pista']) and x0['pista']['fundador_limpio'] == 0 and x0['estado']['fl'] == 0
       and y0['pista']['fundador_limpio'] == 0 and CV.FL == 1 and x['pista']['fundador_limpio'] == 1 and R.sin_ids(x0['linajes']) != R.sin_ids(x['linajes']),
       f"(R) fundador NO limpio: tarea(fl=0, genes de fabrica) == corre_v143.tarea('O1') con FL 0 (salvo ids); pista.fundador_limpio 0; FL restaurado a 1; difiere de fl 1 (s {s + 1}, T 2000)")
    f = R.fila(x, 2000)
    ok(f['fund_n'] > 0 and f['fund_de_siembra'] == f['fund_n'] and f['fund_genes_distintos'] == 1 and f['fund_gen0'] == D and f['coherente'],
       f"(R) fila: todos los fundadores de la siembra con EL genoma ({f['fund_n']}), contabilidad coherente, cruzan {f['cruzan']}/9")
    # (G) generador propio y primer fundador
    class _S: pass
    z = _S(); z._pss = 12345; us = [m.Carro._ps_u(z) for _ in range(20000)]
    ns = []
    for i in range(0, 20000, 2): ns.append(math.sqrt(-2.0 * math.log(us[i])) * math.cos(2.0 * math.pi * us[i + 1]))
    mu = sum(us) / len(us); mn = sum(ns) / len(ns); sd = (sum((v - mn) ** 2 for v in ns) / len(ns)) ** 0.5
    ok(abs(mu - 0.5) < 0.01 and abs(mn) < 0.03 and abs(sd - 1) < 0.03, f"(G) generador propio: uniforme media {mu:.4f}, normal media {mn:.4f} desv {sd:.4f}")
    try:
        R._pon(m, None, CB.SIGMA, CB.DELTA, 1, 1, s); c = m.crea(dict(id='X', indice=0, n_linajes=9, T=100, L=360, PAT={}, rng=None, dote=0.6, rep_umbral=1.0, costo=0.001, costo_a=0.001, rep_X=1, cupo=16, ancho=8, fabrica={}))
        g = c._gen; nz = [j for j in range(6) if g[j] != CB.BASE[j]]
        ok(c._psfund == 0 and c._prof == 1 and len(nz) <= 1 and all(lo <= v <= hi for v, (lo, hi) in zip(g, CB.CLIP)) and c.LIMPIA == int(g[4] > 0.5) and c.HUECO == int(g[5] > 0.5)
           and (c.MARGEN, c.PRUEBA, c.PEN_OTRO, c.PISO) == tuple(g[:4]),
           f"(G) primer fundador sin siembra: origen base, profundidad 1, genes = BASE {CB.BASE} con UNA mutacion en un gen ({[round(v, 4) for v in g]}); el cuerpo lee los genes crudos")
    finally:
        R._quita(m)
    if R.GEN_LETRA is not None:
        for nombre, c, esp in R.casos_sinteticos():
            L = R.lee_serie(*c); v = (L['veredicto'], L['trinquete_gr_umbral']) if isinstance(esp, tuple) else L['veredicto']; ok(v == esp, f"(F) letra sintetica {nombre}: {v} (esperado {esp})")
    else:
        print("  (F) letra de la serie: GEN_LETRA no fijado (se fija tras el mapa; sin casos sinteticos todavia)")
    n = sum(OK); print(f"\nARNES {'PASA' if all(OK) else 'FALLA'}, {n}/{len(OK)} ({time.time() - t0:.1f}s)")
    return 0 if all(OK) else 1


if __name__ == '__main__':
    sys.exit(main())
