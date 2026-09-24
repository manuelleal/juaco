"""identidad_frankenstein.py — ARNES del FRANKENSTEIN: 'todo off == tronco' BIT A BIT y los puertos verbatim.

MISION: llegar a la AGI por este camino. Un proceso, corto. Escribe identidad_frankenstein_salida.txt.
  (0) shas de origen; organismo_frankenstein.py en disco == construye_frankenstein (por anclas)
  (A) OFF == FABRICA bit a bit: pista v1 N=1 compat=1 (x2 semillas, salida entera + rng del mundo); monolito organismo_f9c (plano);
      pista v1 N=9 escalada con fundador limpio; pista v2 (generaciones, quimiostato) N=9
  (B) puertos: SOLO_MODELO == APR (fisica, pista v1 N=9); SOLO_HERENCIA == FAMB_RES de subida_n10b (fisica, pista v2 N=9)
  (C) cada organo solo, y V142 (b5), DIFIEREN de OFF (no son inertes); B-5 divide con R == 0
  (D) determinismo de TODO · (E) chequeo estatico de la carrera; los organos no leen la tabla verdadera ni sortean
  (F) corre_frankenstein.py rechaza banderas desconocidas / abreviadas sin escribir datos
"""
import json, os, subprocess, sys, time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import comun_frank as C

T0 = time.time(); OUT = []; NOK = [0, 0]


def log(s):
    print(s, flush=True); OUT.append(s)


def chk(nombre, ok, extra=''):
    NOK[0] += int(bool(ok)); NOK[1] += 1
    log(f"{'OK ' if ok else 'FALLA'} {nombre} {extra}")


N = lambda x: json.dumps(x, default=str, sort_keys=True)


def sin_carro(r):
    return N(dict(pista=r['pista'], linajes=[{k: v for k, v in d.items() if k != 'carro'} for d in r['linajes']]))


def main():
    import pista as P, pista2 as P2, revisa_carro as RC, construye_frankenstein as K
    # (0)
    for rel, h, s, ok in C.verifica_shas(): chk(f"(0) sha {rel}", ok, h)
    chk("(0) organismo_frankenstein.py == construye (anclas)", open(C.FRANK, encoding='utf-8').read() == K.construye(escribe=False), C.h16(C.FRANK))
    # (A) OFF == FABRICA
    for s in (1, 2):
        a = P.run(s, ['FABRICA'], T=5000, pizarra=0, compat=1); b = P.run(s, [C.carro('OFF', 'FABRICA')], T=5000, pizarra=0, compat=1)
        chk(f"(A1) N1 compat s{s} T5000 salida entera", N(a) == N(b), f"rng {b['pista']['rng_mundo_estado']} muertes {b['linajes'][0]['deaths']}")
    sys.path[:0] = [os.path.join(C.RAIZ, 'experimentos', d) for d in
                    ('nivel09_cuerpo_nuevo_b2', 'nivel09_cuerpo_nuevo', 'nivel13_alma', 'nivel11_mundo_vivo')] + [os.path.join(C.RAIZ, 'organismo')]
    _a = sys.argv; sys.argv = [sys.argv[0]]
    import corre_bloque2 as CB, organismo_f9c as F9C
    sys.argv = _a
    m = F9C.run(1, T=5000, **CB.BRAZOS['REL'])
    f = P.plano(P.run(1, [C.carro('OFF', 'FABRICA')], T=5000, pizarra=0, compat=1)['linajes'][0])
    dif = [k for k in m if k not in f or N(m[k]) != N(f[k])] + [k for k in f if k not in m]
    chk("(A2) monolito organismo_f9c(REL) == OFF (plano)", not dif, f"{len(m)} claves, dif {dif}")
    a = P.run(17990, ['FABRICA'] * 9, T=3000, fundador_limpio=1); b = P.run(17990, [C.carro('OFF', 'FABRICA')] * 9, T=3000, fundador_limpio=1)
    chk("(A3) N9 escalada fundador limpio s17990 T3000 salida entera", N(a) == N(b), f"rng {b['pista']['rng_mundo_estado']}")
    a = P2.run(17991, ['FABRICA'] * 9, T=3000, diag=0, solapadas=1, reposicion='fija')
    b = P2.run(17991, [C.carro('OFF', 'FABRICA')] * 9, T=3000, diag=0, solapadas=1, reposicion='fija')
    chk("(A4) pista v2 quimiostato N9 s17991 T3000 salida entera", N(a) == N(b), f"individuos {sum(len(d['individuos']) for d in b['linajes'])}")
    # (B) puertos
    a = P.run(17992, ['APR'] * 9, T=4000, fundador_limpio=1); b = P.run(17992, [C.carro('SOLO_MODELO', 'APR')] * 9, T=4000, fundador_limpio=1)
    ap = [d['carro']['apr'] for d in a['linajes']]; bp = [d['carro']['frank']['apr'] for d in b['linajes']]
    chk("(B1) SOLO_MODELO == APR (fisica + telemetria de la opcion) N9 s17992 T4000", sin_carro(a) == sin_carro(b) and N(ap) == N(bp),
        f"decisiones {sum(x['fab_mord'] + 0 for x in bp)} td {sum(x['td_n'] for x in bp)}")
    fr = C.carga_mod('FAMB_RES', os.path.join(C.N10B, 'carros', 'FAMB_RES.py'))
    a = P2.run(17993, [('FAMB_RES', fr)] * 9, T=4000, diag=0, solapadas=1, reposicion='fija')
    b = P2.run(17993, [C.carro('SOLO_HERENCIA', 'FAMB_RES')] * 9, T=4000, diag=0, solapadas=1, reposicion='fija')
    chk("(B2) SOLO_HERENCIA == FAMB_RES (subida_n10b) pista v2 N9 s17993 T4000", sin_carro(a) == sin_carro(b),
        f"nacimientos {sum(d['nacimientos'] for d in b['linajes'])} paquetes {sum(d['carro']['frank']['paquetes'] for d in b['linajes'])}")
    # (C) no inertes
    base = sin_carro(P.run(17994, [C.carro('OFF', 'X')] * 9, T=4000, fundador_limpio=1))
    for br in ['V142'] + ['SOLO_' + o.upper() for o in C.frank().ORGANOS]:
        r = P.run(17994, [C.carro(br, 'X')] * 9, T=4000, fundador_limpio=1)
        fk = [d['carro'].get('frank', {}) for d in r['linajes']]
        tel = dict(des=sum(x.get('des_splits', 0) for x in fk), mapa=sum(x.get('pasos_mapa', 0) for x in fk),
                   pruebas=sum(x.get('pruebas', 0) for x in fk), vetos=sum(x.get('vetos_peligro', 0) for x in fk),
                   lenta=sum(x.get('lenta_usa', 0) for x in fk), repasos=sum(x.get('repasos', 0) for x in fk))
        chk(f"(C) {br} difiere de OFF (s17994 T4000)", sin_carro(r) != base, str(tel))
        if br == 'V142': chk("(C) V142: B-5 divide con R == 0", tel['des'] > 0, f"des_splits {tel['des']}")
    # (D)
    a = P.run(17995, [C.carro('TODO', 'X')] * 9, T=2000, fundador_limpio=1); b = P.run(17995, [C.carro('TODO', 'X')] * 9, T=2000, fundador_limpio=1)
    chk("(D) determinismo TODO s17995 T2000", N(a) == N(b))
    # (E)
    v = RC.revisa_fuente(open(C.FRANK, encoding='utf-8').read(), 'organismo_frankenstein')
    chk("(E1) revisa_carro (chequeo estatico de la carrera)", not v, str(v[:3]))
    org = open(os.path.join(AQUI, 'organos_frank.py'), encoding='utf-8').read()
    chk("(E2) los organos no nombran la tabla verdadera (VAL_VIVO/EFECTO/fabrica)", all(w not in org for w in ('VAL_VIVO', 'EFECTO', "ctx['fabrica']")))
    chk("(E3) los organos no sortean (sin rng propio)", 'rng' not in org.replace('rng_hijo', ''))
    # (F)
    ante = set(os.listdir(os.path.join(AQUI, 'datos')))
    malas = [['--bogus'], ['--hum'], ['--mundo', 'carrera', '--brazos', 'TODO', '--semillas', '17001', '--T', '1000', '--pool', '6'],
             ['--mundo', 'luna', '--brazos', 'TODO', '--semillas', '17001', '--T', '1000'],
             ['--mundo', 'carrera', '--brazos', 'NADA', '--semillas', '17001', '--T', '1000'],
             ['--mundo', 'carrera', '--brazos', 'TODO', '--semillas', '4001', '--T', '1000'],
             ['--mundo', 'carrera', '--brazos', 'TODO,OFF,V142', '--semillas', '17001,17002,17003', '--T', '1000'],
             ['--mundo', 'carrera', '--brazos', 'TODO', '--semillas', '17001', '--T', '300000']]
    rcs = [subprocess.run([sys.executable, os.path.join(AQUI, 'corre_frankenstein.py')] + m, capture_output=True).returncode for m in malas]
    chk("(F) corre_frankenstein aborta las 8 formas malas (codigo != 0) y no escribe datos",
        all(x != 0 for x in rcs) and set(os.listdir(os.path.join(AQUI, 'datos'))) == ante, str(rcs))
    log(f"RESULTADO: {NOK[0]}/{NOK[1]}  ({time.time() - T0:.0f} s)")
    open(os.path.join(AQUI, 'identidad_frankenstein_salida.txt'), 'w', encoding='utf-8').write(
        time.strftime('%Y-%m-%d %H:%M:%S') + '\n' + '\n'.join(OUT) + '\n')


if __name__ == '__main__':
    if len(sys.argv) > 1: raise SystemExit("identidad_frankenstein: sin argumentos")
    main()
