"""identidad_termob.py -- ARNES del CARRO V143_TERMOB (TERMO' en la pista de la carrera, para el muro). UN proceso; se corre ANTES de
cualquier humo o serie del carro. Salida -> identidad_termob_salida.txt. Modelo: experimentos/organelos/termo/identidad_termo.py.
MISION: llegar a la AGI por este camino.

  (K) carros/V143_TERMOB.py en disco == construye_v144b.construye() (por anclas desde V143_TERMO, 3db639cab75641fb)
  (a) V143_TERMOB con TERMO = 0 == V143, salida ENTERA (N 9, fundador limpio; s 49091 T 2000)
  (b) V143_TERMOB == V143_TERMO en la FISICA de la pista (todo salvo d['carro']) y en la telemetria de la pieza (d['carro']['termo'])
      con 9 carros, fundador_limpio = 1: s 49091 T 5000 y s 49092 T 20000. En la pista el dS por letra es fijo: la tabla que olvida
      (el ultimo dS) debe decidir lo mismo que la media de APR. Si difiere, se reporta la primera linea distinta (no se ajusta nada).
  (c) TERMO = 2 (TERMOINV con la tabla que olvida) == V143_TERMOINV en la fisica (s 49091 T 5000); la pieza actua en los dos
  (d) determinismo; la pieza lee SU tabla (_tmS) y no la suma de APR (_adS): caso sintetico con _adS "buena" y _tmS "mala".
Semillas de practica 49091-49094 (fuera de todos los papeles de umbrales_examen_v144b.SEMILLAS; no son de ninguna serie).

    python experimentos/tronco_v14_4b_examen/identidad_termob.py
"""
import importlib.util, json, os, sys, time

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
TERMO_DIR = os.path.join(RAIZ, 'experimentos', 'organelos', 'termo')
sys.path.insert(0, TERMO_DIR)
sys.path.insert(0, AQUI)
import corre_termo as CT          # registra V143_TERMO / V143_TERMOINV en la cache de corre_v143 (solo se importa)
import construye_v144b as CO
P = CT.P; CV = CT.CV
N = lambda x: json.loads(json.dumps(x, default=str))


def carga(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


def fis(r):
    out = dict(r); out['linajes'] = [{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']]; return out


def tele(r):
    return [(d.get('carro') or {}).get('termo') for d in r['linajes']]


def primera(a, b):
    la, lb = a['linajes'], b['linajes']
    for i, (x, y) in enumerate(zip(la, lb)):
        for k in sorted(set(x) | set(y)):
            if k != 'carro' and x.get(k) != y.get(k):
                return f"linaje {i}, clave {k!r}: {json.dumps(x.get(k), default=str)[:160]} != {json.dumps(y.get(k), default=str)[:160]}"
    ks = [k for k in a if k != 'linajes' and a.get(k) != b.get(k)]
    return f'claves globales distintas {ks[:6]}'


def main():
    ok = True; t0 = time.time()

    def chk(nombre, cond, det=''):
        nonlocal ok; ok &= bool(cond); print(f"  [{time.time() - t0:5.0f}s] {'OK   ' if cond else 'FALLA'} {nombre}" + ('' if cond or not det else f'  -> {det}'), flush=True)

    ruta = os.path.join(AQUI, 'carros', 'V143_TERMOB.py')
    chk('(K) carros/V143_TERMOB.py en disco == construccion por anclas (origen V143_TERMO 3db639cab75641fb)',
        open(ruta, 'rb').read().decode('utf-8') == CO.construye()['carros/V143_TERMOB.py'])
    CT.registra()
    V143 = CV.modulo('V143'); TM = CV._MODS['V143_TERMO']; TI = CV._MODS['V143_TERMOINV']
    TB = carga('carro_V143_TERMOB', ruta)
    print(f"  sha V143_TERMOB {CO.h16(ruta)} · V143_TERMO {CO.h16(TM.__file__)} · V143_TERMOINV {CO.h16(TI.__file__)} · pista {CO.h16(P.__file__)}")
    run = lambda m, s, T: N(P.run(s, [('C', m)] * 9, T=T, pizarra=1, rep_acum=0, escala=1, mundo_n=None, fundador_limpio=1))

    g = TB.TERMO
    try:
        TB.TERMO = 0; x = run(TB, 49091, 2000)
    finally:
        TB.TERMO = g
    chk('(a) V143_TERMOB con TERMO = 0 == V143, salida ENTERA (N 9, s 49091, T 2000, fundador limpio)', x == run(V143, 49091, 2000))

    R = {}
    for s, T in ((49091, 5000), (49092, 20000)):
        b, a = run(TB, s, T), run(TM, s, T); R[(s, T)] = b
        chk(f"(b) V143_TERMOB == V143_TERMO en la FISICA de la pista (todo salvo d['carro']; N 9, s {s}, T {T})", fis(b) == fis(a),
            '' if fis(b) == fis(a) else primera(b, a))
        chk(f"(b) ... y en la telemetria de la pieza (dec, a_no, a_si, mord por linaje; s {s}, T {T})", tele(b) == tele(a))
    g = TB.TERMO
    try:
        TB.TERMO = 2; bi = run(TB, 49091, 5000)
    finally:
        TB.TERMO = g
    ai = run(TI, 49091, 5000)
    chk('(c) V143_TERMOB con TERMO = 2 (TERMOINV con la tabla que olvida) == V143_TERMOINV en la fisica (s 49091, T 5000)', fis(bi) == fis(ai),
        '' if fis(bi) == fis(ai) else primera(bi, ai))
    act = lambda r: any(t and (t['a_no'] + t['a_si']) > 0 for t in tele(r))
    chk(f"(c) la pieza ACTUA en TERMO' y en su TERMOINV (a_no + a_si > 0): {tele(R[(49091, 5000)])[0]} · {tele(bi)[0]}", act(R[(49091, 5000)]) and act(bi))
    chk('(c) TERMOINV != TERMO\' en la fisica (s 49091, T 5000)', fis(bi) != fis(R[(49091, 5000)]))
    chk('(d) determinismo: V143_TERMOB dos corridas iguales (s 49091, T 5000)', run(TB, 49091, 5000) == R[(49091, 5000)])
    c = object.__new__(TB.Carro)
    c._adS = {'X': [8.0, 0.0, 10]}; c._tmS = {'X': [-0.4, 0.0, 1]}; c._tmU = 1.0; c._tm = dict(dec=0, a_no=0, a_si=0, mord=0)
    b1 = c._tm_boca('X', 0.5, 1.2, True); b2 = c._tm_boca('X', 1.45, 1.2, True)
    c._tmS = {'X': [0.8, 0.0, 1]}
    b3 = c._tm_boca('X', 1.45, 1.2, True); b4 = c._tm_boca('X', 1.2, 1.2, False)
    chk(f"(d) la pieza lee _tmS (el ultimo dS), no la suma de APR: _tmS mala -> la boca de v14.3 ({b1}, {b2}); _tmS buena -> termostato "
        f"(E 1.45 no muerde: {b3}; E 1.2 muerde: {b4})", b1 is True and b2 is True and b3 is False and b4 is True and c._tm['dec'] == 2)
    print(f"ARNES {'PASA' if ok else 'FALLA'} · {time.time() - t0:.0f}s")
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
