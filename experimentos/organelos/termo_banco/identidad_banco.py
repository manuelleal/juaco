"""identidad_banco.py — ARNES del bloque TERMO_BANCO (un proceso; se corre ANTES del humo y de la serie). Salida -> identidad_banco_salida.txt.

MISION: llegar a la AGI por este camino (organismo minimo con reglas locales, sin retropropagacion, peldanos preregistrados con
controles y replicas). Principio del director: que la evolucion construya el organo, no nosotros.
  (K) trae_nube --verifica (los archivos de la nube por sha); construye_evo --verifica (la nube reproduce V143_EVO_* desde V143.py);
      construye_banco --verifica (los 3 carros == anclas desde V143_EVO_BAJO 3187b373654e119f); revisa_carro PASA
  (a) BANCO = 0: V143_EVO_BANCO y V143_EVO_BANCOBAR == V143_EVO_BAJO de la nube, y V143_EVO_BANCO_M40 == V143_EVO_M40, salida ENTERA y
      _TEL (N 9, fundador limpio; s 42913 T 3000 y s 42914 T 8000; con refundaciones de verdad)
  (b) sigma 0 y g fijo 0.40 CON el banco encendido == m40 de la nube en la FISICA (todo salvo d['carro']): V143_EVO_BANCO_M40
      (s 42913 T 5000, s 42914 T 20000) y V143_EVO_BANCOBAR parchado a G_INI (0.4, 0.4), SIGMA 0 (s 42914 T 20000); el banco ACTUA
      en esas corridas (hay fundadores salidos del banco: la identidad no es vacia)
  (c) la regla del banco (funcion pura _bn_toma y metodo _bn_guarda): vacio -> inicial sin gastar rng; modo 1 solo del propio y uniforme;
      modo 2 nunca del propio, linaje ajeno uniforme entre los que tienen; FIFO de tamano cola_max (200)
  (d) en la corrida (s 42914 T 20000, sigma 0 parchado): todo fundador de BANCO con origen 1 tiene el g de un padre de SU linaje; todo
      fundador de BANCOBAR con origen 2 tiene el g de un padre de OTRO linaje; el primer fundador de cada linaje es el de EVO (mismo g)
  (e) el banco se reinicia solo entre corridas (A, B, A sin borrar _BANCO == A); determinismo; la pieza actua
  (f) regla 14: corre_banco.tarea(V143) == corre_v143.tarea y tarea(V143_EVO_BAJO) == corre_evo.tarea de la nube, campo a campo
  (g) corre_banco.verifica(); valida(); ERR-115; la letra en casos sinteticos; bloque()
Uso: python experimentos/organelos/termo_banco/identidad_banco.py
"""
import json, os, sys, time, types

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_banco as CR
import construye_banco as CBB
import construye_evo as CB
import trae_nube as TN
CE = CR.CE; CV = CR.CV; P = CR.P
import numpy as np

N = lambda x: json.loads(json.dumps(x, default=str))


def sin(r, claves):
    out = dict(r); out['linajes'] = [{k: v for k, v in d.items() if k not in claves} for d in r['linajes']]; return out


def main():
    ok = True; t0 = time.time()

    def chk(nombre, cond):
        nonlocal ok; ok &= bool(cond); print(f"  {'OK   ' if cond else 'FALLA'} {nombre}  [{time.time()-t0:.0f}s]", flush=True)

    chk("(K) trae_nube --verifica: los 13 archivos de la nube (c43e12a) con su sha fijado", TN.main(['--verifica']) == 0)
    chk("(K) construye_evo --verifica: la nube reproduce sus 4 carros desde V143.py 2a03048a7f1525e5", CB.main(['--verifica']) == 0)
    chk("(K) construye_banco --verifica: los 3 carros == anclas desde V143_EVO_BAJO 3187b373654e119f (solo perillas/nombre)",
        CBB.main(['--verifica']) == 0)
    for n in CR.PROPIOS:
        vr = CR.RC.revisa_fuente(open(os.path.join(CR.CARROS, n + '.py'), encoding='utf-8').read(), n)
        chk(f"(K) revisa_carro {n}: {'PASA' if not vr else vr[:2]}", not vr)
    CR.registra()
    M = CV._MODS
    MB, MM, MK, MX, MK4 = M['V143_EVO_BAJO'], M['V143_EVO_M40'], M['V143_EVO_BANCO'], M['V143_EVO_BANCOBAR'], M['V143_EVO_BANCO_M40']

    def run(m, s, T):
        m._TEL.clear()
        if hasattr(m, '_BANCO'): m._BANCO.clear()
        r = N(P.run(s, [('C', m)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1))
        return r, N(m._TEL)
    fis = lambda r: sin(r, ('carro',))

    def parche(m, **kw):
        viejo = {k: getattr(m, k) for k in kw}
        for k, v in kw.items(): setattr(m, k, v)
        return viejo

    def origenes(tel):
        return [(int(i), o, g, nb) for i, v in tel.items() for o, g, nb in v.get('fund_banco', [])]

    # (a) BANCO = 0 == la nube, salida entera y _TEL
    for s, T in ((42913, 3000), (42914, 8000)):
        rb, tb = run(MB, s, T); rm, tm = run(MM, s, T)
        ref = sum(d['_carrera']['instancias'] - 1 for d in rb['linajes'])
        chk(f"(a) s {s} T {T}: hay refundaciones en V143_EVO_BAJO ({ref} instancias nuevas)", ref > 0)
        for m, base, tbase, nm in ((MK, rb, tb, 'V143_EVO_BANCO'), (MX, rb, tb, 'V143_EVO_BANCOBAR'), (MK4, rm, tm, 'V143_EVO_BANCO_M40')):
            v = parche(m, BANCO=0)
            try: x, tx = run(m, s, T)
            finally: parche(m, **v)
            chk(f"(a) {nm} con BANCO = 0 == {'V143_EVO_M40' if m is MK4 else 'V143_EVO_BAJO'} de la nube, salida ENTERA y _TEL (s {s}, T {T})",
                x == base and tx == tbase)

    # (b) sigma 0, g 0.40, banco ENCENDIDO == m40 de la nube en la fisica; el banco actua
    for s, T in ((42913, 5000), (42914, 20000)):
        rm, _ = run(MM, s, T); x, tx = run(MK4, s, T); oo = origenes(tx)
        n1 = sum(1 for z in oo if z[1] == 1)
        chk(f"(b) V143_EVO_BANCO_M40 (BANCO 1, g 0.40, sigma 0) == V143_EVO_M40 en la FISICA (s {s}, T {T}); fundadores del banco {n1}",
            fis(x) == fis(rm) and (n1 > 0 or T < 20000))
        if T == 20000: chk(f"(b) el banco ACTUA en la corrida larga de (b): {n1} fundadores salieron del banco propio", n1 > 0)
    v = parche(MX, G_INI=(0.4, 0.4), SIGMA=0.0)
    try: x, tx = run(MX, 42914, 20000)
    finally: parche(MX, **v)
    n2 = sum(1 for z in origenes(tx) if z[1] == 2)
    chk(f"(b) V143_EVO_BANCOBAR parchado a g 0.40, sigma 0 == V143_EVO_M40 en la FISICA (s 42914, T 20000); fundadores de banco ajeno {n2}",
        fis(x) == fis(rm) and n2 > 0)

    # (c) la regla, en frio
    r = np.random.default_rng(7); e0 = r.bit_generator.state
    a1 = MK._bn_toma([], [[1.0], [2.0]], r, 1); a2 = MK._bn_toma([], [[1.0], [2.0]], r, 2)
    chk("(c) banco propio vacio -> (None, 0) en los dos modos, sin gastar el rng", a1 == (None, 0) and a2 == (None, 0) and r.bit_generator.state == e0)
    propio = [0.11, 0.12, 0.13, 0.14, 0.15]; otros = [[0.51, 0.52], [], [0.71]]
    d1 = [MK._bn_toma(propio, otros, r, 1) for _ in range(5000)]
    fr = [sum(1 for g, o in d1 if g == p) / 5000 for p in propio]
    chk(f"(c) modo 1: solo del propio (origen 1) y uniforme (frecuencias {[round(f, 3) for f in fr]})",
        all(o == 1 and g in propio for g, o in d1) and all(0.17 <= f <= 0.23 for f in fr))
    d2 = [MK._bn_toma(propio, otros, r, 2) for _ in range(6000)]
    fa = sum(1 for g, o in d2 if g in (0.51, 0.52)) / 6000; fb = sum(1 for g, o in d2 if g == 0.71) / 6000
    chk(f"(c) modo 2: nunca del propio; linaje ajeno uniforme entre los que tienen semillas (0.5x {fa:.3f}, 0.71 {fb:.3f}; el vacio no cuenta)",
        all(o == 2 and g not in propio for g, o in d2) and 0.47 <= fa <= 0.53 and 0.47 <= fb <= 0.53)
    chk("(c) modo 2 sin ningun banco ajeno con semillas -> (None, 0)", MK._bn_toma(propio, [[], []], r, 2) == (None, 0))
    MK._BANCO.clear(); MK._BANCO[0] = dict(rng=None, g=[], cap=200, fund=[0, 0, 0])
    for k in range(250): MK.Carro._bn_guarda(types.SimpleNamespace(_ind=0, _g=float(k)))
    bb = MK._BANCO[0]['g']; MK._BANCO.clear()
    chk(f"(c) FIFO: 250 partos -> banco de {len(bb)} con los 200 ultimos (tamano = cola_max de la pista {CV.P.cfg_fabrica()['kw']['cola_max']})",
        len(bb) == 200 and bb == [float(k) for k in range(50, 250)] and CV.P.cfg_fabrica()['kw']['cola_max'] == 200)

    # (d) en la corrida, con sigma 0 (los g se pueden rastrear exactos)
    v = parche(MK, SIGMA=0.0)
    try: rk, tk = run(MK, 42914, 20000)
    finally: parche(MK, **v)
    ok1 = [(i, g) for i, o, g, nb in origenes(tk) if o == 1]
    padres = {int(i): {g for t, g in x['partos']} for i, x in tk.items()}
    chk(f"(d) BANCO (sigma 0): los {len(ok1)} fundadores del banco propio tienen el g de un padre de SU linaje",
        ok1 and all(g in padres[i] for i, g in ok1))
    chk("(d) BANCO: el primer fundador de cada linaje sale de la inicial (origen 0) y en [-0.10, 0.10]",
        all(tk[i]['fund_banco'][0][0] == 0 and -0.1 <= tk[i]['fund_banco'][0][1] <= 0.1 for i in tk))
    _, tb20 = run(MB, 42914, 20000)
    chk("(d) BANCO y EVO de la nube: el mismo g en el primer fundador de cada linaje (mismo rng del gen)",
        [tk[i]['vivos'][0][1] for i in sorted(tk)] == [tb20[i]['vivos'][0][1] for i in sorted(tb20)])
    v = parche(MX, SIGMA=0.0)
    try: rx, tx = run(MX, 42914, 20000)
    finally: parche(MX, **v)
    ok2 = [(i, g) for i, o, g, nb in origenes(tx) if o == 2]
    padx = {int(i): {g for t, g in x['partos']} for i, x in tx.items()}
    chk(f"(d) BANCOBAR (sigma 0): los {len(ok2)} fundadores de banco ajeno tienen el g de un padre de OTRO linaje",
        ok2 and all(any(g in padx[j] for j in padx if j != i) for i, g in ok2))
    chk("(d) BANCOBAR: ningun fundador sale del banco propio (origen 1)", all(o != 1 for i, o, g, nb in origenes(tx)))
    nbm = max(nb for i, o, g, nb in origenes(tk) + origenes(tx))
    chk(f"(d) el banco nunca pasa de 200 (maximo visto al fundar {nbm})", nbm <= 200)

    # (e) reinicio solo, determinismo, pieza
    # v2 del caso (e) (ERR de instrumento del creador, declarado): la v1 usaba A = s 42913 T 6000, donde NINGUN fundador sale del banco
    # (los linajes que se refundan nunca parieron) y la comprobacion era vacia. Ahora A = s 42914 T 20000 (24 fundadores del banco).
    MK._TEL.clear(); MK._BANCO.clear()
    A1 = N(P.run(42914, [('C', MK)] * 9, T=20000, fundador_limpio=1)); MK._TEL.clear()
    N(P.run(42913, [('C', MK)] * 9, T=6000, fundador_limpio=1)); MK._TEL.clear()        # SIN borrar _BANCO entre corridas
    A2 = N(P.run(42914, [('C', MK)] * 9, T=20000, fundador_limpio=1))
    nA = sum(d['carro']['evo']['banco']['fund_propio'] for d in A1['linajes'])
    chk(f"(e) el banco se reinicia solo: A, B, A sin borrar _BANCO -> A == A (salida ENTERA; fundadores del banco en A {nA})", A1 == A2 and nA > 0)
    rk2, tk2 = run(MK, 42914, 20000); rk3, tk3 = run(MK, 42914, 20000)
    chk("(e) determinismo: V143_EVO_BANCO dos corridas iguales (salida entera y _TEL; s 42914, T 20000)", rk2 == rk3 and tk2 == tk3)
    rx2, tx2 = run(MX, 42914, 20000)
    gk = [g for i, o, g, nb in origenes(tk2) if o == 1]; gx = [g for i, o, g, nb in origenes(tx2) if o == 2]
    chk(f"(e) con sigma 0.03, los g de los fundadores de banco DIFIEREN entre BANCO ({len(gk)}) y BANCOBAR ({len(gx)}): los sorteos no se copian",
        gk and gx and gk != gx)
    print(f"       DESCRIPTIVO: fisica BANCO == BANCOBAR en s 42914 T 20000: {fis(rk2) == fis(rx2)} (si True: el g del fundador del banco no"
          f" cambio ninguna decision en esa semilla; el fundador nuevo tiene _adS vacio y la pieza solo actua sobre lo ya sentido bueno)")
    t1 = CE.tm_suma([dict(tel_evo=dict(ult=[d['carro'].get('evo') for d in rk2['linajes']]))])
    t2 = CE.tm_suma([dict(tel_evo=dict(ult=[d['carro'].get('evo') for d in rx2['linajes']]))])
    print(f"       pieza banco {t1} - bancobar {t2}")
    chk("(e) la pieza ACTUA en BANCO y en BANCOBAR (V4)", CE.pieza(t1) and CE.pieza(t2))

    # (f) regla 14
    sin_seg = lambda z: N({k: v for k, v in z.items() if k != 'seg'})
    x = CR.tarea((42913, 'V143', 2000)); y = CV.tarea((42913, 'V143', 2000))
    chk("(f) regla 14: corre_banco.tarea(V143) == corre_v143.tarea campo a campo (s 42913, T 2000) y tel_evo vacia",
        x.pop('tel_evo') == dict(ult=[None] * 9, tel=None) and sin_seg(x) == sin_seg(y))
    x = CR.tarea((42913, 'V143_EVO_BAJO', 3000)); y = CE.tarea((42913, 'V143_EVO_BAJO', 3000))
    chk("(f) regla 14: corre_banco.tarea(V143_EVO_BAJO) == corre_evo.tarea de la nube campo a campo (s 42913, T 3000)", sin_seg(x) == sin_seg(y))
    x1 = CR.tarea((42913, 'V143_EVO_BANCO', 6000)); x2 = CR.tarea((42913, 'V143_EVO_BANCO', 6000))
    chk("(f) tarea(): _TEL y _BANCO se borran antes de cada run (dos tareas seguidas iguales)", sin_seg(x1) == sin_seg(x2) and x1['tel_evo']['tel'])

    # (g) runner y letra
    lines = []
    chk("(g) corre_banco.verifica(): shas fijados + carros == construye_banco + revisa_carro + identidad corta", CR.verifica(lines.append))
    for l in lines: print("     " + l)
    SB = list(CR.SERIE_BRAZOS)
    chk("(g) valida: serie 42001-42020 y replica 42021-42040 con los 6 brazos y T 100000 -> OK",
        CR.valida(False, 42001, 20, 100000, SB) is None and CR.valida(False, 42021, 20, 100000, SB) is None)
    chk("(g) valida: rechaza semillas de TERMO_EVO 41001, serie mezclada 42011-42030, T 50000, brazos distintos",
        all(z is not None for z in (CR.valida(False, 41001, 20, 100000, SB), CR.valida(False, 42011, 20, 100000, SB),
                                    CR.valida(False, 42001, 20, 50000, SB), CR.valida(False, 42001, 20, 100000, ['v143', 'banco', 'o1']))))
    chk("(g) valida: humo solo 42911-42914 y T <= 30000",
        CR.valida(True, 42001, 1, 20000, ['banco']) is not None and CR.valida(True, 42911, 2, 40000, ['banco']) is not None)
    try:
        CR.main(['--humo', '--desd', '42911']); e115 = False
    except SystemExit:
        e115 = True
    chk("(g) ERR-115: una bandera abreviada (--desd) ABORTA", e115)

    def caso(v2=True, v143=0.6, act=True, p1=True, p2g=18, dif=0.2, p3n=16, sg=17):
        res = {b: dict(coherente='180/180', gana_e5=False, R0_real_med=0.5) for b in CR.SERIE_BRAZOS}
        res['o1']['gana_e5'] = v2; res['v143']['R0_real_med'] = v143; res['banco']['gana_e5'] = p1
        par = {('banco', 'evo'): dict(semillas=20, gana=p2g, dif_med=dif)}
        tm = {'banco': dict(a_no=3, a_si=1), 'bancobar': dict(a_no=2, a_si=0)}
        p3 = {s: dict(cumple=(k < p3n)) for k, s in enumerate(CR.SERIE)}
        gpar = dict(semillas=20, gana=sg, dif_med=0.01)
        return CR.lee_serie(res, par, tm, p3, gpar, dict(banco=act, bancobar=act), True, 0)
    L = [(caso(), 'FUNCIONA'), (caso(p1=False), 'HAY ALGO MODESTO'), (caso(p1=False, dif=0.05), 'NO'), (caso(p3n=14), 'NO'),
         (caso(p1=False, p3n=14), 'NO'), (caso(p2g=14), 'NO'), (caso(v2=False), 'NO SE LEE'), (caso(v143=0.85), 'NO SE LEE'),
         (caso(act=False), 'NO SE LEE'), (caso(p1=False, p2g=15, dif=0.10, p3n=15), 'HAY ALGO MODESTO')]
    for i, (z, esp) in enumerate(L):
        chk(f"(g) letra caso {i + 1}: {z['veredicto']} == {esp}", z['veredicto'] == esp)
    chk("(g) vocabulario: S 17/20 -> 'DEL PROPIO LINAJE'; S 14/20 -> no especifico",
        'PROPIO' in caso()['vocabulario'] and 'no especifico' in caso(sg=14)['vocabulario'])
    chk("(g) bloque: FUNCIONA+MODESTO -> MODESTO; NO SE LEE+FUNCIONA -> NO SE LEE; NO+NO -> NO",
        CR.bloque('FUNCIONA', 'HAY ALGO MODESTO') == 'HAY ALGO MODESTO' and CR.bloque('NO SE LEE', 'FUNCIONA') == 'NO SE LEE' and CR.bloque('NO', 'NO') == 'NO')

    print(f"\nARNES {'PASA' if ok else 'FALLA'} ({time.time()-t0:.0f} s) - identidad_banco.py sha {CR.h16(os.path.abspath(__file__))} - "
          f"python {sys.version.split()[0]} - numpy {np.__version__}")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
