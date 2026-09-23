"""identidad_apr.py — ARNES de identidad de APR (camino A, aprende_barrer). Un proceso, sin Pool. Se corre y se pega
ENTERO en el informe ANTES de mirar un solo numero de humo.

MISION: llegar a la AGI por este camino.
  (0) origen: FABRICA.py tiene el sha fijado y los tres carros en disco son EXACTAMENTE los que genera construye_apr.py.
  (A) APR con OPCION = 0 == FABRICA BIT A BIT (salida completa de la pista: linajes con telemetria del carro, pista y
      estado final del rng del mundo). N = 1, compat = 1, pizarra 0, semillas 1-3, T = 20000.
  (A2) APR con OPCION = 0 == organismo_f9c.run(**REL) (el monolito), como la identidad corta del juez (s = 1, T = 5000).
  (B) N = 9 en la pista escalada (la de la serie): APR, APR_SIN_HERENCIA y APR_AZAR con OPCION = 0 == 9 FABRICA, s 8001, T = 3000.
  (C) DEBE DIFERIR (ERR-38): con OPCION = 1 la corrida cambia y la opcion decide (> 0 oportunidades).
  (C2) v3: con OPCION = 1 y ALFA_Q = 0 (Q congelado en 0) la fisica es la de FABRICA bit a bit: la opcion arranca en FABRICA.
  (D) determinismo con OPCION = 1.
  (E) la opcion actua SOLO sobre letras malas (lo verifica el arnes con la tabla verdadera, que el carro no lee) y el
      carro no menciona VAL_VIVO / EFECTO / el rng del mundo; revisa_carro PASA los tres.
  (F) herencia: en APR el valor de la opcion llega al cuerpo siguiente (norma > 0 al nacer); en APR_SIN_HERENCIA nace en 0.
  (G) APR_AZAR sin P_AZAR aborta; con P_AZAR = 0.3 muerde el ~30 % de las oportunidades.
Uso: python experimentos/aprende_barrer/identidad_apr.py   (escribe identidad_apr_salida.txt)
"""
import json, os, sys, time, types

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
PISTA = os.path.join(RAIZ, 'experimentos', 'carrera_escuderias')
sys.path[:0] = [AQUI, PISTA]
import numpy as np
import pista as P
import revisa_carro as RC
import construye_apr as CA

N = lambda x: json.loads(json.dumps(x, default=str))
OK = [0, 0]
SAL = open(os.path.join(AQUI, 'identidad_apr_salida.txt'), 'w', encoding='utf-8')


def out(s=''):
    print(s, flush=True); SAL.write(s + '\n'); SAL.flush()


def di(et, ok, extra=''):
    OK[1] += 1; OK[0] += int(bool(ok))
    out(f"  {'OK   ' if ok else 'FALLA'} {et}   {extra}")


def mod(ident, opcion=None, p_azar=None, clase=None):
    m = P.carga_carro(ident)
    if opcion is not None: m.OPCION = opcion
    if p_azar is not None: m.P_AZAR = p_azar
    if clase is not None:
        base = m.Carro; C = clase(base); return ('C', types.SimpleNamespace(crea=lambda ctx: C(ctx)))
    return ('C', m)


def main():
    t0 = time.time()
    out(f"IDENTIDAD APR · {time.strftime('%Y-%m-%d %H:%M:%S')} · UN proceso, sin Pool · python {sys.version.split()[0]} · numpy {np.__version__}")
    out(f"  pista.py {P.h16(os.path.join(PISTA, 'pista.py'))} · FABRICA {P.h16(os.path.join(P.CARROS, 'FABRICA.py'))} · "
        + ' · '.join(f"{n} {P.h16(os.path.join(P.CARROS, n + '.py'))}" for n, _ in CA.VARIANTES))
    out("\n(0) ORIGEN Y CONSTRUCCION")
    di('FABRICA.py sha fijado', P.h16(os.path.join(P.CARROS, 'FABRICA.py')) == CA.SHA_FABRICA, CA.SHA_FABRICA)
    pa = P.carga_carro('APR_AZAR').P_AZAR
    for n, m in CA.VARIANTES:
        b = CA.construye(n, m, pa)
        di(f"{n}.py en disco == construye_apr ({m}, P_AZAR {pa})", open(os.path.join(P.CARROS, n + '.py'), 'rb').read() == b)

    out("\n(A) APR con OPCION = 0 == FABRICA bit a bit · N = 1, compat 1, pizarra 0, T = 20000")
    for sd in (1, 2, 3):
        a = P.run(sd, [mod('FABRICA')], T=20000, pizarra=0, compat=1)
        b = P.run(sd, [mod('APR', opcion=0)], T=20000, pizarra=0, compat=1)
        la, lb = a['linajes'][0], b['linajes'][0]
        di(f"(A) s={sd}", N(a) == N(b), f"R0 {la['descendientes']}/{la['deaths'] + 1} vs {lb['descendientes']}/{lb['deaths'] + 1} · "
           f"rng mundo {a['pista']['rng_mundo_estado']}/{b['pista']['rng_mundo_estado']} · 'apr' en carro: {'apr' in lb['carro']}")

    out("\n(A2) APR con OPCION = 0 == organismo_f9c.run(**REL) (monolito), s = 1, T = 5000")
    sys.path[:0] = [os.path.join(RAIZ, 'experimentos', d) for d in
                    ('nivel09_cuerpo_nuevo_b2', 'nivel09_cuerpo_nuevo', 'nivel13_alma', 'nivel11_mundo_vivo')] + [os.path.join(RAIZ, 'organismo')]
    _a = sys.argv; sys.argv = [sys.argv[0]]
    import corre_bloque2 as CB, organismo_f9c as F9C
    sys.argv = _a
    a = F9C.run(1, T=5000, **CB.BRAZOS['REL'])
    b = P.plano(P.run(1, [mod('APR', opcion=0)], T=5000, pizarra=0, compat=1)['linajes'][0])
    dif = [k for k in a if k not in b or N(a[k]) != N(b[k])] + [k for k in b if k not in a and k != '_carrera']
    di('(A2) monolito == APR(OPCION 0)', not dif and P.h16(P.ORIGEN) == P.SHA_F9C, f"claves {len(a)} · dif {dif[:5]} · sha f9c {P.h16(P.ORIGEN)}")

    out("\n(B) N = 9, pista escalada (L 360, 36 objetos, pizarra 1): variantes con OPCION = 0 == 9 FABRICA · s 8001, T = 3000")
    ref = P.run(8001, [mod('FABRICA')] * 9, T=3000)
    for n, _ in CA.VARIANTES:
        r = P.run(8001, [mod(n, opcion=0, p_azar=0.5 if n == 'APR_AZAR' else None)] * 9, T=3000)
        di(f"(B) {n}", N(r) == N(ref), f"muertes {[l['deaths'] for l in r['linajes']]} · rng {r['pista']['rng_mundo_estado']}/{ref['pista']['rng_mundo_estado']}")

    out("\n(C) DEBE DIFERIR: APR con OPCION = 1 != FABRICA, y la opcion decide")
    r1 = P.run(8001, [mod('APR')] * 9, T=3000)
    opp = [l['carro']['apr']['opp_q'] for l in r1['linajes']]
    di('(C) OPCION 1 cambia la corrida', N(r1['linajes']) != N(ref['linajes']) and sum(map(sum, opp)) > 0,
       f"oportunidades por linaje {[sum(o) for o in opp]} · mordidas {[sum(l['carro']['apr']['mord_q']) for l in r1['linajes']]}")

    out("\n(C2) v3: con OPCION = 1 y el aprendizaje CONGELADO (ALFA_Q = 0 -> Q1 = Q0 = 0) APR muerde EXACTAMENTE como FABRICA")
    m0 = P.carga_carro('APR'); m0.ALFA_Q = 0.0
    rc = P.run(8001, [('C', m0)] * 9, T=3000)
    sin = lambda r: [dict({k: v for k, v in d.items() if k != 'carro'}, carro={k: v for k, v in d['carro'].items() if k != 'apr'}) for d in r['linajes']]
    di('(C2) fisica + telemetria de FABRICA identicas; la opcion decidio y coincidio con la boca de FABRICA',
       N(sin(rc)) == N(sin(ref)) and N(rc['pista']) == N(ref['pista'])
       and all(l['carro']['apr']['fab_mord'] == sum(l['carro']['apr']['mord_q']) for l in rc['linajes']),
       f"oportunidades {sum(sum(l['carro']['apr']['opp_q']) for l in rc['linajes'])} · mordidas {sum(sum(l['carro']['apr']['mord_q']) for l in rc['linajes'])} "
       f"= FABRICA habria {sum(l['carro']['apr']['fab_mord'] for l in rc['linajes'])}")

    out("\n(D) DETERMINISMO con OPCION = 1")
    r2 = P.run(8001, [mod('APR')] * 9, T=3000)
    di('(D) dos corridas iguales', N(r1) == N(r2))

    out("\n(E) LA OPCION ACTUA SOLO SOBRE LETRAS MALAS; el carro no lee la tabla verdadera ni el rng del mundo")
    CF = P.cfg_fabrica(); VV, EF = CF['VAL_VIVO'], CF['EFECTO']   # SOLO el arnes usa la tabla verdadera
    vistas = []
    def espia(base):
        class S(base):
            def _opcion(self, obs, kk, mf, u9, pb):
                r = base._opcion(self, obs, kk, mf, u9, pb)
                if self._apend is not None and self._apend[3] == int(obs['t']): vistas.append(kk)
                return r
        return S
    P.run(8002, [mod('APR', clase=espia)] * 9, T=3000)
    malas = sum(1 for k in vistas if min(EF[VV[k]]) < 0)
    di('(E1) toda decision de la opcion es sobre B o D (letras con algun efecto negativo)', vistas and malas == len(vistas),
       f"decisiones {len(vistas)} · sobre letras malas {malas} · por letra { {k: vistas.count(k) for k in 'ABCD'} }")
    prohib = []
    for n, _ in CA.VARIANTES:
        s = open(os.path.join(P.CARROS, n + '.py'), encoding='utf-8').read()
        prohib += [f"{n}:{w}" for w in ('VAL_VIVO', 'EFECTO', "'mundo'", 'rng_mundo') if w in s]
    di('(E2) los carros APR no nombran VAL_VIVO / EFECTO / el rng del mundo', not prohib, str(prohib))
    rv = {n: RC.revisa(n) for n, _ in CA.VARIANTES}
    di('(E3) revisa_carro PASA APR, APR_SIN_HERENCIA, APR_AZAR', not any(rv.values()), str({k: len(v) for k, v in rv.items()}))

    out("\n(F) HERENCIA del valor de la opcion al cuerpo siguiente del linaje")
    for n, espera in (('APR', 'mayor que 0'), ('APR_SIN_HERENCIA', '0')):
        normas = []
        def espia_n(base):
            class S(base):
                def _apr_nace(self, info):
                    base._apr_nace(self, info); normas.append(float(np.abs(self._aw).sum()))
            return S
        P.run(8003, [mod(n, clase=espia_n)] * 9, T=3000)
        tarde = normas[len(normas) // 2:]
        ok = (min(tarde) > 0 if n == 'APR' else max(normas) == 0.0) and len(normas) > 10
        di(f"(F) {n}: |Q| al nacer {espera}", ok, f"nacimientos {len(normas)} · |Q| al nacer (2a mitad) min {min(tarde):.4f} max {max(tarde):.4f}")

    out("\n(G) APR_AZAR")
    try:
        P.run(1, [mod('APR_AZAR', p_azar=None)], T=10); ok, msg = False, 'NO aborto'
    except SystemExit as e:
        ok, msg = True, str(e)[:90]
    di('(G1) sin P_AZAR aborta al crearse', ok, msg)
    rz = P.run(8001, [mod('APR_AZAR', p_azar=0.3)] * 9, T=3000)
    so = sum(sum(l['carro']['apr']['opp_q']) for l in rz['linajes']); sm = sum(sum(l['carro']['apr']['mord_q']) for l in rz['linajes'])
    di('(G2) con P_AZAR = 0.3 muerde el 0.3 de las oportunidades (+- 4 sigma)', so > 50 and abs(sm / so - 0.3) < 4 * (0.21 / so) ** .5,
       f"{sm}/{so} = {sm / max(so, 1):.3f}")
    out(f"\nTOTAL {OK[0]}/{OK[1]} en {time.time() - t0:.1f}s")
    SAL.close()
    return 0 if OK[0] == OK[1] else 1


if __name__ == '__main__':
    sys.exit(main())
