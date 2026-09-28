"""identidad_termo.py — ARNES del bloque TERMO (un proceso; se corre ANTES del humo y de la serie). Salida -> identidad_termo_salida.txt.

MISION: llegar a la AGI por este camino.
  (K) construye_termo --verifica: carros en disco == construidos por anclas desde V143.py (sha fijado); difieren solo en perillas/nombre
  (a) V143_TERMO y V143_TERMOINV con TERMO = 0 == V143, salida ENTERA (N 9, fundador limpio; s 39913 T 2000 y s 39914 T 5000)
  (b) V143_TERMO == HIBB (boca_buena/carros, BB 'm40', puente boca_buena) en la FISICA bit a bit (todo salvo d['carro']; s 39913 T 5000,
      s 39914 T 20000): la pieza es exactamente el brazo m40 del diagnostico
  (c) V143_TERMOINV == HIBB BB 'tinv40' en la fisica (s 39913 T 5000); TERMOINV != TERMO en la fisica; y la pieza actua en los dos
  (d) corre_termo.verifica(): shas FIJADOS de todo lo que corre (runner, construye, carros, V143, pista, juez, O1, corre_v143,
      revisa_carro) + revisa_carro + identidad corta. Mas: determinismo, valida() rechaza semillas/T/brazos fuera del preregistro,
      ERR-115 (bandera abreviada aborta) y la letra en casos sinteticos.
Uso: python experimentos/organelos/termo/identidad_termo.py
"""
import json, os, sys, time, importlib.util

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_termo as CT
import construye_termo as CB
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

    chk("(K) construye_termo --verifica (carros == anclas desde V143.py 2a03048a7f1525e5; solo perillas/nombre)", CB.main(['--verifica']) == 0)
    CT.registra()
    V143 = CV.modulo('V143'); TM = CV._MODS['V143_TERMO']; TI = CV._MODS['V143_TERMOINV']
    run = lambda m, s, T: N(P.run(s, [('C', m)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1))
    for s, T in ((39913, 2000), (39914, 5000)):
        base = run(V143, s, T)
        for nm, m in (('V143_TERMO', TM), ('V143_TERMOINV', TI)):
            g = m.TERMO
            try:
                m.TERMO = 0; x = run(m, s, T)
            finally:
                m.TERMO = g
            chk(f"(a) {nm} con TERMO = 0 == V143, salida ENTERA (N 9, s {s}, T {T}, fundador limpio)", x == base)

    from hashlib import sha256
    sh = sha256(open(HIBB_RUTA, 'rb').read()).hexdigest()[:16]
    chk(f"(b0) HIBB del diagnostico sha {sh} == {SHA_HIBB}", sh == SHA_HIBB)
    spec = importlib.util.spec_from_file_location('HIBB_termo', HIBB_RUTA); H = importlib.util.module_from_spec(spec); spec.loader.exec_module(H)

    def hibb(bb, s, T):
        H.PUENTES = dict(patas=0, boca_buena=1, boca_mala=0, memoria=0); H.BB = bb; return run(H, s, T)
    fis = lambda r: sin(r, ('carro',))
    R = {}
    for s, T in ((39913, 5000), (39914, 20000)):
        R[(s, T)] = run(TM, s, T)
        chk(f"(b) V143_TERMO == HIBB m40 en la FISICA (todo salvo d['carro']; s {s}, T {T})", fis(R[(s, T)]) == fis(hibb('m40', s, T)))
    ri = run(TI, 39913, 5000)
    chk("(c) V143_TERMOINV == HIBB tinv40 en la FISICA (s 39913, T 5000)", fis(ri) == fis(hibb('tinv40', 39913, 5000)))
    chk("(c) V143_TERMOINV != V143_TERMO en la fisica (s 39913, T 5000)", fis(ri) != fis(R[(39913, 5000)]))
    tt = CT.tm_suma([dict(tel_termo=[d['carro'].get('termo') for d in R[(39913, 5000)]['linajes']])])
    ti = CT.tm_suma([dict(tel_termo=[d['carro'].get('termo') for d in ri['linajes']])])
    print(f"       telemetria termo {tt} · termoinv {ti}")
    chk("(c) la pieza ACTUA en TERMO y en TERMOINV (V4: a_no + a_si > 0)", CT.pieza(tt) and CT.pieza(ti))
    chk("(c) determinismo: V143_TERMO dos corridas iguales (s 39913, T 5000)", run(TM, 39913, 5000) == R[(39913, 5000)])

    lines = []
    chk("(d) corre_termo.verifica(): shas fijados + carros == construye + revisa_carro + identidad corta", CT.verifica(lines.append))
    for l in lines: print("     " + l)
    chk("(d) valida: serie 39101-39120 con los 4 brazos y T 100000 -> OK", CT.valida(False, 39101, 20, 100000, list(CT.SERIE_BRAZOS)) is None)
    chk("(d) valida: replica 39121-39140 -> OK", CT.valida(False, 39121, 20, 100000, list(CT.SERIE_BRAZOS)) is None)
    chk("(d) valida: rechaza semillas del exploratorio 39001", CT.valida(False, 39001, 10, 100000, list(CT.SERIE_BRAZOS)) is not None)
    chk("(d) valida: rechaza serie mezclada 39111-39130", CT.valida(False, 39111, 20, 100000, list(CT.SERIE_BRAZOS)) is not None)
    chk("(d) valida: rechaza T 50000 en serie", CT.valida(False, 39101, 20, 50000, list(CT.SERIE_BRAZOS)) is not None)
    chk("(d) valida: rechaza brazos distintos", CT.valida(False, 39101, 20, 100000, ['v143', 'termo', 'o1']) is not None)
    chk("(d) valida: humo solo 39911-39914 y T <= 30000", CT.valida(True, 39101, 1, 20000, ['termo']) is not None and CT.valida(True, 39911, 2, 40000, ['termo']) is not None)
    try:
        CT.main(['--humo', '--desd', '39911']); e115 = False
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
