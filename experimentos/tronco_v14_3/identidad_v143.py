"""identidad_v143.py — ARNES del bloque tronco_v14_3. Se corre ANTES de mirar cualquier numero de conducta.

MISION: llegar a la AGI por este camino. Con las perillas apagadas (DESAMB = FILTRO = OPCION = 0) cada carro de carros_v143/ es
FABRICA BIT A BIT (y FABRICA == organismo_f9c REL, el monolito del mundo vivo); con solo OPCION es APR bit a bit (la pieza 2 es la
de aprende_barrer, no otra); B-5 es el literal de organismo_v142.py y solo divide con R == 0 (verificado contra la tabla verdadera,
que el ARNES si puede leer y el carro no); el FILTRO nunca deja morder ni apuntar a un obstaculo con meta; sin meta no hay
obstaculos (salvo en la lesion SIEMPRE); el corredor aborta ante banderas desconocidas y semillas ajenas; su entrada == juez.tarea.
Un proceso, sin Pool. Ultima linea: "RESULTADO: N/N". JSON en experimentos/tronco_v14_3/datos/humo/.

    python experimentos/tronco_v14_3/identidad_v143.py
"""
import hashlib, json, os, subprocess, sys, time, types

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import corre_v143 as C
P, J, RC, CV = C.P, C.J, C.RC, C.CV

OK = []; FILAS = []
def chk(nombre, cond, extra=''):
    OK.append(bool(cond)); FILAS.append(dict(n=len(OK), prueba=nombre, ok=bool(cond), extra=str(extra)[:300]))
    print(f"  [{len(OK):2d}] {'OK   ' if cond else 'FALLA'} {nombre}{(' · ' + str(extra)) if extra else ''}", flush=True)

N = lambda x: json.loads(json.dumps(x, default=str))


class Perillas:
    """cambia las perillas de un modulo de carro y las devuelve al salir (el modulo se comparte en el proceso)."""
    def __init__(self, m, **kw): self.m = m; self.kw = kw
    def __enter__(self):
        self.old = {k: getattr(self.m, k) for k in self.kw}
        for k, v in self.kw.items(): setattr(self.m, k, v)
        return self.m
    def __exit__(self, *a):
        for k, v in self.old.items(): setattr(self.m, k, v)


APAGADO = dict(DESAMB=0, FILTRO=0, OPCION=0)


def main():
    t0 = time.time()
    print(f"IDENTIDAD tronco_v14_3 · {time.strftime('%Y-%m-%d %H:%M:%S')} · corre_v143 {C.h16(os.path.join(AQUI, 'corre_v143.py'))} · "
          f"construye_v143 {C.h16(os.path.join(AQUI, 'construye_v143.py'))}")
    # (0) origenes y carros en disco
    malos = [os.path.relpath(r, C.RAIZ) for r, s in C.SHAS.items() if C.h16(r) != s]
    chk("(0a) sha de pista, juez, FABRICA, O1, APR, organismo_v142 (congelado)", not malos, malos or 'todos OK')
    outs = CV.todas()
    dif = [n for n, b in outs.items() if open(os.path.join(C.CARROS_V, n + '.py'), 'rb').read() != b]
    chk("(0b) carros_v143/*.py == construye_v143 (6 variantes; solo difieren en perillas)", not dif, dif or {n: CV.h16b(b) for n, b in outs.items()})
    # (1) chequeo estatico + tokens de la tabla verdadera
    for n, b in outs.items():
        v = RC.revisa_fuente(b.decode('utf-8'), n)
        chk(f"(1) revisa_carro PASA {n}", not v, v[:2])
    tok = [n for n, b in outs.items() if any(t in b.decode('utf-8') for t in ('VAL_VIVO', 'EFECTO', "['fabrica']['VAL", 'rng_mundo'))]
    chk("(1b) ningun carro nombra la tabla verdadera (VAL_VIVO / EFECTO) ni el rng del mundo", not tok, tok)
    FAB = C.modulo('FABRICA'); V3 = C.modulo('V143')
    # (2) perillas en 0 == FABRICA, N 1 compat 1 (== el ancla del monolito), 3 semillas
    for s in (1, 2, 3):
        with Perillas(V3, **APAGADO):
            b = P.run(s, [('C', V3)], T=20000, pizarra=0, compat=1)
        a = P.run(s, [('C', FAB)], T=20000, pizarra=0, compat=1)
        la = a['linajes'][0]; lb = b['linajes'][0]
        chk(f"(2) perillas 0 == FABRICA, N 1 compat 1 T 20000 s{s} (todo, rng del mundo incluido)", N(a) == N(b),
            f"R0 {la['descendientes']}/{la['deaths']} rng {a['pista']['rng_mundo_estado']}")
    # (3) monolito organismo_f9c REL == plano(perillas 0)
    sys.path[:0] = [os.path.join(C.RAIZ, 'experimentos', d) for d in ('nivel09_cuerpo_nuevo_b2', 'nivel09_cuerpo_nuevo', 'nivel13_alma', 'nivel11_mundo_vivo')] + [os.path.join(C.RAIZ, 'organismo')]
    _a = sys.argv; sys.argv = [sys.argv[0]]
    import corre_bloque2 as CB, organismo_f9c as F9C
    sys.argv = _a
    m0 = F9C.run(1, T=5000, **CB.BRAZOS['REL'])
    with Perillas(V3, **APAGADO):
        p0 = P.plano(P.run(1, [('C', V3)], T=5000, pizarra=0, compat=1)['linajes'][0])
    d0 = [k for k in m0 if k not in p0 or N(m0[k]) != N(p0[k])] + [k for k in p0 if k not in m0]
    chk("(3) monolito organismo_f9c REL (sha 9dd1fb91ecec35ae) == V143 con perillas 0 (vista plana, s1 T 5000)",
        not d0 and P.h16(P.ORIGEN) == P.SHA_F9C, f"{len(m0)} claves, dif {d0[:5]}")
    # (4) N 9 escalada, fundador limpio: las 6 variantes con perillas 0 == 9 FABRICA
    ref = N(P.run(14281, [('C', FAB)] * 9, T=2000, fundador_limpio=1))
    for n in outs:
        m = C.modulo(n)
        with Perillas(m, **APAGADO):
            b = N(P.run(14281, [('C', m)] * 9, T=2000, fundador_limpio=1))
        chk(f"(4) {n} con perillas 0 == 9 FABRICA (N 9, s14281, T 2000, fundador limpio)", b == ref, ref['pista']['rng_mundo_estado'])
    # (5) pieza 2 == APR: solo OPCION = 1 (MODO aprende) == carros/APR.py
    APR = P.carga_carro('APR')
    with Perillas(V3, DESAMB=0, FILTRO=0, OPCION=1):
        b = P.run(14281, [('C', V3)] * 9, T=3000, fundador_limpio=1)
    a = P.run(14281, [('C', APR)] * 9, T=3000, fundador_limpio=1)
    for d in b['linajes']: d['carro'].pop('v143', None)
    chk("(5) pieza 2: V143 con solo OPCION == APR (aprende_barrer) bit a bit (N 9, s14281, T 3000)", N(a) == N(b),
        f"oportunidades APR {sum(sum(d['carro']['apr']['opp_q']) for d in a['linajes'])}")
    # (6) B-5 (DESAMB): difiere de FABRICA y SOLO divide con R == 0 (tabla verdadera, que lee el arnes)
    CF = P.cfg_fabrica(); VAL, EF = CF['VAL_VIVO'], CF['EFECTO']
    V142 = C.modulo('V142')
    r = P.run(14282, [('C', V142)] * 9, T=8000, fundador_limpio=1)
    ev = [e for d in r['linajes'] for e in d['carro']['v143']['des_t']]
    nd = sum(d['carro']['v143']['des_splits'] for d in r['linajes'])
    rf = P.run(14282, [('C', FAB)] * 9, T=8000, fundador_limpio=1)
    chk("(6a) V142 (B-5) difiere de FABRICA y divide por R == 0 (N 9, s14282, T 8000)", nd > 0 and N(r['linajes'][0]['deaths']) is not None and N(r) != N(rf),
        f"divisiones por R==0 {nd}")
    chk("(6b) TODA division B-5 fue en una mordida con efecto 0 en la necesidad activa (tabla verdadera)",
        ev and all(EF[VAL[k]][na] == 0.0 for _, k, na in ev), f"{len(ev)} eventos; letras {sorted({(k, na) for _, k, na in ev})}")
    lit = open(os.path.join(C.RAIZ, 'organismo', 'organismo_v142.py'), encoding='utf-8').read()
    src = outs['V143'].decode('utf-8')
    chk("(6c) la condicion B-5 del carro es la de organismo_v142.py (mismo texto salvo espacios y nombres de perilla)",
        CV.LITERAL_V142[0] in lit and "if (Wb[c] * R < 0 or (DESAMB and R == 0)) and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(KW[c] @ P) and (~activa).any():" in src
        and CV.LITERAL_V142[0].replace(' ', '').replace('desambiguar', 'DESAMB') ==
        "if (Wb[c] * R < 0 or (DESAMB and R == 0)) and abs(float(Wb[c])) > 0.2 and float(kj @ P) > float(KW[c] @ P) and (~activa).any():".replace(' ', ''))
    # (7) FILTRO: se espia actua/_see del carro (sin tocar su conducta) y se verifica la regla
    log = dict(apunta_obst=0, muerde_obst=0, pasos_meta=0, pasos_sin_meta=0, obst_sin_meta=0, sobre_obst=0, n=0)
    def espia(modulo, rel):
        orig_see = modulo.Carro._see; orig_actua = modulo.Carro.actua
        def see(self, pos, objs, t, contar=False):
            best = orig_see(self, pos, objs, t, contar)
            if modulo.FILTRO and self._v3m and best is not None and best[1] in self._v3o: rel['apunta_obst'] += 1
            return best
        def actua(self, obs):
            out = orig_actua(self, obs)
            rel['n'] += 1; m = self._v3m; rel['pasos_meta' if m else 'pasos_sin_meta'] += 1
            if not m and self._v3o: rel['obst_sin_meta'] += 1
            p2 = (obs['pos'] + out['mov']) % self.L
            if m and p2 in obs['objs'] and obs['objs'][p2] in self._v3o:
                rel['sobre_obst'] += 1; rel['muerde_obst'] += int(out['muerde'])
            return out
        modulo.Carro._see = see; modulo.Carro.actua = actua
        return lambda: (setattr(modulo.Carro, '_see', orig_see), setattr(modulo.Carro, 'actua', orig_actua))
    deshaz = espia(V3, log)
    try: rv = P.run(14283, [('C', V3)] * 9, T=6000, fundador_limpio=1)
    finally: deshaz()
    rv2 = P.run(14283, [('C', V3)] * 9, T=6000, fundador_limpio=1)
    chk("(7a) espiar no cambia la conducta (misma corrida con y sin espia)", N(rv) == N(rv2))
    chk("(7b) FILTRO: con meta, las patas NUNCA apuntan a un obstaculo", log['apunta_obst'] == 0 and log['pasos_meta'] > 0, log)
    chk("(7c) FILTRO: con meta, la boca NUNCA muerde un obstaculo (y el cuerpo si pasa por encima de alguno)", log['muerde_obst'] == 0 and log['sobre_obst'] > 0,
        f"sobre obstaculo {log['sobre_obst']}")
    chk("(7d) META = 1: sin meta no hay obstaculos (la limpieza queda posible)", log['obst_sin_meta'] == 0 and log['pasos_sin_meta'] >= 0,
        f"pasos sin meta {log['pasos_sin_meta']}")
    SI = C.modulo('V143_SIEMPRE'); log2 = dict(apunta_obst=0, muerde_obst=0, pasos_meta=0, pasos_sin_meta=0, obst_sin_meta=0, sobre_obst=0, n=0)
    deshaz = espia(SI, log2)
    try: P.run(14283, [('C', SI)] * 9, T=6000, fundador_limpio=1)
    finally: deshaz()
    chk("(7e) SIEMPRE (lesion): hay obstaculos tambien SIN meta; con meta no apunta ni muerde obstaculos", (log2['obst_sin_meta'] > 0 or log2['pasos_sin_meta'] == 0)
        and log2['apunta_obst'] == 0 and log2['muerde_obst'] == 0, log2)
    tv = sum(d['carro']['v143']['todo_obst'] for d in rv['linajes'])
    chk("(7f) V143 (META 1): nunca queda TODO como obstaculo (el respaldo de _see es inerte en el candidato)", tv == 0, f"todo_obst {tv}")
    t1 = time.time()
    with Perillas(V3, CACHE=0):
        rc0 = N(P.run(14285, [('C', V3)] * 9, T=6000, fundador_limpio=1)); s0 = time.time() - t1
    t1 = time.time(); rc1 = N(P.run(14285, [('C', V3)] * 9, T=6000, fundador_limpio=1)); s1 = time.time() - t1
    chk("(7g) CACHE de las dos filas (solo rendimiento, tras el humo) == sin CACHE bit a bit (N 9, s14285, T 6000)", rc0 == rc1,
        f"seg sin cache {s0:.1f} · con cache {s1:.1f}")
    # (8) controles difieren, determinismo
    rs = {n: N(P.run(14284, [('C', C.modulo(n))] * 9, T=3000, fundador_limpio=1)) for n in outs}
    chk("(8a) las 6 variantes son distintas entre si (N 9, s14284, T 3000)", len({json.dumps(v, sort_keys=True) for v in rs.values()}) == 6)
    chk("(8b) determinismo: V143 dos veces igual", rs['V143'] == N(P.run(14284, [('C', V3)] * 9, T=3000, fundador_limpio=1)))
    chk("(8c) INVERTIDO lee la letra pareja (A<->B, C<->D) y el resto es V143", C.modulo('V143_INVERTIDO').INVIERTE == 1 and V3.INVIERTE == 0
        and C.modulo('V143_INVERTIDO').PAREJA == {'A': 'B', 'B': 'A', 'C': 'D', 'D': 'C'})
    # (9) el corredor: aborta ante banderas desconocidas y semillas ajenas; su entrada == juez.tarea
    cor = os.path.join(AQUI, 'corre_v143.py')
    p1 = subprocess.run([sys.executable, cor, '--humo', '--desde', '99999', '--bandera_que_no_existe'], capture_output=True, text=True, timeout=120)
    p2 = subprocess.run([sys.executable, cor, '--humo', '--desde', '99999', '--brazo', 'v143'], capture_output=True, text=True, timeout=120)
    chk("(9a) corre_v143 ABORTA ante banderas desconocidas o abreviadas (ERR-115), sin correr nada", p1.returncode != 0 and p2.returncode != 0
        and 'unrecognized arguments' in p1.stderr and 'unrecognized arguments' in p2.stderr and 'CORRE_V143' not in p1.stdout + p2.stdout,
        f"codigos {p1.returncode}, {p2.returncode}")
    e = [C.valida(True, 14301, 1, 20000, ['v143']), C.valida(False, 14281, 20, 100000, ['v143']), C.valida(False, 14301, 20, 30000, ['v143']),
         C.valida(True, 14281, 1, 20000, ['nuevo']), C.valida(True, 14281, 2, 20000, ['fab', 'v142', 'v143', 'o1']), C.valida(False, 14315, 10, 100000, ['v143'])]
    chk("(9b) corre_v143 rechaza semillas ajenas, T distinta, brazos desconocidos, > 6 corridas de humo y rangos que cruzan serie/replica",
        all(x is not None for x in e) and C.valida(False, 14301, 20, 100000, list(C.SERIE_BRAZOS)) is None
        and C.valida(False, 14321, 20, 100000, list(C.REPLICA_BRAZOS)) is None, e)
    x = C.tarea((14281, 'FABRICA', 2000)); y = J.tarea((14281, ['FABRICA'] * 9, 2000, 1, 0, 1, None, 1))
    chk("(9c) regla 14: corre_v143.tarea == juez.tarea (9 FABRICA, s14281, T 2000, fundador limpio)",
        N(x['linajes']) == N(y['linajes']) and N(x['pista']) == N(y['pista']) and x['R0_pista'] == y['R0_pista'])
    n_ok = sum(OK)
    os.makedirs(C.DATOS_HUMO, exist_ok=True)
    rj = os.path.join(C.DATOS_HUMO, f"identidad_v143_{time.strftime('%Y%m%d_%H%M%S')}.json")
    with open(rj, 'w', encoding='utf-8') as fh:
        json.dump(dict(filas=FILAS, ok=n_ok, total=len(OK), seg=round(time.time() - t0, 1),
                       shas={n: CV.h16b(b) for n, b in outs.items()}), fh, ensure_ascii=False, indent=1)
    print(f"  JSON {rj} (sha {C.h16(rj)}) · {time.time() - t0:.1f}s")
    print(f"RESULTADO: {n_ok}/{len(OK)}")
    return 0 if n_ok == len(OK) else 1


if __name__ == '__main__':
    sys.exit(main())
