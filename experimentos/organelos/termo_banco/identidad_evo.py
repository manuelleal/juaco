"""identidad_evo.py — ARNES del bloque TERMO_EVO (un proceso; se corre ANTES del humo y de la serie). Salida -> identidad_evo_salida.txt.

MISION: llegar a la AGI por este camino.
  (K) construye_evo --verifica: carros en disco == construidos por anclas desde V143.py (sha fijado); difieren solo en perillas/nombre
  (a) los 4 carros con EVO = 0 == V143, salida ENTERA (N 9, fundador limpio; s 41913 T 2000 y s 41914 T 5000)
  (b) EVO con sigma 0 y g fijo 0.40 == HIBB m40 (boca_buena/carros, puente boca_buena) en la FISICA bit a bit (todo salvo d['carro']):
      V143_EVO_M40 (s 41913 T 5000, s 41914 T 20000); y V143_EVO_BAJO y V143_EVO_SINHER con perillas G_INI (0.4, 0.4), SIGMA 0
      (s 41913 T 5000): la herencia y el re-sorteo son la MISMA fisica cuando el gen no varia
  (c) SINHER == EVO en el primer fundador: el g del primer cuerpo de cada linaje es el mismo en los dos, y la fisica es identica hasta
      el paso del primer nacimiento de la cola (T = t_primer_nace + 1); despues se separan (T 5000)
  (d) el rng del gen no toca el del cuerpo: Generator.spawn deja el estado del rng del cuerpo intacto (numpy)
  (e) herencia: con sigma 0 (BAJO parchado) todo g de un nacido es el g de algun padre al parir; en SINHER no (s 41914 T 20000);
      con sigma 0.03 los g de nacidos quedan en G_CLIP; los fundadores de BAJO/SINHER en U[-0.10, 0.10]
  (f) la pieza ACTUA en EVO y SINHER; determinismo (dos corridas iguales)
  (g) corre_evo.verifica(): shas FIJADOS + revisa_carro + identidad corta; valida() rechaza semillas/T/brazos fuera del preregistro;
      ERR-115 (bandera abreviada aborta); la letra en casos sinteticos.
Uso: python experimentos/organelos/termo_evo/identidad_evo.py
"""
import json, os, sys, time, importlib.util
from hashlib import sha256

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_evo as CE
import construye_evo as CB
P = CE.P; CV = CE.CV
import numpy as np
HIBB_RUTA = os.path.join(os.path.dirname(AQUI), 'boca_buena', 'carros', 'HIBB.py')
SHA_HIBB = '3ca86aed6c409a11'

N = lambda x: json.loads(json.dumps(x, default=str))


def sin(r, claves):
    out = dict(r); out['linajes'] = [{k: v for k, v in d.items() if k not in claves} for d in r['linajes']]; return out


def main():
    ok = True; t0 = time.time()

    def chk(nombre, cond):
        nonlocal ok; ok &= bool(cond); print(f"  {'OK   ' if cond else 'FALLA'} {nombre}", flush=True)

    chk("(K) construye_evo --verifica (carros == anclas desde V143.py 2a03048a7f1525e5; solo perillas/nombre)", CB.main(['--verifica']) == 0)
    CE.registra()
    V143 = CV.modulo('V143'); M = {n: CV._MODS[n] for n in CE.PROPIOS}
    run = lambda m, s, T: N(P.run(s, [('C', m)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1))
    fis = lambda r: sin(r, ('carro',))

    def parche(m, **kw):
        viejo = {k: getattr(m, k) for k in kw}
        for k, v in kw.items(): setattr(m, k, v)
        return viejo

    for s, T in ((41913, 2000), (41914, 5000)):
        base = run(V143, s, T)
        for nm, m in M.items():
            v = parche(m, EVO=0)
            try: x = run(m, s, T)
            finally: parche(m, **v)
            chk(f"(a) {nm} con EVO = 0 == V143, salida ENTERA (N 9, s {s}, T {T}, fundador limpio)", x == base)

    sh = sha256(open(HIBB_RUTA, 'rb').read()).hexdigest()[:16]
    chk(f"(b0) HIBB del diagnostico sha {sh} == {SHA_HIBB}", sh == SHA_HIBB)
    spec = importlib.util.spec_from_file_location('HIBB_evo', HIBB_RUTA); H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)

    def hibb(bb, s, T):
        H.PUENTES = dict(patas=0, boca_buena=1, boca_mala=0, memoria=0); H.BB = bb; return run(H, s, T)
    R40 = {}
    for s, T in ((41913, 5000), (41914, 20000)):
        R40[(s, T)] = run(M['V143_EVO_M40'], s, T); hb = hibb('m40', s, T)
        chk(f"(b) V143_EVO_M40 (EVO 1, g 0.40 fijo, sigma 0) == HIBB m40 en la FISICA (todo salvo d['carro']; s {s}, T {T})", fis(R40[(s, T)]) == fis(hb))
        if s == 41914: R40['hibb'] = hb
    for nm in ('V143_EVO_BAJO', 'V143_EVO_SINHER'):
        m = M[nm]; v = parche(m, G_INI=(0.4, 0.4), SIGMA=0.0)
        try: x = run(m, 41913, 5000)
        finally: parche(m, **v)
        chk(f"(b) {nm} parchado a G_INI (0.4, 0.4), SIGMA 0 == HIBB m40 en la FISICA (s 41913, T 5000)", fis(x) == fis(R40[(41913, 5000)]))

    # (c) SINHER == EVO en el primer fundador
    MB = M['V143_EVO_BAJO']; MS = M['V143_EVO_SINHER']
    MB._TEL.clear(); rb = run(MB, 41914, 5000); tb = json.loads(json.dumps(MB._TEL))
    MS._TEL.clear(); rs = run(MS, 41914, 5000); ts = json.loads(json.dumps(MS._TEL))
    g1b = [tb[i]['vivos'][0][1] for i in sorted(tb)]; g1s = [ts[i]['vivos'][0][1] for i in sorted(ts)]
    chk(f"(c) g del primer fundador de cada linaje igual en EVO y SINHER (9 linajes, s 41914): {g1b[:3]}...", g1b == g1s and len(g1b) == 9)
    tn = min([t for v in tb.values() for t, g in v['nacidos']] + [10 ** 9])
    chk(f"(c) hay un primer nacimiento de la cola antes de T 5000 (t {tn})", tn < 5000)
    if tn < 5000:
        a1 = run(MB, 41914, tn + 1); b1 = run(MS, 41914, tn + 1)
        chk(f"(c) fisica EVO == SINHER hasta el paso del primer nacimiento (T = {tn + 1})", fis(a1) == fis(b1))
    chk("(c) y a T 5000 se separan (la herencia cambia algo)", fis(rb) != fis(rs))

    # (d) spawn no avanza el rng del cuerpo
    r = np.random.default_rng([41914, 3, 11, 0]); e0 = r.bit_generator.state; r.spawn(1); r.spawn(1)
    r2 = np.random.default_rng([41914, 3, 11, 0])
    chk("(d) Generator.spawn deja intacto el estado del rng del cuerpo (y su siguiente sorteo)", r.bit_generator.state == e0 and r.random() == r2.random())

    # (e) herencia
    v = parche(MB, SIGMA=0.0)
    try:
        MB._TEL.clear(); run(MB, 41914, 20000); te = json.loads(json.dumps(MB._TEL))
    finally: parche(MB, **v)
    gp = {g for x in te.values() for t, g in x['partos']}; gn = [g for x in te.values() for t, g in x['nacidos']]
    chk(f"(e) sigma 0: los {len(gn)} nacidos tienen el g de algun padre al parir ({len(gp)} valores de padres)", gn and all(g in gp for g in gn))
    MS._TEL.clear(); run(MS, 41914, 20000); tsx = json.loads(json.dumps(MS._TEL))
    gps = {g for x in tsx.values() for t, g in x['partos']}; gns = [g for x in tsx.values() for t, g in x['nacidos']]
    chk(f"(e) SINHER: los nacidos NO copian al padre ({sum(g in gps for g in gns)}/{len(gns)} coinciden por azar)", gns and sum(g in gps for g in gns) < len(gns) / 2)
    MB._TEL.clear(); rbx = run(MB, 41914, 20000); tbx = json.loads(json.dumps(MB._TEL))
    gnb = [g for x in tbx.values() for t, g in x['nacidos']]
    fund = [x['vivos'][0][1] for x in tbx.values()] + [g for x in tbx.values() for t, g, e, h, o in x['muertes'] if o == 0]
    chk(f"(e) sigma 0.03: {len(gnb)} nacidos en G_CLIP [-0.2, 1.0]; fundadores de BAJO en U[-0.10, 0.10] ({len(fund)})",
        gnb and all(-0.2 <= g <= 1.0 for g in gnb) and all(-0.1 <= g <= 0.1 for g in fund))
    fs = [g for x in tsx.values() for t, g, e, h, o in x['muertes']]
    chk(f"(e) SINHER: todo cuerpo (fundador o nacido) en U[-0.10, 0.10] ({len(fs)} muertos)", fs and all(-0.1 <= g <= 0.1 for g in fs))

    # (f) pieza y determinismo
    tt = CE.tm_suma([dict(tel_evo=dict(ult=[d['carro'].get('evo') for d in rbx['linajes']]))])
    ti = CE.tm_suma([dict(tel_evo=dict(ult=[d['carro'].get('evo') for d in rs['linajes']]))])
    print(f"       pieza evo {tt} · sinher {ti}")
    chk("(f) la pieza ACTUA en EVO y en SINHER (V4: a_no + a_si > 0)", CE.pieza(tt) and CE.pieza(ti))
    MB._TEL.clear(); rby = run(MB, 41914, 20000); tby = json.loads(json.dumps(MB._TEL))
    chk("(f) determinismo: V143_EVO_BAJO dos corridas iguales, fisica, carro y telemetria del gen (s 41914, T 20000)", rby == rbx and tby == tbx)
    x1 = CE.tarea((41913, 'V143_EVO_BAJO', 3000)); x2 = CE.tarea((41913, 'V143_EVO_BAJO', 3000))
    chk("(f) tarea(): _TEL se borra antes de cada run (dos tareas seguidas dan la misma telemetria)",
        x1['tel_evo'] == x2['tel_evo'] and x1['tel_evo']['tel'] is not None)

    lines = []
    chk("(g) corre_evo.verifica(): shas fijados + carros == construye + revisa_carro + identidad corta", CE.verifica(lines.append))
    for l in lines: print("     " + l)
    chk("(g) valida: serie 41001-41020 con los 6 brazos y T 100000 -> OK", CE.valida(False, 41001, 20, 100000, list(CE.SERIE_BRAZOS)) is None)
    chk("(g) valida: replica 41021-41040 -> OK", CE.valida(False, 41021, 20, 100000, list(CE.SERIE_BRAZOS)) is None)
    chk("(g) valida: larga 41041-41050, T 300000, evo y sinher -> OK", CE.valida(False, 41041, 10, 300000, list(CE.LARGA_BRAZOS)) is None)
    chk("(g) valida: rechaza semillas de TERMO 39101", CE.valida(False, 39101, 20, 100000, list(CE.SERIE_BRAZOS)) is not None)
    chk("(g) valida: rechaza serie mezclada 41011-41030", CE.valida(False, 41011, 20, 100000, list(CE.SERIE_BRAZOS)) is not None)
    chk("(g) valida: rechaza T 50000 en serie y T 100000 en la larga", CE.valida(False, 41001, 20, 50000, list(CE.SERIE_BRAZOS)) is not None
        and CE.valida(False, 41041, 10, 100000, list(CE.LARGA_BRAZOS)) is not None)
    chk("(g) valida: rechaza brazos distintos", CE.valida(False, 41001, 20, 100000, ['v143', 'evo', 'o1']) is not None)
    chk("(g) valida: humo solo 41911-41914 y T <= 30000", CE.valida(True, 41001, 1, 20000, ['evo']) is not None and CE.valida(True, 41911, 2, 40000, ['evo']) is not None)
    try:
        CE.main(['--humo', '--desd', '41911']); e115 = False
    except SystemExit:
        e115 = True
    chk("(g) ERR-115: bandera abreviada --desd (de --desde) aborta antes de correr nada", e115)
    # la letra en casos sinteticos
    res0 = {b: dict(coherente='9/9', gana_e5=False, R0_real_med=0.5) for b in CE.SERIE_BRAZOS}; res0['o1']['gana_e5'] = True
    tm0 = {CE.CAND: dict(a_no=1), CE.CTRL: dict(a_si=1)}

    def L(cand_e5, gc, dif, p3n, v143=0.5, o1=True, ab=0, tm=tm0):
        r = json.loads(json.dumps(res0)); r[CE.CAND]['gana_e5'] = cand_e5; r['v143']['R0_real_med'] = v143; r['o1']['gana_e5'] = o1
        par = {(CE.CAND, CE.CTRL): dict(semillas=20, gana=gc, dif_med=dif)}
        p3 = {s: dict(n=5, media=(0.3 if i < p3n else 0.05), cumple=i < p3n) for i, s in enumerate(range(41001, 41021))}
        return CE.lee_serie(r, par, tm, p3, True, ab)['veredicto']
    casos = [(L(True, 18, 0.4, 16), 'FUNCIONA'), (L(False, 18, 0.4, 16), 'HAY ALGO MODESTO'), (L(False, 12, 0.15, 15), 'HAY ALGO MODESTO'),
             (L(True, 18, 0.4, 14), 'NO'), (L(False, 18, 0.05, 16), 'NO'), (L(False, 10, 0.4, 16), 'NO'), (L(True, 14, 0.4, 16), 'HAY ALGO MODESTO'),
             (L(True, 18, 0.4, 16, v143=0.39), 'NO SE LEE'), (L(True, 18, 0.4, 16, o1=False), 'NO SE LEE'), (L(True, 18, 0.4, 16, ab=1), 'NO SE LEE'),
             (L(True, 18, 0.4, 16, tm={CE.CAND: dict(a_no=1), CE.CTRL: {}}), 'NO SE LEE')]
    bien = sum(a == b for a, b in casos)
    chk(f"(g) la letra en {len(casos)} casos sinteticos ({bien}/{len(casos)}) · bloque(FUNCIONA, MODESTO) = {CE.bloque('FUNCIONA', 'HAY ALGO MODESTO')}",
        bien == len(casos) and CE.bloque('FUNCIONA', 'HAY ALGO MODESTO') == 'HAY ALGO MODESTO')
    print(f"ARNES {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
