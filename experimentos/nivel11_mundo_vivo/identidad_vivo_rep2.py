"""Arnes de identidad de organismo_vivo_rep2 (bloque 2 de reproduccion). Regla 2 de registro/EQUIPO.md.

Cadena de origen: organismo_v14 (tronco, v14.1) -> organismo_vivo -> organismo_vivo_rep -> organismo_vivo_rep2.

  APAGADA (reproduccion=0): organismo_vivo_rep2 == organismo_vivo, mismas claves, en 11 escenarios x 2 semillas
      (incluye el escenario con TODAS las rep_* y rep2 encendidas y la maestra apagada: deben ser inertes).
  CADENA: rep2(vivo=0, n_nec=1) == organismo_v14, clave por clave (base e inversion).
  REP (rep2=0): rep2 == organismo_vivo_rep en TODAS las claves y con el mismo conjunto, en los 7 brazos del bloque 2.
  ENCENDIDA (rep2=1): claves viejas == organismo_vivo_rep bit a bit; solo aparecen 4 claves nuevas; las 9 claves que
      dependen del flujo del rng identicas (el rng no se consume); y COHERENCIA de los diagnosticos: len(vidas) == deaths,
      sum(vidas) + vida_final == T, desc_regalo <= descendientes.
  DEBEN FALLAR: CUELLO_MIN y REP_SIN_COSTE (con rep2=1) != organismo_vivo VIVO.

Un proceso, sin Pool (regla 3). T = 20000. OJO (ERR-28): organismo/ va primero en sys.path.
Uso:  python experimentos/nivel11_mundo_vivo/identidad_vivo_rep2.py
"""
import hashlib, json, os, sys, time

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path[:0] = [AQUI, os.path.join(RAIZ, 'organismo')]

import organismo_v14 as V14
import organismo_vivo as VV
import organismo_vivo_rep as VR
import organismo_vivo_rep2 as V2
import mini_vivo as MV
import corre_vivo_rep as C1

T = 20000
SEM = (1, 2)
NUEVAS_REP2 = {'desc_regalo', 'vidas', 'vida_final', 'rep2'}
RNG_DEP = ('split_t', 'deaths', 'mord', 'vis', 'sobre', 'llegadas', 'sin_objetivo', 'W', 'comp')


def h16(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]


def N(x):
    return json.loads(json.dumps(x, default=str))


def compara(a, b, quitar=()):
    bb = {k: v for k, v in b.items() if k not in quitar}
    falta = [k for k in a if k not in bb]
    dif = [k for k in a if k in bb and N(a[k]) != N(bb[k])]
    extra = [k for k in bb if k not in a]
    return falta, dif, extra


def caso(etiq, f_a, f_b, t0, debe_diferir=False, quitar=(), extra_esperado=None):
    ok, det = 0, ''
    for s in SEM:
        a, b = f_a(s), f_b(s)
        falta, dif, extra = compara(a, b, quitar)
        igual = (not falta and not dif and
                 ((set(extra) == extra_esperado) if extra_esperado is not None else (not extra)))
        ok += int(igual != debe_diferir)
        if (falta or dif or (extra and extra_esperado is None)) and not det:
            det = f"  falta {falta[:3]} dif {dif[:4]} extra {extra[:3]}"
    marca = 'DIFIERE (como debe)' if debe_diferir else 'IDENTICO'
    print(f"  [{time.time()-t0:6.1f}s] {etiq:62s} {ok}/{len(SEM)} {marca if ok == len(SEM) else 'FALLA' + det}", flush=True)
    return ok, len(SEM)


if __name__ == '__main__':
    t0 = time.time()
    for nom, p in [('organismo_v14 (TRONCO congelado)', os.path.join(RAIZ, 'organismo', 'organismo_v14.py')),
                   ('organismo_vivo.py', os.path.join(AQUI, 'organismo_vivo.py')),
                   ('organismo_vivo_rep.py (origen)', os.path.join(AQUI, 'organismo_vivo_rep.py')),
                   ('construye_vivo_rep2.py', os.path.join(AQUI, 'construye_vivo_rep2.py')),
                   ('organismo_vivo_rep2.py', os.path.join(AQUI, 'organismo_vivo_rep2.py'))]:
        print(f"  sha {nom:36s} {h16(p)}")
    print(f"  T = {T}, semillas {SEM}, UN proceso\n")
    ok = tot = 0
    B = MV.BRAZOS
    V14A = dict(vivo=1, n_nec=1, estims=('A', 'B'), costo_a=0.0, A_ini=1.0)
    MED2 = dict(C1.MED, rep2=1, rep2_regalo=600)
    BR2 = {b: dict(C1.BRAZOS[b], **MED2) for b in ('VIVO', 'CUELLO_MIN', 'REP_SIN_COSTE', 'UNA_NEC', 'ESCALAR', 'BARAJA_CON', 'BARAJA_POL')}

    print("APAGADA (reproduccion=0): organismo_vivo_rep2 == organismo_vivo, mismas claves")
    for etiq, kw, extra in [
            ('(A1) VIVO', B['VIVO'], dict()), ('(A2) UNA_NEC', B['UNA_NEC'], dict()), ('(A3) ESCALAR', B['ESCALAR'], dict()),
            ('(A4) BARAJA_POL', B['BARAJA_POL'], dict()), ('(A5) BARAJA_CON', B['BARAJA_CON'], dict()),
            ('(A6) NO_INFORMA', B['NO_INFORMA'], dict()), ('(A7) ancla V14 (1 necesidad, 2 estimulos)', V14A, dict()),
            ('(A8) vivo=0 base', dict(vivo=0, n_nec=1), dict()),
            ('(A9) vivo=0 con inversion en 10k', dict(vivo=0, n_nec=1, invertir_en=10000), dict()),
            ('(A10) VIVO con TODAS las rep_* y rep2 encendidas, maestra apagada', B['VIVO'],
             dict(reproduccion=0, rep_mide=1, rep_coste=0.4, rep_cuello=2, rep_X=10, rep2=1, rep2_regalo=5)),
            ('(A11) vivo=0 linaje v13 (mask_rel=0, puerta_pat=0)', dict(vivo=0, n_nec=1, mask_rel=0, puerta_pat=0), dict())]:
        a, b = caso(etiq, lambda s, kw=kw: VV.run(s, T=T, **kw), lambda s, kw=kw, extra=extra: V2.run(s, T=T, **kw, **extra), t0)
        ok += a; tot += b

    print("\nCADENA AL TRONCO: rep2(vivo=0, n_nec=1) == organismo_v14")
    a, b = caso('(B1) base', lambda s: V14.run(s, T=T), lambda s: V2.run(s, T=T, vivo=0, n_nec=1), t0); ok += a; tot += b
    a, b = caso('(B2) inversion en 10k', lambda s: V14.run(s, T=T, invertir_en=10000),
                lambda s: V2.run(s, T=T, vivo=0, n_nec=1, invertir_en=10000), t0); ok += a; tot += b

    print("\nREP (rep2=0): organismo_vivo_rep2 == organismo_vivo_rep, mismas claves, en los 7 brazos del bloque 2")
    for bname in BR2:
        kw = C1.BRAZOS[bname]
        a, b = caso(f'(C) {bname} (rep2=0)', lambda s, kw=kw: VR.run(s, T=T, **kw), lambda s, kw=kw: V2.run(s, T=T, **kw), t0)
        ok += a; tot += b

    print("\nENCENDIDA (rep2=1): claves viejas == organismo_vivo_rep + 4 nuevas; coherencia de los diagnosticos")
    for bname in ('VIVO', 'ESCALAR', 'CUELLO_MIN', 'BARAJA_POL'):
        a, b = caso(f'(D) {bname} + rep2', lambda s, k=bname: VR.run(s, T=T, **C1.BRAZOS[k]),
                    lambda s, k=bname: V2.run(s, T=T, **BR2[k]), t0, extra_esperado=NUEVAS_REP2)
        ok += a; tot += b
        coh = 0
        for s in SEM:
            r = V2.run(s, T=T, **BR2[bname])
            c = (len(r['vidas']) == r['deaths'] and sum(r['vidas']) + r['vida_final'] == T and r['desc_regalo'] <= r['descendientes'])
            coh += int(c)
            print(f"        {bname:12s} s{s}: deaths {r['deaths']} = vidas {len(r['vidas'])}; sum+final {sum(r['vidas'])+r['vida_final']} = T; "
                  f"desc {r['descendientes']} regalo {r['desc_regalo']}  -> {'coherente' if c else '*** INCOHERENTE'}")
        ok += coh; tot += len(SEM)
    a1 = VR.run(1, T=T, **C1.BRAZOS['VIVO']); b1 = V2.run(1, T=T, **BR2['VIVO'])
    print(f"        claves dependientes del rng identicas con rep2 encendido: {sum(N(a1[k]) == N(b1[k]) for k in RNG_DEP)}/{len(RNG_DEP)}")

    print("\nCONTROLES QUE DEBEN FALLAR")
    for bname in ('CUELLO_MIN', 'REP_SIN_COSTE'):
        a, b = caso(f'(E) {bname} (rep2=1) != organismo_vivo VIVO', lambda s: VV.run(s, T=T, **B['VIVO']),
                    lambda s, k=bname: V2.run(s, T=T, **BR2[k]), t0, debe_diferir=True, quitar=C1.NUEVAS_REP | NUEVAS_REP2)
        ok += a; tot += b

    print(f"\nIDENTIDAD {ok}/{tot}" + ("  -> el paquete puede correr." if ok == tot else "  -> NO se corre nada hasta que sea 100%."))
    sys.exit(0 if ok == tot else 1)
