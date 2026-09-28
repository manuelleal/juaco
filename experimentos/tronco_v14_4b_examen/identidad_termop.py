"""identidad_termop.py = experimentos/organelos/termo/identidad_termo.py (95249ad33bbde643) para TERMO' (carrera). GENERADO por construye_carrera_termop.py. NO editar a mano. Salida -> identidad_termop_salida.txt."""
"""identidad_termo.py — ARNES del bloque TERMO (un proceso; se corre ANTES del humo y de la serie). Salida -> identidad_termo_salida.txt.

MISION: llegar a la AGI por este camino.
  (K) construye_termo --verifica: carros en disco == construidos por anclas desde V143.py (sha fijado); difieren solo en perillas/nombre
  (a) V143_TERMO y V143_TERMOINV con TERMO = 0 == V143, salida ENTERA (N 9, fundador limpio; s 49993 T 2000 y s 49994 T 5000)
  (b) V143_TERMO == HIBB (boca_buena/carros, BB 'm40', puente boca_buena) en la FISICA bit a bit (todo salvo d['carro']; s 49993 T 5000,
      s 49994 T 20000): la pieza es exactamente el brazo m40 del diagnostico
  (c) V143_TERMOINV == HIBB BB 'tinv40' en la fisica (s 49993 T 5000); TERMOINV != TERMO en la fisica; y la pieza actua en los dos
  (d) corre_termo.verifica(): shas FIJADOS de todo lo que corre (runner, construye, carros, V143, pista, juez, O1, corre_v143,
      revisa_carro) + revisa_carro + identidad corta. Mas: determinismo, valida() rechaza semillas/T/brazos fuera del preregistro,
      ERR-115 (bandera abreviada aborta) y la letra en casos sinteticos.
Uso: python experimentos/organelos/termo/identidad_termo.py
"""
import json, os, sys, time, importlib.util

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_termop as CT
import construye_termop as CB
P = CT.P; CV = CT.CV
HIBB_RUTA = os.path.join(os.path.dirname(AQUI), 'boca_buena', 'carros', 'HIBB.py')
SHA_HIBB = '3ca86aed6c409a11'

N = lambda x: json.loads(json.dumps(x, default=str))


def sin(r, claves):
    out = dict(r); out['linajes'] = [{k: v for k, v in d.items() if k not in claves} for d in r['linajes']]; return out


def main():
    ok = True; t0 = time.time()

    def chk(nombre, cond):
        nonlocal ok; ok &= bool(cond); print(f"  {'OK   ' if cond else 'FALLA'} {nombre}", flush=True)

    chk("(K) construye_termop: carros en disco == construccion por anclas desde V143_TERMO / V143_TERMOINV (sha fijados)",
        all(open(os.path.join(AQUI, k), 'rb').read() == v.encode('utf-8') for k, v in CB.construye().items() if k.startswith('carros')))
    CT.registra()
    V143 = CV.modulo('V143'); TM = CV._MODS['V143_TERMOP']; TI = CV._MODS['V143_TERMOPINV']
    run = lambda m, s, T: N(P.run(s, [('C', m)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1))
    for s, T in ((49993, 2000), (49994, 5000)):
        base = run(V143, s, T)
        for nm, m in (('V143_TERMOP', TM), ('V143_TERMOPINV', TI)):
            g = m.TERMO
            try:
                m.TERMO = 0; x = run(m, s, T)
            finally:
                m.TERMO = g
            chk(f"(a) {nm} con TERMO = 0 == V143, salida ENTERA (N 9, s {s}, T {T}, fundador limpio)", x == base)

    import importlib.util as _iu
    def _carga(n, ruta):
        s_ = _iu.spec_from_file_location(n, ruta); m_ = _iu.module_from_spec(s_); s_.loader.exec_module(m_); return m_
    TD_ = os.path.join(CT.RAIZ, 'experimentos', 'organelos', 'termo', 'carros')
    T0, T0I = _carga('carro_TERMO_ref', os.path.join(TD_, 'V143_TERMO.py')), _carga('carro_TERMOINV_ref', os.path.join(TD_, 'V143_TERMOINV.py'))
    fis = lambda r: sin(r, ('carro', 'id'))
    R = {}
    for s, T in ((49993, 5000), (49994, 20000)):
        R[(s, T)] = run(TM, s, T)
        chk(f"(b) pista QUIETA: V143_TERMOP == V143_TERMO en la FISICA (todo salvo d['carro'] e id; s {s}, T {T}): la media movil de un dS "
            f"constante es ese dS", fis(R[(s, T)]) == fis(run(T0, s, T)))
    ri = run(TI, 49993, 5000)
    chk("(c) V143_TERMOPINV == V143_TERMOINV en la FISICA (s 49993, T 5000)", fis(ri) == fis(run(T0I, 49993, 5000)))
    chk("(c) V143_TERMOPINV != V143_TERMOP en la fisica (s 49993, T 5000)", fis(ri) != fis(R[(49993, 5000)]))
    tt = CT.tm_suma([dict(tel_termo=[d['carro'].get('termo') for d in R[(49993, 5000)]['linajes']])])
    ti = CT.tm_suma([dict(tel_termo=[d['carro'].get('termo') for d in ri['linajes']])])
    print(f"       telemetria termop {tt} · termopinv {ti}")
    chk("(c) la pieza ACTUA en TERMOP y en TERMOPINV (V4: a_no + a_si > 0)", CT.pieza(tt) and CT.pieza(ti))
    chk("(c) determinismo: V143_TERMOP dos corridas iguales (s 49993, T 5000)", run(TM, 49993, 5000) == R[(49993, 5000)])
    c = object.__new__(TM.Carro); c._tmM = {}; c._tmL = 0.05; ref = None; okm = True
    for x in [(0.8, 0.0)] * 20 + [(-0.4, 0.0)] * 30:
        c._tm_dS('A', x); ref = [x[0], x[1], 1] if ref is None else [ref[0] + 0.05 * (x[0] - ref[0]), ref[1] + 0.05 * (x[1] - ref[1]), 1]
        okm &= c._tmM['A'] == ref
    chk(f"(c) la memoria de TERMO' se DESDICE: tras 20 x (+0.8) y 30 x (-0.4) vale {c._tmM['A'][0]:.3f} < 0 (media movil, ema_c 0.05 de "
        f"FABRICA); la de TERMO seguiria en {(20 * 0.8 - 30 * 0.4) / 50:+.3f}", okm and c._tmM['A'][0] < 0)
    lines = []
    chk("(d) corre_termo.verifica(): shas fijados + carros == construye + revisa_carro + identidad corta", CT.verifica(lines.append))
    for l in lines: print("     " + l)
    chk("(d) valida: serie 49941-49960 con los 4 brazos y T 100000 -> OK", CT.valida(False, 49941, 20, 100000, list(CT.SERIE_BRAZOS)) is None)
    chk("(d) valida: replica 49961-49980 -> OK", CT.valida(False, 49961, 20, 100000, list(CT.SERIE_BRAZOS)) is None)
    chk("(d) valida: rechaza semillas del exploratorio de TERMO 39001", CT.valida(False, 39001, 10, 100000, list(CT.SERIE_BRAZOS)) is not None)
    chk("(d) valida: rechaza serie mezclada 39111-39130", CT.valida(False, 39111, 20, 100000, list(CT.SERIE_BRAZOS)) is not None)
    chk("(d) valida: rechaza T 50000 en serie", CT.valida(False, 49941, 20, 50000, list(CT.SERIE_BRAZOS)) is not None)
    chk("(d) valida: rechaza brazos distintos", CT.valida(False, 49941, 20, 100000, ['v143', 'termop', 'o1']) is not None)
    chk("(d) valida: humo solo 49991-49994 y T <= 30000", CT.valida(True, 49941, 1, 20000, ['termop']) is not None and CT.valida(True, 49991, 2, 40000, ['termop']) is not None)
    try:
        CT.main(['--humo', '--desd', '49991']); e115 = False
    except SystemExit:
        e115 = True
    chk("(d) ERR-115: bandera abreviada --desd (de --desde) aborta antes de correr nada", e115)
    # la letra en casos sinteticos
    res0 = {b: dict(coherente='9/9', gana_e5=False, R0_real_med=0.5) for b in CT.SERIE_BRAZOS}; res0['o1']['gana_e5'] = True
    tm0 = {CT.CAND: dict(a_no=1), CT.CTRL: dict(a_si=1)}
    def L(cand_e5, gana, dif, gc, ctrl_e5=False, v143=0.5, o1=True, ab=0, tm=tm0):
        r = json.loads(json.dumps(res0)); r[CT.CAND]['gana_e5'] = cand_e5; r[CT.CTRL]['gana_e5'] = ctrl_e5; r['v143']['R0_real_med'] = v143
        r['o1']['gana_e5'] = o1
        par = {(CT.CAND, 'v143'): dict(semillas=20, gana=gana, dif_med=dif), (CT.CAND, CT.CTRL): dict(semillas=20, gana=gc, dif_med=0.5)}
        return CT.lee_serie(r, par, tm, True, ab)['veredicto']
    casos = [(L(True, 19, 0.4, 20), 'FUNCIONA'), (L(False, 18, 0.4, 20), 'HAY ALGO MODESTO'), (L(False, 18, 0.05, 20), 'NO'),
             (L(False, 14, 0.4, 20), 'NO'), (L(True, 19, 0.4, 20, ctrl_e5=True), 'HAY ALGO MODESTO'), (L(True, 19, 0.4, 20, v143=0.39), 'NO SE LEE'),
             (L(True, 19, 0.4, 20, o1=False), 'NO SE LEE'), (L(True, 19, 0.4, 20, ab=1), 'NO SE LEE'),
             (L(True, 19, 0.4, 20, tm={CT.CAND: dict(a_no=1), CT.CTRL: {}}), 'NO SE LEE'), (L(False, 18, 0.4, 10), 'NO')]
    bien = sum(a == b for a, b in casos)
    chk(f"(d) la letra en {len(casos)} casos sinteticos ({bien}/{len(casos)}) · bloque(FUNCIONA, MODESTO) = {CT.bloque('FUNCIONA', 'HAY ALGO MODESTO')}",
        bien == len(casos) and CT.bloque('FUNCIONA', 'HAY ALGO MODESTO') == 'HAY ALGO MODESTO')
    print(f"ARNES {'PASA' if ok else 'FALLA'} · {time.time()-t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
